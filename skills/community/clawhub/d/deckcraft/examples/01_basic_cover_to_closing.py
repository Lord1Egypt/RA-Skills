#!/usr/bin/env python3
"""
Example 1: Basic Deck (Cover → Content → Closing)

The simplest DeckCraft workflow: 5 slides in 10 lines.
Use this as your starting template for any new deck.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine import DeckEngine

OUTPUT = os.path.join(os.path.dirname(__file__), "output", "01_basic_output.pptx")

eng = DeckEngine(theme_name="business", canvas="16:9")  # 16:9 widescreen (default)

# Stage 1: Cover
eng.cover(
    title="Q3 2026 Marketing Plan",
    subtitle="Strategic Roadmap & Budget Allocation",
    author="Marketing Team",
    date="June 3, 2026",
)

# Stage 2: Table of Contents
eng.toc(items=[
    ("01", "Market Context", "Industry & competitive landscape"),
    ("02", "Q2 Recap", "What we shipped, what we learned"),
    ("03", "Q3 Strategy", "Three-pillar plan"),
    ("04", "Budget & Timeline", "Spend by channel, milestones"),
])

# Stage 3: Section Divider
eng.section_divider("Market Context", section_number=1, subtitle="Where we are")

# Stage 4: Content Slide
eng.content(
    title="Industry Trends",
    bullets=[
        "Short-form video continues to dominate (3.2x engagement vs static)",
        "AI-generated content adoption up 47% YoY",
        "Privacy-first measurement becoming table stakes",
    ],
    key_point="Creators and AI tools are the new media plan, not just channels.",
)

# Stage 5: Closing
eng.closing(title="Thank You", message="Questions? Let's discuss.", contact="marketing@example.com")

eng.save(OUTPUT)
print(f"✓ Saved: {OUTPUT}")
print(f"  {eng._slide_count} slides, {eng.prs.slide_width/914400:.1f}\" × {eng.prs.slide_height/914400:.1f}\"")
