#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
缠论技术分析 - 主入口脚本
支持生成图表 PNG 图片和 Markdown 报告

添加超时和信号处理机制，避免进程僵尸化
"""

import sys
import os
import argparse
import signal
from datetime import datetime

# 添加脚本目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# 设置脚本超时时间（秒）
SCRIPT_TIMEOUT = 300  # 5 分钟超时

def timeout_handler(signum, frame):
    """超时处理函数"""
    print(f'\n❌ 脚本执行超时 ({SCRIPT_TIMEOUT}秒)，自动退出...')
    sys.exit(1)

def signal_handler(signum, frame):
    """信号处理函数（Ctrl+C 等）"""
    print(f'\n⚠️ 收到中断信号，清理资源后退出...')
    sys.exit(0)

# 注册信号处理
signal.signal(signal.SIGALRM, timeout_handler)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

from chanlun_core import analyze_stock, ChanLunCore
from chanlun_divergence import DivergenceDetector
from chanlun_chart import ChanLunChart, plot_chanlun_chart

def generate_report(stock_code: str, analyzer, output_dir: str = './outputs', chart_path: str = None) -> str:
    """生成 Markdown 分析报告 - 核心结论优先"""
    import os
    from datetime import datetime
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取分析结果
    trend = analyzer.get_current_trend()
    trend_cn = {'uptrend': '上涨', 'downtrend': '下跌', 'consolidation': '盘整'}.get(trend, '未知')
    
    fractals = analyzer.fractals
    strokes = analyzer.strokes
    segments = analyzer.segments
    pivots = analyzer.identify_pivots()
    
    # 背驰检测
    detector = DivergenceDetector(analyzer.processed_klines, strokes)
    divergence = detector.detect_trend_divergence()
    
    latest = analyzer.df.iloc[-1]
    prev = analyzer.df.iloc[-2]
    price_change = (latest['close'] - prev['close']) / prev['close'] * 100
    
    # ========== 核心结论判定 ==========
    # 趋势状态
    if trend == 'uptrend':
        trend_emoji = '🔴'
        trend_action = '持有为主'
        trend_risk = '关注顶分型出现'
        trend_signal = '若出现顶背驰或顶分型，考虑减仓'
    elif trend == 'downtrend':
        trend_emoji = '🟢'
        trend_action = '观望为主'
        trend_risk = '等待底分型或背驰信号'
        trend_signal = '若出现底背驰，可轻仓试探'
    else:
        trend_emoji = '🟡'
        trend_action = '区间操作'
        trend_risk = '等待突破方向'
        trend_signal = '中枢震荡，高抛低吸'
    
    # 背驰信号
    if divergence['detected']:
        if divergence['type'] == 'bullish':
            div_emoji = '📈'
            div_signal = '**底背驰信号** - 潜在买点'
        else:
            div_emoji = '📉'
            div_signal = '**顶背驰信号** - 潜在卖点'
        div_conf = f"置信度 {divergence['confidence']:.1%}"
    else:
        div_emoji = '➖'
        div_signal = '无背驰信号'
        div_conf = ''
    
    # 最近关键位置
    last_top = fractals['tops'][-1] if fractals.get('tops') else None
    last_bottom = fractals['bottoms'][-1] if fractals.get('bottoms') else None
    
    # ========== 构建报告 ==========
    report = f"""# {stock_code} 缠论技术分析报告

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 🎯 核心结论（最重要的判断）

### 走势状态

| 维度 | 判断 |
|------|------|
| **当前趋势** | {trend_emoji} **{trend_cn}** |
| **背驰信号** | {div_emoji} {div_signal} {div_conf} |
| **操作建议** | **{trend_action}** |

### 关键信号

| 信号 | 内容 |
|------|------|
| **趋势风险** | {trend_risk} |
| **行动触发** | {trend_signal} |

### 关键价位

| 类型 | 价格 | K线位置 |
|------|------|--------|
| **最新价** | {latest['close']:.2f} 元 | - |
"""
    
    if last_top:
        report += f"| **最近顶分型** | {last_top['price']:.2f} 元 | 第 {last_top['index']} 根K线 |\n"
    if last_bottom:
        report += f"| **最近底分型** | {last_bottom['price']:.2f} 元 | 第 {last_bottom['index']} 根K线 |\n"
    
    # 中枢关键位
    if pivots:
        last_pivot = pivots[-1]
        report += f"| **当前中枢** | {last_pivot['low']:.2f} ~ {last_pivot['high']:.2f} 元 | - |\n"
    
    # 图表展示
    if chart_path and os.path.exists(chart_path):
        report += f"""
---

## 📊 缠论分析图表

![{stock_code} 缠论分析图]({chart_path})

**图例说明**:
- **T** = 顶分型 (Top Fractal) - 绿色圆圈
- **B** = 底分型 (Bottom Fractal) - 红色圆圈
- **蓝色实线** = 向上笔
- **紫色虚线** = 向下笔
- **黄色区域** = 中枢区间
"""
    
    # 分项统计
    report += f"""
---

## 📋 分项统计与分析

### 一、行情概况

| 项目 | 数值 |
|------|------|
| **最新价** | {latest['close']:.2f} 元 |
| **涨跌幅** | {price_change:+.2f}% |
| **最高价** | {latest['high']:.2f} 元 |
| **最低价** | {latest['low']:.2f} 元 |
| **成交量** | {latest['volume']:,.0f} |

### 二、分型统计

| 类型 | 数量 | 最近位置 |
|------|:----:|---------|
| **顶分型** | {len(fractals.get('tops', []))} 个 | {f"{last_top['price']:.2f} 元 (第{last_top['index']}根)" if last_top else '-'} |
| **底分型** | {len(fractals.get('bottoms', []))} 个 | {f"{last_bottom['price']:.2f} 元 (第{last_bottom['index']}根)" if last_bottom else '-'} |

### 三、笔分析

| 项目 | 数值 |
|------|------|
| **笔数量** | {len(strokes)} 笔 |
"""
    
    if strokes:
        last_stroke = strokes[-1]
        stroke_dir = "向上笔 ↑" if last_stroke['direction'] == 'up' else "向下笔 ↓"
        report += f"| **当前笔** | {stroke_dir} |\n"
        report += f"| **笔起点** | {last_stroke['start_price']:.2f} 元 |\n"
        report += f"| **笔终点** | {last_stroke['end_price']:.2f} 元 |\n"
        report += f"| **笔幅度** | {abs(last_stroke['end_price'] - last_stroke['start_price']):.2f} 元 |\n"
    
    report += f"""
### 四、中枢分析

| 项目 | 数值 |
|------|------|
| **中枢数量** | {len(pivots)} 个 |
"""
    
    if pivots:
        for i, pivot in enumerate(pivots[-3:], 1):
            report += f"| **中枢 {i} 区间** | {pivot['low']:.2f} ~ {pivot['high']:.2f} 元 |\n"
            report += f"| **中枢 {i} 振幅** | {(pivot['high'] - pivot['low']) / pivot['low'] * 100:.1f}% |\n"
    
    report += f"""
### 五、背驰检测

| 项目 | 结果 |
|------|------|
| **是否检测到背驰** | {'✅ 是' if divergence['detected'] else '❌ 否'} |
"""
    
    if divergence['detected']:
        report += f"| **背驰类型** | {'📈 看涨背驰（底背驰）' if divergence['type'] == 'bullish' else '📉 看跌背驰（顶背驰）'} |\n"
        report += f"| **置信度** | {divergence['confidence']:.1%} |\n"
    
    # 风险提示
    report += f"""
---

## ⚠️ 风险提示

本报告仅供学习和研究使用，不构成任何投资建议。缠论分析存在主观性，实际操作需结合：

1. 基本面分析
2. 市场情绪
3. 资金流向
4. 宏观环境

**股市有风险，投资需谨慎！**

---

*报告由缠论技术分析系统自动生成*
"""
    
    # 保存报告
    filepath = os.path.join(output_dir, f'{stock_code}_chanlun_report.md')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return filepath

def main():
    parser = argparse.ArgumentParser(description='缠论技术分析工具')
    parser.add_argument('stock_code', help='股票代码（如 601688）')
    parser.add_argument('--period', default='daily', help='周期：daily, 60, 30 等 (默认：daily)')
    parser.add_argument('--output', default='./outputs', help='输出目录 (默认：./outputs)')
    parser.add_argument('--chart', action='store_true', help='生成图表')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    parser.add_argument('--verbose', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    # 启动超时计时器
    signal.alarm(SCRIPT_TIMEOUT)
    
    print('=' * 60)
    print('缠论技术分析')
    print('=' * 60)
    print(f'股票代码：{args.stock_code}')
    print(f'周期：{args.period}')
    print(f'分析时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'超时限制：{SCRIPT_TIMEOUT}秒')
    print('=' * 60)
    
    try:
        # 创建分析器
        print('\n[1/5] 获取股票数据...')
        analyzer = analyze_stock(args.stock_code, args.period)
        print(f'✅ 数据获取成功，共 {len(analyzer.df)} 根 K 线')
        
        # 识别分型
        print('\n[2/5] 识别分型...')
        fractals = analyzer.identify_fractals()
        print(f'✅ 顶分型：{len(fractals["tops"])}, 底分型：{len(fractals["bottoms"])}')
        
        # 识别笔
        print('\n[3/5] 识别笔...')
        strokes = analyzer.identify_strokes()
        print(f'✅ 笔数量：{len(strokes)}')
        
        # 识别线段和中枢
        print('\n[4/5] 识别线段和中枢...')
        segments = analyzer.identify_segments()
        pivots = analyzer.identify_pivots()
        print(f'✅ 线段：{len(segments)}, 中枢：{len(pivots)}')
        
        # 背驰检测
        print('\n[5/5] 背驰检测...')
        detector = DivergenceDetector(analyzer.processed_klines, strokes)
        divergence = detector.detect_trend_divergence()
        if divergence['detected']:
            print(f'✅ 发现背驰：{"看涨" if divergence["type"] == "bullish" else "看跌"} (置信度：{divergence["confidence"]:.1%})')
        else:
            print('✅ 未发现背驰')
        
        # 输出结果
        print('\n' + '=' * 60)
        print('分析结果')
        print('=' * 60)
        
        trend = analyzer.get_current_trend()
        trend_cn = {'uptrend': '上涨', 'downtrend': '下跌', 'consolidation': '盘整'}.get(trend, '未知')
        print(f'当前走势：{trend_cn}')
        
        if args.json:
            import json
            result = {
                'stock_code': args.stock_code,
                'trend': trend,
                'fractals': {
                    'tops_count': len(fractals['tops']),
                    'bottoms_count': len(fractals['bottoms'])
                },
                'strokes_count': len(strokes),
                'segments_count': len(segments),
                'pivots_count': len(pivots),
                'divergence': divergence
            }
            print('\n' + json.dumps(result, indent=2, ensure_ascii=False))
        
        # 生成图表（必需输出）
        print(f'\n生成缠论分析图表...')
        chart = ChanLunChart(analyzer.df, analyzer, args.output)
        chart_path = chart.plot_full_chart(args.stock_code)
        print(f'✅ 图表已保存：{chart_path}')
        
        # 生成报告（包含图表引用）
        print(f'\n生成分析报告...')
        report_path = generate_report(args.stock_code, analyzer, args.output, chart_path)
        print(f'✅ 报告已保存：{report_path}')
        
        print('\n' + '=' * 60)
        print('分析完成')
        print('=' * 60)
        
        # 取消超时计时器
        signal.alarm(0)
        
    except Exception as e:
        print(f'\n❌ 分析失败：{e}')
        # 取消超时计时器
        signal.alarm(0)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    
    finally:
        # 确保超时计时器被取消
        signal.alarm(0)


if __name__ == '__main__':
    main()
