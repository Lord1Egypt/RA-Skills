"""
Data Viz Suite - 基本使用示例
"""

import pandas as pd
import numpy as np
import sys
import os

# 添加脚本路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from chart_engine import ChartEngine, Theme
from dashboard import Dashboard
from report_generator import ReportGenerator


def demo_charts():
    """演示各种图表"""
    print("=" * 50)
    print("图表生成示例")
    print("=" * 50)
    
    # 准备数据
    sales_data = {
        '月份': ['1月', '2月', '3月', '4月', '5月', '6月'],
        '销售额': [120, 150, 180, 170, 200, 220],
        '利润': [30, 45, 55, 50, 65, 70]
    }
    
    # 初始化引擎
    engine = ChartEngine(backend='plotly', theme=Theme.LIGHT)
    
    # 折线图
    print("\n1. 生成折线图...")
    fig = engine.line_chart(sales_data, x='月份', y='销售额', 
                           title='月度销售趋势', markers=True)
    fig.write_html('/tmp/demo_line.html')
    print("   已保存: /tmp/demo_line.html")
    
    # 柱状图
    print("\n2. 生成柱状图...")
    product_data = {
        '产品': ['产品A', '产品B', '产品C', '产品D'],
        '销量': [350, 280, 420, 310]
    }
    fig = engine.bar_chart(product_data, x='产品', y='销量', 
                          title='产品销量对比')
    fig.write_html('/tmp/demo_bar.html')
    print("   已保存: /tmp/demo_bar.html")
    
    # 饼图
    print("\n3. 生成饼图...")
    region_data = {
        '区域': ['华东', '华南', '华北', '西南', '其他'],
        '占比': [35, 25, 20, 12, 8]
    }
    fig = engine.pie_chart(region_data, values='占比', names='区域',
                          title='销售区域分布')
    fig.write_html('/tmp/demo_pie.html')
    print("   已保存: /tmp/demo_pie.html")
    
    # 散点图
    print("\n4. 生成散点图...")
    np.random.seed(42)
    scatter_data = {
        '广告投入': np.random.randint(10, 100, 50),
        '销售额': np.random.randint(50, 500, 50),
        '客户数': np.random.randint(100, 1000, 50)
    }
    fig = engine.scatter_chart(scatter_data, x='广告投入', y='销售额',
                              size='客户数', title='广告投入 vs 销售额')
    fig.write_html('/tmp/demo_scatter.html')
    print("   已保存: /tmp/demo_scatter.html")


def demo_dashboard():
    """演示仪表盘"""
    print("\n" + "=" * 50)
    print("仪表盘示例")
    print("=" * 50)
    
    # 准备数据
    sales_data = {
        '月份': ['1月', '2月', '3月', '4月', '5月', '6月'],
        '销售额': [120, 150, 180, 170, 200, 220]
    }
    
    user_data = {
        '渠道': ['搜索', '社交媒体', '邮件', '直接访问'],
        '新增用户': [1200, 800, 500, 1500]
    }
    
    # 创建仪表盘
    dash = Dashboard(title='业务数据监控大屏', theme='dark')
    
    # 添加KPI
    print("\n添加 KPI 指标...")
    dash.add_kpi('总销售额', 1250000, change=12.5, prefix='¥')
    dash.add_kpi('新增用户', 54321, change=-2.3)
    dash.add_kpi('订单数', 3421, change=8.1)
    dash.add_kpi('转化率', 3.24, change=0.5, suffix='%')
    
    # 添加图表
    print("添加图表...")
    engine = ChartEngine(backend='plotly')
    fig1 = engine.line_chart(sales_data, x='月份', y='销售额', title='销售趋势')
    fig2 = engine.bar_chart(user_data, x='渠道', y='新增用户', title='用户来源')
    
    dash.add_chart('sales', fig1, '月度销售趋势')
    dash.add_chart('users', fig2, '用户来源分布')
    
    # 保存
    dash.save('/tmp/demo_dashboard.html')
    print("\n仪表盘已保存: /tmp/demo_dashboard.html")


def demo_report():
    """演示报表生成"""
    print("\n" + "=" * 50)
    print("报表生成示例")
    print("=" * 50)
    
    # 准备数据
    df = pd.DataFrame({
        '产品': ['产品A', '产品B', '产品C', '产品D', '产品E'],
        '销量': [1200, 980, 1500, 800, 1100],
        '销售额': [120000, 98000, 150000, 80000, 110000],
        '增长率': [12.5, -2.3, 18.2, 5.1, 8.7]
    })
    
    # 创建报表
    print("\n生成 HTML 报表...")
    report = ReportGenerator(title='季度销售报表')
    report.add_section('概览', text='本季度销售业绩良好，总销售额同比增长15%。')
    report.add_table('销售明细', df)
    report.export('/tmp/demo_report.html')
    print("   已保存: /tmp/demo_report.html")


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print(" Data Viz Suite - 数据可视化套件示例 ")
    print("=" * 60)
    
    demo_charts()
    demo_dashboard()
    demo_report()
    
    print("\n" + "=" * 60)
    print("所有示例已完成！")
    print("=" * 60)
