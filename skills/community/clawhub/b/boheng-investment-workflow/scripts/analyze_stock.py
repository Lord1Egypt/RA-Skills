#!/usr/bin/env python3
"""
投资研究系统 - 股票分析入口（简化版）
用法：python analyze_stock.py <股票代码> [股票名称]

说明：
- 使用多数据源获取实时行情（腾讯/雪球/百度）
- AKShare财务数据接口可能较慢，建议在交易时间使用
"""
import sys
import os

# 添加脚本路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import WATCHLIST_FILE, REPORTS_DIR
from monitor import AShareMonitor
from analysts import run_all_analysts, calculate_weighted_vote
from report_generator import generate_report, save_report, generate_personalized_advice


def analyze_stock(code: str, name: str = None, use_akshare: bool = False, 
                  enable_trend: bool = True, enable_industry: bool = True) -> dict:
    """
    分析单只股票
    
    Args:
        code: 6位股票代码
        name: 股票名称（可选）
        use_akshare: 是否使用AKShare获取财务数据
        enable_trend: 是否启用财务趋势分析
        enable_industry: 是否启用行业对比分析
        
    Returns:
        分析结果字典
    """
    # 验证代码格式
    if not code.isdigit() or len(code) != 6:
        return {
            'error': f'无效的股票代码格式：{code} (应为6位数字)'
        }
    
    print(f"\n{'='*60}")
    print(f"📊 开始分析 {code}")
    print('='*60)
    
    # 获取实时行情（使用多数据源备用方案）
    print("📈 正在获取实时行情...")
    monitor = AShareMonitor()
    quote = monitor.get_quote(code)
    
    if 'error' in quote:
        return quote
    
    # 使用行情中的名称（如果没提供）
    if not name:
        name = quote.get('名称', '未知')
    
    print(f"✅ {code} {name}: ¥{quote.get('现价', 'N/A')} ({quote.get('涨跌幅', 'N/A')})")
    
    # 财务数据 (默认获取，使用三级 fallback)
    financial = {}
    
    # 始终尝试获取财务数据（不管 use_akshare 参数）
    # use_akshare 参数现在主要用于控制是否使用 AKShare 的特殊功能
    try:
        from financial_data import FinancialDataFetcher
        fetcher = FinancialDataFetcher(delay=0.3)
        
        print("\n📊 正在获取财务数据（AKShare/baostock/估算）...")
        print("   ⏳ 这可能需要一些时间，请耐心等待...")
        
        # 财务指标
        financial['财务指标'] = fetcher.get_financial_indicators(code)
        
        # 估值数据
        financial['估值'] = fetcher.get_valuation_data(code)
        
        # 历史估值
        financial['估值分位'] = fetcher.get_historical_pe_pb(code)
        
        # K线数据
        financial['技术指标'] = fetcher.get_kline_data(code)
        
        # 资金流向
        financial['资金流向'] = fetcher.get_fund_flow(code)
        
        # 行业信息
        financial['行业'] = fetcher.get_industry_info(code)
        
        print("   ✅ 财务数据获取完成")
        
    except Exception as e:
            print(f"⚠️ 财务数据获取失败: {str(e)}")
            print("   将使用行情数据进行简化分析...")
            financial = {}
    
    # 显示财务数据概览
    if financial:
        print("\n" + "=" * 60)
        print("📊 财务数据概览")
        print("=" * 60)
        
        fi = financial.get('财务指标', {})
        if fi and 'error' not in fi:
            print(f"\n📈 盈利能力：")
            print(f"   ROE: {fi.get('ROE', 0):.2f}%  |  毛利率: {fi.get('毛利率', 0):.2f}%  |  净利率: {fi.get('净利率', 0):.2f}%")
            print(f"\n📊 成长能力：")
            print(f"   营收增速: {fi.get('营收增速', 0):.2f}%  |  利润增速: {fi.get('利润增速', 0):.2f}%")
        else:
            print("\n⚠️ 财务指标数据暂不可用")
        
        ev = financial.get('估值分位', {})
        if ev and 'error' not in ev:
            print(f"\n💰 估值指标：")
            print(f"   PE: {ev.get('PE当前', 0)}倍 ({ev.get('PE分位', 0)}%分位)  |  PB: {ev.get('PB当前', 0)}倍")
            print(f"   估值评级: {ev.get('估值评级', '-')}")
        
        valuation = financial.get('估值', {})
        if valuation and 'error' not in valuation:
            print(f"   股息率: {valuation.get('股息率', 0):.2f}%")
    
    # 财务趋势分析（新增）
    trend_result = None
    if enable_trend and use_akshare:
        try:
            print("\n" + "=" * 60)
            print("📈 财务趋势分析...")
            print("=" * 60)
            
            from financial_trend import analyze_stock_trend
            trend_result = analyze_stock_trend(code, years=5)
            
            if "error" not in trend_result:
                print(trend_result.get("report", ""))
                
                # 将风险信号添加到财务数据
                if trend_result.get("risks"):
                    financial['趋势风险'] = trend_result['risks']
            else:
                print(f"⚠️ 趋势分析失败: {trend_result.get('error')}")
                
        except Exception as e:
            print(f"⚠️ 趋势分析失败: {str(e)}")
    
    # 行业对比分析（新增）
    industry_result = None
    if enable_industry and use_akshare:
        try:
            print("\n" + "=" * 60)
            print("🏭 行业对比分析...")
            print("=" * 60)
            
            from industry_comparison import analyze_industry_comparison
            industry_result = analyze_industry_comparison(code, name or quote.get('名称', ''))
            
            if "error" not in industry_result:
                print(industry_result.get("report", ""))
                
                # 将行业排名添加到财务数据
                if industry_result.get("ranking"):
                    financial['行业排名'] = industry_result['ranking']
            else:
                print(f"⚠️ 行业分析失败: {industry_result.get('error')}")
                
        except Exception as e:
            print(f"⚠️ 行业分析失败: {str(e)}")
    
    # 运行8位分析师
    print("\n" + "=" * 60)
    print("🔍 启动8位分析师进行多维度分析...")
    print("=" * 60)
    
    analyst_results = run_all_analysts(quote, financial)
    
    # 计算加权投票
    final_vote, final_score = calculate_weighted_vote(analyst_results)
    
    # 生成报告
    report = generate_report(
        code=code,
        name=name,
        quote=quote,
        analyst_results=analyst_results,
        final_vote=final_vote,
        final_score=final_score,
        financial=financial
    )
    
    # 生成个性化投资建议
    print("\n💡 正在生成个性化投资建议...")
    personalized_advice = generate_personalized_advice(
        code=code,
        name=name,
        quote=quote,
        financial=financial,
        analyst_results=analyst_results,
        final_vote=final_vote,
        final_score=final_score,
        user_profile=None,  # 自动从 USER.md 加载
        graham_score=None   # 自动计算
    )
    
    # 保存报告
    os.makedirs(REPORTS_DIR, exist_ok=True)
    report_path = save_report(code, name, report + personalized_advice)
    
    # 输出报告
    print()
    print(report)
    print(personalized_advice)
    print()
    print(f"📄 报告已保存至：{report_path}")
    
    return {
        'code': code,
        'name': name,
        'quote': quote,
        'financial': financial,
        'analyst_results': analyst_results,
        'final_vote': final_vote,
        'final_score': final_score,
        'report_path': report_path
    }


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法：python analyze_stock.py <股票代码> [股票名称] [--akshare]")
        print("\n示例:")
        print("  python analyze_stock.py 600919                    # 快速分析（仅行情）")
        print("  python analyze_stock.py 600919 江苏银行            # 指定名称")
        print("  python analyze_stock.py 600919 --akshare           # 使用AKShare获取财务数据")
        sys.exit(1)
    
    code = sys.argv[1]
    name = None
    use_akshare = False
    
    # 解析参数
    enable_trend = True
    enable_industry = True
    
    for arg in sys.argv[2:]:
        if arg == '--akshare':
            use_akshare = True
        elif arg == '--no-trend':
            enable_trend = False
        elif arg == '--no-industry':
            enable_industry = False
        else:
            name = arg
    
    result = analyze_stock(code, name, use_akshare, enable_trend, enable_industry)
    
    if 'error' in result:
        print(f"\n❌ 错误：{result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()