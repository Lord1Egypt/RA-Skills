# OpenClaw Memory Hub — Manual Setup Guide

> **Tip**: Use `bash scripts/auto-setup.sh` for one-command interactive setup. This is the manual alternative.

## Prerequisites

- OpenClaw >= v25.9.0
- Node.js >= 18
- Internet connection (for downloading Ollama and bge-m3 model)

## Step 1: Install Ollama

### Option A: Standard
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Option B: Intel Edition (OpenVINO backend)
```bash
curl -L -o /usr/local/bin/ollama https://github.com/intel/ollama/releases/latest/download/ollama-linux-amd64
chmod +x /usr/local/bin/ollama
```

Start Ollama:
```bash
ollama serve
```

Verify:
```bash
curl http://127.0.0.1:11434/api/tags
```

### Step 1.5: Pull bge-m3 Embedding Model

```bash
ollama pull bge-m3
```

## Step 2: Plugin Conflict Check

Before installing memory-core, check if `subconscious-personality-guardian` is present:

```bash
grep -q "subconscious-personality-guardian" ~/.openclaw/openclaw.json
```

If found, add to `plugins.disabled` and `plugins.deny` in `openclaw.json`:
```json
{
  "plugins": {
    "disabled": ["subconscious-personality-guardian"],
    "deny": ["subconscious-personality-guardian"]
  }
}
```

## Step 3: Install memory-core Plugin

### Manual Config

Add to `openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "memory-core": {
        "config": {
          "embeddingUrl": "http://127.0.0.1:11434/api/embed",
          "embeddingModel": "bge-m3",
          "dimension": 1024
        }
      }
    }
  }
}
```

Restart Gateway:

```bash
openclaw gateway restart
```

Verify status:

```bash
openclaw memory status
```

## Step 3: Install MemOS Cloud Plugin (Optional)

Required for cross-device memory sync.

### Recommended Full Config (in `openclaw.json`):

```json
{
  "plugins": {
    "entries": {
      "memos-cloud-openclaw-plugin": {
        "enabled": true,
        "config": {
          "url": "https://your-memos-server.com",
          "token": "your-memos-api-token",
          "resetOnNew": true,
          "recallEnabled": true,
          "recallFilterFailOpen": true,
          "asyncMode": true,
          "addEnabled": true,
          "queryPrefix": "important user context preferences decisions ",
          "memoryLimitNumber": 9,
          "preferenceLimitNumber": 6,
          "relativity": 0.45,
          "maxItemChars": 8000,
          "includeAssistant": true,
          "includePreference": true,
          "tags": ["openclaw", "memory"]
        },
        "hooks": {
          "allowConversationAccess": true
        }
      }
    }
  }
}
```

**Key parameters explained:**

| Parameter | Value | Why |
|-----------|-------|-----|
| `recallFilterFailOpen` | `true` | Don't block pipeline if MemOS API is unreachable — let memory-core still serve context |
| `asyncMode` | `true` | Run asynchronously so memory-core can execute its own retrieval |
| `resetOnNew` | `true` | Fresh context per session, no stale data carried over |
| `queryPrefix` | `"important user context preferences decisions "` | Semantic anchor to prioritize recall relevance |
| `memoryLimitNumber` | `9` | Max recalled memory items per session |
| `preferenceLimitNumber` | `6` | Max recalled preference items per session |
| `relativity` | `0.45` | Relevance threshold — filter out low-confidence matches |
| `maxItemChars` | `8000` | Max characters per memory item |
| `includeAssistant` | `true` | Include AI's own past outputs as memory context |
| `includePreference` | `true` | Include detected user preferences in recall |
| `tags` | `["openclaw", "memory"]` | Tagging for multi-instance filtering |

## Step 4: Configure Runtime Files

### AGENTS.md — Memory Rules

Add to your `AGENTS.md`:

```markdown
## 🧠 Memory System

- **L0 Runtime Retrieval**: memory-core plugin (Ollama bge-m3 → SQLite-vec), semantic + BM25 hybrid
- **L1 Working Memory**: `memory/YYYY-MM-DD.md` files, 30-90 day retention
- **L2 Long-term Memory**: `MEMORY.md` read-only base
- **Dreaming**: Daily 03:00 UTC — auto-analyze and promote to L2
- **Writing Rules**: Important decisions → L1 log; "记住" → L1 + verify via memory_search
- **Lessons**: Update AGENTS.md / TOOLS.md
- **Errors**: `.learnings/ERRORS.md`

**MEMORY.md is read-only** — agent loads at bootstrap. New memories go to L1 files.
```

### SOUL.md — Core Identity

```markdown
## Continuity

Each session is a fresh start. These files _are_ your memory. Read them. Update them.

## Memory

- Use memory files for persistence, not session recall
- The Dreaming pipeline runs daily — no need to report it
- Trust the system: auto-indexing + daily promotion covers continuity
```

### TOOLS.md — Environment Config

```markdown
## 🧠 Memory System (memory-core)

- **Embedding backend**: Ollama (`http://127.0.0.1:11434`)
- **Embedding model**: `bge-m3` (1024-dim, multi-language)
- **Database**: `~/.openclaw/memory/main.sqlite`
- **Index**: `openclaw memory index --force`
- **Status**: `openclaw memory status`
- **Dreaming**: Daily 03:00 UTC
```

## Step 5: Set Up Cron Jobs

### Dreaming Pipeline (Daily 03:00 UTC)

```bash
# Using openclaw cron
openclaw cron add --name "memory-dreaming-pipeline" \
  --cron "0 3 * * *" \
  --agent "default" \
  --announce \
  --message "Run Dreaming pipeline: scan logs, extract insights, promote to MEMORY.md"
```

### Active Memory (Built-in Plugin)

Enable in `openclaw.json` to activate pre-reply sub-agent memory search:

```json5
{
  plugins: {
    entries: {
      "active-memory": {
        enabled: true,
        config: {
          enabled: true,
          agents: ["main"],
          allowedChatTypes: ["direct"],
          promptStyle: "balanced",
          timeoutMs: 15000,
          modelFallback: "ollama/qwen3:8b",
        },
      },
    },
  },
}
```

### auto-memory v2 (18:30, 22:30 CST)

Place `scripts/auto_memory_extract.py` in `user_workspace/scripts/` and install the `auto-memory` skill:

```bash
openclaw cron add --name "auto-memory-extract" \
  --cron "30 18,22 * * *" \
  --tz "Asia/Shanghai" \
  --task "python3 user_workspace/scripts/auto_memory_extract.py --mode full"
```

Requires MemOS Cloud plugin + sync to provide input data (`memos-cloud-*.md` files).

### Three-Way Sync (18:00, 20:00, 22:00 CST)

Place sync scripts in `user_workspace/scripts/`:

1. `sync-cloud-pull.py` — Pulls new entries from MemOS Cloud API
2. `sync-cloud-push.py` — Pushes local markdown changes to Cloud
3. `sync-vector-index.py` — Generates MEMORY_INDEX.md from vector DB
4. `sync-all.sh` — Orchestrator

Cron schedule (UTC):

```bash
# 10:00 / 12:00 / 14:00 UTC = 18:00 / 20:00 / 22:00 CST
0 10,12,14 * * * ~/.openclaw/workspace/user_workspace/scripts/sync-all.sh
```

## Step 6: Verify Setup

```bash
# Check memory status
openclaw memory status

# Force index
openclaw memory index --force

# List cron jobs
openclaw cron list

# Check logs
openclaw logs --follow --plain
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Embedding fails | Ollama not running | `ollama serve` |
| bge-m3 not found | Model not pulled | `ollama pull bge-m3` |
| Plugin not loaded | Restart needed | `openclaw gateway restart` |
| Slow search | Index stale | `openclaw memory index --force` |
| Cloud sync fails | Token expired | Refresh MemOS API token |
| Dreaming not running | Cron disabled | `openclaw cron list` → verify |
