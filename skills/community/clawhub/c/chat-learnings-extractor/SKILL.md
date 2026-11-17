---


name: chat-learnings-extractor
description: "Extract structured learnings (lessons, decisions, patterns, dead ends) from AI conversation exports using a local Ollama model or any OpenAI-compatible API. Pairs with chat-history-importer. Trigger phrases: extract learnings from conversations, analyze chat exports, mine conversation insights, extract lessons from chats, chat learnings extractor."
metadata: {"clawdbot":{"emoji":"\ud83e\udde0","requires":{"bins":["python3"],"env":[]},"os":["linux","darwin","win32"],"envVars":[{"name":"OPENAI_API_KEY","required":false,"description":"OpenAI-compatible API key. Enables remote model mode. Leave unset to use local Ollama."},{"name":"OPENAI_BASE_URL","required":false,"description":"OpenAI-compatible endpoint base URL. Only set this to a trusted HTTPS provider you control."},{"name":"OLLAMA_BASE_URL","required":false,"description":"Ollama endpoint. Defaults to http://127.0.0.1:11434 (loopback)."},{"name":"OPENCLAW_WORKSPACE","required":false,"description":"Agent workspace path. Defaults to ~/.openclaw/workspace."}],"version":"1.0.4"}}
---



# Conversation Learnings Extractor

Extract structured learnings (lessons, decisions, patterns, dead ends) from exported AI conversations using either a local Ollama model or any OpenAI-compatible API. This skill is designed to work with exports from OpenAI and Anthropic, and pairs well with the [chat-history-importer](https://clawhub.ai/djc00p/chat-history-importer) skill for a complete conversation analysis workflow.

## Data Handling and Safety

This skill reads private conversation exports and writes model-generated output into
your agent's persistent memory. Treat both directions as sensitive.

- **Dry run first.** Always start with `--dry-run` and read the output before letting
  it write anything to memory.
- **Prefer local processing.** The default Ollama path runs against
  `http://127.0.0.1:11434` on loopback, so export contents never leave your machine.
- **Remote endpoints send your exports.** When `OPENAI_API_KEY` is set, conversation
  content and the API key are sent to the configured endpoint. Only set
  `OPENAI_BASE_URL` to a trusted HTTPS provider you control.
- **Review before you trust.** Model output is unreviewed text written into persistent
  agent memory. Read the generated learnings before relying on them.
- **Scope the input.** Narrow `--dir` and `--since` so you import only what you intend.

See `references/model-modes-and-categories.md` for the OpenAI-compatible API setup and the full extraction category list.

Configuration, model modes, and the full output format are documented in `references/model-modes-and-categories.md`.

## Quick Start

### Using Ollama (default)

```bash
python3 scripts/extract.py --dir /path/to/exports --limit 3 --dry-run
python3 scripts/extract.py --file single-conversation.json
python3 scripts/extract.py --dir /path/to/exports --since 2026-04-01
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


## Flags

- `--dir DIR` — Process all JSON files in directory
- `--file FILE` — Process single file
- `--limit N` — Process only first N conversations (useful for testing or limiting API costs)
- `--since YYYY-MM-DD` — Skip conversations before this date
- `--model MODEL` — Override default model name
- `--dry-run` — Print output without writing to disk or updating dedup state



## References

- `references/model-modes-and-categories.md` — Configuration, model modes, output format
- `references/prompt-template.md` — The extraction prompt sent to the model
- `scripts/extract.py` — Main script (reuses parsers from sibling skill)

## Implementation Notes

- Tracks processed chat IDs in `.processed_ids` to avoid re-processing
- Workspace detection: checks `OPENCLAW_WORKSPACE` env var, falls back to `~/.openclaw/workspace`
- Automatically detects OpenAI vs Anthropic export formats
- Truncates long messages for context efficiency
