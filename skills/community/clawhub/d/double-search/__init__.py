"""
Double Search Skill - 双搜索功能实现
支持Tavily和Kimi两个搜索引擎的并行搜索和结果合并
"""

import asyncio
import os
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod


class SearchEngine(ABC):
    """搜索引擎抽象基类"""

    @abstractmethod
    async def search(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """执行搜索"""
        pass


class TavilySearch(SearchEngine):
    """Tavily搜索引擎实现"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")
        self.engine_name = "tavily"

        if not self.api_key:
            raise ValueError("TAVILY_API_KEY environment variable not set")

    async def search(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """
        执行Tavily搜索

        Args:
            query: 搜索查询
            **kwargs: 其他参数

        Returns:
            搜索结果列表
        """
        try:
            import aiohttp

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Accept": "application/json"
            }

            params = {
                "q": query,
                "max_results": kwargs.get("limit_per_source", 5),
                "format": "json"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://api.tavily.com/search",
                    headers=headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = []

                        for item in data.get("results", []):
                            results.append({
                                "title": item.get("title", ""),
                                "url": item.get("url", ""),
                                "snippet": item.get("content", ""),
                                "source": self.engine_name
                            })

                        return results
                    else:
                        error_text = await response.text()
                        raise Exception(f"Tavily API error: {response.status} - {error_text}")

        except ImportError:
            # 模拟搜索结果（用于演示）
            await asyncio.sleep(0.1)
            return [
                {
                    "title": f"Tavily结果: {query}",
                    "url": "https://tavily.com/demo",
                    "snippet": "这是Tavily搜索的模拟结果。实际使用时需要安装aiohttp库。",
                    "source": self.engine_name
                }
            ]


class KimiSearch(SearchEngine):
    """Kimi搜索引擎实现"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("KIMI_API_KEY")
        self.engine_name = "kimi"

        if not self.api_key:
            raise ValueError("KIMI_API_KEY environment variable not set")

    async def search(self, query: str, **kwargs) -> List[Dict[str, Any]]:
        """
        执行Kimi搜索

        Args:
            query: 搜索查询
            **kwargs: 其他参数

        Returns:
            搜索结果列表
        """
        try:
            import aiohttp

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "query": query,
                "max_results": kwargs.get("limit_per_source", 5)
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.moonshot.cn/v1/chat/completions",
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 200:
                        json_data = await response.json()

                        # 解析Kimi API响应
                        results = []
                        for choice in json_data.get("choices", []):
                            message = choice.get("message", {})
                            content = message.get("content", "")

                            # 简化解析（实际需要根据Kimi API返回格式调整）
                            results.append({
                                "title": content[:50] + "..." if len(content) > 50 else content,
                                "url": "https://kimi.com/search",
                                "snippet": content,
                                "source": self.engine_name
                            })

                        return results
                    else:
                        error_text = await response.text()
                        raise Exception(f"Kimi API error: {response.status} - {error_text}")

        except ImportError:
            # 模拟搜索结果（用于演示）
            await asyncio.sleep(0.1)
            return [
                {
                    "title": f"Kimi结果: {query}",
                    "url": "https://kimi.com/demo",
                    "snippet": "这是Kimi搜索的模拟结果。实际使用时需要安装aiohttp库。",
                    "source": self.engine_name
                }
            ]


class MultiSearchManager:
    """多搜索管理器"""

    def __init__(self):
        self.engines: Dict[str, SearchEngine] = {}
        self._load_engines()

    def _load_engines(self):
        """加载可用的搜索引擎"""
        try:
            if os.getenv("TAVILY_API_KEY"):
                self.engines["tavily"] = TavilySearch()
                print(f"✅ Tavily搜索引擎已加载")

            if os.getenv("KIMI_API_KEY"):
                self.engines["kimi"] = KimiSearch()
                print(f"✅ Kimi搜索引擎已加载")

            if not self.engines:
                raise ValueError("没有可用的搜索引擎API keys")

        except Exception as e:
            print(f"⚠️  警告: {e}")
            print(f"💡 提示: 请设置TAVILY_API_KEY和/或KIMI_API_KEY环境变量")

    async def search_all(
        self,
        query: str,
        limit_per_source: int = 5
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        同时搜索所有配置的搜索引擎

        Args:
            query: 搜索查询
            limit_per_source: 每个搜索引擎的结果数量

        Returns:
            各个搜索引擎的搜索结果
        """
        if not self.engines:
            raise ValueError("没有可用的搜索引擎")

        tasks = {}
        for name, engine in self.engines.items():
            tasks[name] = engine.search(query, limit_per_source=limit_per_source)

        # 并行执行所有搜索
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)

        # 整理结果
        final_results = {}
        for name, result in zip(tasks.keys(), results):
            if isinstance(result, Exception):
                print(f"⚠️  {name}搜索失败: {result}")
                final_results[name] = []
            else:
                final_results[name] = result

        return final_results

    def get_available_engines(self) -> List[str]:
        """获取可用的搜索引擎列表"""
        return list(self.engines.keys())


class DoubleSearcher:
    """双重搜索器 - 主要接口类"""

    def __init__(self):
        self.search_manager = MultiSearchManager()

    async def search(
        self,
        query: str,
        merge_results: bool = True,
        limit_per_source: int = 5
    ) -> Dict[str, Any]:
        """
        执行统一搜索

        Args:
            query: 搜索查询
            merge_results: 是否合并结果（默认True）
            limit_per_source: 每个搜索引擎的结果数量

        Returns:
            搜索结果字典
        """
        print(f"\n🔍 搜索查询: {query}")
        print(f"📊 可用搜索引擎: {', '.join(self.search_manager.get_available_engines())}")

        # 执行搜索
        source_results = await self.search_manager.search_all(
            query,
            limit_per_source=limit_per_source
        )

        # 构建响应
        response = {
            "query": query,
            "source_breakdown": source_results
        }

        # 合并结果（如果需要）
        if merge_results and source_results:
            response["merged_results"] = self._merge_results(source_results)
        elif source_results:
            response["results"] = source_results

        print(f"✅ 搜索完成，共找到 {len(response.get('merged_results', []))} 条结果\n")

        return response

    def _merge_results(self, source_results: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        合并来自不同搜索引擎的结果

        Args:
            source_results: 各搜索引擎的结果字典

        Returns:
            合并后的结果列表
        """
        merged = []

        for source, results in source_results.items():
            for result in results:
                # 添加来源标识
                result["source"] = source
                merged.append(result)

        # 按标题排序
        return sorted(merged, key=lambda x: x["title"].lower())


async def main():
    """主函数 - 用于测试"""
    searcher = DoubleSearcher()

    test_query = "人工智能发展趋势"

    print("=" * 60)
    print("Double Search 功能测试")
    print("=" * 60)

    results = await searcher.search(test_query)

    print("\n" + "=" * 60)
    print("搜索结果汇总")
    print("=" * 60)

    # 打印合并的结果
    for i, item in enumerate(results.get('merged_results', [])[:3], 1):
        print(f"\n{i}. [{item['source']}] {item['title']}")
        print(f"   链接: {item['url']}")
        print(f"   摘要: {item['snippet'][:100]}...")

    # 打印各搜索引擎的统计
    print("\n" + "=" * 60)
    print("搜索引擎统计")
    print("=" * 60)

    for source, results in results.get('source_breakdown', {}).items():
        print(f"{source.upper()}: {len(results)} 条结果")


if __name__ == "__main__":
    # 运行测试
    asyncio.run(main())
