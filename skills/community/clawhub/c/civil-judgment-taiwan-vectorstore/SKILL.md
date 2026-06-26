---
name: civil-judgment-taiwan-vectorstore
description: Ingest Taiwan civil court judgments (HTML or PDF) — exclusively covering Taiwan civil cases — into Qdrant with Ollama embeddings, preserving traceability, deduplication, and incremental updates.
user-invocable: true
---

# Taiwan Civil Judgment → Vector DB (Qdrant) Ingestion

**Scope: Taiwan civil court judgments only** (民事判決). This skill ingests Taiwan civil cases (HTML **or PDF** files) into Qdrant. All parsing, chunking, and embedding logic lives in `scripts/ingest.py` — your job is to **run the script**, not to reimplement the pipeline.

---

## Quick Start (follow these steps in order)

### Step 1 — Activate venv

```bash
source {baseDir}/.venv/bin/activate
```

### Step 2 — Identify the run folder

The user will provide an **absolute path** to a run folder.

Example: `/path/to/output/judicialyuan/20260305_142030`

Verify it exists and has HTML or PDF files:
```bash
ls <RUN_FOLDER>/archive/ | grep -E '\.(html|pdf)$' | head -5
```

If no `archive/*.html` or `archive/*.pdf` files → **stop and tell the user** the folder has no ingestible data.

### Step 3 — Run ingestion

Use absolute paths throughout — no `cd` needed:

```bash
python3 {baseDir}/scripts/ingest.py \
  --run-folder <RUN_FOLDER>
```

The script handles everything: pre-flight checks, collection auto-creation (creates `civil_case_doc` / `civil_case_chunk` if they don't exist), canonicalization, chunking, embedding, Qdrant upsert, manifest + report writing.

**Re-running the same command on the same folder is always safe** — deterministic IDs mean upsert = overwrite. No special `--resume` flag needed; just run the same command again.

### Step 4 — Check the result

**Successful output looks like:**
```
OK files=42 processed=42 skipped=0 errored=0 doc_points=42 chunk_points=187
manifest=<RUN_FOLDER>/ingest_manifest.jsonl
report=<RUN_FOLDER>/ingest_report.md
```

**Read the report** (human-readable stats summary):
```bash
cat <RUN_FOLDER>/ingest_report.md
```

If there are errors, check the **manifest** (machine-readable, one JSON line per file) for per-file diagnosis:
```bash
grep -E '"status":"(skipped|error|partial)"' <RUN_FOLDER>/ingest_manifest.jsonl
```

### Step 5 — Report to user

Tell the user:
- How many docs were ingested (`doc_points`)
- How many chunks were created (`chunk_points`)
- Whether any were skipped or errored
- Where the report file is

**Done.** Do not proceed to additional steps unless the user asks.

---

## DO NOT rules (critical)

- **DO NOT** write your own HTML parsing, chunking, or embedding code. `ingest.py` handles all of this.
- **DO NOT** modify parsing/chunking logic casually. Only change heading detection or chunk fallback when the user explicitly asks to improve PDF/OCR robustness, and validate on a small sample before re-running a large batch.
- **DO NOT** call Qdrant or Ollama APIs directly. The script does this.
- **DO NOT** use `verify=False` or skip SSL verification for any HTTP request.
- **DO NOT** modify or delete files under `archive/`. Raw HTML is immutable source of truth.
- **DO NOT** change chunking defaults (`--max-chars`, `--overlap-chars`) unless the user explicitly asks.

---

## Hard constraints

- **Raw HTML/PDF is source of truth**; never overwrite it.
- **Deterministic**: same input → same canonical text → same SHA-256 → same Qdrant point IDs. Safe to re-run.
- **Traceability**: every Qdrant point carries `doc_url` + `local_path`.
- **Batched upserts** (≤ 64 points/batch) to avoid Qdrant 32MB payload limit.
- **`parser_version`** in every point's metadata. Current: `v3.5-sentence-boundary`.

---

## Troubleshooting

### `PREFLIGHT_FAILED: Qdrant not reachable`

Qdrant is down or unreachable at the default/configured URL.

```bash
# Check if Qdrant is running
curl -s http://localhost:6333/collections | head -1

# If not running, start it (or ask the user)
```

### `PREFLIGHT_FAILED: Ollama not reachable`

```bash
# Check Ollama
curl -s http://localhost:11434/api/tags | head -5
```

### `PREFLIGHT_FAILED: Ollama model missing: bge-m3:latest`

```bash
ollama pull bge-m3:latest
```

Then re-run Step 3.

### `PREFLIGHT_FAILED: No archive/*.html or archive/*.pdf found`

The run folder exists but has no archived detail pages. Check:
- Is this the correct run folder?

### Output shows `skipped > 0` or `errored > 0`

Check `ingest_manifest.jsonl` for per-file details:
```bash
grep -E '"status":"(skipped|error|partial)"' "<RUN_FOLDER>/ingest_manifest.jsonl"
```

| Manifest status | Meaning | Action |
|-----------------|---------|--------|
| `ok` | Doc + all chunks ingested | None |
| `partial` | Doc upserted, but some section chunks failed embedding | Check Ollama stability; can re-run safely |
| `skipped` | Doc-level embedding failed — nothing upserted for this doc | Check Ollama; re-run safely |
| `error` | HTML read/parse failed | Check if the HTML file is corrupted |

Re-running is always safe — use the exact same command. No special flags needed; deterministic IDs → upsert/overwrite.

### Override service endpoints

```bash
# Via environment variables
OLLAMA_URL=http://localhost:11434 QDRANT_URL=http://localhost:6333 \
  python3 scripts/ingest.py --run-folder "..."

# Via CLI flags (take precedence over env vars)
python3 scripts/ingest.py --run-folder "..." \
  --ollama http://localhost:11434 --qdrant http://localhost:6333
```

Default endpoints:

| Service | Default | Env override |
|---------|---------|--------------|
| Ollama | `http://localhost:11434` | `$OLLAMA_URL` |
| Qdrant | `http://localhost:6333` | `$QDRANT_URL` |

### Test with a small batch first

```bash
python3 scripts/ingest.py --run-folder "..." --limit 5
```

---

## Input folder structure (expected)

```
<run_folder>/
  archive/
    fjud_detail_001.html               ← HTML input
    fjud_detail_002.html
    fjud_detail_003.pdf                ← PDF input (also supported)
    fint_detail_001.html               (if system=both)
  results_fjud.jsonl                   (optional)
  results_fint.jsonl                   (optional)
```

The script discovers all `archive/*.html` and `archive/*.pdf` files automatically (sorted by filename). HTML and PDF files can coexist in the same run folder.

**v1 limitation**: The `system` metadata field is currently hardcoded to `FJUD`. If a run folder contains both FJUD and FINT files, FINT files will be ingested but mislabeled as `FJUD`. This does not affect chunking or embeddings — only the `system` metadata field on the resulting Qdrant points.

---

## CLI reference

```
python3 scripts/ingest.py --run-folder <PATH> [options]
```

| Flag | Default | Description |
|------|---------|-------------|
| `--run-folder` | (required) | Path to an input folder |
| `--ollama` | `$OLLAMA_URL` or `http://localhost:11434` | Ollama endpoint |
| `--qdrant` | `$QDRANT_URL` or `http://localhost:6333` | Qdrant endpoint |
| `--embed-model` | `bge-m3:latest` | Ollama embedding model |
| `--vector-size` | `1024` | Vector dimension |
| `--max-chars` | `900` | Max chars per chunk (500–1000) |
| `--overlap-chars` | `150` | Overlap between chunks (10–20% of max-chars) |
| `--limit` | `0` (no limit) | Process only first N files sorted by filename (lexicographic order); for testing |

---

## Outputs

- **Qdrant collections**: `civil_case_doc` (1 point/doc), `civil_case_chunk` (many points/doc). Auto-created if they don't exist.
- **`ingest_report.md`**: human-readable summary (doc/chunk counts, error counts). **Read this first** after ingestion.
- **`ingest_manifest.jsonl`**: machine-readable, one JSON line per doc with status (`ok` / `partial` / `skipped` / `error`). **Read this to diagnose specific file failures** (grep for non-`ok` statuses). Both files overlap on aggregate counts; the manifest adds per-file detail.

---

## Roadmap
- **v1** (current): doc + section-aware chunks
- **v2**: candidate issue extraction (爭點抽取)
- **v3**: issue-level index (`civil_case_issue` collection)

---

## Internal details

For metadata schema, canonicalization rules, section-splitting patterns, and chunking implementation, see [`references/internals.md`](references/internals.md).

---

## Lessons learned / operational gotchas
- Qdrant rejects non-UUID/non-integer point IDs (`400 Bad Request`). The script uses deterministic UUIDs — do not change the ID generation logic.
- Qdrant rejects payloads > 32MB. The script batches at 64 points — do not increase batch size.
- Re-running on the same folder is safe: deterministic IDs mean upsert = overwrite.
- 台灣判決書 section headings 格式不統一（e.g.「理　由」with fullwidth space、兼容字如「⽂」）。目前 parser 已先做 heading normalization；若仍切不出 section，會 fallback 對 `full` 做 chunking，避免只留下 doc-level points。
