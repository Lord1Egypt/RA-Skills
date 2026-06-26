---
name: memory-flush
description: "Save session context to memory before compaction, with local LLM-based fact extraction via Ollama. No external API required."
metadata: { "openclaw": { "emoji": "🧠", "events": ["session:compact:before", "command:new"], "requires": { "config": ["workspace.dir"] } } }
---

# Memory Flush Hook

Saves session context to memory files at two key moments:

1. **Before compaction** (`session:compact:before`): Reads session transcript, extracts structured facts via local LLM, and saves a conversation snapshot.

2. **On session reset** (`command:new`): Reads session transcript, extracts facts via local LLM, and logs the reset event.

## 🔒 Data Handling (Local-First)

- **Reads** session transcript files from disk (`*.jsonl`)
- **Processes** messages locally via Ollama (`http://localhost:11434`) — no data leaves your machine
- **Saves** extracted facts and snapshots locally to `workspace/memory/`

Optional: Set `baseUrl` and `apiKey` in config to use an external OpenAI-compatible API instead.

## Output

Files written to `<workspace>/memory/`:
- `YYYY-MM-DD-facts-*.md` — extracted structured facts (`[PREF]`, `[DECIDE]`, `[RULE]`, `[INFO]`)
- `YYYY-MM-DD-compact-*.md` — pre-compaction conversation snapshots
- `YYYY-MM-DD-session-log.md` — session reset logs

## Configuration

```json5
{
  hooks: {
    internal: {
      enabled: true,
      entries: {
        "memory-flush": {
          enabled: true,
          extractionModel: "qwen2.5:7b",           // optional, default shown
          baseUrl: "http://localhost:11434/v1/chat/completions"  // optional, default shown
        }
      }
    }
  }
}
```
