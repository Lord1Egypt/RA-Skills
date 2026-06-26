"""Intent routing policy — classifies intents and assigns agent roles.

Consensus Commons uses a policy-based router to decide which agent panel
should handle a given public intent. The router analyses the intent's
content and payload to produce a RouteDecision with:

* ``role`` — the primary domain category (e.g. "finance", "general")
* ``agents`` — the ordered list of agent roles to spawn
* ``is_supported`` — whether the intent is eligible for public council
* ``reason`` — human-readable explanation of the routing decision

Policies
========

* **finance / strategy / compliance** — capital allocation questions
  requiring financial analyst, contrarian, and compliance validator roles.
* **general analyst / contrarian / validator** — generic public decisions
  where no private data is needed.
* **reject** — topics that require private data, PII, or are otherwise
  inappropriate for public council.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from typing import Any

from cme.spacebase.models import Intent


@dataclass
class RouteDecision:
    """Output of the intent routing policy."""

    role: str
    agents: list[str] = field(default_factory=list)
    is_supported: bool = True
    reason: str = ""
    confidence: float = 1.0
    tags: list[str] = field(default_factory=list)


# Keyword sets for classification — lowercased, stripped of diacritics.

_FINANCE_KEYWORDS = {
    "capital", "allocation", "investment", "portfolio", "fund", "grant",
    "budget", "revenue", "financial", "cfo", "sec", "filing", "dividend",
    "equity", "debt", "roi", "irr", "npv", "treasury", "liquidity",
    "hedge", "risk", "audit", "compliance", "regulatory", "sox", "gaap",
    "ifrs", "market", "stock", "bond", "yield", "valuation", "credit",
    "loan", "interest", "inflation", "gdp", "fiscal", "monetary",
    "funding", "finance", "invest", "fund allocation", "capital allocation",
    "grant allocation",
}

_STRATEGY_KEYWORDS = {
    "strategy", "strategic", "roadmap", "plan", "planning", "initiative",
    "launch", "expansion", "pivot", "restructure", "merger", "acquisition",
    "partnership", "collaboration", "joint", "venture", "scale", "growth",
    "competitive", "advantage", "market entry", "product", "innovation",
    "r&d", "research", "development", "transformation", "digital",
    "okr", "kpi", "milestone", "objective", "goal", "target",
}

_GENERAL_KEYWORDS = {
    "should", "decide", "decision", "vote", "poll", "opinion", "public",
    "consensus", "agree", "disagree", "debate", "discuss", "council",
    "committee", "proposal", "recommend", "suggest", "evaluate", "assess",
    "compare", "choose", "select", "pick", "prefer", "best", "better",
    "option", "alternative", "tradeoff", "trade-off", "pros", "cons",
    "advantage", "disadvantage", "merit", "demerit", "criterion",
}

_REJECT_KEYWORDS = {
    "private", "confidential", "secret", "pii", "social security",
    "password", "credential", "internal", "proprietary", "classified",
    "hr", "salary", "compensation", "employee record", "medical",
    "health", "diagnosis", "personal", "identity", "ssn",
}


def _normalise(text: str) -> str:
    """Lowercase, strip diacritics, and collapse whitespace."""
    nfkd = unicodedata.normalize("NFKD", text)
    stripped = "".join(c for c in nfkd if not unicodedata.category(c).startswith("M"))
    return re.sub(r"\s+", " ", stripped.lower().strip())


def _keyword_score(text: str, keywords: set[str]) -> float:
    """Return 0.0–1.0 based on how many keywords match."""
    normalised = _normalise(text)
    words = set(normalised.split())
    direct_hits = words & keywords
    # Also check bigrams
    bigrams = {normalised[i:i + j] for i in range(len(normalised)) for j in range(4, 20)}
    bigram_hits = bigrams & keywords
    total_hits = len(direct_hits) + len(bigram_hits)
    if not keywords:
        return 0.0
    return min(1.0, total_hits / max(len(keywords) * 0.08, 1))


class IntentRouter:
    """Policy-based intent classifier.

    Analyses the intent content and produces a RouteDecision that tells
    the council which agents to spawn and whether the intent is eligible
    for public deliberation.
    """

    def __init__(self) -> None:
        self._custom_policies: list[tuple[str, set[str], list[str]]] = []

    def add_policy(self, role: str, keywords: set[str], agents: list[str]) -> None:
        """Register a custom routing policy.

        Policies are evaluated in order; the first policy with a score
        above the threshold wins.
        """
        self._custom_policies.append((role, keywords, agents))

    def classify(self, intent: Intent) -> RouteDecision:
        """Classify an intent and return a routing decision.

        The classifier uses comparative scoring across all domain policies
        and picks the best match. Rejection is checked first as a guard rail.

        1. Rejection guard — if PII/private keywords score > 0.2
        2. Score all domain policies (custom, finance, strategy, general)
        3. Pick the highest-scoring policy above its threshold
        4. Default — supported with general agent panel if nothing matches
        """
        content = intent.content
        payload_str = str(intent.payload) if intent.payload else ""

        # 1. Check rejection (always first)
        reject_score = max(
            _keyword_score(content, _REJECT_KEYWORDS),
            _keyword_score(payload_str, _REJECT_KEYWORDS),
        )
        if reject_score > 0.2:
            return RouteDecision(
                role="reject",
                is_supported=False,
                reason="Intent references private or confidential data. "
                       "This topic requires a private council and cannot be "
                       "processed in the public commons.",
                confidence=reject_score,
                tags=["private", "rejected"],
            )

        combined = f"{content} {payload_str}"

        # 2. Score all candidates and pick the best
        candidates: list[tuple[float, RouteDecision]] = []

        # Custom policies
        for role, keywords, agents in self._custom_policies:
            score = _keyword_score(combined, keywords)
            if score > 0.05:
                candidates.append((score, RouteDecision(
                    role=role,
                    agents=list(agents),
                    is_supported=True,
                    reason=f"Matched custom policy '{role}' (score={score:.2f}).",
                    confidence=score,
                    tags=["custom", role],
                )))

        # Finance
        finance_score = _keyword_score(combined, _FINANCE_KEYWORDS)
        if finance_score > 0.05:
            candidates.append((finance_score, RouteDecision(
                role="finance",
                agents=["financial-analyst", "contrarian", "compliance-validator"],
                is_supported=True,
                reason=f"Detected financial domain keywords (score={finance_score:.2f}). "
                       f"Routing to finance/strategy/compliance panel.",
                confidence=finance_score,
                tags=["finance", "capital-allocation"],
            )))

        # Strategy
        strategy_score = _keyword_score(combined, _STRATEGY_KEYWORDS)
        if strategy_score > 0.05:
            candidates.append((strategy_score, RouteDecision(
                role="strategy",
                agents=["strategic-analyst", "contrarian", "validator"],
                is_supported=True,
                reason=f"Detected strategic planning keywords (score={strategy_score:.2f}). "
                       f"Routing to strategy panel.",
                confidence=strategy_score,
                tags=["strategy", "planning"],
            )))

        # General
        general_score = _keyword_score(combined, _GENERAL_KEYWORDS)
        if general_score > 0.02:
            candidates.append((general_score, RouteDecision(
                role="general",
                agents=["analyst", "contrarian", "validator"],
                is_supported=True,
                reason=f"Detected general decision-making keywords (score={general_score:.2f}). "
                       f"Routing to general analyst/contrarian/validator panel.",
                confidence=general_score,
                tags=["general", "public-decision"],
            )))

        # Pick highest score
        if candidates:
            candidates.sort(key=lambda x: x[0], reverse=True)
            return candidates[0][1]

        # Default — supported but low confidence
        return RouteDecision(
            role="general",
            agents=["analyst", "contrarian", "validator"],
            is_supported=True,
            reason="No strong keyword match. Defaulting to general public "
                   "decision panel with analyst/contrarian/validator.",
            confidence=0.1,
            tags=["general", "default"],
        )
