"""Deterministic scoring for MC / FIB / TF items."""
from __future__ import annotations
import re
from typing import Any, Dict, List, Set

def _normalize(s: str) -> str:
    if s is None: return ""
    s = str(s).strip()
    s = re.sub(r"\s+", "", s)
    # full-width to half-width digits and common punctuation
    trans = str.maketrans("０１２３４５６７８９，。；：（）", "0123456789,.;:()")
    return s.translate(trans).lower()

def grade_objective(item: Dict[str, Any], key: Dict[str, Any]) -> Dict[str, Any]:
    max_pt = float(item.get("points", 1))
    student = _normalize(item.get("student_answer", ""))
    correct = key.get("answer")
    if isinstance(correct, list):
        synonyms = set(_normalize(c) for c in correct)
        ok = student in synonyms
    else:
        synonyms_extra: Set[str] = set(_normalize(s) for s in key.get("synonyms", []))
        ok = student == _normalize(correct) or student in synonyms_extra
    return {
        "item_id": item["id"], "type": item["type"],
        "earned": max_pt if ok else 0.0, "max": max_pt,
        "correct": bool(ok),
        "feedback": "答案正确" if ok else f"参考答案: {correct}",
    }
