"""
Claw-News Result Aggregator
搜索结果聚合与去重模块
"""

import json
from typing import List, Dict, Set
from datetime import datetime
from search_engine import SearchResult


class ResultAggregator:
    """结果聚合器 - 去重、分类、排序"""
    
    def __init__(self):
        self.seen_urls: Set[str] = set()
        self.seen_hashes: Set[str] = set()
    
    def aggregate(self, search_results: List[Dict]) -> Dict[str, List[SearchResult]]:
        """
        聚合多个搜索结果
        
        Args:
            search_results: 多个搜索返回的结果列表
                [{"source": "kimi", "results": [SearchResult, ...]}, ...]
        
        Returns:
            按 interest_id 分类的结果字典
        """
        all_results = []
        
        for sr in search_results:
            if sr.get("success"):
                for result in sr.get("results", []):
                    if self._is_unique(result):
                        all_results.append(result)
        
        # 按 interest_id 分类
        categorized = {}
        for result in all_results:
            interest_id = getattr(result, 'interest_id', 'general')
            if interest_id not in categorized:
                categorized[interest_id] = []
            categorized[interest_id].append(result)
        
        # 对每个分类内的结果排序（按时间 + 相关性）
        for interest_id in categorized:
            categorized[interest_id] = self._sort_results(categorized[interest_id])
        
        return categorized
    
    def _is_unique(self, result: SearchResult) -> bool:
        """检查结果是否唯一（去重）"""
        # URL 去重
        normalized_url = self._normalize_url(result.url)
        if normalized_url in self.seen_urls:
            return False
        
        # Hash 去重
        if result.hash in self.seen_hashes:
            return False
        
        self.seen_urls.add(normalized_url)
        self.seen_hashes.add(result.hash)
        return True
    
    def _normalize_url(self, url: str) -> str:
        """规范化 URL 用于去重"""
        # 移除跟踪参数
        import re
        url = re.sub(r'[?&](utm_source|utm_medium|utm_campaign|ref|source)=[^&]*', '', url)
        # 移除末尾斜杠
        url = url.rstrip('/')
        # 转小写
        return url.lower()
    
    def _sort_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """对结果排序（时间倒序 + 质量评分）"""
        def score_result(r: SearchResult) -> float:
            score = 0.0
            
            # 时间因素（越新越高分）
            try:
                pub_date = datetime.fromisoformat(r.published_at.replace('Z', '+00:00'))
                hours_ago = (datetime.now() - pub_date).total_seconds() / 3600
                score += max(0, 24 - hours_ago)  # 24 小时内的新闻
            except:
                score += 12  # 默认中等分数
            
            # 内容质量因素
            if len(r.title) > 20:  # 标题足够长
                score += 2
            if len(r.summary) > 50:  # 摘要有内容
                score += 3
            if r.source and r.source not in ['unknown', '']:  # 有明确来源
                score += 2
            
            # 来源可信度（简单规则）
            trusted_sources = ['reuters', 'bloomberg', 'techcrunch', 'the verge', 
                             'bbc', 'cnn', '华尔街日报', '财新', '36kr', '知乎']
            if any(ts in r.source.lower() for ts in trusted_sources):
                score += 3
            
            return score
        
        return sorted(results, key=score_result, reverse=True)
    
    def deduplicate_by_similarity(self, results: List[SearchResult], 
                                   threshold: float = 0.8) -> List[SearchResult]:
        """
        基于标题相似度的去重（简单实现）
        
        Args:
            results: 原始结果列表
            threshold: 相似度阈值
        """
        if not results:
            return results
        
        unique_results = [results[0]]
        
        for result in results[1:]:
            is_duplicate = False
            for unique in unique_results:
                similarity = self._calculate_similarity(result.title, unique.title)
                if similarity >= threshold:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_results.append(result)
        
        return unique_results
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算两个文本的相似度（简单 Jaccard 实现）"""
        # 转小写并分词
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union)
    
    def merge_with_cache(self, new_results: List[SearchResult], 
                         cache_file: str = None) -> List[SearchResult]:
        """与缓存合并，避免重复推送"""
        # 简化实现：暂时直接返回新结果
        # 未来可以实现：读取已推送记录，过滤已推送的 URL
        return new_results
    
    def get_statistics(self, categorized_results: Dict[str, List[SearchResult]]) -> Dict:
        """生成统计信息"""
        total = sum(len(results) for results in categorized_results.values())
        by_source = {}
        by_api = {}
        
        for results in categorized_results.values():
            for r in results:
                by_source[r.source] = by_source.get(r.source, 0) + 1
                by_api[r.search_api] = by_api.get(r.search_api, 0) + 1
        
        return {
            "total_results": total,
            "categories": len(categorized_results),
            "by_source": by_source,
            "by_api": by_api
        }
