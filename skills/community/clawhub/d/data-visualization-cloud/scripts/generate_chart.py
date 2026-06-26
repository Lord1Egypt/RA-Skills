#!/usr/bin/env python3
"""
数据可视化图表生成脚本 - AI智能分析版本
使用Plotly生成精美、专业的数据可视化仪表板
支持多种图表类型，根据数据特征智能选择最佳可视化方案
"""

import argparse
import os
import sys
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime


def read_data(input_file):
    """
    读取输入数据文件，支持CSV和Excel格式
    
    Args:
        input_file: 输入文件路径
    
    Returns:
        pandas DataFrame
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"输入文件不存在: {input_file}")
    
    file_ext = os.path.splitext(input_file)[1].lower()
    
    if file_ext == '.csv':
        df = pd.read_csv(input_file)
    elif file_ext in ['.xlsx', '.xls']:
        df = pd.read_excel(input_file)
    else:
        raise ValueError(f"不支持的文件格式: {file_ext}")
    
    return df


def analyze_data_characteristics(df):
    """
    分析数据特征，为图表选择提供依据
    
    Args:
        df: pandas DataFrame
    
    Returns:
        dict: 数据特征字典
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime']).columns.tolist()
    
    # 尝试识别日期列
    for col in df.columns:
        if col not in datetime_cols:
            try:
                pd.to_datetime(df[col])
                if col not in categorical_cols:
                    datetime_cols.append(col)
            except:
                pass
    
    characteristics = {
        'total_rows': len(df),
        'total_cols': len(df.columns),
        'numeric_cols': numeric_cols,
        'numeric_count': len(numeric_cols),
        'categorical_cols': categorical_cols,
        'categorical_count': len(categorical_cols),
        'datetime_cols': datetime_cols,
        'datetime_count': len(datetime_cols),
        'numeric_stats': {},
        'categorical_stats': {},
        'correlations': None
    }
    
    # 数值列统计
    for col in numeric_cols:
        characteristics['numeric_stats'][col] = {
            'mean': df[col].mean(),
            'median': df[col].median(),
            'std': df[col].std(),
            'min': df[col].min(),
            'max': df[col].max(),
            'skewness': df[col].skew(),
            'unique_count': df[col].nunique(),
            'missing_rate': df[col].isna().sum() / len(df)
        }
    
    # 分类列统计
    for col in categorical_cols:
        characteristics['categorical_stats'][col] = {
            'unique_count': df[col].nunique(),
            'mode': df[col].mode().iloc[0] if len(df[col].mode()) > 0 else None,
            'missing_rate': df[col].isna().sum() / len(df)
        }
    
    # 相关性分析
    if len(numeric_cols) >= 2:
        try:
            correlations = df[numeric_cols].corr()
            characteristics['correlations'] = correlations
        except:
            pass
    
    return characteristics


def recommend_charts(characteristics):
    """
    根据数据特征智能推荐图表类型
    
    Args:
        characteristics: 数据特征字典
    
    Returns:
        list: 推荐的图表列表
    """
    recommended = []
    
    numeric_cols = characteristics['numeric_cols']
    categorical_cols = characteristics['categorical_cols']
    datetime_cols = characteristics['datetime_cols']
    numeric_count = characteristics['numeric_count']
    categorical_count = characteristics['categorical_count']
    
    # 1. 数据概览表格（总是包含）
    recommended.append({
        'type': 'table',
        'title': '数据概览',
        'priority': 10
    })
    
    # 2. 数值列分布分析
    if numeric_count > 0:
        for col in numeric_cols:
            stats = characteristics['numeric_stats'].get(col, {})
            unique_count = stats.get('unique_count', 0)
            
            # 根据唯一值数量选择分布图类型
            if unique_count <= 10:
                # 少量唯一值：使用柱状图
                recommended.append({
                    'type': 'value_counts_bar',
                    'col': col,
                    'title': f'{col}分布',
                    'priority': 8
                })
            else:
                # 大量唯一值：使用直方图
                recommended.append({
                    'type': 'histogram',
                    'col': col,
                    'title': f'{col}分布',
                    'priority': 8
                })
                
                # 如果数据量大且有偏态，添加箱线图
                if characteristics['total_rows'] >= 10:
                    recommended.append({
                        'type': 'box_single',
                        'col': col,
                        'title': f'{col}箱线图',
                        'priority': 6
                    })
    
    # 3. 分类数据分析
    if categorical_count > 0 and numeric_count > 0:
        for cat_col in categorical_cols[:2]:  # 最多取前2个分类列
            cat_stats = characteristics['categorical_stats'].get(cat_col, {})
            unique_count = cat_stats.get('unique_count', 0)
            
            # 只处理合理数量的分类
            if 2 <= unique_count <= 15:
                # 柱状图对比
                for num_col in numeric_cols[:2]:  # 最多取前2个数值列
                    recommended.append({
                        'type': 'grouped_bar',
                        'cat_col': cat_col,
                        'num_col': num_col,
                        'title': f'{num_col}按{cat_col}',
                        'priority': 9
                    })
                    
                    # 饼图（分类数量适中）
                    if unique_count <= 8:
                        recommended.append({
                            'type': 'pie',
                            'cat_col': cat_col,
                            'num_col': num_col,
                            'title': f'{num_col}占比',
                            'priority': 7
                        })
                    
                    # 箱线图（展示分布差异）
                    if characteristics['total_rows'] >= 10:
                        recommended.append({
                            'type': 'box_grouped',
                            'cat_col': cat_col,
                            'num_col': num_col,
                            'title': f'{num_col}分布差异',
                            'priority': 7
                        })
                    
                    # 小提琴图（更详细的分布展示）
                    if unique_count <= 6 and characteristics['total_rows'] >= 20:
                        recommended.append({
                            'type': 'violin',
                            'cat_col': cat_col,
                            'num_col': num_col,
                            'title': f'{num_col}分布密度',
                            'priority': 5
                        })
    
    # 4. 时间序列分析
    if len(datetime_cols) > 0 and numeric_count > 0:
        for dt_col in datetime_cols[:1]:
            for num_col in numeric_cols[:2]:
                recommended.append({
                    'type': 'line',
                    'x_col': dt_col,
                    'y_col': num_col,
                    'title': f'{num_col}趋势',
                    'priority': 9
                })
                
                # 面积图
                recommended.append({
                    'type': 'area',
                    'x_col': dt_col,
                    'y_col': num_col,
                    'title': f'{num_col}面积图',
                    'priority': 6
                })
    
    # 5. 相关性分析
    if numeric_count >= 2:
        # 散点图矩阵（取前几个重要数值列）
        main_numeric_cols = numeric_cols[:min(4, numeric_count)]
        for i in range(len(main_numeric_cols)):
            for j in range(i+1, len(main_numeric_cols)):
                x_col = main_numeric_cols[i]
                y_col = main_numeric_cols[j]
                
                # 检查相关性强度
                if characteristics['correlations'] is not None:
                    corr_value = abs(characteristics['correlations'].loc[x_col, y_col])
                    priority = 8 if corr_value > 0.3 else 5
                else:
                    priority = 6
                
                recommended.append({
                    'type': 'scatter',
                    'x_col': x_col,
                    'y_col': y_col,
                    'title': f'{x_col} vs {y_col}',
                    'priority': priority
                })
        
        # 相关性热力图
        if numeric_count >= 3:
            recommended.append({
                'type': 'heatmap',
                'cols': numeric_cols,
                'title': '相关性热力图',
                'priority': 7
            })
    
    # 6. 多变量分析
    if numeric_count >= 3:
        # 平行坐标图
        recommended.append({
            'type': 'parallel_coordinates',
            'cols': numeric_cols[:5],
            'title': '多维度分析',
            'priority': 5
        })
    
    # 7. 分类列之间的关系
    if categorical_count >= 2:
        for i in range(min(2, categorical_count)):
            for j in range(i+1, min(3, categorical_count)):
                recommended.append({
                    'type': 'sunburst',
                    'cat_cols': [categorical_cols[i], categorical_cols[j]],
                    'num_col': numeric_cols[0] if numeric_count > 0 else None,
                    'title': '层级分析',
                    'priority': 4
                })
    
    # 按优先级排序
    recommended.sort(key=lambda x: x['priority'], reverse=True)
    
    # 限制图表数量（最多15个）
    return recommended[:15]


def create_metric_card(title, value, change=None, icon="📊", color="#667eea"):
    """
    创建指标卡片
    
    Args:
        title: 标题
        value: 数值
        change: 变化值
        icon: 图标
        color: 颜色
    
    Returns:
        HTML字符串
    """
    change_html = ""
    if change is not None:
        change_color = "#10b981" if change >= 0 else "#ef4444"
        change_icon = "↑" if change >= 0 else "↓"
        change_html = f'<div style="color: {change_color}; font-size: 14px; margin-top: 8px;"><span style="font-weight: bold;">{change_icon} {abs(change):.1f}%</span> vs 上期</div>'
    
    return f"""
    <div style="background: linear-gradient(135deg, {color} 0%, {color}dd 100%); 
                border-radius: 16px; 
                padding: 24px; 
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                color: white;">
        <div style="font-size: 32px; margin-bottom: 8px;">{icon}</div>
        <div style="font-size: 14px; opacity: 0.9; margin-bottom: 4px;">{title}</div>
        <div style="font-size: 32px; font-weight: bold; margin-bottom: 4px;">{value}</div>
        {change_html}
    </div>
    """


def generate_unified_dashboard(df, output_file="visualization_dashboard.html"):
    """
    生成精美、专业的数据可视化仪表板
    
    Args:
        df: pandas DataFrame
        output_file: 输出文件路径
    """
    # 分析数据特征
    characteristics = analyze_data_characteristics(df)
    
    # 智能推荐图表
    recommended_charts = recommend_charts(characteristics)
    
    numeric_cols = characteristics['numeric_cols']
    categorical_cols = characteristics['categorical_cols']
    
    # 专业配色方案
    color_list = [
        '#6366F1', '#8B5CF6', '#EC4899', '#F59E0B', 
        '#10B981', '#3B82F6', '#14B8A6', '#EF4444',
        '#F97316', '#84CC16', '#06B6D4', '#A855F7'
    ]
    
    # 创建指标卡片HTML
    metrics_html = ""
    metrics_html += create_metric_card("总数据量", f"{characteristics['total_rows']:,}", icon="📈", color="#6366F1")
    
    if characteristics['numeric_count'] > 0:
        avg_value = df[numeric_cols[0]].mean()
        metrics_html += create_metric_card(f"{numeric_cols[0]}平均值", f"{avg_value:,.0f}", icon="📊", color="#8B5CF6")
    
    if characteristics['categorical_count'] > 0 and characteristics['numeric_count'] > 0:
        max_cat = df[categorical_cols[0]].value_counts().idxmax()
        metrics_html += create_metric_card(f"最常见{categorical_cols[0]}", f"{max_cat}", icon="🏷️", color="#10B981")
    
    if characteristics['numeric_count'] > 0:
        total_sum = df[numeric_cols[0]].sum()
        metrics_html += create_metric_card(f"{numeric_cols[0]}总计", f"{total_sum:,.0f}", icon="💰", color="#F59E0B")
    
    # 构建图表列表（根据推荐生成）
    chart_list = []
    
    for chart_info in recommended_charts:
        chart_type = chart_info['type']
        
        if chart_type == 'table':
            chart_list.append({
                'title': f'📋 {chart_info["title"]}',
                'type': 'table',
                'full_width': True
            })
        
        elif chart_type == 'histogram':
            chart_list.append({
                'title': f'📊 {chart_info["title"]}',
                'type': 'histogram',
                'col': chart_info['col']
            })
        
        elif chart_type == 'value_counts_bar':
            chart_list.append({
                'title': f'📊 {chart_info["title"]}',
                'type': 'value_counts_bar',
                'col': chart_info['col']
            })
        
        elif chart_type == 'box_single':
            chart_list.append({
                'title': f'📦 {chart_info["title"]}',
                'type': 'box_single',
                'col': chart_info['col']
            })
        
        elif chart_type == 'grouped_bar':
            chart_list.append({
                'title': f'📈 {chart_info["title"]}',
                'type': 'grouped_bar',
                'cat_col': chart_info['cat_col'],
                'num_col': chart_info['num_col']
            })
        
        elif chart_type == 'pie':
            chart_list.append({
                'title': f'🥧 {chart_info["title"]}',
                'type': 'pie',
                'cat_col': chart_info['cat_col'],
                'num_col': chart_info['num_col']
            })
        
        elif chart_type == 'box_grouped':
            chart_list.append({
                'title': f'📦 {chart_info["title"]}',
                'type': 'box_grouped',
                'cat_col': chart_info['cat_col'],
                'num_col': chart_info['num_col']
            })
        
        elif chart_type == 'violin':
            chart_list.append({
                'title': f'🎻 {chart_info["title"]}',
                'type': 'violin',
                'cat_col': chart_info['cat_col'],
                'num_col': chart_info['num_col']
            })
        
        elif chart_type == 'line':
            chart_list.append({
                'title': f'📉 {chart_info["title"]}',
                'type': 'line',
                'x_col': chart_info['x_col'],
                'y_col': chart_info['y_col']
            })
        
        elif chart_type == 'area':
            chart_list.append({
                'title': f'🏔️ {chart_info["title"]}',
                'type': 'area',
                'x_col': chart_info['x_col'],
                'y_col': chart_info['y_col']
            })
        
        elif chart_type == 'scatter':
            chart_list.append({
                'title': f'🔵 {chart_info["title"]}',
                'type': 'scatter',
                'x_col': chart_info['x_col'],
                'y_col': chart_info['y_col']
            })
        
        elif chart_type == 'heatmap':
            chart_list.append({
                'title': f'🌡️ {chart_info["title"]}',
                'type': 'heatmap',
                'cols': chart_info['cols'],
                'full_width': True
            })
        
        elif chart_type == 'parallel_coordinates':
            chart_list.append({
                'title': f'🧭 {chart_info["title"]}',
                'type': 'parallel_coordinates',
                'cols': chart_info['cols'],
                'full_width': True
            })
        
        elif chart_type == 'sunburst':
            chart_list.append({
                'title': f'☀️ {chart_info["title"]}',
                'type': 'sunburst',
                'cat_cols': chart_info['cat_cols'],
                'num_col': chart_info['num_col']
            })
    
    # 创建子图布局
    n_charts = len(chart_list)
    cols = 2
    
    subplot_titles = []
    specs = []
    
    i = 0
    while i < n_charts:
        chart = chart_list[i]
        
        if chart.get('full_width'):
            subplot_titles.append(chart['title'])
            specs.append([{"type": "domain" if chart['type'] in ['pie', 'sunburst'] else "table" if chart['type'] == 'table' else "xy", "colspan": 2}, None])
            i += 1
        else:
            subplot_titles.append(chart['title'])
            
            if i + 1 < n_charts:
                next_chart = chart_list[i + 1]
                subplot_titles.append(next_chart['title'])
                
                # 判断图表类型
                def get_trace_type(chart_type):
                    if chart_type in ['pie', 'sunburst']:
                        return "domain"
                    elif chart_type == 'heatmap':
                        return "xy"
                    else:
                        return "xy"
                
                type1 = get_trace_type(chart['type'])
                type2 = get_trace_type(next_chart['type'])
                
                specs.append([{"type": type1}, {"type": type2}])
                i += 2
            else:
                type1 = get_trace_type(chart['type'])
                specs.append([{"type": type1}, {"type": "xy"}])
                i += 1
    
    rows = len(specs)
    
    # 创建子图
    fig = make_subplots(
        rows=rows, cols=cols,
        subplot_titles=subplot_titles,
        specs=specs,
        vertical_spacing=0.08,
        horizontal_spacing=0.10
    )
    
    # 添加图表
    current_row = 1
    current_col = 1
    color_idx = 0
    
    # 定义位置推进函数
    def advance_position():
        nonlocal current_row, current_col, color_idx
        if current_col == 2:
            current_col = 1
            current_row += 1
        else:
            current_col = 2
        color_idx += 1
    
    for chart in chart_list:
        chart_type = chart['type']
        
        if chart_type == 'table':
            # 数据表格
            fig.add_trace(
                go.Table(
                    columnwidth=[200] + [150] * (len(df.columns) - 1),
                    header=dict(
                        values=[f"<b>{col}</b>" for col in df.columns],
                        fill_color=color_list[color_idx % len(color_list)],
                        font=dict(color='white', size=14, family='Arial'),
                        align='center',
                        height=45,
                        line=dict(color='white', width=2)
                    ),
                    cells=dict(
                        values=[df[col] for col in df.columns],
                        fill_color=[['#F8FAFC', '#EEF2FF'] * (len(df) // 2 + 1)],
                        font=dict(color='#1E293B', size=13, family='Arial'),
                        align='center',
                        height=38,
                        line=dict(color='#E2E8F0', width=1)
                    )
                ),
                row=current_row, col=1
            )
            current_row += 1
        
        elif chart_type == 'histogram':
            # 直方图
            fig.add_trace(
                go.Histogram(
                    x=df[chart['col']],
                    name=chart['col'],
                    marker_color=color_list[color_idx % len(color_list)],
                    opacity=0.8,
                    marker_line=dict(color='white', width=2),
                    hovertemplate=f'<b>{chart["col"]}:</b> %{{x}}<br><b>频数:</b> %{{y}}<extra></extra>'
                ),
                row=current_row, col=current_col
            )
            advance_position()
        
        elif chart_type == 'value_counts_bar':
            # 值计数柱状图
            value_counts = df[chart['col']].value_counts()
            fig.add_trace(
                go.Bar(
                    x=value_counts.index.astype(str),
                    y=value_counts.values,
                    name=chart['col'],
                    marker_color=color_list[color_idx % len(color_list)],
                    opacity=0.9,
                    marker_line=dict(color='white', width=2),
                    text=value_counts.values,
                    textposition='outside',
                    hovertemplate=f'<b>{chart["col"]}:</b> %{{x}}<br><b>数量:</b> %{{y}}<extra></extra>'
                ),
                row=current_row, col=current_col
            )
            advance_position()
        
        elif chart_type == 'box_single':
            # 单变量箱线图
            fig.add_trace(
                go.Box(
                    y=df[chart['col']],
                    name=chart['col'],
                    marker_color=color_list[color_idx % len(color_list)],
                    boxmean='sd',
                    marker=dict(size=5),
                    line=dict(width=2)
                ),
                row=current_row, col=current_col
            )
            advance_position()
        
        elif chart_type == 'grouped_bar':
            # 分组柱状图
            grouped = df.groupby(chart['cat_col'])[chart['num_col']].sum().reset_index()
            fig.add_trace(
                go.Bar(
                    x=grouped[chart['cat_col']],
                    y=grouped[chart['num_col']],
                    name=chart['num_col'],
                    marker_color=color_list[color_idx % len(color_list)],
                    opacity=0.9,
                    marker_line=dict(color='white', width=2),
                    text=[f'{v:,.0f}' for v in grouped[chart['num_col']]],
                    textposition='outside',
                    textfont=dict(size=11),
                    hovertemplate=f'<b>{chart["cat_col"]}:</b> %{{x}}<br><b>{chart["num_col"]}:</b> %{{y:,.0f}}<extra></extra>'
                ),
                row=current_row, col=current_col
            )
            advance_position()
        
        elif chart_type == 'pie':
            # 饼图
            grouped = df.groupby(chart['cat_col'])[chart['num_col']].sum().reset_index()
            fig.add_trace(
                go.Pie(
                    labels=grouped[chart['cat_col']],
                    values=grouped[chart['num_col']],
                    hole=0.6,
                    marker_colors=color_list[:len(grouped)],
                    textinfo='percent+label',
                    textposition='outside',
                    textfont=dict(size=13),
                    hovertemplate='<b>%{label}</b><br>数值: %{value:,.0f}<br>占比: %{percent}<extra></extra>',
                    pull=[0.08 if i == 0 else 0.02 for i in range(len(grouped))],
                    marker=dict(line=dict(color='white', width=3)),
                    rotation=45
                ),
                row=current_row, col=current_col
            )
            advance_position()
        
        elif chart_type == 'box_grouped':
            # 分组箱线图
            fig.add_trace(
                go.Box(
                    x=df[chart['cat_col']],
                    y=df[chart['num_col']],
                    name=chart['num_col'],
                    marker_color=color_list[color_idx % len(color_list)],
                    boxmean='sd',
                    boxpoints='outliers',
                    marker=dict(size=6),
                    line=dict(width=3),
                    opacity=0.7
                ),
                row=current_row, col=current_col
            )
            advance_position()
        
        elif chart_type == 'violin':
            # 小提琴图
            fig.add_trace(
                go.Violin(
                    x=df[chart['cat_col']],
                    y=df[chart['num_col']],
                    name=chart['num_col'],
                    box_visible=True,
                    meanline_visible=True,
                    fillcolor=color_list[color_idx % len(color_list)],
                    opacity=0.6,
                    marker=dict(size=3)
                ),
                row=current_row, col=current_col
            )
            advance_position()
        
        elif chart_type == 'line':
            # 折线图
            x_data = df[chart['x_col']] if chart['x_col'] in df.columns else list(range(len(df)))
            fig.add_trace(
                go.Scatter(
                    x=x_data,
                    y=df[chart['y_col']],
                    mode='lines+markers',
                    name=chart['y_col'],
                    line=dict(
                        color=color_list[color_idx % len(color_list)],
                        width=3,
                        shape='spline',
                        smoothing=1.3
                    ),
                    marker=dict(size=8, color='white', line=dict(color=color_list[color_idx % len(color_list)], width=2)),
                    hovertemplate=f'<b>{chart["y_col"]}:</b> %{{y:,.0f}}<extra></extra>'
                ),
                row=current_row, col=current_col
            )
            advance_position()
        
        elif chart_type == 'area':
            # 面积图
            x_data = df[chart['x_col']] if chart['x_col'] in df.columns else list(range(len(df)))
            fig.add_trace(
                go.Scatter(
                    x=x_data,
                    y=df[chart['y_col']],
                    mode='lines',
                    name=chart['y_col'],
                    fill='tozeroy',
                    fillcolor=f'rgba(99, 102, 241, 0.2)',
                    line=dict(color=color_list[color_idx % len(color_list)], width=3),
                    hovertemplate=f'<b>{chart["y_col"]}:</b> %{{y:,.0f}}<extra></extra>'
                ),
                row=current_row, col=current_col
            )
            advance_position()
        
        elif chart_type == 'scatter':
            # 散点图
            fig.add_trace(
                go.Scatter(
                    x=df[chart['x_col']],
                    y=df[chart['y_col']],
                    mode='markers',
                    name=f'{chart["x_col"]} vs {chart["y_col"]}',
                    marker=dict(
                        color=color_list[color_idx % len(color_list)],
                        size=12,
                        opacity=0.6,
                        line=dict(color='white', width=2)
                    ),
                    hovertemplate=f'<b>{chart["x_col"]}:</b> %{{x:,.0f}}<br><b>{chart["y_col"]}:</b> %{{y:,.0f}}<extra></extra>'
                ),
                row=current_row, col=current_col
            )
            advance_position()
        
        elif chart_type == 'heatmap':
            # 相关性热力图
            if characteristics['correlations'] is not None:
                corr = characteristics['correlations']
                fig.add_trace(
                    go.Heatmap(
                        z=corr.values,
                        x=corr.columns,
                        y=corr.index,
                        colorscale='RdBu',
                        zmid=0,
                        text=[[f'{val:.2f}' for val in row] for row in corr.values],
                        texttemplate='%{text}',
                        textfont=dict(size=10),
                        hovertemplate='%{x} vs %{y}: %{z:.3f}<extra></extra>',
                        colorbar=dict(title='相关系数', len=0.8)
                    ),
                    row=current_row, col=1
                )
            current_row += 1
        
        elif chart_type == 'parallel_coordinates':
            # 平行坐标图
            dimensions = []
            for col in chart['cols']:
                dimensions.append(dict(
                    label=col,
                    values=df[col]
                ))
            
            fig.add_trace(
                go.Parcoords(
                    line=dict(
                        color=df[chart['cols'][0]],
                        colorscale='Viridis',
                        showscale=True
                    ),
                    dimensions=dimensions
                ),
                row=current_row, col=1
            )
            current_row += 1
        
        elif chart_type == 'sunburst':
            # 旭日图
            if chart['num_col']:
                path = chart['cat_cols'] + [chart['num_col']]
                fig.add_trace(
                    go.Sunburst(
                        labels=df[chart['cat_cols'][0]],
                        parents=[''] * len(df),
                        values=df[chart['num_col']] if chart['num_col'] else None,
                        marker_colors=color_list[:len(df)],
                        hovertemplate='<b>%{label}</b><br>数值: %{value}<extra></extra>'
                    ),
                    row=current_row, col=current_col
                )
            advance_position()
    
    # 更新布局
    fig.update_layout(
        height=420 * rows,
        title=dict(text="", x=0.5, xanchor='center'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#FFFFFF',
        showlegend=False,
        hovermode='closest',
        margin=dict(l=70, r=70, t=30, b=70),
        font=dict(family='Arial', size=13)
    )
    
    # 更新坐标轴样式
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#F1F5F9',
        linecolor='#CBD5E1',
        linewidth=2,
        ticks='outside',
        tickwidth=2,
        ticklen=6,
        tickfont=dict(size=12, family='Arial', color='#475569'),
        title_font=dict(size=14, family='Arial', color='#1E293B'),
        title_standoff=15,
        mirror=False
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#F1F5F9',
        linecolor='#CBD5E1',
        linewidth=2,
        ticks='outside',
        tickwidth=2,
        ticklen=6,
        tickfont=dict(size=12, family='Arial', color='#475569'),
        title_font=dict(size=14, family='Arial', color='#1E293B'),
        title_standoff=15,
        mirror=False
    )
    
    # 更新子图标题样式
    fig.update_annotations(font=dict(size=16, family='Arial', color='#1E293B'), borderpad=10)
    
    # 生成图表HTML
    plotly_html = fig.to_html(
        include_plotlyjs='cdn', 
        full_html=False,
        config={
            'displayModeBar': False,
            'displaylogo': False,
            'scrollZoom': True,
            'editable': False
        }
    )
    
    # 完整HTML模板
    html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数据可视化仪表板</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 30px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 36px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 12px;
        }}
        
        .header .subtitle {{
            color: #64748B;
            font-size: 16px;
        }}
        
        .header .timestamp {{
            color: #94A3B8;
            font-size: 14px;
            margin-top: 8px;
        }}
        
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .metric-card {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 28px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.5);
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        }}
        
        .charts {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}
        
        .footer {{
            text-align: center;
            padding: 30px;
            color: rgba(255, 255, 255, 0.9);
            font-size: 14px;
        }}
        
        @media (max-width: 1024px) {{
            body {{
                padding: 20px 15px;
            }}
            .header {{
                padding: 30px 20px;
            }}
            .header h1 {{
                font-size: 28px;
            }}
            .metrics {{
                grid-template-columns: repeat(2, 1fr);
            }}
            .charts {{
                padding: 20px;
            }}
        }}
        
        @media (max-width: 768px) {{
            .metrics {{
                grid-template-columns: 1fr;
            }}
            .header h1 {{
                font-size: 24px;
            }}
        }}
        
        html {{
            scroll-behavior: smooth;
        }}
        
        @keyframes fadeIn {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .header, .metrics, .charts {{
            animation: fadeIn 0.6s ease-out;
        }}
        
        .plotly-graph-div {{
            margin: 15px auto !important;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 智能数据可视化仪表板</h1>
            <div class="subtitle">
                <span>AI驱动的数据分析与可视化</span>
            </div>
            <div class="timestamp">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>
        
        <div class="metrics">
            {metrics_html}
        </div>
        
        <div class="charts">
            {plotly_html}
        </div>
        
        <div class="footer">
            <p>💡 AI智能数据可视化 · 自动选择最佳图表类型</p>
        </div>
    </div>
</body>
</html>
    """
    
    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)


def generate_auto_charts(df, output_dir="auto_charts"):
    """
    自动生成图表
    
    Args:
        df: pandas DataFrame
        output_dir: 输出目录
    
    Returns:
        生成的图表文件列表
    """
    os.makedirs(output_dir, exist_ok=True)
    
    dashboard_file = os.path.join(output_dir, "visualization_dashboard.html")
    generate_unified_dashboard(df, output_file=dashboard_file)
    
    return [dashboard_file]


def main():
    parser = argparse.ArgumentParser(description='数据可视化图表生成工具 - AI智能分析版本')
    parser.add_argument('--input', '-i', required=True, help='输入数据文件路径 (CSV或Excel)')
    parser.add_argument('--output', '-o', default='visualization_dashboard.html', help='输出文件路径')
    parser.add_argument('--output-dir', help='输出目录')
    
    args = parser.parse_args()
    
    try:
        # 读取数据
        df = read_data(args.input)
        print(f"✅ 成功读取数据，共 {len(df)} 行，{len(df.columns)} 列")
        print(f"📋 列名: {list(df.columns)}")
        
        # 分析数据特征
        print(f"\n🔍 正在分析数据特征...")
        characteristics = analyze_data_characteristics(df)
        print(f"   - 数值列: {characteristics['numeric_count']} 个")
        print(f"   - 分类列: {characteristics['categorical_count']} 个")
        print(f"   - 日期列: {characteristics['datetime_count']} 个")
        
        # 智能推荐图表
        print(f"\n🤖 AI正在推荐最佳图表组合...")
        recommended = recommend_charts(characteristics)
        print(f"   推荐了 {len(recommended)} 种图表类型:")
        
        chart_type_names = {
            'table': '数据表格',
            'histogram': '直方图',
            'value_counts_bar': '值计数柱状图',
            'box_single': '箱线图',
            'grouped_bar': '分组柱状图',
            'pie': '饼图',
            'box_grouped': '分组箱线图',
            'violin': '小提琴图',
            'line': '折线图',
            'area': '面积图',
            'scatter': '散点图',
            'heatmap': '热力图',
            'parallel_coordinates': '平行坐标图',
            'sunburst': '旭日图'
        }
        
        for chart in recommended:
            chart_name = chart_type_names.get(chart['type'], chart['type'])
            print(f"   - {chart_name} (优先级: {chart['priority']})")
        
        # 生成仪表板
        output_file = args.output
        generate_unified_dashboard(df, output_file)
        
        print(f"\n✨ AI智能可视化仪表板已成功生成!")
        print(f"📁 文件路径: {output_file}")
        print(f"\n💡 提示: 图表类型由AI根据数据特征自动选择")
    
    except Exception as e:
        print(f"❌ 错误: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
