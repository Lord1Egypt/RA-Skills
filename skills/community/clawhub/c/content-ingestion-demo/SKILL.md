---
name: content-ingestion-demo
description: Demo skill that turns a raw digital-content file (e.g. a markdown note) into a reusable skill package. Given a source file, it builds a SKILL.md, extracts metadata (title, source path, size, sha256), copies the file under references/, and produces a ready-to-publish .skill package. Used for demonstrating a full ingest-and-publish pipeline.
---

# Content Ingestion Demo

Transform a single raw content file into a skill package suitable for publishing.

## Quick start

```bash
content-ingest.sh <input-file> <output-skill-dir>
```

Example:

```bash
content-ingest.sh ./article.md ./skills/article-note
```

## What it produces

- `SKILL.md` with name/description populated from the input filename and an auto-computed summary.
- `references/article.md` copy of the input (kept readable for human consumers).
- `assets/metadata.json` with size, sha256, created_at, source_path.

## When to use it

- Turn a downloaded article, spec, or note into a reusable asset.
- Feed the resulting folder into `clawhub publish` to land it in the resource center.
- Demos / pipelines where "file in, skill package out" is the unit of work.

## Scripts

`scripts/content-ingest.sh` — the actual converter. Reads `$1`, writes a skill tree under `$2`.
