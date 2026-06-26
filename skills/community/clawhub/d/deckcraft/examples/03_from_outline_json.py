#!/usr/bin/env python3
"""
Example 3: Generate from Outline JSON

Use a JSON file as the source of truth (e.g. from a CMS, Airtable, or AI).
The outline schema matches the CLI (generate_ppt.py) input format, so you can
swap between API and CLI without rewriting the outline.

Outline JSON schema (per page):
{
  "type": "cover" | "toc" | "section" | "content" | "stat_cards" | "chart_bar"
        | "vs_compare" | "summary" | "closing" | ...,
  "title": "...",
  ... (other fields depending on type — see scripts/generate_ppt.py for full mapping)
}
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine import DeckEngine

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTLINE = os.path.join(OUT_DIR, "output", "03_outline.json")
OUTPUT = os.path.join(OUT_DIR, "output", "03_from_outline.pptx")

# A realistic outline — could come from a CMS, Airtable, or be AI-generated
outline = {
    "theme": "tech",
    "canvas": "16:9",
    "pages": [
        {
            "type": "cover",
            "title": "Engineering Productivity Report",
            "subtitle": "Q1–Q2 2026",
            "author": "Platform Team",
            "date": "2026-06-03",
        },
        {
            "type": "toc",
            "items": [
                ["01", "Deploy Frequency", "How often we ship"],
                ["02", "Lead Time", "Commit to production"],
                ["03", "MTTR", "Mean time to recover"],
                ["04", "Change Fail Rate", "Defects in production"],
            ],
        },
        {
            "type": "stat_cards",
            "title": "Q2 Numbers at a Glance",
            "stats": [
                ("42", "Deploys / day"),
                ("2.1h", "Lead time (median)"),
                ("18m", "MTTR (median)"),
                ("3.2%", "Change fail rate"),
            ],
        },
        {
            "type": "chart_bar",
            "title": "Deploy Frequency by Service",
            "data": [[48, 32, 24, 16, 8]],
            "labels": ["Auth", "API", "Frontend", "Workers", "Reports"],
            "series_names": ["Deploys / week"],
        },
        {
            "type": "vs_compare",
            "title": "Before vs After Platform Engineering",
            "left_title": "Before (2025)",
            "right_title": "After (2026)",
            "rows": [
                ("Deploys / day", "8", "42"),
                ("Lead time", "3.5 days", "2.1h"),
                ("MTTR", "2.4h", "18m"),
                ("On-call load", "High", "Low"),
            ],
        },
        {
            "type": "summary",
            "title": "What's Next",
            "content": [
                "Reduce lead time further (target: < 1h by Q4)",
                "Invest in self-service deployment tooling",
                "Expand on-call rotation fairness",
            ],
            "conclusion": "Roadmap finalized in next week's eng leadership sync",
        },
        {
            "type": "closing",
            "title": "Q&A",
            "message": "Let's discuss tradeoffs",
        },
    ],
}

# Write the outline (this is what your CMS / AI would produce)
with open(OUTLINE, "w", encoding="utf-8") as f:
    json.dump(outline, f, indent=2, ensure_ascii=False)
print(f"✓ Wrote outline: {OUTLINE}")

# Generate the PPTX using the same schema→API mapping as scripts/generate_ppt.py
eng = DeckEngine(theme_name=outline.get("theme", "business"), canvas=outline.get("canvas", "16:9"))

PAGE_HANDLERS = {
    "cover": lambda e, p: e.cover(title=p.get("title", ""), subtitle=p.get("subtitle", ""),
                                  author=p.get("author", ""), date=p.get("date", ""),
                                  image_path=p.get("image")),
    "closing": lambda e, p: e.closing(title=p.get("title", "Thank You"),
                                      message=p.get("message", ""),
                                      contact=p.get("contact", "")),
    "toc": lambda e, p: e.toc(items=p.get("items", [])),
    "section": lambda e, p: e.section_divider(section_title=p.get("title", ""),
                                               section_number=p.get("number"),
                                               subtitle=p.get("subtitle", "")),
    "content": lambda e, p: e.content(title=p.get("title", ""),
                                      bullets=p.get("content", p.get("bullets", [])),
                                      key_point=p.get("key_point", ""),
                                      image_path=p.get("image")),
    "stat_cards": lambda e, p: e.stat_cards(title=p.get("title", ""),
                                            stats=p.get("stats", [])),
    "chart_bar": lambda e, p: e.chart_bar(title=p.get("title", ""),
                                          data=p.get("data", [[]]),
                                          labels=p.get("labels", []),
                                          series_names=p.get("series_names")),
    "vs_compare": lambda e, p: e.vs_compare(title=p.get("title", ""),
                                            left_title=p.get("left_title", "A"),
                                            right_title=p.get("right_title", "B"),
                                            rows=p.get("rows", [])),
    "summary": lambda e, p: e.summary(title=p.get("title", ""),
                                      key_points=p.get("content", p.get("key_points", [])),
                                      conclusion=p.get("conclusion", "")),
}

for page in outline["pages"]:
    ptype = page.get("type", "content")
    handler = PAGE_HANDLERS.get(ptype)
    if handler is None:
        print(f"  ⚠ Unknown page type '{ptype}', skipping")
        continue
    handler(eng, page)

eng.save(OUTPUT)
print(f"✓ Generated: {OUTPUT}  ({eng._slide_count} slides)")
