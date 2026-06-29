# Python scatter for deliverables (from report correlation type, env=deliverables)
# Use Plotly for interactive HTML export. Restrained: single accent, warm paper, short labels.
import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    'X (Complexity)': [1,2,3,4,5],
    'Y (Density)': [2,3,5,4,6],
    'Size (Restraint)': [10,20,15,25,30],
    'Label': ['V1.1', 'V1.2', 'V2.1', 'V2.2', 'V3.1']
})

fig = px.scatter(df, x='X (Complexity)', y='Y (Density)', size='Size (Restraint)', color_discrete_sequence=['#002FA7'],
                 title='Correlation: Complexity vs Density (restrained)', text='Label')

fig.update_layout(
    plot_bgcolor='#f5f0eb',
    paper_bgcolor='#f5f0eb',
    font_color='#1B365D',
    showlegend=False
)

fig.write_html('scatter-correlation.html')
print('Generated scatter for final deliverable. Open HTML.')
