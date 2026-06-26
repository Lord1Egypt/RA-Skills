#!/usr/bin/env python3
"""Chart Enhanced - 图表增强功能"""

import os


def plot_3d_surface(data, x_col, y_col, z_col, title=''):
    """3D表面图"""
    try:
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        import pandas as pd
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        if isinstance(data, pd.DataFrame):
            surf = ax.plot_surface(
                data[x_col].values.reshape(-1, 1),
                data[y_col].values.reshape(1, -1),
                data[z_col].values.reshape(*data[x_col].shape),
                cmap='viridis'
            )
        
        ax.set_title(title)
        return fig
    except ImportError:
        return None


def plot_3d_scatter(data, x_col, y_col, z_col, title=''):
    """3D散点图"""
    try:
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        import pandas as pd
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        if isinstance(data, pd.DataFrame):
            ax.scatter(data[x_col], data[y_col], data[z_col], c='blue', s=50)
        
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_zlabel(z_col)
        ax.set_title(title)
        return fig
    except ImportError:
        return None


def plot_3d_bar(data, x_col, y_col, z_col, title=''):
    """3D柱状图"""
    try:
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        import pandas as pd
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        if isinstance(data, pd.DataFrame):
            ax.bar3d(data[x_col], data[y_col], data[z_col], dx=0.5, dy=0.5, dz=data[z_col])
        
        ax.set_title(title)
        return fig
    except ImportError:
        return None


def plot_animated_line(data, x_col, y_cols, title='', interval=50):
    """动画折线图"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib.animation as animation
        import pandas as pd
        
        fig, ax = plt.subplots()
        lines = []
        
        if isinstance(data, pd.DataFrame):
            for col in y_cols:
                line, = ax.plot([], [], label=col)
                lines.append(line)
        
        ax.set_xlim(data[x_col].min(), data[x_col].max())
        ax.set_ylim(data[y_cols].min() * 0.9, data[y_cols].max() * 1.1)
        ax.legend()
        ax.set_title(title)
        
        def update(frame):
            for i, col in enumerate(y_cols):
                lines[i].set_data(data[x_col][:frame], data[col][:frame])
            return lines
        
        ani = animation.FuncAnimation(fig, update, frames=len(data), interval=interval, blit=True)
        return fig
    except ImportError:
        return None


def plot_amap(data, lat_col, lon_col, title='', zoom_start=10):
    """高德地图"""
    try:
        import amap
    except ImportError:
        return None


def plot_bmap(data, lat_col, lon_col, title='', zoom=10):
    """百度地图"""
    try:
        import bmap
    except ImportError:
        return None


def plot_folium_heatmap(data, lat_col, lon_col, title='', radius=10):
    """folium热力图"""
    try:
        import folium
        from folium.plugins import HeatMap
        
        center = [data[lat_col].mean(), data[lon_col].mean()]
        m = folium.Map(location=center, zoom_start=10)
        
        heat_data = [[row[lat_col], row[lon_col]] for _, row in data.iterrows()]
        HeatMap(heat_data, radius=radius).add_to(m)
        
        return m
    except ImportError:
        return None


def plot_folium_marker(data, lat_col, lon_col, popups=None, title=''):
    """folium标记"""
    try:
        import folium
        
        center = [data[lat_col].mean(), data[lon_col].mean()]
        m = folium.Map(location=center, zoom_start=10)
        
        for idx, row in data.iterrows():
            folium.Marker(
                location=[row[lat_col], row[lon_col]],
                popup=str(row[popups]) if popups else f"Point {idx}"
            ).add_to(m)
        
        return m
    except ImportError:
        return None


def create_dashboard_grid(rows, cols, titles=None):
    """创建网格仪表盘"""
    try:
        import matplotlib.pyplot as plt
        from matplotlib.gridspec import GridSpec
        
        fig = plt.figure(figsize=(cols * 6, rows * 4))
        gs = GridSpec(rows, cols, figure=fig)
        
        axes = []
        for i in range(rows):
            for j in range(cols):
                ax = fig.add_subplot(gs[i, j])
                axes.append(ax)
        
        if titles:
            for ax, title in zip(axes, titles):
                ax.set_title(title)
        
        return fig, axes
    except ImportError:
        return None


def plot_gantt(data, start_col, end_col, task_col, title=''):
    """甘特图"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        import pandas as pd
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if isinstance(data, pd.DataFrame):
            for i, (_, row) in enumerate(data.iterrows()):
                ax.barh(i, 
                      (row[end_col] - row[start_col]).days,
                      left=row[start_col],
                      height=0.5)
                ax.text(row[start_col], i, row[task_col], va='center')
        
        ax.set_yticks(range(len(data)))
        ax.set_yticklabels(data[task_col])
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.set_title(title)
        plt.xticks(rotation=45)
        return fig
    except ImportError:
        return None


def plot_sankey(source, target, value, title=''):
    """桑基图"""
    try:
        import plotly.graph_objects as go
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(pad=15, thickness=20, label=source),
            link=dict(source=source, target=target, value=value)
        )])
        fig.update_layout(title=title)
        return fig
    except ImportError:
        return None


def plot_treemap(data, labels, values, title=''):
    """树图"""
    try:
        import plotly.graph_objects as go
        
        fig = go.Figure(go.Treemap(labels=labels, values=values))
        fig.update_layout(title=title)
        return fig
    except ImportError:
        return None


def plot_sunburst(data, labels, parents, values, title=''):
    """旭日图"""
    try:
        import plotly.graph_objects as go
        
        fig = go.Figure(go.Sunburst(labels=labels, parents=parents, values=values))
        fig.update_layout(title=title)
        return fig
    except ImportError:
        return None


if __name__ == "__main__":
    print("Chart Enhanced loaded")