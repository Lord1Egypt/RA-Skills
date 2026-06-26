"""
Double Search Skill 示例代码
演示如何在机器人中使用双搜索功能
"""

import asyncio
from double_search import DoubleSearcher


async def example_basic_search():
    """示例1：基本搜索"""
    print("=" * 60)
    print("示例1: 基本搜索")
    print("=" * 60)

    searcher = DoubleSearcher()

    results = await searcher.search("人工智能发展趋势")

    return results


async def example_custom_query():
    """示例2：自定义搜索查询"""
    print("\n" + "=" * 60)
    print("示例2: 自定义搜索查询")
    print("=" * 60)

    searcher = DoubleSearcher()

    query = "2024年投资策略分析"
    results = await searcher.search(query)

    return results


async def example_no_merge():
    """示例3：不合并结果"""
    print("\n" + "=" * 60)
    print("示例3: 不合并结果")
    print("=" * 60)

    searcher = DoubleSearcher()

    # 不合并结果，查看每个搜索源的单独结果
    results = await searcher.search(
        query="机器学习算法",
        merge_results=False
    )

    print("\nTavily搜索结果:")
    for item in results.get('tavily', []):
        print(f"  - {item['title']}")

    print("\nKimi搜索结果:")
    for item in results.get('kimi', []):
        print(f"  - {item['title']}")

    return results


async def example_filtered_search():
    """示例4：过滤特定领域结果"""
    print("\n" + "=" * 60)
    print("示例4: 过滤财经领域结果")
    print("=" * 60)

    searcher = DoubleSearcher()

    results = await searcher.search("股票市场分析")

    # 过滤财经相关结果
    financial_results = [
        item for item in results.get('merged_results', [])
        if '财经' in item['snippet'] or '股票' in item['snippet'] or '市场' in item['snippet']
    ]

    print(f"\n找到 {len(financial_results)} 条财经相关结果:")
    for item in financial_results[:3]:
        print(f"  - {item['source']}: {item['title']}")

    return financial_results


async def example_market_analysis():
    """示例5：市场分析任务"""
    print("\n" + "=" * 60)
    print("示例5: 市场分析任务")
    print("=" * 60)

    searcher = DoubleSearcher()

    query = "2024年科技行业投资机会"
    results = await searcher.search(query)

    # 分析结果
    analysis = {
        "query": query,
        "total_results": len(results.get('merged_results', [])),
        "sources": results.get('source_breakdown', {}),
        "key_topics": extract_key_topics(results)
    }

    return analysis


def extract_key_topics(results):
    """从搜索结果中提取关键主题"""
    topics = set()

    for item in results.get('merged_results', []):
        snippet = item['snippet'].lower()
        if '人工智能' in snippet or 'AI' in snippet:
            topics.add('AI/人工智能')
        if '投资' in snippet or '基金' in snippet:
            topics.add('投资')
        if '市场' in snippet or '行情' in snippet:
            topics.add('市场分析')
        if '趋势' in snippet or '发展' in snippet:
            topics.add('趋势')

    return sorted(list(topics))


async def example_comparison():
    """示例6：比较不同搜索引擎的结果"""
    print("\n" + "=" * 60)
    print("示例6: 比较不同搜索引擎")
    print("=" * 60)

    searcher = DoubleSearcher()

    results = await searcher.search("区块链技术发展")

    # 比较不同搜索引擎的结果数量
    tavily_count = len(results.get('tavily', []))
    kimi_count = len(results.get('kimi', []))

    print(f"\n搜索引擎对比:")
    print(f"  Tavily: {tavily_count} 条结果")
    print(f"  Kimi:   {kimi_count} 条结果")
    print(f"  总计:   {tavily_count + kimi_count} 条结果")

    return results


async def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("Double Search Skill - 示例代码")
    print("=" * 60)

    try:
        # 运行示例
        await example_basic_search()
        await example_custom_query()
        await example_no_merge()
        await example_filtered_search()
        await example_market_analysis()
        await example_comparison()

        print("\n" + "=" * 60)
        print("✅ 所有示例运行完成")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
