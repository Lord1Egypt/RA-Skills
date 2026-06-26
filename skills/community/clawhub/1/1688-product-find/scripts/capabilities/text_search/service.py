# -*- coding: utf-8 -*-
"""
文本搜索能力实现
解析用户自然语言描述，提取商品关键词，执行搜索
"""

from typing import Dict, List, Any

from _http import search_products


class TextSearchExecutor:
    """文本搜索执行器"""
    
    def __init__(self, platform: str = "1688"):
        self.platform = platform
    
    def search(self, query: str, limit: int = 10,
               sort_type: str = None, score_level: str = "high",
               purchase_amount: int = 1,
               tags: str = "4306497", ic_tags: str = None) -> Dict[str, Any]:
        """
        执行文本搜索
        
        Args:
            query: 用户查询关键词
            limit: 返回数量
            sort_type: 排序类型（price_asc/price_desc/sold_desc/yx_desc）
            score_level: 相关性档位（high/medium/low）
            purchase_amount: 采购件数
            tags: TC标（品池标签），英文逗号分隔
            ic_tags: IC标（品池标签），英文逗号分隔
            
        Returns:
            搜索结果
        """
        # 执行 API 搜索
        results = self._search_via_api(query, limit, sort_type, score_level, purchase_amount, tags, ic_tags)
        
        return {
            "success": True,
            "query": query,
            "similar_products": results,
            "search_type": "text_search",
            "total_results": len(results)
        }
    
    def _search_via_api(self, query: str, limit: int,
                        sort_type: str = None, score_level: str = "high",
                        purchase_amount: int = 1,
                        tags: str = "4306497", ic_tags: str = None) -> List[Dict]:
        """通过 API 搜索"""
        request = {
            "query": query,
            "pageSize": limit,
            "purchaseAmount": purchase_amount
        }
        # 排序类型（可选）
        if sort_type:
            request["sortType"] = sort_type
        
        # 相关性档位（默认 high）
        if score_level:
            request["scoreLevel"] = score_level
        
        # 品池标签
        if tags:
            request["tags"] = tags
        if ic_tags:
            request["icTags"] = ic_tags
        
        return search_products(request)


# ========== 主入口函数 ==========

def text_search(query: str, platform: str = "1688", limit: int = 10,
                sort_type: str = None, score_level: str = "high",
                purchase_amount: int = 1,
                tags: str = "4306497", ic_tags: str = None) -> Dict[str, Any]:
    """
    文本搜索主函数
    
    Args:
        query: 用户搜索关键词
        platform: 目标平台
        limit: 返回数量
        sort_type: 排序类型（price_asc/price_desc/sold_desc/yx_desc）
        score_level: 相关性档位（high/medium/low）
        purchase_amount: 采购件数
        tags: TC标（品池标签），英文逗号分隔，默认 "4306497"
        ic_tags: IC标（品池标签），英文逗号分隔
        
    Returns:
        搜索结果
    """
    executor = TextSearchExecutor(platform=platform)
    return executor.search(query, limit=limit,
                           sort_type=sort_type, score_level=score_level,
                           purchase_amount=purchase_amount,
                           tags=tags, ic_tags=ic_tags)


if __name__ == "__main__":
    # 测试示例
    test_query = "黑色连帽卫衣"
    result = text_search(test_query)
    print(f"搜索：{test_query}")
    print(f"找到 {result['total_results']} 个商品")
