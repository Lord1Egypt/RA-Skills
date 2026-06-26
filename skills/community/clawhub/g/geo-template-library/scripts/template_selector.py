"""
template_selector.py

Helper functions for the `geo-template-library` skill.

These functions are illustrative and are not required for the skill to work.
They show how a deterministic system could map from a user scenario to one or
more template families defined in `references/templates-catalog.md`.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List


class TemplateType(str, Enum):
    DEFINITION_ARTICLE = "definition-article"
    FAQ_PAGE = "faq-page"
    COMPARISON_GUIDE = "comparison-guide"
    HOWTO_GUIDE = "howto-guide"
    STATS_ROUNDUP = "stats-roundup"
    PRODUCT_PAGE = "product-page"
    GEO_BLOG = "geo-blog"


@dataclass
class Scenario:
    """Lightweight representation of a user scenario."""

    goal: str
    main_query_pattern: str
    channel: str


def select_templates(scenario: Scenario) -> List[TemplateType]:
    """
    Very simple rule-based selector mapping a scenario to one or more template types.

    This is intentionally minimal; the real selection logic will be driven by the
    skill instructions and the LLM's reasoning rather than this code.
    """
    goal = scenario.goal.lower()
    query = scenario.main_query_pattern.lower()

    if "what is" in query or "definition" in goal:
        return [TemplateType.DEFINITION_ARTICLE]

    if "faq" in goal or "frequently asked" in goal:
        return [TemplateType.FAQ_PAGE]

    if " vs " in query or "compare" in goal or "comparison" in goal:
        return [TemplateType.COMPARISON_GUIDE]

    if "how to" in query or "step-by-step" in goal or "tutorial" in goal:
        return [TemplateType.HOWTO_GUIDE]

    if "statistics" in goal or "benchmarks" in goal or "data roundup" in goal:
        return [TemplateType.STATS_ROUNDUP]

    if "product" in goal or "feature" in goal or "landing page" in goal:
        return [TemplateType.PRODUCT_PAGE]

    channel = scenario.channel.lower()

    # Channel-based hints when intent is ambiguous.
    if "docs" in channel or "documentation" in channel or "knowledge base" in channel:
        return [TemplateType.HOWTO_GUIDE]

    if "blog" in channel:
        return [TemplateType.GEO_BLOG]

    # Fallback: use a GEO blog / deep-dive template.
    return [TemplateType.GEO_BLOG]


__all__ = ["TemplateType", "Scenario", "select_templates"]

