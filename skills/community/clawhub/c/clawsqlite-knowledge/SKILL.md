---
name: clawsqlite-knowledge
description: Knowledge base skill that wraps the clawsqlite knowledge CLI for ingest/search/show.
version: 1.0.2
metadata: {"openclaw":{"homepage":"https://github.com/ernestyu/clawsqlite","tags":["knowledge","sqlite","search","cli"],"requires":{"bins":["python"],"env":[]},"install":[{"id":"clawsqlite_knowledge_bootstrap","kind":"python","label":"Install clawsqlite from PyPI","script":"bootstrap_deps.py"}],"runtime":{"entry":"run_clawknowledge.py"},"first_run":{"summary":"Before relying on this skill, run `clawsqlite knowledge doctor --json` once to check knowledge DB paths, vec0/embedding, and small LLM configuration.","steps":[{"id":"run_doctor","kind":"manual","label":"Run clawsqlite knowledge doctor","command":"clawsqlite knowledge doctor --json","notes":"Inspect the JSON report and address any missing paths (CLAWSQLITE_ROOT/DB), vec0/vec index issues, or incomplete EMBEDDING_* / SMALL_LLM_* settings before using this skill in production agents."}]}}}
---

# clawsqlite-knowledge (OpenClaw Skill)

`clawsqlite-knowledge` is a knowledge base Skill built around the PyPI package **clawsqlite**.

It is a **thin wrapper**:

- it does not vendor the source code and does not git clone any repository;
- during installation, it installs `clawsqlite>=1.0.2` (with a workspace-prefix fallback when the runtime env is not writable);
- during runtime, it operates the knowledge base only through the `clawsqlite knowledge ...` CLI.

Its main capabilities are grouped into three areas:

1. **Ingestion**
   - ingest from a URL (together with an existing fetch tool such as clawfetch);
   - ingest from a piece of text, an idea, or an excerpt (marked as a local source).
2. **Retrieval**
   - hybrid retrieval (LLM-aware query_refine/query_tags + FTS/vec with
     automatic downgrade)
   - show a full record by id (including full content).
3. **Reporting (via underlying CLI)**
   - build interest clusters (summary/tag embeddings → interest topics)
   - generate periodic interest reports (Markdown + PNG, optional HTML/PDF)
     for the current knowledge base, based on previously built interest clusters.

---

## Installation (performed by ClawHub / OpenClaw)

This skill is meant to be installed and run inside an OpenClaw/ClawHub runtime.
It assumes:

- Python 3.10+ is available in the Skill runtime environment;
- the environment can access PyPI to install the `clawsqlite` package;
- the runtime model has access to a workspace directory where this skill lives
  under `skills/clawsqlite-knowledge`.

### Stage 1 — install the skill shell

Use the OpenClaw CLI to install the skill into your active workspace:

```bash
openclaw skills install clawsqlite-knowledge
```

This step downloads the skill package from ClawHub into:

```text
~/.openclaw/workspace/skills/clawsqlite-knowledge
```

At this point the directory only contains:

- `SKILL.md`
- `manifest.yaml`
- `bootstrap_deps.py`
- `run_clawknowledge.py`
- `README.md` / `README_zh.md`

The `clawsqlite` PyPI package itself **is not yet guaranteed to be installed**.

### Stage 2 — install or upgrade `clawsqlite` (PyPI, >=0.1.4)

The second stage is handled by the bootstrap script declared in
`manifest.yaml`:

```yaml
install:
  - id: clawsqlite_knowledge_bootstrap
    kind: python
    label: Install clawsqlite from PyPI
    script: bootstrap_deps.py
```

`bootstrap_deps.py` is intentionally small and auditable. In simplified form:

```python
requirement = "clawsqlite>=1.0.2"
cmd = [sys.executable, "-m", "pip", "install", requirement]
proc = subprocess.run(cmd)
if proc.returncode != 0:
    prefix = _workspace_prefix()
    subprocess.run([
        sys.executable,
        "-m",
        "pip",
        "install",
        requirement,
        f"--prefix={prefix}",
    ])
```

Semantics:

- First, it tries to install `clawsqlite>=1.0.2` into the default venv used for
  the Skill runtime.
- If that fails (e.g. read-only venv), it falls back to a **workspace-local
  prefix**:

  ```text
  <workspace>/skills/clawsqlite-knowledge/.clawsqlite-venv
  ```

- On success in the prefix, it prints a `NEXT:` hint describing:
  - Where the package is installed; and
  - Which site-packages path will be added to `PYTHONPATH` at runtime.

From the OpenClaw CLI, you typically do not need to call
`bootstrap_deps.py` manually; `openclaw skills install clawsqlite-knowledge`
(or a future `openclaw skills update ...`) will run the install hooks. If you
want to force a re-install or upgrade of `clawsqlite` to 0.1.4+ inside the
skill directory, you can run:

```bash
cd ~/.openclaw/workspace/skills/clawsqlite-knowledge
python bootstrap_deps.py
```

### Where does the `clawsqlite` CLI live?

Depending on how `pip` is configured:

- If the first `pip install` succeeds in the base env, the `clawsqlite`
  command and `clawsqlite_cli` module live in that venv;
- If we fall back to the workspace prefix, `clawsqlite` will be installed
  under `.clawsqlite-venv` and the Skill runtime adds its site-packages
  directory to `PYTHONPATH` before invoking `run_clawknowledge.py`.

For advanced users, this means you can also invoke the CLI manually from the
same prefix, for example:

```bash
cd ~/.openclaw/workspace/skills/clawsqlite-knowledge
PYTHONPATH="$(python - << 'EOF'
from bootstrap_deps import _workspace_prefix, _site_packages
p = _workspace_prefix()
print(_site_packages(p))
EOF)"$PYTHONPATH" \
  python -m clawsqlite_cli knowledge --help
```

In normal Skill usage (agents calling the JSON API), you do **not** need to
manage this manually.

---

## Runtime entry

The Skill runtime calls `run_clawknowledge.py`. This script:

- reads a JSON payload from stdin;
- routes by the `action` field to the matching handler;
- calls `python -m clawsqlite_cli knowledge ...` to perform the actual operation;
- writes the result JSON back to stdout.

All CLI calls are centralized in one function, which also injects the
workspace-prefix site-packages path into `PYTHONPATH` when present so that the
fallback installation works transparently.

If the underlying CLI emits `NEXT:` hints, this runtime surfaces them as a
structured `next` array in the JSON response. On failure, it also includes an
`error_kind` field for quick classification.

---

## Supported actions

### 1. `ingest_url`

Ingest an article from a URL. The actual fetching logic is determined by the
environment variable `CLAWSQLITE_SCRAPE_CMD` (recommended: the clawfetch CLI).
This Skill does not fetch web pages directly.

**Example payload:**

```json
{
  "action": "ingest_url",
  "url": "https://mp.weixin.qq.com/s/UzgKeQwWWoV4v884l_jcrg",
  "title": "WeChat article: Ground Station project",   // optional
  "category": "web",                                   // optional (default: web)
  "tags": "wechat,ground-station",                     // optional
  "gen_provider": "openclaw",                          // optional: openclaw|llm|off (default: openclaw)
  "root": "/data/clawsqlite-knowledge"                 // optional storage directory
}
```

**Behavior:**

- calls `clawsqlite knowledge ingest --url ...`;
- by default uses `provider=openclaw`:
  - generates a long summary with heuristics (first ~800 characters, cut by
    sentence/paragraph boundaries);
  - generates tags with jieba or a lightweight algorithm (in 0.1.4 these are
    backed by the new keyword/semantic pipelines);
  - if embedding configuration is complete, generates an embedding for the long
    summary and stores it in the vec table;
- filenames use pinyin plus an English slug for easier cross-platform storage;
- the database keeps the original title and `source_url`.

**Returns:**

```json
{
  "ok": true,
  "data": { "id": 1, "title": "...", "local_file_path": "...", ... }
}
```

### 2. `ingest_text`

Ingest a piece of text, an idea, or an excerpt, marked as a local source.

**Example payload:**

```json
{
  "action": "ingest_text",
  "text": "Today I had an idea about a web scraping architecture...",
  "title": "Notes on web scraping architecture",   // optional; auto-generated if omitted
  "category": "idea",                              // optional (default: note)
  "tags": "crawler,architecture",                  // optional
  "gen_provider": "openclaw",                      // optional
  "root": "/data/clawsqlite-knowledge"             // optional storage directory
}
```

**Behavior:**

- calls `clawsqlite knowledge ingest --text ...`;
- generates long summary, tags, and embedding the same way as in the URL case,
  depending on configuration;
- `source_url` will be `Local`;
- filenames use pinyin / English slug for easier cross-platform handling.

### 3. `search`

Search the knowledge base using the full `clawsqlite>=1.0.2` search
pipeline (query_refine/query_tags + FTS/vec hybrid), with automatic
downgrade when embeddings or vec0 are not available.

**Example payload:**

```json
{
  "action": "search",
  "query": "web scraping architecture",
  "mode": "hybrid",               // optional: hybrid|fts|vec (default: hybrid)
  "topk": 10,                     // optional
  "category": "idea",             // optional
  "tag": "crawler",               // optional
  "include_deleted": false,       // optional
  "root": "/data/clawsqlite-knowledge"   // optional storage directory
}
```

**Behavior (high level):**

- Calls `clawsqlite knowledge search ...` with `--json` and forwards filters.
- Uses the new four-mode capability model inside clawsqlite:
  - Mode1: LLM + Embedding → query_refine + query_tags from SMALL_LLM,
    content/tag vectors + FTS + lexical tags.
  - Mode2: LLM + no Embedding → LLM-based query_refine/query_tags + FTS +
    lexical tags.
  - Mode3: no LLM + Embedding → heuristic query_refine/query_tags + content
    vectors + tag vectors + FTS/lexical tags.
  - Mode4: no LLM + no Embedding → heuristic query_refine/query_tags + FTS +
    lexical tags only.
- In all modes, natural-language queries are converted into:
  - `query_refine`: a single, search-friendly sentence;
  - `query_tags`: a small set of keywords (length controlled by
    `CLAWSQLITE_SEARCH_QUERY_TAG_MIN/MAX`).
- When embeddings are available, the search scorer uses:
  - content vectors (summary-based) for semantic similarity;
  - tag vectors + lexical tag matches as a tag channel;
  - FTS rank for BM25-like keyword matching;
  - priority and recency as light biases.
- Tag scoring is split into semantic and lexical parts, controlled by
  `CLAWSQLITE_TAG_VEC_FRACTION` and `CLAWSQLITE_TAG_FTS_LOG_ALPHA`.
- Final scores are a weighted sum of these channels, with per-mode default
  weights tunable via `CLAWSQLITE_SCORE_WEIGHTS_MODE1..4` (and legacy
  `CLAWSQLITE_SCORE_WEIGHTS*`).

This skill does **not** re-implement scoring; it simply forwards the JSON
result and lets agents inspect `score`, `score_components`, and any
`next` hints surfaced by the underlying CLI.

**Returns:**

```json
{
  "ok": true,
  "data": [
    {"id": 3, "title": "...", "category": "idea", "score": 0.92, ...},
    ...
  ]
}
```

### 4. `show`

Show one record from the knowledge base by id, optionally including full
content.

**Example payload:**

```json
{
  "action": "show",
  "id": 3,
  "full": true,                   // optional, default: true
  "root": "/data/clawsqlite-knowledge"   // optional storage directory
}
```

**Behavior:**

- calls `clawsqlite knowledge show --id ... --full --json`;
- returns full metadata and optional body content (the `content` field).

---

## FTS/jieba fallback (CJK)

This Skill relies on the underlying `clawsqlite` CLI for FTS tokenization.
When the CJK tokenizer extension `libsimple` cannot be loaded, `clawsqlite`
can switch to a jieba-based pre-segmentation mode controlled by
`CLAWSQLITE_FTS_JIEBA=auto|on|off`:

- `auto` (default): only enable when `libsimple` is unavailable **and** `jieba` is installed.
- `on`: force jieba pre-segmentation even if `libsimple` is available.
- `off`: disable jieba pre-segmentation.

In jieba mode, CJK text is segmented with jieba and joined with spaces before
being written to the FTS index; queries apply the same normalization, so
write/rebuild/query stay consistent.

If you change this setting on an existing DB, rebuild the FTS index:

```bash
clawsqlite knowledge reindex --rebuild --fts
```

---

## Maintenance (CLI only)

This skill intentionally does **not** expose destructive maintenance actions
via its JSON API. To clean up orphan files, old backups, or compact the
knowledge database, use the `clawsqlite` CLI directly from a trusted
administrative context, for example:

```bash
# Preview maintenance (no deletions)
clawsqlite knowledge maintenance prune \
  --root /data/clawsqlite-knowledge \
  --days 3 \
  --dry-run \
  --json

# Apply maintenance (delete orphans + old backups, then VACUUM)
clawsqlite knowledge maintenance prune \
  --root /data/clawsqlite-knowledge \
  --days 7 \
  --json
```

Only administrators or scheduled automation should run these commands. Agents
using the `clawsqlite-knowledge` skill have access only to ingestion,
retrieval, and show operations.

---

## Security and auditability

- The Skill depends only on the `clawsqlite` package from PyPI.
- It does not vendor source code, does not git clone, and does not download
  extra binaries.
- All knowledge base operations are performed through explicit
  `clawsqlite knowledge ...` CLI calls, and their `stdout/stderr` can be fully
  audited in logs.
