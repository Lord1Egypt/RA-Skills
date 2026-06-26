# OpenClaw Memory Hub — Architecture

## Design Principles

1. **Local-first**: Primary storage is local SQLite + markdown files; cloud is sync target, not source of truth
2. **Progressive disclosure**: L0 catches everything, L1 structures daily context, L2 curates what matters
3. **Zero-latency retrieval**: bge-m3 embedding runs on local Ollama; no API latency
4. **Multi-language**: bge-m3 supports 100+ languages, 1024-dim vectors
5. **DAG-based composition**: memory-core uses DAG for multi-agent memory lineage

## Four-Tier Architecture

```
┌─────────────────────────────────────────────┐
│                L0 — Runtime                  │
│  ┌─────────────────┐  ┌──────────────────┐  │
│  │  memory-core     │  │  MemOS Cloud     │  │
│  │  (Ollama bge-m3) │  │  (Cloud Recall)  │  │
│  │  SQLite + vec    │  │  Lifecycle hooks │  │
│  └────────┬────────┘  └────────┬─────────┘  │
│           │                     │            │
│  ┌────────▼─────────────────────▼─────────┐  │
│  │  Active Memory (built-in plugin)       │  │
│  │  Pre-reply sub-agent memory search     │  │
│  └────────┬───────────────────────────────┘  │
│           │                                  │
│  ┌────────▼───────────────────────────────┐  │
│  │  Hybrid Search (semantic + BM25)       │  │
│  └────────────────┬───────────────────────┘  │
└───────────────────┼──────────────────────────┘
                    │
┌───────────────────▼──────────────────────────┐
│              L1 — Working Memory              │
│  memory/YYYY-MM-DD.md (30-90 day retention)  │
│  - Daily conversation summaries              │
│  - Technical notes & decisions               │
│  - TODOs & reminders                         │
│  - Hand-editable, human-readable             │
└───────────────────┬──────────────────────────┘
             L2a — Index Layer (MEMORY.md, ~90 lines)
             L2b — Archive Layer (ARCHIVE.md, ~220 lines)
             L2c — Knowledge Graph (facts.sqlite)
                    │  Dreaming pipeline
                    │  (Daily 03:00 UTC)
                    ▼
┌──────────────────────────────────────────────┐
│           L2 — Long-term Memory               │
│  MEMORY.md (read-only base, auto-curated)     │
│  - Key user facts & profile                   │
│  - Permanent decisions & preferences          │
│  - Encrypted sensitive info (SHA-256)         │
│  - Promoted high-scoring insights             │
└──────────────────────────────────────────────┘
```

## Memory Plugins

### memory-core (Primary)

- **Provider**: OpenClaw Plugin Registry
- **Embedding Backend**: Ollama (`http://127.0.0.1:11434`)
- **Model**: `bge-m3` (BAAI, 1024-dimension, multi-language)
- **Vector Storage**: SQLite + sqlite-vec extension
- **Search**: Semantic vector similarity + BM25 keyword hybrid
- **Database**: `~/.openclaw/memory/main.sqlite`
- **Indexing**: Automatic on file save; manual via `openclaw memory index --force`

### MemOS Cloud Plugin (Supplementary)

- **Lifecycle Hook**: Captures and recalls memory via `POST /api/memo` hooks
- **Recall**: Injects relevant memory context into session at bootstrap
- **Cross-device**: Syncs memory across multiple OpenClaw instances

## Dual-Plugin Collaborative Workflow

This is the core innovation of the architecture — **two plugins working in layers, not competing**:

```
User sends message → Gateway receives
         │
         ▼
┌─────────────────────────────────────────────┐
│ 1. MemOS Cloud Plugin                       │
│    (before_agent_start lifecycle hook)       │
│                                              │
│    → Injects:                                │
│      • Long-term facts ("User rides a 703F") │
│      • User preferences ("Hates sweets")     │
│      • Profile constants ("Name is Victor")  │
│                                              │
│    Layer: Static / low-frequency truths      │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│ 2. memory-core                               │
│    (Runtime semantic retrieval)               │
│                                              │
│    → Injects:                                │
│      • Recent conversation snippets          │
│      • Topically relevant past discussions   │
│      • Working memory (today's context)      │
│                                              │
│    Layer: Dynamic / high-frequency context   │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│ Agent receives complete memory context:      │
│                                              │
│  "Victor rides a 703F" (fact — MemOS)        │
│  + "Yesterday discussed Zettelkasten"        │
│    (recent — memory-core)                    │
│  + "Today's weather forecast" (today — L1)  │
└─────────────────────────────────────────────┘
```

### Division of Responsibility

| Aspect | MemOS Cloud | memory-core |
|--------|-------------|-------------|
| **Data type** | Facts, preferences, profile | Conversations, working context |
| **Frequency** | Static / rarely changes | Dynamic / every session |
| **Source** | Cloud API (`POST /api/memo`) | Local SQLite-vec index |
| **Trigger** | `before_agent_start` hook | Runtime semantic query |
| **Retention** | Permanent (cloud) | Configurable (last N chunks) |
| **Scope** | Cross-device, long-term | Single device, recent history |
| **Conflict** | None — complementary | None — complementary |

### Critical Configurations

These settings in `openclaw.json` are **required** for the two plugins to work together without blocking each other:

#### MemOS Cloud Plugin (`plugins.entries.memos-cloud-openclaw-plugin`)

```json
{
  "enabled": true,
  "config": {
    "resetOnNew": true,
    "recallEnabled": true,
    "recallFilterFailOpen": true,
    "asyncMode": true,
    "addEnabled": true
  },
  "hooks": {
    "allowConversationAccess": true
  }
}
```

| Setting | Why it matters |
|---------|----------------|
| `recallFilterFailOpen: true` | **Critical.** If MemOS recall fails (API timeout/network), don't block the pipeline — let memory-core still inject context |
| `asyncMode: true` | **Critical.** MemOS runs asynchronously so memory-core can execute its own retrieval afterward |
| `resetOnNew: true` | Fresh context per session — no stale data carried over |
| `hooks.allowConversationAccess: true` | Allows hooks to read/write conversation data for memory injection |
| `recallEnabled: true` | Enable recall at session start |
| `addEnabled: true` | Auto-capture new memories during conversation |

#### Recommended Full Config (with all tunable params)

```json
{
  "enabled": true,
  "config": {
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
```

#### memory-core Plugin (`plugins.entries.memory-core`)

```json
{
  "enabled": true,
  "config": {
    "dreaming": {
      "enabled": true
    }
  }
}
```

`dreaming.enabled: true` activates the daily Dreaming pipeline.

### Why This Works

- **No overlap**: MemOS handles static facts; memory-core handles dynamic conversation context
- **Fail-safe**: If MemOS Cloud is unreachable, `recallFilterFailOpen: true` keeps the pipeline running
- **Async execution**: MemOS hooks fire async; memory-core retrieval runs independently
- **Layered context**: Agent receives who-you-are facts first, then what-we-talked-about context

## File Anatomy

### Runtime Context Files

| File | Purpose |
|------|---------|
| `AGENTS.md` | Memory rules, safe operation protocol, execution guidelines |
| `SOUL.md` | Agent persona, core principles, independent values |
| `USER.md` | User profile, preferences, communication style |
| `TOOLS.md` | Environment-specific configuration, known issues |
| `MEMORY.md` | Long-term facts (L2), read-only base loaded at bootstrap |

### Daily Memory Files

```
memory/
├── YYYY-MM-DD.md          # Day's conversation log, key decisions
├── MEMORY_INDEX.md         # Auto-generated vector BM25 summary
├── memos-cloud-*.md        # Cloud-pulled memory (read-only cache)
├── .sync-cloud-state.json  # Cloud pull cursor (last fetch timestamp)
├── .sync-push-state.json   # Cloud push state (SHA256 per file)
└── DREAMS.md              # Latest Dreaming analysis output
├── projects/
│   ├── README.md          # Project memory index
│   ├── clawguard.md       # Per-project memory (clawguard)
│   ├── anamnesis-hub.md
│   └── openclaw-dir-inventory.md
```

### Project Memory (P2)

Each GitHub project gets an independent `memory/projects/{slug}.md` file:
- Isolates project-specific decisions, lessons, and conventions
- Prevents project context from polluting MEMORY.md
- Agent-independent: can be loaded by specific sub-agents
- Template: project slug, GitHub URL, status, key decisions, TODOs

### Alias Resolution (P2)

facts.db `aliases` table maps colloquial names to canonical entities:
- "软路由" → "iStoreOS"
- "小爱" → "卧室小爱音箱"
- "anamnesis-hub" → "anamnesis-hub"

Enables natural language queries like "软路由的IP是多少" to resolve to `SELECT * FROM facts WHERE entity='iStoreOS' AND key='ip'`.

## Automated Pipelines

### Dreaming Pipeline

Runs daily at **03:00 UTC** (11:00 CST):

1. **REM Backfill**: Scans recent session logs, extracts structured facts
2. **DeepSeek Analysis**: Runs AI analysis on extracted facts:
   - Preference changes
   - Lessons learned
   - Relationship updates
   - Project criteria
3. **Dreaming Promotion**: Evaluates candidates against threshold (minScore: 0.8, max 10 items) and promotes to MEMORY.md

Output delivered via QQ:
- 📄 REM Backfill: status report
- 🔬 DeepSeek 分析: extracted insights count
- 🌙 Dreaming Promotion: promoted count

### auto-memory v3 (Two-Stage Pipeline)

Runs at **18:30 / 22:30 CST** (30 min after three-way sync):

Reads the latest MemOS Cloud synced facts, filters noise, and writes in two stages:
1. **Stage 1 — ARCHIVE.md archive**: Full entries with SHA-256 dedup, organized under `## Auto-Extracted 历史归档`
2. **Stage 2 — MEMORY.md summary**: One-line index like `Auto-Extracted ({date}): {n} 条新记忆 → ARCHIVE.md:{line}`

**Key difference from v2**: No longer appends raw entries to MEMORY.md. Detailed content goes to ARCHIVE.md, only a summary line stays in MEMORY.md.

```
agent_end → MemOS Cloud (real-time capture + cloud LLM extraction)
              ↓
        sync-cloud-pull.py (every 30 min)
              ↓
        memos-cloud-YYYY-MM-DD.md (structured facts)
              ↓
        auto_memory_extract.py → qwen3 filter + memos-extractor-0.6b
              ↓
        ┌─ Stage 1: ARCHIVE.md (完整归档, SHA-256 去重)
        └─ Stage 2: MEMORY.md (一行摘要, 不写入详细内容)
```

**Key difference from v2**: No longer appends raw entries to MEMORY.md. Two-stage pipeline ensures ARCHIVE.md gets full content with SHA-256 dedup, and MEMORY.md stays clean as a pure index layer (~90 lines).

### Three-Way Sync

Runs at **18:00 / 20:00 / 22:00 CST** (covering user active hours 19–23):

```
┌──────────┐    ┌──────────┐    ┌──────────┐
│  Cloud   │◄──►│Markdown  │◄──►│  Vector  │
│ (Memos)  │    │ (Files)  │    │ (SQLite) │
└──────────┘    └──────────┘    └──────────┘
     │               │               │
     │  sync-pull    │  sync-push    │  sync-index
     ▼               ▼               ▼
  memos-cloud*.md → Cloud API     MEMORY_INDEX.md
```

**Sync Rules**:
- Cloud → MD: New/changed entries since last pull (cursor-based)
- MD → Cloud: SHA256 hash comparison, push only changed files
- Vector → MD: FTS5 BM25 clustering, score > 0.65, grouped by source_file
- Excluded from push: `memos-cloud-*.md`, `MEMORY_INDEX.md`, `DREAMS.md`, `.sync-*.json`

### Wiki Compilation (Planned)

Runs daily at **04:00 UTC** after Dreaming completes:
- Scan memory-core DB + latest Dreaming output
- Extract new entities, concepts, syntheses
- Deduplicate via fuzzy filename matching
- Write new wiki vault pages
- Report new page count only

### session-extract

Runs at **22:00 CST** as part of unified pipeline:
- Scans `~/.openclaw/agents/main/sessions/` JSONL files
- Two-pass extraction via MemOS extractor + reranker
- **Pass 1**: `.jsonl` → `.analyzed1` → `.learnings/ERRORS.md` + `.learnings/LEARNINGS.md`
- **Pass 2**: `.analyzed1` → `.analyzed2` → archive to trash
- Output: `.learnings/` (permanent) + `memory/YYYY-MM-DD.md`
- State tracking: `memory/.session-extract-state.json`
- Auto-skips running session to prevent corruption

### facts.db Activation & Decay

**facts.db** provides structured entity/key/value lookup with Hebbian activation:

| Component | Mechanism |
|-----------|----------|
| **Activation** | Each fact query triggers `activation += 0.5, access_count += 1` |
| **Daily Decay** | Non-permanent facts: `activation *= 0.95` (floor: 0.005) |
| **Classification** | HOT (>2.0) / WARM (0.02~2.0) / COOL (<0.02) |
| **GC Candidates** | COOL facts flagged for review, not auto-deleted |

### LCM Pre-Write Protection

Configured in `openclaw.json` under `agents.defaults.memoryFlush`:
- `enabled: true` — activate pre-compaction flush
- `triggerPercent: 80` — flush when context window reaches 80%
- `flushTo: memory/YYYY-MM-DD.md` — write critical decisions to daily log
- `flushMode: critical_decisions_only` — preserve confirmed decisions, skip noise

This prevents the "Summer Yue scenario" where compaction causes loss of chat-only instructions.

## Sensitive Information

SHA-256 hashing with salt `VictorQR_7x9K2mP` for:

- Passwords & verification hashes
- Phone numbers, ID numbers
- Email addresses (all accounts)
- Social media IDs (WeChat, QQ, Douyin)

Stored in `MEMORY.md` hash table, verified by SHA-256 comparison before access.

## Known Conflicts & Compatibility

### ❌ subconscious-personality-guardian ↔ memory-core

**Status: Incompatible**

Both plugins attempt to use the same OpenClaw memory slot. Installing both causes:
- Memory write conflicts (race conditions on save)
- Retrieval logic duplication (both inject into context)
- Context management conflicts (duplicate or conflicting memory context in prompts)

**Fix**: Disable or remove `subconscious-personality-guardian`:
```json
// openclaw.json
{
  "plugins": {
    "disabled": ["subconscious-personality-guardian"],
    "deny": ["subconscious-personality-guardian"]
  }
}
```

### ✅ memory-core + MemOS Cloud Plugin

**Status: Compatible — designed to work in layers**

They are **not competing** memory systems. They operate at different layers with different responsibilities:

| | memory-core | MemOS Cloud |
|--|-------------|-------------|
| Role | Recent/working context | Long-term facts & preferences |
| Data | Conversations, discussions | User profile, habits, decisions |
| Timing | Every session (runtime query) | Session start (lifecycle hook) |
| Storage | Local SQLite-vec | Remote cloud API |

**Execution order**:
1. MemOS Cloud fires `before_agent_start` → injects static facts
2. memory-core queries local vector DB → injects dynamic context
3. Agent receives layered memory: "who the user is" + "what we talked about recently"

**No overlap**: One handles local retrieval, the other handles cloud sync. Both should be enabled simultaneously for best results.

### ⚠️ MemOS Cloud Plugin + ReMe

**Status: Potentially conflicting**

Both provide cloud memory functionality. Installing both may cause:
- File layer overlap (both write to `memory/`)
- Retrieval logic duplication
- API endpoint conflicts (competing memory services)

**Recommendation**: Choose one. MemOS Cloud is recommended if using OpenClaw natively.

## Performance Characteristics

- **Embedding speed**: ~50ms per query on RTX 4070 Super (12GB VRAM)
- **Database size**: ~100MB for 10K+ memory chunks
- **Hybrid search latency**: <100ms for top-10 results
- **Dreaming pipeline**: ~30 seconds per full run
- **Sync run**: ~10 seconds per direction
