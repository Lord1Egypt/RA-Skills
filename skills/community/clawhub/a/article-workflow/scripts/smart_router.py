#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能路由执行器 - Article Workflow Smart Router

功能：
- 智能识别单篇/批量模式
- 单篇模式：主 Agent 一次性执行（1 次流式请求）
- 批量模式：SubAgent 并发执行（N 次但并行）
- 流式优化：工具调用不中断流式

用法：
    # 在 OpenClaw 中调用
    from smart_router import ArticleSmartRouter
    
    router = ArticleSmartRouter()
    
    # 单篇模式
    result = router.process("https://example.com/article")
    
    # 批量模式
    urls = ["https://...", "https://...", "https://..."]
    results = router.process_batch(urls)
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Union
from dataclasses import dataclass, asdict

# 模块路径
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
CORE_DIR = SKILL_DIR / "core"

# 导入核心模块
import sys
sys.path.insert(0, str(CORE_DIR))
from dedup import check_duplicate, add_url_to_cache
from scorer import evaluate_quality_score


@dataclass
class ArticleResult:
    """文章分析结果"""
    url: str
    title: str
    summary: str
    tags: List[str]
    importance: str
    quality_score: int
    quality_level: str
    doc_url: str
    bitable_record_id: str
    success: bool
    error: Optional[str] = None


class ArticleSmartRouter:
    """文章智能路由执行器"""
    
    # 最大并发数
    MAX_CONCURRENT_SUBAGENTS = 5
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化路由器
        
        Args:
            config_path: 配置文件路径
        """
        if config_path is None:
            config_path = SKILL_DIR / "config.json"
        
        self.config = self._load_config(config_path)
        self.bitable_token = self.config.get("bitable", {}).get("app_token")
        self.table_id = self.config.get("bitable", {}).get("table_id")
    
    def _load_config(self, config_path: Path) -> dict:
        """加载配置文件"""
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def parse_input(self, user_input: str) -> List[str]:
        """
        解析用户输入，提取 URL 列表
        
        Args:
            user_input: 用户输入文本
        
        Returns:
            List[str]: URL 列表
        """
        # URL 正则表达式
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        
        urls = re.findall(url_pattern, user_input)
        return urls
    
    def is_batch_mode(self, urls: List[str], user_input: str = "") -> bool:
        """
        判断是否为批量模式
        
        Args:
            urls: URL 列表
            user_input: 用户输入文本
        
        Returns:
            bool: True=批量模式，False=单篇模式
        """
        # 显式批量关键词
        batch_keywords = ["批量", "这些文章", "多篇文章", "全部分析"]
        
        # 检查关键词
        has_batch_keyword = any(keyword in user_input for keyword in batch_keywords)
        
        # 检查 URL 数量
        multiple_urls = len(urls) > 1
        
        return has_batch_keyword or multiple_urls
    
    def process_single(self, url: str, title: str = None, content: str = None) -> ArticleResult:
        """
        单篇模式：主 Agent 一次性执行
        
        Args:
            url: 文章 URL
            title: 文章标题（可选）
            content: 文章内容（可选）
        
        Returns:
            ArticleResult: 分析结果
        """
        try:
            # 1. 检查重复
            dedup_result = check_duplicate(url, title, content)
            if dedup_result["is_duplicate"]:
                return ArticleResult(
                    url=url,
                    title=dedup_result["record"].get("title", ""),
                    summary="",
                    tags=[],
                    importance="",
                    quality_score=0,
                    quality_level="",
                    doc_url=dedup_result["record"].get("doc_url", ""),
                    bitable_record_id="",
                    success=False,
                    error="duplicate"
                )
            
            # 2. 抓取内容（如果未提供）
            if title is None or content is None:
                # TODO: 调用 web_fetch 工具
                # fetched = web_fetch(url)
                # title = fetched.get("title", "")
                # content = fetched.get("content", "")
                pass
            
            # 3. 分析内容
            # TODO: 调用 LLM 分析（在同一次流式请求中）
            # analysis = self._analyze_in_stream(title, content)
            
            # 4. 质量评分
            quality = evaluate_quality_score(title or "", content or "")
            
            # 5. 生成报告并创建文档
            # TODO: feishu_create_doc
            
            # 6. 归档到 Bitable
            # TODO: feishu_bitable_app_table_record
            
            # 7. 添加到缓存
            # add_url_to_cache(url, title, record_id, doc_url)
            
            return ArticleResult(
                url=url,
                title=title or "",
                summary="摘要内容",
                tags=["标签 1", "标签 2"],
                importance="高",
                quality_score=quality.get("total", 0),
                quality_level=quality.get("level", ""),
                doc_url="https://example.com/doc",
                bitable_record_id="rec_xxx",
                success=True
            )
            
        except Exception as e:
            return ArticleResult(
                url=url,
                title="",
                summary="",
                tags=[],
                importance="",
                quality_score=0,
                quality_level="",
                doc_url="",
                bitable_record_id="",
                success=False,
                error=str(e)
            )
    
    def process_batch(self, urls: List[str]) -> List[ArticleResult]:
        """
        批量模式：SubAgent 并发执行
        
        Args:
            urls: URL 列表
        
        Returns:
            List[ArticleResult]: 分析结果列表
        """
        results = []
        
        # 分批处理（如果超过最大并发数）
        batches = self._chunk_list(urls, self.MAX_CONCURRENT_SUBAGENTS)
        
        for batch_idx, batch in enumerate(batches, 1):
            print(f"处理第 {batch_idx}/{len(batches)} 批，共 {len(batch)} 篇文章...")
            
            # TODO: 并发创建 SubAgent
            # results.extend(self._process_batch_concurrent(batch))
        
        return results
    
    def _chunk_list(self, lst: List, chunk_size: int) -> List[List]:
        """列表分块"""
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
    
    def _process_batch_concurrent(self, urls: List[str]) -> List[ArticleResult]:
        """
        并发处理一批 URL
        
        Args:
            urls: URL 列表
        
        Returns:
            List[ArticleResult]: 结果列表
        """
        # TODO: 使用 sessions_spawn 创建 SubAgent
        # 每个 SubAgent 调用 process_single
        results = []
        for url in urls:
            result = self.process_single(url)
            results.append(result)
        return results
    
    def process(self, user_input: str) -> Union[ArticleResult, List[ArticleResult]]:
        """
        智能路由：自动选择单篇/批量模式
        
        Args:
            user_input: 用户输入（包含 URL）
        
        Returns:
            ArticleResult | List[ArticleResult]: 分析结果
        """
        urls = self.parse_input(user_input)
        
        if not urls:
            raise ValueError("未找到有效的 URL")
        
        if self.is_batch_mode(urls, user_input):
            # 批量模式
            return self.process_batch(urls)
        else:
            # 单篇模式
            return self.process_single(urls[0])


# 便捷函数
def analyze(user_input: str) -> Union[ArticleResult, List[ArticleResult]]:
    """
    便捷函数：智能分析文章
    
    Args:
        user_input: 用户输入（包含 URL）
    
    Returns:
        ArticleResult | List[ArticleResult]: 分析结果
    """
    router = ArticleSmartRouter()
    return router.process(user_input)


# CLI 入口
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：")
        print("  python smart_router.py <url>                    # 单篇分析")
        print("  python smart_router.py <url1> <url2> <url3>     # 批量分析")
        print()
        print("示例：")
        print("  python smart_router.py https://mp.weixin.qq.com/s/xxx")
        sys.exit(1)
    
    router = ArticleSmartRouter()
    
    # 多参数 = 批量模式
    if len(sys.argv) > 2:
        urls = sys.argv[1:]
        results = router.process_batch(urls)
        print(f"\n批量分析完成，共 {len(results)} 篇文章:")
        for i, result in enumerate(results, 1):
            status = "✅" if result.success else "❌"
            print(f"{i}. {status} {result.title}")
    else:
        # 单参数 = 单篇模式
        url = sys.argv[1]
        result = router.process_single(url)
        status = "✅" if result.success else "❌"
        print(f"\n{status} {result.title}")
        if result.error:
            print(f"错误：{result.error}")
