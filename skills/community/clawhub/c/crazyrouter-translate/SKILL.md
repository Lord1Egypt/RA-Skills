---
name: crazyrouter-translate
description: AI-powered translation via Crazyrouter. Translate text between any languages using GPT-5, Claude, DeepSeek, or Qwen. Supports file translation and multi-model comparison. Use when user asks to translate text, documents, or compare translations. Requires environment variable CRAZYROUTER_API_KEY (get at https://crazyrouter.com).
---

# AI Translation via Crazyrouter

Translate text between any languages using the best AI models through [Crazyrouter](https://crazyrouter.com).

## Script Directory

**Agent Execution**:
1. `SKILL_DIR` = this SKILL.md file's directory
2. Script path = `${SKILL_DIR}/scripts/main.mjs`

## Step 0: Check API Key ⛔ BLOCKING

```bash
[ -n "${CRAZYROUTER_API_KEY}" ] && echo "key_present" || echo "not_set"
```

| Result | Action |
|--------|--------|
| `key_present` | Continue |
| `not_set` | Ask user to set `CRAZYROUTER_API_KEY`. Get key at https://crazyrouter.com |

## Usage

```bash
# Basic translation
node ${SKILL_DIR}/scripts/main.mjs --text "Hello world" --to zh

# Translate file
node ${SKILL_DIR}/scripts/main.mjs --input article.md --to ja --output article_ja.md

# Use specific model
node ${SKILL_DIR}/scripts/main.mjs --text "Bonjour le monde" --to en --model deepseek-r1

# Specify source language
node ${SKILL_DIR}/scripts/main.mjs --text "你好世界" --from zh --to ko

# Keep formatting (Markdown)
node ${SKILL_DIR}/scripts/main.mjs --input README.md --to ja --output README_ja.md --format markdown
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--text <text>` | Text to translate | — |
| `--input <file>` | Read from file | — |
| `--output <file>` | Save to file | stdout |
| `--from <lang>` | Source language | auto-detect |
| `--to <lang>` | Target language (required) | — |
| `--model <id>` | AI model | `gpt-4o-mini` |
| `--format <fmt>` | `plain` or `markdown` | `plain` |

### Language Codes

en, zh, ja, ko, es, fr, de, pt, ru, ar, vi, th, id, tr, it, pl, nl, sv, hi, ...
