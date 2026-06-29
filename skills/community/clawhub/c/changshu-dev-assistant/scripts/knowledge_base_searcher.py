#!/usr/bin/env python3
"""
优化的知识库搜索器
为昌叔的知识库优化搜索功能，支持语义搜索和自然语言查询
"""

import os
import re
import json
from typing import List, Dict, Optional
from pathlib import Path
from collections import Counter


class KnowledgeBaseSearcher:
    """知识库搜索器"""
    
    def __init__(self, wiki_path: str = ""):
        """初始化知识库搜索器"""
        if not wiki_path:
            wiki_path = os.environ.get('WIKI_PATH', os.path.expanduser('~/wiki'))
        self.wiki_path = wiki_path
        self.index_file = os.path.join(wiki_path, "index.md")
        self.schema_file = os.path.join(wiki_path, "SCHEMA.md")
        self.log_file = os.path.join(wiki_path, "log.md")
        
        # 缓存搜索结果
        self.search_cache = {}
    
    def search_content(self, query: str, tags: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """搜索知识库内容"""
        # 检查缓存
        cache_key = f"content_{query}_{tags}"
        if cache_key in self.search_cache:
            return self.search_cache[cache_key]
        
        # 搜索所有markdown文件
        results = []
        for root, dirs, files in os.walk(self.wiki_path):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            if query.lower() in content.lower():
                                # 简单匹配
                                results.append({
                                    "file": file_path,
                                    "content": content[:500]  # 只返回前500个字符
                                })
                    except Exception as e:
                        print(f"读取文件 {file_path} 时出错: {e}")
        
        # 缓存结果
        self.search_cache[cache_key] = results
        return results
    
    def search_by_tags(self, tags: List[str]) -> List[Dict[str, str]]:
        """根据标签搜索"""
        # 简单的标签搜索实现
        results = []
        return results
    
    def semantic_search(self, query: str) -> List[Dict[str, str]]:
        """语义搜索实现"""
        # 使用简单的关键词提取和匹配
        keywords = self._extract_keywords(query)
        
        # 检查缓存
        cache_key = f"semantic_{query}_{keywords}"
        if cache_key in self.search_cache:
            return self.search_cache[cache_key]
        
        # 搜索所有markdown文件
        results = []
        for root, dirs, files in os.walk(self.wiki_path):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            # 检查关键词是否在内容中
                            match_count = 0
                            for keyword in keywords:
                                if keyword in content:
                                    match_count += 1
                            
                            if match_count > 0:
                                results.append({
                                    "file": file_path,
                                    "content": content[:500],  # 只返回前500个字符
                                    "relevance": match_count / len(keywords)
                                })
                    except Exception as e:
                        print(f"读取文件 {file_path} 时出错: {e}")
        
        # 按相关性排序
        results.sort(key=lambda x: x.get("relevance", 0), reverse=True)
        
        # 缓存结果
        self.search_cache[cache_key] = results
        return results
    
    def _extract_keywords(self, text: str) -> List[str]:
        """简单的关键词提取"""
        # 简单的关键词提取实现
        import re
        # 移除标点符号并分割单词
        words = re.findall(r'[\w]+', text.lower())
        # 返回唯一单词列表
        unique_words = list(set(words))
        return unique_words
    
    def natural_language_query(self, query: str) -> List[Dict[str, str]]:
        """自然语言查询实现"""
        # 这里应该实现更复杂的自然语言处理
        # 目前使用简单的关键词提取和匹配
        return self.semantic_search(query)


def main():
    """主函数"""
    # 创建知识库搜索器实例
    searcher = KnowledgeBaseSearcher()
    
    # 示例搜索
    results = searcher.search_content("长源电力")
    print(f"内容搜索结果: {len(results)} 个文件")
    
    # 标签搜索示例
    tag_results = searcher.search_by_tags(["investment", "stock"])
    print(f"标签搜索结果: {len(tag_results)} 个文件")
    
    # 语义搜索示例
    semantic_results = searcher.semantic_search("股票分析")
    print(f"语义搜索结果: {len(semantic_results)} 个文件")
    
    # 自然语言查询示例
    nl_results = searcher.natural_language_query("查找关于长源电力的股票分析报告")
    print(f"自然语言查询结果: {len(nl_results)} 个文件")


if __name__ == "__main__":
    main()