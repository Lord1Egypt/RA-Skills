"""
Model Router - 模型选择路由

AOrchestra 的核心洞察之二：编排器为每个子任务选择合适的模型，优化成本-性能权衡。

模型选择策略：
1. 任务复杂度 → 模型能力
2. 任务类型 → 模型特长
3. 成本预算 → 模型价格

模型能力分层：
- FAST: glm - 便宜、速度快、中文好
- CODE: kimi - 长上下文、代码强
- CREATIVE: gemini - 创意好、多模态
- REASONING: sonnet - 均衡、推理稳
- BEST: opus - 最强推理
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
import re


class TaskType(Enum):
    """任务类型"""
    SEARCH = "search"           # 搜索、信息收集
    CODE = "code"               # 代码实现、调试
    ANALYSIS = "analysis"       # 深度分析、对比
    CREATIVE = "creative"       # 写作、创意
    REASONING = "reasoning"     # 复杂推理、规划
    SIMPLE = "simple"           # 简单任务


class ModelTier(Enum):
    """模型层级"""
    FAST = "fast"           # 快速、便宜
    CODE = "code"           # 代码、长上下文
    CREATIVE = "creative"   # 创意
    REASONING = "reasoning" # 推理
    BEST = "best"           # 最强


@dataclass
class ModelInfo:
    """模型信息"""
    name: str                   # 模型名称（OpenClaw alias）
    tier: ModelTier             # 层级
    input_price: float          # 输入价格 $/1K tokens
    output_price: float         # 输出价格 $/1K tokens
    context_window: int         # 上下文窗口
    strengths: List[str]        # 特长
    
    def get_price(self, input_tokens: int, output_tokens: int) -> float:
        """计算价格"""
        return (input_tokens * self.input_price + output_tokens * self.output_price) / 1000


# 模型配置（价格为估算，实际以 OpenClaw 配置为准）
MODEL_REGISTRY: Dict[str, ModelInfo] = {
    "glm": ModelInfo(
        name="glm",
        tier=ModelTier.FAST,
        input_price=0.001,
        output_price=0.001,
        context_window=128000,
        strengths=["快速", "便宜", "中文好"],
    ),
    "kimi": ModelInfo(
        name="kimi",
        tier=ModelTier.CODE,
        input_price=0.01,
        output_price=0.01,
        context_window=128000,
        strengths=["长上下文", "代码强", "推理好"],
    ),
    "gemini": ModelInfo(
        name="gemini",
        tier=ModelTier.CREATIVE,
        input_price=0.01,
        output_price=0.02,
        context_window=1000000,
        strengths=["创意", "多模态", "写作"],
    ),
    "sonnet": ModelInfo(
        name="sonnet",
        tier=ModelTier.REASONING,
        input_price=0.03,
        output_price=0.15,
        context_window=200000,
        strengths=["均衡", "推理稳", "工具调用强"],
    ),
    "opus": ModelInfo(
        name="opus",
        tier=ModelTier.BEST,
        input_price=0.15,
        output_price=0.75,
        context_window=200000,
        strengths=["最强推理", "复杂任务"],
    ),
}


class ModelRouter:
    """
    模型选择路由器
    
    根据任务特征选择最优模型
    
    Example:
        >>> router = ModelRouter(available_models=["glm", "kimi", "sonnet"])
        >>> model = router.select("实现一个排序算法")
        >>> print(model)  # "kimi"
    """
    
    def __init__(
        self,
        available_models: List[str] = None,
        default_model: str = "glm",
        cost_aware: bool = True,
        verbose: bool = False,
    ):
        self.available_models = available_models or list(MODEL_REGISTRY.keys())
        self.default_model = default_model
        self.cost_aware = cost_aware
        self.verbose = verbose
    
    def select(
        self,
        task: str,
        context: List[str] = None,
        hint: str = None,
    ) -> str:
        """
        选择最优模型
        
        Args:
            task: 任务描述
            context: 上下文（用于估算 token）
            hint: 额外提示（如 "需要深度分析"）
            
        Returns:
            模型名称
        """
        # 1. 分类任务类型
        task_type = self._classify_task(task, hint)
        
        # 2. 根据任务类型选择模型层级
        tier = self._task_type_to_tier(task_type)
        
        # 3. 从可用模型中选择最匹配的
        model = self._select_from_tier(tier)
        
        # 4. 成本感知调整
        if self.cost_aware:
            model = self._adjust_for_cost(model, task, context)
        
        if self.verbose:
            print(f"\n📍 模型选择:")
            print(f"   任务类型: {task_type.value}")
            print(f"   目标层级: {tier.value}")
            print(f"   选择模型: {model}")
        
        return model
    
    def _classify_task(self, task: str, hint: str = None) -> TaskType:
        """
        分类任务类型
        
        基于关键词和模式匹配
        """
        task_lower = task.lower()
        hint_lower = (hint or "").lower()
        combined = task_lower + " " + hint_lower
        
        # 代码相关
        code_keywords = ["代码", "实现", "编程", "调试", "bug", "code", "implement", "debug"]
        if any(kw in combined for kw in code_keywords):
            return TaskType.CODE
        
        # 搜索相关
        search_keywords = ["搜索", "查找", "收集", "调研", "search", "find", "research"]
        if any(kw in combined for kw in search_keywords):
            return TaskType.SEARCH
        
        # 分析相关
        analysis_keywords = ["分析", "对比", "比较", "评估", "analyze", "compare", "evaluate"]
        if any(kw in combined for kw in analysis_keywords):
            return TaskType.ANALYSIS
        
        # 创意相关
        creative_keywords = ["写作", "创作", "文案", "设计", "write", "create", "design", "创意"]
        if any(kw in combined for kw in creative_keywords):
            return TaskType.CREATIVE
        
        # 推理相关
        reasoning_keywords = ["推理", "规划", "决策", "reasoning", "plan", "decide", "为什么"]
        if any(kw in combined for kw in reasoning_keywords):
            return TaskType.REASONING
        
        # 默认简单任务
        return TaskType.SIMPLE
    
    def _task_type_to_tier(self, task_type: TaskType) -> ModelTier:
        """任务类型映射到模型层级"""
        mapping = {
            TaskType.SEARCH: ModelTier.FAST,
            TaskType.SIMPLE: ModelTier.FAST,
            TaskType.CODE: ModelTier.CODE,
            TaskType.ANALYSIS: ModelTier.CODE,
            TaskType.CREATIVE: ModelTier.CREATIVE,
            TaskType.REASONING: ModelTier.REASONING,
        }
        return mapping.get(task_type, ModelTier.FAST)
    
    def _select_from_tier(self, tier: ModelTier) -> str:
        """从层级中选择可用模型"""
        # 查找该层级中的可用模型
        for name, info in MODEL_REGISTRY.items():
            if name in self.available_models and info.tier == tier:
                return name
        
        # 回退到更高层级
        tier_priority = [tier, ModelTier.REASONING, ModelTier.CODE, ModelTier.FAST]
        for t in tier_priority:
            for name, info in MODEL_REGISTRY.items():
                if name in self.available_models and info.tier == t:
                    return name
        
        # 最终回退到默认
        return self.default_model
    
    def _adjust_for_cost(
        self,
        model: str,
        task: str,
        context: List[str] = None,
    ) -> str:
        """
        成本感知调整
        
        简单任务不使用昂贵模型
        """
        info = MODEL_REGISTRY.get(model)
        if not info:
            return model
        
        # 估算任务规模
        task_tokens = len(task) // 4
        context_tokens = sum(len(c) for c in (context or [])) // 4
        total_tokens = task_tokens + context_tokens
        
        # 如果任务很小且模型很贵，降级
        if total_tokens < 1000 and info.tier in [ModelTier.BEST, ModelTier.REASONING]:
            if "glm" in self.available_models:
                if self.verbose:
                    print(f"   成本优化: 任务较小({total_tokens} tokens)，从 {model} 降级到 glm")
                return "glm"
        
        return model
    
    def get_model_info(self, model: str) -> Optional[ModelInfo]:
        """获取模型信息"""
        return MODEL_REGISTRY.get(model)
    
    def estimate_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
    ) -> float:
        """估算成本"""
        info = MODEL_REGISTRY.get(model)
        if info:
            return info.get_price(input_tokens, output_tokens)
        return 0.0


# === 便捷函数 ===

def select_model(
    task: str,
    available_models: List[str] = None,
    context: List[str] = None,
) -> str:
    """
    快速模型选择的便捷函数
    
    Example:
        >>> model = select_model("实现一个排序算法")
        >>> print(model)  # "kimi"
    """
    router = ModelRouter(available_models=available_models)
    return router.select(task, context)