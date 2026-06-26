#!/usr/bin/env python3
"""
财务风险分析主脚本

命令行入口：python3 analyze_company.py <ts_code> [--years N] [--output PATH]

流程：
1. 调用data_fetcher获取数据
2. 调用risk_calculator计算21个指标
3. 汇总评分，判断严重程度
4. 调用report_generator生成报告
5. 输出报告路径
"""

import os
import sys
import argparse
import logging
from datetime import datetime
import time

# 添加模块路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from data_fetcher import FinancialDataFetcher
from risk_calculator import RiskCalculator
from report_generator import ReportGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description='财务风险扫描 - 分析上市公司财务报表风险信号',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 analyze_company.py 000001.SZ                # 分析平安银行，默认10年数据
  python3 analyze_company.py 000001.SZ --years 5      # 分析5年数据
  python3 analyze_company.py 000001.SZ --output /tmp/report.md  # 自定义输出路径
        """
    )
    
    parser.add_argument(
        'ts_code',
        help='股票代码 (格式: 代码.交易所，如 000001.SZ, 600000.SH)'
    )
    
    parser.add_argument(
        '--years',
        type=int,
        default=10,
        help='获取历史年数 (默认: 10年)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='报告输出路径 (默认: ~/.openclaw/workspace/memory/financial-risk/)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='显示详细输出'
    )
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 打印标题
    print("=" * 70)
    print("📊 Financial Risk Scanner - 财务风险扫描器")
    print("=" * 70)
    print(f"目标公司: {args.ts_code}")
    print(f"历史数据: {args.years} 年")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    start_time = time.time()
    
    try:
        # === 步骤1: 获取财务数据 ===
        print("\n[步骤 1/4] 获取财务数据...")
        print("-" * 70)
        
        fetcher = FinancialDataFetcher()
        financial_data = fetcher.fetch_all_financial_data(
            ts_code=args.ts_code,
            years=args.years,
            report_type='1'  # 年报
        )
        
        # 检查数据完整性
        data_check = check_data_completeness(financial_data)
        print_data_summary(data_check)
        
        if data_check['critical_missing']:
            print("\n⚠️ 警告: 缺少关键数据表，分析可能不完整")
            print(f"   缺失: {', '.join(data_check['critical_missing'])}")
        
        # === 步骤2: 计算风险指标 ===
        print("\n[步骤 2/4] 计算风险指标...")
        print("-" * 70)
        
        calculator = RiskCalculator(financial_data)
        risk_results = calculator.calculate_all_indicators()
        
        # === 步骤3: 生成报告 ===
        print("\n[步骤 3/4] 生成风险报告...")
        print("-" * 70)
        
        generator = ReportGenerator()
        report_path = generator.generate_report(
            stock_info=financial_data.get('stock_info', {}),
            risk_results=risk_results,
            financial_data=financial_data,
            output_path=args.output
        )
        
        # === 步骤4: 输出结果 ===
        print("\n[步骤 4/4] 输出结果...")
        print("-" * 70)
        
        summary = risk_results['_summary']
        
        print(f"\n✅ 分析完成!")
        print(f"\n📋 风险摘要:")
        print(f"   公司名称: {financial_data.get('stock_info', {}).get('name', 'N/A')}")
        print(f"   股票代码: {args.ts_code}")
        print(f"   总分: {summary['total_score']} 分 (满分 63 分)")
        print(f"   严重程度: {summary['severity']}")
        print(f"   指标统计:")
        print(f"     - 🔴 严重 (3分): {summary['critical_count']} 个")
        print(f"     - 🟠 中等 (2分): {summary['high_count']} 个")
        print(f"     - 🟡 轻微 (1分): {summary['moderate_count']} 个")
        print(f"     - 🟢 无风险 (0分): {summary['low_count']} 个")
        
        print(f"\n📄 报告路径: {report_path}")
        
        # 显示重点关注指标
        high_risk = [(k, v) for k, v in risk_results.items() 
                    if k != '_summary' and v.get('score', 0) >= 2]
        
        if high_risk:
            print(f"\n⚠️ 重点关注指标:")
            high_risk.sort(key=lambda x: x[1]['score'], reverse=True)
            
            indicator_names = {
                'cash_debt_paradox': '存贷双高',
                'receivables_anomaly': '应收账款畸高',
                'inventory_anomaly': '存货异常',
                'cash_profit_divergence': '净现比背离',
                'gross_margin_anomaly': '毛利率异常',
                'abnormal_non_recurring': '异常非经常性损益',
                'asset_impairment_bath': '资产减值洗大澡',
                'goodwill_high': '商誉占比过高',
                'debt_ratio_high': '资产负债率畸高',
                'short_term_liquidity': '短期偿债压力',
                'non_standard_opinion': '非标审计意见',
            }
            
            for key, value in high_risk[:5]:  # 只显示前5个
                name = indicator_names.get(key, key)
                score = value['score']
                icon = '🔴' if score == 3 else '🟠'
                print(f"   {icon} {name}: {score} 分")
        
        # 计算耗时
        elapsed_time = time.time() - start_time
        print(f"\n⏱️ 分析耗时: {elapsed_time:.1f} 秒")
        
        print("\n" + "=" * 70)
        print("分析完成！建议查阅完整报告进行详细评估。")
        print("=" * 70)
        
        return report_path
        
    except Exception as e:
        logger.error(f"❌ 分析失败: {e}")
        print(f"\n❌ 错误: {e}")
        print("\n可能的原因:")
        print("  1. Tushare Token 未配置 (需设置环境变量 TUSHARE_TOKEN)")
        print("  2. 股票代码格式错误 (应为: 代码.交易所，如 000001.SZ)")
        print("  3. API 调用频率限制 (请稍后再试)")
        print("  4. 目标公司无足够历史数据")
        
        sys.exit(1)


def check_data_completeness(financial_data: dict) -> dict:
    """检查数据完整性"""
    result = {
        'tables': {},
        'record_counts': {},
        'critical_missing': [],
        'warnings': [],
    }
    
    critical_tables = ['balance', 'income', 'cashflow']
    
    for table_name in ['balance', 'income', 'cashflow', 'fina_indicator', 'audit']:
        data = financial_data.get(table_name)
        
        if data is None or (hasattr(data, 'empty') and data.empty):
            result['tables'][table_name] = False
            result['record_counts'][table_name] = 0
            
            if table_name in critical_tables:
                result['critical_missing'].append(table_name)
        else:
            result['tables'][table_name] = True
            result['record_counts'][table_name] = len(data) if hasattr(data, '__len__') else 1
    
    # 检查公司信息
    stock_info = financial_data.get('stock_info')
    if not stock_info or not stock_info.get('name'):
        result['warnings'].append('公司基本信息缺失')
    
    # 检查历史数据长度
    for table_name in ['balance', 'income', 'cashflow']:
        count = result['record_counts'].get(table_name, 0)
        if count < 3:
            result['warnings'].append(f'{table_name} 历史数据不足 (< 3年)')
    
    return result


def print_data_summary(data_check: dict):
    """打印数据摘要"""
    print("\n📊 数据获取结果:")
    
    table_names = {
        'balance': '资产负债表',
        'income': '利润表',
        'cashflow': '现金流量表',
        'fina_indicator': '财务指标',
        'audit': '审计意见',
    }
    
    for table_name, display_name in table_names.items():
        count = data_check['record_counts'].get(table_name, 0)
        status = '✅' if count > 0 else '❌'
        print(f"   {status} {display_name}: {count} 条记录")
    
    stock_info_status = '✅' if data_check.get('stock_info', {}).get('name') else '❌'
    print(f"   {stock_info_status} 公司基本信息")


if __name__ == "__main__":
    main()