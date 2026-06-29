#!/usr/bin/env python3
"""AI PM 成本计算器 — 估算 LLM API 调用成本"""

import json
import sys
from typing import Dict, List, Tuple


# 模型参考价格 (2026年6月参考值，实际以官方定价为准)
MODEL_PRICES: Dict[str, Dict[str, float]] = {
    # 单位: 元/百万Token
    "gpt-4o": {"input": 18.0, "output": 54.0},
    "gpt-4o-mini": {"input": 1.1, "output": 4.4},
    "gpt-4.1": {"input": 15.0, "output": 60.0},
    "deepseek-v3": {"input": 2.0, "output": 8.0},
    "deepseek-r1": {"input": 4.0, "output": 16.0},
    "claude-sonnet-4": {"input": 22.0, "output": 88.0},
    "qwen-max": {"input": 3.0, "output": 12.0},
    "qwen-turbo": {"input": 0.5, "output": 1.5},
    "glm-4": {"input": 1.0, "output": 1.0},
    "text-embedding-3-small": {"input": 0.1, "output": 0.0},
    "text-embedding-3-large": {"input": 0.9, "output": 0.0},
}


def estimate_cost(
    model: str,
    dau: int,
    calls_per_user: float,
    avg_input_tokens: int,
    avg_output_tokens: int,
    cache_hit_rate: float = 0.0,
) -> Dict:
    """估算日/月成本和Token消耗"""
    price = MODEL_PRICES.get(model.lower())
    if not price:
        return {"error": f"未知模型: {model}，支持的模型: {list(MODEL_PRICES.keys())}"}

    daily_calls = int(dau * calls_per_user)
    daily_input_tokens = daily_calls * avg_input_tokens
    daily_output_tokens = daily_calls * avg_output_tokens

    # 原始成本 (无缓存)
    daily_cost_raw = (daily_input_tokens / 1_000_000) * price["input"] + (
        daily_output_tokens / 1_000_000
    ) * price["output"]

    # 缓存节省 (假设缓存命中节省70%输入成本)
    effective_input_cost = daily_cost_raw * (
        1 - cache_hit_rate * 0.7
    )
    
    return {
        "model": model,
        "input_price_per_1M": price["input"],
        "output_price_per_1M": price["output"],
        "dau": dau,
        "calls_per_user": calls_per_user,
        "daily_calls": daily_calls,
        "avg_input_tokens": avg_input_tokens,
        "avg_output_tokens": avg_output_tokens,
        "daily_input_tokens": daily_input_tokens,
        "daily_output_tokens": daily_output_tokens,
        "daily_input_tokens_M": round(daily_input_tokens / 1_000_000, 2),
        "daily_output_tokens_M": round(daily_output_tokens / 1_000_000, 2),
        "daily_cost_raw_yuan": round(daily_cost_raw, 2),
        "daily_cost_with_cache_yuan": round(effective_input_cost, 2),
        "monthly_cost_raw_yuan": round(daily_cost_raw * 30, 2),
        "monthly_cost_with_cache_yuan": round(effective_input_cost * 30, 2),
        "cache_hit_rate": cache_hit_rate,
        "cache_saving_percent": round(cache_hit_rate * 70, 1),
    }


def compare_models(
    dau: int,
    calls_per_user: float,
    avg_input_tokens: int,
    avg_output_tokens: int,
    models: List[str] = None,
) -> List[Dict]:
    """多模型成本对比"""
    if models is None:
        models = [m for m in MODEL_PRICES if "embedding" not in m]
    
    results = []
    for model in models:
        result = estimate_cost(model, dau, calls_per_user, avg_input_tokens, avg_output_tokens)
        if "error" not in result:
            results.append(result)
    
    results.sort(key=lambda x: x["monthly_cost_raw_yuan"])
    return results


def print_cost_report(result: Dict):
    """格式化输出成本报告"""
    if "error" in result:
        print(f"错误: {result['error']}")
        return

    print(f"""
╔══════════════════════════════════════════╗
║        AI 调用成本估算报告               ║
╠══════════════════════════════════════════╣
║ 模型: {result['model']:<33}║
╠══════════════════════════════════════════╣
║ 输入价格: ¥{result['input_price_per_1M']}/百万Token                      
║ 输出价格: ¥{result['output_price_per_1M']}/百万Token                      
╠══════════════════════════════════════════╣
║ 日活用户: {result['dau']:,}
║ 人均调用: {result['calls_per_user']}次
║ 日调用量: {result['daily_calls']:,}
║ 平均输入: {result['avg_input_tokens']} tokens
║ 平均输出: {result['avg_output_tokens']} tokens
╠══════════════════════════════════════════╣
║ 📊 Token消耗
║ 日输入: {result['daily_input_tokens_M']}M tokens
║ 日输出: {result['daily_output_tokens_M']}M tokens
╠══════════════════════════════════════════╣
║ 💰 成本估算
║ 日成本 (无缓存): ¥{result['daily_cost_raw_yuan']:,}
║ 日成本 (缓存{result['cache_hit_rate']*100:.0f}%): ¥{result['daily_cost_with_cache_yuan']:,}
║ 月成本 (无缓存): ¥{result['monthly_cost_raw_yuan']:,}
║ 月成本 (缓存{result['cache_hit_rate']*100:.0f}%): ¥{result['monthly_cost_with_cache_yuan']:,}
║ 缓存节省: {result['cache_saving_percent']}%
╚══════════════════════════════════════════╝
""")


def print_compare_report(results: List[Dict]):
    """格式化输出多模型对比报告"""
    print(f"\n{'模型':<20} {'日成本(无缓存)':>14} {'日成本(50%缓存)':>16} {'月成本(无缓存)':>14}")
    print("-" * 66)
    for r in results:
        cost_with_cache = estimate_cost(
            r["model"], r["dau"], r["calls_per_user"],
            r["avg_input_tokens"], r["avg_output_tokens"],
            cache_hit_rate=0.5
        )
        print(
            f"{r['model']:<20} ¥{r['daily_cost_raw_yuan']:>10,.2f}   "
            f"¥{cost_with_cache['daily_cost_with_cache_yuan']:>10,.2f}   "
            f"¥{r['monthly_cost_raw_yuan']:>10,.2f}"
        )
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python cost_calculator.py single <model> <dau> <calls_per_user> <avg_input> <avg_output> [cache_rate]")
        print("  python cost_calculator.py compare <dau> <calls_per_user> <avg_input> <avg_output>")
        print()
        print("示例:")
        print("  python cost_calculator.py single gpt-4o-mini 10000 5 500 200 0.3")
        print("  python cost_calculator.py compare 10000 5 500 200")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "single":
        model = sys.argv[2]
        dau = int(sys.argv[3])
        calls_per_user = float(sys.argv[4])
        avg_input = int(sys.argv[5])
        avg_output = int(sys.argv[6])
        cache_rate = float(sys.argv[7]) if len(sys.argv) > 7 else 0.0
        
        result = estimate_cost(model, dau, calls_per_user, avg_input, avg_output, cache_rate)
        print_cost_report(result)

    elif cmd == "compare":
        dau = int(sys.argv[2])
        calls_per_user = float(sys.argv[3])
        avg_input = int(sys.argv[4])
        avg_output = int(sys.argv[5])
        
        results = compare_models(dau, calls_per_user, avg_input, avg_output)
        print_compare_report(results)
