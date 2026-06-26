#!/usr/bin/env python3
"""
Example 6: Role Mode (v6.0+)

Demonstrates the optional "multi" role_mode for strategist → executor workflow.

In multi mode, DeckEngine provides:
  1. strategist_plan(brief) → returns a plan template (JSON schema)
  2. You feed the template to your LLM to fill in strategy
  3. execute_plan(filled_plan) → generates all slides from the plan

DeckEngine does NOT call any LLM. You control the LLM interaction.
This example shows the API with a manually-filled plan.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine import DeckEngine
import json

OUTPUT = os.path.join(os.path.dirname(__file__), "output", "06_role_mode_output.pptx")

# ── Step 1: Create engine with role_mode="multi" ──────────────────────

eng = DeckEngine(theme_name="business", canvas="16:9", role_mode="multi")

# ── Step 2: Define brief and get plan template ────────────────────────

brief = {
    "title": "Q3 2026 Strategy Review",
    "audience": "Executive Team",
    "goal": "Approve Q3 budget allocation",
    "duration": "20 min",
}

plan_template = eng.strategist_plan(brief)
print("📋 Plan template (schema):")
print(json.dumps(plan_template, indent=2, ensure_ascii=False))

# ── Step 3: Fill the plan (normally your LLM does this) ──────────────
#
# Here we manually fill it to demonstrate the API.
# In practice, you would:
#   1. Serialize plan_template to JSON
#   2. Send to your LLM with instructions to fill strategy + content_plan
#   3. Parse the LLM response back into a dict
#   4. Pass to execute_plan()

filled_plan = {
    "meta": {
        "source_brief": "Q3 2026 Strategy Review",
        "theme": "business",
        "canvas": "16:9",
    },
    "strategy": {
        "total_pages": 5,
        "page_allocation": [
            {"page": 1, "type": "cover"},
            {"page": 2, "type": "content"},
            {"page": 3, "type": "stat_cards"},
            {"page": 4, "type": "summary"},
            {"page": 5, "type": "closing"},
        ],
        "visual_style": "professional",
        "emphasis_pages": [3],
    },
    "content_plan": [
        {
            "type": "cover",
            "title": "Q3 2026 Strategy Review",
            "subtitle": "Budget & Growth Roadmap",
            "author": "Strategy Team",
            "date": "June 2026",
        },
        {
            "type": "content",
            "title": "Market Outlook",
            "bullets": [
                "AI adoption accelerating across enterprise verticals (+47% YoY)",
                "Short-form video content driving 3.2x engagement vs. static",
                "Privacy-first measurement becoming industry standard",
            ],
            "key_point": "The convergence of AI + video is the defining opportunity for Q3.",
        },
        {
            "type": "stat_cards",
            "title": "Key Metrics",
            "stats": [
                ("$12.4M", "Q2 Revenue"),
                ("47%", "YoY Growth"),
                ("89%", "Customer Retention"),
                ("156", "Enterprise Clients"),
            ],
        },
        {
            "type": "summary",
            "title": "Q3 Strategic Priorities",
            "key_points": [
                "Launch AI-powered content studio (budget: $2.1M)",
                "Expand enterprise sales team by 30%",
                "Achieve 95%+ customer retention through success programs",
            ],
            "conclusion": "Total Q3 investment: $8.5M → Projected ROI: 3.2x",
        },
        {
            "type": "closing",
            "title": "Thank You",
            "message": "Questions & Discussion",
            "contact": "strategy@company.com",
        },
    ],
}

# ── Step 4: Execute the plan ──────────────────────────────────────────

eng.execute_plan(filled_plan)
eng.save(OUTPUT)

print(f"\n✓ Saved: {OUTPUT}")
print(f"  {eng.slide_count} slides, role_mode={eng.role_mode!r}")
print(f"\n💡 Tip: In production, replace Step 3 with your LLM call.")
print(f"   Pass plan_template to the LLM, ask it to fill strategy + content_plan.")
