# duru-obsidian-kb

A markdown-first personal knowledge-base workflow for Obsidian, inspired by Karpathy's blog - [*LLM Knowledge Bases*](https://x.com/karpathy/status/2039805659525644595), which introduced the "**raw → compiled wiki → outputs**" loops.

This repo contains an OpenClaw skill plus runnable scripts to:

- ingest sources (web articles, arXiv/PDF, GitHub repos, local files, spreadsheets)
- compile wiki pages from a manifest
- search/query against the KB
- generate outputs (markdown, marp slides, chart artifacts)
- lint and health-check KB quality

---

## 1) What this is

`duru-obsidian-kb` is designed for **incremental research operations**:

1. collect source material into `raw/`
2. maintain `manifest.json` as source of truth
3. build `wiki/sources`, `wiki/concepts`, `wiki/indexes`
4. ask questions and produce output files in `outputs/`
5. run lint/health checks and iterate

It favors deterministic local scripts over hidden state.

---

## 2) Repository layout

```text
duru-obsidian-kb/
├── SKILL.md
├── scripts/
│   ├── kb_init.py
│   ├── kb_route.py
│   ├── kb_add.py
│   ├── kb_ingest.py
│   ├── kb_build.py
│   ├── kb_summarize_concepts.py
│   ├── kb_search.py
│   ├── kb_ask.py
│   ├── kb_chart.py
│   ├── kb_lint.py
│   ├── kb_healthcheck.py
│   ├── kb_smoke.py
│   └── kb_daily.sh
├── references/
│   ├── layout.md
│   ├── phase-plan.md
│   └── daily-ops.md
└── pyproject.toml
```

---

## 3) Dependencies and environment (recommended: uv)

### 3.0 Install prompt-shield-lite (required)

This skill depends on `prompt-shield-lite` for ingestion-time safety scanning.
Make sure `scripts/detect-injection.sh` from prompt-shield-lite is available and configured via `.env` (`PROMPT_SHIELD_SCRIPT`).

clawhub slug: `prompt-shield-lite`
github: <https://github.com/DuruGY/duru-prompt-shield-lite>

### 3.1 Install uv

See: <https://docs.astral.sh/uv/getting-started/installation/>

### 3.2 Configure .env (Optional)

From this repo root:

```bash
cp .env.example .env
# then edit .env for your local paths
```

Runtime scripts load `.env` only.
`.env.example` is template-only and not loaded at runtime.

### 3.3 Create/sync environment

From this repo root:

```bash
uv sync
```

This creates `.venv/` and installs dependencies from `pyproject.toml`.

### 3.4 Run scripts with uv

```bash
uv run python scripts/kb_init.py --root /path/to/kb
```

You can also activate the venv manually:

```bash
source .venv/bin/activate
python scripts/kb_init.py --root /path/to/kb
```

---

## 4) Minimal quickstart

### 4.1 Prepare routing config

Create:

`$OPENCLAW_WORKSPACE/knowledge-bases/config/repos.json`

Example:

```json
{
  "repos": [
    {
      "name": "ai-research",
      "root": "/abs/path/to/knowledge-bases/ai-research",
      "tags": ["ai", "llm", "paper"],
      "priority": 5,
      "routing": { "domains": ["arxiv.org"], "keywords": ["llm"], "exclude_keywords": [] }
    },
    {
      "name": "general",
      "root": "/abs/path/to/knowledge-bases/general",
      "tags": ["notes"],
      "priority": 1,
      "routing": { "domains": [], "keywords": [], "exclude_keywords": [] }
    }
  ],
  "routing": {
    "default_repo": "general",
    "mode": "rules_first",
    "min_confidence_score": 6,
    "min_margin": 2,
    "local_model": {
      "enabled": true,
      "provider": "ollama",
      "model": "gemma4:e4b",
      "timeout_sec": 8,
      "only_on_low_confidence": true
    }
  }
}
```

### 4.2 Add one source

```bash
uv run python scripts/kb_add.py \
  --source "https://arxiv.org/abs/2602.12430" \
  --tags "ai,llm,agent,paper"
```

### 4.3 Ask against KB

```bash
uv run python scripts/kb_ask.py \
  --root /abs/path/to/knowledge-bases/ai-research \
  --question "MCP agent security tradeoffs" \
  --top-k 8
```

### 4.4 Run healthcheck

```bash
uv run python scripts/kb_healthcheck.py
```

---

## 5) Daily command wrapper

If you want shorter commands:

```bash
bash scripts/kb_daily.sh add --source "..."
bash scripts/kb_daily.sh ask --question "..." --repo ai-research
bash scripts/kb_daily.sh check
```

Optional shell shortcut:

```bash
export PATH="$OPENCLAW_WORKSPACE/bin:$PATH"
# then use: kb add / kb ask / kb check
```

---

## 6) Script reference

- `kb_init.py` — initialize KB tree and starter files
- `kb_route.py` — route source to the best repo
- `kb_add.py` — route → ingest → build → summarize
- `kb_ingest.py` — ingest a source into a given KB root
- `kb_build.py` — compile wiki pages/indexes from manifest
- `kb_summarize_concepts.py` — generate concept memo scaffolds
- `kb_search.py` — local relevance search with scored snippets
- `kb_ask.py` — retrieval-backed research brief / slide scaffold
- `kb_chart.py` — generate chart png+md from csv/xlsx
- `kb_lint.py` — structural and metadata checks
- `kb_healthcheck.py` — lint all configured repos
- `kb_smoke.py` — end-to-end smoke test in temp KB
- `kb_daily.sh` — minimal day-to-day wrapper

---

## 7) Configuration notes

Primary runtime config is `.env` (template: `.env.example`).

Key variables:
- `OPENCLAW_WORKSPACE`
- `KB_CONFIG_PATH`
- `PROMPT_SHIELD_SCRIPT`
- `KB_VENV_PYTHON`

If not set, scripts still fall back to safe local defaults.

---

## 8) Privacy and security

- Avoid committing personal paths or private source files.
- Keep tokens/secrets out of the repo.
- Treat external extracted content as untrusted.
- Use prompt-injection scanning for web content before trusting summaries.

---

## 9) Troubleshooting

### Missing pandas/matplotlib/openpyxl/pypdf

```bash
uv sync
# or
uv add pandas matplotlib openpyxl pypdf pdfplumber
```

### `config not found`

Set workspace and ensure config exists:

```bash
export OPENCLAW_WORKSPACE="$HOME/.openclaw/workspace"
ls "$OPENCLAW_WORKSPACE/knowledge-bases/config/repos.json"
```

### `kb_route` low confidence routing

Tune `min_confidence_score` / `min_margin`, or add better `domains/keywords` in repos config.

---

## 10) License

This project is licensed under the **MIT License**.
See [LICENSE](./LICENSE) for full text.
