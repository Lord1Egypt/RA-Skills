# Internals Reference — judgment-vectorstore

> This file documents the internal implementation details of `scripts/ingest.py`.
> You do **not** need to read this file to run ingestion — see SKILL.md Quick Start.
> Read this only when debugging parsing issues or planning changes to the pipeline.

---

## Metadata schema (v1)

### Doc point (`civil_case_doc`) — required fields

| Field | Type | Source |
|-------|------|--------|
| `title` | string | HTML `<title>` tag |
| `court` | string | First token of title |
| `court_tier` | string | `supreme` / `high` / `district` / `other` (classified from court name) |
| `date` | string (ISO) | Parsed from 裁判日期（民國→西元） |
| `date_raw` | string | Original 裁判日期 text |
| `case_no` | string | 裁判字號 |
| `cause` | string | 裁判案由 |
| `parties_raw` | string | Raw party block (heuristic) |
| `doc_url` | string | Canonical detail-page URL |
| `local_path` | string | Absolute path to archived HTML file |
| `doc_sha256` | string | SHA-256 of canonical plain text |
| `source_run` | string | Run folder name prefix (timestamp) |
| `system` | string | `FJUD` or `FINT` |
| `parser_version` | string | e.g. `v1.1-meta` |
| `level` | string | `"doc"` |

### Chunk point (`civil_case_chunk`) — all doc fields plus:

| Field | Type | Description |
|-------|------|-------------|
| `section` | string | `holding` / `facts` / `claims` / `reasoning` / `conclusion` |
| `chunk_index` | int | 0-based index within section |
| `chunk_sha256` | string | SHA-256 of chunk text |
| `text` | string | Chunk plain text (for payload retrieval) |
| `level` | string | `"chunk"` |

---

## Canonicalization rules

All rules are implemented in `ingest.py` and applied **deterministically** — same HTML → same canonical text.

1. **Tag removal**: decompose `<script>`, `<style>`, `<noscript>` elements.
2. **Text extraction**: `soup.get_text("\n")` (newline separator preserves block structure).
3. **Whitespace normalization** (in this exact order):
   - `\r\n` / `\r` → `\n`
   - Strip trailing whitespace per line
   - Collapse 3+ consecutive newlines → 2
   - Collapse 2+ consecutive spaces/tabs → 1 space
   - Strip leading/trailing whitespace from entire text
4. **Encoding**: UTF-8. Undecodable bytes → `errors="ignore"`.
5. **Title prepend**: if parsed title is non-empty and text doesn't already start with it, prepend `title + "\n\n"` before normalization.

> **Any change to these rules MUST bump `parser_version`.**

---

## Section splitting

Rule-based heading detection on the canonical plain text.

### Heading patterns (exact line match)

| Section key | Heading synonyms |
|-------------|-----------------|
| `holding` | 主文 |
| `facts` | 事實, 事實及理由, 理由 |
| `claims` | 理由, 兩造, 當事人 |
| `reasoning` | 理由, 理由要旨 |
| `conclusion` | 結論, 綜上, 據上, 依據, 如主文 |

### Fallback
If **no heading is detected** → entire document is treated as a single section `"full"`.

**`full` section behavior**: The `full` section is **never chunked** — it produces zero chunk points in `civil_case_chunk`. It is used only for the doc-level embedding in `civil_case_doc` (first ≤ 1200 chars of canonical text). When headings *are* detected, `full` is still stored internally (the complete text) but explicitly skipped during chunk generation (`if section_name == "full": continue`).

---

## Chunking parameters

| Parameter | Default | CLI flag | Acceptable range |
|-----------|---------|----------|-----------------|
| `max_chars` | 900 | `--max-chars` | 500–1000 CJK chars |
| `overlap_chars` | 150 | `--overlap-chars` | 10–20% of `max_chars` |

Character-level chunker (not token-based). Overlap ensures cross-boundary retrieval.

---

## Collections (v1)

| Collection | Granularity | Vector | Distance |
|------------|-------------|--------|----------|
| `civil_case_doc` | 1 point per doc | 1024 dims | cosine |
| `civil_case_chunk` | many points per doc | 1024 dims | cosine |

If a collection does not exist, `ingest.py` auto-creates it.

---

## Manifest status values

Each doc produces exactly one row in `ingest_manifest.jsonl`:

| Status | Meaning |
|--------|---------|
| `ok` | Doc + all chunks ingested successfully |
| `partial` | Doc point upserted, but some section chunks failed embedding (`error` field lists which sections) |
| `skipped` | Doc-level embedding failed — nothing upserted for this doc |
| `error` | HTML read or parse failed — nothing upserted for this doc |

---

For extraction algorithm design (reasoning snippets, norm citations, fact-finding
paragraphs), see [extraction-design.md](extraction-design.md).
