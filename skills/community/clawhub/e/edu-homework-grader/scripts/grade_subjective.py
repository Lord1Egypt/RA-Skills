"""Rubric-driven partial-credit scoring for short answer / essay / math."""
from __future__ import annotations
from typing import Any, Dict


def grade_subjective(item: Dict[str, Any], key: Dict[str, Any], rubric: Dict[str, Any] | None) -> Dict[str, Any]:
    max_pt = float(item.get("points", 10))
    student = item.get("student_answer", "") or ""
    keypoints = key.get("keypoints", [])  # list of {text, weight}
    earned = 0.0
    hit = []
    miss = []
    for kp in keypoints:
        kp_text = kp.get("text", "")
        weight = float(kp.get("weight", 1))
        if kp_text and kp_text in student:
            earned += weight
            hit.append(kp_text)
        else:
            miss.append(kp_text)
    total_weight = sum(float(kp.get("weight", 1)) for kp in keypoints) or 1.0
    scaled = round(earned / total_weight * max_pt, 1)
    return {
        "item_id": item["id"], "type": item["type"],
        "earned": scaled, "max": max_pt,
        "hit_keypoints": hit,
        "missed_keypoints": miss,
        "feedback": (
            f"覆盖关键点 {len(hit)}/{len(keypoints)}；缺失: {', '.join(miss[:3])}"
            if miss else "全部关键点已覆盖"
        ),
    }
