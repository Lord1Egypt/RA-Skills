#!/usr/bin/env python3
"""
综合评分模块
基于逐事实验证结果，计算最终可信度评分
"""

import json
import argparse
import sys
from pathlib import Path


def calc_score(verification_results: list, consistency_result: dict) -> dict:
    """
    计算综合评分
    
    评分规则：
    - 每个事实基础分：verdict == "true" → 1.0，else → 0.0
    - 加权：基础分 × confidence
    - 总分 = 加权平均分 × 100
    - 一致性扣分：如果回答自相矛盾，总分 × 0.8
    """
    if not verification_results:
        return {
            "score": 0,
            "verdict": "unknown",
            "summary": "无有效事实可验证"
        }

    # 计算加权平均分
    weighted_sum = 0.0
    verdict_counts = {"true": 0, "false": 0, "uncertain": 0}

    for r in verification_results:
        verdict = r.get("verdict", "uncertain")
        confidence = r.get("confidence", 0.5)

        verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1

        if verdict == "true":
            weighted_sum += 1.0 * confidence
        elif verdict == "false":
            weighted_sum += 0.0
        else:  # uncertain
            weighted_sum += 0.5 * confidence  # 无法验证的给一半分

    avg_score = weighted_sum / len(verification_results)
    score = round(avg_score * 100)

    # 一致性扣分
    if not consistency_result.get("consistent", True):
        score = round(score * 0.8)
        consistency_penalty = True
    else:
        consistency_penalty = False

    # 确定最终verdict
    total = len(verification_results)
    true_ratio = verdict_counts["true"] / total
    false_ratio = verdict_counts["false"] / total

    if false_ratio > 0.5:
        final_verdict = "false"
    elif true_ratio > 0.5:
        final_verdict = "true"
    else:
        final_verdict = "partial"

    # 生成文字摘要
    summary = (
        f"验证完成：{verdict_counts['true']}个事实正确，"
        f"{verdict_counts['false']}个事实错误，"
        f"{verdict_counts['uncertain']}个无法验证。"
    )
    if consistency_penalty:
        summary += " 注意：回答存在自相矛盾，已扣分。"

    return {
        "score": score,
        "verdict": final_verdict,
        "summary": summary,
        "details": {
            "facts_total": total,
            "facts_true": verdict_counts["true"],
            "facts_false": verdict_counts["false"],
            "facts_uncertain": verdict_counts["uncertain"],
            "consistency_penalty": consistency_penalty,
            "contradictions": consistency_result.get("contradictions", [])
        }
    }


def format_output(result: dict, facts: list) -> str:
    """生成用户友好的输出格式"""
    verdict_emoji = {
        "true": "✅",
        "false": "❌",
        "partial": "⚠️",
        "unknown": "❓"
    }

    lines = []
    lines.append(f"{verdict_emoji.get(result['verdict'], '❓')} 验证结果：{result['verdict']}（{result['score']}分）")
    lines.append("")
    lines.append(f"📊 {result['summary']}")
    lines.append("")

    # 逐条显示
    for r in facts:
        emoji = verdict_emoji.get(r["verdict"], "❓")
        lines.append(f"{emoji} [{r['verdict']}] {r['text']}（置信度：{r['confidence']:.0%}）")
        if r.get("reason"):
            lines.append(f"   └─ {r['reason']}")

    # 一致性检测结果
    if result["details"].get("contradictions"):
        lines.append("")
        lines.append("⚠️ 检测到内部矛盾：")
        for c in result["details"]["contradictions"]:
            lines.append(f"   └─ {c.get('location', '')}: {c.get('description', '')}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="综合评分")
    parser.add_argument("--verification", type=str, required=True, help="验证结果JSON文件")
    parser.add_argument("--consistency", type=str, required=True, help="一致性检测结果JSON文件")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="输出格式")
    args = parser.parse_args()

    with open(args.verification, "r", encoding="utf-8") as f:
        verification = json.load(f)
    with open(args.consistency, "r", encoding="utf-8") as f:
        consistency = json.load(f)

    facts = verification.get("results", [])
    score_result = calc_score(facts, consistency)

    if args.format == "json":
        output = {
            "score": score_result["score"],
            "verdict": score_result["verdict"],
            "summary": score_result["summary"],
            "details": {
                "facts": facts,
                "consistency": consistency
            }
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(format_output(score_result, facts))


if __name__ == "__main__":
    main()
