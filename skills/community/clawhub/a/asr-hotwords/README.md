# ASR Hotwords

An OpenClaw skill that automatically mines hotwords and ambiguous terms from all OpenClaw agent conversation histories using a local NLP pipeline (jieba + fuzzy pinyin + LLM refinement).

## Overview

ASR (Automatic Speech Recognition) systems often misrecognize domain-specific terms, proper nouns, and niche vocabulary. This tool extracts conversation data from **all** OpenClaw agent sessions and runs a local hotword mining pipeline to build a unified disambiguation vocabulary table.

The generated hotword table (`hotwords.md`) can be directly injected into ASR model prompts (e.g., Qwen2.5-Omni) to improve transcription accuracy.

**Pipeline:**

```
All OpenClaw Sessions (.jsonl) → Extract & Filter → Local Mining (jieba + LLM) → Vocabulary Table → hotwords.md
```

## Features

- **Fully local processing** — All mining runs locally; API key is only used to call your configured LLM directly, never sent to third-party servers
- **Global hotword table** — Scans all agents' sessions, builds a unified vocabulary
- **Smart filtering** — Skips system noise (cron tasks, heartbeats, sub-agent metadata, NO_REPLY, pure English, URLs, code blocks)
- **Incremental anchors** — Loads all historical vocab results as anchors, vocabulary only grows
- **Zero-config credentials** — Reads LLM API key, base URL, and model from `~/.openclaw/openclaw.json` automatically
- **UTC→CST date handling** — Correctly filters messages by CST date, not UTC
- **Safe re-runs** — Automatically backs up previous results when re-running the same date
- **Multiple export formats** — txt, json, csv, prompt (for ASR injection)

## Project Structure

```
asr-hotwords/
├── README.md               # This file
├── SKILL.md                # OpenClaw skill instructions & install wizard
├── config.yaml             # Configuration
├── build_words.py          # Core mining engine (jieba + fuzzy pinyin + LLM)
├── extract_sessions.py     # Session data extraction module
├── run.py                  # Main pipeline controller (includes export)
├── run.sh                  # Shell entry point
├── requirements.txt        # Python dependencies
└── output/                 # Mining results archive (git-ignored)
    └── vocab_YYYY-MM-DD.json
```

## Prerequisites

- Python 3.9+
- OpenClaw installed with session history in `~/.openclaw/agents/`

**Python dependencies:**

```bash
pip install -r requirements.txt
```

Dependencies: `pyyaml`, `jieba`, `pypinyin`, `openai`, `anthropic`

## Installation

Install to `~/.openclaw/skills/asr-hotwords/`:

```bash
# Install via ClawHub
clawhub install asr-hotwords
```

See `SKILL.md` for the full installation wizard.

## Quick Start

```bash
# Mine yesterday's conversations (default, background)
nohup bash run.sh > run.log 2>&1 &

# Mine a specific date
nohup bash run.sh --date 2026-04-26 > run.log 2>&1 &

# Mine a date range
nohup bash run.sh --start 2026-04-20 --end 2026-04-26 > run.log 2>&1 &

# Export only (no mining, runs instantly)
bash run.sh --export-only -f prompt -o hotwords.md
```

## Configuration

Edit `config.yaml`:

```yaml
extract:
  agents: ["*"]               # ["*"] = all agents, or specify ["main", "claude"]
  max_content_len: 300        # Max chars per message (truncates beyond)
  min_freq: 3                 # Minimum word frequency threshold
```

### Credential Resolution

LLM API key, base URL, and model are **automatically** resolved from `~/.openclaw/openclaw.json`:

```
agents.defaults.model.primary → "provider/model_id"
    ↓
models.providers.{provider} → apiKey, baseUrl, api format
```

No manual API key or model configuration is needed.

## How It Works

### 1. Session Extraction (`extract_sessions.py`)

Scans `~/.openclaw/agents/*/sessions/*.jsonl` files and extracts `user`/`assistant` message pairs for the target date(s) from all agents.

**Filtering rules:**
- Only `type: "message"` with `role: "user"` or `role: "assistant"`
- UTC timestamps converted to CST before date comparison
- Skips: NO_REPLY, HEARTBEAT_OK, cron contexts, sub-agent metadata, system internals, pure JSON, code blocks, pure English (no Chinese characters), URLs
- Files with mtime before target date are skipped entirely (fast path)
- Messages truncated to `max_content_len` characters
- Output format: `发送者：内容` (one message per line)

### 2. Anchor Loading

Loads all `output/vocab_*.json` files (excluding `.bak` backups), merges by term with deduplication. Vocabulary only grows over time — terms discovered in earlier runs are never lost.

### 3. Local Mining (`build_words.py`)

Runs a 5-stage pipeline locally:

1. **Data Preparation** — Parse chat + load anchors + build fuzzy pinyin index
2. **Data Cleaning** — Rule-based pre-analysis + LLM correction
3. **Statistical Filter** — Word frequency + fuzzy pinyin collision detection
4. **LLM Refinement** — Review + supplement + mixed Chinese/English + scene description
5. **Validation** (optional) — Reverse injection testing

All LLM calls go directly to your configured provider.

### 4. Export (integrated in `run.py`)

`run.py` automatically exports `hotwords.md` after mining. For standalone export:

```bash
bash run.sh --export-only -f prompt -o hotwords.md
```

**Supported formats:**

| Format | Command | Use Case |
|--------|---------|----------|
| `prompt` | `-f prompt -o hotwords.md` | Direct ASR prompt injection |
| `json` | `-f json -o hotwords.json` | Programmatic access |
| `csv` | `-f csv -o hotwords.csv` | Human review / spreadsheet |
| `txt` | `-f txt` | Simple word list |

### 5. ASR Integration

The generated `hotwords.md` is in prompt format, ready to be injected into ASR model system prompts:

```
产品术语：飞书、OpenClaw、ClawHub
技术术语：VLA、持久化、多模态
人名：小苝
易混淆词：飞书/飞鼠、VLA/微辣
```

## Modules

### `extract_sessions.py`

Standalone module for OpenClaw session data extraction.

```bash
python3 extract_sessions.py --date 2026-04-26 --output chat.txt
python3 extract_sessions.py --start 2026-04-20 --end 2026-04-26 --agents main claude
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--date` | Yesterday | Target date (YYYY-MM-DD) |
| `--start` | - | Start date for range |
| `--end` | - | End date for range |
| `--agents` | `*` (all) | Agent names to extract |
| `--max-len` | 300 | Max characters per message |
| `--output` | stdout | Output file path |

### `run.py`

Main pipeline controller.

```bash
python3 run.py --date 2026-04-26
python3 run.py --start 2026-04-20 --end 2026-04-26
python3 run.py --export-only -f prompt -o hotwords.md
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--date` | Yesterday | Target date |
| `--start` | - | Start date for range |
| `--end` | - | End date for range |
| `--export-only` | - | Export only, no mining |
| `-f, --format` | `prompt` | Export format: txt, json, csv, prompt |
| `-o, --output` | stdout | Export file path |
| `--min-freq` | 1 | Minimum frequency filter |

## License

Internal use only.
