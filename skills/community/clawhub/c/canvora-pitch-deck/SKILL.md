---
name: pitch-deck
version: 1.0.0
description: Build presentation decks with Canvora — pitch decks, sales decks, training and webinar slides, or a whole PDF/DOCX report turned into slides. Use when the user wants a presentation, deck, slide set, investor pitch, sales enablement slides, or asks to turn a document into slides.
homepage: https://canvora.ai/for-agents
metadata: {"openclaw":{"emoji":"📊","requires":{"bins":["canvora"],"env":["CANVORA_API_KEY"]}}}
---

# Decks and presentations

Deck formats run through Canvora's **structured slide pipeline**: one planning
pass builds the narrative arc and a shared design system, then every slide is
rendered against it. That is why a deck holds together where N separate images
would not. Your job is the narrative input and the format choice — the pipeline
does the rest. Setup and credits: see the `canvora` skill.

## Pick the format by audience, not by shape

| Format | Size | Use for |
|---|---|---|
| `pitch_deck` | 16:9 | investors, fundraising, "the story of the company" |
| `sales_deck` | 16:9 | prospects, product value, objection handling |
| `presentation_slide` | 16:9 1920×1080 | the general default — talks, internal, conference |
| `training_slide` | 16:9 | teaching, onboarding, step-by-step instruction |
| `webinar_slide` | 16:9 | live sessions, screen-share readability |
| `presentation_4x3` | 4:3 1024×768 | only when the user's projector/template demands it |

All six are carousel formats: **15 credits per slide**. A 10-slide deck = 150.
State the cost in the same message as the run — announce it, don't ask
permission. When *you* chose the slide count (the defaults below) rather than
the user, confirm that number with them; when they said "10 slides", just run it.

Every deck is 3+ outputs, so fire-and-poll instead of `--wait`: most harnesses
kill a shell command at 120s while the deck carries on rendering server-side.
Never re-run `generate` after a timeout — that starts a second, separate job.
Poll `status`. See the `canvora` skill's "Long runs" section.

## Intake — three questions, maximum

1. **What's the source?** A document (`--file-url`), a link (`--url`), written
   content (`--input`), or just the pitch in their head (`--idea`)?
2. **How many slides?** If they don't know, use the audience: pitch 10,
   sales 8, training as many as there are steps, general 8. Cap is 10 per call.
3. **Whose brand?** `canvora brands --json` → `--brand` (+ `--logo` — decks are
   the one place a logo on every slide is expected).

If they gave you a document, do NOT read it and paraphrase it into `--idea`.
Pass the file directly — extraction is part of the pipeline and keeps the
numbers, names and structure intact.

## The canonical runs

```bash
# Document → deck (the highest-value flow: report, memo, whitepaper, spec)
ID=$(canvora generate --file-url https://example.com/q3-report.pdf \
  --format presentation_slide --slides presentation_slide=8 \
  --brand $BRAND --logo | head -1)
canvora status "$ID" --json    # repeat every ~30s until completed

# Investor pitch from a description
ID=$(canvora generate --idea "Seed pitch for a B2B logistics SaaS: problem, market size, product, traction, team, ask" \
  --format pitch_deck --slides pitch_deck=10 \
  --brand $BRAND --logo --style corporate --cta | head -1)
canvora status "$ID" --json

# Sales deck from the product page
ID=$(canvora generate --url https://example.com/product \
  --format sales_deck --slides sales_deck=8 --brand $BRAND --logo --cta | head -1)
canvora status "$ID" --json

# Training slides from content the user wrote
ID=$(canvora generate --input "$COURSE_OUTLINE" \
  --format training_slide --slides training_slide=10 | head -1)
canvora status "$ID" --json
```

## Narrative shaping (this is where a deck is won)

- **Name the arc in the brief when it's a pitch.** "problem, market, product,
  traction, team, ask" beats "a pitch deck for my startup" — the planner maps
  each beat to a slide.
- **One claim per slide.** If the source has 20 points and they asked for 8
  slides, say which 8 matter; otherwise the planner compresses for you.
- **`--cta` for anything persuasive.** Pitch and sales decks should close on an
  ask. Training decks usually shouldn't.
- **`--style`:** investors/enterprise → `corporate` or `minimal`; product
  launches → `bold`; premium/brand-led → `elegant`. Omitting pins `modern`.
- **Don't art-direct slide by slide.** But if the user has a stated look or an
  existing template aesthetic, pass it as one line.

## Delivering a deck

1. **Sort by `sortOrder`.** A deck out of order is worthless.
2. **Export to PPTX or PDF** — this is the step users actually want, and it is
   an **MCP-only** capability today: `export_visuals(generation_id, format:
   "pptx" | "pdf")`. On the CLI, `canvora download <id> --dir ./deck` gets the
   images and the user exports from the Canvora dashboard. Tell them that
   plainly instead of pretending the CLI can do it.
3. **Fix a single slide with `edit`** (3 credits, design preserved) — never
   regenerate the deck because slide 4 has a typo.

## Quality checklist

- [ ] Source passed directly (file/URL), not paraphrased
- [ ] Slide count matches the narrative beats
- [ ] Brand kit + `--logo` applied when a kit exists
- [ ] `--cta` on pitch/sales, off on training
- [ ] Cost stated up front (15 × slides)
- [ ] Outputs sorted by `sortOrder`; export path explained
