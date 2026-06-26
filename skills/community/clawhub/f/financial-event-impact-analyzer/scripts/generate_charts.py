#!/usr/bin/env python3
"""
Generate charts for financial event impact analysis.
Creates dual-axis time series comparison charts with Chinese labels.
每类受影响资产单独生成一张时序对比图。
"""

import argparse
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from typing import Dict, List, Tuple
import os
import warnings

warnings.filterwarnings('ignore')

# === 中文字体配置 ===
# 字体优先级列表（skill.json 中约定的顺序）
FONT_PRIORITY = [
    'WenQuanYi Micro Hei',  # Linux 常用（优先，已安装）
    'WenQuanYi Zen Hei',    # Linux 文泉驿正黑
    'SimHei',               # Windows 黑体
    'Noto Sans CJK SC',     # 现代 Linux
    'PingFang SC',          # macOS
    'Heiti SC',             # macOS
    'Microsoft YaHei',      # Windows 微软雅黑
    'Source Han Sans CN',   # 思源黑体
]
FALLBACK_FONT = 'DejaVu Sans'


def check_chinese_font_available() -> Tuple[bool, str, str]:
    """
    前置检查：验证中文字体是否可用
    
    Returns:
        (is_available, selected_font, message)
    """
    import matplotlib.font_manager as fm
    
    # 强制重建字体缓存（确保识别系统字体）
    fm._load_fontmanager(try_read_cache=False)
    
    # 查找可用字体
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    # 按优先级选择
    for font in FONT_PRIORITY:
        if font in available_fonts:
            return True, font, f"✓ 中文字体可用: {font}"
    
    # 检查是否有任何包含 CJK 的字体
    cjk_fonts = [f for f in available_fonts if any(kw in f for kw in ['CJK', 'Hei', 'Noto', 'WenQuanYi', 'Chinese', 'PingFang', 'Hiragino'])]
    
    if cjk_fonts:
        return True, cjk_fonts[0], f"✓ 找到备选CJK字体: {cjk_fonts[0]}"
    
    # 无中文字体
    return False, FALLBACK_FONT, f"❌ 未找到中文字体，图表将显示方框。请安装: sudo apt install fonts-wqy-microhei fonts-noto-cjk"


def setup_chinese_font() -> str:
    """
    配置中文字体，必须在生成图表前调用
    
    Returns:
        使用的字体名称
    """
    is_available, selected_font, message = check_chinese_font_available()
    print(message)
    
    if is_available:
        plt.rcParams['font.family'] = selected_font
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    else:
        # 使用回退字体，但图表中文会显示异常
        plt.rcParams['font.family'] = FALLBACK_FONT
        plt.rcParams['axes.unicode_minus'] = False
        print("⚠ 严重警告: 图表中文标注将显示为方框！")
    
    return selected_font


# 初始化字体
setup_chinese_font()

# 图表样式设置
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (16, 9)
plt.rcParams['figure.dpi'] = 150
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 12


def load_indicator_data(filepath: str) -> pd.DataFrame:
    """Load indicator data from CSV or JSON."""
    if filepath.endswith('.json'):
        with open(filepath, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data['data'])
    else:
        df = pd.read_csv(filepath)
    
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    return df


def calculate_date_range_months(df: pd.DataFrame) -> int:
    """计算数据跨度（月数）"""
    date_range = df['date'].max() - df['date'].min()
    return int(date_range.days / 30)


def auto_adjust_x_axis_interval(ax, df: pd.DataFrame) -> int:
    """
    根据数据跨度自动调整X轴时间刻度间隔，避免标签重叠
    
    Returns:
        间隔月数
    """
    months = calculate_date_range_months(df)
    
    # 根据数据跨度自动调整间隔
    if months <= 12:
        interval = 1  # 每月
    elif months <= 24:
        interval = 3  # 每季度
    elif months <= 60:
        interval = 6  # 半年
    elif months <= 120:
        interval = 12  # 每年
    else:
        interval = 24  # 每两年
    
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval))
    return interval


def plot_dual_axis_comparison(
    primary_df: pd.DataFrame, 
    primary_name: str,
    related_df: pd.DataFrame, 
    related_name: str,
    events: List[Dict],
    output_path: str,
    current_event: Dict = None,
    event_results: List[Dict] = None
) -> str:
    """
    绘制双Y轴时序对比图：表征指标（左轴）vs 关联资产指标（右轴）
    
    ⭐ 核心改动：
    - 过往同类事件时间区间红色虚线方框，**覆盖整个Y轴区域**（从底部到顶部）
    - 每一项相关指标都必须生成单独的图表
    - X轴自动调整间隔避免重叠
    - 每个事件区间添加事件编号和涨跌幅标注
    
    Args:
        primary_df: 表征指标数据
        primary_name: 表征指标中文名称
        related_df: 关联资产数据
        related_name: 关联资产中文名称
        events: 历史事件列表
        output_path: 输出文件路径
        current_event: 当前事件
        event_results: 事件结果数据
    
    Returns:
        保存的文件路径
    """
    # 根据数据跨度调整图表宽度，避免标签重叠
    months = calculate_date_range_months(primary_df)
    if months <= 24:
        fig_width = 14
    elif months <= 60:
        fig_width = 18
    elif months <= 120:
        fig_width = 22
    else:
        fig_width = 26  # 长时间跨度使用更宽的图表
    
    fig, ax1 = plt.subplots(figsize=(fig_width, 10))
    
    # 左Y轴：表征指标
    color_primary = '#E74C3C'  # 红色
    ax1.plot(primary_df['date'], primary_df['close'], 
             linewidth=2, color=color_primary, label=primary_name)
    ax1.set_xlabel('日期', fontsize=12)
    ax1.set_ylabel(primary_name, fontsize=12, color=color_primary)
    ax1.tick_params(axis='y', labelcolor=color_primary)
    
    # 右Y轴：关联资产指标
    ax2 = ax1.twinx()
    color_related = '#3498DB'  # 蓝色
    ax2.plot(related_df['date'], related_df['close'], 
             linewidth=2, color=color_related, label=related_name)
    ax2.set_ylabel(related_name, fontsize=12, color=color_related)
    ax2.tick_params(axis='y', labelcolor=color_related)
    
    # ⭐ 核心改动：在绘制所有曲线后，强制确定Y轴范围
    ax1.relim()
    ax1.autoscale_view(scalex=False, scaley=True)
    ax2.relim()
    ax2.autoscale_view(scalex=False, scaley=True)
    
    # === 添加历史事件红色虚线方框（覆盖整个Y轴区域） ===
    # 最多显示5个历史事件，避免图表过于拥挤
    max_events_to_show = min(5, len(events))
    
    # 使用不同颜色深度区分不同事件
    event_colors = ['#C0392B', '#A93226', '#922B21', '#7B241C', '#641E16']
    
    # ⭐ 核心修改：使用 ax.get_xaxis_transform() 让矩形覆盖整个Y轴区域
    # Y坐标从 0（底部）到 1（顶部），覆盖整个图表区域
    
    for i, event in enumerate(events[:max_events_to_show]):
        start_date = pd.to_datetime(event['start_date'])
        end_date = pd.to_datetime(event['end_date'])
        
        # ⭐ 核心修改：使用 axes coordinates，Y从0到1覆盖整个图表区域
        rect = plt.Rectangle(
            (mdates.date2num(start_date), 0),  # Y=0（底部）
            mdates.date2num(end_date) - mdates.date2num(start_date),
            1,  # Y高度=1（从底部到顶部，覆盖整个Y轴）
            fill=True, facecolor=event_colors[i % len(event_colors)] + '15',  # 15%透明度填充
            edgecolor=event_colors[i % len(event_colors)], linestyle='--',
            linewidth=2.5, alpha=0.8,
            transform=ax1.get_xaxis_transform(),  # ⭐ 关键：X轴数据坐标，Y轴axes坐标
            clip_on=False  # 允许超出轴边界
        )
        ax1.add_patch(rect)
        
        # 添加事件标签（显示事件编号 + 主指标涨跌幅）
        primary_change = event.get('change_pct', 0)
        change_str = f"+{primary_change}%" if primary_change > 0 else f"{primary_change}%"
        
        # 标签位置：在矩形框上方中央（使用 axes coordinates）
        mid_date = start_date + (end_date - start_date) / 2
        ax1.annotate(
            f"事件{i+1} [{change_str}]",
            xy=(mdates.date2num(mid_date), 1.05),  # Y=1.05（稍超出顶部）
            fontsize=11, color=event_colors[i % len(event_colors)], 
            weight='bold', alpha=0.9,
            ha='center', va='bottom',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                      edgecolor=event_colors[i % len(event_colors)], alpha=0.7),
            clip_on=False
        )
    
    # === 标记当前事件（红色实线框，覆盖整个Y轴区域） ===
    if current_event:
        curr_start = pd.to_datetime(current_event.get('start_date', 
                              primary_df['date'].iloc[-90].strftime('%Y-%m-%d')))
        curr_end = pd.to_datetime(current_event.get('current_date', 
                              primary_df['date'].iloc[-1].strftime('%Y-%m-%d')))
        
        # ⭐ 核心修改：实线框使用 axes coordinates 覆盖整个Y轴高度
        rect = plt.Rectangle(
            (mdates.date2num(curr_start), 0),  # Y=0（底部）
            mdates.date2num(curr_end) - mdates.date2num(curr_start),
            1,  # Y高度=1（覆盖整个Y轴）
            fill=True, facecolor='#E74C3C' + '25',  # 25%透明度填充
            edgecolor='#E74C3C', linestyle='-',
            linewidth=3.5, alpha=1.0,
            transform=ax1.get_xaxis_transform(),  # ⭐ 关键：X轴数据坐标，Y轴axes坐标
            clip_on=False
        )
        ax1.add_patch(rect)
        
        # 当前事件标签（使用 axes coordinates）
        ax1.annotate(
            "当前事件",
            xy=(mdates.date2num(curr_end), 1.05),  # Y=1.05（稍超出顶部）
            fontsize=13, color='#E74C3C', weight='bold',
            ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                      edgecolor='#E74C3C', linewidth=2, alpha=0.9),
            clip_on=False
        )
    
    # === 自动调整X轴间隔，避免标签重叠 ===
    interval = auto_adjust_x_axis_interval(ax1, primary_df)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y.%m'))
    
    # 旋转标签并调整位置，避免重叠
    plt.xticks(rotation=30, ha='right')
    
    # 设置标题（中文）
    ax1.set_title(f'{primary_name} vs {related_name} 历史走势对比', 
                  fontsize=16, weight='bold', pad=20)
    
    # 合并图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    
    # 添加事件区间图例说明
    event_legend_text = "红色虚线框 = 历史事件区间"
    ax1.legend(lines1 + lines2, labels1 + labels2 + [event_legend_text], 
               loc='upper left', fontsize=10, framealpha=0.9)
    
    ax1.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"已生成: {output_path}")
    return output_path


def plot_all_dual_axis_charts(
    primary_indicator: str,
    primary_data_path: str,
    related_data_path: str,
    performance_data_path: str,
    output_dir: str,
    indicator_names: Dict[str, str] = None
) -> Dict[str, str]:
    """
    为每类相关资产生成单独的双Y轴时序对比图
    
    新增功能：
    - 传入 event_results 用于显示关联资产涨跌幅
    
    Returns:
        图表类型到文件路径的映射
    """
    charts = {}
    
    # 默认指标中文名称映射
    default_names = {
        # 大宗商品
        'brent_crude': '布伦特原油',
        'wti_crude': 'WTI原油',
        'gold': '黄金',
        'silver': '白银',
        'copper': '铜',
        'aluminum': '铝',
        'natural_gas': '天然气',
        # 美股指数
        'sp500': '标普500',
        'nasdaq': '纳斯达克',
        'dow_jones': '道琼斯',
        'russell2000': '罗素2000',
        'vix': 'VIX恐慌指数',
        # 美股行业ETF
        'xlk': '科技ETF',
        'xle': '能源ETF',
        'xlf': '金融ETF',
        'xlv': '医疗ETF',
        'xli': '工业ETF',
        'jets': '航空ETF',
        'iyr': '房地产ETF',
        'gdx': '黄金矿业ETF',
        'tlt': '长期美债ETF',
        'xlp': '必需消费ETF',
        'xlu': '公用事业ETF',
        # 外汇
        'usd_index': '美元指数',
        'usd_cny': '美元/人民币',
        'usd_jpy': '美元/日元',
        'usd_krw': '美元/韩元',
        'eur_usd': '欧元/美元',
        'gbp_usd': '英镑/美元',
        'usd_hkd': '美元/港币',
        # 美债
        'us_10y_treasury': '10年期美债收益率',
        'us_2y_treasury': '2年期美债收益率',
        # ⭐ 中国市场（新增）
        'csi300': '沪深300',
        'sse_composite': '上证指数',
        'chinext': '创业板指',
        'sse50': '上证50',
        'csi500': '中证500',
        'csi1000': '中证1000',
        'shanghai_tech': '科创50',
        'hsi': '恒生指数',
        'hsi_tech': '恒生科技',
        'hang_seng_china': '恒生中国企业',
        # 中国宏观
        'cpi_china': '中国CPI',
        'ppi_china': '中国PPI',
        'gdp_china': '中国GDP',
        'm2_china': '中国M2',
        'm1_china': '中国M1',
        'social_financing': '社会融资规模',
        'pmi_china': '中国PMI',
        'loan_rate_china': '中国LPR',
        'bond_10y_china': '中国10Y国债收益率',
        # ⭐ 日本市场（新增）
        'nikkei225': '日经225',
        'topix': 'TOPIX东证指数',
        'japan_10y_bond': '日本10Y国债',
        'gdp_japan': '日本GDP',
        'cpi_japan': '日本CPI',
        'm2_japan': '日本M2',
        # ⭐ 韩国市场（新增）
        'kospi': '韩国KOSPI',
        'kosdaq': '韩国KOSDAQ',
        'gdp_korea': '韩国GDP',
        'cpi_korea': '韩国CPI',
        # ⭐ 欧洲市场（新增）
        'eu_stoxx50': '欧洲斯托克50',
        'dax': '德国DAX',
        'cac40': '法国CAC40',
        'ftse100': '英国富时100',
        'ftse_mib': '意大利MIB',
        'ibex35': '西班牙IBEX35',
        'euro_10y_bond': '德国10Y国债',
        'gdp_eurozone': '欧元区GDP',
        'cpi_eurozone': '欧元区CPI',
        'm2_eurozone': '欧元区M2',
        # ⭐ 亚太新兴市场（新增）
        'sgx_nifty': '印度Nifty50',
        'sensex': '印度BSE Sensex',
        'jakarta': '雅加达指数',
        'bangkok': '泰国SET指数',
        # 美国宏观
        'fed_funds_rate': '联邦基金利率',
        'cpi_us': '美国CPI',
        'gdp_us': '美国GDP',
        'unemployment_us': '美国失业率',
    }
    
    names = indicator_names or default_names
    
    # 加载主指标数据
    primary_df = load_indicator_data(primary_data_path)
    primary_name = names.get(primary_indicator, primary_indicator)
    
    # 加载相关资产数据
    with open(related_data_path, 'r') as f:
        related_data = json.load(f)
    
    # 加载表现数据（获取事件列表和事件结果）
    with open(performance_data_path, 'r') as f:
        perf_data = json.load(f)
    
    events = perf_data.get('events', [])
    current_event = perf_data.get('current_event', {})
    event_results = perf_data.get('event_results', [])
    
    # 如果 perf_data 中没有 events，从 events.json 加载
    if not events and perf_data.get('primary_indicator'):
        # 尝试从同目录下的 events.json 加载
        events_path = f"{output_dir}/../events.json"
        if os.path.exists(events_path):
            with open(events_path, 'r') as f:
                events_data = json.load(f)
            events = events_data.get('similar_events', [])
            current_event = events_data.get('current_event', {})
    
    # 收集所有相关指标
    all_related = []
    for category in ['benefited', 'harmed', 'neutral_uncertain']:
        for asset in related_data.get(category, []):
            if 'indicator' in asset:
                all_related.append({
                    'indicator': asset['indicator'],
                    'category': category,
                    'reason': asset.get('reason', '')
                })
    
    print(f"\n正在生成 {len(all_related)} 张双Y轴时序对比图...")
    print(f"  主指标: {primary_name}")
    print(f"  历史事件数: {len(events)}")
    print(f"  数据跨度: {calculate_date_range_months(primary_df)} 个月")
    
    # 为每个相关资产生成单独的图表
    for related_info in all_related:
        related_indicator = related_info['indicator']
        related_name = names.get(related_indicator, related_indicator)
        
        # 尝试加载相关资产数据
        related_data_file = None
        for ext in ['.json', '.csv']:
            test_path = f"{output_dir}/../data/{related_indicator}{ext}"
            if os.path.exists(test_path):
                related_data_file = test_path
                break
        
        if not related_data_file:
            print(f"  跳过 {related_indicator}: 数据文件不存在")
            continue
        
        try:
            related_df = load_indicator_data(related_data_file)
            
            # 生成双Y轴对比图
            chart_path = f"{output_dir}/{primary_indicator}_vs_{related_indicator}.png"
            
            plot_dual_axis_comparison(
                primary_df, primary_name,
                related_df, related_name,
                events, chart_path, current_event,
                event_results=event_results  # 传入事件结果
            )
            
            charts[f'{primary_indicator}_vs_{related_indicator}'] = chart_path
            
        except Exception as e:
            print(f"  生成 {related_indicator} 图表失败: {e}")
    
    return charts


def plot_performance_comparison(performance_data: Dict, output_path: str,
                                 indicator_names: Dict[str, str] = None) -> str:
    """
    绘制各资产平均收益对比图（中文标签）
    """
    if not performance_data:
        return None
    
    # 中文名称映射
    default_names = {
        'xlk': '科技ETF', 'xle': '能源ETF', 'xlf': '金融ETF',
        'xlv': '医疗ETF', 'xli': '工业ETF', 'jets': '航空ETF',
        'gdx': '黄金矿业', 'tlt': '长期美债', 'gold': '黄金',
        'silver': '白银', 'sp500': '标普500', 'nasdaq': '纳斯达克',
    }
    names = indicator_names or default_names
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    # 准备数据
    indicators = list(performance_data.keys())
    indicator_labels = [names.get(ind, ind) for ind in indicators]
    avg_returns = [performance_data[ind]['avg_return_pct'] for ind in indicators]
    positive_pct = [performance_data[ind]['positive_events'] / 
                    performance_data[ind]['total_events'] * 100 
                    for ind in indicators]
    
    # 中国习惯：红色=上涨，绿色=下跌
    colors_returns = ['#E74C3C' if r > 0 else '#27AE60' for r in avg_returns]
    
    # 图1：平均收益
    ax1 = axes[0]
    bars1 = ax1.barh(indicator_labels, avg_returns, color=colors_returns)
    ax1.set_xlabel('平均收益率 (%)', fontsize=12)
    ax1.set_title('历史事件期间各资产平均收益', fontsize=14, weight='bold')
    ax1.axvline(x=0, color='black', linewidth=0.8)
    ax1.grid(True, alpha=0.3, axis='x')
    
    # 添加数值标签
    for bar, val in zip(bars1, avg_returns):
        ax1.text(val + 0.5 if val >= 0 else val - 0.5, 
                 bar.get_y() + bar.get_height()/2,
                 f"{val:.1f}%", 
                 ha='left' if val >= 0 else 'right', 
                 va='center', fontsize=10)
    
    # 图2：正向事件占比
    ax2 = axes[1]
    bars2 = ax2.barh(indicator_labels, positive_pct, color='#3498DB')
    ax2.set_xlabel('正向事件占比 (%)', fontsize=12)
    ax2.set_title('历史事件中录得正收益的比例', fontsize=14, weight='bold')
    ax2.set_xlim(0, 100)
    ax2.grid(True, alpha=0.3, axis='x')
    
    # 添加数值标签
    for bar, val in zip(bars2, positive_pct):
        ax2.text(val + 2, bar.get_y() + bar.get_height()/2,
                 f"{val:.0f}%", ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"已生成: {output_path}")
    return output_path


def plot_event_matrix_heatmap(event_results: List[Dict], output_path: str,
                               indicator_names: Dict[str, str] = None) -> str:
    """
    绘制事件×资产收益矩阵热力图（中文标签）
    """
    if not event_results:
        return None
    
    # 中文名称映射
    default_names = {
        'xlk': '科技ETF', 'xle': '能源ETF', 'xlf': '金融ETF',
        'xlv': '医疗ETF', 'xli': '工业ETF', 'jets': '航空ETF',
        'gdx': '黄金矿业', 'tlt': '长期美债', 'gold': '黄金',
        'silver': '白银', 'sp500': '标普500', 'nasdaq': '纳斯达克',
    }
    names = indicator_names or default_names
    
    # 收集所有指标
    all_indicators = set()
    for result in event_results:
        all_indicators.update(result['related_performance'].keys())
    all_indicators = sorted(list(all_indicators))
    
    # 构建数据矩阵
    event_labels = [f"事件{i+1}" for i in range(len(event_results))]
    indicator_labels = [names.get(ind, ind) for ind in all_indicators]
    
    data_matrix = []
    for indicator in all_indicators:
        row = []
        for result in event_results:
            perf = result['related_performance'].get(indicator, {})
            row.append(perf.get('total_return_pct', 0))
        data_matrix.append(row)
    
    data_array = np.array(data_matrix)
    
    fig, ax = plt.subplots(figsize=(14, max(8, len(all_indicators) * 0.5)))
    
    # 热力图（中国习惯：红色=正收益，绿色=负收益）
    im = ax.imshow(data_array, cmap='RdYlGn_r', aspect='auto')
    
    # 设置标签
    ax.set_xticks(np.arange(len(event_labels)))
    ax.set_xticklabels(event_labels, fontsize=10, rotation=45, ha='right')
    ax.set_yticks(np.arange(len(indicator_labels)))
    ax.set_yticklabels(indicator_labels, fontsize=10)
    
    # 添加数值标注
    for i in range(len(all_indicators)):
        for j in range(len(event_labels)):
            val = data_array[i, j]
            color = 'white' if abs(val) > 10 else 'black'
            ax.text(j, i, f"{val:.1f}", ha='center', va='center', 
                    color=color, fontsize=9)
    
    ax.set_title('各资产在各历史事件中的收益率 (%)', fontsize=14, weight='bold')
    
    # 添加颜色条
    cbar = plt.colorbar(im, ax=ax, shrink=0.6)
    cbar.set_label('收益率 (%)', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"已生成: {output_path}")
    return output_path


def generate_all_charts(
    primary_indicator: str,
    primary_data_path: str,
    events_data_path: str,
    related_data_path: str,
    performance_data_path: str,
    output_dir: str
) -> Dict[str, str]:
    """
    生成所有图表
    
    Returns:
        图表类型到文件路径的映射
    """
    charts = {}
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 加载事件数据
    with open(events_data_path, 'r') as f:
        events_data = json.load(f)
    events = events_data.get('similar_events', [])
    current_event = events_data.get('current_event', {})
    
    # 加载表现数据
    with open(performance_data_path, 'r') as f:
        perf_data = json.load(f)
    
    aggregate_stats = perf_data.get('aggregate_stats', {})
    event_results = perf_data.get('event_results', [])
    
    # 1. 生成双Y轴时序对比图（每类资产一张）
    dual_charts = plot_all_dual_axis_charts(
        primary_indicator,
        primary_data_path,
        related_data_path,
        performance_data_path,
        output_dir
    )
    charts.update(dual_charts)
    
    # 2. 生成表现汇总图
    if aggregate_stats:
        comp_path = f"{output_dir}/performance_summary.png"
        charts['performance_summary'] = plot_performance_comparison(
            aggregate_stats, comp_path
        )
    
    # 3. 生成事件矩阵热力图
    if event_results:
        matrix_path = f"{output_dir}/event_matrix_heatmap.png"
        charts['event_matrix'] = plot_event_matrix_heatmap(
            event_results, matrix_path
        )
    
    return charts


def preflight_check(output_dir: str) -> Tuple[bool, List[str]]:
    """
    执行前置条件检查
    
    Returns:
        (all_passed, messages)
    """
    messages = []
    all_passed = True
    
    # 1. 中文字体检查
    is_font_ok, font_name, font_msg = check_chinese_font_available()
    messages.append(font_msg)
    if not is_font_ok:
        all_passed = False
    
    # 2. 输出目录权限检查
    try:
        os.makedirs(output_dir, exist_ok=True)
        test_file = f"{output_dir}/.write_test"
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        messages.append(f"✓ 输出目录权限正常: {output_dir}")
    except Exception as e:
        messages.append(f"❌ 输出目录权限异常: {e}")
        all_passed = False
    
    # 3. matplotlib 基础检查
    try:
        import matplotlib
        messages.append(f"✓ matplotlib 版本: {matplotlib.__version__}")
    except ImportError:
        messages.append("❌ matplotlib 未安装")
        all_passed = False
    
    return all_passed, messages


def main():
    parser = argparse.ArgumentParser(
        description='生成金融事件影响分析图表（中文标签）'
    )
    parser.add_argument('--primary-indicator', required=True, 
                        help='表征指标ID')
    parser.add_argument('--primary-data', required=True, 
                        help='表征指标数据文件')
    parser.add_argument('--events', required=True, 
                        help='事件JSON文件')
    parser.add_argument('--related', required=True, 
                        help='相关资产JSON文件')
    parser.add_argument('--performance', required=True, 
                        help='表现分析JSON文件')
    parser.add_argument('--output-dir', default='./charts', 
                        help='图表输出目录')
    parser.add_argument('--skip-preflight', action='store_true',
                        help='跳过前置检查')
    
    args = parser.parse_args()
    
    # 前置检查
    if not args.skip_preflight:
        print("\n=== 前置条件检查 ===")
        passed, msgs = preflight_check(args.output_dir)
        for msg in msgs:
            print(f"  {msg}")
        
        if not passed:
            print("\n❌ 前置检查失败，建议修复后再继续")
            print("继续执行可能导致图表中文乱码")
        else:
            print("\n✓ 前置检查全部通过")
    
    # 设置字体（必须在绘图前）
    setup_chinese_font()
    
    charts = generate_all_charts(
        args.primary_indicator,
        args.primary_data,
        args.events,
        args.related,
        args.performance,
        args.output_dir
    )
    
    print(f"\n=== 已生成图表 ===")
    for chart_type, path in charts.items():
        print(f"  {chart_type}: {path}")
    
    # 保存图表路径清单
    manifest_path = f"{args.output_dir}/charts_manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(charts, f, indent=2)
    print(f"\n图表清单已保存: {manifest_path}")


if __name__ == '__main__':
    main()