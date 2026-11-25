#!/usr/bin/env python3
"""
弱监督特征提取脚本（ASR / 无标注友好版）

用途：
- 从标准化后的对话中抽取稳健特征
- 生成正向/负向/风险/质量 signals
- 计算 good_score / bad_score / confidence
- 输出 good_seed / bad_seed / gray
"""
import argparse
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)


def load_scene_config(scene: str) -> Dict[str, Any]:
    import yaml
    skill_dir = os.path.dirname(SCRIPT_DIR)
    path = os.path.join(skill_dir, "scenes", f"{scene}.yaml")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_feature_rules(scene: str) -> Dict[str, Any]:
    config = load_scene_config(scene)
    return config.get("feature_rules", {})


def load_weak_supervision(scene: str) -> Dict[str, Any]:
    config = load_scene_config(scene)
    return config.get("weak_supervision", {})


def load_normalized_dialogs(input_path: str) -> List[Dict[str, Any]]:
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("dialogs", [])


def count_keywords(text: str, keywords: List[str]) -> List[str]:
    if not text:
        return []
    return [kw for kw in keywords if kw in text]


def check_anchor_missing(turns: List[Dict[str, str]], anchor_keywords: List[str], confirm_keywords: List[str]) -> bool:
    for i, turn in enumerate(turns[:-1]):
        if turn.get("role") == "user" and turn.get("text") in {"嗯", "好的", "行", "对", "是"}:
            next_turns = turns[i + 1:i + 3]
            next_agent_text = " ".join(t.get("text", "") for t in next_turns if t.get("role") == "agent")
            if next_agent_text:
                has_confirm = any(kw in next_agent_text for kw in confirm_keywords)
                has_anchor = any(kw in next_agent_text for kw in anchor_keywords)
                if not has_confirm and not has_anchor:
                    return True
    return False


def detect_special_scenes(user_text: str, special_keywords: Dict[str, List[str]]) -> List[str]:
    detected = []
    for scene_name, keywords in special_keywords.items():
        if any(kw in user_text for kw in keywords):
            detected.append(scene_name)
    return detected


def detect_repeated_push(turns: List[Dict[str, str]], push_keywords: List[str]) -> bool:
    hits = 0
    for turn in turns:
        if turn.get("role") == "agent" and any(kw in turn.get("text", "") for kw in push_keywords):
            hits += 1
    return hits >= 2


def detect_long_monologue(meta: Dict[str, Any]) -> bool:
    return meta.get("avg_agent_len", 0) >= 30 and meta.get("agent_turn_count", 0) >= meta.get("user_turn_count", 0)


def detect_early_hangup(meta: Dict[str, Any]) -> bool:
    return meta.get("turn_count", 0) <= 4 and meta.get("dialog_end_type") in {"user_stop", "possible_hangup"}


def detect_natural_close(turns: List[Dict[str, str]], natural_close_keywords: List[str]) -> bool:
    if not turns:
        return False
    tail = " ".join(t.get("text", "") for t in turns[-2:])
    return any(kw in tail for kw in natural_close_keywords)


def detect_scheduled_followup(turns: List[Dict[str, str]]) -> bool:
    text = " ".join(t.get("text", "") for t in turns)
    return any(k in text for k in ["半小时之后", "两点吧", "下午", "到时候联系", "回头联系", "稍后联系"])


def detect_user_response_decay(turns: List[Dict[str, str]]) -> bool:
    user_turns = [t.get("text", "") for t in turns if t.get("role") == "user"]
    if len(user_turns) < 3:
        return False
    first_half = user_turns[: max(1, len(user_turns)//2)]
    second_half = user_turns[max(1, len(user_turns)//2):]
    first_avg = sum(len(x) for x in first_half) / max(len(first_half), 1)
    second_avg = sum(len(x) for x in second_half) / max(len(second_half), 1)
    short_tail = sum(1 for x in second_half if len(x) <= 2)
    return second_avg < first_avg * 0.6 and short_tail >= max(1, len(second_half)//2)


def detect_product_objection(text: str) -> List[str]:
    keywords = ["利率高", "利息高", "额度低", "借不出来", "不划算", "太高了", "额度太低", "失败过"]
    return [k for k in keywords if k in text]


def detect_conversation_rejection(text: str) -> List[str]:
    keywords = ["不用了", "不需要", "别打了", "挂了", "不想听", "不方便", "别说了", "就这样"]
    return [k for k in keywords if k in text]


def detect_agent_negative_sentiment(text: str) -> List[str]:
    keywords = ["烦不烦", "骚扰", "骗人", "有病吧", "黑名单"]
    return [k for k in keywords if k in text]


def detect_stage(turns: List[Dict[str, str]], stage_keywords: Dict[str, Any]) -> Dict[str, Any]:
    """检测对话到达的最高流程阶段"""
    stage_order = ["stage_a", "stage_b", "stage_c", "stage_d"]
    stage_reached = "stage_a"  # 默认至少在 A
    stage_confidence = 0.5
    all_text = " ".join(t.get("text", "") for t in turns)

    for stage_key in stage_order:
        cfg = stage_keywords.get(stage_key, {})
        agent_markers = cfg.get("agent_markers", [])
        user_markers = cfg.get("user_markers", [])
        agent_hits = sum(1 for kw in agent_markers if kw in all_text)
        user_hits = sum(1 for kw in user_markers if kw in all_text)
        total = len(agent_markers) + len(user_markers)
        if total > 0 and (agent_hits + user_hits) >= max(1, total * 0.15):
            stage_reached = stage_key
            stage_confidence = min(1.0, (agent_hits + user_hits) / max(total, 1))

    # 确定对话在哪个阶段断开
    last_user_turns = [t for t in turns if t.get("role") == "user"]
    last_user_text = last_user_turns[-1].get("text", "") if last_user_turns else ""
    break_stage = stage_reached  # 断开阶段 = 最高到达阶段

    return {
        "stage_reached": stage_reached,
        "stage_confidence": round(stage_confidence, 2),
        "break_stage": break_stage,
        "is_stage_a_drop": stage_reached == "stage_a" and break_stage == "stage_a",
        "is_mid_flow_drop": stage_reached in ["stage_b", "stage_c"],
    }


def detect_user_question_types(user_text: str, question_types: Dict[str, Any]) -> Dict[str, Any]:
    """检测用户主动提问的具体类型"""
    found_types = []
    for qtype, cfg in question_types.items():
        keywords = cfg.get("keywords", [])
        hits = [kw for kw in keywords if kw in user_text]
        if hits:
            found_types.append({
                "type": qtype,
                "description": cfg.get("description", ""),
                "matched_keywords": hits,
            })
    return {
        "has_question": len(found_types) > 0,
        "question_types": found_types,
        "question_count": len(found_types),
    }


def detect_interruption_and_reconnect(
    turns: List[Dict[str, str]],
    interruption_cfg: Dict[str, Any],
    reconnection_cfg: Dict[str, Any],
) -> Dict[str, Any]:
    """检测用户打断和机器人拉回情况"""
    interruption_kw = interruption_cfg.get("user_interruption_keywords", [])
    topic_shift_kw = interruption_cfg.get("user_topic_shift_keywords", [])
    reconnect_kw = reconnection_cfg.get("agent_reconnect_keywords", [])

    interruptions = []
    reconnects = []
    failed_reconnects = []

    for i, turn in enumerate(turns):
        if turn.get("role") != "user":
            continue
        text = turn.get("text", "")
        is_interruption = any(kw in text for kw in interruption_kw)
        is_topic_shift = any(kw in text for kw in topic_shift_kw)

        if is_interruption or is_topic_shift:
            interruption_type = "interruption" if is_interruption else "topic_shift"
            # Check if agent reconnects in the next 2 turns
            next_turns = turns[i + 1 : i + 3]
            agent_response = " ".join(
                t.get("text", "") for t in next_turns if t.get("role") == "agent"
            )
            has_reconnect = any(kw in agent_response for kw in reconnect_kw)

            entry = {
                "turn_index": i,
                "user_text": text[:80],
                "type": interruption_type,
                "agent_reconnected": has_reconnect,
            }
            interruptions.append(entry)
            if has_reconnect:
                reconnects.append(entry)
            else:
                failed_reconnects.append(entry)

    return {
        "interruption_count": len(interruptions),
        "reconnect_count": len(reconnects),
        "failed_reconnect_count": len(failed_reconnects),
        "interruptions": interruptions[:10],  # cap detail
    }


def detect_compliance_risk_extended(agent_text: str, compliance_cfg: Dict[str, Any]) -> Dict[str, Any]:
    """扩展版合规风险检测"""
    found_risks = []
    for risk_type, cfg in compliance_cfg.items():
        keywords = cfg.get("keywords", [])
        hits = [kw for kw in keywords if kw in agent_text]
        if hits:
            found_risks.append({
                "type": risk_type,
                "description": cfg.get("description", ""),
                "matched_keywords": hits,
            })
    return {
        "has_compliance_risk": len(found_risks) > 0,
        "risk_details": found_risks,
        "risk_count": len(found_risks),
    }


def extract_features(dialog: Dict[str, Any], feature_rules: Dict[str, Any]) -> Dict[str, Any]:
    user_text = dialog.get("user_text", "")
    agent_text = dialog.get("agent_text", "")
    turns = dialog.get("turns", [])
    meta = dialog.get("meta", {})

    features = {
        "dialog_id": dialog.get("dialog_id"),
        "explicit_rejection": count_keywords(user_text, feature_rules.get("user_refusal", {}).get("keywords", [])),
        "product_objection": detect_product_objection(user_text),
        "conversation_rejection": detect_conversation_rejection(user_text),
        "busy_hits": count_keywords(user_text, feature_rules.get("user_busy", {}).get("keywords", [])),
        "question_hits": count_keywords(user_text, feature_rules.get("user_question", {}).get("keywords", [])),
        "explicit_interest": count_keywords(user_text, feature_rules.get("user_interest", {}).get("keywords", [])),
        "explicit_acceptance": count_keywords(user_text, feature_rules.get("user_acceptance", {}).get("keywords", [])),
        "negative_emotion": count_keywords(user_text, feature_rules.get("user_negative_emotion", {}).get("keywords", [])),
        "agent_negative_sentiment": detect_agent_negative_sentiment(user_text),
        "terminal_hits": count_keywords(user_text, feature_rules.get("user_terminal", {}).get("keywords", [])),
        "forbidden_hits": count_keywords(agent_text, feature_rules.get("agent_forbidden", {}).get("keywords", [])),
        "benefit_hits": count_keywords(agent_text, feature_rules.get("agent_benefit", {}).get("keywords", [])),
        "confirm_hits": count_keywords(agent_text, feature_rules.get("agent_confirm", {}).get("keywords", [])),
        "push_hits": count_keywords(agent_text, feature_rules.get("agent_push", {}).get("keywords", [])),
        "anchor_missing": check_anchor_missing(
            turns,
            feature_rules.get("agent_anchor", {}).get("keywords", []),
            feature_rules.get("agent_confirm", {}).get("keywords", []),
        ),
        "special_scenes": detect_special_scenes(user_text, feature_rules.get("special_scene_keywords", {})),
        "long_agent_monologue": detect_long_monologue(meta),
        "agent_repeated_push": detect_repeated_push(turns, feature_rules.get("agent_push", {}).get("keywords", [])),
        "early_hangup": detect_early_hangup(meta),
        "natural_close": detect_natural_close(turns, feature_rules.get("natural_close", {}).get("keywords", [])),
        "scheduled_followup": detect_scheduled_followup(turns),
        "user_response_decay": detect_user_response_decay(turns),
        "dialog_end_type": meta.get("dialog_end_type", "unknown"),
        "asr_noise_score": meta.get("asr_noise_score", 0.0),
    }

    # === 新增：流程阶段检测 ===
    stage_keywords = feature_rules.get("stage_keywords", {})
    if stage_keywords:
        stage_info = detect_stage(turns, stage_keywords)
        features["stage_reached"] = stage_info["stage_reached"]
        features["stage_confidence"] = stage_info["stage_confidence"]
        features["break_stage"] = stage_info["break_stage"]
        features["is_stage_a_drop"] = stage_info["is_stage_a_drop"]
        features["is_mid_flow_drop"] = stage_info["is_mid_flow_drop"]

    # === 新增：用户提问分类 ===
    question_types = feature_rules.get("user_question_types", {})
    if question_types:
        q_info = detect_user_question_types(user_text, question_types)
        features["user_question_detail"] = q_info

    # === 新增：流程打断与拉回 ===
    interruption_cfg = feature_rules.get("interruption_signals", {})
    reconnection_cfg = feature_rules.get("reconnection_signals", {})
    if interruption_cfg:
        ir_info = detect_interruption_and_reconnect(turns, interruption_cfg, reconnection_cfg)
        features["interruption_count"] = ir_info["interruption_count"]
        features["reconnect_count"] = ir_info["reconnect_count"]
        features["failed_reconnect_count"] = ir_info["failed_reconnect_count"]
        features["interruption_detail"] = ir_info["interruptions"]

    # === 新增：扩展合规风险 ===
    compliance_cfg = feature_rules.get("compliance_keywords", {})
    if compliance_cfg:
        cr_info = detect_compliance_risk_extended(agent_text, compliance_cfg)
        features["compliance_risk_detail"] = cr_info

    return features


def build_signals(features: Dict[str, Any]) -> Dict[str, List[str]]:
    positive, negative, risk, quality = [], [], [], []

    if features.get("explicit_acceptance"):
        positive.append("explicit_acceptance")
    if features.get("explicit_interest"):
        positive.append("explicit_interest")
    if features.get("benefit_hits") and features.get("explicit_interest"):
        positive.append("request_followup_action")
    if features.get("natural_close"):
        positive.append("natural_close")
    if features.get("scheduled_followup"):
        positive.append("scheduled_followup")

    if features.get("product_objection"):
        negative.append("product_objection")
    if features.get("conversation_rejection"):
        negative.append("conversation_rejection")
    if features.get("negative_emotion"):
        negative.append("product_negative_sentiment")
    if features.get("agent_negative_sentiment"):
        negative.append("agent_negative_sentiment")
    if features.get("early_hangup"):
        negative.append("early_hangup")
    if features.get("agent_repeated_push"):
        negative.append("agent_repeated_push")
    if features.get("long_agent_monologue"):
        negative.append("long_agent_monologue")
    if features.get("user_response_decay"):
        negative.append("user_response_decay")
    if features.get("anchor_missing"):
        negative.append("state_anchor_missed")

    forbidden_hits = features.get("forbidden_hits", [])
    if forbidden_hits:
        risk.append("forbidden_expression")
    if any(k in forbidden_hits for k in ["保证", "一定", "肯定通过", "100%", "绝对"]):
        risk.append("compliance_risk")
    if features.get("conversation_rejection") and features.get("early_hangup"):
        risk.append("hangup_after_rejection")
    if (features.get("negative_emotion") or features.get("agent_negative_sentiment")) and features.get("early_hangup"):
        risk.append("hangup_after_negative_emotion")
    if features.get("long_agent_monologue") and features.get("early_hangup"):
        risk.append("hangup_after_long_monologue")
    if features.get("agent_repeated_push") and features.get("early_hangup"):
        risk.append("hangup_after_repeated_push")

    if features.get("product_objection") and (features.get("explicit_acceptance") or features.get("explicit_interest")):
        positive.append("engaged_objection")

    # === 新增信号 ===
    # 流程阶段信号
    if features.get("is_stage_a_drop"):
        negative.append("stage_a_drop")
    if features.get("is_mid_flow_drop"):
        negative.append("mid_flow_drop")

    # 用户提问信号
    q_detail = features.get("user_question_detail", {})
    if q_detail.get("has_question"):
        positive.append("user_active_question")
        for qt in q_detail.get("question_types", []):
            positive.append(f"user_question_{qt['type']}")

    # 打断与拉回信号
    if features.get("failed_reconnect_count", 0) >= 1:
        negative.append("failed_reconnect")
    if features.get("interruption_count", 0) >= 2 and features.get("reconnect_count", 0) == 0:
        negative.append("no_reconnect_on_interruption")
    if features.get("interruption_count", 0) >= 1 and features.get("reconnect_count", 0) >= 1:
        positive.append("successful_reconnect")

    # 扩展合规风险信号
    cr_detail = features.get("compliance_risk_detail", {})
    if cr_detail.get("has_compliance_risk"):
        risk.append("compliance_risk")
        for rd in cr_detail.get("risk_details", []):
            risk.append(f"compliance_{rd['type']}")

    if features.get("asr_noise_score", 0) >= 0.5:
        quality.append("high_asr_noise")
    if features.get("dialog_end_type") == "unknown":
        quality.append("uncertain_end_type")

    return {
        "positive": positive,
        "negative": negative,
        "risk": risk,
        "quality": quality,
    }


def compute_scores(signals: Dict[str, List[str]], weak_cfg: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:
    weights = weak_cfg.get("signal_weights", {})
    good_score = sum(weights.get(s, 0) for s in signals.get("positive", []))
    bad_score = sum(weights.get(s, 0) for s in signals.get("negative", [])) + sum(weights.get(s, 0) for s in signals.get("risk", []))

    confidence = 1.0
    noise = meta.get("asr_noise_score", 0.0)
    if noise >= 0.7:
        confidence -= 0.2
    elif noise >= 0.5:
        confidence -= 0.1
    if meta.get("speaker_switch_confidence", 1.0) < 0.5:
        confidence -= 0.15
    if meta.get("dialog_end_type") == "unknown":
        confidence -= 0.05
    confidence = round(max(0.0, min(confidence, 1.0)), 3)

    gray_score = max(0, 10 - abs(good_score - bad_score))
    return {
        "good_score": good_score,
        "bad_score": bad_score,
        "gray_score": gray_score,
        "confidence": confidence,
    }


def determine_seed_label(scores: Dict[str, Any], weak_cfg: Dict[str, Any], features: Dict[str, Any] = None) -> str:
    seed = weak_cfg.get("seed_thresholds", {})
    gray_cfg = weak_cfg.get("gray_thresholds", {})
    good_min = seed.get("good_seed_min", 8)
    bad_min = seed.get("bad_seed_min", 8)
    confidence_min = seed.get("confidence_min", 0.75)

    # 合规一票否决：agent 有合规风险 → 不得进入 good_seed
    has_compliance_veto = False
    if features:
        forbidden = features.get("forbidden_hits", [])
        if isinstance(forbidden, list) and len(forbidden) > 0:
            has_compliance_veto = True
        cr_detail = features.get("compliance_risk_detail", {})
        if isinstance(cr_detail, dict) and cr_detail.get("has_compliance_risk"):
            has_compliance_veto = True

    if scores["bad_score"] >= bad_min and scores["confidence"] >= confidence_min:
        return "bad_seed"
    if has_compliance_veto:
        # 有合规风险但用户接受了 → 降为 gray_high_risk，不进 good_seed
        if scores["good_score"] >= good_min:
            return "gray_high_risk"
        return "gray_high_risk" if scores["bad_score"] >= gray_cfg.get("high_risk_min", 6) else "gray"
    if scores["good_score"] >= good_min and scores["bad_score"] <= 3 and scores["confidence"] >= confidence_min:
        return "good_seed"
    if scores["bad_score"] >= gray_cfg.get("high_risk_min", 6):
        return "gray_high_risk"
    if scores["good_score"] >= gray_cfg.get("potential_good_min", 5):
        return "gray_potential_good"
    return "gray"


def summarize_reason(signals: Dict[str, List[str]], seed_label: str) -> str:
    signal_list = signals.get("positive", []) + signals.get("negative", []) + signals.get("risk", [])
    if not signal_list:
        return f"{seed_label}: 无明显高置信信号"
    return f"{seed_label}: 命中信号 {', '.join(signal_list[:4])}"


def process_dialogs(dialogs: List[Dict[str, Any]], scene: str) -> Dict[str, Any]:
    feature_rules = load_feature_rules(scene)
    weak_cfg = load_weak_supervision(scene)

    results = []
    stats = {
        "good_seed": 0,
        "bad_seed": 0,
        "gray": 0,
        "gray_high_risk": 0,
        "gray_potential_good": 0,
    }

    for dialog in dialogs:
        features = extract_features(dialog, feature_rules)
        signals = build_signals(features)
        scores = compute_scores(signals, weak_cfg, dialog.get("meta", {}))
        seed_label = determine_seed_label(scores, weak_cfg, features)
        stats[seed_label] = stats.get(seed_label, 0) + 1

        results.append({
            "dialog_id": dialog.get("dialog_id"),
            "seed_label": seed_label,
            "features": features,
            "signals": signals,
            "scores": scores,
            "reason_summary": summarize_reason(signals, seed_label),
            "dialog": dialog,
        })

    return {
        "stats": {"total": len(dialogs), **stats},
        "results": results,
        "created_at": datetime.now().isoformat(),
    }


def save_grayzone(match_result: Dict[str, Any], output_path: str) -> str:
    grayzone_path = output_path.replace(".json", "-grayzone.json")
    grayzone_dialogs = [r for r in match_result["results"] if r["seed_label"].startswith("gray")]

    with open(grayzone_path, "w", encoding="utf-8") as f:
        json.dump({
            "total": len(grayzone_dialogs),
            "dialogs": grayzone_dialogs,
            "created_at": datetime.now().isoformat(),
        }, f, ensure_ascii=False, indent=2)

    return grayzone_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="弱监督特征提取与 seed 分桶")
    parser.add_argument("--input", required=True, help="标准化对话 JSON")
    parser.add_argument("--scene", required=True, help="场景")
    parser.add_argument("--output", required=True, help="输出匹配结果 JSON")
    args = parser.parse_args()

    dialogs = load_normalized_dialogs(args.input)
    result = process_dialogs(dialogs, args.scene)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    grayzone_path = save_grayzone(result, args.output)

    print(f"✅ 弱监督特征提取完成: {args.output}")
    print(f"   - good_seed: {result['stats']['good_seed']} 条")
    print(f"   - bad_seed: {result['stats']['bad_seed']} 条")
    print(f"   - gray: {result['stats']['gray']} 条")
    print(f"   - gray_high_risk: {result['stats']['gray_high_risk']} 条")
    print(f"   - gray_potential_good: {result['stats']['gray_potential_good']} 条")
    print(f"   - gray 数据: {grayzone_path}")
