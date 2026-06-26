# Data Visualization - 数据可视化仪表盘

> 图表生成/仪表盘制作/实时数据看板/自动报告
> 最后更新：2026-04-13

---

## 功能概述

- 📊 **图表生成**：折线/柱状/饼图/热力图
- 📈 **K线图表**：股票/期货专用图表
- 🖥️ **仪表盘**：多图表组合看板
- 🔄 **实时更新**：数据自动刷新
- 📝 **报告导出**：PDF/HTML/PNG

---

## 图表生成

### 1. Matplotlib基础图表
```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 非交互式后端

# 设置中文
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

def plot_line(data, title, xlabel, ylabel, output='chart.png'):
    """折线图"""
    plt.figure(figsize=(12, 6))
    plt.plot(data['x'], data['y'])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.savefig(output, dpi=100, bbox_inches='tight')
    plt.close()
    return output

def plot_bar(categories, values, title, output='bar.png'):
    """柱状图"""
    plt.figure(figsize=(12, 6))
    plt.bar(categories, values)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output, dpi=100)
    plt.close()
    return output

def plot_pie(sizes, labels, title, output='pie.png'):
    """饼图"""
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title(title)
    plt.savefig(output)
    plt.close()
    return output
```

### 2. K线图表
```python
import mplfinance as mpf

def plot_candlestick(data, title='K线图', output='candle.png'):
    """K线图"""
    # data需要包含: Date, Open, High, Low, Close, Volume
    mpf.plot(
        data.set_index('Date'),
        type='candle',
        title=title,
        style='charles',
        savefig=output
    )
    return output

def plot_volume(data, output='volume.png'):
    """成交量图"""
    mpf.plot(
        data.set_index('Date'),
        type='line',
        volume=True,
        savefig=output
    )
    return output
```

### 3. 热力图
```python
import seaborn as sns
import numpy as np

def plot_heatmap(data, title, output='heatmap.png'):
    """热力图"""
    plt.figure(figsize=(12, 8))
    sns.heatmap(data, annot=True, fmt='.2f', cmap='YlOrRd')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output)
    plt.close()
    return output

def correlation_matrix(df, output='corr.png'):
    """相关系数矩阵"""
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Matrix')
    plt.savefig(output)
    plt.close()
    return output
```

---

## 仪表盘制作

### 1. 多图表组合
```python
from matplotlib.gridspec import GridSpec

def create_dashboard(data, output='dashboard.png'):
    """创建仪表盘"""
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(3, 2, figure=fig)
    
    # 图1：K线
    ax1 = fig.add_subplot(gs[0, :])
    mpf.plot(data['kline'], type='candle', ax=ax1, show=False)
    
    # 图2：成交量
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.bar(data['volume']['date'], data['volume']['vol'])
    ax2.set_title('Volume')
    
    # 图3：资金流
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.plot(data['money_flow'])
    ax3.set_title('Money Flow')
    
    # 图4：收益曲线
    ax4 = fig.add_subplot(gs[2, :])
    ax4.plot(data['equity'])
    ax4.set_title('Equity Curve')
    
    plt.tight_layout()
    plt.savefig(output, dpi=100)
    plt.close()
    return output
```

### 2. 实时看板
```python
import time

class LiveDashboard:
    """实时看板"""
    
    def __init__(self, refresh_interval=60):
        self.refresh_interval = refresh_interval
        self.data_sources = {}
    
    def add_source(self, name, func):
        """添加数据源"""
        self.data_sources[name] = func
    
    def update(self):
        """更新所有数据"""
        results = {}
        for name, func in self.data_sources.items():
            try:
                results[name] = func()
            except Exception as e:
                print(f"Failed to update {name}: {e}")
        return results
    
    def run(self, duration=3600):
        """运行看板"""
        start = time.time()
        while time.time() - start < duration:
            data = self.update()
            self.render(data)
            time.sleep(self.refresh_interval)
```

---

## HTML看板

### 1. Plotly交互图
```python
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_html_dashboard(data):
    """创建HTML仪表盘"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('K线', '成交量', '资金流', '收益曲线')
    )
    
    # K线
    fig.add_trace(
        go.Candlestick(x=data['date'], open=data['open'], 
                      high=data['high'], low=data['low'], close=data['close']),
        row=1, col=1
    )
    
    # 成交量
    fig.add_trace(
        go.Bar(x=data['date'], y=data['volume']),
        row=1, col=2
    )
    
    # 收益曲线
    fig.add_trace(
        go.Scatter(x=data['date'], y=data['equity'], name='Equity'),
        row=2, col=1
    )
    
    fig.update_layout(height=800, showlegend=True)
    
    html = fig.to_html(full_html=False)
    return html
```

### 2. 数据表格
```python
def create_data_table(data, columns, title='数据表'):
    """创建数据表格HTML"""
    html = f'''
    <h3>{title}</h3>
    <table style="width:100%; border-collapse: collapse;">
        <tr style="background:#f0f0f0;">
            {"".join([f"<th>{c}</th>" for c in columns])}
        </tr>
    '''
    
    for row in data:
        html += '<tr>' + "".join([f"<td>{v}</td>" for v in row]) + '</tr>'
    
    html += '</table>'
    return html
```

---

## 核心命令

### 1. 生成图表
```
命令：生成图表 [类型] [数据]

示例：
- 生成图表 折线图 [1,2,3,4,5]
- 生成图表 柱状图 苹果:100,香蕉:80
```

### 2. 生成K线
```
命令：生成K线 [股票代码]

示例：
- 生成K线 600519
```

### 3. 生成报告
```
命令：生成报告 [报告名称]

示例：
- 生成报告 每日看板
- 生成报告 股票分析
```

---

## 应用场景

### 1. 股票分析报告
```python
def stock_report(code):
    """生成股票报告"""
    # 获取数据
    data = get_stock_data(code)
    
    # 生成图表
    chart1 = plot_candlestick(data['kline'], f'{code} K线')
    chart2 = plot_bar(data['volume']['date'], data['volume']['vol'], '成交量')
    
    # 生成HTML报告
    html = f'''
    <html>
    <head><title>{code} 分析报告</title></head>
    <body>
        <h1>{code} 分析报告</h1>
        <img src="{chart1}">
        <img src="{chart2}">
    </body>
    </html>
    '''
    
    with open(f'{code}_report.html', 'w') as f:
        f.write(html)
    
    return f'{code}_report.html'
```

### 2. 策略回测报告
```python
def backtest_report(results):
    """生成回测报告"""
    # 收益曲线
    equity_chart = plot_line({
        'x': results['dates'],
        'y': results['equity']
    }, '收益曲线', '日期', '资金')
    
    # 统计
    stats = calculate_stats(results)
    
    html = f'''
    <html>
    <body>
        <h1>策略回测报告</h1>
        <img src="{equity_chart}">
        <h2>统计数据</h2>
        <ul>
            <li>总收益率: {stats['total_return']:.2f}%</li>
            <li>年化收益: {stats['annual_return']:.2f}%</li>
            <li>夏普比率: {stats['sharpe']:.2f}</li>
            <li>最大回撤: {stats['max_drawdown']:.2f}%</li>
        </ul>
    </body>
    </html>
    '''
    
    return html
```

---

## 图表类型选择

| 场景 | 推荐图表 |
|------|---------|
| 趋势变化 | 折线图 |
| 对比分析 | 柱状图 |
| 占比分布 | 饼图/环形图 |
| 相关性 | 热力图/散点图 |
| K线走势 | 蜡烛图 |
| 分布情况 | 直方图/箱线图 |
| 地理数据 | 地图热力图 |

---

## 注意事项

1. **数据量**：大数据集要采样
2. **中文显示**：配置中文字体
3. **交互性**：需要交互用Plotly
4. **导出格式**：PNG清晰/HTML交互


## Code Implementation

Python实现: chart_generator.py

`python
from chart_generator import ChartGenerator, quick_chart

# 快速图表
chart = quick_chart(data, 'line', 'date', ['sales', 'profit'])
chart.save('chart.png')

# 或使用完整API
gen = ChartGenerator()
gen.line_chart(data, 'date', 'sales', title='Sales')
gen.bar_chart(data, 'category', 'value')
gen.pie_chart(data, 'name', 'value')
gen.scatter_chart(data, 'x', 'y', size='size', color='category')
`
