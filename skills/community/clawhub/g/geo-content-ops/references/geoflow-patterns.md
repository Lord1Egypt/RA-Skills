# GEOFlow Patterns For OpenClaw

Use this reference when translating GEOFlow's architecture into OpenClaw without adopting GEOFlow as a CMS.

## What To Borrow

### 1. Content Engineering Pipeline

GEOFlow's useful pipeline:

```text
knowledge base / materials / prompts
  -> task configuration
  -> queue generation
  -> draft / review / publish
  -> distribution queue
  -> target site artifacts
  -> analytics
```

OpenClaw mapping:

```text
catalogs/sources + topic clusters
  -> Hunter/Tony/factory task manifest
  -> draft + audit receipts
  -> Peter source apply / deploy
  -> target-specific distribution receipts
  -> patrol + visibility analytics
```

### 2. Knowledge Source First

Do not start from keyword volume alone. Require source material that can support a useful answer.

Minimum source fields:

```json
{
  "id": "source-stable-id",
  "type": "product_doc|case_study|faq|competitor|customer_note|web_url",
  "title": "Human readable title",
  "url": "optional URL",
  "owner": "optional owner",
  "capturedAt": "ISO timestamp",
  "trustLevel": "owned|verified|third_party|unverified",
  "summary": "What this source proves",
  "entities": ["OpenClaw"],
  "usableFor": ["cluster-name"]
}
```

### 3. Task State Machine

Keep local generation and public distribution separate:

```text
planned
  -> sourced
  -> drafted
  -> audited
  -> source_published
  -> built
  -> deployed
  -> live_checked
  -> monitored
```

Target-level states:

```text
queued -> sending -> synced
queued -> sending -> failed -> retry_scheduled
skipped
```

This prevents one failed remote target from making the whole article look unpublished.

### 4. Publication Provider Abstraction

Each target should implement the same conceptual interface:

```text
health()
publishArticle(payload)
updateArticle(payload)
deleteOrUnpublish(payload)
syncAssets(payload)
return remoteId, remoteUrl, status, logs
```

Start with:

- `clawlite_blog`
- `wordpress_rest`
- `static_geo_site`
- `x_post`
- `feishu_doc`

Do not mix provider-specific credentials or response bodies into generic task records. Store them under provider metadata and redact secrets in logs.

### 5. GEO Artifact Layer

For each public web target, maintain a target artifact record:

```json
{
  "target": "clawlite_blog",
  "liveUrl": "https://clawlite.ai/blog/slug",
  "canonical": "https://clawlite.ai/blog/slug",
  "sitemapIncluded": true,
  "llmsTxtIncluded": true,
  "txtMapIncluded": true,
  "schemaTypes": ["Article", "FAQPage"],
  "openGraph": true,
  "lastVerifiedAt": "ISO timestamp"
}
```

### 6. Analytics Model

Separate production analytics from visibility analytics:

Production:

- created tasks
- completed drafts
- failed audits
- publish queue count
- deployed pages
- failed targets

Visibility:

- indexed pages
- sitemap/`llms.txt` coverage
- AI crawler hits
- search impressions/clicks when available
- AI citation checks
- top pages by views or mentions
- stale pages and missing internal links

### 7. Daily To Weekly Promotion

Daily findings should land in receipts first. Promote only validated patterns to durable assets:

- daily keyword candidate -> `keywords-master.json`
- recurring question -> `topic-clusters.md`
- verified source -> `catalogs/sources.jsonl`
- failed page -> rescue task
- strong article -> social/X derivative and internal link expansion

## What Not To Borrow

- Full Laravel/PHP CMS unless OpenClaw intentionally wants a second content backend.
- Admin UI assumptions that duplicate existing OpenClaw dashboard work.
- Blind batch generation without source grounding.
- A single "published" boolean for multi-target content.
- SEO/GEO claims without evidence receipts.
