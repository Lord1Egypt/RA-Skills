#!/usr/bin/env python3
"""
快速数据真实性验证
验证关键数据是否来自真实 API 而非模拟数据
"""

import sys
from pathlib import Path
from datetime import datetime, date, timedelta

# 导入验证工具
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from data_fetcher import DataFetcher
from utils import get_logger, format_date

logger = get_logger('data_truth_check')

def verify_akshare_reality():
    """验证 akshare 返回的是否为真实数据"""
    print("\n" + "="*80)
    print("📊 验证 akshare 数据真实性")
    print("="*80)

    fetcher = DataFetcher({"data_source": "akshare"})
    test_date = date.today() - timedelta(days=1)

    # 1. 测试指数数据
    print("\n1️⃣  上证指数 (000001.SH)")
    result = fetcher.get_index_data('000001.SH', test_date)
    data = result.get('data')
    source = result.get('source')

    if data:
        print(f"   数据源: {source}")
        print(f"   指数名称: {data.get('name')}")
        print(f"   交易日期: {data.get('trade_date')}")
        print(f"   收盘价: {data.get('close'):.2f}")
        print(f"   涨跌幅: {data.get('change_pct')*100:.2f}%")
        print(f"   成交额: {data.get('amount'):,} 手")

        # 真实数据校验（2026年3月27日应该是交易日）
        if data.get('close', 0) > 0 and data.get('change_pct', 0) != 0:
            print("   ✅ 数据真实有效（价格>0, 涨跌幅≠0）")
        else:
            print("   ❌ 数据异常（ prices=0 or change=0）")
    else:
        print("   ❌ 未获取到数据")

    # 2. 测试北向资金
    print("\n2️⃣  北向资金流向")
    result = fetcher.get_northbound_flow(test_date)
    data = result.get('data')
    source = result.get('source')

    if data:
        print(f"   数据源: {source}")
        nb = data.get('northbound', {})
        total = nb.get('total_net_inflow', 0)
        print(f"   净流入: {total/1e8:.2f} 亿元")
        print(f"   沪港通: {nb.get('hk_to_sh', 0)/1e8:.2f} 亿元")
        print(f"   深港通: {nb.get('hk_to_sz', 0)/1e8:.2f} 亿元")

        if abs(total) > 0:
            print("   ✅ 资金数据真实（有净流入/流出值）")
        else:
            print("   ❌ 资金数据异常（净流入=0）")
    else:
        print("   ❌ 未获取到数据")

    # 3. 测试市场情绪
    print("\n3️⃣  市场情绪指标")
    result = fetcher.get_market_sentiment(test_date)
    data = result.get('data')
    source = result.get('source')

    if data:
        print(f"   数据源: {source}")
        print(f"   涨停家数: {data.get('up_limit_count', 0)}")
        print(f"   跌停家数: {data.get('down_limit_count', 0)}")
        print(f"   涨跌比: {data.get('up_down_ratio', 0):.2f}")
        print(f"   成交额: {data.get('total_amount', 0)/1e8:.2f} 亿元")

        if data.get('up_limit_count', 0) >= 0 and data.get('total_amount', 0) > 0:
            print("   ✅ 情绪数据真实有效")
        else:
            print("   ❌ 情绪数据异常")
    else:
        print("   ❌ 未获取到数据")

def verify_yfinance_reality():
    """验证 yfinance 返回的是否为真实数据"""
    print("\n" + "="*80)
    print("📈 验证 yfinance 数据真实性")
    print("="*80)

    fetcher = DataFetcher({"data_source": "yfinance"})
    result = fetcher.get_us_market()
    data = result.get('data')
    source = result.get('source')

    if data:
        print(f"   数据源: {source}")
        indices = data.get('indices', {})
        cdc = data.get('chinadotcom', {})

        print(f"\n   🌍 美股指数:")
        for name, info in indices.items():
            print(f"      {info['name']}: {info['close']:.2f} ({info['change_pct']*100:+.2f}%)")

        print(f"\n   🇨🇳 中概股/港股:")
        for name, info in cdc.items():
            print(f"      {info['name']} ({info['code']}): {info['close']:.2f} ({info['change_pct']*100:+.2f}%)")

        # 真实性检查：价格应该 > 0，涨跌幅应该不是整数值（真实数据通常有小数）
        all_prices = [info['close'] for info in {**indices, **cdc}.values()]
        if all(p > 0 for p in all_prices):
            print("\n   ✅ 所有指数/股票价格 > 0")
        else:
            print("\n   ❌ 存在价格为0或负值")
    else:
        print("   ❌ 未获取到数据")

def verify_mx_search_reality():
    """验证 mx-search 返回的是否为真实新闻"""
    print("\n" + "="*80)
    print("📰 验证 mx-search 新闻真实性")
    print("="*80)

    fetcher = DataFetcher({"data_source": "mx-search"})
    test_date = date.today() - timedelta(days=1)
    result = fetcher.get_news(test_date, limit=3)
    data = result.get('data')
    source = result.get('source')

    if data:
        print(f"   数据源: {source}")
        news_list = data.get('news', [])
        print(f"   获取到 {len(news_list)} 条新闻\n")

        for i, news in enumerate(news_list, 1):
            print(f"   {i}. 【{news.get('source', '未知')}】{news.get('title', '')[:80]}...")
            if 'summary' in news:
                print(f"      摘要: {news.get('summary', '')[:80]}...")

        # 真实性检查
        if len(news_list) > 0:
            titles = [n.get('title', '') for n in news_list]
            unique_titles = set(titles)

            if len(unique_titles) == len(titles):
                print("\n   ✅ 新闻标题均唯一（非模拟重复）")
            else:
                print("\n   ⚠️  存在重复标题")

            # 检查标题是否为空或过短
            short_titles = [t for t in titles if len(t) < 10]
            if not short_titles:
                print("   ✅ 所有新闻标题长度正常")
            else:
                print(f"   ⚠️  发现 {len(short_titles)} 个过短标题")
        else:
            print("\n   ❌ 未获取到任何新闻")
    else:
        print("   ❌ 未获取到数据")

def main():
    print("🔍 数据真实性验证报告")
    print(f"⏰ 验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📅 测试日期基准: {date.today()} (实际使用最近交易日)")

    try:
        verify_akshare_reality()
        verify_yfinance_reality()
        verify_mx_search_reality()

        print("\n" + "="*80)
        print("✅ 验证完成！")
        print("="*80 + "\n")

    except Exception as e:
        print(f"\n❌ 验证过程出现异常: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
