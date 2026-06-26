# GEO-First SEO

**Platforms:** Claude · Openclaw · Codex
**Domain:** SEO

## Purpose

A Generative Engine Optimization (GEO) workflow. It makes content more likely to be **cited and
surfaced by AI answer engines** — ChatGPT, Perplexity, Google AI Overviews, Gemini, and Copilot —
rather than chasing the traditional SEO goal of ranking high for clicks. Traditional SEO optimizes
to *rank and be clicked*; GEO optimizes to *be quoted* inside a synthesized answer.

It runs end-to-end: GEO strategy and query research, creating new content or auditing and rewriting
an existing page, technical markup, and a final scorecard — covering both the **content layer** and
the **technical layer**.

## When to Use

- When you want a topic or page to get cited by ChatGPT, Perplexity, or Google AI Overviews
- When you have an existing article or URL and want it audited and rewritten for AI search
- When you need the technical markup (schema.org JSON-LD, `llms.txt`, FAQ structure) for AI crawlers
- When you want to know which user questions your content should win citations for, and whether it does

It is **not** for traditional keyword-ranking audits, paid ads, or link-building campaigns.

## What It Does

**Phase 1: Strategy & Intake**
1. Captures topic/page, audience, target engines, and the query cluster the content should win
2. Runs citation-gap research (when web access is available) and produces a short content brief

**Phase 2: Create or Audit**
3. Drafts new content, or diagnoses and rewrites existing content
4. Applies seven GEO content principles (answer-first, self-contained chunks, entity coverage,
   citable elements, scannable structure, authority/freshness signals, plain language)

**Phase 3: Technical GEO**
5. Generates schema.org JSON-LD, `llms.txt`, and semantic FAQ/heading markup as paste-ready blocks

**Phase 4: GEO Scorecard & Iterate**
6. Scores against a seven-criterion rubric and revises weak items

## Notes

This skill is self-contained; the main workflow in `SKILL.md` runs without opening the reference
files. `references/geo-content-tactics.md` holds before/after rewrites and per-engine notes;
`references/technical-geo.md` holds JSON-LD snippets, an `llms.txt` template, and a markup checklist.

The skill never fabricates statistics, quotes, sources, or dates; it marks anything it cannot verify
with `[verify]`. Web access is optional and read-only, and the skill never publishes content on your
behalf.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/open-skill-hub/issues) — improvements are welcome.
