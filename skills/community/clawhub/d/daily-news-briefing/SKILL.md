---
name: daily-news-briefing
description: Produce polished, production-ready daily news briefings, morning reports, market snapshots, executive digests, and founder updates with verified sourcing, clear prioritization, and premium formatting. Use when Codex is asked to create a daily briefing, daily report, morning newsletter, CEO digest, investor update, industry roundup, trend snapshot, or any recurring news summary that must be commercially usable, aesthetically refined, current, and trustworthy.
---

# Daily News Briefing

Produce a briefing that feels editorially serious, commercially publishable, and immediately useful to decision-makers. Default to a premium operator mindset: concise, beautiful, verified, and opinionated about what matters.

## Overview

Use this skill to turn current developments into a polished daily briefing, morning newsletter, executive digest, investor memo, or market snapshot. It is optimized for high-trust outputs with clear sourcing, premium formatting, and strong editorial judgment.

## Quick Start

Use the skill when a user asks for any of these:

- "Make me a polished AI daily brief for founders."
- "Write a premium morning newsletter covering the top startup stories."
- "Create an executive digest of today's crypto and macro moves."
- "Summarize the most important market developments and explain why they matter."

## Workflow

1. Confirm the briefing frame.
   Capture or infer:
   - exact date and timezone
   - audience: founder, CEO, investment team, operators, consumers
   - coverage scope: general news, AI, crypto, finance, startup, company-specific, regional
   - format: quick digest, executive memo, newsletter, Markdown, HTML
   - tone: authoritative, energetic, analytical, calm

2. Gather current information.
   News is time-sensitive, so verify with web browsing whenever the report depends on latest developments. Use exact calendar dates in the output and avoid ambiguous phrases such as "today" unless paired with the full date.

3. Filter aggressively.
   Keep only items that pass all of these checks:
   - materially new within the requested window
   - relevant to the chosen audience
   - supported by reliable primary or strong secondary sources
   - distinct from other selected items
   Drop low-signal stories, speculative filler, and duplicate angles.

4. Build the editorial hierarchy.
   Organize the report in decreasing decision value:
   - lead story or top line
   - key developments
   - implications and why it matters
   - watchlist and next signals

5. Render with polish.
   Use strong headings, clean spacing, compact summaries, and restrained emphasis. The report should read like a premium product, not a raw notes dump.

6. Run a final quality gate.
   Check the report against the scorecard in [editorial-standards.md](references/editorial-standards.md). If the piece is bloated, repetitive, weakly sourced, or visually flat, revise before delivering.

## Example Requests

- Create a China AI daily briefing for operators with 5 top stories and a short watchlist.
- Draft a US market-open note for investors using exact dates and inline source links.
- Produce a clean Markdown founder digest focused on fundraising, product launches, and policy shifts.
- Generate an HTML morning newsletter shell for a premium subscriber product.

## Default Output Shape

Unless the user specifies another structure, produce the briefing in this order:

1. Masthead
   Include title, exact date, audience, and scope.

2. Executive Summary
   Write 3 to 5 bullets that surface the highest-value developments first.

3. Top Stories
   For each item include:
   - a sharp headline
   - a 2 to 4 sentence summary
   - "Why it matters" in 1 sentence
   - source links

4. Signals and Watchlist
   Include emerging items that are not yet large enough for the main section but deserve monitoring.

5. Closing Take
   End with a short synthesis, forecast, or operator takeaway.

## Formatting Rules

- Prefer Markdown unless the user asks for HTML or another format.
- Keep paragraphs short. Dense walls of text lower perceived quality.
- Use one visual system consistently: neutral luxury, newsroom, or modern tech publication.
- Bold only the most important nouns, numbers, or takeaways.
- Never paste long source excerpts. Summarize and cite.
- Make links easy to scan and attach them directly to the related item.
- If the user wants a branded artifact, use the templates in [assets/briefing-template.md](assets/briefing-template.md) or [assets/briefing-template.html](assets/briefing-template.html) as the starting point.

## Audience Presets

- Founder / CEO:
  prioritize market shifts, regulation, competitors, fundraising, distribution, major product launches, and second-order implications.
- Investors:
  prioritize capital markets, multiples, M&A, policy, macro, category velocity, and company-specific catalysts.
- Operators:
  prioritize product launches, go-to-market moves, platform changes, pricing, partnerships, and execution signals.
- Public audience:
  reduce jargon, explain context, and optimize for readability over insider shorthand.

For a highly specific audience, read [output-blueprints.md](references/output-blueprints.md) and adapt the structure before drafting.

## Sourcing Rules

- Prefer primary sources first: company blogs, filings, official statements, product docs, regulator updates, earnings materials.
- Use strong reporting from credible outlets when primary sources are unavailable or incomplete.
- If a claim appears unstable, contested, or breaking, say so directly.
- Cite every major story.
- Avoid unsupported synthesis. If making an inference, label it clearly as an inference.

## Production Quality Bar

Deliver only when the piece is:
- current
- correctly dated
- visually clean
- non-redundant
- insight-dense
- source-linked
- tailored to the requested audience

If the user asks for a recurring or operational workflow, generate a reusable scaffold first with:

```bash
python3 scripts/render_briefing_package.py \
  --title "AI Daily Brief" \
  --date "2026-03-18" \
  --audience "Founders and investors" \
  --scope "AI and startup ecosystem" \
  --tone "authoritative" \
  --format markdown \
  --output /tmp/ai-daily-brief
```

This creates a clean package with a ready-to-fill Markdown or HTML draft plus a JSON manifest.

## Security Notes

- The bundled script only renders local templates into an output folder.
- Do not ask the user to run remote shell commands or download opaque installers.
- Keep source links visible and near each story so the user can verify claims quickly.
- Prefer local template rendering plus verified web research over hidden automation.

## Resources

- Read [editorial-standards.md](references/editorial-standards.md) when you need the quality rubric, failure modes, and source-ranking rules.
- Read [output-blueprints.md](references/output-blueprints.md) when the user wants a specific briefing style such as executive memo, investor brief, polished newsletter, or market open note.
- Use [scripts/render_briefing_package.py](scripts/render_briefing_package.py) to generate a production-ready skeleton instead of hand-writing repetitive structure.
