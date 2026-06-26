# Table Schema

Use this reference when designing the Feishu multi-dimensional table or mapping code fields to table columns.

## Core record

Each row represents one canonical paper.

Recommended columns:

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `paper_id` | text | yes | Stable ID such as `paper_2026_000123` or hash-based ID |
| `title` | text | yes | Canonical title after normalization |
| `doc_link` | url | yes | Feishu cloud-docs link to PDF or link-index doc |
| `source_link` | url | yes | Original source URL |
| `source_type` | single select | yes | `pdf`, `arxiv`, `openreview`, `publisher`, `project`, `other` |
| `summary_one_line` | text | yes | One-sentence summary |
| `tags_topic` | multi-select | yes | Broad themes |
| `tags_method` | multi-select | no | Methods or mechanisms |
| `tags_task` | multi-select | no | Tasks or benchmarks |
| `tags_domain` | multi-select | no | Domain or industry |
| `tags_stage` | multi-select | yes | Reading and curation status |
| `authors` | text | no | Prefer `First Author et al.` if long |
| `venue` | text | no | Venue, archive, or publisher |
| `year` | number | no | Publication year |
| `message_link` | url | yes | Feishu message permalink |
| `ingested_at` | datetime | yes | First ingest time |
| `updated_at` | datetime | yes | Last metadata update |
| `taxonomy_version` | text | yes | Example: `v1`, `v2` |
| `status` | single select | yes | `new`, `classified`, `taxonomy-reviewed`, `duplicate`, `error` |

## Optional operational columns

Add these only if the workflow needs them:

| Field | Type | Notes |
| --- | --- | --- |
| `doi` | text | Useful for exact deduplication |
| `external_id` | text | arXiv ID, OpenReview ID, ACL Anthology ID |
| `language` | single select | For multilingual corpora |
| `reviewer_notes` | text | Human notes outside the one-line summary |
| `ingest_channel` | single select | Which Feishu group or bot route produced the paper |
| `attachment_hash` | text | Prevent duplicate PDF uploads |

## Record lifecycle

Suggested row states:

1. `new`: source captured, summary/tags not finalized
2. `classified`: summary and tags completed
3. `taxonomy-reviewed`: row updated by a taxonomy refresh
4. `duplicate`: merged into another canonical row
5. `error`: ingest failed and needs retry

## Retrieval design

The table should support these common filters without extra processing:

- by topic, method, task, domain, or stage
- by year or venue
- by source type
- by ingestion time
- by taxonomy version

This is why the tag dimensions are split instead of using one giant tag column.
