---
name: bestseller-writer
description: Turn a shower idea into a full best-seller manuscript in one command. Multi-agent pipeline — Planner → Character Designer → Chapter Writers (parallel) → Editor → KDP Packager. Produces a complete book (50-80k words) ready to publish on Amazon KDP with title, description, keywords, categories, and cover brief. Works for fiction and non-fiction. Run with the standalone CLI script or let your agent orchestrate it step-by-step.
version: 1.0.0
license: MIT
author: felipe-lobo
tags: [book, writing, bestseller, KDP, amazon, self-publish, fiction, non-fiction, multi-agent, pipeline, passive-income]
category: Content Creation
---

# Bestseller Writer 📚

> **One idea → Full manuscript → Amazon KDP listing. Fully autonomous.**

Turn a shower thought into a publishable book. 5-stage multi-agent pipeline handles everything: story structure, characters, all chapters (written in parallel), editorial pass, and a complete Amazon KDP publishing package.

**No writing experience needed. No blank page. Just your idea.**

---

## What You Get

| Output | Description |
|--------|-------------|
| `MANUSCRIPT.md` | Complete book (50-80k words, 25-35 chapters) |
| `kdp_package.md` | Title options, Amazon description, 7 keywords, BISAC categories, pricing strategy, cover brief + Midjourney prompt |
| `plan.md` | Full story/argument structure with chapter-by-chapter outline |
| `characters.md` | Deep character profiles with arcs (fiction) or authority framework (non-fiction) |
| `editorial_memo.md` | Professional developmental edit notes |

---

## Quick Start (CLI)

### Install dependency
```bash
cd skills/bestseller-writer/scripts
npm install
```

### Generate a book
```bash
# Thriller
node generate.js --idea "A detective discovers evidence of her own murder" --genre thriller

# Self-help  
node generate.js --idea "How to build a $10k/month business in 90 days using AI" --genre self-help

# Romance
node generate.js --idea "Two rival food truck owners forced to share a festival spot" --genre romance

# Business/non-fiction
node generate.js --idea "Why most startups fail at hiring and how to fix it" --genre business
```

### Options
```
--idea, -i     Your book concept (required)
--genre, -g    Genre: thriller, romance, self-help, business, memoir, fantasy, nonfiction
--output, -o   Output directory (default: ./book-output/[slug])
--chapters     Number of chapters (default: 25)
--batch        Parallel chapter batch size (default: 4)
--planner      Model for Planner + Editor (default: claude-opus-4-5)
--writer       Model for writing agents (default: claude-sonnet-4-5)
```

### Environment
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

---

## Agent-Orchestrated Mode

If you're running inside an OpenClaw agent, the agent follows this pipeline directly using `sessions_spawn`. Trigger with:

> "Write me a book about [idea]" or "Generate a bestseller about [idea]"

The agent will:
1. Create output directory at `~/Desktop/books/[slug]/`
2. Run all 5 stages sequentially (chapters in parallel batches)
3. Deliver `kdp_package.md` as the final deliverable
4. Report word count and publish checklist

---

## Pipeline Architecture

```
💡 Your Idea
     │
     ▼
┌─────────────────────────────────────┐
│  Stage 1: PLANNER (Opus)            │
│  Market positioning, title options, │
│  full chapter-by-chapter outline,   │
│  comparable titles, pitch           │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│  Stage 2: CHARACTER DESIGNER        │
│  (Sonnet)                           │
│  Deep profiles, arcs, voice guide   │
│  (fiction) or authority/reader      │
│  avatar framework (non-fiction)     │
└──────────────────┬──────────────────┘
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
  ┌─────────────┐     ┌─────────────┐
  │ Chapters    │ ... │ Chapters    │  ← Parallel batches
  │ 1-4 (Sonnet)│     │ 21-25       │    (4 at a time)
  └──────┬──────┘     └──────┬──────┘
         └─────────┬─────────┘
                   ▼
┌─────────────────────────────────────┐
│  Stage 4: EDITOR (Opus)             │
│  Consistency, pacing, voice,        │
│  opening/ending assessment,         │
│  marketability score                │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│  Stage 5: KDP PACKAGER (Sonnet)     │
│  Title, description, keywords,      │
│  categories, pricing, cover brief,  │
│  Midjourney prompt, launch checklist│
└─────────────────────────────────────┘
                   │
                   ▼
        📦 MANUSCRIPT.md + kdp_package.md
```

---

## Genre Support

| Genre | Framework | Avg Length |
|-------|-----------|------------|
| Thriller/Mystery | Save the Cat beats + 3-act | 70-80k words |
| Romance | Meet cute → Black moment → HEA | 60-70k words |
| Fantasy/Sci-Fi | World + Hero's Journey | 80-100k words |
| Self-Help | Problem → Framework → Transformation | 40-50k words |
| Business | Insight → Evidence → Application | 45-55k words |
| Memoir | Chronological + thematic arc | 55-70k words |

---

## Revenue Model

**Amazon KDP passive income per book:**
- Average: $50-500/month
- Stack 10 books: $500-5,000/month
- Stack 30 books: $1,500-15,000/month

**Launch strategy (built into kdp_package.md):**
1. Publish at $0.99 → enroll KDP Select
2. Day 1-4: Paid launch, collect reviews
3. Day 5-9: Free promo (spikes ranking)
4. Day 10+: Raise to $2.99-$4.99 (70% royalty)
5. Repeat with next book

**Niche targeting (highest ROI):**
- Cozy mysteries with recurring characters (series = repeat buyers)
- Self-help for specific professions (accountants, nurses, teachers)
- Business books for specific industries
- Local history/interest books (low competition)

---

## Cost Estimate

| Stage | Model | API Cost (approx) |
|-------|-------|-------------------|
| Planner | Opus | ~$0.15 |
| Characters | Sonnet | ~$0.05 |
| 25 chapters | Sonnet × 25 | ~$0.75 |
| Editor | Opus | ~$0.20 |
| KDP Package | Sonnet | ~$0.05 |
| **Total** | | **~$1.20 per book** |

One book costs ~$1.20 to generate and can earn $50-500/month. ROI is infinite.

---

## Agent Instructions (for OpenClaw)

When the user asks to write a book or generate a manuscript:

### Step 1 — Collect Info
Ask for (or infer from context):
- The idea (required)
- Genre (infer if obvious, otherwise ask)
- Fiction or non-fiction

### Step 2 — Run Pipeline
Create output dir: `~/Desktop/books/[slug]/`

Spawn agents in sequence using `sessions_spawn` with `runtime="subagent"`:

**Agent 1 — Planner:**
Task: Full planning prompt (see scripts/generate.js `buildPlannerPrompt`)
Save output to: `plan.md`

**Agent 2 — Character Designer:**
Task: Character/authority prompt with plan as context
Save output to: `characters.md`

**Agents 3-N — Chapter Writers (parallel, max 4 at once):**
Task: Chapter writing prompt with plan + characters + prev chapter ending
Save output to: `chapter_NN.md`

**Agent N+1 — Editor:**
Task: Editorial pass prompt with plan + sample chapters
Save output to: `editorial_memo.md`

**Agent N+2 — KDP Packager:**
Task: KDP package prompt with plan + editorial
Save output to: `kdp_package.md`

### Step 3 — Assemble
Concatenate all `chapter_NN.md` files into `MANUSCRIPT.md`

### Step 4 — Deliver
Send user:
- Word count
- Path to MANUSCRIPT.md
- Key items from kdp_package.md (chosen title, pricing, first keyword string)
- Next steps for publishing

---

## Troubleshooting

**Chapters are too short?**
The writer agents are prompted for 2,000-2,500 words. If output is shorter, re-run that specific chapter with: "This chapter is too short. Expand to at least 2,000 words, adding more scene depth, dialogue, and sensory detail."

**Voice is inconsistent?**
The editor stage catches this. After the editorial memo, re-run any flagged chapters with the specific feedback.

**KDP keywords not relevant?**
Edit `kdp_package.md` keywords manually using Google Keyword Planner or Publisher Rocket to verify search volume before uploading.

**Want a series?**
After Book 1 is done, pass `plan.md` + `characters.md` into a new run with `--idea "Book 2: [continuation]"`. Characters and world are already built.
