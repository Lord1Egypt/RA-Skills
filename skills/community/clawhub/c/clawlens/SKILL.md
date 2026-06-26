---
name: clawlens
description: What do you use Claw for most? Where do you get stuck? Clawlens analyzes your conversation history to surface usage patterns, friction points, and skill effectiveness — your personal OpenClaw retrospective.
user-invocable: true
dependencies:
  - litellm
  - markdown
required-env:
  - DEEPSEEK_API_KEY or OPENAI_API_KEY or ANTHROPIC_API_KEY (only when --model is specified manually; not needed for auto-detect)
reads:
  - ~/.openclaw/agents/{agentId}/sessions/sessions.json
  - ~/.openclaw/agents/{agentId}/sessions/*.jsonl
  - ~/.openclaw/skills/
  - ~/.openclaw/openclaw.json
  - ~/.openclaw/agents/{agentId}/agent/auth-profiles.json
writes:
  - ~/.openclaw/agents/{agentId}/sessions/.clawlens-cache/
external-api:
  - LLM provider specified by --model via litellm (sends conversation transcript summaries for analysis)
---

# Clawlens - OpenClaw Usage Insights

Generate a comprehensive usage insights report by analyzing conversation history.

## When to Use

| User Says | Action |
|-----------|--------|
| "show me my usage report" | Run full report |
| "analyze my conversations" | Run full report |
| "how am I using Claw" | Run full report |
| "clawlens" / "claw lens" | Run full report |
| "usage insights" / "usage analysis" | Run full report |

## How to Run

Execute the analysis script:

```bash
python3 scripts/clawlens.py [OPTIONS]
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--agent-id` | `main` | Agent ID to analyze |
| `--days` | `180` | Analysis time window in days |
| `--model` | auto-detect | LLM model in litellm format (e.g. `deepseek/deepseek-chat`). If omitted, auto-detected from OpenClaw config. |
| `--lang` | `zh` | Report language: `zh` or `en` |
| `--format` | `md` | Output format: `md` (Markdown) or `html` (self-contained dark-themed HTML) |
| `--no-cache` | false | Ignore cached facet extraction results |
| `--max-sessions` | `2000` | Maximum sessions to process |
| `--concurrency` | `10` | Max parallel LLM calls |
| `--verbose` | false | Print progress to stderr |
| `-o` / `--output` | stdout | Output file path |

### Model Selection (Agent Interaction)

When the user requests a clawlens report without specifying a model, **you must ask the user before running**:

> 是否使用 OpenClaw 当前配置的模型来生成报告？如果不使用，请告诉我你想用的模型（litellm 格式，如 `deepseek/deepseek-chat`）。

- **User agrees to use OpenClaw model**: Run **without** `--model` (the script auto-detects from `~/.openclaw/openclaw.json`).
- **User specifies a different model**: Run with `--model <user-choice>`. The user must also set the corresponding API key env var (e.g. `DEEPSEEK_API_KEY`).

Note: Each user's OpenClaw model configuration may differ — some use API-key-based providers (e.g. `openai-completions`), others use OAuth-based providers (e.g. `anthropic-messages`). The script handles both transparently.

### Examples

```bash
# Auto-detect model from OpenClaw config (simplest)
python3 scripts/clawlens.py --verbose

# Auto-detect, English, last 7 days
python3 scripts/clawlens.py --lang en --days 7

# Manually specify model (DeepSeek)
DEEPSEEK_API_KEY=sk-xxx python3 scripts/clawlens.py --model deepseek/deepseek-chat

# OpenAI, English, last 7 days
OPENAI_API_KEY=sk-xxx python3 scripts/clawlens.py --model openai/gpt-4o --lang en --days 7

# Verbose, save to file
ANTHROPIC_API_KEY=sk-xxx python3 scripts/clawlens.py --model anthropic/claude-sonnet-4-20250514 --verbose -o /tmp/clawlens-report.md

# HTML report (dark-themed, self-contained)
DEEPSEEK_API_KEY=sk-xxx python3 scripts/clawlens.py --model deepseek/deepseek-chat --format html -o /tmp/clawlens-report.html
```

## Output

The script outputs a report to stdout (or to the file specified by `-o`). Progress messages go to stderr when `--verbose` is set.

- **Markdown** (`--format md`, default): Plain Markdown report. Present it directly to the user.
- **HTML** (`--format html`): Self-contained dark-themed HTML file with glassmorphism styling, animated stat cards, CSS bar charts, and interactive navigation. Opens directly in any browser — no external dependencies. Requires the `markdown` Python package for Markdown-to-HTML conversion.

The report includes all dimensions: usage overview, task classification, friction analysis, skills ecosystem, autonomous behavior audit, and multi-channel analysis.

**Present the output directly to the user.** Do not summarize or truncate it.

## Model Configuration

`--model` is optional. If omitted, the model is automatically resolved from OpenClaw configuration:

1. Reads primary model from `~/.openclaw/openclaw.json` (`agents.defaults.model.primary`, e.g. `kimi-code/kimi-for-coding`)
2. Looks up the provider's `baseUrl` and `api` type (e.g. `openai-completions`, `anthropic-messages`)
3. Retrieves API key/token from `~/.openclaw/agents/{agentId}/agent/auth-profiles.json`
4. Maps to litellm format automatically (e.g. `openai/kimi-for-coding` with custom `api_base`)

If you prefer to specify a model manually, use `--model` with [litellm's provider format](https://docs.litellm.ai/docs/providers):

| Provider | `--model` value | Required env var |
|----------|----------------|------------------|
| DeepSeek | `deepseek/deepseek-chat` | `DEEPSEEK_API_KEY` |
| OpenAI | `openai/gpt-4o` | `OPENAI_API_KEY` |
| Anthropic | `anthropic/claude-sonnet-4-20250514` | `ANTHROPIC_API_KEY` |
| OpenAI-compatible | `openai/<model-id>` + set `OPENAI_API_BASE` | `OPENAI_API_KEY` |

The format is always `<provider>/<model-id>`. Refer to litellm docs for the full list of supported providers and their env var naming conventions.

## Data Source

The script reads conversation data from:
- `~/.openclaw/agents/{agentId}/sessions/sessions.json` (session index)
- `~/.openclaw/agents/{agentId}/sessions/*.jsonl` (per-session logs, including unindexed historical files)
- `~/.openclaw/skills/` (installed skills directory for ecosystem analysis)

Cache is written to `~/.openclaw/agents/{agentId}/sessions/.clawlens-cache/facets/` to avoid re-analyzing the same sessions.

## Privacy Notice

This skill sends conversation transcript data to an **external LLM provider** (specified by `--model`) for analysis. Specifically:

- **Stage 2 (Facet Extraction)**: Each session's conversation transcript (truncated to ~80K chars) is sent to the LLM to extract structured analysis (task categories, friction points, etc.). Results are cached locally so each session is only sent once.
- **Stage 4 (Report Generation)**: Aggregated statistics and session summaries (not raw transcripts) are sent to the LLM to generate the report sections.

**API key handling:** When `--model` is omitted, this skill reads `openclaw.json` and `auth-profiles.json` to auto-detect the model and retrieve the API key. The API key is used only for LLM calls during report generation and is not stored or transmitted elsewhere. When `--model` is specified explicitly, the user must provide the API key via environment variables — no OpenClaw config files are accessed for credentials.
