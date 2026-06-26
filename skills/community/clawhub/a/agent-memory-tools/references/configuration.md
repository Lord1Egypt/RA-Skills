# Configuration Guide

## Quick Setup

1. Copy `scripts/config.json` and edit for your setup
2. Set your workspace path (or leave empty for auto-detect)
3. Choose a preset or configure custom LLM/embeddings

### Environment Variable
```bash
export MEMORY_WORKSPACE="/path/to/your/workspace"
```
If not set, auto-detects the skill's parent directory.

## Platform Support

| Platform | Scan/File/Post-compaction | Watch (daemon) | LaunchAgent |
|----------|--------------------------|-----------------|-------------|
| macOS | ✅ | ✅ fswatch or polling | ✅ native |
| Linux | ✅ | ✅ polling (30s) | systemd/cron |
| Windows | ✅ | ✅ polling (30s) | Task Scheduler |

### macOS (LaunchAgent)
```xml
<!-- ~/Library/LaunchAgents/com.memory-auto-ingest.plist -->
<plist version="1.0">
<dict>
    <key>Label</key><string>com.memory-auto-ingest</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/path/to/memory-auto-ingest.sh</string>
    </array>
    <key>WatchPaths</key>
    <array>
        <string>/path/to/workspace/memory</string>
    </array>
    <key>ThrottleInterval</key><integer>300</integer>
</dict>
</plist>
```

### Linux (systemd timer)
```ini
# ~/.config/systemd/user/memory-ingest.timer
[Timer]
OnCalendar=*:0/5
Persistent=true
[Install]
WantedBy=timers.target
```

### Windows (Task Scheduler)
```powershell
schtasks /create /tn "MemoryAutoIngest" /tr "python scripts/auto_ingest.py --scan" /sc minute /mo 5
```

## Choosing Your LLM

### By RAM Available

| RAM | LLM | Embed | Cost | Quality |
|-----|-----|-------|------|---------|
| **4 GB** | gemma3:1b | nomic-embed-text | $0 | ⭐⭐ Basic |
| **8 GB** | **gemma3:4b** ← recommended | nomic-embed-text-v2-moe | $0 | ⭐⭐⭐⭐ Good |
| **16 GB** | qwen3.5:27b, mistral-small3.2 | nomic-embed-text-v2-moe | $0 | ⭐⭐⭐⭐ Great |
| **32+ GB** | qwen3.5:35b (MLX), llama-3.3:70b | nomic-embed-text-v2-moe | $0 | ⭐⭐⭐⭐⭐ Best |

### By Budget (API)

| Option | LLM | Embed | Cost/month* | Quality |
|--------|-----|-------|-------------|---------|
| **Free** | gemma-3-4b-it:free (OpenRouter) | — need local embed | $0 | ⭐⭐⭐ |
| **Cheap** | gpt-4o-mini | text-embedding-3-small | ~$1-5 | ⭐⭐⭐⭐ |
| **Best** | claude-sonnet-4-5 / gpt-4o | text-embedding-3-large | ~$10-50 | ⭐⭐⭐⭐⭐ |

*Estimated for ~100 queries/day

### Key Warnings

⚠ **Qwen 3.5 (all sizes)** — Puts JSON output in "thinking" field instead of response. Works for reasoning/multihop but **fails for JSON extraction**. Use gemma3 for JSON tasks via `scriptOverrides`.

⚠ **Models < 1B params** — Unreliable JSON output, frequent hallucinations. Not recommended.

✅ **gemma3:4b** — Best ratio quality/speed for structured output. ~2s per call on modern hardware.

## Presets

Use `--preset` on any script:

```bash
python3 scripts/unified_recall.py "query" --preset ollama
python3 scripts/extract_facts.py "text" --preset openai --store
```

| Preset | LLM | Embed | Needs |
|--------|-----|-------|-------|
| `ollama` | gemma3:4b | nomic-v2-moe | Ollama running |
| `ollama-big` | qwen3.5:27b | nomic-v2-moe | Ollama + 16GB RAM |
| `lmstudio` | auto (loaded model) | nomic | LM Studio running |
| `openai` | gpt-4o-mini | text-embedding-3-small | OPENAI_API_KEY |
| `openrouter` | gemma-3-4b:free | text-embedding-3-small | OPENROUTER_API_KEY + OPENAI_API_KEY |

## Per-Script Overrides

Use different models for different tasks:

```json
"scriptOverrides": {
  "extract": { "llm": { "model": "gemma3:4b", "apiFormat": "ollama" } },
  "recall":  { "llm": { "model": "gemma3:4b", "apiFormat": "ollama" } },
  "multihop": { "llm": { "model": "qwen3.5:27b" } },
  "graph": { "llm": { "model": "qwen3.5:27b" } }
}
```

**Strategy:** Fast model (gemma3) for JSON tasks, big model for reasoning.

## Install Models (Ollama)

```bash
# Minimum (8GB RAM)
ollama pull gemma3:4b
ollama pull nomic-embed-text-v2-moe

# Extended (16GB+ RAM)
ollama pull qwen3.5:27b
ollama pull mistral-small3.2
```
