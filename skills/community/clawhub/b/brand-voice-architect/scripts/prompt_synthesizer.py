"""
prompt_synthesizer.py
---------------------
Transforms brand pillars and constraints into a high-fidelity
system prompt ready for LLM deployment.
"""

from __future__ import annotations
import json
from dataclasses import dataclass, field
from typing import Literal


# ------------------------------------------------------------------
# Data model
# ------------------------------------------------------------------

@dataclass
class BrandConfig:
    name: str
    pillars: list[str]                            # 3 core attributes
    this_not_that: dict[str, str]                 # e.g. {"concise": "verbose"}
    complexity: Literal[
        "Short, punchy sentences",
        "Medium, balanced sentences",
        "Long, multi-clause structures",
    ]
    prohibited: list[str]                          # banned words
    preferred: list[str]                           # encouraged vocabulary
    tone_description: str
    formatting: str
    platforms: dict[str, str] = field(default_factory=dict)  # platform → pivot notes
    avg_sentence_length: float | None = None       # from corpus analysis
    cadence_variance: float | None = None          # from corpus analysis
    sentiment_temperature: float | None = None     # 0.0–1.0


# ------------------------------------------------------------------
# Core generator
# ------------------------------------------------------------------

def generate_system_prompt(config: BrandConfig) -> str:
    """Generate a deployable LLM system prompt from a BrandConfig."""

    this_not_that_block = "\n".join(
        f"  ✓ {this}  ✗ NOT {that}"
        for this, that in config.this_not_that.items()
    )

    platform_block = ""
    if config.platforms:
        lines = "\n".join(f"  - {k}: {v}" for k, v in config.platforms.items())
        platform_block = f"\n# PLATFORM PIVOTS:\n{lines}"

    metrics_block = ""
    metrics = []
    if config.avg_sentence_length is not None:
        metrics.append(f"  - Target ASL: {config.avg_sentence_length} words/sentence")
    if config.cadence_variance is not None:
        metrics.append(f"  - Cadence variance (σ): {config.cadence_variance}")
    if config.sentiment_temperature is not None:
        metrics.append(f"  - Sentiment temperature: {config.sentiment_temperature}/1.0")
    if metrics:
        metrics_block = "\n# CORPUS-DERIVED METRICS (match these):\n" + "\n".join(metrics)

    prompt = f"""# ROLE: {config.name} Brand Voice Engine

# CORE PILLARS:
{chr(10).join(f"  {i+1}. {p}" for i, p in enumerate(config.pillars))}

# THIS, NOT THAT:
{this_not_that_block}

# VOICE CONSTRAINTS:
  - Sentence Complexity: {config.complexity}
  - Prohibited Words: {", ".join(config.prohibited)}
  - Preferred Vocabulary: {", ".join(config.preferred)}
  - Tone: {config.tone_description}

# FORMATTING:
  - {config.formatting}
{metrics_block}
{platform_block}

# MISSION:
Transform every input into the brand's unique Linguistic DNA.
Never break voice for clarity alone — rephrase to stay on-brand.
When prohibited words appear in input, replace with a preferred equivalent silently.
"""
    return prompt.strip()


# ------------------------------------------------------------------
# Platform pivot generator
# ------------------------------------------------------------------

PLATFORM_DEFAULTS: dict[str, str] = {
    "LinkedIn": "Professional, first-person thought leadership. 150–300 words. No slang.",
    "Twitter/X": "Single punchy idea. Max 280 chars. Hook in first 5 words.",
    "Technical Docs": "Imperative voice. No marketing language. Code examples where relevant.",
    "Email": "Direct subject line. BLUF (Bottom Line Up Front). Clear CTA.",
    "Blog": "Narrative arc. Subheadings every 200–300 words. Conversational but expert.",
}


def generate_platform_pivot(config: BrandConfig, platform: str) -> str:
    """Adapt a brand voice for a specific platform while preserving core DNA."""
    note = config.platforms.get(platform) or PLATFORM_DEFAULTS.get(platform, "Standard voice guidelines apply.")
    return f"""
# {config.name} — {platform} Pivot

Core pillars still apply: {", ".join(config.pillars)}

Platform-specific guidance:
{note}

Prohibited words remain: {", ".join(config.prohibited)}
"""


# ------------------------------------------------------------------
# CLI / example usage
# ------------------------------------------------------------------

EXAMPLE_CONFIG = BrandConfig(
    name="TechNexus",
    pillars=["Clinical", "Forward-thinking", "Dense"],
    this_not_that={
        "precise": "vague",
        "systematic": "ad-hoc",
        "evidence-based": "opinionated",
    },
    complexity="Long, multi-clause structures",
    prohibited=["easy", "simple", "revolutionary", "game-changer"],
    preferred=["systematic", "optimized", "rigorous", "precise", "scalable"],
    tone_description="Objective and devoid of marketing fluff. Peer-reviewed paper energy.",
    formatting="Markdown with technical headers; bullet points for lists only",
    platforms={
        "LinkedIn": "Use first-person plural (we/our). Lead with a data point. No emojis.",
        "Technical Docs": "Imperative mood only. Every claim must be reproducible.",
    },
    avg_sentence_length=17.3,
    cadence_variance=4.2,
    sentiment_temperature=0.3,
)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            data = json.load(f)
        config = BrandConfig(**data)
    else:
        config = EXAMPLE_CONFIG

    print("=" * 60)
    print("GENERATED SYSTEM PROMPT")
    print("=" * 60)
    print(generate_system_prompt(config))
    print()

    if config.platforms:
        print("=" * 60)
        print("PLATFORM PIVOTS")
        print("=" * 60)
        for platform in config.platforms:
            print(generate_platform_pivot(config, platform))
