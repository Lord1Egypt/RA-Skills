"""
图表生成器 - Chart Generator
支持多种图表类型：折线图、柱状图、饼图、散点图、热力图
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Union, List, Dict, Any


class ChartGenerator:
    """图表生成器类"""
    
    THEMES = {
        'corporate': {'primary': '#1f77b4', 'secondary': '#ff7f0e', 'bg': '#ffffff'},
        'dark': {'primary': '#2ca02c', 'secondary': '#d62728', 'bg': '#1a1a1a'},
        'colorful': {'primary': '#9467bd', 'secondary': '#8c564b', 'bg': '#f0f0f0'}
    }
    
    def __init__(self, theme: str = 'corporate'):
        """
        初始化图表生成器
        
        Args:
            theme: 主题名称 ('corporate', 'dark', 'colorful')
        """
        self.theme = self.THEMES.get(theme, self.THEMES['corporate'])
        self.color_sequence = px.colors.qualitative.Plotly
    
    def line_chart(self, data: Union[pd.DataFrame, Dict], x: str, y: Union[str, List[str]], 
                   title: str = "", **kwargs) -> go.Figure:
        """生成折线图"""
        if isinstance(data, dict):
            data = pd.DataFrame(data)
        
        fig = px.line(data, x=x, y=y, title=title, 
                      color_discrete_sequence=self.color_sequence,
                      **kwargs)
        fig.update_layout(template='plotly_white')
        return fig
    
    def bar_chart(self, data: Union[pd.DataFrame, Dict], x: str, y: str,
                  title: str = "", orientation: str = 'v', **kwargs) -> go.Figure:
        """生成柱状图"""
        if isinstance(data, dict):
            data = pd.DataFrame(data)
        
        if orientation == 'h':
            fig = px.bar(data, y=x, x=y, title=title, orientation='h', **kwargs)
        else:
            fig = px.bar(data, x=x, y=y, title=title, **kwargs)
        fig.update_layout(template='plotly_white')
        return fig
    
    def pie_chart(self, data: Union[pd.DataFrame, Dict], names: str, values: str,
                  title: str = "", **kwargs) -> go.Figure:
        """生成饼图"""
        if isinstance(data, dict):
            data = pd.DataFrame(data)
        
        fig = px.pie(data, names=names, values=values, title=title, **kwargs)
        return fig
    
    def scatter_chart(self, data: Union[pd.DataFrame, Dict], x: str, y: str,
                      color: str = None, size: str = None, title: str = "", **kwargs) -> go.Figure:
        """生成散点图"""
        if isinstance(data, dict):
            data = pd.DataFrame(data)
        
        fig = px.scatter(data, x=x, y=y, color=color, size=size, title=title, **kwargs)
        fig.update_layout(template='plotly_white')
        return fig
    
    def heatmap(self, data: Union[pd.DataFrame, List[List]], 
                title: str = "", labels: Dict = None, **kwargs) -> go.Figure:
        """生成热力图"""
        if isinstance(data, list):
            data = pd.DataFrame(data)
        
        fig = px.imshow(data, title=title, labels=labels, **kwargs)
        return fig
    
    def export_static(self, fig: go.Figure, filepath: str, width: int = 800, height: int = 600):
        """导出静态图片"""
        fig.write_image(filepath, width=width, height=height)
