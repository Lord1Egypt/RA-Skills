"""Design Policy Engine: IR slide -> archetype, by rules with confidence.

Plan decision D6: pure rules, dual evidence, confidence scores, and a
guaranteed-renderable fallback archetype. No LLM in this module — L1/L2
autonomy (P6) plugs in *around* it by choosing among the candidates this
module emits, never by inventing geometry.

Every decision is recorded as a Decision Trace entry (D10): structural
evidence only (counts/flags — content-free by construction).

Initial archetype set (grows via the local-hardening flywheel):
  kpi_wall        metrics dominate -> metric cards row + supporting stack
  full_table      a single table is the slide          -> full-canvas table
  quote_focus     a quote is the anchor                -> large quote + context
  list_stack      list(s) dominate                     -> bulleted panel(s)
  image_story     image is the anchor                  -> image + caption
  evidence_stack  THE FALLBACK: any content renders as a stack of cards
"""

from __future__ import annotations

from dataclasses import dataclass

FALLBACK_ARCHETYPE = "evidence_stack"
CONFIDENCE_FLOOR = 0.55

# P12-refine: supported page-level composition intent families.
_REFINE_TYPES = ("split", "wheel", "contrast", "spotlight")

# narrative_intent -> built-in style pack (v3 route_audience equivalent).
# The pack name is a filename stem under styles/; the engine resolves it.
_NARRATIVE_STYLE = {
    "report": "consulting-light",
    "proposal": "consulting-blueprint-hybrid",
    "product": "product-report",
    "research": "editorial-knowledge",
    "training": "technical-blueprint",
    "generic": "consulting-light",
}

# audience keyword fallbacks when narrative_intent is absent.
_AUDIENCE_STYLE = (
    ("executive", "consulting-light"),
    ("strategy", "consulting-light"),
    ("engineer", "technical-blueprint"),
    ("architect", "technical-blueprint"),
    ("product", "product-report"),
    ("operator", "product-report"),
    ("creator", "editorial-knowledge"),
    ("reader", "editorial-knowledge"),
)

DEFAULT_STYLE = "consulting-light"


def select_style_pack(ir: dict) -> str:
    """Choose a built-in style pack from the IR's narrative/audience signals.

    Content-aware styling (v3 route_audience): the deck's declared intent
    and audience select the visual system, so a McKinsey report renders in
    the boardroom blue palette, not the editorial warm-paper palette. The
    model supplies intent/audience as content metadata; it never picks
    colors directly — the mapping is engine-owned and deterministic.
    """
    deck = ir.get("deck", {}) or {}
    intent = deck.get("narrative_intent")
    if intent in _NARRATIVE_STYLE:
        return _NARRATIVE_STYLE[intent]
    audience = (deck.get("audience") or "").lower()
    for keyword, pack in _AUDIENCE_STYLE:
        if keyword in audience:
            return pack
    return DEFAULT_STYLE


@dataclass
class Decision:
    slide_id: str
    chosen: str
    confidence: float
    chosen_by: str  # rule | fallback | autonomy_l1 | autonomy_l2
    candidates: list[dict]
    evidence: list[dict]
    autonomy: dict | None = None  # P11: {"tier", "proposal_accepted"|"proposal_rejected", ...}


def _features(slide: dict) -> dict:
    counts: dict[str, int] = {}
    for block in slide.get("blocks", []):
        counts[block.get("role", "?")] = counts.get(block.get("role", "?"), 0) + 1
    blocks = slide.get("blocks", [])
    return {
        "block_count": len(blocks),
        "metric_count": counts.get("metric", 0),
        "table_count": counts.get("table", 0),
        "list_count": counts.get("list", 0),
        "quote_count": counts.get("quote", 0),
        "image_count": counts.get("image", 0),
        "fact_count": counts.get("fact", 0),
        "insight_count": counts.get("insight", 0),
        "risk_count": counts.get("risk", 0),
        "relation_count": len(slide.get("relations", []) or []),
        "has_steps": any(b.get("role") == "list" and b.get("semantics") in ("steps", "stages")
                         for b in blocks),
    }


def _candidates(f: dict) -> list[dict]:
    scores: list[dict] = []

    if f["metric_count"] >= 2:
        conf = min(0.6 + 0.1 * f["metric_count"], 0.95)
        scores.append({"choice": "kpi_wall", "confidence": round(conf, 2),
                       "rule_id": "rule-metrics-dominant"})
    if f["table_count"] == 1 and f["block_count"] <= 3:
        scores.append({"choice": "full_table", "confidence": 0.9,
                       "rule_id": "rule-single-table"})
    if f["quote_count"] >= 1 and f["block_count"] <= 3:
        scores.append({"choice": "quote_focus", "confidence": 0.75,
                       "rule_id": "rule-quote-anchor"})
    if f["image_count"] >= 1 and f["block_count"] <= 3:
        scores.append({"choice": "image_story", "confidence": 0.7,
                       "rule_id": "rule-image-anchor"})
    if f["has_steps"]:
        scores.append({"choice": "step_cards", "confidence": 0.85,
                       "rule_id": "rule-steps-sequence"})
    if f["list_count"] >= 1 and f["list_count"] + f["fact_count"] == f["block_count"] \
            and f["list_count"] >= f["fact_count"]:
        scores.append({"choice": "list_stack", "confidence": 0.7,
                       "rule_id": "rule-list-dominant"})

    scores.append({"choice": FALLBACK_ARCHETYPE, "confidence": 0.5,
                   "rule_id": "rule-fallback-always"})
    scores.sort(key=lambda c: (-c["confidence"], c["choice"]))
    return scores[:4]


def decide_slide(slide: dict) -> Decision:
    features = _features(slide)
    evidence = [{"feature": k, "value": v} for k, v in features.items()]

    # v4.1: an explicit chart/diagram payload is the strongest signal — the
    # model supplied structure (still content-only), the engine owns layout.
    if slide.get("chart"):
        choice = f"chart_{slide['chart'].get('type', 'column')}"
        candidates = [{"choice": choice, "confidence": 0.95,
                       "rule_id": "rule-llm-chart"}]
        return Decision(slide_id=slide["id"], chosen=choice, confidence=0.95,
                        chosen_by="rule", candidates=candidates,
                        evidence=evidence + [{"feature": "chart", "value": True}])
    if slide.get("diagram_ir"):
        dtype = slide["diagram_ir"].get("diagram_type", "causal_chain")
        choice = f"diagram_{dtype}"
        candidates = [{"choice": choice, "confidence": 0.9,
                       "rule_id": "rule-llm-diagram"}]
        return Decision(slide_id=slide["id"], chosen=choice, confidence=0.9,
                        chosen_by="rule", candidates=candidates,
                        evidence=evidence + [{"feature": "diagram", "value": dtype}])

    # P12-refine: explicit page-level composition intent (split/wheel/contrast/
    # spotlight). Structure is engine-validated; geometry and QA stay engine-owned.
    if slide.get("refine"):
        rtype = slide["refine"].get("type", "")
        choice = f"refine_{rtype}" if rtype else None
        if choice and rtype in _REFINE_TYPES:
            candidates = [{"choice": choice, "confidence": 0.85,
                           "rule_id": "rule-refine-intent"}]
            return Decision(slide_id=slide["id"], chosen=choice, confidence=0.85,
                            chosen_by="rule", candidates=candidates,
                            evidence=evidence + [{"feature": "refine", "value": rtype}])
        # unknown refine type -> fall through to rule archetype (honest degrade)

    candidates = _candidates(features)
    top = candidates[0]
    if top["confidence"] >= CONFIDENCE_FLOOR:
        chosen, chosen_by, confidence = top["choice"], "rule", top["confidence"]
    else:
        chosen, chosen_by, confidence = FALLBACK_ARCHETYPE, "fallback", 0.5
    return Decision(slide_id=slide["id"], chosen=chosen, confidence=confidence,
                    chosen_by=chosen_by, candidates=candidates, evidence=evidence)


def decide_deck(ir: dict) -> list[Decision]:
    return [decide_slide(slide) for slide in ir.get("slides", [])]


def decisions_to_trace(decisions: list[Decision], *, run_id: str, engine_version: str,
                       ir_sha256: str, style_pack: dict, autonomy_tier: str = "L0",
                       profile: str = "standard") -> dict:
    entries = []
    for idx, d in enumerate(decisions, 1):
        entry = {
            "decision_id": f"d-{idx:03d}",
            "slide_id": d.slide_id,
            "stage": "archetype",
            "evidence": {"structural": d.evidence},
            "candidates": d.candidates,
            "chosen": d.chosen,
            "chosen_by": d.chosen_by,
            "confidence": d.confidence,
        }
        if d.autonomy is not None:
            entry["autonomy"] = d.autonomy
        entries.append(entry)
    return {
        "schema_version": "4.0.0",
        "run": {
            "run_id": run_id,
            "engine_version": engine_version,
            "ir_sha256": ir_sha256,
            "style_pack": style_pack,
            "profile": profile,
            "autonomy_tier": autonomy_tier,
        },
        "decisions": entries,
    }
