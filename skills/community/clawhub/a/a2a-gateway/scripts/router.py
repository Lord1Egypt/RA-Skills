"""
A2A Gateway v2 — Capability Router

Constraint-based routing: keyword matching (MVP) with scoring support.
Each candidate agent receives a capability_fit + context_fit + risk_fit score.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from schema import (
    new_routing_score, new_event, EventType, LatencyClass, ReliabilityTier,
)
from event_log import append

from registry import load as _load_registry


def _keyword_match(keyword: str, card: Dict[str, Any]) -> float:
    """
    Compute capability fit via keyword matching.
    Searches: skills, capabilities, name, description.
    Returns a score 0.0–1.0.
    """
    keyword_lower = keyword.lower()

    # Fields to search with different weights
    search_corpus = {
        "skills": " ".join(card.get("skills", [])).lower(),
        "capabilities": " ".join(card.get("capabilities", [])).lower(),
        "name": card.get("name", "").lower(),
        "description": card.get("description", "").lower(),
    }

    # Exact match in skills/capabilities → 1.0
    skills_lower = [s.lower() for s in card.get("skills", [])]
    caps_lower = [c.lower() for c in card.get("capabilities", [])]
    if keyword_lower in skills_lower or keyword_lower in caps_lower:
        return 1.0

    # Partial match
    if keyword_lower in search_corpus["skills"]:
        return 0.8
    if keyword_lower in search_corpus["capabilities"]:
        return 0.7
    if keyword_lower in search_corpus["name"]:
        return 0.5
    if keyword_lower in search_corpus["description"]:
        return 0.4

    # Fuzzy: individual word overlap
    kw_words = set(keyword_lower.split())
    for field in ["skills", "capabilities"]:
        field_words = set(search_corpus[field].split())
        overlap = len(kw_words & field_words)
        if overlap > 0:
            return min(0.3 + overlap * 0.1, 0.6)

    return 0.0


def _context_fit(card: Dict[str, Any]) -> float:
    """Compute context fit based on agent status and freshness."""
    status = card.get("status", "unknown")
    if status == "online":
        return 1.0
    elif status == "degraded":
        return 0.5
    else:
        return 0.1


def _risk_fit(card: Dict[str, Any]) -> float:
    """
    Compute risk fit based on contract fields.
    Lower risk = higher fit.
    """
    contract = card.get("contract", {})

    # Non-side-effect agents are safer
    side_effects = contract.get("side_effects", True)
    risk = 0.5 if not side_effects else 0.0

    # Reliability tier bonus
    tier = contract.get("reliability_tier", "at_most_once")
    if tier == ReliabilityTier.EXACTLY_ONCE.value:
        risk += 0.3
    elif tier == ReliabilityTier.AT_LEAST_ONCE.value:
        risk += 0.15

    return min(risk, 1.0)


def route(
    keyword: str,
    *,
    weights: Optional[Dict[str, float]] = None,
    min_score: float = 0.15,
    top_k: int = 3,
    exclude_agents: Optional[List[str]] = None,
    adaptive: bool = False,
) -> List[Dict[str, Any]]:
    """
    Route a keyword to the best matching agent(s).

    Returns a list of scored candidates, sorted by total score descending.
    Logs route.attempt and route.match/miss events.

    When adaptive=True, blends static keyword-matching scores with
    dynamic performance data from the agent performance ledger.
    """
    registry = _load_registry()
    exclude = set(exclude_agents or [])

    # Log route attempt
    append(new_event(
        event_type=EventType.ROUTE_ATTEMPT,
        payload={"keyword": keyword, "min_score": min_score},
    ))

    candidates: List[Tuple[float, Dict[str, Any]]] = []

    # Lazy import to avoid circular dependency
    adaptive_scorer = None
    if adaptive:
        from performance import reliability_score as _reliability
        adaptive_scorer = _reliability

    # Preload performance stats for adaptive mode
    perf_stats = {}
    if adaptive:
        from performance import rebuild_stats
        perf_stats = rebuild_stats()

    for agent_id, card in registry.items():
        if agent_id in exclude:
            continue

        capability_fit = _keyword_match(keyword, card)
        if capability_fit == 0.0:
            continue

        context_fit = _context_fit(card)
        risk_fit = _risk_fit(card)

        if adaptive and adaptive_scorer and agent_id in perf_stats:
            # Blend static scores with dynamic reliability
            perf_fit = adaptive_scorer(perf_stats[agent_id])
            w = weights or {"capability": 0.40, "context": 0.20, "risk": 0.15, "performance": 0.25}
            total = (
                capability_fit * w.get("capability", 0.40) +
                context_fit * w.get("context", 0.20) +
                risk_fit * w.get("risk", 0.15) +
                perf_fit * w.get("performance", 0.25)
            )
            score = {
                "agent_id": agent_id,
                "static_scores": {"capability_fit": capability_fit, "context_fit": context_fit, "risk_fit": risk_fit},
                "dynamic_scores": {"performance_fit": round(perf_fit, 4)},
                "weights": w,
                "total": round(total, 4),
            }
        else:
            score = new_routing_score(
                agent_id=agent_id,
                capability_fit=capability_fit,
                context_fit=context_fit,
                risk_fit=risk_fit,
                weights=weights,
            )

        if score["total"] >= min_score:
            candidates.append((score["total"], score))

    # Sort by total score descending
    candidates.sort(key=lambda x: x[0], reverse=True)

    result = [c[1] for c in candidates[:top_k]]

    if result:
        append(new_event(
            event_type=EventType.ROUTE_MATCH,
            payload={
                "keyword": keyword,
                "candidates": [
                    {"agent_id": r["agent_id"], "score": r["total"]}
                    for r in result
                ],
            },
        ))
    else:
        append(new_event(
            event_type=EventType.ROUTE_MISS,
            payload={"keyword": keyword, "reason": "No agents matched"},
        ))

    return result


def get_best_agent(keyword: str, **kwargs) -> Optional[Dict[str, Any]]:
    """Route and return the single best agent, or None."""
    results = route(keyword, top_k=1, **kwargs)
    return results[0] if results else None


# ── CLI ────────────────────────────────────────────────────────────────────

def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 router.py <keyword> [--top-k N] [--min-score M]")
        print()
        print("Example:")
        print("  python3 router.py 周报")
        print("  python3 router.py 报修 --top-k 3")
        sys.exit(1)

    keyword = sys.argv[1]
    top_k = 3
    min_score = 0.15

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--top-k" and i + 1 < len(sys.argv):
            top_k = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--min-score" and i + 1 < len(sys.argv):
            min_score = float(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    results = route(keyword, top_k=top_k, min_score=min_score)

    if not results:
        print(f"❌ No agents matched keyword '{keyword}'")
        sys.exit(1)

    print(f"🔍 Routing results for '{keyword}':")
    print("-" * 60)
    for r in results:
        print(f"  {r['agent_id']:<35}  score: {r['total']:.4f}")
        print(f"    capability={r['scores']['capability_fit']:.2f}  "
              f"context={r['scores']['context_fit']:.2f}  "
              f"risk={r['scores']['risk_fit']:.2f}")
        print()


if __name__ == "__main__":
    main()
