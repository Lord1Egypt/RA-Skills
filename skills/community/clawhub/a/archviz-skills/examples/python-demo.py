"""archviz-skills Python Demo — Plotly scatter + line (restrained)"""
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=[1,2,3,4,5,6,7,8,9,10],
    y=[2,5,8,12,18,22,28,35,42,50],
    mode='lines+markers',
    name='Growth',
    line=dict(color='#002FA7', width=2),
    marker=dict(size=8, color='#002FA7')
))
fig.add_trace(go.Scatter(
    x=[1,2,3,4,5,6,7,8,9,10],
    y=[1,3,6,10,15,20,26,32,38,45],
    mode='lines+markers',
    name='Baseline',
    line=dict(color='#a8a29e', width=1, dash='dash'),
    marker=dict(size=6, color='#a8a29e')
))
fig.update_layout(
    title='Growth vs Baseline',
    paper_bgcolor='#f5f0eb',
    plot_bgcolor='#f5f0eb',
    font=dict(family='system-ui', color='#44403c', size=13),
    xaxis=dict(title='Week', gridcolor='#d6d3d1'),
    yaxis=dict(title='Value', gridcolor='#d6d3d1'),
    legend=dict(x=0.02, y=0.98)
)
fig.write_html('scatter-demo.html')
print('Saved: scatter-demo.html')
