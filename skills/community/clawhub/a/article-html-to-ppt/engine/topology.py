"""Deterministic information-topology classification for Template planning."""

from __future__ import annotations


TOPOLOGIES = frozenset({
    "statement", "comparison", "trend", "sequence", "causal", "hierarchy",
    "matrix", "risk_mitigation", "dashboard", "method",
})

LEGACY_PATTERN_TO_TOPOLOGY = {
    "three-keyword cover": "statement",
    "three conclusion cards": "statement",
    "two-sided contrast": "comparison",
    "four-stage timeline": "sequence",
    "process comparison": "sequence",
    "multi-node comparison": "comparison",
    "chapter insight": "statement",
    "cycle relationship": "causal",
    "dual metric": "dashboard",
    "large-small comparison": "comparison",
    "native chart dashboard": "dashboard",
    "parallel function panels": "comparison",
    "funnel conclusion": "statement",
    "objective comparison": "comparison",
    "progression": "sequence",
    "parallel comparison": "comparison",
    "parallel leadership evidence": "comparison",
    "multi-node practice map": "matrix",
    "workflow capability map": "hierarchy",
    "layered workforce view": "hierarchy",
    "three-way comparison": "comparison",
    "outcome cards": "statement",
    "signal-uncertainty-action": "risk_mitigation",
    "risk and mitigation": "risk_mitigation",
    "pyramid": "hierarchy",
    "method relationship map": "method",
    "funnel priorities": "statement",
    "capability radar": "dashboard",
    "closing statement": "statement",
}


def infer_topology(content_page: dict, storyboard_page: dict) -> dict:
    """Classify information structure without silently guessing unknown intent.

    A structured content-binding declaration is authoritative.  Legacy layout
    patterns are a temporary migration signal only, preserving compatibility
    until every manuscript emits topology explicitly.
    """
    explicit = content_page.get("topology") if isinstance(content_page, dict) else None
    if isinstance(explicit, str) and explicit in TOPOLOGIES:
        return {"topology": explicit, "source": "content_binding"}
    rationale = storyboard_page.get("layout_rationale", {}) if isinstance(storyboard_page, dict) else {}
    pattern = rationale.get("layout_pattern") if isinstance(rationale, dict) else None
    inferred = LEGACY_PATTERN_TO_TOPOLOGY.get(pattern) if isinstance(pattern, str) else None
    if inferred is not None:
        return {"topology": inferred, "source": "legacy_pattern"}
    return {"topology": None, "source": "unclassified"}
