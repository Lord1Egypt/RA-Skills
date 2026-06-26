#!/usr/bin/env python3
"""
Data Visualization Toolkit
数据可视化: 图表生成/导出
"""

import os
import base64
from io import BytesIO
from typing import List, Dict, Any, Optional, Union

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


# 设置中文字体
def setup_chinese_font():
    """设置中文字体"""
    if not MATPLOTLIB_AVAILABLE:
        return
    
    # 尝试查找系统中的中文字体
    font_candidates = [
        'SimHei', 'Microsoft YaHei', 'SimSun', 
        'STHeiti', 'WenQuanYi Micro Hei', 'Noto Sans CJK SC'
    ]
    
    for font in font_candidates:
        font_path = fm.findfont(font)
        if font_path:
            plt.rcParams['font.sans-serif'] = [font]
            break
    
    plt.rcParams['axes.unicode_minus'] = False


class ChartGenerator:
    """图表生成器"""
    
    def __init__(self):
        setup_chinese_font()
        self.fig = None
    
    # ============== 折线图 ==============
    def line_chart(self, data: Union[pd.DataFrame, Dict], 
                   x: str, y: Union[str, List[str]],
                   title: str = '', **kwargs) -> 'ChartGenerator':
        """生成折线图"""
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError('matplotlib not installed')
        
        df = pd.DataFrame(data) if isinstance(data, dict) else data
        
        self.fig, ax = plt.subplots(figsize=kwargs.get('figsize', (10, 6)))
        
        ys = [y] if isinstance(y, str) else y
        for y_col in ys:
            ax.plot(df[x], df[y_col], marker='o', label=y_col)
        
        ax.set_title(title or kwargs.get('title', ''))
        ax.set_xlabel(kwargs.get('xlabel', x))
        ax.set_ylabel(kwargs.get('ylabel', ''))
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        return self
    
    # ============== 柱状图 ==============
    def bar_chart(self, data: Union[pd.DataFrame, Dict],
                  x: str, y: Union[str, List[str]],
                  title: str = '', **kwargs) -> 'ChartGenerator':
        """生成柱状图"""
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError('matplotlib not installed')
        
        df = pd.DataFrame(data) if isinstance(data, dict) else data
        
        self.fig, ax = plt.subplots(figsize=kwargs.get('figsize', (10, 6)))
        
        ys = [y] if isinstance(y, str) else y
        x_pos = range(len(df[x]))
        
        width = kwargs.get('width', 0.35)
        for i, y_col in enumerate(ys):
            offset = (i - len(ys)/2 + 0.5) * width
            ax.bar([p + offset for p in x_pos], df[y_col], width, label=y_col)
        
        ax.set_title(title or kwargs.get('title', ''))
        ax.set_xticks(x_pos)
        ax.set_xticklabels(df[x])
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        return self
    
    # ============== 饼图 ==============
    def pie_chart(self, data: Union[pd.DataFrame, Dict],
                  names: str, values: str,
                  title: str = '', **kwargs) -> 'ChartGenerator':
        """生成饼图"""
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError('matplotlib not available')
        
        df = pd.DataFrame(data) if isinstance(data, dict) else data
        
        self.fig, ax = plt.subplots(figsize=kwargs.get('figsize', (8, 8)))
        
        ax.pie(df[values], labels=df[names], autopct='%1.1f%%', startangle=90)
        ax.set_title(title or kwargs.get('title', ''))
        
        return self
    
    # ============== 散点图 ==============
    def scatter_chart(self, data: Union[pd.DataFrame, Dict],
                      x: str, y: str, size: str = None,
                      color: str = None, title: str = '',
                      **kwargs) -> 'ChartGenerator':
        """生成散点图"""
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError('matplotlib not installed')
        
        df = pd.DataFrame(data) if isinstance(data, dict) else data
        
        self.fig, ax = plt.subplots(figsize=kwargs.get('figsize', (10, 6)))
        
        s = df[size] if size else 50
        c = df[color] if color else None
        
        ax.scatter(df[x], df[y], s=s, c=c, alpha=0.6)
        ax.set_title(title or kwargs.get('title', ''))
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.grid(True, alpha=0.3)
        
        return self
    
    # ============== 保存 ==============
    def save(self, path: str, dpi: int = 100, **kwargs):
        """保存图表"""
        if self.fig:
            self.fig.savefig(path, dpi=dpi, bbox_inches='tight', **kwargs)
            plt.close(self.fig)
            return path
        return None
    
    def to_base64(self, format: str = 'png', dpi: int = 100) -> str:
        """转为Base64"""
        if not self.fig:
            return None
        
        buffer = BytesIO()
        self.fig.savefig(buffer, format=format, dpi=dpi, bbox_inches='tight')
        buffer.seek(0)
        
        return base64.b64encode(buffer.read()).decode()
    
    def show(self):
        """显示图表"""
        if self.fig:
            plt.show()


# ============== Plotly 图表 ==============
class PlotlyChart:
    """Plotly交互式图表"""
    
    @staticmethod
    def line(df: pd.DataFrame, x: str, y: Union[str, List[str]], 
             title: str = '') -> go.Figure:
        """折线图"""
        fig = px.line(df, x=x, y=y, title=title)
        return fig
    
    @staticmethod
    def bar(df: pd.DataFrame, x: str, y: Union[str, List[str]],
            title: str = '', orientation: str = 'v') -> go.Figure:
        """柱状图"""
        fig = px.bar(df, x=x, y=y, title=title, orientation=orientation)
        return fig
    
    @staticmethod
    def scatter(df: pd.DataFrame, x: str, y: str,
                color: str = None, size: str = None,
                title: str = '') -> go.Figure:
        """散点图"""
        fig = px.scatter(df, x=x, y=y, color=color, size=size, title=title)
        return fig
    
    @staticmethod
    def pie(df: pd.DataFrame, names: str, values: str,
            title: str = '') -> go.Figure:
        """饼图"""
        fig = px.pie(df, names=names, values=values, title=title)
        return fig
    
    @staticmethod
    def to_html(fig: go.Figure) -> str:
        """转为HTML"""
        return fig.to_html()
    
    @staticmethod
    def save(fig: go.Figure, path: str, format: str = 'html'):
        """保存图表"""
        if format == 'html':
            fig.write_html(path)
        elif format == 'png':
            fig.write_image(path)
        return path


# ============== 便捷函数 ==============
def quick_chart(data: Union[pd.DataFrame, Dict], 
                chart_type: str, x: str, y: str = None,
                **kwargs) -> ChartGenerator:
    """快速生成图表"""
    generator = ChartGenerator()
    
    if chart_type == 'line':
        return generator.line_chart(data, x, y, **kwargs)
    elif chart_type == 'bar':
        return generator.bar_chart(data, x, y, **kwargs)
    elif chart_type == 'pie':
        return generator.pie_chart(data, x, y, **kwargs)
    elif chart_type == 'scatter':
        return generator.scatter_chart(data, x, y, **kwargs)
    
    raise ValueError(f'Unknown chart type: {chart_type}')


def chart_to_image(data: Union[pd.DataFrame, Dict],
                   chart_type: str, x: str, y: str = None,
                   output_path: str = 'chart.png', **kwargs):
    """快速生成并保存图表"""
    chart = quick_chart(data, chart_type, x, y, **kwargs)
    return chart.save(output_path)


# ==================== 增强图表功能 ====================

def plot_heatmap(data, x_col, y_col, title='', cmap='YlOrRd'):
    """绘制热力图"""
    if not MATPLOTLIB_AVAILABLE:
        return None
    import numpy as np
    import pandas as pd
    if isinstance(data, pd.DataFrame):
        matrix = data.pivot_table(index=y_col, columns=x_col, aggfunc='sum', fill_value=0)
        plt.figure(figsize=(10, 8))
        plt.imshow(matrix.values, cmap=cmap, aspect='auto')
        plt.colorbar()
        plt.title(title)
        return plt.gcf()
    return None


def plot_histogram(data, column, bins=30, title=''):
    """绘制直方图"""
    if not MATPLOTLIB_AVAILABLE:
        return None
    import pandas as pd
    if isinstance(data, pd.DataFrame):
        plt.figure(figsize=(10, 6))
        data[column].hist(bins=bins)
        plt.title(title)
        plt.xlabel(column)
        return plt.gcf()
    return None


def plot_corr_matrix(data, title='Correlation'):
    """绘制相关性矩阵"""
    if not MATPLOTLIB_AVAILABLE:
        return None
    import pandas as pd
    if isinstance(data, pd.DataFrame):
        corr = data.select_dtypes(include=['number']).corr()
        plt.figure(figsize=(10, 8))
        plt.imshow(corr.values, cmap='coolwarm', vmin=-1, vmax=1)
        plt.colorbar()
        plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
        plt.yticks(range(len(corr.columns)), corr.columns)
        plt.title(title)
        return plt.gcf()
    return None


def plot_stacked_bar(data, x_col, y_cols, title=''):
    """绘制堆叠柱状图"""
    if not MATPLOTLIB_AVAILABLE:
        return None
    import pandas as pd
    if isinstance(data, pd.DataFrame):
        plt.figure(figsize=(12, 6))
        data.plot.bar(x=x_col, y=y_cols, stacked=True)
        plt.title(title)
        return plt.gcf()
    return None


def plot_timeline(data, x_col, y_cols, title=''):
    """绘制时间线"""
    if not MATPLOTLIB_AVAILABLE:
        return None
    import pandas as pd
    if isinstance(data, pd.DataFrame):
        plt.figure(figsize=(14, 6))
        for col in y_cols:
            plt.plot(data[x_col], data[col], marker='o', label=col)
        plt.title(title)
        plt.legend()
        plt.grid(True)
        return plt.gcf()
    return None


def plot_gauge(value, title='', max_value=100):
    """绘制仪表盘"""
    if not MATPLOTLIB_AVAILABLE:
        return None
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlim(0, max_value)
    ax.set_ylim(0, 1)
    ax.add_patch(plt.Rectangle((0, 0.3), max_value, 0.4, color='lightgray'))
    ax.add_patch(plt.Rectangle((0, 0.3), value, 0.4, color='green'))
    plt.title(title)
    return fig


def plot_funnel(data, stage_col, value_col, title=''):
    """绘制漏斗图"""
    if not MATPLOTLIB_AVAILABLE:
        return None
    import pandas as pd
    if isinstance(data, pd.DataFrame):
        fig, ax = plt.subplots(figsize=(10, 6))
        y_pos = range(len(data))
        ax.barh(y_pos, data[value_col])
        ax.set_yticks(y_pos)
        ax.set_yticklabels(data[stage_col])
        ax.invert_yaxis()
        plt.title(title)
        return fig
    return None


def plot_wordcloud(text, output_path=None):
    """绘制词云"""
    try:
        from wordcloud import WordCloud
    except ImportError:
        return None
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    if output_path:
        plt.savefig(output_path)
    return plt.gcf()


def plot_map(data, lat_col, lon_col, title='', output_path=None):
    """绘制地图"""
    try:
        import folium
    except ImportError:
        return None
    m = folium.Map(location=[data[lat_col].mean(), data[lon_col].mean()], zoom_start=10)
    for _, row in data.iterrows():
        folium.CircleMarker(location=[row[lat_col], row[lon_col]], radius=5).add_to(m)
    if output_path:
        m.save(output_path)
    return m


def batch_charts(data, output_dir='charts'):
    """批量生成图表"""
    import os
    import pandas as pd
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    results = []
    if isinstance(data, pd.DataFrame):
        for col in data.select_dtypes(include=['number']).columns[:10]:
            try:
                fig = data[col].plot()
                out_path = os.path.join(output_dir, f'{col}.png')
                plt.savefig(out_path)
                results.append(out_path)
            except:
                continue
    return results


def dashboard(data, output_path='dashboard.html'):
    """生成仪表盘"""
    if not PLOTLY_AVAILABLE:
        return None
    import plotly.subplots as tls
    import plotly.graph_objects as go
    import pandas as pd
    if not isinstance(data, pd.DataFrame):
        return None
    fig = tls.make_subplots(rows=2, cols=2, subplot_titles=['Line', 'Bar', 'Pie', 'Stats'])
    numeric_cols = data.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        fig.add_trace(go.Scatter(y=data[numeric_cols[0]], name='Line'), row=1, col=1)
    fig.update_layout(height=800)
    fig.write_html(output_path)
    return output_path


COLOR_SCHEMES = {
    'default': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
    'pastel': ['#f7bfb6', '#b5e3c4', '#c4b5e3', '#e3c4b5'],
    'neon': ['#ff00ff', '#00ffff', '#ff00aa', '#aaff00'],
}


def get_color_scheme(name='default'):
    """获取颜色方案"""
    return COLOR_SCHEMES.get(name, COLOR_SCHEMES['default'])



# ============== 测试 ==============
if __name__ == '__main__':
    print('Data Visualization toolkit loaded')
    print(f'matplotlib: {MATPLOTLIB_AVAILABLE}')
    print(f'plotly: {PLOTLY_AVAILABLE}')
    
    if MATPLOTLIB_AVAILABLE:
        # 测试
        data = {
            'date': ['2026-01', '2026-02', '2026-03', '2026-04'],
            'sales': [100, 150, 130, 180],
            'profit': [20, 35, 25, 40]
        }
        
        chart = ChartGenerator()
        chart.line_chart(data, 'date', ['sales', 'profit'], title='Sales & Profit')
        chart.save('test_chart.png')
        print('Test chart saved to test_chart.png')