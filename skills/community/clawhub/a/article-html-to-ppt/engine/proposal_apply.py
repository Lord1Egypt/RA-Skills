"""P11: autonomy proposal application — apply engine-validated L1/L2
proposals onto policy decisions.

L1 (advisor): the model picks an archetype from the engine's own candidate
menu (decide_deck candidates). Valid → adopted with the candidate's
confidence; invalid → fall back to the rule choice, recorded honestly.

L2 (constrained composition): the model proposes a row/column grid
assignment of block ids. Validated by validate_proposals(); if valid the
decision's archetype becomes ``proposed_grid`` and the proposal is carried
on the slide for layout_deck to consume. If invalid → rule fallback.

Neither tier ever invents geometry: the engine lays out everything; QA
gates the result; a rejected proposal is a degradation, never a failure.
"""

from __future__ import annotations

from typing import Any

from .autonomy import validate_proposals

PROPOSED_GRID = "proposed_grid"


def apply_proposals(ir: dict, decisions: list) -> dict:
    """Apply slide proposals onto the policy decisions.

    Returns a report dict:
      {
        "accepted": [{slide_id, tier, choice|rows}],
        "rejected": [{slide_id, tier, code, reason}],
        "no_proposal": [slide_id, ...],
      }
    Mutates decisions in place (Decision.chosen/confidence/chosen_by) and
    records the effective tier per slide on the Decision (``.autonomy``).
    """
    report: dict[str, list] = {"accepted": [], "rejected": [], "no_proposal": []}
    slides = {s["id"]: s for s in ir.get("slides", [])}
    decision_map = {d.slide_id: d for d in decisions}

    for slide_id, decision in decision_map.items():
        slide = slides.get(slide_id)
        proposal = (slide or {}).get("proposal") if slide else None
        if not proposal:
            report["no_proposal"].append(slide_id)
            continue

        tier = proposal.get("tier")
        if tier == "L1":
            _apply_l1(proposal, slide_id, decision, report)
        elif tier == "L2":
            _apply_l2(proposal, slide_id, decision, report, slides)
        else:
            report["rejected"].append({
                "slide_id": slide_id, "tier": tier or "?",
                "code": "PROPOSAL_TIER_UNKNOWN",
                "reason": f"unknown tier '{tier}'"})
            decision.autonomy = {"tier": "L0", "proposal_rejected": True,
                                 "code": "PROPOSAL_TIER_UNKNOWN"}
    return report


def _apply_l1(proposal: dict, slide_id: str, decision: Any, report: dict) -> None:
    choice = proposal.get("archetype_choice")
    if not choice:
        report["rejected"].append({
            "slide_id": slide_id, "tier": "L1",
            "code": "PROPOSAL_L1_NO_CHOICE",
            "reason": "L1 proposal missing archetype_choice"})
        decision.autonomy = {"tier": "L0", "proposal_rejected": True,
                             "code": "PROPOSAL_L1_NO_CHOICE"}
        return
    # the engine's own candidate menu for this slide
    menu = {c.get("choice") for c in decision.candidates}
    if choice not in menu:
        report["rejected"].append({
            "slide_id": slide_id, "tier": "L1", "choice": choice,
            "code": "PROPOSAL_L1_NOT_IN_MENU",
            "reason": f"'{choice}' not in engine candidate menu "
                      f"{sorted(menu)}"})
        decision.autonomy = {"tier": "L0", "proposal_rejected": True,
                             "code": "PROPOSAL_L1_NOT_IN_MENU",
                             "requested": choice}
        return
    cand = next(c for c in decision.candidates if c["choice"] == choice)
    decision.chosen = choice
    decision.confidence = cand["confidence"]
    decision.chosen_by = "autonomy_l1"
    decision.autonomy = {"tier": "L1", "proposal_accepted": True, "choice": choice}
    report["accepted"].append({"slide_id": slide_id, "tier": "L1", "choice": choice})


def _apply_l2(proposal: dict, slide_id: str, decision: Any, report: dict,
              slides: dict) -> None:
    rows = proposal.get("rows")
    if not rows:
        report["rejected"].append({
            "slide_id": slide_id, "tier": "L2",
            "code": "PROPOSAL_L2_NO_ROWS",
            "reason": "L2 proposal missing rows"})
        decision.autonomy = {"tier": "L0", "proposal_rejected": True,
                             "code": "PROPOSAL_L2_NO_ROWS"}
        return
    # validate_proposals reads slide.blocks for block ids; give it the slide
    ir_shape = {"slides": [slides.get(slide_id) or {"id": slide_id, "blocks": []}]}
    errors = validate_proposals([{
        "slide_id": slide_id, "rows": rows}], ir_shape)
    if errors:
        codes = sorted({e["code"] for e in errors})
        report["rejected"].append({
            "slide_id": slide_id, "tier": "L2",
            "code": codes[0] if codes else "PROPOSAL_L2_INVALID",
            "reason": "; ".join(e["message"] for e in errors[:3])})
        decision.autonomy = {"tier": "L0", "proposal_rejected": True,
                             "code": codes[0] if codes else "PROPOSAL_L2_INVALID"}
        return
    decision.chosen = PROPOSED_GRID
    decision.confidence = 0.85
    decision.chosen_by = "autonomy_l2"
    decision.autonomy = {"tier": "L2", "proposal_accepted": True,
                         "row_count": len(rows)}
    report["accepted"].append(
        {"slide_id": slide_id, "tier": "L2", "rows": rows})
