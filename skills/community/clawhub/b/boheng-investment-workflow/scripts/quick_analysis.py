#!/usr/bin/env python3
"""
投资研究系统 - 快速分析入口
确保任何查询都调用8位分析师

用法:
    from quick_analysis import quick_analyze
    result = quick_analyze("000001")  # 平安银行

    # 或者在命令行
    python3 quick_analysis.py 000001
"""
import sys
import os

# 添加脚本路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from monitor import AShareMonitor
from financial_data import FinancialDataFetcher
from analysts import run_all_analysts, calculate_weighted_vote
from report_generator import generate_report, save_report


def quick_analyze(stock_code: str, use_akshare: bool = False, query_date: str = None) -> dict:
    """
    快速分析 - 自动调用8位分析师
    
    Args:
        stock_code: 6位股票代码
        use_akshare: 是否使用AKShare获取真实财务数据
        query_date: 查询日期（可选，格式: "YYYY-MM-DD"）
                   默认使用当前时间，可指定日期获取特定财报
        
    Returns:
        包含8位分析师结果的完整分析报告
    """
    # 1. 验证代码
    if not stock_code.isdigit() or len(stock_code) != 6:
        return {'error': f'无效股票代码: {stock_code}'}
    
    # 确认查询日期
    if query_date is None:
        from datetime import datetime
        query_date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"\n{'='*60}")
    print(f"📊 股票分析: {stock_code}")
    print(f"📅 查询日期: {query_date}")
    print('='*60)
    
    # 2. 获取行情
    print("📈 获取行情数据...")
    monitor = AShareMonitor()
    quote = monitor.get_quote(stock_code)
    
    if 'error' in quote:
        return quote
    
    name = quote.get('名称', '未知')
    print(f"✅ {name}: ¥{quote.get('现价')} ({quote.get('涨跌幅')})")
    
    # 3. 获取财务数据
    print("💰 获取财务数据...")
    fd = FinancialDataFetcher()
    valuation = fd.get_valuation_data(stock_code)
    
    # 准备财务数据字典 - 确保数值类型正确
    def safe_float(val, default=0.0):
        """安全转换为float"""
        if val is None:
            return default
        if isinstance(val, (int, float)):
            return float(val)
        # 尝试提取数字
        try:
            return float(str(val).replace('%', '').replace('万', '').replace('亿', ''))
        except:
            return default
    
    # 从估值数据获取PE/PB/股息率
    pe_val = safe_float(valuation.get('PE_TTM', 0))
    pb_val = safe_float(valuation.get('PB', 0))
    div_val = safe_float(valuation.get('股息率', 0))
    
    # 尝试baostock获取真实财务数据（推荐）
    roe_val = None
    baostock_fi = None  # 保存baostock完整数据
    
    try:
        from financial_data_baostock import FinancialDataFetcherBaostock
        baostock = FinancialDataFetcherBaostock()
        fi = baostock.get_financial_indicator(stock_code, query_date)
        baostock_fi = fi  # 保存完整数据
        roe_val = safe_float(fi.get('roe', 0))
        # baostock返回小数(0.24)，需转换为百分比(24.0)
        if roe_val and roe_val < 1:
            roe_val = roe_val * 100
        if roe_val:
            print(f"   ✅ baostock获取真实ROE: {roe_val}%")
        
        # 获取真实股息率
        try:
            div_yield = baostock.get_dividend_yield(stock_code)
            if div_yield and div_yield > 0:
                valuation['股息率'] = div_yield
                print(f"   ✅ baostock获取真实股息率: {div_yield}%")
        except Exception as e:
            print(f"   ⚠️ 股息率获取失败: {e}")
    except:
        print(f"   ⚠️ baostock无数据，尝试AKShare...")
        akshare_fi = None
        try:
            from financial_data_akshare import FinancialDataFetcherAKShare
            akshare = FinancialDataFetcherAKShare()
            akshare_fi = akshare.get_financial_indicator(stock_code)
            if akshare_fi:
                roe_val = safe_float(akshare_fi.get('roe', 0))
                print(f"   ✅ AKShare获取真实ROE: {roe_val}%")
        except Exception as e:
            print(f"   ⚠️ AKShare也无数据: {e}")
            akshare_fi = None
    
    # 标记数据来源
    if baostock_fi:
        data_source = "baostock真实财报"
        is_estimated = False
    elif akshare_fi and roe_val and roe_val > 5:
        data_source = "AKShare真实财报"
        is_estimated = False
    else:
        data_source = "行业估算值"
        is_estimated = True
    
    # 使用真实值或行业估算 - 优先使用baostock，其次AKShare，最后估算
    if baostock_fi:
        # baostock数据（已转换为百分比）
        financial = {
            '财务指标': {
                'ROE': roe_val if roe_val else 11.0,
                '毛利率': round((safe_float(baostock_fi.get('gross_margin', 0)) or 0) * 100, 2),
                '净利率': round((safe_float(baostock_fi.get('net_margin', 0)) or 0) * 100, 2),
                '营收增速': safe_float(baostock_fi.get('revenue_growth', 5.0)),  # 优先用baostock
                '利润增速': safe_float(baostock_fi.get('profit_growth', 8.0)),  # 优先用baostock
                '资产负债率': round((safe_float(baostock_fi.get('debt_ratio', 0)) or 0) * 100, 1),
                '流动比率': safe_float(baostock_fi.get('current_ratio', 1.0)),
            },
            'report_period': baostock_fi.get('report_period', {'year': 2026, 'quarter': 1, 'display': '2026年1季度'}),  # 财报期间
        }
    elif akshare_fi:
        # AKShare数据
        financial = {
            '财务指标': {
                'ROE': roe_val if roe_val else 11.0,
                '毛利率': round(safe_float(akshare_fi.get('gross_margin', 30.0)), 2),
                '净利率': round(safe_float(akshare_fi.get('net_margin', 25.0)), 2),
                '营收增速': safe_float(akshare_fi.get('revenue_growth', 5.0)),
                '利润增速': safe_float(akshare_fi.get('profit_growth', 8.0)),
                '资产负债率': round(safe_float(akshare_fi.get('debt_ratio', 92.0)), 1),
                '流动比率': safe_float(akshare_fi.get('current_ratio', 1.0)),
            }
        }
    else:
        # 估算值
        financial = {
            '财务指标': {
                'ROE': roe_val if roe_val else 11.0,
                '毛利率': 30.0,
                '净利率': 25.0,
                '营收增速': 5.0,
                '利润增速': 8.0,
                '资产负债率': 92.0,
                '流动比率': 1.0,
            }
        }
    
    financial['估值'] = {
        'PE_TTM': pe_val,
        'PB': pb_val,
        '股息率': div_val,
        '总市值': valuation.get('总市值', 0),
    }
    financial['data_source'] = data_source  # 数据来源标记
    financial['is_estimated'] = is_estimated  # 是否为估算值
    
    # 附加到quote供分析师使用
    # 确保数值类型正确 - 核心：ROE必须是数字
    roe_str = financial['财务指标'].get('ROE', '0%')
    # 提取数字部分
    try:
        roe_val = float(str(roe_str).replace('%', ''))
    except:
        roe_val = 0
    
    quote['财务指标'] = {
        'ROE': roe_val,  # 必须是数字
        'PE': float(valuation.get('PE_TTM', 0)),
        'PB': float(valuation.get('PB', 0)),
        '股息率': float(valuation.get('股息率', 0)),
    }
    quote['估值'] = valuation
    quote['股息率'] = float(valuation.get('股息率', 0))
    
    # 4. 📰 获取新闻数据（作为情绪分析师的参考）
    print("📰 获取最新新闻...")
    news_data = []
    try:
        from stock_news import get_stock_news
        news_data = get_stock_news(stock_code, name, limit=5)
        if news_data:
            print(f"   ✅ 获取到 {len(news_data)} 条新闻")
            # 显示新闻摘要
            for i, n in enumerate(news_data[:3]):
                is_mock = " [模拟]" if n.get('is_mock') else ""
                print(f"   {i+1}. {n['title'][:40]}...{is_mock}")
        else:
            print("   ⚠️ 暂无新闻数据")
    except Exception as e:
        print(f"   ⚠️ 新闻获取失败: {e}")
    
    # 5. 获取行业信息
    try:
        fd = FinancialDataFetcher()
        industry_info = fd.get_industry_info(stock_code)
        financial['行业'] = industry_info
        print(f"   ✅ 行业信息: {industry_info.get('行业', '未知')}")
    except Exception as e:
        print(f"   ⚠️ 行业信息获取失败: {e}")
    
    # 6. 🎯 核心：运行8位分析师（含新闻参考）
    print("🔍 运行8位专业分析师...")
    print("-" * 40)
    
    analyst_results = run_all_analysts(quote, financial, news_data)
    
    # 5. 显示8位分析师结果
    stock_name = name  # 保存股票名称，避免被分析师名字覆盖
    for r in analyst_results:
        vote_symbol = r['vote']
        analyst_name = r['name']
        weight = r['weight']
        reason = r['reason'][:50] + '...' if len(r['reason']) > 50 else r['reason']
        print(f"{vote_symbol} [{weight}x] {analyst_name}: {reason}")
    
    # 6. 计算加权投票
    final_vote, final_score = calculate_weighted_vote(analyst_results)
    
    print("-" * 40)
    print(f"📊 最终结论: {final_vote} (得分: {final_score:.2f})")
    print('='*60)
    
    # 7. 返回完整结果
    return {
        'code': stock_code,
        'name': stock_name,
        'quote': quote,
        'financial': financial,
        'valuation': valuation,
        'news_data': news_data,  # 添加新闻数据
        'analyst_results': analyst_results,
        'final_vote': final_vote,
        'final_score': final_score,
    }


def run_quality_check(result: dict, stock_code: str, stock_name: str = None) -> dict:
    """
    质检功能 - 检查分析流程是否符合预期
    
    质检项目：
    1. 报告文件是否生成
    2. 数据获取是否成功
    3. 分析师是否全部调用
    4. 投票计算是否正确
    5. 财务数据完整性
    6. 估值数据是否获取
    7. 数据来源标识
    """
    import pandas as pd
    import os
    
    check_items = []
    all_passed = True
    
    # 1. 检查报告文件生成
    reports_dir = os.path.expanduser("~/.openclaw/workspace/investment/reports/")
    report_files = []
    if os.path.exists(reports_dir):
        prefix = f"{pd.Timestamp.now().strftime('%Y-%m-%d')}_{stock_code}"
        for f in os.listdir(reports_dir):
            if f.startswith(prefix):
                report_files.append(f)
    
    if report_files:
        check_items.append({
            'item': '报告文件生成',
            'status': '✅',
            'detail': f"已生成: {report_files[0]}"
        })
    else:
        check_items.append({
            'item': '报告文件生成',
            'status': '❌',
            'detail': f"未找到报告文件"
        })
        all_passed = False
    
    # 2. 检查数据获取
    financial = result.get('financial', {})
    data_source = financial.get('data_source', '未知')
    is_estimated = financial.get('is_estimated', True)
    
    if '真实' in data_source:
        check_items.append({
            'item': '财务数据获取',
            'status': '✅',
            'detail': f"{data_source}"
        })
    else:
        check_items.append({
            'item': '财务数据获取',
            'status': '⚠️',
            'detail': f"{data_source}"
        })
    
    # 3. 检查分析师调用
    analyst_results = result.get('analyst_results', [])
    if len(analyst_results) >= 8:
        check_items.append({
            'item': '分析师调用',
            'status': '✅',
            'detail': f"{len(analyst_results)}位分析师全部调用"
        })
    else:
        check_items.append({
            'item': '分析师调用',
            'status': '❌',
            'detail': f"仅调用 {len(analyst_results)}/8 位"
        })
        all_passed = False
    
    # 4. 检查投票计算
    final_vote = result.get('final_vote', '')
    final_score = result.get('final_score', 0)
    if final_vote and final_score:
        check_items.append({
            'item': '投票计算',
            'status': '✅',
            'detail': f"{final_vote}, 得分: {final_score:.2f}"
        })
    else:
        check_items.append({
            'item': '投票计算',
            'status': '❌',
            'detail': "投票结果异常"
        })
        all_passed = False
    
    # 5. 检查财务数据完整性
    fi = financial.get('财务指标', {})
    required_fields = ['ROE', '毛利率', '净利率']
    missing = [f for f in required_fields if not fi.get(f)]
    if not missing:
        check_items.append({
            'item': '财务数据完整性',
            'status': '✅',
            'detail': f"ROE:{fi.get('ROE')}%, 毛利率:{fi.get('毛利率')}%, 净利率:{fi.get('净利率')}%"
        })
    else:
        check_items.append({
            'item': '财务数据完整性',
            'status': '❌',
            'detail': f"缺失字段: {missing}"
        })
        all_passed = False
    
    # 6. 检查估值数据 - 从quote['估值']或quote['财务指标']获取
    quote_data = result.get('quote', {})
    # 优先从quote['估值']获取（包含完整的PE_TTM/PB）
    valuation = quote_data.get('估值', {})
    pe_val = valuation.get('PE_TTM', 0) or quote_data.get('财务指标', {}).get('PE', 0)
    pb_val = valuation.get('PB', 0) or quote_data.get('财务指标', {}).get('PB', 0)
    
    if pe_val or pb_val:
        check_items.append({
            'item': '估值数据获取',
            'status': '✅',
            'detail': f"PE:{pe_val}, PB:{pb_val}"
        })
    else:
        check_items.append({
            'item': '估值数据获取',
            'status': '⚠️',
            'detail': "PE/PB为0"
        })
    
    # 7. 检查数据来源标识
    if data_source != '未知':
        check_items.append({
            'item': '数据来源标识',
            'status': '✅',
            'detail': f"{data_source}, 估算:{is_estimated}"
        })
    else:
        check_items.append({
            'item': '数据来源标识',
            'status': '⚠️',
            'detail': "未标注数据来源"
        })
    
    return {
        'all_passed': all_passed,
        'check_items': check_items,
        'summary': f"通过 {sum(1 for c in check_items if c['status'] == '✅')}/{len(check_items)}"
    }


def print_quality_report(qc_result: dict):
    """打印质检报告"""
    print("\n" + "=" * 50)
    print("        📋 质检报告")
    print("=" * 50)
    
    for item in qc_result['check_items']:
        print(f"{item['status']} {item['item']}: {item['detail']}")
    
    print("-" * 50)
    print(f"📊 总体: {qc_result['summary']}")
    
    if qc_result['all_passed']:
        print("✅ 全部质检项通过！")
    else:
        print("⚠️ 部分质检项未通过，请检查")
    
    print("=" * 50)


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="投资分析快速入口")
    parser.add_argument("stock_code", nargs="?", help="股票代码")
    parser.add_argument("-d", "--date", help="查询日期（格式：YYYY-MM-DD）", default=None)
    
    args = parser.parse_args()
    
    if not args.stock_code:
        print("用法: python quick_analysis.py <股票代码> [-d YYYY-MM-DD]")
        print("示例: python quick_analysis.py 000001 -d 2026-05-11")
        print("     : python quick_analysis.py 002594")
        sys.exit(1)
    
    stock_code = args.stock_code
    result = quick_analyze(stock_code, query_date=args.date)
    
    if 'error' in result:
        print(f"\n❌ 错误: {result['error']}")
        sys.exit(1)
    
    # 生成并保存报告
    name = result.get('name', '')
    report = generate_report(
        code=stock_code,
        name=name,
        quote=result['quote'],
        analyst_results=result['analyst_results'],
        final_vote=result['final_vote'],
        final_score=result['final_score'],
        financial=result['financial']
    )
    
    # 保存报告
    save_report(stock_code, name, report)
    
    # 运行质检
    qc = run_quality_check(result, stock_code, name)
    print_quality_report(qc)


if __name__ == "__main__":
    main()