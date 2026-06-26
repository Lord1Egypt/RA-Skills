# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [1.0.0] — 2026-03-09

First stable release. Incorporates all changes from v0.1.0 through v0.4.0; see those
entries for the full feature history. This release marks the completion of milestones
M0–M3 and the first version recommended for production use.

### Changed
- Minor wording fixes across documentation

### Notes
- All four milestones passed acceptance testing (M0–M3)
- Known debt: `doc_url` missing for ~49% of ingested docs (upstream extraction issue);
  tracked for a future patch release

---

## [0.4.0] — 2026-03-09

### Added
- **`civil_case_reasoning` collection** — each reasoning snippet from `civil_case_doc`
  is now a standalone vector point, enabling direct semantic search over subsumption
  conclusions without retrieving the full judgment
- **`scripts/build_reasoning_collection.py`** — idempotent build script that reads all
  `civil_case_doc` points, embeds each `reasoning_snippets[]` entry via Ollama, and
  upserts into `civil_case_reasoning` with deterministic UUIDs; supports `--rebuild`
  (drop and recreate), `--dry-run`, and `--limit` flags
- Intra-doc snippet deduplication in the build script to prevent identical context
  windows from creating duplicate points

### Notes
- M3 acceptance passed (2026-03-09): 1761 points, 317/317 docs covered, 0 cue-word
  mismatches, cross-collection links verified, human retrieval quality passed
- Known debt: 201 source docs in `civil_case_doc` have empty `doc_url` (upstream
  ingestion issue); does not affect retrieval quality

---

## [0.3.0] — 2026-03-06

### Added
- **Rich semantic fields per judgment** — each Qdrant doc point now carries extracted
  payload ready for RAG filtering and display (`parser_version: v3.5-sentence-boundary`):
  - `reasoning_snippets`: the court's own subsumption conclusions (涵攝推理), detected
    by 17 inferential connectives (是故/因此/準此/從而 etc.); each snippet spans the
    triggering sentence plus one sentence of context on either side
  - `norms_reasoning_snippets`: norm citations together with their applied-fact context;
    expanded backwards/forwards when the sentence ends with 定有明文 or continues with 又
  - `fact_reason_snippets`: key fact-finding paragraphs, triggered by 查/經查/惟查
  - `cited_norms`: flat list of cited statutes and precedents (民法, 民事訴訟法, 釋字, 最高法院判例 etc.)
  - `candidate_issues`: disputed issues (爭點) extracted from explicit 爭點/爭執事項 blocks
- **`issues.jsonl`** written per run folder — machine-readable list of candidate issues
  across all ingested documents
- **Supreme Court handling** — 最高法院 judgments always use the full text for extraction
  (their format does not contain the standard reasoning-section headers)
- **Noise filters** — party assertions (sentences ending with `等語`) and prior-court
  citations (sentences starting with `原審以/認/為`) are excluded from all extractions

### Changed
- Snippet boundaries are now sentence-accurate — splitting changed from `str.split("。")`
  to a character-by-character scan so that the terminal「。」is preserved on each sentence,
  preventing boundary drift when sentences are rejoined

### Notes
- M1 quality check passed (2026-03-06): `court_tier` filter confirmed working, traceability
  fields (`doc_url` + `local_path`) present on all documents, reasoning chunks readable and
  free of navigation/toolbar noise

---

## [0.2.0] — 2026-03-05

### Added
- **PDF ingestion** — judgment PDFs are now accepted alongside HTML; the pipeline
  auto-discovers both file types under `archive/` (via `pypdf`)
- **Structured metadata from HTML tables** — court, date, case number, cause, and parties
  are parsed from the judgment's information table rather than inferred from free text
- **ISO dates** — ROC calendar dates (民國年) are converted to ISO 8601 for reliable
  range filtering in Qdrant
- **Court tier classification** — each document is labelled `supreme` / `high` /
  `district` / `other` based on the court name, enabling tier-scoped queries
- **Stable point IDs** — UUIDs derived deterministically from content hash; re-ingesting
  the same file always produces the same ID, so upsert is safe and idempotent
- **Batched upserts** — writes to Qdrant in batches of ≤ 64 points to stay within the
  32 MB payload limit

### Changed
- Collections renamed to domain-scoped names:
  `jy_doc_index` / `jy_chunk_index` → `civil_case_doc` / `civil_case_chunk`

---

## [0.1.0] — 2026-03-05

### Added
- **End-to-end ingestion pipeline** — takes a `judicialyuan-search` run folder and
  produces searchable vectors in Qdrant: HTML → canonical text → section split →
  chunking → Ollama embedding → upsert
- **Section-aware chunking** — documents are split at structural headings
  (主文/事實/理由/結論) before chunking, so chunk boundaries respect legal document
  structure; falls back to full-document chunking when no headings are detected
- **CJK-optimised chunker** — character-level splitting at 900 chars with 150-char
  overlap; no tokeniser dependency
- **Multilingual embedding** via Ollama `bge-m3:latest` (1024 dims, cosine distance)
- **Two-level index**: `civil_case_doc` (one point per judgment for document-level
  retrieval) and `civil_case_chunk` (one point per chunk for passage-level retrieval);
  both collections are auto-created on first run
- **Safe re-runs** — SHA-256 content hashing produces deterministic point IDs;
  re-ingesting the same file is always an overwrite, never a duplicate
- **Run artefacts**: `ingest_manifest.jsonl` (per-file status: `ok` / `partial` /
  `skipped` / `error`) and `ingest_report.md` (human-readable summary)
- **Flexible endpoint config** — Ollama and Qdrant URLs configurable via CLI flags or
  `OLLAMA_URL` / `QDRANT_URL` environment variables
- **Pre-flight checks** — validates Qdrant reachability, Ollama reachability, model
  availability, and presence of archive files before starting ingestion

[Unreleased]: https://github.com/alex02131926/civil-judgment-taiwan-vectorstore/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/alex02131926/civil-judgment-taiwan-vectorstore/compare/v0.4.0...v1.0.0
[0.4.0]: https://github.com/alex02131926/civil-judgment-taiwan-vectorstore/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/alex02131926/civil-judgment-taiwan-vectorstore/releases/tag/v0.3.0
[0.2.0]: https://github.com/alex02131926/civil-judgment-taiwan-vectorstore/releases/tag/v0.2.0
[0.1.0]: https://github.com/alex02131926/civil-judgment-taiwan-vectorstore/releases/tag/v0.1.0
