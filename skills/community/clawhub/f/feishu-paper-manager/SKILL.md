---
name: feishu-openclaw-paper-manager
description: Design or implement a paper-management workflow built on a Feishu bot plus OpenClaw. Use when the user wants to ingest papers from Feishu messages, save PDFs or source links into a Feishu cloud-docs paper folder, maintain a searchable multi-dimensional table of paper metadata and reusable tags, or evolve the tag taxonomy after every 50 newly added papers.
---

# Feishu OpenClaw Paper Manager

Use this skill when the task is to design, review, or implement a paper-management agent that runs through a Feishu bot and OpenClaw.

## Primary objective

Build a workflow with three durable outputs:

1. A cloud-docs `paper` folder that stores the paper asset or an index document for the source link.
2. A Feishu multi-dimensional table that stores normalized paper metadata.
3. A taxonomy iteration loop that improves labels whenever total paper count crosses `50`, `100`, `150`, and so on.

## Workflow

Follow this sequence:

1. Map the ingestion sources from Feishu messages.
2. Normalize each paper into one canonical record.
3. Save or register the paper in the cloud-docs `paper` folder.
4. Generate summary and reusable multi-label tags.
5. Write the record into the multi-dimensional table.
6. Check whether the total record count has reached a multiple of 50.
7. If yes, run taxonomy refinement and backfill historical rows.

## Ingestion rules

Treat these as valid paper inputs:

- PDF attachment in a Feishu message
- arXiv, OpenReview, ACL Anthology, publisher, or project links in a message
- Mixed messages that contain both a PDF and a source link

For every incoming item:

1. Extract the raw message URL, sender, timestamp, and all detected paper candidates.
2. Resolve whether the message refers to a new paper or an existing one.
3. Create exactly one canonical paper record per paper.

Deduplication priority:

1. DOI
2. arXiv ID or OpenReview forum ID
3. normalized title
4. source URL fingerprint

If a duplicate exists, update missing fields instead of creating a new row.

## Storage model

Always separate binary storage from metadata storage:

- The cloud-docs `paper` folder is for the PDF file or a small link-index doc when the PDF is unavailable.
- The multi-dimensional table is the system of record for metadata, classification, and retrieval.

When a PDF is available:
- upload the PDF into the `paper` folder
- use a deterministic filename from `year + first_author + short_title`

When only a link is available:
- create a lightweight cloud doc in the `paper` folder containing the title, source link, access date, and capture notes
- still create the metadata row in the table

## Required table fields

Create or expect these fields in the Feishu multi-dimensional table:

- `paper_id`: stable unique ID
- `title`: paper title
- `doc_link`: cloud-docs link to the stored PDF or link-index doc
- `source_link`: original paper URL
- `source_type`: `pdf`, `arxiv`, `openreview`, `publisher`, `project`, `other`
- `summary_one_line`: one-sentence summary in plain language
- `tags_topic`: reusable topical tags
- `tags_method`: reusable method tags
- `tags_task`: reusable task tags
- `tags_domain`: reusable domain tags
- `tags_stage`: reusable maturity tags such as `reading`, `worth-reproducing`, `survey-only`
- `authors`: normalized author string
- `venue`: venue or source
- `year`: publication year
- `status`: `new`, `classified`, `taxonomy-reviewed`, `duplicate`, `error`
- `message_link`: original Feishu message link
- `ingested_at`: ingestion timestamp
- `taxonomy_version`: taxonomy version used for the row

Use multi-select fields for all `tags_*` columns so users can filter and search by labels directly in Feishu.

## Tagging policy

A paper can have multiple tags, but tags must stay reusable. Do not create a new free-form label when an existing reusable label is close enough.

Use a layered taxonomy:

- `tags_topic`: broad themes such as `llm`, `multimodal`, `agent`, `retrieval`, `alignment`, `reasoning`
- `tags_method`: technical mechanisms such as `rag`, `rl`, `distillation`, `synthetic-data`, `moe`, `benchmark`
- `tags_task`: applied tasks such as `code-gen`, `translation`, `information-extraction`, `math`, `search`
- `tags_domain`: business or science domain such as `biology`, `finance`, `education`, `robotics`
- `tags_stage`: actionability and curation state

Keep tags short, lowercase, and singular where possible.

Prefer this decision rule:

1. reuse an existing tag if it is at least 80 percent semantically correct
2. add a synonym mapping instead of a brand-new visible tag when possible
3. only introduce a new visible tag if it will likely apply to at least 5 papers in the next 100 rows

See `references/tag-taxonomy.md` for the starter taxonomy and merge rules.

## One-line summary policy

The `summary_one_line` field must answer:

- what the paper does
- what makes it different
- in language that a technically literate teammate can scan in under 10 seconds

Avoid hype, citation-style phrasing, and long clauses.

## Taxonomy iteration loop

Whenever the table row count reaches a multiple of 50, run a taxonomy review pass.

The review pass must:

1. export or inspect all existing tags and their frequencies
2. identify sparse tags, duplicates, synonyms, and overloaded tags
3. propose a new taxonomy version that improves reuse and filtering quality
4. map old tags to new tags
5. backfill historical rows
6. mark affected rows with the new `taxonomy_version`
7. produce a short change log explaining merges, splits, and renamed tags

Optimization goals:

- fewer near-duplicate tags
- better coverage of high-volume themes
- stable filters across time
- minimal churn for already-good tags

Do not relabel everything from scratch unless the old taxonomy is clearly broken. Prefer merge-and-backfill over wholesale replacement.

## Output contract

When asked to design the system, return:

1. end-to-end workflow
2. Feishu table schema
3. tagging strategy
4. taxonomy iteration logic
5. implementation notes for Feishu bot and OpenClaw boundaries

When asked to implement or review code, anchor decisions to:

- ingestion reliability
- deduplication correctness
- idempotent writes
- table filterability
- taxonomy evolution safety

## Boundary between Feishu bot and OpenClaw

Default division of responsibility:

- Feishu bot: receive messages, fetch attachments or links, send confirmations, surface errors
- OpenClaw: parse payloads, deduplicate, summarize, classify, write docs and table rows, trigger taxonomy reviews

If the user has an existing architecture, preserve it and only adapt the workflow.

## Development contract

When the user wants implementation guidance, assume this integration shape unless the project already defines another one:

1. Feishu bot receives the event and verifies the request.
2. Feishu bot converts the raw event into a normalized ingestion payload.
3. Feishu bot calls an OpenClaw workflow entrypoint with that payload.
4. OpenClaw performs enrichment, storage, classification, and table updates.
5. OpenClaw returns a structured result for user-visible confirmation.
6. Feishu bot posts a success, duplicate, or failure message back to the conversation.

Design the integration around these engineering constraints:

- idempotent processing for webhook retries
- explicit deduplication before any write
- append-safe and patch-safe updates to the table
- stable identifiers for files, rows, and taxonomy versions
- clear status reporting back to the chat thread

Use `references/api-contracts.md` for payload shapes and responsibility boundaries.
Use `references/event-flows.md` for event sequences and retry behavior.

## Feishu-side implementation expectations

On the Feishu side, prefer these components:

- webhook endpoint for message events
- message parser for attachments and URLs
- file fetcher for PDF downloads
- Feishu document client for folder upload or doc creation
- Feishu table client for row create and row update
- reply formatter for confirmations and error notices

The Feishu bot should emit one normalized payload per detected paper candidate, not one per message if a message contains multiple papers.

Before calling OpenClaw, the Feishu side should:

1. verify event authenticity
2. extract message metadata
3. collect attachment metadata and URLs
4. collect raw hyperlinks in the message body
5. attach a stable `event_id` and `message_id`
6. include enough source metadata for later retries without rereading the original message when possible

## OpenClaw-side implementation expectations

On the OpenClaw side, prefer these stages:

1. ingest payload validation
2. paper candidate normalization
3. metadata enrichment from PDF or source page
4. duplicate lookup
5. cloud-docs write
6. one-line summary generation
7. multi-dimensional tagging
8. table upsert
9. taxonomy-threshold check
10. taxonomy review workflow when threshold is hit

OpenClaw should treat the table as an upsert target, not append-only storage.

For duplicates:

- keep the canonical row
- patch missing metadata
- optionally append the new `message_link` to notes or an audit field if the implementation supports it
- return a `duplicate` result instead of creating a new paper row

## Taxonomy review trigger contract

The threshold is based on canonical non-duplicate paper rows, not raw messages.

Trigger a taxonomy review only when:

- the current canonical row count is divisible by `50`
- the taxonomy review for that exact threshold has not already run

Persist a review checkpoint such as `last_review_count = 100` or `taxonomy_version = v3` so retries do not rerun the same migration.

## Output expectations for implementation tasks

When implementing code, prefer returning these artifacts:

1. module boundaries
2. payload schemas
3. idempotency rules
4. event sequence
5. failure handling and retry rules
6. sample success and duplicate responses

When reviewing code, check specifically for:

- webhook retry safety
- duplicate PDF uploads
- row duplication from concurrent events
- inconsistent tag writes across dimensions
- taxonomy backfill that can partially fail without rollback

## Failure policy

The default failure strategy is:

- fail fast on invalid payloads
- retry transient network or API errors
- do not retry deterministic classification errors forever
- never create a table row before deduplication completes
- never advance taxonomy version markers before backfill succeeds

If partial writes are possible, require compensating logic or a resumable reconciliation job.

## Resources

- Table schema and record lifecycle: `references/table-schema.md`
- Tag starter set and refinement rules: `references/tag-taxonomy.md`
- Feishu/OpenClaw payload and boundary contracts: `references/api-contracts.md`
- Event sequences, retries, and examples: `references/event-flows.md`
