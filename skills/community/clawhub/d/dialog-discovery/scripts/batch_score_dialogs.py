#!/usr/bin/env python3
"""
批量对话评分脚本（重构版）

支持四种模式：
- rules: 规则式快速评分（从 scenes yaml 读取评分标准）
- llm: 调用大模型评分
- hybrid: 规则式打底，边界样本走 LLM
- weak_label: 弱监督 seed 分桶（适用于 ASR 脏文本 + 无标注数据）
"""
import argparse
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from common import WORKSPACE_DIR
from llm_client import call_messages, parse_json_response
from template_match_dialogs import load_weak_supervision, build_signals, compute_scores, determine_seed_label


def load_scene_config(scene: str) -> Dict[str, Any]:
    """加载场景配置"""
    import yaml
    skill_dir = os.path.dirname(SCRIPT_DIR)
    path = os.path.join(skill_dir, "scenes", f"{scene}.yaml")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_score_prompt(scene: str) -> str:
    """加载评分 Prompt"""
    skill_dir = os.path.dirname(SCRIPT_DIR)
    path = os.path.join(skill_dir, "prompts", scene, "score-dialog.md")
    if not os.path.exists(path):
        return "你是对话评分器，只输出 JSON。"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_dialogs(input_path: str) -> List[Dict[str, Any]]:
    """加载对话数据"""
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("dialogs", data.get("results", []))


def get_grade_thresholds(scoring: Dict[str, Any]) -> Dict[str, int]:
    """获取分类阈值"""
    thresholds = scoring.get("grade_thresholds", {})
    return {
        "good": thresholds.get("good", 80),
        "pass": thresholds.get("pass", 60),
        "bad": thresholds.get("bad", 0),
    }


def score_by_rules_from_config(dialog: Dict[str, Any], scoring: Dict[str, Any]) -> Dict[str, Any]:
    """基于配置的规则评分"""
    features = dialog.get("features", {})
    
    # 初始化
    bottom_violations = []
    foundation_issues = []
    top_bonuses = []
    
    # 从配置读取基础分
    bottom_tier = scoring.get("bottom_tier", {})
    foundation_tier = scoring.get("foundation_tier", {})
    top_tier = scoring.get("top_tier", {})
    
    base_bottom = bottom_tier.get("base_score", 40)
    base_foundation = foundation_tier.get("base_score", 55)
    
    foundation_score = base_foundation
    top_score = 0
    
    # 底线层检查
    has_bottom_violation = False
    
    # 禁止表达 → 底线违规
    forbidden_hits = features.get("forbidden_hits", [])
    if forbidden_hits:
        bottom_violations.append({
            "name": "命中禁止表达",
            "evidence": forbidden_hits
        })
        has_bottom_violation = True
    
    # 基础层检查
    if features.get("anchor_missing"):
        foundation_issues.append({
            "name": "状态锚定缺失",
            "penalty": -5,
            "count": 1,
            "evidence": []
        })
        foundation_score -= 5
    
    refusal_hits = features.get("refusal_hits", [])
    if refusal_hits and not features.get("confirm_hits"):
        foundation_issues.append({
            "name": "拒绝后缺少二次确认",
            "penalty": -5,
            "count": 1,
            "evidence": refusal_hits
        })
        foundation_score -= 5
    
    # 拔高层加分
    if features.get("benefit_hits"):
        top_bonuses.append({
            "name": "福利导向",
            "bonus": 5,
            "evidence": features.get("benefit_hits", [])
        })
        top_score += 5
    
    if features.get("special_scenes") and features.get("busy_hits"):
        top_bonuses.append({
            "name": "特殊场景感知",
            "bonus": 3,
            "evidence": features.get("special_scenes", [])
        })
        top_score += 3
    
    # 计算总分
    # 有底线违规 → 总分 = 0
    if has_bottom_violation:
        total_score = 0
    else:
        total_score = base_bottom + foundation_score + top_score
    
    # 分类
    thresholds = get_grade_thresholds(scoring)
    if has_bottom_violation:
        classification = "badcase"
    elif total_score >= thresholds["good"]:
        classification = "goodcase"
    elif total_score < thresholds["pass"]:
        classification = "badcase"
    else:
        classification = "grayzone"
    
    return {
        "dialog_id": dialog.get("dialog_id") or dialog.get("dialog", {}).get("dialog_id"),
        "total_score": total_score,
        "bottom_tier": {
            "violations": bottom_violations,
            "impact": "Bad" if has_bottom_violation else "Pass"
        },
        "foundation_tier": {
            "issues": foundation_issues,
            "score": foundation_score
        },
        "top_tier": {
            "bonuses": top_bonuses,
            "score": top_score
        },
        "classification": classification,
        "features": features,
    }


def build_llm_prompt(dialog: Dict[str, Any], scene: str) -> List[Dict[str, str]]:
    """构建 LLM Prompt（精简版：只传对话文本和评分标准，不传完整配置）"""
    scene_config = load_scene_config(scene)
    prompt_text = load_score_prompt(scene)
    
    # 精简：只传对话文本，不传 features 和完整 scoring 配置
    dialog_id = dialog.get("dialog_id") or dialog.get("dialog", {}).get("dialog_id")
    user_text = dialog.get("dialog", {}).get("user_text") or dialog.get("user_text", "")
    agent_text = dialog.get("dialog", {}).get("agent_text") or dialog.get("agent_text", "")
    
    # Truncate very long texts to keep prompt manageable
    if len(user_text) > 500:
        user_text = user_text[:500] + "...(截断)"
    if len(agent_text) > 2000:
        agent_text = agent_text[:2000] + "...(截断)"
    
    content = json.dumps({
        "dialog_id": dialog_id,
        "user_text": user_text,
        "agent_text": agent_text,
    }, ensure_ascii=False)
    
    return [
        {"role": "system", "content": prompt_text},
        {"role": "user", "content": content}
    ]


def normalize_classification(classification: str) -> str:
    """统一分类名称：Good/Pass/Bad → goodcase/grayzone/badcase"""
    mapping = {
        "Good": "goodcase",
        "goodcase": "goodcase",
        "Pass": "grayzone",
        "grayzone": "grayzone",
        "Bad": "badcase",
        "badcase": "badcase",
    }
    return mapping.get(classification, classification)


def score_by_llm(dialog: Dict[str, Any], scene: str, scoring: Dict[str, Any], model_name: str = None) -> Dict[str, Any]:
    """LLM 评分（带重试和超时）"""
    import time as _time
    messages = build_llm_prompt(dialog, scene)
    max_retries = 2
    for attempt in range(max_retries + 1):
        try:
            raw = call_messages(messages, model_name=model_name, max_tokens=2000, timeout=180)
            parsed = parse_json_response(raw)
            if not parsed:
                fallback = score_by_rules_from_config(dialog, scoring)
                fallback["llm_fallback"] = True
                fallback["raw_response"] = (raw or "")[:500]
                return fallback
            parsed["dialog_id"] = dialog.get("dialog_id") or dialog.get("dialog", {}).get("dialog_id")
            parsed["features"] = dialog.get("features", {})
            parsed["classification"] = normalize_classification(parsed.get("classification", "grayzone"))
            return parsed
        except Exception as e:
            if attempt < max_retries:
                _time.sleep(5)
                continue
            fallback = score_by_rules_from_config(dialog, scoring)
            fallback["llm_fallback"] = True
            fallback["llm_error"] = str(e)[:200]
            return fallback


def batch_score(dialogs: List[Dict[str, Any]], scene: str, mode: str, model_name: str = None, output_path: str = None) -> List[Dict[str, Any]]:
    """批量评分"""
    scene_config = load_scene_config(scene)
    scoring = scene_config.get("scoring", {})
    
    weak_cfg = load_weak_supervision(scene)
    results = []
    total = len(dialogs)
    for idx, dialog in enumerate(dialogs):
        if mode == "llm" and idx % 5 == 0:
            print(f"  LLM 评分进度: {idx}/{total} ...", flush=True)
        if mode == "rules":
            result = score_by_rules_from_config(dialog, scoring)
        elif mode == "llm":
            result = score_by_llm(dialog, scene, scoring, model_name)
        elif mode == "weak_label":
            signals = build_signals(dialog.get("features", {}))
            scores = compute_scores(signals, weak_cfg, dialog.get("dialog", {}).get("meta", {}))
            result = {
                "dialog_id": dialog.get("dialog_id") or dialog.get("dialog", {}).get("dialog_id"),
                "signals": signals,
                "scores": scores,
                "seed_label": determine_seed_label(scores, weak_cfg),
                "features": dialog.get("features", {}),
            }
        else:  # hybrid
            preliminary = score_by_rules_from_config(dialog, scoring)
            if preliminary["classification"] == "grayzone":
                result = score_by_llm(dialog, scene, scoring, model_name)
            else:
                result = preliminary
        results.append(result)
        # Checkpoint: save intermediate results every 10 items (LLM mode)
        if mode == "llm" and len(results) % 10 == 0 and output_path:
            save_results(results, output_path + ".checkpoint")
    return results


def save_results(results: List[Dict[str, Any]], output_path: str) -> None:
    """保存结果"""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "total": len(results),
            "results": results,
            "created_at": datetime.now().isoformat(),
        }, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量对话评分")
    parser.add_argument("--input", required=True, help="输入灰度对话 json")
    parser.add_argument("--scene", required=True, help="场景")
    parser.add_argument("--output", required=True, help="输出评分 json")
    parser.add_argument("--mode", default="rules", choices=["rules", "llm", "hybrid", "weak_label"], help="评分模式")
    parser.add_argument("--model-name", default=None, help="模型名称")
    parser.add_argument("--limit", type=int, default=None, help="限制评分数量")
    parser.add_argument("--seed-filter", default=None, help="只评分指定 seed_label（如 bad_seed, good_seed）")
    args = parser.parse_args()

    dialogs = load_dialogs(args.input)
    
    # Filter by seed_label if specified
    if args.seed_filter:
        dialogs = [d for d in dialogs if d.get('seed_label') == args.seed_filter]
    
    # Limit count
    if args.limit:
        dialogs = dialogs[:args.limit]
        print(f"限制评分数量: {args.limit}, 实际: {len(dialogs)} 条")
    results = batch_score(dialogs, args.scene, args.mode, args.model_name, args.output)
    save_results(results, args.output)
    print(f"✅ 评分完成: {len(results)} 条 -> {args.output}")