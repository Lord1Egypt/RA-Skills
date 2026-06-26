"""
ChartEngine - 数据可视化引擎
支持 Plotly、Matplotlib、Seaborn 三大后端
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from enum import Enum
from typing import Dict, List, Optional, Union, Any


class Theme(Enum):
    LIGHT = 'light'
    DARK = 'dark'
    CORPORATE = 'corporate'


class ChartEngine:
    """数据可视化引擎"""
    
    def __init__(self, backend: str = 'plotly', theme: Theme = Theme.LIGHT):
        self.backend = backend
        self.theme = theme
        self._setup_theme()
    
    def _setup_theme(self):
        """设置主题"""
        if self.backend == 'plotly':
            if self.theme == Theme.DARK:
                self.color_template = 'plotly_dark'
            elif self.theme == Theme.CORPORATE:
                self.color_template = 'plotly_white'
            else:
                self.color_template = 'plotly'
        elif self.backend == 'matplotlib':
            style = 'dark_background' if self.theme == Theme.DARK else 'default'
            plt.style.use(style)
    
    def _to_dataframe(self, data: Union[pd.DataFrame, Dict]) -> pd.DataFrame:
        """转换为 DataFrame"""
        if isinstance(data, dict):
            return pd.DataFrame(data)
        return data
    
    def line_chart(self, data: Union[pd.DataFrame, Dict], x: str, y: str,
                   title: str = '', color: Optional[str] = None,
                   markers: bool = True) -> Union[go.Figure, Any]:
        """折线图"""
        df = self._to_dataframe(data)
        
        if self.backend == 'plotly':
            fig = px.line(df, x=x, y=y, color=color, title=title,
                         markers=markers, template=self.color_template)
            fig.update_layout(showlegend=True)
            return fig
        else:
            plt.figure(figsize=(10, 6))
            if color:
                for name, group in df.groupby(color):
                    plt.plot(group[x], group[y], marker='o', label=name)
                plt.legend()
            else:
                plt.plot(df[x], df[y], marker='o')
            plt.title(title)
            plt.xlabel(x)
            plt.ylabel(y)
            return plt.gcf()
    
    def bar_chart(self, data: Union[pd.DataFrame, Dict], x: str, y: str,
                  title: str = '', color: Optional[str] = None,
                  orientation: str = 'v') -> Union[go.Figure, Any]:
        """柱状图"""
        df = self._to_dataframe(data)
        
        if self.backend == 'plotly':
            fig = px.bar(df, x=x, y=y, color=color, title=title,
                        template=self.color_template, orientation=orientation)
            return fig
        else:
            plt.figure(figsize=(10, 6))
            if orientation == 'h':
                plt.barh(df[x], df[y])
            else:
                plt.bar(df[x], df[y])
            plt.title(title)
            return plt.gcf()
    
    def pie_chart(self, data: Union[pd.DataFrame, Dict], values: str,
                  names: str, title: str = '') -> Union[go.Figure, Any]:
        """饼图"""
        df = self._to_dataframe(data)
        
        if self.backend == 'plotly':
            fig = px.pie(df, values=values, names=names, title=title,
                        template=self.color_template)
            return fig
        else:
            plt.figure(figsize=(8, 8))
            plt.pie(df[values], labels=df[names], autopct='%1.1f%%')
            plt.title(title)
            return plt.gcf()
    
    def scatter_chart(self, data: Union[pd.DataFrame, Dict], x: str, y: str,
                      size: Optional[str] = None, color: Optional[str] = None,
                      title: str = '') -> Union[go.Figure, Any]:
        """散点图"""
        df = self._to_dataframe(data)
        
        if self.backend == 'plotly':
            fig = px.scatter(df, x=x, y=y, size=size, color=color,
                           title=title, template=self.color_template)
            return fig
        else:
            plt.figure(figsize=(10, 6))
            plt.scatter(df[x], df[y], s=df[size] if size else 50)
            plt.title(title)
            plt.xlabel(x)
            plt.ylabel(y)
            return plt.gcf()
    
    def heatmap(self, data: Union[pd.DataFrame, np.ndarray],
                title: str = '', labels: Optional[List[str]] = None) -> Union[go.Figure, Any]:
        """热力图"""
        if isinstance(data, np.ndarray):
            df = pd.DataFrame(data, columns=labels, index=labels)
        else:
            df = data
        
        if self.backend == 'plotly':
            fig = px.imshow(df, title=title, template=self.color_template,
                          aspect='auto')
            return fig
        else:
            plt.figure(figsize=(10, 8))
            sns.heatmap(df, annot=True, cmap='coolwarm')
            plt.title(title)
            return plt.gcf()
    
    def box_chart(self, data: Union[pd.DataFrame, Dict], x: Optional[str] = None,
                  y: Optional[str] = None, title: str = '') -> Union[go.Figure, Any]:
        """箱线图"""
        df = self._to_dataframe(data)
        
        if self.backend == 'plotly':
            fig = px.box(df, x=x, y=y, title=title, template=self.color_template)
            return fig
        else:
            plt.figure(figsize=(10, 6))
            if x:
                df.boxplot(column=y, by=x)
            else:
                plt.boxplot(df[y])
            plt.title(title)
            return plt.gcf()
    
    def histogram(self, data: Union[pd.DataFrame, List], x: Optional[str] = None,
                  bins: int = 20, title: str = '') -> Union[go.Figure, Any]:
        """直方图"""
        if isinstance(data, list):
            df = pd.DataFrame({'value': data})
            x = 'value'
        else:
            df = self._to_dataframe(data)
        
        if self.backend == 'plotly':
            fig = px.histogram(df, x=x, nbins=bins, title=title,
                             template=self.color_template)
            return fig
        else:
            plt.figure(figsize=(10, 6))
            plt.hist(df[x], bins=bins)
            plt.title(title)
            return plt.gcf()
    
    def save(self, fig, path: str, format: Optional[str] = None):
        """保存图表"""
        if self.backend == 'plotly':
            if path.endswith('.html'):
                fig.write_html(path)
            else:
                fig.write_image(path)
        else:
            fig.savefig(path, format=format, bbox_inches='tight')


if __name__ == '__main__':
    # 测试代码
    data = {
        '月份': ['1月', '2月', '3月', '4月', '5月'],
        '销售额': [120, 150, 180, 170, 200],
        '利润': [30, 45, 55, 50, 65]
    }
    
    engine = ChartEngine(backend='plotly')
    fig = engine.line_chart(data, x='月份', y='销售额', title='月度销售趋势')
    fig.write_html('test_chart.html')
    print("图表已保存到 test_chart.html")
