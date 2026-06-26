---
name: chat-learnings-extractor
description: "Extract structured learnings (lessons, decisions, patterns, dead ends) from AI conversation exports using a local Ollama model or any OpenAI-compatible API. Pairs with chat-history-importer. Trigger phrases: extract learnings from conversations, analyze chat exports, mine conversation insights, extract lessons from chats, chat learnings extractor."
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["python3"],"env":[]},"os":["linux","darwin","win32"]}}
---

# Conversation Learnings Extractor

Extract structured learnings (lessons, decisions, patterns, dead ends) from exported AI conversations using either a local Ollama model or any OpenAI-compatible API. This skill is designed to work with exports from OpenAI and Anthropic, and pairs well with the [chat-history-importer](https://clawhub.ai/djc00p/chat-history-importer) skill for a complete conversation analysis workflow.

## Quick Start

### Using Ollama (default)

```bash
python3 scripts/extract.py --dir /path/to/exports --limit 3 --dry-run
python3 scripts/extract.py --file single-conversation.json
python3 scripts/extract.py --dir /path/to/exports --since 2026-04-01
```

### Using OpenAI-compatible API (e.g., OpenAI, Anthropic Bedrock, etc.)

```bash
export OPENAI_API_KEY=sk-...
export OPENAI_BASE_URL=https://api.openai.com/v1  # optional, defaults to OpenAI
python3 scripts/extract.py --dir /path/to/exports --model gpt-4o-mini
```

## How It Works

1. **Parse** OpenAI/Anthropic JSON exports using bundled parsers (from sibling `chat-history-importer` skill)
2. **Deduplicate** via `.processed_ids` file (skip already-processed chats)
3. **Summarize** conversation to key excerpts (to fit model context)
4. **Extract** structured learnings using your chosen model: lessons, decisions, patterns, dead ends
5. **Append** results to `memory/semantic/learnings-from-exports.md`

## Integration with chat-history-importer

This skill pairs with `chat-history-importer`:

1. **First**, run `chat-history-importer` to ingest raw conversations into episodic memory (`memory/episodic/YYYY-MM-DD.md`)
2. **Then**, run this skill to extract structured learnings into semantic memory (`memory/semantic/learnings-from-exports.md`)

This workflow keeps raw conversation logs separate from actionable insights, enabling better knowledge organization.

## Configuration

### Using Ollama (Local)

**Prerequisites:** Ollama running at `http://127.0.0.1:11434` (default)

```bash
# Use default model (gemma4:26b)
python3 scripts/extract.py --dir /path/to/exports

# Use a different local model
python3 scripts/extract.py --dir /path/to/exports --model llama2

# Custom Ollama endpoint
export OLLAMA_BASE_URL=http://ollama.example.com:11434
python3 scripts/extract.py --dir /path/to/exports
```

**Environment Variables:**
- `OLLAMA_BASE_URL` — Ollama API endpoint (default: `http://127.0.0.1:11434`)

### Using OpenAI-compatible API

Any API supporting the OpenAI `/chat/completions` endpoint (OpenAI, Bedrock, LM Studio, etc.)

```bash
export OPENAI_API_KEY=sk-...
export OPENAI_BASE_URL=https://api.openai.com/v1  # optional
python3 scripts/extract.py --dir /path/to/exports --model gpt-4o-mini
```

**Environment Variables:**
- `OPENAI_API_KEY` — API key (required to enable this mode; if set, OpenAI mode is used instead of Ollama)
- `OPENAI_BASE_URL` — API base URL (default: `https://api.openai.com/v1`)

**Model auto-selection:**
- If `OPENAI_API_KEY` is set → defaults to `gpt-4o-mini`
- If `OPENAI_API_KEY` is not set → defaults to `gemma4:26b` (Ollama)

## Flags

- `--dir DIR` — Process all JSON files in directory
- `--file FILE` — Process single file
- `--limit N` — Process only first N conversations (useful for testing or limiting API costs)
- `--since YYYY-MM-DD` — Skip conversations before this date
- `--model MODEL` — Override default model name
- `--dry-run` — Print output without writing to disk or updating dedup state

## Output Format

Results are appended to `memory/semantic/learnings-from-exports.md` with this structure:

```markdown
## Chat Title (YYYY-MM-DD)

### Lessons Learned

- [bullet points]

### Decisions Made

- [bullet points]

### Patterns Noticed

- [bullet points]

### Dead Ends

- [bullet points]
```

Each category is optional — if a conversation doesn't have notable insights for a category, it will show "None".

## References

- `references/prompt-template.md` — The extraction prompt sent to the model
- `scripts/extract.py` — Main script (reuses parsers from sibling skill)

## Implementation Notes

- Tracks processed chat IDs in `.processed_ids` to avoid re-processing
- Workspace detection: checks `OPENCLAW_WORKSPACE` env var, falls back to `~/.openclaw/workspace`
- Automatically detects OpenAI vs Anthropic export formats
- Truncates long messages for context efficiency
