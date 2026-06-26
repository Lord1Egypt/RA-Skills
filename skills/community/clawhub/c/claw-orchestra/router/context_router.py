"""
Context Router - 上下文精选路由

AOrchestra 的核心洞察之一：编排器精选任务相关的上下文，而不是全量传递。

上下文路由器负责：
1. 从历史记录中提取最相关的信息
2. 避免噪声干扰
3. 控制 token 消耗

路由策略：
1. 关键词匹配（快速、无成本）
2. Embedding 相似度（准确、需要模型）
3. LLM 判断（最准确、成本高）
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
import re
from collections import Counter


@dataclass
class ContextItem:
    """上下文条目"""
    content: str                    # 内容
    source: str = ""                # 来源（如 "subtask_1", "user_input"）
    relevance_score: float = 0.0    # 相关性分数 (0-1)
    tokens: int = 0                 # token 数量（估算）
    
    def __post_init__(self):
        if self.tokens == 0:
            self.tokens = self._estimate_tokens()
    
    def _estimate_tokens(self) -> int:
        """估算 token 数量（粗略：1 token ≈ 4 字符）"""
        return len(self.content) // 4


class ContextRouter:
    """
    上下文精选路由器
    
    从历史中精选最相关的上下文，避免噪声和 token 浪费
    
    Example:
        >>> router = ContextRouter(max_items=5)
        >>> history = ["搜索了 LangChain", "发现 3 个框架", "对比了性能"]
        >>> context = router.route("分析 CrewAI", history)
        >>> print(context)  # 最相关的 5 条
    """
    
    def __init__(
        self,
        max_items: int = 5,
        max_tokens: int = 2000,
        strategy: str = "hybrid",  # keyword | embedding | llm | hybrid
        verbose: bool = False,
    ):
        self.max_items = max_items
        self.max_tokens = max_tokens
        self.strategy = strategy
        self.verbose = verbose
    
    def route(
        self,
        task: str,
        history: List[str],
        additional_context: List[str] = None,
    ) -> List[str]:
        """
        从历史中精选上下文
        
        Args:
            task: 当前任务
            history: 历史记录列表
            additional_context: 额外上下文
            
        Returns:
            精选的上下文列表
        """
        if not history and not additional_context:
            return []
        
        # 构建候选列表
        candidates = []
        for i, item in enumerate(history):
            candidates.append(ContextItem(
                content=item,
                source=f"history_{i}",
            ))
        
        if additional_context:
            for i, item in enumerate(additional_context):
                candidates.append(ContextItem(
                    content=item,
                    source=f"additional_{i}",
                ))
        
        # 计算相关性分数
        candidates = self._score_relevance(task, candidates)
        
        # 排序并选择
        candidates.sort(key=lambda x: x.relevance_score, reverse=True)
        
        # 控制 token 数量
        selected = []
        total_tokens = 0
        
        for item in candidates:
            if len(selected) >= self.max_items:
                break
            if total_tokens + item.tokens > self.max_tokens:
                continue
            selected.append(item.content)
            total_tokens += item.tokens
        
        if self.verbose:
            print(f"\n📍 上下文路由:")
            print(f"   候选: {len(candidates)} 条")
            print(f"   选择: {len(selected)} 条 ({total_tokens} tokens)")
            for i, item in enumerate(selected[:3]):
                print(f"   [{i+1}] {item[:50]}...")
        
        return selected
    
    def _score_relevance(
        self,
        task: str,
        candidates: List[ContextItem],
    ) -> List[ContextItem]:
        """
        计算相关性分数
        
        Args:
            task: 当前任务
            candidates: 候选上下文
            
        Returns:
            带分数的候选列表
        """
        if self.strategy == "keyword":
            return self._score_by_keyword(task, candidates)
        elif self.strategy == "embedding":
            return self._score_by_embedding(task, candidates)
        elif self.strategy == "llm":
            return self._score_by_llm(task, candidates)
        else:  # hybrid
            return self._score_hybrid(task, candidates)
    
    def _score_by_keyword(
        self,
        task: str,
        candidates: List[ContextItem],
    ) -> List[ContextItem]:
        """
        关键词匹配评分（快速、无成本）
        
        提取任务关键词，计算与候选的重叠度
        """
        # 提取任务关键词
        task_keywords = self._extract_keywords(task)
        
        for item in candidates:
            item_keywords = self._extract_keywords(item.content)
            # Jaccard 相似度
            intersection = len(task_keywords & item_keywords)
            union = len(task_keywords | item_keywords)
            item.relevance_score = intersection / union if union > 0 else 0.0
        
        return candidates
    
    def _extract_keywords(self, text: str) -> set:
        """提取关键词（简单版：过滤停用词）"""
        # 中文停用词
        stop_words = {"的", "了", "是", "在", "和", "与", "或", "等", "这", "那", "有", "对"}
        
        # 分词（简单版：按空格和标点）
        words = re.findall(r'[\w\u4e00-\u9fff]+', text.lower())
        
        # 过滤停用词和短词
        keywords = {w for w in words if w not in stop_words and len(w) > 1}
        
        return keywords
    
    def _score_by_embedding(
        self,
        task: str,
        candidates: List[ContextItem],
    ) -> List[ContextItem]:
        """
        Embedding 相似度评分（需要嵌入模型）
        
        TODO: 接入 OpenClaw 的 embedding 工具
        """
        # 暂时回退到关键词
        return self._score_by_keyword(task, candidates)
    
    def _score_by_llm(
        self,
        task: str,
        candidates: List[ContextItem],
    ) -> List[ContextItem]:
        """
        LLM 判断相关性（最准确、成本高）
        
        TODO: 接入 LLM 判断
        """
        # 暂时回退到关键词
        return self._score_by_keyword(task, candidates)
    
    def _score_hybrid(
        self,
        task: str,
        candidates: List[ContextItem],
    ) -> List[ContextItem]:
        """
        混合评分：关键词 + 位置权重 + 时序权重
        
        综合多种信号
        """
        # 先用关键词评分
        candidates = self._score_by_keyword(task, candidates)
        
        # 位置权重：后面的历史更重要（更接近当前任务）
        for i, item in enumerate(candidates):
            if item.source.startswith("history_"):
                idx = int(item.source.split("_")[1])
                total = len([c for c in candidates if c.source.startswith("history_")])
                position_weight = (idx + 1) / total if total > 0 else 1.0
                item.relevance_score = 0.7 * item.relevance_score + 0.3 * position_weight
        
        return candidates


def route_context(
    task: str,
    history: List[str],
    max_items: int = 5,
) -> List[str]:
    """
    快速上下文路由的便捷函数
    
    Example:
        >>> context = route_context("分析 CrewAI", ["搜索了 LangChain", "发现 3 个框架"])
    """
    router = ContextRouter(max_items=max_items)
    return router.route(task, history)