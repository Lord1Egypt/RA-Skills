---
name: openclaw-geo-content-ops
description: Use when Ray asks to design, operate, audit, or improve OpenClaw GEO content operations beyond single-article writing: knowledge sources, topic clusters, content tasks, publish targets, llms.txt, schema, multi-site distribution, receipts, AI crawler visibility, or GEO analytics.
version: "0.1.0"
license: MIT
tags:
  - openclaw
  - geo
  - ai-search-visibility
  - content-ops
  - distribution
  - analytics
---

# OpenClaw GEO Content Ops

This skill turns GEO from "write more posts" into an operating system for trusted source material, content production, publication targets, LLM-friendly artifacts, receipts, and visibility analytics.

It is inspired by GEOFlow's content-engineering architecture, but it does not require adopting GEOFlow's Laravel CMS. Use it to extend the existing OpenClaw SEO/GEO workflow, not to replace `openclaw-seo-geo-workflow` or `ai-search-visibility-content-writing`.

## Use Boundaries

Use this skill for:

- GEO operating model design.
- Content asset inventory and source-of-truth planning.
- Topic cluster, keyword, FAQ, and question map organization.
- Daily/weekly content ops planning.
- Multi-site or multi-channel publication design.
- `llms.txt`, sitemap, TXT map, Schema, Open Graph, and AI-summary artifact planning.
- Receipt design for publish, crawl, citation, and analytics evidence.
- GEO dashboard/KPI design.
- Deciding what to borrow from GEOFlow.

Do not use this skill as the writing layer for a single article. Use `ai-search-visibility-content-writing` for that.

Do not claim live publish, indexing, ranking, crawler visits, or AI citations without receipts.

## Core Object Model

Use these nouns consistently:

| Object | Purpose | Example Artifact |
| --- | --- | --- |
| `knowledge_sources` | Trusted facts, docs, product pages, customer proof, FAQs, competitor notes | `catalogs/sources.jsonl`, source briefs, uploaded docs |
| `topic_clusters` | Search/AI questions grouped by intent and entity | keyword master, topic cluster markdown |
| `content_tasks` | Planned work units with owner, date, source, status, target query, and publish scope | daily manifest, task JSON |
| `draft_assets` | Generated article, metadata, schema, social/X derivative, images | `delivery/seo-geo/YYYY-MM-DD/` |
| `publication_targets` | Where content can go | ClawLite blog, WordPress, static GEO site, X, Feishu doc |
| `geo_artifacts` | LLM/search-readable outputs around content | `llms.txt`, sitemap, Schema, TXT map, FAQ blocks |
| `receipts` | Durable proof of state transitions | generation, audit, publish, deploy, live QA, patrol |
| `visibility_signals` | Evidence content is discoverable or useful | crawl logs, GA4, indexing, AI crawler, citation checks |

Canonical source catalog:

```text
clawlite-brain/catalogs/sources.jsonl
```

Relationship to ClawLite wiki:

- `knowledge_sources` is the evidence/source index. It points to raw docs, canonical files, receipts, URLs, and selected compiled wiki pages.
- `clawlite-brain/wiki/` is the durable compiled knowledge layer for project memory and retrieval.
- `synthadoc/wiki/` is a readable/generated wiki layer for brand, SEO, Hunter topics, and agent navigation.
- Prefer raw/canonical sources for factual claims; use wiki pages for fast orientation and retrieval.
- When daily findings become durable, promote them from receipts into `sources.jsonl` and then into topic/entity/synthesis wiki pages when warranted.

## Operating Loop

1. **Collect sources.** Confirm the facts are real, owned, current, and citeable.
2. **Build clusters.** Convert sources into user questions, entity maps, keywords, comparison angles, and FAQs.
3. **Create tasks.** For each task, define target reader, core query, primary answer, required sources, publish target, and success signal.
4. **Generate and audit.** Use the writing layer for drafts; require source grounding, direct answer, extractable structure, metadata, and schema hints.
5. **Publish by target.** Treat source publish, site deploy, social post, and remote distribution as separate state transitions.
6. **Emit GEO artifacts.** Keep `llms.txt`, sitemap, TXT map, Schema, Open Graph, and canonical data aligned with published content.
7. **Write receipts.** Store what happened, what was skipped, what failed, and which evidence supports the claim.
8. **Measure signals.** Monitor AI crawler hits, search index state, page views, citations, top content, failures, and stale content.
9. **Feed learning back.** Promote useful daily findings into `keywords-master.json`, topic clusters, source catalog, or rescue tasks.

## Required Task Brief

Every GEO content task should include:

```json
{
  "taskId": "geo-YYYY-MM-DD-slug",
  "status": "planned",
  "targetReader": "specific reader",
  "coreQuery": "question this page answers",
  "primaryAnswer": "short answer the page must give",
  "requiredSources": ["source-id-or-url"],
  "entities": ["OpenClaw", "ClawLite"],
  "topicCluster": "cluster-name",
  "publishScope": ["clawlite_blog"],
  "geoArtifacts": ["schema", "sitemap", "llms_txt"],
  "successSignals": ["live_url", "index_check", "ai_crawler_log"]
}
```

If any field is missing, make the smallest honest assumption and mark it in the receipt. Do not silently invent sources.

## Publication Target Rules

- `clawlite_blog`: requires source apply/build evidence and, for production claims, deploy plus live QA.
- `wordpress_rest`: requires remote ID/URL, media sync result, and API response receipt.
- `static_geo_site`: requires generated HTML/Markdown, sitemap/TXT map update, and reachable URL check.
- `x_post`: requires a derivative artifact tied to the article's narrative spine; do not treat social posting as blog publication.
- `feishu_doc`: useful for internal review; not a public GEO signal unless explicitly published externally.

Remote distribution failure must not rewrite history. Mark the target as `FAILED` or `NEEDS_RETRY`; keep local publish status separate.

## GEO Artifact Checklist

For public web targets, check whether each published page or batch has:

- canonical URL and stable slug
- title and meta description
- Open Graph/Twitter metadata where relevant
- Article/FAQ/HowTo/Organization schema where appropriate
- sitemap inclusion
- `llms.txt` or site-level AI-readable map inclusion
- TXT map or Markdown index for important content hubs
- internal links to and from related cluster pages
- source/evidence block where claims need grounding
- clear update timestamp for evergreen pages

## Receipts

Recommended receipt shape:

```json
{
  "date": "YYYY-MM-DD",
  "taskId": "geo-YYYY-MM-DD-slug",
  "stage": "publish|artifact|patrol|analytics",
  "target": "clawlite_blog",
  "status": "PASS|FAIL|SKIPPED|NEEDS_DATA|PASS_WITH_WARNINGS",
  "evidence": {
    "localPath": "path/to/file",
    "liveUrl": "https://example.com/page",
    "deployId": "optional",
    "checkedAt": "ISO timestamp"
  },
  "warnings": [],
  "nextActions": []
}
```

Status vocabulary must match `openclaw-seo-geo-workflow` where possible.

## Analytics Questions

When designing or auditing GEO analytics, answer:

- What was created, audited, published, deployed, skipped, or failed?
- Which sources and clusters produced publishable work?
- Which targets received the content?
- Which pages are included in sitemap/`llms.txt`/TXT maps?
- Which content received crawler traffic or AI crawler hits?
- Which pages need refresh, consolidation, internal links, or rescue?
- Which daily findings should be promoted into durable source/keyword/topic files?

## When Borrowing From GEOFlow

Borrow patterns, not the whole stack:

- structured source library before generation
- task queue state machine
- local publish separate from remote distribution
- target-site Agent / WordPress provider abstraction
- `llms.txt`, sitemap, TXT map, Schema output
- access-log and AI-crawler analytics

Read `references/geoflow-patterns.md` when designing implementation details or mapping this to code.
