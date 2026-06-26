---
name: clawfeedradar
description: Personal "news radar" skill built on top of a clawsqlite knowledge base and its interest clusters.
version: 0.1.0
metadata: {"openclaw":{"homepage":"https://github.com/ernestyu/clawfeedradar","tags":["news","rss","recommendation","clawsqlite"],"requires":{"bins":["python"],"env":[]},"install":[{"id":"clawfeedradar_bootstrap","kind":"bash","label":"Install clawfeedradar Python package","script":"bootstrap_deps.sh"}],"runtime":{"entry":"run_clawfeedradar.py"}}}
---

# clawfeedradar (OpenClaw Skill)

`clawfeedradar` is a **personal "news radar"** skill built on top of an
existing [clawsqlite](https://github.com/ernestyu/clawsqlite) knowledge
base and its interest clusters.

It answers one question:

> "Given what I have been reading / saving into clawsqlite, what new
>  articles on Hacker News / RSS / arXiv etc. am I likely to care about
>  today?"

The heavy lifting (interest clusters, embeddings, hybrid search) lives in
`clawsqlite`. This skill focuses on:

1. Fetching candidates from external sources (HN/RSS/etc.)
2. Scoring them against your **long‑term interest clusters** in clawsqlite
3. Generating per‑source RSS feeds (XML + JSON sidecar) with optional
   small‑LLM summaries and bilingual bodies

---

## 1. Relationship to clawsqlite & clawsqlite-knowledge

- **clawsqlite**
  - Maintains your knowledge base and interest clusters
  - Provides the `interest_clusters` + `interest_cluster_members` tables
  - Writes an `interest_meta` key
    `interest_clusters_last_built_at` after each cluster build

- **clawsqlite-knowledge (skill)**
  - High‑level ingest/search/show skill for OpenClaw agents
  - Runs on the same DB / articles directory as clawsqlite

- **clawfeedradar (this skill)**
  - Reads `interest_clusters` & `interest_meta` from the same DB
  - Never mutates the clawsqlite DB schema or articles
  - Uses the embedding config (EMBEDDING_* + CLAWSQLITE_VEC_DIM) shared
    with clawsqlite to embed candidate articles into the same interest
    space
  - Writes XML/JSON feeds to a separate `CLAWFEEDRADAR_OUTPUT_DIR`
  - Optionally publishes generated feeds to a git repository for
    GitHub/Gitee Pages

> In short: **clawsqlite knows what you like, clawfeedradar goes out and
> finds similar things, then packages them as RSS.**

---

## 2. Installation & bootstrap

This skill expects a Python runtime with access to PyPI (for the
`clawfeedradar` package) and a workspace where the skill lives under
`skills/clawfeedradar`.

### 2.1 Install the skill shell

```bash
openclaw skills install clawfeedradar
```

This will create:

```text
~/.openclaw/workspace/skills/clawfeedradar
  ├── SKILL.md
  ├── manifest.yaml
  ├── bootstrap_deps.sh
  ├── run_clawfeedradar.py
  ├── README.md
  ├── README_zh.md
  └── ENV_EXAMPLE.md
```

> Note: this skill does **not** read an `.env` inside the skill
> directory. All configuration lives in the upstream `clawfeedradar`
> project (or at the agent/host level), and the skill simply reuses that
> environment.

The actual Python package `clawfeedradar` is installed by the bootstrap
script, **not** vendored here.

### 2.2 Install / upgrade the clawfeedradar package

The `manifest.yaml` declares a bash bootstrap step:

```yaml
install:
  - id: clawfeedradar_bootstrap
    kind: bash
    label: Install clawfeedradar Python package
    script: bootstrap_deps.sh
```

`bootstrap_deps.sh` is a tiny wrapper around `python -m pip install` with
an optional workspace prefix fallback, similar to the pattern used by the
`clawsqlite-knowledge` skill.

In simplified form, it:

- Tries to install `clawfeedradar` into the default Python environment
  used by the skill;
- If that fails (read‑only env, no pip), tries again with
  `--prefix="$WORKSPACE/skills/clawfeedradar/.venv"`;
- Prints a `NEXT:` hint on success so you know where the package was
  installed and which `site-packages` will be added to `PYTHONPATH`.

You normally do not need to run this script manually; `openclaw skills
install clawfeedradar` (and a future `openclaw skills update
clawfeedradar`) will run it for you.

---

## 3. Runtime contract

The skill runtime calls `run_clawfeedradar.py` with a JSON payload on
stdin and expects a JSON response on stdout.

Common fields:

- `root` (optional): path to the clawsqlite knowledge root (if omitted,
  `CLAWSQLITE_ROOT` / `.env` defaults are used)
- `action`: one of the supported actions below

All handlers return a JSON object with at least:

- `ok: true|false`
- `data: ...` on success, or `error` / `exit_code` / `stdout` /
  `stderr` on failure
- `next: [...]` when the underlying CLI emits NEXT hints
- `error_kind` for coarse classification (e.g. missing embedding /
  scraper / vec ext)

Internally, the runtime:

- Ensures the workspace‑local site‑packages prefix is on `PYTHONPATH`;
- Executes `python -m clawfeedradar.cli ...` with the right arguments;
- Captures `stdout/stderr` and parses JSON when possible.

---

## 4. Supported actions

### 4.1 `run_once`

Run the radar once for a single source URL (HN/RSS/etc.), score
candidates against interest clusters, and write XML/JSON feeds.

**Payload example:**

```json
{
  "action": "run_once",
  "source_url": "https://feeds.bbci.co.uk/news/technology/rss.xml",
  "max_source_items": 30,
  "max_items": 12,
  "score_threshold": 0.4,
  "source_lang": "en",
  "target_lang": "zh",
  "enable_preview": true,
  "preview_words": 512,
  "root": "/home/node/.openclaw/workspace/knowledge_data"
}
```

**Behavior (high level):**

- Resolves the source type (HN / RSS / etc.) from `source_url`;
- Fetches up to `max_source_items` raw items from that source;
- Normalizes URLs and deduplicates using a 7‑day `seen_urls` statefile;
- Embeds each candidate into the same interest space as clawsqlite using
  the shared `EMBEDDING_*` + `CLAWSQLITE_VEC_DIM` config;
- Loads `interest_clusters` and warns if
  `interest_clusters_last_built_at` is older than 7 days;
- Computes an `interest_score_raw` for each candidate based on:

  ```text
  interest_raw = Σ_k (cluster_weight_k * max(0, sim_k))
  cluster_weight_k = size_k / Σ_j size_j
  ```

- Maps `interest_raw` into `[0,1]` via a sigmoid:

  ```text
  interest_score = sigmoid(k*(interest_raw - 0.5))
  k = CLAWFEEDRADAR_INTEREST_SIGMOID_K (default 4.0)
  ```

- Adds a small bias from recency and popularity:

  ```text
  interest_bias = w_recency * rec + w_popularity * pop
  ```

  where `rec`/`pop` are in `[0,1]` and weights are controlled by
  `CLAWFEEDRADAR_W_RECENCY` / `CLAWFEEDRADAR_W_POPULARITY`.

- Computes `final_score ≈ interest_score + interest_bias + source_extras`;
- Filters by `score_threshold` and picks up to `max_items` top
  candidates;
- Fetches fulltext for the selected items (per‑host serial, cross‑host
  parallel);
- Optionally calls a small LLM to generate:
  - `summary_preview` (preview summary, controlled by
    `preview_words` / `CLAWFEEDRADAR_LLM_CONTEXT_TOKENS`)
  - `body_bilingual` (bilingual body paragraphs, controlled by
    `CLAWFEEDRADAR_LLM_MAX_PARAGRAPH_CHARS` and lang env);
- Writes:
  - `<OUTPUT_DIR>/<slug>.xml` — RSS feed for your reader;
  - `<OUTPUT_DIR>/<slug>.json` — JSON sidecar with full debug info
    (scores, cluster matches, fulltext, bilingual body, etc.).

If publishing to git is configured (see `ENV_EXAMPLE.md`), the runtime
will also update a remote git repo (GitHub/Gitee) so you can subscribe
via Pages.

**Return value:** a JSON object with a summary of the run (number of
candidates, selected items, output paths, warnings if any).

### 4.2 `schedule_from_sources_json`

Run the radar for multiple sources defined in a `sources.json` file.

This is a higher‑level wrapper around `run_once` that:

- Reads a sources JSON (same shape as the clawfeedradar CLI);
- Iterates over enabled sources, applying per‑source config
  (max_items/threshold/lang/etc.);
- Aggregates results and returns a summary per source.

**Payload example:**

```json
{
  "action": "schedule_from_sources_json",
  "sources_file": "/home/node/.openclaw/workspace/clawfeedradar/sources.json",
  "root": "/home/node/.openclaw/workspace/knowledge_data"
}
```

The exact JSON shape for `sources.json` is documented in the
clawfeedradar README/SPEC; this skill does not invent a new format.

---

## 5. ENV configuration (summary)

This skill itself does not read a `.env` file; it relies on the
underlying `clawfeedradar` and `clawsqlite` CLIs, which support
project‑level `.env` files.

In OpenClaw deployments you typically configure env vars at the agent
(or host) level so both skills and direct CLI usage share the same
configuration.

Key envs (see `ENV_EXAMPLE.md` for a consolidated list):

- Knowledge base
  - `CLAWSQLITE_ROOT` / `CLAWSQLITE_DB`
- Embedding service
  - `EMBEDDING_BASE_URL` / `EMBEDDING_MODEL` / `EMBEDDING_API_KEY`
  - `CLAWSQLITE_VEC_DIM`
- Interest clusters (configured on clawsqlite side)
  - `CLAWSQLITE_INTEREST_*` (algo, PCA, min_size, max_clusters, etc.)
- Fulltext fetch
  - `CLAWFEEDRADAR_SCRAPE_CMD`
  - `CLAWFEEDRADAR_SCRAPE_WORKERS`
- LLM summaries / bilingual body
  - `SMALL_LLM_*`
  - `CLAWFEEDRADAR_LLM_*` (context tokens, paragraph size, sleep,
    source/target lang)
- Scoring
  - `CLAWFEEDRADAR_INTEREST_SIGMOID_K`
  - `CLAWFEEDRADAR_W_RECENCY` / `CLAWFEEDRADAR_W_POPULARITY`
  - `CLAWFEEDRADAR_RECENCY_HALF_LIFE_DAYS`
- Output & publish
  - `CLAWFEEDRADAR_OUTPUT_DIR`
  - `CLAWFEEDRADAR_PUBLISH_GIT_REPO` /
    `CLAWFEEDRADAR_PUBLISH_GIT_BRANCH` /
    `CLAWFEEDRADAR_PUBLISH_GIT_PATH`

---

## 6. When to use this skill

Use **clawfeedradar (skill)** when:

- You already have a clawsqlite knowledge base with interest clusters;
- You want an agent‑friendly way to:
  - run daily/weekly news radar jobs;
  - generate and publish personalized RSS feeds;
  - inspect scores / clusters per article via JSON.

Use **clawfeedradar (CLI)** when:

- You are developing or debugging the radar itself;
- You want full control over CLI flags / env without going through the
  skill JSON API.

Both run against the same clawsqlite DB and can coexist.

---

## 7. Security & limits

- This skill does **not** modify the clawsqlite DB schema or articles;
- It only reads embeddings and interest cluster metadata;
- All external network requests (feeds, fulltext, LLM, git) are made via
  the underlying `clawfeedradar` CLI and are fully auditable.

If you need stricter control (e.g. only allow certain sources, or
completely disable publishing), you can wrap this skill with your own
policy layer or restrict env/config at the agent level.

---

For full implementation details (candidate model, scoring formula, LLM
pipelines), see the upstream
[clawfeedradar docs](https://github.com/ernestyu/clawfeedradar/tree/main/docs).

In particular:

- `docs/SPEC_en.md` / `docs/SPEC_zh.md`: formal spec for the pipeline
- `README.md` / `README_zh.md`: human‑oriented overview and usage
instructions
