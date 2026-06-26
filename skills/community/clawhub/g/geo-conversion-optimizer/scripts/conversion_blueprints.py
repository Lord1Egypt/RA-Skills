"""
Helper models and utilities for the geo-conversion-optimizer skill.

This module is intentionally lightweight. It is designed as a reference
for how to represent GEO + conversion-aware page blueprints, calls to
action (CTAs), and simple experiment plans in a structured way.

You do not need to execute this file to use the skill. Treat it as an
optional helper and source of inspiration for data structures that
product, marketing, and engineering teams can adopt.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class CTA:
    """
    Represents a primary or secondary call-to-action on a page.
    """

    id: str
    label: str
    goal: str  # e.g., "free_trial", "book_demo", "add_to_cart"
    priority: str = "primary"  # "primary" or "secondary"
    location_hint: str = ""  # e.g., "hero", "mid-page", "footer"
    notes: str = ""


@dataclass
class Section:
    """
    Represents a logical section of a page or long-form content.
    """

    id: str
    title: str
    description: str
    geo_role: str  # how this section helps GEO / AI
    conversion_role: str  # how this section helps conversion
    key_elements: List[str] = field(default_factory=list)
    ctas: List[CTA] = field(default_factory=list)


@dataclass
class PageBlueprint:
    """
    High-level blueprint for a single page, designed for both GEO and conversion.
    """

    page_id: str
    page_type: str  # e.g., "saas_landing", "pdp", "comparison_article", "location_page"
    primary_goal: str  # business KPI this page should move
    secondary_goals: List[str] = field(default_factory=list)
    assumptions: Dict[str, Any] = field(default_factory=dict)
    sections: List[Section] = field(default_factory=list)


@dataclass
class ExperimentPlan:
    """
    Simple representation of an experiment plan for GEO + conversion changes.
    """

    id: str
    hypothesis: str
    variants: List[str]  # e.g., ["control", "geo_conv_variant_A"]
    primary_metric: str  # e.g., "conversion_rate", "add_to_cart_rate"
    guardrail_metrics: List[str] = field(default_factory=list)
    notes: str = ""


def example_saas_landing_blueprint() -> PageBlueprint:
    """
    Return an illustrative blueprint for a SaaS landing page
    that needs both GEO improvements and strong free-trial conversion.
    """

    hero_cta = CTA(
        id="hero_free_trial",
        label="Start free trial",
        goal="free_trial",
        priority="primary",
        location_hint="hero",
        notes="Emphasize low friction (no credit card required, if true).",
    )

    hero_section = Section(
        id="hero",
        title="Hero: Clear value proposition",
        description="Top-of-page section that states who the product is for and what main outcome it delivers.",
        geo_role="Provides concise, entity-rich description of the product and category for AI to understand relevance.",
        conversion_role="Quickly answers 'what is this?' and 'is it for me?' while presenting a strong primary CTA.",
        key_elements=[
            "Primary headline that names the category or job-to-be-done",
            "Short supporting subheading",
            "Primary CTA button",
            "Optional secondary CTA for low-commitment action",
        ],
        ctas=[hero_cta],
    )

    faq_section = Section(
        id="faqs",
        title="FAQs and objection handling",
        description="FAQ block targeting the most common questions and objections about the product and trial.",
        geo_role="Provides structured Q&A content that is easy for AI to cite and map to user questions.",
        conversion_role="Reduces friction and anxiety by proactively answering key objections before sign-up.",
        key_elements=[
            "Top 5–10 questions mapped to real user concerns",
            "Short, factual answers aligned with legal/compliance requirements",
        ],
        ctas=[],
    )

    return PageBlueprint(
        page_id="example_saas_landing",
        page_type="saas_landing",
        primary_goal="free_trial_signups",
        secondary_goals=["newsletter_signups"],
        assumptions={
            "traffic_source": "mixed organic + AI-recommended traffic",
            "stage": "consideration_to_decision",
        },
        sections=[hero_section, faq_section],
    )


def example_experiment_plan() -> ExperimentPlan:
    """
    Return an illustrative experiment plan for testing a GEO + conversion variant.
    """

    return ExperimentPlan(
        id="saas_landing_geo_conv_test",
        hypothesis=(
            "Adding a structured FAQ section and clarifying the hero value proposition "
            "will increase AI citability and maintain or improve free-trial conversion rate."
        ),
        variants=["control", "geo_conv_variant_A"],
        primary_metric="free_trial_conversion_rate",
        guardrail_metrics=["bounce_rate", "time_on_page"],
        notes="Run for a sufficient period to reach statistical confidence; monitor trial-to-paid conversion downstream.",
    )


__all__ = [
    "CTA",
    "Section",
    "PageBlueprint",
    "ExperimentPlan",
    "example_saas_landing_blueprint",
    "example_experiment_plan",
]

