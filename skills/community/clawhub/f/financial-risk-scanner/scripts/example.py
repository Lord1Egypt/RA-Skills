#!/usr/bin/env python3
"""
财务风险扫描示例脚本

演示如何使用 Financial Risk Scanner 分析单个公司的财务风险
"""

import os
import sys
import time
from datetime import datetime

# 添加模块路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from data_fetcher import FinancialDataFetcher
from risk_calculator import RiskCalculator
from report_generator import ReportGenerator


def example_analyze_company(ts_code: str = '000001.SZ', years: int = 5):
    """
    示例：分析单个公司的财务风险

    Args:
        ts_code: 股票代码 (默认: 000001.SZ 平安银行)
        years: 获取历史年数 (默认: 5年)
    """
    print("=" * 70)
    print("📊 Financial Risk Scanner - 使用示例")
    print("=" * 70)
    print(f"分析目标: {ts_code}")
    print(f"历史数据: {years} 年")
    print("=" * 70)

    start_time = time.time()

    # ========================================
    # 第一步: 初始化数据获取器
    # ========================================
    print("\n【第一步】初始化数据获取器...")
    print("-" * 70)

    fetcher = FinancialDataFetcher()

    # ========================================
    # 第二步: 获取财务数据
    # ========================================
    print("\n【第二步】获取财务数据...")
    print("-" * 70)

    financial_data = fetcher.fetch_all_financial_data(
        ts_code=ts_code,
        years=years,
        report_type='1'  # 年报
    )

    # 显示获取结果
    print("\n获取的数据表:")
    for key, value in financial_data.items():
        if hasattr(value, '__len__'):
            print(f"  - {key}: {len(value)} 条记录")
        elif isinstance(value, dict):
            print(f"  - {key}: {value.get('name', 'N/A')}")

    # ========================================
    # 第三步: 计算风险指标
    # ========================================
    print("\n【第三步】计算风险指标...")
    print("-" * 70)

    calculator = RiskCalculator(financial_data)
    risk_results = calculator.calculate_all_indicators()

    # ========================================
    # 第四步: 生成报告
    # ========================================
    print("\n【第四步】生成风险报告...")
    print("-" * 70)

    generator = ReportGenerator()
    report_path = generator.generate_report(
        stock_info=financial_data.get('stock_info', {}),
        risk_results=risk_results,
        financial_data=financial_data
    )

    # ========================================
    # 第五步: 输出结果摘要
    # ========================================
    print("\n【第五步】结果摘要...")
    print("-" * 70)

    summary = risk_results['_summary']
    stock_info = financial_data.get('stock_info', {})

    print(f"\n公司: {stock_info.get('name', 'N/A')} ({ts_code})")
    print(f"行业: {stock_info.get('industry', 'N/A')}")
    print(f"\n风险评分:")
    print(f"  总分: {summary['total_score']} 分")
    print(f"  严重程度: {summary['severity']}")
    print(f"\n指标分布:")
    print(f"  🔴 严重 (3分): {summary['critical_count']} 个")
    print(f"  🟠 中等 (2分): {summary['high_count']} 个")
    print(f"  🟡 轄微 (1分): {summary['moderate_count']} 个")
    print(f"  🟢 无风险 (0分): {summary['low_count']} 个")

    # 显示高风险指标
    high_risk = [(k, v) for k, v in risk_results.items()
                if k != '_summary' and v.get('score', 0) >= 2]

    if high_risk:
        print(f"\n⚠️ 高风险指标:")
        for key, value in high_risk:
            print(f"  - {key}: {value['score']} 分, 趋势: {value['trend']}")

    elapsed_time = time.time() - start_time
    print(f"\n⏱️ 分析耗时: {elapsed_time:.1f} 秒")
    print(f"\n📄 报告路径: {report_path}")

    print("\n" + "=" * 70)
    print("示例完成!")
    print("=" * 70)

    return report_path


def example_quick_check(ts_code: str = '600000.SH'):
    """
    示例：快速检查单个风险指标

    Args:
        ts_code: 股票代码 (默认: 600000.SH 浦发银行)
    """
    print("\n" + "=" * 70)
    print("📊 快速风险检查示例")
    print("=" * 70)

    # 获取数据
    fetcher = FinancialDataFetcher()
    financial_data = fetcher.fetch_all_financial_data(ts_code, years=3)

    # 计算风险
    calculator = RiskCalculator(financial_data)

    # 只计算特定指标
    print(f"\n检查存贷双高指标...")

    result = calculator.calc_cash_debt_paradox()

    print(f"结果:")
    print(f"  评分: {result['score']} 分")
    print(f"  趋势: {result['trend']}")
    print(f"  详情: {result['details']}")

    return result


def example_batch_analysis(stock_codes: list = None):
    """
    示例：批量分析多个公司

    Args:
        stock_codes: 股票代码列表
    """
    if stock_codes is None:
        stock_codes = ['000001.SZ', '600000.SH', '000002.SZ']

    print("\n" + "=" * 70)
    print("📊 批量风险分析示例")
    print("=" * 70)
    print(f"分析目标: {len(stock_codes)} 家公司")
    print("=" * 70)

    fetcher = FinancialDataFetcher()
    generator = ReportGenerator()

    results = []

    for i, ts_code in enumerate(stock_codes, 1):
        print(f"\n[{i}/{len(stock_codes)}] 分析 {ts_code}...")

        try:
            # 获取数据
            financial_data = fetcher.fetch_all_financial_data(ts_code, years=5)

            # 计算风险
            calculator = RiskCalculator(financial_data)
            risk_results = calculator.calculate_all_indicators()

            # 汇总结果
            summary = risk_results['_summary']
            stock_info = financial_data.get('stock_info', {})

            results.append({
                'ts_code': ts_code,
                'name': stock_info.get('name', 'N/A'),
                'total_score': summary['total_score'],
                'severity': summary['severity'],
                'critical_count': summary['critical_count'],
            })

            print(f"  ✅ {stock_info.get('name', 'N/A')}: {summary['total_score']} 分, {summary['severity']}")

        except Exception as e:
            print(f"  ❌ 分析失败: {e}")
            results.append({
                'ts_code': ts_code,
                'name': 'N/A',
                'total_score': -1,
                'severity': '分析失败',
                'critical_count': 0,
            })

    # 打印汇总表
    print("\n" + "=" * 70)
    print("批量分析结果汇总")
    print("=" * 70)
    print("\n| 序号 | 公司 | 股票代码 | 总分 | 严重程度 |")
    print("|------|------|----------|------|----------|")

    for i, r in enumerate(results, 1):
        severity_icon = {
            '🔴 Critical': '🔴',
            '🟠 High': '🟠',
            '🟡 Moderate': '🟡',
            '🟢 Low': '🟢',
        }
        icon = severity_icon.get(r['severity'], '⚪')
        print(f"| {i} | {r['name']} | {r['ts_code']} | {r['total_score']} | {icon} {r['severity']} |")

    return results


def main():
    """主函数 - 运行所有示例"""
    print("\n" + "=" * 70)
    print("📊 Financial Risk Scanner - 完整示例演示")
    print("=" * 70)
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # 示例1: 单个公司完整分析
    print("\n\n" + "▶" * 35)
    print("示例 1: 单个公司完整分析")
    print("▶" * 35)

    try:
        report_path = example_analyze_company('000001.SZ', years=5)
    except Exception as e:
        print(f"示例1运行失败: {e}")

    # 示例2: 快速检查单个指标
    print("\n\n" + "▶" * 35)
    print("示例 2: 快速检查单个指标")
    print("▶" * 35)

    try:
        result = example_quick_check('600000.SH')
    except Exception as e:
        print(f"示例2运行失败: {e}")

    # 示例3: 批量分析
    print("\n\n" + "▶" * 35)
    print("示例 3: 批量分析多个公司")
    print("▶" * 35)

    try:
        results = example_batch_analysis(['000001.SZ', '600000.SH'])
    except Exception as e:
        print(f"示例3运行失败: {e}")

    print("\n" + "=" * 70)
    print("所有示例演示完成!")
    print("=" * 70)


if __name__ == "__main__":
    # 可以选择运行单个示例或全部示例

    import argparse

    parser = argparse.ArgumentParser(description='Financial Risk Scanner 示例脚本')
    parser.add_argument('--mode', choices=['single', 'quick', 'batch', 'all'],
                       default='all', help='运行模式')
    parser.add_argument('--ts-code', default='000001.SZ', help='股票代码')
    parser.add_argument('--years', type=int, default=5, help='历史年数')

    args = parser.parse_args()

    if args.mode == 'single':
        example_analyze_company(args.ts_code, args.years)
    elif args.mode == 'quick':
        example_quick_check(args.ts_code)
    elif args.mode == 'batch':
        example_batch_analysis()
    else:
        main()