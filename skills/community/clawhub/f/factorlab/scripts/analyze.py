#!/usr/bin/env python3
"""
FactorLab CLI - Stock factor analysis and buy recommendation tool.

Usage:
  python analyze.py <stock_code>                    # Analyze single stock
  python analyze.py <code1> <code2> <code3>         # Analyze multiple stocks
  python analyze.py --batch                         # Scan default stock pool
  python analyze.py --batch --codes 000001,600519   # Scan specific codes
  python analyze.py --batch --min-score 60          # Filter by min score
  python analyze.py --batch --top 10                # Return top 10
  python analyze.py --batch --no-live               # Use simulated data
  python analyze.py 000001 --json                   # Output as JSON

Output: Markdown report (default) or JSON (--json flag).
"""

import argparse
import json
import os
import sys

# Add scripts directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from factorlab_engine import (
    analyze_stock,
    batch_scan,
    DEFAULT_POOL,
    signal_icon,
)


def format_single_report(result):
    """Format a single stock analysis result as Markdown."""
    if 'error' in result:
        return f"❌ {result['error']}"

    code = result['code']
    name = result['name']
    price = result['price']
    change_pct = result['change_pct']
    factors = result['factors']
    rec = result['recommendation']
    data_source = result.get('data_source', 'unknown')
    data_tag = '📡 实时数据' if data_source == 'live' else '🔬 模拟数据'

    lines = []
    lines.append(f"# FactorLab 因子分析报告 — {name}({code})")
    lines.append(f"> 分析时间: {result.get('analyze_time', '')} | 数据源: {data_tag}")
    lines.append("")

    # ── Price summary ──
    change_str = f"{change_pct:+.2f}%"
    change_emoji = "🔴" if change_pct > 0 else "🟢" if change_pct < 0 else "⚪"
    lines.append(f"## 📊 行情概览")
    lines.append(f"| 项目 | 数值 |")
    lines.append(f"|------|------|")
    lines.append(f"| 当前价格 | ¥{price:.2f} |")
    lines.append(f"| 涨跌幅 | {change_emoji} {change_str} |")
    lines.append(f"| 数据点数 | {factors.get('data_points', 0)} 根K线 |")
    lines.append("")

    # ── Buy recommendation (most important - put first for AI consumption) ──
    verdict = rec['verdict']
    confidence = rec['confidence']
    fl_score = rec['factorlab_score']
    lines.append(f"## 🎯 购买建议: {verdict}")
    lines.append(f"**置信度: {confidence}%** | FactorLab因子评分: {fl_score}")
    lines.append("")
    lines.append(f"> {rec['action']}")
    lines.append("")

    # ── Reasons ──
    if rec['reasons']:
        lines.append("### ✅ 看多理由")
        for r in rec['reasons']:
            lines.append(f"- {r}")
        lines.append("")

    # ── Risks ──
    if rec['risks']:
        lines.append("### ⚠️ 风险提示")
        for r in rec['risks']:
            lines.append(f"- {r}")
        lines.append("")

    # ── Factor details ──
    lines.append("## 🔬 因子切割论明细")
    lines.append(f"| 因子 | 原始值 | 子分 | 权重 | 状态 |")
    lines.append(f"|------|--------|------|------|------|")
    lines.append(f"| 理想反转 | {factors['ideal_reversal']:+.4f} | {factors['ideal_reversal_score']} | 35% | {factors['ideal_reversal_ok']} |")
    lines.append(f"| 理想振幅 | {factors['ideal_amplitude']:+.4f} | {factors['ideal_amplitude_score']} | 30% | {factors['ideal_amplitude_ok']} |")
    lines.append(f"| 长端动量 | {factors['long_momentum']:+.4f} | {factors['long_momentum_score']} | 35% | {factors['long_momentum_ok']} |")
    lines.append(f"| **综合评分** | — | **{factors['factorlab_score']}** | 100% | {factors['signal_icon']} {factors['signal']} |")
    lines.append("")

    # ── Factor explanation ──
    lines.append("## 📖 因子说明")
    lines.append("- **理想反转因子**: 以20日平均单笔成交金额为刀，切割20日涨跌幅。值越负=低成交额组涨幅越高，反转效应越强。")
    lines.append("- **理想振幅因子**: 以20日收盘价为刀，切割20日振幅。值越负=高价股振幅小于低价股，结构更健康。")
    lines.append("- **长端动量因子**: 以160日振幅为刀，切割160日Alpha收益。值越大=低振幅日Alpha越高，动量持续性强。")
    lines.append("")
    lines.append("---")
    lines.append("*⚠️ 本报告基于开源金工研报因子切割论模型，仅供量化研究参考，不构成投资建议。*")

    return "\n".join(lines)


def format_batch_report(results):
    """Format batch scan results as Markdown."""
    if not results:
        return "扫描完成，未发现符合条件的股票。可尝试降低 --min-score 参数。"

    lines = []
    lines.append(f"# FactorLab 批量扫描报告")
    lines.append(f"> 共扫描到 {len(results)} 只符合评分阈值的股票")
    lines.append("")

    lines.append(f"| 排名 | 代码 | 名称 | 价格 | 涨跌幅 | FactorLab评分 | 建议 |")
    lines.append(f"|------|------|------|------|--------|-------------|------|")

    for i, r in enumerate(results, 1):
        change_str = f"{r['change_pct']:+.2f}%"
        rec = r.get('recommendation', {})
        verdict = rec.get('verdict', '')
        lines.append(
            f"| {i} | {r['code']} | {r['name']} | ¥{r['price']:.2f} | {change_str} | "
            f"{r['factorlab_score']} | {verdict} |"
        )

    lines.append("")

    # Top 3 detailed
    lines.append("## 🏆 TOP 3 详细分析")
    for r in results[:3]:
        lines.append("")
        lines.append(f"### {r['name']}({r['code']}) — {r['recommendation']['verdict']}")
        lines.append(f"- 价格: ¥{r['price']:.2f} ({r['change_pct']:+.2f}%)")
        lines.append(f"- FactorLab评分: {r['factorlab_score']}")
        lines.append(f"- 建议: {r['recommendation']['action']}")
        if r['recommendation']['reasons']:
            lines.append(f"- 看多理由: {'; '.join(r['recommendation']['reasons'][:3])}")
        if r['recommendation']['risks']:
            lines.append(f"- 风险: {'; '.join(r['recommendation']['risks'][:2])}")

    lines.append("")
    lines.append("---")
    lines.append("*⚠️ 本报告基于开源金工研报因子切割论模型，仅供量化研究参考，不构成投资建议。*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='FactorLab 因子分析与购买建议工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('codes', nargs='*', help='股票代码（1个或多个），如 000001 600519')
    parser.add_argument('--batch', action='store_true', help='批量扫描模式')
    parser.add_argument('--codes-list', dest='codes_list', help='批量扫描的股票代码列表，逗号分隔')
    parser.add_argument('--min-score', dest='min_score', type=float, default=55, help='最低FactorLab评分阈值（默认55）')
    parser.add_argument('--top', dest='top_k', type=int, default=30, help='返回前N名（默认30）')
    parser.add_argument('--no-live', dest='no_live', action='store_true', help='使用模拟数据（不连接TDX服务器）')
    parser.add_argument('--json', dest='as_json', action='store_true', help='输出JSON格式')

    args = parser.parse_args()
    prefer_live = not args.no_live

    # ── Batch mode ──
    if args.batch:
        codes = None
        if args.codes_list:
            codes = [c.strip() for c in args.codes_list.split(',') if c.strip()]
        results = batch_scan(codes=codes, min_score=args.min_score, top_k=args.top_k, prefer_live=prefer_live)
        if args.as_json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(format_batch_report(results))
        return

    # ── Single/multi stock mode ──
    if not args.codes:
        parser.print_help()
        sys.exit(1)

    if len(args.codes) == 1:
        result = analyze_stock(args.codes[0], prefer_live=prefer_live)
        if args.as_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_single_report(result))
    else:
        # Multiple stocks: analyze each and output summary
        all_results = []
        for code in args.codes:
            result = analyze_stock(code, prefer_live=prefer_live)
            all_results.append(result)

        if args.as_json:
            print(json.dumps(all_results, ensure_ascii=False, indent=2))
        else:
            for result in all_results:
                print(format_single_report(result))
                print("\n" + "=" * 80 + "\n")


if __name__ == '__main__':
    main()
