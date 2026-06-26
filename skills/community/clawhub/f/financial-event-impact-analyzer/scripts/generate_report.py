#!/usr/bin/env python3
"""
Generate final analysis report in Markdown format.
Embeds all generated charts into the report for easy viewing.
"""

import argparse
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple


# 中文名称映射
INDICATOR_NAMES = {
    'brent_crude': '布伦特原油',
    'wti_crude': 'WTI原油',
    'gold': '黄金',
    'silver': '白银',
    'copper': '铜',
    'sp500': '标普500',
    'nasdaq': '纳斯达克',
    'dow_jones': '道琼斯',
    'vix': 'VIX恐慌指数',
    'xlk': '科技ETF',
    'xle': '能源ETF',
    'xlf': '金融ETF',
    'xlv': '医疗ETF',
    'xli': '工业ETF',
    'xly': '消费ETF',
    'jets': '航空ETF',
    'iyr': '房地产ETF',
    'gdx': '黄金矿业ETF',
    'tlt': '长期美债ETF',
    'usd_index': '美元指数',
    'usd_cny': '美元/人民币',
    'us_10y_treasury': '10年期美债收益率',
    'csi300': '沪深300',
    'sse_composite': '上证指数',
    'chinext': '创业板指',
}

# 颜色约定（中国习惯）
COLOR_POSITIVE = '🔴'
COLOR_NEGATIVE = '🟢'


def load_json(filepath: str) -> Dict:
    """Load JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def get_indicator_name(indicator_id: str) -> str:
    """Get Chinese name for indicator."""
    return INDICATOR_NAMES.get(indicator_id, indicator_id)


def format_change(change_pct: float) -> str:
    """Format change percentage with color (Chinese convention)."""
    if change_pct > 0:
        return f"{COLOR_POSITIVE} +{change_pct:.1f}%"
    elif change_pct < 0:
        return f"{COLOR_NEGATIVE} {change_pct:.1f}%"
    else:
        return f"0.0%"


def generate_change_table(event_results: List[Dict], primary_indicator: str, 
                          related_indicators: List[str]) -> str:
    """Generate change table in Markdown format."""
    
    primary_name = get_indicator_name(primary_indicator)
    
    # Table header
    header = "| 事件 | 时间区间 | " + primary_name + " |"
    for ind in related_indicators[:6]:  # 最多显示6个相关指标
        header += f" {get_indicator_name(ind)} |"
    header += "\n"
    
    # Separator
    sep = "|:----:|:--------:|:------:|"
    for _ in range(min(6, len(related_indicators))):
        sep += ":------:|"
    sep += "\n"
    
    # Table rows (从最新到最早)
    rows = ""
    for i, result in enumerate(event_results):
        event = result.get('event', {})
        primary_perf = result.get('primary_performance', {})
        related_perf = result.get('related_performance', {})
        
        # 事件编号和时间区间
        time_range = f"{event['start_date'][:7]} ~ {event['end_date'][:7]}"
        row = f"| **事件{i+1}** | {time_range} | "
        
        # 主指标涨跌幅
        primary_change = primary_perf.get('total_return_pct', 0)
        row += format_change(primary_change) + " |"
        
        # 相关指标涨跌幅
        for ind in related_indicators[:6]:
            perf = related_perf.get(ind, {})
            change = perf.get('total_return_pct', 0)
            row += f" {format_change(change)} |"
        
        row += "\n"
        rows += row
    
    return header + sep + rows


def generate_summary_table(aggregate_stats: Dict) -> str:
    """Generate summary statistics table."""
    
    header = "| 资产 | 平均收益 | 胜率 | 收益波动 | 确定性评级 |\n"
    sep = "|:-----|:-------:|:----:|:--------:|:----------:|\n"
    
    rows = ""
    # 按胜率排序
    sorted_stats = sorted(aggregate_stats.items(), 
                          key=lambda x: x[1]['win_rate_pct'], reverse=True)
    
    for indicator, stats in sorted_stats:
        avg_return = stats['avg_return_pct']
        win_rate = stats['win_rate_pct']
        std_return = stats['std_return_pct']
        
        # 确定性评级（基于胜率）
        if win_rate >= 90:
            rating = "⭐⭐⭐⭐⭐"
        elif win_rate >= 70:
            rating = "⭐⭐⭐⭐"
        elif win_rate >= 50:
            rating = "⭐⭐⭐"
        elif win_rate >= 30:
            rating = "⭐⭐"
        else:
            rating = "⭐"
        
        rows += f"| **{get_indicator_name(indicator)}** | {format_change(avg_return)} | {win_rate:.0f}% | ±{std_return:.1f}% | {rating} |\n"
    
    return header + sep + rows


def generate_chart_section(charts: Dict[str, str], output_dir: str) -> str:
    """Generate chart embedding section with Markdown image references."""
    
    section = "## 📈 时序对比图（各资产与表征指标）\n\n"
    section += "> 🔴 **红色虚线框** = 历史事件发生时间区间\n\n"
    
    # 按相关性分类展示图表
    dual_charts = {k: v for k, v in charts.items() if '_vs_' in k}
    
    for chart_type, chart_path in dual_charts.items():
        # 解析指标名称
        parts = chart_type.split('_vs_')
        if len(parts) == 2:
            primary = get_indicator_name(parts[0])
            related = get_indicator_name(parts[1])
            section += f"### {primary} vs {related}\n\n"
        
        # 使用相对路径嵌入图片
        # Markdown 图片语法：![描述](路径)
        relative_path = os.path.basename(chart_path)
        section += f"![{chart_type}](charts/{relative_path})\n\n"
    
    # 添加表现汇总图
    if 'performance_summary' in charts:
        section += "## 📊 表现汇总图\n\n"
        section += f"![表现汇总](charts/performance_summary.png)\n\n"
    
    # 添加事件矩阵热力图
    if 'event_matrix' in charts:
        section += "## 🔥 事件矩阵热力图\n\n"
        section += f"![事件矩阵](charts/event_matrix_heatmap.png)\n\n"
    
    return section


def generate_full_report(
    primary_indicator: str,
    events_data: Dict,
    related_data: Dict,
    performance_data: Dict,
    charts_manifest: Dict,
    output_dir: str
) -> str:
    """Generate full analysis report in Markdown."""
    
    primary_name = get_indicator_name(primary_indicator)
    current_event = events_data.get('current_event', {})
    similar_events = events_data.get('similar_events', [])
    event_results = performance_data.get('event_results', [])
    aggregate_stats = performance_data.get('aggregate_stats', {})
    
    # 收集相关指标
    related_indicators = []
    for category in ['benefited', 'harmed', 'neutral_uncertain']:
        for asset in related_data.get(category, []):
            if 'indicator' in asset:
                related_indicators.append(asset['indicator'])
    
    # 报告头部
    report = f"""# {primary_name}快速上涨历史影响分析报告

**生成时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}  
**分析工具**: financial-event-impact-analyzer 🐂

---

## 🎯 核心结论

"""
    
    # 核心结论（基于胜率最高的资产）
    if aggregate_stats:
        top_asset = max(aggregate_stats.items(), 
                        key=lambda x: x[1]['win_rate_pct'])
        top_name = get_indicator_name(top_asset[0])
        top_win_rate = top_asset[1]['win_rate_pct']
        top_avg_return = top_asset[1]['avg_return_pct']
        
        report += f"**{top_name}是{primary_name}上涨最确定的受益资产**："
        report += f"在历史上{len(similar_events)}次{primary_name}快速上涨事件中，"
        report += f"{top_name}**{top_win_rate:.0f}%录得正收益**，"
        report += f"平均涨幅{top_avg_return:.1f}%。\n\n"
    
    # 当前事件特征
    report += f"""---

## 📋 当前事件特征

| 特征 | 数值 |
|:-----|:----:|
| **90天涨跌幅** | {format_change(current_event.get('change_90d', 0))} |
| **当前价格** | $ {current_event.get('current_price', 'N/A')} |
| **事件类型** | {current_event.get('event_type', '重大价格上涨')} |
| **波动率** | {current_event.get('volatility_30d', 0):.1f}% |

---

## 📜 历史相似事件 ({len(similar_events)}个)

"""
    
    # 事件列表
    report += "| 事件 | 时间区间 | 涨跌幅 | 背景 |\n"
    report += "|:----:|:--------:|:------:|:-----|\n"
    
    for i, event in enumerate(similar_events[:10]):  # 最多显示10个
        time_range = f"{event['start_date'][:10]} ~ {event['end_date'][:10]}"
        change = event.get('change_pct', 0)
        report += f"| **事件{i+1}** | {time_range} | {format_change(change)} | - |\n"
    
    # 变动幅度表格
    report += f"""

---

## 📊 变动幅度表格（从最新到最早）

{generate_change_table(event_results, primary_indicator, related_indicators)}

---

## 🔑 汇总统计

{generate_summary_table(aggregate_stats)}

"""
    
    # 图表部分（嵌入图片）
    if charts_manifest:
        report += generate_chart_section(charts_manifest, output_dir)
    
    # 分析局限性
    report += """
---

## ⚠️ 分析局限性

1. **历史不代表未来**：历史表现仅供参考，不构成投资建议
2. **样本数量有限**：相似事件数量可能较少，统计显著性有待验证
3. **宏观环境差异**：每次事件的宏观背景不同，需结合当前环境判断
4. **数据源局限**：部分数据可能缺失或存在误差

---

🐂 **报告生成完毕** | 基于 {len(similar_events)} 个历史事件分析
"""
    
    return report


def main():
    parser = argparse.ArgumentParser(
        description='生成金融事件影响分析报告（Markdown格式，嵌入图片）'
    )
    parser.add_argument('--primary-indicator', required=True, 
                        help='表征指标ID')
    parser.add_argument('--events', required=True, 
                        help='事件JSON文件')
    parser.add_argument('--related', required=True, 
                        help='相关资产JSON文件')
    parser.add_argument('--performance', required=True, 
                        help='表现分析JSON文件')
    parser.add_argument('--charts-manifest', required=True,
                        help='图表清单JSON文件')
    parser.add_argument('--output-dir', required=True,
                        help='报告输出目录')
    parser.add_argument('--output', '-o', default='report.md',
                        help='报告文件名')
    
    args = parser.parse_args()
    
    # 加载所有数据
    events_data = load_json(args.events)
    related_data = load_json(args.related)
    performance_data = load_json(args.performance)
    charts_manifest = load_json(args.charts_manifest)
    
    # 生成报告
    report = generate_full_report(
        args.primary_indicator,
        events_data,
        related_data,
        performance_data,
        charts_manifest,
        args.output_dir
    )
    
    # 保存报告
    output_path = f"{args.output_dir}/{args.output}"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✓ 报告已生成: {output_path}")
    print(f"  包含 {len(charts_manifest)} 张嵌入图表")
    
    # 输出报告内容预览
    print(f"\n=== 报告预览 ===")
    preview_lines = report.split('\n')[:30]
    for line in preview_lines:
        print(line)
    print("...")


if __name__ == '__main__':
    main()