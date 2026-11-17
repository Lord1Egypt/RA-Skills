---
title: Wiki schema
description: How this wiki is organized and how agents and people add to it. Read before substantial work.
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: procedure
tags: [wiki]
---

# Wiki schema

## Domain

<One paragraph: what this wiki holds and for whom.>

This wiki stores curated, durable knowledge. It is not a transcript store and not the system
of record for live data: for anything that can change, it says what was true when written and
where to check.

Owner: <person or role who gets review digests and escalations>
Decisions are made by: <people whose word makes something a decision; agents propose>

## Layout

- `concepts/`: ideas, methods, terms
- `entities/`: organizations, products, systems
- `people/`: people, with what they own and how to reach them
- `decisions/`: what was decided, when, by whom and why
- `procedures/`: how to do something that will be done again
- `queries/`: substantial answers worth keeping
- `raw/`: source material, immutable after ingestion
- `_archive/`: superseded pages, kept for history

File names are lowercase words separated by hyphens.

## Frontmatter

Every page except raw sources:

```yaml
---
title: Page Title
description: One line on what the page answers or holds.
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | procedure | decision | query | summary
tags: [approved-tag]
sources: [raw/articles/source-name.md, https://example.com/page]
confidence: high | medium | low      # optional; use for fast-moving or single-source pages
contested: false                     # optional; true while a conflict is unresolved
stale_after: YYYY-MM-DD              # optional; recheck on or after this date
verified: YYYY-MM-DD                 # optional; last date the claims were checked against sources
---
```

Raw sources:

```yaml
---
source_url: https://example.com/source
ingested: YYYY-MM-DD
sha256: <hex digest of the body after the closing --->
---
```

## Tags

Add a tag here before using it on a page.

- Kind: entity, concept, comparison, procedure, decision, query, summary
- Subject: <your subjects>
- Quality: draft, reviewed, contested, deprecated

## Thresholds

- Create a page when a subject will matter again, appears in several sources, or is central
  to one authoritative source. Otherwise add to the page that covers it.
- Split a page past about 200 lines into focused, linked pages.
- File substantial synthesized answers under `queries/`; not trivial lookups.
- Never store secrets, credentials, payment details, routine progress, TODOs or raw chat.
- Each page should link to at least two related pages where relevant.

## Writing

- Date anything that can change ("as of YYYY-MM-DD", or "read YYYY-MM-DD" for a source).
- Cite the source next to the claim.
- Label claims that are not first-hand, in brackets after the claim: `(vendor-sourced)` for a
  company's claim about itself, `(estimate)` for derived figures, `(unverified)` for anything
  recalled, unconfirmed or unsourced, with a reason after a colon when it helps
  (`(unverified: one chat, not checked)`).
- Edit the smallest section that records the change. Leave a note on every change saying
  what changed and why, under the writer's name.

## Conflicts

1. Check dates, provenance and the current system of record.
2. Replace a claim only when the new one is clearly more authoritative; keep a dated line of
   what it replaced when the history matters.
3. Otherwise keep both, set `contested: true`, and lower `confidence`.
4. Escalate material conflicts to the owner.

## Before substantial work

1. Read this page.
2. List the pages and scan their descriptions.
3. Check recent changes.
4. Search before creating a page.
