# clawsqlite-knowledge (ClawHub Skill)

`clawsqlite-knowledge` is a ClawHub skill that wraps the
[clawsqlite](https://github.com/ernestyu/clawsqlite) **knowledge** CLI and
exposes a small, opinionated API for day‑to‑day knowledge base work.

It is **not** a generic SQLite tool. Instead, it focuses on the common
operations you actually want to automate in OpenClaw agents:

- Ingest articles from the web (URL → markdown + SQLite)
- Ingest your own notes/ideas/quotes as text
- Search the knowledge base (FTS / hybrid / vec)
- Show a single record by id
- Use the underlying `clawsqlite` CLI for maintenance (orphan detection + GC)

All heavy lifting (schema, indexing, embedding, maintenance) is implemented
in the `clawsqlite` PyPI package. This skill is just a thin, auditable
wrapper.

For environment sanity checks (paths, vec0, embedding, small LLM), the
underlying CLI now exposes a `doctor` subcommand:

```bash
# Installed via PyPI
clawsqlite knowledge doctor --json

# From source (inside the repo) without installing the wheel
python -m clawsqlite_knowledge.cli doctor
```

It is strongly recommended to run `clawsqlite knowledge doctor` once when
setting up a new environment or troubleshooting search/embedding behavior.

> If you need full control over `clawsqlite` (plumbing commands, custom
> tables, advanced CLIs), use the Python package and CLI directly instead of
> this skill.

---

## 1. Relationship to clawsqlite

- **clawsqlite (PyPI / GitHub)**
  - A general‑purpose CLI and library for SQLite‑backed knowledge bases.
  - Exposes multiple namespaces: `clawsqlite knowledge|db|index|fs|embed`.
  - Suitable for direct shell use, scripting, and other applications.

- **clawsqlite-knowledge (this skill)**
  - Lives under `clawhub-skills/clawsqlite-knowledge`.
  - Installed inside the ClawHub/OpenClaw environment as a skill.
  - Depends on `clawsqlite` via PyPI (no vendored source, no git clone).
  - Exposes a **small JSON API** over stdin/stdout (and expects
    `clawsqlite knowledge doctor` to be available in the environment):
    - `ingest_url`
    - `ingest_text`
    - `search`
    - `show`

The idea is:

- Use `clawsqlite` when you want the **full CLI** and Python library;
- Use `clawsqlite-knowledge` when you want a **high‑level skill** your agents can
  call to manage a personal knowledge base.

---

## 2. Installation & upgrade (two-stage)

This skill is installed and upgraded in **two stages**:

1. Install / update the **skill shell** from ClawHub
2. Install / update the **clawsqlite PyPI package (v0.1.7+)** that the skill
   depends on

### 2.1 Stage 1 — install the skill shell

From the OpenClaw environment, use the skills CLI to install the skill into
your active workspace:

```bash
openclaw skills install clawsqlite-knowledge
```

This will create a directory like:

```text
~/.openclaw/workspace/skills/clawsqlite-knowledge
```

At this point you only have:

- `SKILL.md`
- `manifest.yaml`
- `bootstrap_deps.py`
- `run_clawknowledge.py`
- `README.md` / `README_zh.md`

> **Important:** After Stage 1, the skill shell is present, but the underlying
> `clawsqlite` CLI may still be missing or outdated. Stage 2 ensures
> `clawsqlite>=1.0.2` is available in the runtime Python environment.

### 2.2 Stage 2 — install or upgrade `clawsqlite` (PyPI, v0.1.7)

The second stage is handled by the bootstrap script declared in
`manifest.yaml`:

```yaml
install:
  - id: clawsqlite_knowledge_bootstrap
    kind: python
    label: Install clawsqlite from PyPI
    script: bootstrap_deps.py
```

The script content (simplified) is:

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

This means:

- It first tries to install `clawsqlite>=1.0.2` into the default Python
  environment used by the skill runtime;
- If that environment is read‑only (or `pip install` fails), it falls back to a
  **workspace‑local prefix** under:

  ```text
  <workspace>/skills/clawsqlite-knowledge/.clawsqlite-venv
  ```

- On success in the prefix, the script prints a `NEXT:` hint describing how the
  runtime will add the prefix site‑packages directory to `PYTHONPATH`, so both
  the skill and any manual CLI calls can see the installed `clawsqlite`.

To trigger Stage 2 explicitly after installing the skill shell, run:

```bash
cd ~/.openclaw/workspace/skills/clawsqlite-knowledge
python bootstrap_deps.py
```

or, from the OpenClaw CLI if supported:

```bash
openclaw skills install clawsqlite-knowledge  # re-runs the install hooks
```

> **Note:** This skill **never** vendors `clawsqlite` source code or clones the
> GitHub repo. The only way it brings in code is via `pip install
> "clawsqlite>=1.0.2"`.

### 2.3 Where is the `clawsqlite` CLI installed?

Depending on your environment:

- If `pip install clawsqlite>=1.0.2` succeeds in the base runtime venv, the
  `clawsqlite` entrypoint will live in that venv’s `bin` directory and be
  importable as the `clawsqlite_cli` module.
- If the bootstrap falls back to the workspace prefix,
  `clawsqlite` will be installed under:

  ```text
  <workspace>/skills/clawsqlite-knowledge/.clawsqlite-venv/
  ```

  The runtime will add that prefix’s `site-packages` directory to
  `PYTHONPATH` before executing `run_clawknowledge.py`, so that
  `python -m clawsqlite_cli` works as expected.

For OpenClaw users who also want to use the `clawsqlite` CLI manually on the
host, a safe pattern is:

```bash
cd ~/.openclaw/workspace/skills/clawsqlite-knowledge
PYTHONPATH="$(python - << 'EOF'
from bootstrap_deps import _workspace_prefix, _site_packages
p = _workspace_prefix()
print(_site_packages(p))
EOF)"$PYTHONPATH" \
  python -m clawsqlite_cli knowledge --help
```

But in normal Skill usage, you do **not** need to care about this — the runtime
handles it automatically.

---

## 3. Runtime contract

The runtime entry `run_clawknowledge.py`:

- Reads a JSON object from stdin
- Inspects the `action` field
- Dispatches to a handler
- Calls `python -m clawsqlite_cli knowledge ...` under the hood
- Writes a JSON result to stdout

Common fields:

- `root` (optional): override the knowledge root directory
- `action`: one of the supported actions below

All handlers return a JSON object with at least:

- `ok: true|false`
- `data: ...` on success, or `error` / `exit_code` / `stdout` / `stderr` on failure
- `next: [...]` when the underlying CLI emits NEXT hints
- `error_kind` on failures (e.g., missing scraper / vec / permission)

---

## 4. Recommended first step: run `doctor`

Before using this skill in a new environment, it is recommended that an
agent or human operator first run the underlying doctor command and
inspect the report:

```bash
clawsqlite knowledge doctor --json
```

This checks:

- CLAWSQLITE_ROOT / CLAWSQLITE_DB paths (do they exist?)
- sqlite-vec extension and vec tables (vec0/vec index availability)
- Embedding configuration (EMBEDDING_* + CLAWSQLITE_VEC_DIM)
- Small LLM configuration (SMALL_LLM_* triple)
- Overall capability mode (LLM+Embedding / LLM-only / Embedding-only / FTS-only)

Agents can use this report to decide which search modes to enable (fts vs
hybrid/vec), and whether to surface NEXT hints to the user.

## 5. Supported actions

### 4.1 `ingest_url`

Ingest a web article via URL.

**Payload example:**

```json
{
  "action": "ingest_url",
  "url": "https://mp.weixin.qq.com/s/UzgKeQwWWoV4v884l_jcrg",
  "title": "WeChat article: Ground Station project",
  "category": "web",
  "tags": "wechat,ground-station",
  "gen_provider": "openclaw",
  "root": "/home/node/.openclaw/workspace/knowledge_data"
}
```

Notes:

- Actual scraping is done by `clawsqlite knowledge ingest --url ...` using
  the configured `CLAWSQLITE_SCRAPE_CMD` (recommended: the `clawfetch`
  skill/CLI).
- `ingest_url` only wraps that CLI call and returns the JSON result.

### 4.2 `ingest_text`

Ingest a note/idea/quote as plain text.

**Payload example:**

```json
{
  "action": "ingest_text",
  "text": "Today I had an idea about a web scraping architecture...",
  "title": "Notes on web scraping architecture",
  "category": "idea",
  "tags": "crawler,architecture",
  "gen_provider": "openclaw",
  "root": "/home/node/.openclaw/workspace/knowledge_data"
}
```

This is the path for:

- spontaneous ideas
- quotes from books/novels
- short notes you dictate to an agent

The underlying `clawsqlite knowledge ingest --text ...` call will:

- Generate a long summary (up to ~800 characters, soft‑truncated)
- Extract tags using jieba/heuristics (in clawsqlite>=1.0.2 these reuse the
  same TextRank/semantic pipelines as the query‑side keyword extraction)
- Optionally embed the summary (when embedding is configured)
- Store a markdown file with a pinyin/ASCII slug filename

### 4.3 `search`

Search the knowledge base using the new `clawsqlite>=1.0.2` search
pipeline (LLM-aware query_refine/query_tags + FTS/vec hybrid).

Under the hood this calls `clawsqlite knowledge search ... --json` and
forwards filters, then surfaces the structured results.

High-level behavior:

- Queries are split into:
  - `query_refine`: a search-friendly sentence (LLM or heuristic);
  - `query_tags`: a small set of keywords (length controlled by
    `CLAWSQLITE_SEARCH_QUERY_TAG_MIN/MAX`).
- Capability modes are decided by whether embeddings and SMALL_LLM are
  available:
  - Mode1 (LLM + Embedding): LLM builds query_refine/query_tags, then the
    scorer uses content/tag vectors + FTS + lexical tags.
  - Mode2 (LLM + no Embedding): LLM builds query_refine/query_tags, then
    the scorer uses FTS + lexical tags only.
  - Mode3 (no LLM + Embedding): heuristic query_refine/query_tags,
    content/tag vectors + FTS + lexical tags.
  - Mode4 (no LLM + no Embedding): heuristic query_refine/query_tags,
    FTS + lexical tags only.
- When embeddings are enabled, the scorer:
  - embeds both summary and tags into vec0 tables;
  - normalizes vector distances via a logistic sigmoid over `1/(1+d)`;
  - splits the tag channel into semantic (vector) and lexical (FTS)
    parts, controlled by `CLAWSQLITE_TAG_VEC_FRACTION` and
    `CLAWSQLITE_TAG_FTS_LOG_ALPHA`.
- Final scores are a weighted sum of vec/fts/tag/priority/recency
  channels. Per-mode default weights are controlled by
  `CLAWSQLITE_SCORE_WEIGHTS_MODE1..4` (and legacy
  `CLAWSQLITE_SCORE_WEIGHTS*`).

See the upstream `ENV.example` and `README` in the `clawsqlite`
project root for details and recommended values for mixed
Chinese/English knowledge bases. Do **not** create a `.env` inside this
skill directory; configure env on the agent/host or in the upstream
project instead.

**Payload example:**

```json
{
  "action": "search",
  "query": "web scraping architecture",
  "mode": "hybrid",
  "topk": 10,
  "category": "idea",
  "tag": "crawler",
  "include_deleted": false,
  "root": "/home/node/.openclaw/workspace/knowledge_data"
}
```

Semantics:

- `mode=hybrid`:
  - If embeddings + vec table are available: use vec + FTS hybrid
  - If not: automatically downgrade to FTS‑only
- Filters by `category`, `tag`, optional `since`/`priority`

The result is a list of hits with `id`, `title`, `category`, `score`,
`created_at`, etc.

### 4.4 `show`

Retrieve a single record by id.

**Payload example:**

```json
{
  "action": "show",
  "id": 3,
  "full": true,
  "root": "/home/node/.openclaw/workspace/knowledge_data"
}
```

When `full=true`, the handler uses `clawsqlite knowledge show --full`
under the hood and returns the markdown content as well.

---

## 5. Error handling & NEXT hints

The underlying `clawsqlite` CLI is designed for agents and prints
navigation‑style error hints, e.g.:

```text
ERROR: db not found at /path/to/db. Check --root/--db or .env configuration.
NEXT: set --root/--db (or CLAWSQLITE_ROOT/CLAWSQLITE_DB) to an existing knowledge_data directory, or run an ingest command first to initialize the DB.
```

`run_clawknowledge.py` captures non‑zero exit codes and returns them in the
JSON response so agents can inspect and act on these hints.
It also surfaces `NEXT` hints as a structured `next` array and adds an
`error_kind` field so agents can decide the next action (e.g., missing
scraper, vec extension, or permissions).

---

## 6. When to use this skill vs. clawsqlite directly

Use **clawknowledge** when:

- You are inside ClawHub/OpenClaw and want a high‑level knowledge base
  skill for agents.
- You mostly need:
  - URL/text ingest
  - search
  - show
  - light maintenance

Use **clawsqlite (PyPI/CLI)** when:

- You want full flexibility over the knowledge DB and pipelines.
- You need plumbing commands like:
  - `clawsqlite db schema/exec/backup/vacuum`
  - `clawsqlite index check/rebuild`
  - `clawsqlite fs list-orphans/gc`
  - `clawsqlite embed column`
- You are writing new applications beyond a single personal KB.

### FTS/jieba fallback (CJK)

This skill relies on the underlying `clawsqlite` CLI for FTS tokenization.
When the CJK tokenizer extension `libsimple` cannot be loaded, `clawsqlite`
can switch to a jieba-based pre-segmentation mode controlled by
`CLAWSQLITE_FTS_JIEBA=auto|on|off`:

- `auto` (default): only enable when `libsimple` is unavailable **and** `jieba` is installed.
- `on`: force jieba pre-segmentation even if `libsimple` is available.
- `off`: disable jieba pre-segmentation.

In jieba mode, CJK text is segmented with jieba and joined with spaces before
being written to the FTS index; queries apply the same normalization so
write/rebuild/query stay consistent. English text is unaffected.

If you change this setting on an existing DB, rebuild the FTS index:

```bash
clawsqlite knowledge reindex --rebuild --fts
```

See the `clawsqlite` README for the full behavior and env matrix.

---

## 7. Upgrade notes (clawsqlite>=1.0.2)

- This Skill now depends on `clawsqlite>=1.0.2`; updates will install the new PyPI version via `bootstrap_deps.py`.
- In OpenClaw, a typical rollout is: `openclaw skills update clawsqlite-knowledge`, then rebuild FTS if you changed `CLAWSQLITE_FTS_JIEBA`.

## 8. Interest clusters & weekly reports (via underlying clawsqlite CLI)

This Skill deliberately keeps its JSON API small (ingest/search/show), but
it runs on top of the same SQLite DB and articles directory as the
full `clawsqlite knowledge` CLI.

If you want to analyze and report on your own interests over time, you can
use the **interest clusters** and **interest report** commands directly
against the same DB:

```bash
# Build or refresh interest clusters from existing embeddings
clawsqlite knowledge build-interest-clusters \
  --db /path/to/knowledge.sqlite3 \
  --min-size 5 \
  --max-clusters 16

# Inspect cluster quality (radius / distances / PCA plot)
clawsqlite knowledge inspect-interest-clusters \
  --db /path/to/knowledge.sqlite3 \
  --vec-dim 1024

# Generate a weekly interest report (Markdown + PNG, optional HTML/PDF)
clawsqlite knowledge report-interest \
  --db /path/to/knowledge.sqlite3 \
  --days 7 \
  --vec-dim 1024 \
  --lang zh \
  --format html \
  --out-dir /path/to/reports
```

The `report-interest` command will create a dated report directory under
`--out-dir` (default `./reports`):

- `report.md`  – a Markdown report describing:
  - total new articles and clusters touched in the window;
  - daily new article counts (table + PNG bar chart);
  - per-cluster distribution (size, share, mean_radius, sample articles);
  - a PCA 2D scatter plot of cluster centroids;
  - "heating / cooling" clusters compared to the previous window.
- `images/`    – PNG charts (`daily_articles.png`,
  `cluster_distribution.png`, `interest_clusters_pca.png`).
- optional `report.pdf` – a PDF generated via `pandoc report.md -o report.pdf`
  (best-effort; missing LaTeX will not cause the CLI to fail).
- optional `report.html` – when `--format html` is set and `pandoc` is
  available, a self-contained HTML report generated via:

  ```bash
  pandoc report.md -s -o report.html --mathjax --self-contained
  ```

This Skill does **not** expose interest cluster or report actions directly
in its JSON API. Instead, it stays focused on ingestion and retrieval,
while the underlying `clawsqlite` CLI provides the full cluster/report
tooling on the same knowledge base.
