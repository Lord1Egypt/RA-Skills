# duru-memory

A production-ready markdown memory skill for OpenClaw with:

- Hybrid retrieval (keyword + semantic embedding)
- Local semantic index (`SQLite + sqlite-vec`)
- Incremental embedding cache
- RRF re-ranking with keyword and directory priors
- Negative-memory safeguards (`⚠ Avoided Pitfalls`)
- Local auto-tagging via `qwen3.5:2b`
- Retention lifecycle (hot/warm/cold)
  - weekly compaction
  - monthly archive/forget

## Repository Structure

```text
.
├── SKILL.md
├── LICENSE
├── README.md
├── references/
└── scripts/
```

## Install in OpenClaw

From your OpenClaw workspace:

```bash
mkdir -p skills/duru-memory
cp -R <this-repo>/* skills/duru-memory/
```

Or clone this repository into your workspace `skills/` directory directly:

```bash
git clone https://github.com/DuruGY/duru-memory.git skills/duru-memory
```

Recommended first-time setup order:

```bash
cd skills/duru-memory
uv sync
cp config.example.yaml config.yaml
ollama pull qwen3-embedding:0.6b
ollama pull gemma4:e4b
```

## Prerequisites

Before using this skill, make sure these are installed on your machine:

- `uv` (for the skill's isolated Python environment)
- `Ollama` (required for local embedding / tagging / compaction model calls)
- Python 3.11+

Notes:

- `sqlite-vec` and `apsw` are Python dependencies managed by `uv`, so you do not need to install them separately if `uv sync` succeeds.
- This skill stores its semantic index in local SQLite files under `memory/`.

## Runtime Setup

This skill uses a dedicated `uv` environment.

```bash
cd skills/duru-memory
uv sync
```

Then prepare your local config:

```bash
cp config.example.yaml config.yaml
```

Then make sure the required Ollama models are available locally:

```bash
ollama pull qwen3-embedding:0.6b
ollama pull gemma4:e4b
```

Ollama models are configurable via `config.yaml`.

Default setup:

- `qwen3-embedding:0.6b` (semantic retrieval)
- `gemma4:e4b` (auto-tagging / compaction suggestions)

## Configuration

Default shared config template:

```text
config.example.yaml
```

Create your local private config:

```bash
cp config.example.yaml config.yaml
```

`config.yaml` is gitignored and intended for your actual local settings.

Example knobs:
- `ollama.base_url`
- `models.embedding`
- `models.tagger`
- `models.compact`
- `semantic.min_score`
- `fusion.mode`

CLI args still override config values.

## Key Scripts

- `scripts/memory-search.sh` — hybrid search entrypoint
- `scripts/memory-semantic-search.py` — SQLite + sqlite-vec semantic retrieval
- `scripts/memory-auto-tag.py` — incremental auto-tagging (`tag`/`review` modes)
- `scripts/memory-write-tag.sh` — write + immediate tagging helper
- `scripts/memory-compact.py` — weekly compaction
- `scripts/memory-forget.py` — monthly archive/forget
- `scripts/session-start.sh` — startup helper
- `scripts/session-close.sh` — close helper

## Suggested Scheduling

- Daily: auto-tag review
- Weekly: compaction (`daily -> summaries`)
- Monthly: archive old stale entries

## Safety Model

- Do not use negative memory as execution basis.
- Surface negative matches as warnings.
- Keep retention actions auditable.
- Prefer review mode over aggressive overwrite.

---

If you use this in production, keep token/credential material out of memory files and rotate any GitHub/Ollama secrets regularly.
