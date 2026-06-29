"""LLM 提供商定价数据模块。

包含真实的 API 定价数据，支持模型对比、推荐和成本估算。
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ModelPricing:
    """单个模型的定价信息。"""

    model_name: str
    provider_name: str
    input_price_per_1M: float  # 每百万输入 token 价格（美元）
    output_price_per_1M: float  # 每百万输出 token 价格（美元）
    context_window: int  # 上下文窗口大小（token 数）
    task_tags: List[str] = field(default_factory=list)  # 任务标签: chat, coding, reasoning


def get_all_pricing() -> List[ModelPricing]:
    """获取所有模型的定价数据。

    返回所有支持的 LLM 提供商的真实定价信息。
    """
    return [
        # ── Anthropic ──────────────────────────────────────────
        ModelPricing(
            model_name="Claude Sonnet 4",
            provider_name="Anthropic",
            input_price_per_1M=3.00,
            output_price_per_1M=15.00,
            context_window=200_000,
            task_tags=["chat", "coding", "reasoning"],
        ),
        ModelPricing(
            model_name="Claude Opus 4",
            provider_name="Anthropic",
            input_price_per_1M=15.00,
            output_price_per_1M=75.00,
            context_window=200_000,
            task_tags=["chat", "coding", "reasoning"],
        ),
        ModelPricing(
            model_name="Claude Haiku",
            provider_name="Anthropic",
            input_price_per_1M=0.80,
            output_price_per_1M=4.00,
            context_window=200_000,
            task_tags=["chat", "coding"],
        ),

        # ── OpenAI ─────────────────────────────────────────────
        ModelPricing(
            model_name="GPT-4o",
            provider_name="OpenAI",
            input_price_per_1M=2.50,
            output_price_per_1M=10.00,
            context_window=128_000,
            task_tags=["chat", "coding", "reasoning"],
        ),
        ModelPricing(
            model_name="GPT-4.1",
            provider_name="OpenAI",
            input_price_per_1M=2.00,
            output_price_per_1M=8.00,
            context_window=1_000_000,
            task_tags=["chat", "coding", "reasoning"],
        ),
        ModelPricing(
            model_name="GPT-4.1-mini",
            provider_name="OpenAI",
            input_price_per_1M=0.40,
            output_price_per_1M=1.60,
            context_window=1_000_000,
            task_tags=["chat", "coding"],
        ),

        # ── DeepSeek ───────────────────────────────────────────
        ModelPricing(
            model_name="deepseek-chat",
            provider_name="DeepSeek",
            input_price_per_1M=0.27,
            output_price_per_1M=1.10,
            context_window=128_000,
            task_tags=["chat", "coding"],
        ),
        ModelPricing(
            model_name="deepseek-reasoner",
            provider_name="DeepSeek",
            input_price_per_1M=0.55,
            output_price_per_1M=2.19,
            context_window=128_000,
            task_tags=["chat", "coding", "reasoning"],
        ),

        # ── Google ─────────────────────────────────────────────
        ModelPricing(
            model_name="Gemini 1.5 Pro",
            provider_name="Google",
            input_price_per_1M=1.25,
            output_price_per_1M=5.00,
            context_window=2_000_000,
            task_tags=["chat", "coding", "reasoning"],
        ),
        ModelPricing(
            model_name="Gemini 1.5 Flash",
            provider_name="Google",
            input_price_per_1M=0.075,
            output_price_per_1M=0.30,
            context_window=1_000_000,
            task_tags=["chat", "coding"],
        ),

        # ── OpenRouter ─────────────────────────────────────────
        ModelPricing(
            model_name="claude-sonnet-4 (OpenRouter)",
            provider_name="OpenRouter",
            input_price_per_1M=3.50,
            output_price_per_1M=17.50,
            context_window=200_000,
            task_tags=["chat", "coding", "reasoning"],
        ),
        ModelPricing(
            model_name="gpt-4o (OpenRouter)",
            provider_name="OpenRouter",
            input_price_per_1M=2.75,
            output_price_per_1M=11.00,
            context_window=128_000,
            task_tags=["chat", "coding", "reasoning"],
        ),

        # ── Mistral ────────────────────────────────────────────
        ModelPricing(
            model_name="mistral-large",
            provider_name="Mistral",
            input_price_per_1M=2.00,
            output_price_per_1M=6.00,
            context_window=128_000,
            task_tags=["chat", "coding", "reasoning"],
        ),
        ModelPricing(
            model_name="mistral-small",
            provider_name="Mistral",
            input_price_per_1M=0.20,
            output_price_per_1M=0.60,
            context_window=128_000,
            task_tags=["chat", "coding"],
        ),
    ]


def _total_cost(m: ModelPricing, input_tokens: int = 0, output_tokens: int = 0) -> float:
    """计算指定 token 用量的总成本。"""
    return (
        m.input_price_per_1M * input_tokens / 1_000_000
        + m.output_price_per_1M * output_tokens / 1_000_000
    )


def compare_models(
    task_type: str = "chat",
    input_tokens: int = 100_000,
    output_tokens: int = 50_000,
) -> List[tuple]:
    """根据任务类型返回排序后的推荐模型列表。

    Args:
        task_type: 任务类型，可选 "chat"、"coding"、"reasoning"
        input_tokens: 用于排序的参考输入 token 数
        output_tokens: 用于排序的参考输出 token 数

    Returns:
        List[tuple]: [(ModelPricing, total_cost), ...] 按总成本升序排列
    """
    models = [m for m in get_all_pricing() if task_type in m.task_tags]
    results = [(m, _total_cost(m, input_tokens, output_tokens)) for m in models]
    results.sort(key=lambda x: x[1])
    return results


def estimate_cost(model_name: str, input_tokens: int, output_tokens: int) -> Optional[float]:
    """估算指定模型在给定 token 用量下的 API 成本。

    Args:
        model_name: 模型名称（需与 providers.py 中的名称完全匹配）
        input_tokens: 输入 token 数量
        output_tokens: 输出 token 数量

    Returns:
        float: 美元成本，若未找到模型则返回 None
    """
    for m in get_all_pricing():
        if m.model_name == model_name:
            return _total_cost(m, input_tokens, output_tokens)
    return None


def find_model(model_name: str) -> Optional[ModelPricing]:
    """根据名称查找模型。"""
    for m in get_all_pricing():
        if m.model_name == model_name:
            return m
    return None
