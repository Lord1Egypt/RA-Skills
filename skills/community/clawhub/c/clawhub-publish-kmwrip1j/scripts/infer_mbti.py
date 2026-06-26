#!/usr/bin/env python3
"""Infer MBTI from the evidence pool."""

from __future__ import annotations

import argparse
from collections import defaultdict
from itertools import product
from pathlib import Path
from typing import Dict, List, Tuple

from mbti_common import (
    AXIS_SIDES,
    TYPE_FUNCTIONS,
    clean_text,
    confidence_label,
    confidence_to_weight,
    family_for_type,
    family_label,
    iso_now,
    load_json,
    process_roles,
    strength_to_weight,
    type_label,
    visible_function_order,
    write_json,
)


AXIS_QUESTIONS = {
    "E/I": "在重要问题上，你更常先自己想清楚再表达，还是边聊边形成结论？",
    "S/N": "你更自然地抓住具体执行细节，还是先形成框架、模式和可能性？",
    "T/F": "做关键判断时，你更先看逻辑与代价，还是更先看意义与对人的影响？",
    "J/P": "面对外部安排、人和事情时，你更自然是先定下来推进，还是先保持开放继续了解与适应？",
}

SNAPSHOT_TEMPLATES = {
    "nt": "Your profile leans analytical, abstract, and systems-oriented, with a strong pull toward leverage, structure, and conceptual clarity.",
    "nf": "Your profile leans idealistic, interpretive, and people-aware, with meaning and pattern coherence showing up repeatedly in the evidence.",
    "st": "Your profile leans practical, grounded, and execution-focused, with attention to workable detail and operational reliability.",
    "sf": "Your profile leans relational, concrete, and support-oriented, with repeated evidence of interpersonal sensitivity and practical care.",
}

NARRATIVE_TEMPLATES = {
    "E": "You often externalize energy through interaction, visible discussion, and collaborative framing.",
    "I": "You often consolidate internally first, showing more reflective or self-contained processing before expression.",
    "S": "You repeatedly return to concrete execution, implementation detail, and practical anchors.",
    "N": "You repeatedly move toward abstraction, pattern recognition, and future-facing framing.",
    "T": "Your evaluations often privilege logic, structure, contradiction checks, and tradeoff language.",
    "F": "Your evaluations often preserve meaning, values, and human impact rather than logic alone.",
    "J": "You show a noticeable drive toward closure, explicit next steps, and external structure.",
    "P": "You show a noticeable preference for optionality, exploration, and delayed closure while learning.",
}

PRESSURE_NOTES = {
    "I": "Under pressure, you may narrow too far and over-hold conclusions before sharing them.",
    "E": "Under pressure, you may process in public too quickly and outrun quieter signals.",
    "S": "Under pressure, you may over-anchor on what is already proven and underweight emerging possibilities.",
    "N": "Under pressure, you may over-index on patterns and skip concrete constraints.",
    "T": "Under pressure, your clarity can read as bluntness or overcorrection.",
    "F": "Under pressure, preserving alignment can delay necessary friction.",
    "J": "Under pressure, you may rush closure before enough evidence has landed.",
    "P": "Under pressure, you may keep too many options open and postpone commitment too long.",
}


def evidence_weight(item: Dict) -> float:
    return round(
        strength_to_weight(item["strength"])
        * confidence_to_weight(item["confidence"])
        * max(0.5, float(item["independence_score"])),
        3,
    )


def aggregate_dimensions(evidence_pool: List[Dict]) -> Tuple[Dict[str, Dict], Dict[str, float]]:
    axis_scores = {axis: defaultdict(float) for axis, _, _ in AXIS_SIDES}
    evidence_weights: Dict[str, float] = {}
    for item in evidence_pool:
        evidence_weights[item["evidence_id"]] = evidence_weight(item)
        if item["is_pseudosignal"]:
            continue
        for hint in item["dimension_hints"]:
            axis_scores[hint["axis"]][hint["side"]] += evidence_weights[item["evidence_id"]]

    results: Dict[str, Dict] = {}
    for axis, left, right in AXIS_SIDES:
        left_score = axis_scores[axis][left]
        right_score = axis_scores[axis][right]
        total = left_score + right_score
        if total <= 0.0:
            results[axis] = {
                "axis": axis,
                "left": left,
                "right": right,
                "selected": "?",
                "left_weight": 0.0,
                "right_weight": 0.0,
                "left_pct": 50,
                "right_pct": 50,
                "margin": 0.0,
                "confidence": "low",
            }
            continue
        left_pct = round((left_score / total) * 100)
        right_pct = 100 - left_pct
        margin = abs(left_score - right_score) / total
        selected = left if left_score >= right_score else right
        confidence = "high" if margin >= 0.3 else "medium" if margin >= 0.14 else "low"
        results[axis] = {
            "axis": axis,
            "left": left,
            "right": right,
            "selected": selected,
            "left_weight": round(left_score, 3),
            "right_weight": round(right_score, 3),
            "left_pct": left_pct,
            "right_pct": right_pct,
            "margin": round(margin, 3),
            "confidence": confidence,
        }
    return results, evidence_weights


def evidence_ids_for_side(evidence_pool: List[Dict], axis: str, side: str) -> List[str]:
    matches = []
    for item in evidence_pool:
        if item["is_pseudosignal"]:
            continue
        if any(hint["axis"] == axis and hint["side"] == side for hint in item["dimension_hints"]):
            matches.append(item["evidence_id"])
    return matches


def build_candidate_types(dimension_results: Dict[str, Dict]) -> List[str]:
    options = []
    for axis, left, right in AXIS_SIDES:
        selected = dimension_results[axis]["selected"]
        if selected == "?":
            options.append([left, right])
        elif dimension_results[axis]["confidence"] == "low":
            options.append([selected, right if selected == left else left])
        else:
            options.append([selected])
    candidates = ["".join(parts) for parts in product(*options)]
    return sorted(set(candidates))[:8]


def function_weights(evidence_pool: List[Dict], evidence_weight_map: Dict[str, float]) -> Dict[str, float]:
    scores = defaultdict(float)
    for item in evidence_pool:
        if item["is_pseudosignal"]:
            continue
        weight = evidence_weight_map[item["evidence_id"]]
        for hint in item["function_hints"]:
            scores[hint["function"]] += weight
    return scores


def preference_score(type_code: str, dimension_results: Dict[str, Dict]) -> float:
    score = 0.0
    for index, (axis, left, right) in enumerate(AXIS_SIDES):
        result = dimension_results[axis]
        total = result["left_weight"] + result["right_weight"]
        if total <= 0:
            score += 0.5
            continue
        if type_code[index] == left:
            score += result["left_weight"] / total
        else:
            score += result["right_weight"] / total
    return round(score, 3)


def visible_function_consistency(type_code: str, function_score_map: Dict[str, float]) -> float:
    order = visible_function_order(type_code)
    slot_weights = [1.0, 0.78, 0.28, 0.12]
    consistency = 0.0
    for slot_weight, function_name in zip(slot_weights, order):
        consistency += slot_weight * function_score_map.get(function_name, 0.0)
    return round(consistency, 3)


def rank_candidates(candidates: List[str], dimension_results: Dict[str, Dict], function_score_map: Dict[str, float]) -> List[Dict]:
    ranked = []
    for type_code in candidates:
        roles = process_roles(type_code)
        ranked.append(
            {
                "type": type_code,
                "label": type_label(type_code),
                "family_key": family_for_type(type_code),
                "family_label": family_label(type_code),
                "preference_score": preference_score(type_code, dimension_results),
                "function_consistency": visible_function_consistency(type_code, function_score_map),
                "dominant_function": roles["dominant_function"],
                "auxiliary_function": roles["auxiliary_function"],
                "outer_function": roles["outer_function"],
                "jp_reflects": roles["jp_reflects"],
            }
        )
    ranked.sort(key=lambda item: (item["preference_score"], item["function_consistency"]), reverse=True)
    return ranked


def selected_evidence_ids(evidence_pool: List[Dict], evidence_weight_map: Dict[str, float], final_type: str) -> List[str]:
    chosen = []
    for index, (axis, _, _) in enumerate(AXIS_SIDES):
        side = final_type[index]
        ids = evidence_ids_for_side(evidence_pool, axis, side)
        ids.sort(key=lambda evidence_id: evidence_weight_map[evidence_id], reverse=True)
        chosen.extend(ids[:2])
    return list(dict.fromkeys(chosen))[:10]


def dimension_summaries(dimension_results: Dict[str, Dict], evidence_pool: List[Dict], evidence_weight_map: Dict[str, float]) -> Dict[str, Dict]:
    evidence_by_id = {item["evidence_id"]: item for item in evidence_pool}
    summaries: Dict[str, Dict] = {}
    for axis, left, right in AXIS_SIDES:
        result = dimension_results[axis]
        support_ids = evidence_ids_for_side(evidence_pool, axis, result["selected"]) if result["selected"] != "?" else []
        counter_side = right if result["selected"] == left else left
        counter_ids = evidence_ids_for_side(evidence_pool, axis, counter_side) if result["selected"] != "?" else []
        support_ids.sort(key=lambda evidence_id: evidence_weight_map[evidence_id], reverse=True)
        counter_ids.sort(key=lambda evidence_id: evidence_weight_map[evidence_id], reverse=True)
        summaries[axis] = {
            **result,
            "support_ids": support_ids[:3],
            "counter_ids": counter_ids[:2],
            "support_summary": [evidence_by_id[eid]["summary"] for eid in support_ids[:2]],
            "counter_summary": [evidence_by_id[eid]["summary"] for eid in counter_ids[:2]],
        }
    return summaries


def build_followups(dimension_results: Dict[str, Dict]) -> List[str]:
    questions = []
    for axis, result in dimension_results.items():
        if result["confidence"] == "low":
            questions.append(AXIS_QUESTIONS[axis])
    return questions[:4]


def build_followup_items(dimension_results: Dict[str, Dict]) -> List[Dict[str, str]]:
    items = []
    for axis, result in dimension_results.items():
        if result["confidence"] != "low":
            continue
        items.append(
            {
                "axis": axis,
                "selected": result["selected"],
                "confidence": result["confidence"],
                "question": AXIS_QUESTIONS[axis],
                "support_summary": "; ".join(result["support_summary"]) or "No clear support extracted.",
                "counter_summary": "; ".join(result["counter_summary"]) or "No strong opposing pattern captured.",
            }
        )
    return items[:4]


def overall_confidence(dimension_results: Dict[str, Dict], candidates: List[Dict]) -> Tuple[float, str]:
    conf_scores = {"low": 0.4, "medium": 0.65, "high": 0.85}
    avg = sum(conf_scores[result["confidence"]] for result in dimension_results.values()) / len(dimension_results)
    if len(candidates) >= 2:
        gap = candidates[0]["preference_score"] - candidates[1]["preference_score"]
        avg += min(0.08, max(0.0, gap / 2.2))
    avg = max(0.35, min(0.92, round(avg, 3)))
    return avg, confidence_label(avg)


def build_strength_cards(type_code: str) -> List[Dict[str, str]]:
    family = family_for_type(type_code)
    cards = {
        "nt": [
            ("Conceptual leverage", "You seem comfortable compressing messy material into structures, patterns, and operating models."),
            ("System pressure testing", "You often surface contradictions or weak assumptions instead of letting them slide."),
            ("Strategic range", "The evidence repeatedly points to future-oriented reasoning rather than purely local optimization."),
        ],
        "nf": [
            ("Meaning sensitivity", "You seem to notice what matters, not just what works in the narrow sense."),
            ("Patterned empathy", "You often connect interpersonal consequences with deeper motives or values."),
            ("Narrative coherence", "You tend to synthesize people, ideas, and direction into a unified picture."),
        ],
        "st": [
            ("Operational reliability", "You seem anchored in what can actually be done, shipped, verified, or maintained."),
            ("Concrete problem solving", "You repeatedly move toward specific constraints, details, and execution hooks."),
            ("Stability under load", "You appear comfortable grounding decisions in what is observable and testable."),
        ],
        "sf": [
            ("Practical care", "You seem to translate attention to people into concrete, usable action."),
            ("Interpersonal steadiness", "You often preserve continuity, support, and workable social flow."),
            ("Grounded responsiveness", "The evidence suggests you stay close to what is present and humanly relevant."),
        ],
    }
    return [{"title": title, "body": body} for title, body in cards[family]]


def build_blindspot_cards(type_code: str) -> List[Dict[str, str]]:
    family = family_for_type(type_code)
    cards = {
        "nt": [
            ("Underweighting emotional context", "Strong structural reasoning can make softer interpersonal signals easier to miss."),
            ("Premature abstraction", "Pattern confidence can outrun the practical specifics needed by other people."),
        ],
        "nf": [
            ("Overprotecting alignment", "A strong values lens can delay friction that would actually clarify the issue."),
            ("Narrative overreach", "Pattern and meaning synthesis can occasionally jump past the most grounded reading."),
        ],
        "st": [
            ("Constraint lock-in", "What is proven can crowd out higher-variance but high-upside possibilities."),
            ("Local optimization bias", "Execution focus can reduce attention to broader narrative or symbolic factors."),
        ],
        "sf": [
            ("Harmony drag", "Preserving stability and goodwill can make sharper boundary-setting slower than needed."),
            ("Soft conflict handling", "A people-aware stance can under-serve decisions that require crisp disagreement."),
        ],
    }
    return [{"title": title, "body": body} for title, body in cards[family]]


def build_pressure_cards(type_code: str) -> List[Dict[str, str]]:
    cards = []
    for letter in type_code:
        cards.append({"title": letter, "body": PRESSURE_NOTES[letter]})
    return cards[:3]


def narrative_for_type(type_code: str) -> str:
    pieces = [SNAPSHOT_TEMPLATES[family_for_type(type_code)]]
    for letter in type_code:
        pieces.append(NARRATIVE_TEMPLATES[letter])
    return " ".join(pieces[:3])


def adjacent_comparisons(final_type: str, candidates: List[Dict]) -> List[Dict[str, str]]:
    comparisons = []
    for candidate in candidates[1:3]:
        comparisons.append(
            {
                "title": candidate["type"],
                "body": clean_text(
                    f"{candidate['type']} stayed in range because parts of the evidence still point in its direction, "
                    f"but {final_type} kept the lead on the four preference axes. Function hints were used only as a secondary coherence check."
                ),
            }
        )
    return comparisons


def uncertainty_cards(dimension_results: Dict[str, Dict], followups: List[str]) -> List[Dict[str, str]]:
    cards = []
    for axis, result in dimension_results.items():
        if result["confidence"] == "low":
            cards.append(
                {
                    "title": axis,
                    "body": "This axis remains weakly separated. The available evidence leans one way, but the counter-pattern is still active.",
                }
            )
    for question in followups:
        cards.append({"title": "Follow-up", "body": question})
    return cards or [{"title": "Current state", "body": "No major unresolved axis stood out after evidence pooling."}]


def function_validation(type_code: str, function_score_map: Dict[str, float]) -> Dict:
    roles = process_roles(type_code)
    visible_order = visible_function_order(type_code)
    visible_scores = {function_name: function_score_map.get(function_name, 0.0) for function_name in visible_order[:4]}
    if type_code.startswith("I"):
        summary = clean_text(
            f"Under Myers's model, {type_code} shows its auxiliary more readily in outward behavior than its dominant. "
            f"For this type, the expected outer process is {roles['outer_function']} and the dominant inner process is {roles['dominant_function']}. "
            f"The observed function hints were checked against that visible order, but they did not override the four-axis preference result."
        )
    else:
        summary = clean_text(
            f"Under Myers's model, {type_code} tends to show its dominant process directly in the outer world. "
            f"For this type, the expected outer process is {roles['outer_function']}, supported by the auxiliary {roles['auxiliary_function']}. "
            f"The observed function hints were used as a coherence check, not as the main classifier."
        )
    return {
        "dominant_function": roles["dominant_function"],
        "auxiliary_function": roles["auxiliary_function"],
        "outer_function": roles["outer_function"],
        "jp_reflects": roles["jp_reflects"],
        "visible_order": visible_order,
        "function_scores": visible_scores,
        "summary": summary,
    }


def infer_payload(evidence_payload: Dict, source_summary: Dict) -> Dict:
    evidence_pool = evidence_payload["evidence_pool"]

    dim_results, evidence_weight_map = aggregate_dimensions(evidence_pool)
    dim_results = dimension_summaries(dim_results, evidence_pool, evidence_weight_map)

    candidates = build_candidate_types(dim_results)
    function_score_map = function_weights(evidence_pool, evidence_weight_map)
    candidate_rank = rank_candidates(candidates, dim_results, function_score_map)
    final_type = candidate_rank[0]["type"] if candidate_rank else "INTJ"
    followup_items = build_followup_items(dim_results)
    followups = [item["question"] for item in followup_items]
    confidence_score, confidence_text = overall_confidence(dim_results, candidate_rank)
    chosen_ids = selected_evidence_ids(evidence_pool, evidence_weight_map, final_type)
    function_check = function_validation(final_type, function_score_map)

    return {
        "generated_at": iso_now(),
        "source_summary": source_summary,
        "final_type": final_type,
        "type_label": type_label(final_type),
        "family_key": family_for_type(final_type),
        "family_label": family_label(final_type),
        "overall_confidence": {
            "score": confidence_score,
            "label": confidence_text,
        },
        "snapshot": narrative_for_type(final_type),
        "type_narrative": narrative_for_type(final_type),
        "dimension_results": dim_results,
        "function_validation": function_check,
        "candidate_types": candidate_rank[:4],
        "selected_evidence_ids": chosen_ids,
        "followup_questions": followups,
        "followup_items": followup_items,
        "needs_followup": bool(followup_items),
        "strengths": build_strength_cards(final_type),
        "blindspots": build_blindspot_cards(final_type),
        "pressure_patterns": build_pressure_cards(final_type),
        "adjacent_type_comparison": adjacent_comparisons(final_type, candidate_rank),
        "uncertainties": uncertainty_cards(dim_results, followups),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Infer MBTI from an evidence pool.")
    parser.add_argument("--evidence-pool", required=True, help="Path to evidence_pool.json")
    parser.add_argument("--source-summary", required=True, help="Path to source_summary.json")
    parser.add_argument("--output", required=True, help="Path to analysis_result.json")
    args = parser.parse_args()

    evidence_payload = load_json(Path(args.evidence_pool).expanduser().resolve())
    source_summary = load_json(Path(args.source_summary).expanduser().resolve())
    payload = infer_payload(evidence_payload, source_summary)
    write_json(Path(args.output).expanduser().resolve(), payload)


if __name__ == "__main__":
    main()
