#!/usr/bin/env python3
"""
小Z 置信度检测器 — 简化版
基于论文启发：arXiv:2604.13068 (pre-generation knowledge boundary signal) + UQLM PTrue架构

MiniMax API不暴露token概率，所以使用简化替代方案：
1. 一致性检测：同一问题生成两次，检查回答是否一致
2.  Hedging语言检测：检测"我认为""可能""不确定"等弱化词

工作流程：
- 小Z生成回答 → 调用check_confidence → 如果置信度低，加"[🤔 不确定]"标记
"""

import json
import os
import subprocess
import re

CONFIDENCE_THRESHOLD = 0.6  # 一致性阈值：低于此值标记不确定

# Hedging语言列表（中文+英文混合）
HEDGING_PATTERNS = [
    r"我认为", r"我觉得", r"可能", r"大概", r"也许", r"似乎",
    r"不太确定", r"不确定", r"我说不准", r"不一定",
    r"应该", r"可能是", r"大概是", r"看起来",
    r"I think", r"I believe", r"probably", r"maybe", r"perhaps",
    r"likely", r"possibly", r"not sure", r"uncertain",
    r"I'm not certain", r"might be", r"could be",
    r"应该", r"或许", r"不太确定",
]


def call_minimax(messages, model="MiniMax-M2.7", temperature=0.7):
    """
    调用MiniMax API
    messages: list of {"role": "user"/"assistant"/"system", "content": str}
    Returns: (response_dict, error_msg)
    """
    api_key = os.environ.get("MINIMAX_API_KEY", "")
    if not api_key:
        config_path = os.path.expanduser("~/.openclaw/config/minimax.json")
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                api_key = config.get("api_key", "")
        except:
            return None, "No API key"

    cmd = ["mmx", "text", "chat", "--model", model, "--temperature", str(temperature),
           "--output", "json", "--non-interactive"]

    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        cmd.extend(["--message", f"{role}: {content}"])

    env = os.environ.copy()
    env["MINIMAX_API_KEY"] = api_key

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, env=env)

    if result.returncode == 0:
        try:
            resp = json.loads(result.stdout)
            # 解析MiniMax的响应格式：content是数组，每个block有type
            text_response = ""
            content = resp.get("content", [])
            for block in content:
                if block.get("type") == "text":
                    text_response = block.get("text", "").strip()
                    break
            resp["_parsed_text"] = text_response
            return resp, None
        except:
            return None, f"Failed to parse: {result.stdout[:200]}"
    else:
        return None, f"API error: {result.stderr[:200]}"


def has_hedging(text: str) -> float:
    """
    检测hedging语言，返回 hedging 分数 (0-1)
    0 = 完全确定，1 = 高度不确定
    """
    hedging_count = 0
    for pattern in HEDGING_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            hedging_count += 1

    # 0个hedging词 = 0分，3个以上 = 1分
    if hedging_count == 0:
        return 0.0
    elif hedging_count == 1:
        return 0.3
    elif hedging_count == 2:
        return 0.6
    else:
        return 0.9


def check_consistency(question: str, answer: str, model: str = "MiniMax-M2.7") -> tuple:
    """
    一致性检测：问同一个问题两次，检查回答是否一致
    返回 (consistency_score, details)
    """
    ptrue_prompt = f"""Question: {question}

Proposed Answer: {answer}

Is the proposed answer correct? Answer with EXACTLY one word: TRUE or FALSE."""

    messages = [
        {"role": "system", "content": "You are a precise evaluator. Answer with exactly one word: TRUE or FALSE. No explanation."},
        {"role": "user", "content": ptrue_prompt}
    ]

    response, error = call_minimax(messages, model=model, temperature=0.3)

    if error:
        return None, f"一致性检测失败: {error}"

    # 解析MiniMax响应
    content = response.get("_parsed_text", "").lower()

    # 判断TRUE/FALSE
    if "true" in content and "false" not in content:
        consistency = 0.85  # 高置信度
        details = f"[一致性] 高置信度 (response: {content})"
    elif "false" in content:
        consistency = 0.15  # 低置信度
        details = f"[一致性] 低置信度/错误 (response: {content})"
    else:
        consistency = None  # 无法判断
        details = f"[一致性] 无法解析: {content}"

    return consistency, details


def check_answer(question: str, answer: str, model: str = "MiniMax-M2.7") -> dict:
    """
    主函数：检查小Z的回答是否需要"不确定"标记

    Returns:
        {
            "needs_uncertain_marker": bool,
            "confidence": float or None,
            "marker_text": str,
            "detail": str,
            "hedging_score": float,
            "consistency": float or None
        }
    """
    # 1. Hedging语言检测
    hedging_score = has_hedging(answer)

    # 2. 一致性检测（可选，降低API调用频率）
    consistency, consistency_detail = check_consistency(question, answer, model)

    # 3. 综合判断
    scores = []
    if hedging_score > 0:
        scores.append(hedging_score)
    if consistency is not None:
        # consistency是置信度，hedging_score是不确定性
        # 要统一：consistency高=确定，hedging_score高=不确定
        scores.append(1 - consistency)  # 转换为不确定性

    if not scores:
        # 无法判断，默认标记为不确定以保护ano
        confidence = None
        needs_marker = True
        detail = "[保护性] 无法判断置信度，默认标记"
    else:
        avg_uncertainty = sum(scores) / len(scores)
        confidence = 1 - avg_uncertainty
        needs_marker = avg_uncertainty > (1 - CONFIDENCE_THRESHOLD)
        detail = f"[综合] 置信度={confidence:.2f} | {consistency_detail} | hedging={hedging_score:.1f}"

    if needs_marker:
        marker_text = "🤔 不确定"
    else:
        marker_text = ""

    return {
        "needs_uncertain_marker": needs_marker,
        "confidence": confidence,
        "marker_text": marker_text,
        "detail": detail,
        "hedging_score": hedging_score,
        "consistency": consistency
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("用法: python3 confidence_checker.py <问题> <回答>")
        print("示例: python3 confidence_checker.py '什么是AI' 'AI是人工智能'")
        sys.exit(1)

    question = sys.argv[1]
    answer = sys.argv[2]

    result = check_answer(question, answer)

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result["needs_uncertain_marker"]:
        print(f"\n⚠️  建议在回复前加标记: {result['marker_text']}")
    else:
        print(f"\n✅ 置信度正常，直接发出")