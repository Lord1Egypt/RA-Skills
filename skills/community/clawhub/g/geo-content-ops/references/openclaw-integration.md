# OpenClaw Integration

This reference explains how `openclaw-geo-content-ops` coordinates existing OpenClaw SEO/GEO assets.

## Skill Boundaries

| Skill | Use it for | Hand off when |
| --- | --- | --- |
| `openclaw-geo-content-ops` | Source catalog, content tasks, publish targets, GEO artifacts, receipts, analytics | A single article needs drafting or today's publish status needs deterministic receipt inspection |
| `openclaw-seo-geo-workflow` | Hunter/Tony/Peter daily workflow, blog factory status, publish/build/live QA, patrol | Durable source catalog or weekly content ops planning is needed |
| `ai-search-visibility-content-writing` | Article or landing page writing/rewrite, answer-first structure, citeable sections, schema hints | The task is source ingestion, distribution, live QA, or analytics |
| `claw-wiki` | Regenerating readable ClawLite wiki pages from canonical source files | Raw sources or receipts need registration first |

## Recommended Local Paths

These paths are workspace conventions, not public repo requirements:

```text
clawlite-brain/catalogs/sources.jsonl
clawlite-brain/wiki/
synthadoc/wiki/
references/clawlite-brand/
references/clawlite-seo/
mission-control/data/
delivery/seo-geo/YYYY-MM-DD/
```

## Daily Loop

1. Read yesterday and today receipts before claiming state.
2. Register valuable new evidence in `clawlite-brain/catalogs/sources.jsonl`.
3. Create or update content tasks with source IDs.
4. Use the writing skill for each article body.
5. Use the SEO/GEO workflow for publish and live QA.
6. Add GEO artifact checks to receipts.
7. Promote durable learning into topic clusters or wiki pages.

## Weekly Loop

1. Review source catalog quality.
2. Consolidate repeated questions into topic clusters.
3. Refresh wiki pages.
4. Inspect visibility analytics.
5. Create rescue tasks for failed or stale pages.
