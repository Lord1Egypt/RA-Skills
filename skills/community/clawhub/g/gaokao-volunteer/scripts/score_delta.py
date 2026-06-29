#!/usr/bin/env python3
"""
score_delta.py — 线差法计算引擎

基于"线差 = 考生分数 - 批次线"的方法，将当年分数映射到往年等效分数。
当无法获取一分一段表（位次数据）时，使用线差法作为fallback。

用法:
  python score_delta.py --score 650 --batch-line 530 \
    --prev-lines 525,520,515 --prev-years 2025,2024,2023
"""

import json
import argparse
import sys


def compute_line_deltas(score: int, current_batch_line: int,
                        prev_batch_lines: list[int],
                        prev_years: list[int]) -> dict:
    """
    计算线差和等效分。

    参数:
      score: 当年考生分数
      current_batch_line: 当年批次线
      prev_batch_lines: 往年批次线列表（按年份降序）
      prev_years: 对应对往年列表

    返回: {
      "current_line_delta": int,
      "equivalent_scores": [{"year": 2025, "score": int, "delta": int}, ...],
      "avg_equivalent_score": float
    }
    """
    current_delta = score - current_batch_line

    equivalents = []
    for i, prev_line in enumerate(prev_batch_lines):
        year = prev_years[i] if i < len(prev_years) else 2025 - i
        eq_score = prev_line + current_delta
        equivalents.append({
            "year": year,
            "equivalent_score": eq_score,
            "prev_batch_line": prev_line,
            "delta": current_delta
        })

    avg_eq = sum(e["equivalent_score"] for e in equivalents) / len(equivalents) if equivalents else score

    return {
        "current_score": score,
        "current_batch_line": current_batch_line,
        "current_line_delta": current_delta,
        "equivalent_scores": equivalents,
        "avg_equivalent_score": round(avg_eq, 1),
        "delta_trend": _compute_trend(equivalents)
    }


def _compute_trend(equivalents: list[dict]) -> str:
    """分析等效分趋势"""
    if len(equivalents) < 2:
        return "stable"
    scores = [e["equivalent_score"] for e in equivalents]
    if scores[0] > scores[-1] + 2:
        return "declining"  # 等效分逐年下降，说明分数线在涨
    elif scores[0] < scores[-1] - 2:
        return "rising"  # 等效分逐年上升
    return "stable"


def estimate_rank_from_score(score: int, batch_line: int,
                             approx_rank_per_delta: int = 500) -> int:
    """
    从分数估算位次（非常粗略的估算）。

    假设每分对应约500名考生（在批次线附近，实际看一分一段表更准）。
    使用场景: 用户只有分数没有位次时做初筛。
    """
    delta = score - batch_line
    # 假设在批次线处约有全省50%考生在该批以上
    # 越往上位次越小（排名越靠前）
    base_rank = 100000  # 粗略基准，实际取决于省份
    estimated = max(1, base_rank - delta * approx_rank_per_delta)
    return estimated


def main():
    parser = argparse.ArgumentParser(description="线差法计算引擎")
    parser.add_argument("--score", type=int, required=True, help="当年考生分数")
    parser.add_argument("--batch-line", type=int, required=True, help="当年批次线")
    parser.add_argument("--prev-lines", type=str, required=True,
                        help="往年批次线，逗号分隔 (如 525,520,515)")
    parser.add_argument("--prev-years", type=str, default=None,
                        help="对应往年，逗号分隔 (如 2025,2024,2023)")
    parser.add_argument("--output", type=str, default=None, help="输出JSON文件路径")

    args = parser.parse_args()

    prev_lines = [int(x.strip()) for x in args.prev_lines.split(",") if x.strip()]
    if args.prev_years:
        prev_years = [int(x.strip()) for x in args.prev_years.split(",") if x.strip()]
    else:
        prev_years = list(range(2025, 2025 - len(prev_lines), -1))

    result = compute_line_deltas(args.score, args.batch_line, prev_lines, prev_years)
    result["estimated_rank"] = estimate_rank_from_score(args.score, args.batch_line)
    result["note"] = "estimated_rank为粗略估算，建议优先使用一分一段表获取准确位次"

    if args.output:
        from pathlib import Path
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[score_delta] 结果已保存到 {args.output}", file=sys.stderr)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
