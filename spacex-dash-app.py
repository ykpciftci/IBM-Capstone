import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options = [
                                                    {'label':'All Sites','value':'ALL'},
                                                    {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                                    {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                                                    {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                                    {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'}
                                             ],
                                                value = 'ALL',
                                                placeholder = 'Select a Launch Site Here',
                                                searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min = 0, max = 10000, step = 1000, value = [min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id = 'success-pie-chart',component_property = 'figure'),
             Input(component_id = 'site-dropdown',component_property = 'value'))
def get_pie_chart(entered_site):
        if entered_site == 'ALL':
            data = spacex_df.groupby('Launch Site')['class'].agg(class_sum ='sum').reset_index()
            fig = px.pie(data, values='class_sum', names='Launch Site', title='Total Success Launches by Site')
            return fig
        else:
            df = spacex_df[spacex_df['Launch Site'] == entered_site].value_counts('class').reset_index(name='launches')
            fig = px.pie(df, values='launches', names='class', title= f'Total Success Launches for site {entered_site}')
            return fig
            
    
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
             [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter(entered_site, pay_range):
    if entered_site == 'ALL':
        data = spacex_df[(spacex_df['Payload Mass (kg)'] >=pay_range[0]) &(spacex_df['Payload Mass (kg)']<=pay_range[1])]
        fig = px.scatter(data, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category')
        return fig
    else:
        df = spacex_df[(spacex_df['Launch Site'] == entered_site) &
                       (spacex_df['Payload Mass (kg)'] >= pay_range[0]) &
                       (spacex_df['Payload Mass (kg)'] <= pay_range[1])]
        fig = px.scatter(df, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category')
        return fig
# Run the app
if __name__ == '__main__':
    app.run()
