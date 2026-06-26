# ASR Personal Hotwords

An OpenClaw skill that automatically mines personalized hotwords and ambiguous terms from OpenClaw conversation histories, powered by the [asr-corrector](https://github.com/asr-corrector) service.

## Overview

ASR (Automatic Speech Recognition) systems often misrecognize domain-specific terms, proper nouns, and niche vocabulary. This tool extracts conversation data from OpenClaw agent sessions and feeds it into a hotword mining pipeline to build a **per-agent personalized** disambiguation vocabulary table.

The generated hotword table (`hotwords.md`) can be directly injected into ASR model prompts (e.g., Qwen2.5-Omni) to improve transcription accuracy.

**Pipeline:**

```
OpenClaw Sessions (.jsonl) → Extract & Filter → asr-corrector API → Vocabulary Table → hotwords.md
```

## Features

- **Per-agent isolation** — Each agent maintains its own hotword table; `["self"]` mode auto-detects the current agent from skill path + `openclaw.json`
- **Smart filtering** — Skips system noise (cron tasks, heartbeats, sub-agent metadata, NO_REPLY, pure English, URLs, code blocks)
- **Incremental anchors** — Loads **all** historical vocab results as anchors (not just the latest), vocabulary only grows
- **Auto-chunking** — Splits large data into API-compliant chunks (≤400 lines / ≤10,000 chars) and merges results with deduplication
- **Zero-config credentials** — Reads LLM API key, base URL, and model from `~/.openclaw/openclaw.json` automatically
- **UTC→CST date handling** — Correctly filters messages by CST date, not UTC
- **HTTP retry** — 3 retries with exponential backoff for 502/503/504 errors
- **Safe re-runs** — Automatically backs up previous results when re-running the same date
- **Multiple export formats** — txt, json, csv, prompt (for ASR injection)

## Project Structure

```
asr-personal-hotwords/
├── README.md               # This file
├── SKILL.md                # OpenClaw skill instructions & install wizard
├── config.yaml             # Configuration
├── extract_sessions.py     # Session data extraction module
├── run.py                  # Main pipeline controller (includes export)
├── run.sh                  # Shell entry point
├── hotwords.md             # Generated hotword table (git-ignored)
└── output/                 # Mining results archive (git-ignored)
    └── vocab_YYYY-MM-DD.json
```

## Prerequisites

- Python 3.9+
- A running [asr-corrector](https://github.com/asr-corrector) service
- OpenClaw installed with session history in `~/.openclaw/agents/`

**Python dependencies:**

```bash
pip install requests pyyaml
```

## Installation

This skill is designed to be installed **per-agent** in the agent's workspace:

1. Determine the agent's workspace from `~/.openclaw/openclaw.json` (`agents.list[].workspace` or `agents.defaults.workspace`)
2. Install to `{workspace}/skills/asr-personal-hotwords/`

```bash
# Install to agent workspace
clawhub install asr-personal-hotwords
```

See `SKILL.md` for the full 7-step installation wizard.

## Quick Start

```bash
# Mine yesterday's conversations (default)
bash run.sh

# Mine a specific date
bash run.sh --date 2026-04-26

# Mine a date range
bash run.sh --start 2026-04-20 --end 2026-04-26

# Export hotword table only (no mining)
bash run.sh --export-only -f prompt -o hotwords.md
```

## Configuration

Edit `config.yaml`:

```yaml
# Remote asr-corrector service
server_url: "http://124.174.11.138:65000"

# Extraction settings
extract:
  agents: ["self"]            # ["self"] = auto-detect, ["*"] = all, or ["main", "claude"]
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

Scans `~/.openclaw/agents/{agent}/sessions/*.jsonl` files and extracts `user`/`assistant` message pairs for the target date(s).

**Agent resolution (`["self"]` mode):**
1. Infers workspace path from the skill's file location
2. Looks up `~/.openclaw/openclaw.json` to find the matching agent by workspace path
3. Falls back to `OPENCLAW_AGENT_NAME` env var, then `"main"`

**Filtering rules:**
- Only `type: "message"` with `role: "user"` or `role: "assistant"`
- UTC timestamps converted to CST before date comparison
- Skips: NO_REPLY, HEARTBEAT_OK, cron contexts, sub-agent metadata, system internals, pure JSON, code blocks, pure English (no Chinese characters), URLs
- Files with mtime before target date are skipped entirely (fast path)
- Messages truncated to `max_content_len` characters
- Output format: `发送者：内容` (one message per line)

### 2. Anchor Loading

Loads **all** `output/vocab_*.json` files (excluding `.bak` backups), merges by term with deduplication. This ensures the vocabulary only grows over time — terms discovered in earlier runs are never lost.

### 3. API Submission (`run.py`)

Chat data is submitted to the asr-corrector service's `/api/build-vocab` endpoint. If data exceeds API limits, it is automatically split into chunks. Each chunk is submitted as a separate task, polled for completion, and results are merged with deduplication and frequency aggregation.

**Reliability:**
- HTTP requests use a retry-enabled session (3 retries, exponential backoff, 502/503/504)
- Task polling with configurable timeout (default 600s)
- Same-date re-runs automatically back up previous results

### 4. Export (integrated in `run.py`)

`run.py` automatically exports `hotwords.md` after mining. For standalone export:

```bash
bash run.sh --export-only -f prompt -o hotwords.md
```

Merges all historical vocab files and exports a clean hotword table.

**Supported formats:**

| Format | Command | Use Case |
|--------|---------|----------|
| `prompt` | `bash run.sh --export-only -f prompt -o hotwords.md` | Direct ASR prompt injection |
| `json` | `bash run.sh --export-only -f json -o hotwords.json` | Programmatic access |
| `csv` | `bash run.sh --export-only -f csv -o hotwords.csv` | Human review / spreadsheet |
| `txt` | `bash run.sh --export-only -f txt` | Simple word list |

Entries with both empty `desc` and empty `possible_asr_errors` are automatically filtered out.

### 5. ASR Integration

The generated `hotwords.md` is in prompt format, ready to be injected into ASR model system prompts:

```
以下是用户场景中的专有名词和易混淆词汇表。
语音转录时，如果听到与「常见误识别」列发音相近的内容，请优先转录为「正确词」列的写法。

| 正确词 | 常见误识别 |
|--------|-----------|
| 飞书 | 飞鼠、非书、肥书 |
| VLA | 微辣、微拉、为了啊 |
| 持久化 | 持酒话、迟就化 |
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
```

| Argument | Default | Description |
|----------|---------|-------------|
| `--date` | Yesterday | Target date |
| `--start` | - | Start date for range |
| `--end` | - | End date for range |

### `run.py --export-only`

Standalone hotword table export.

```bash
bash run.sh --export-only -f prompt -o hotwords.md
bash run.sh --export-only -f json --min-freq 3
```

| Argument | Default | Description |
|----------|---------|-------------|
| `-f, --format` | `prompt` | Output format: txt, json, csv, prompt |
| `-o, --output` | stdout | Output file path |
| `--output-dir` | `./output` | Vocab files directory |
| `--min-freq` | 1 | Minimum frequency filter |

## Example Output

```
$ bash run.sh --date 2026-04-26

18:07:54 INFO 从 openclaw.json 自动读取 LLM 配置...
18:07:54 INFO   Model: claude-opus-4-6, Format: anthropic
18:07:54 INFO 检查远端服务 http://124.174.11.138:65000...
18:07:54 INFO   服务正常 ✓
18:07:54 INFO 提取对话: 2026-04-26 ~ 2026-04-26 (agents: ['self'])
18:07:54 INFO 自动识别当前 agent: main
18:07:54 INFO 扫描 10 个文件, 2 个匹配, 提取 3 条消息
18:07:54 INFO 从 2 个历史文件加载 91 个 anchors（去重后）
18:08:33 INFO 块 1 完成: 100 条热词
18:08:33 INFO 结果保存到: output/vocab_2026-04-26.json

{
  "status": "success",
  "date": "2026-04-26",
  "messages_count": 3,
  "vocab_count": 100,
  "top_terms": [
    {"term": "飞书", "freq": 2, "asr_errors": ["飞鼠", "飞输", "非书"]},
    {"term": "机器之心", "freq": 2, "asr_errors": ["机器知心", "机器之新"]},
    {"term": "反爬虫", "freq": 2, "asr_errors": ["反扒虫", "翻爬虫"]}
  ]
}
```

## License

Internal use only.
