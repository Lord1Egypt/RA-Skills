#!/usr/bin/env python3
"""
跨境电商选品工具 CLI
用法: cross-border <command> [args]
"""
import sys
import json
import argparse

# 确保项目根目录在 Python 路径
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services import KeywordAnalyzer, CompetitorScraper, ProfitCalculator, AIListingGenerator

# 全局服务实例
kw_analyzer = KeywordAnalyzer()
competitor_scraper = CompetitorScraper()
ai_listing_gen = AIListingGenerator()


def cmd_keyword(args):
    """关键词分析"""
    result = kw_analyzer.analyze(args.keyword)
    
    if args.json:
        print(json.dumps({
            "keyword": result.keyword,
            "search_volume": result.search_volume,
            "competition": result.competition,
            "competition_level": _competition_level(result.competition),
            "trend": result.trend,
            "related_keywords": result.related_keywords,
            "suggested_bid": result.suggested_bid
        }, ensure_ascii=False, indent=2))
        return
    
    print(f"\n📊 {result.keyword} 关键词分析")
    print("━" * 40)
    print(f"🔍 搜索量: {result.search_volume:,}/月")
    print(f"📈 竞争度: {result.competition:.0%} ({_competition_level(result.competition)})")
    print(f"📊 趋势: {_trend_emoji(result.trend)} {result.trend}")
    print(f"💰 参考竞价: ${result.suggested_bid:.2f}")
    print(f"🔗 相关词: {', '.join(result.related_keywords)}")
    print()


def cmd_keywords(args):
    """批量关键词分析"""
    keywords = [k.strip() for k in args.keywords.split(',')]
    results = kw_analyzer.batch_analyze(keywords)
    
    print(f"\n📊 批量关键词分析 ({len(results)}个)")
    print("━" * 60)
    
    for r in results:
        bar = _competition_bar(r.competition)
        print(f"  {r.keyword:<25} 搜索量:{r.search_volume:>10,}  {bar} {_trend_emoji(r.trend)}")
    print()


def cmd_profit(args):
    """利润计算"""
    calc = ProfitCalculator(args.platform or 'amazon')
    result = calc.calculate(
        product_cost=args.cost,
        shipping_cost=args.shipping or 0,
        selling_price=args.price,
        other_cost=args.other or 0,
        is_fba=args.fba
    )
    
    platform_name = "亚马逊" if args.platform == 'amazon' else "eBay"
    fba_tag = " FBA" if args.fba else ""
    
    print(f"\n💰 {platform_name}{fba_tag} 利润分析")
    print("━" * 40)
    print(f"📦 产品成本: ${result.product_cost:.2f}")
    print(f"🚢 运费: ${result.shipping_cost:.2f}")
    if args.fba or args.platform == 'amazon':
        print(f"🏭 平台费: ${result.platform_fee:.2f}")
        print(f"💳 推荐费 (15%): ${result.referral_fee:.2f}")
    print(f"📊 总成本: ${result.total_cost:.2f}")
    print(f"💵 售价: ${result.selling_price:.2f}")
    print("━" * 40)
    print(f"✅ 利润: ${result.profit:.2f}")
    print(f"📈 利润率: {result.profit_margin/100:.1%} ({_profit_status(result.profit_margin/100)})")
    print()


def cmd_suggest_price(args):
    """建议售价"""
    calc = ProfitCalculator(args.platform or 'amazon')
    suggested = calc.suggest_price(
        product_cost=args.cost,
        target_margin=args.margin / 100
    )
    print(f"\n💡 目标利润率 {args.margin}% 时，建议售价: ${suggested:.2f}")
    print()


def cmd_listing(args):
    """AI Listing生成"""
    kw_analysis = None
    competitor_data = None
    
    if args.include_analysis:
        kw_result = kw_analyzer.analyze(args.product_name)
        kw_analysis = {
            "keyword": kw_result.keyword,
            "search_volume": kw_result.search_volume,
            "competition": kw_result.competition,
            "related_keywords": kw_result.related_keywords
        }
        competitor_data = competitor_scraper.analyze_market(
            args.product_name, args.platform or 'amazon'
        )
    
    result = ai_listing_gen.generate(
        product_name=args.product_name,
        keyword_analysis=kw_analysis,
        competitor_data=competitor_data,
        target_market=args.market or 'US'
    )
    
    print(f"\n🤖 AI Listing: {args.product_name}")
    print("━" * 50)
    print(f"\n📝 标题:\n  {result.title}")
    print(f"\n⚡ 5点描述:")
    for i, point in enumerate(result.short_description.split('\n'), 1):
        if point.strip():
            print(f"  {i}. {point.strip()}")
    print(f"\n📄 完整描述:\n  {result.full_description}")
    print(f"\n🏷️ 关键词: {', '.join(result.keywords)}")
    if result.suggested_price:
        print(f"💵 建议售价: ${result.suggested_price:.2f}")
    print()


# ===== 辅助函数 =====

def _competition_level(c: float) -> str:
    if c >= 0.8: return "非常高"
    elif c >= 0.6: return "高"
    elif c >= 0.4: return "中等"
    elif c >= 0.2: return "低"
    else: return "非常低"

def _competition_bar(c: float) -> str:
    total = 20
    filled = int(c * total)
    return '█' * filled + '░' * (total - filled)

def _trend_emoji(t: str) -> str:
    return {"rising": "📈", "stable": "➡️", "falling": "📉"}.get(t, "➡️")

def _profit_status(m: float) -> str:
    if m >= 0.3: return "优秀"
    elif m >= 0.2: return "良好"
    elif m >= 0.1: return "一般"
    elif m >= 0: return "较低"
    else: return "亏损"


# ===== 主程序 =====

def main():
    parser = argparse.ArgumentParser(
        description="🛒 跨境电商选品工具 - 关键词分析/利润计算/AI Listing生成",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest='command', required=True)
    
    # keyword
    p_kw = sub.add_parser('keyword', help='分析单个关键词')
    p_kw.add_argument('keyword', help='要分析的关键词')
    p_kw.add_argument('--json', action='store_true', help='JSON格式输出')
    
    # keywords
    p_kws = sub.add_parser('keywords', help='批量分析关键词（逗号分隔）')
    p_kws.add_argument('keywords', help='多个关键词，逗号分隔')
    
    # profit
    p_pf = sub.add_parser('profit', help='计算利润')
    p_pf.add_argument('--cost', type=float, required=True, help='产品成本 ($)')
    p_pf.add_argument('--price', type=float, required=True, help='售价 ($)')
    p_pf.add_argument('--shipping', type=float, default=0, help='运费 ($)')
    p_pf.add_argument('--other', type=float, default=0, help='其他成本 ($)')
    p_pf.add_argument('--platform', default='amazon', choices=['amazon', 'ebay'], help='平台')
    p_pf.add_argument('--fba', action='store_true', help='使用FBA')
    
    # suggest-price
    p_sp = sub.add_parser('suggest-price', help='计算建议售价')
    p_sp.add_argument('--cost', type=float, required=True, help='产品成本 ($)')
    p_sp.add_argument('--margin', type=float, required=True, help='目标利润率 (%%)')
    p_sp.add_argument('--platform', default='amazon', choices=['amazon', 'ebay'], help='平台')
    
    # listing
    p_lt = sub.add_parser('listing', help='AI生成Listing')
    p_lt.add_argument('product_name', help='产品名称')
    p_lt.add_argument('--market', default='US', help='目标市场 (US/UK/DE...)')
    p_lt.add_argument('--platform', default='amazon', choices=['amazon', 'ebay'], help='平台')
    p_lt.add_argument('--include-analysis', action='store_true', help='包含关键词和竞品分析')
    
    args = parser.parse_args()
    
    if args.command == 'keyword':
        cmd_keyword(args)
    elif args.command == 'keywords':
        cmd_keywords(args)
    elif args.command == 'profit':
        cmd_profit(args)
    elif args.command == 'suggest-price':
        cmd_suggest_price(args)
    elif args.command == 'listing':
        cmd_listing(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
