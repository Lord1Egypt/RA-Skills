# AVM - AI Virtual Memory

> **AVM** — 面向多 Agent 的本地零成本共享记忆系统。语义搜索，FUSE 挂载，私有+共享隔离。

## Core Value

- **面向多 Agent 的本地共享记忆** — 多个 Agent 共享同一记忆层，私有空间互不干扰
- **零成本** — 本地 sentence-transformers (all-MiniLM-L6-v2)，无需任何 API key，无网络依赖
- **语义搜索** — 不是关键词匹配，是向量相似度。"伊朗军事冲突" 能找到 "中东局势紧张"
- **FUSE 挂载** — `cat`/`echo`/`ls` 直接操作记忆，shell 脚本和任何工具都能用
- **多 Agent 隔离** — 私有空间 (`/memory/private/{agent}/`) + 共享空间 (`/memory/shared/`)，协作不混淆

## Why You Need AVM

**The Problem:** LLMs forget everything between sessions. Context windows are limited. RAG retrieves chunks, not structured knowledge.

**AVM solves this:**

| Challenge | Without AVM | With AVM |
|-----------|-------------|----------|
| **Multi-agent sync** | Copy-paste, version chaos | Shared namespaces, `:delta` for changes |
| **Memory isolation** | All-or-nothing access | Private + shared, per-agent permissions |
| **Context limits** | Fixed window, truncate | Token-aware recall, fit any budget |
| **Knowledge structure** | Flat vector chunks | Linked graph, typed relationships |
| **Discovery** | Need exact keywords | Semantic search + browse/explore/timeline |

**Real examples:**

```python
# Trading agent remembers across sessions
trader.remember("NVDA RSI at 72, overbought", importance=0.9, tags=["market"])
# 3 months later...
trader.recall("what did I observe about NVDA?", max_tokens=500)

# Agent forgets what it knows
trader.topics()      # "technical: 12, crypto: 8, macro: 5"
trader.timeline(7)   # "Mon: BTC signal, Tue: Fed notes..."

# Multi-agent collaboration
analyst.remember("SPY pattern", namespace="shared")
trader.recall("market patterns")  # sees analyst's shared memory
```

## When to Use AVM

**Best for:**
- 📦 **Shared knowledge** — Company docs, cron configs, market analysis that multiple agents access
- 🤝 **Multi-agent collaboration** — Agent A writes analysis, Agent B recalls it
- 🔄 **Incremental sync** — Read only changes since last read with `:delta`
- 🗂️ **External references** — Paths, schedules, entity descriptions (not file content itself)

**Not needed for:**
- 🔒 **Private agent memory** — Most agent frameworks have built-in memory tools
- 📄 **Code indexing** — IDEs and LSP do this better
- 📝 **Ephemeral notes** — Use TTL or just don't store

**Rule of thumb:** If only one agent needs it, use the agent's native memory. If multiple agents need it, put it in AVM `/memory/shared/`.

## AVM vs MemGPT

| | **MemGPT/Letta** | **AVM** |
|---|---|---|
| **Philosophy** | LLM manages its own memory | Explicit API, you control |
| **Memory decisions** | LLM decides when to store/retrieve | Agent calls `remember()`/`recall()` |
| **Architecture** | Agent framework | Pure storage layer |
| **LLM dependency** | Needs LLM for every memory op | No LLM needed |
| **Multi-agent** | Single agent focus | Built-in isolation + sharing |
| **Interface** | Python SDK | FUSE mount, MCP, CLI, Python |
| **Integration** | Self-contained | Works with shell, editors, any tool |

**Analogy:**
- MemGPT = **Autopilot** (LLM drives)
- AVM = **Manual transmission** (you drive)

**When to use which:**
- **MemGPT**: Want autonomous memory, single agent, hands-off
- **AVM**: Want explicit control, multi-agent, integrate with existing tools

**They can work together:** Use AVM as storage backend, add MemGPT-style logic on top for automatic memory management.

<details>
<summary><b>🎮 See it in action (click to expand)</b></summary>

```
    ╔═══════════════════════════════════════════════════════════╗
    ║     █████╗ ██╗   ██╗███╗   ███╗                          ║
    ║    ██╔══██╗██║   ██║████╗ ████║                          ║
    ║    ███████║██║   ██║██╔████╔██║                          ║
    ║    ██╔══██║╚██╗ ██╔╝██║╚██╔╝██║                          ║
    ║    ██║  ██║ ╚████╔╝ ██║ ╚═╝ ██║                          ║
    ║    AI Virtual Memory - Playground                         ║
    ╚═══════════════════════════════════════════════════════════╝

============================================================
  1. BASIC READ/WRITE
============================================================
✓ Written: /memory/lessons/risk_management.md
✓ Written: /memory/market/NVDA_analysis.md

📌 Read content:
   # Risk Management Rules
   ## Position Sizing
   - Never risk more than 2% of portfolio on a single trade
   - Use stop-loss orders religiously

============================================================
  2. FULL-TEXT SEARCH
============================================================
📌 Search: 'RSI overbought':
   [0.85] /memory/lessons/risk_management.md
   [0.72] /memory/market/NVDA_analysis.md

============================================================
  3. KNOWLEDGE GRAPH (LINKING)
============================================================
✓ Linked: NVDA_analysis → risk_management (related)

📌 Links from risk_management.md:
   → /memory/market/NVDA_analysis.md (related)

============================================================
  4. AGENT MEMORY (TOKEN-AWARE RECALL)
============================================================
✓ Remembered: NVDA warning (importance: 0.9)
✓ Remembered: BTC observation (importance: 0.7)

📌 Recall: 'NVDA risk' (max 500 tokens):
   ## Relevant Memory (2 items, ~120 tokens)
   [/memory/private/trader/nvda_warning.md] (0.92)
   NVDA showing weakness. RSI at 72, reduce exposure.

============================================================
  5. MULTI-AGENT ISOLATION
============================================================
✓ Analyst stored: SPY pattern (private to analyst)

📌 Trader tries to recall analyst's memory:
   Cannot access - private to analyst

📌 Trader stats: Private: 3
📌 Analyst stats: Private: 1

============================================================
  6. INCREMENTAL COLLABORATION
============================================================
# Analyst updates shared report
$ echo "New finding" >> /shared/report.md

# Trader reads only the changes
$ cat /shared/report.md:delta
# v3 (2026-03-07 10:30)
--- +++ @@ -5 +5,2 @@
+New finding

# Next read shows no changes
$ cat /shared/report.md:delta
(no changes)

============================================================
  6. METADATA & TAGS
============================================================
📌 Tag Cloud:
   market: 2, nvda: 1, warning: 1, btc: 1

============================================================
  7. NAVIGATION & DISCOVERY
============================================================
📌 Topics:
   📁 private: 3 memories
   🏷️ market: 2, technical: 1, crypto: 1

📌 Timeline (today):
   [14:30] nvda_alert: NVDA RSI at 72...
   [14:25] btc_note: BTC holding $65K...

📌 Workflow: topics() → browse() → explore() → recall()

============================================================
  DEMO COMPLETE 🎉
============================================================
```

**Run it yourself:**
```bash
pip install -e .
python playground.py
```

</details>

## Performance

Benchmarked on Apple M2 Pro, 16GB RAM, macOS 15.7, Python 3.13, SQLite 3.45 (WAL mode).

| Metric | Value | Notes |
|--------|-------|-------|
| Write throughput | 468 ops/s | WAL + async embedding |
| Read throughput (hot) | 724,000 ops/s | LRU cache hit |
| Read throughput (cold) | 3,300 ops/s | Cache miss → SQLite |
| Search throughput | 2,000 ops/s | FTS5 full-text |
| Cache hit rate | 95% | Zipf access pattern |
| Token savings | 97%+ | vs. loading all memories |

**Key findings:**
- **LRU cache is the dominant optimization** — 420x read improvement
- **Multi-agent contention** — SQLite write lock serializes writes; per-agent throughput drops linearly with agent count
- **Cold start** — First query ~6x slower due to embedding model initialization

See [detailed benchmarks and ablation study](https://bkmashiro.moe/posts/projects/avm-performance-analysis) for full analysis.

### Multi-Agent Discovery

| Method | Hops | Latency | Architecture |
|--------|------|---------|--------------|
| Traditional recall | 4 | ~3.5ms | Per-agent search |
| TopicIndex | 1 | ~0.5ms | Pre-computed index |
| Librarian | 1 | ~1.7ms | Centralized router |
| Gossip | 1 | ~0.5ms | Decentralized bloom filters |

## Features

- **FUSE Mount** - Mount as filesystem, use `ls`, `cat`, `echo`
- **Virtual Nodes** - Access metadata via `:meta`, `:links`, `:tags`
- **MCP Server** - Integrate with AI agents via MCP protocol
- **Agent Memory** - Token-aware recall with scoring strategies
- **Multi-Agent** - Permissions, quotas, audit logging
- **Tell System** - Cross-agent messaging with priority levels (urgent/normal/low)
- **Full-Text Search** - FTS5 (English recommended; Chinese lacks tokenizer support)
- **Semantic Search** - Local embedding (all-MiniLM-L6-v2), zero API cost, auto-index on write
- **TopicIndex** - O(1) recall for known topics, reduces hop count from 4 to 1
- **Librarian** - Global knowledge router for multi-agent discovery (95% hop reduction)
- **Gossip Protocol** - Decentralized agent discovery using bloom filter digests
- **Memory Consolidation** - Sleep-like memory processing: decay, merge, summarize

## Install

```bash
pip install -e .

# For FUSE mount (optional)
pip install fusepy
# macOS: brew install macfuse
# Linux: apt install fuse3
```

## Quick Start

### Python API

```python
from avm import AVM

avm = AVM()

# Read/Write
avm.write("/memory/lesson.md", "# Trading Lesson\n\nRSI > 70 = overbought")
node = avm.read("/memory/lesson.md")

# Search
results = avm.search("RSI")

# Agent Memory
mem = avm.agent_memory("akashi")
mem.remember("NVDA showing weakness", tags=["market", "nvda"])
context = mem.recall("NVDA risk", max_tokens=4000)
```

### CLI

```bash
# Read/Write
avm read /memory/lesson.md
avm write /memory/lesson.md --content "New lesson"

# Full-text search
avm search "RSI"

# Semantic search (embedding)
avm semantic "Iran conflict news"           # semantic similarity
avm semantic "BTC market" --limit 5         # limit results
avm semantic "trading" --agent akashi       # agent context

# Agent Memory (token-aware recall, hybrid FTS+embedding)
avm recall "NVDA risk" --agent akashi --max-tokens 4000
```

### FUSE Mount

Mount AVM as a filesystem for shell access.

**Requirements:**
- macOS: `brew install macfuse` (approve system extension in System Settings → Privacy & Security)
- Linux: `apt install fuse3`

```bash
# Configure mounts in ~/.config/avm/mounts.yaml
# Example:
#   mounts:
#     - mountpoint: ~/.openclaw/workspace/avm
#       agent_id: myagent

# Start daemon (manages all mounts)
avm-daemon start --daemon

# Check status
avm-daemon status

# Reload config
avm-daemon reload

# Stop daemon
avm-daemon stop

# Use standard shell commands
ls /mnt/avm/memory/
cat /mnt/avm/memory/lesson.md
echo "New insight" > /mnt/avm/memory/log.md

# Virtual nodes (append suffix to any file path)
cat /mnt/avm/memory/lesson.md:meta      # Metadata (JSON)
cat /mnt/avm/memory/lesson.md:links     # Related nodes
cat /mnt/avm/memory/lesson.md:tags      # Tags
cat /mnt/avm/memory/lesson.md:ttl       # Time-to-live
cat /mnt/avm/memory/lesson.md:history   # Version history
cat /mnt/avm/memory/:list               # Directory listing
cat '/mnt/avm/memory/:list?limit=10'    # Paginated
cat '/mnt/avm/memory/:list?tag=work'    # Filter by tag
cat '/mnt/avm/memory/:changes?minutes=5' # Recent changes
cat /mnt/avm/memory/:stats              # Statistics
cat "/mnt/avm/:search?q=RSI"            # Search
cat "/mnt/avm/:recall?q=NVDA"           # Token-aware recall

# Shortcuts - quick access via @xxx prefix
cat /mnt/avm/memory/:list               # Shows: @abc  lesson.md  Risk management...
cat /mnt/avm/@abc                       # Access file by shortcut
cat /mnt/avm/@abc:meta                  # Works with suffixes too
```

### MCP Server

```bash
# Start MCP server
avm-mcp --user akashi
```

```yaml
# mcp_servers.yaml
avm-memory:
  command: avm-mcp
  args: ["--user", "akashi"]
```

**MCP Tools:**

| Tool | Description |
|------|-------------|
| `avm_recall` | Token-controlled memory retrieval |
| `avm_browse` | Get paths + summaries (two-pe) |
| `avm_fetch` | Get full content of selected paths |
| `avm_remember` | Store memory with tags/importance |
| `avm_search` | Full-text search |
| `avm_list` | List by prefix |
| `avm_read` | Read specific path |
| `avm_tags` | Tag cloud |
| `avm_recent` | Time-based queries |
| `avm_stats` | Statistics |

## Navigation & Discovery

When an agent forgets context or doesn't know keywords, use navigation methods:

```python
mem = avm.agent_memory("trader")

# 1. Topic overview - see what's in memory
mem.topics()
# ## Memory Topics
# ### By Category:
#   📁 private: 15 memories
# ### By Tag:
#   🏷️ technical: 4 occurrences
#   🏷️ crypto: 3 occurrences

# 2. Browse tree - drill down without keywords
mem.browse("/memory", depth=2)
# 📁 private (15)
#   📁 trader (15)

# 3. Timeline - "what did I observe recently?"
mem.timeline(days=7, limit=10)
# ## Timeline (last 7 days)
# ### 2026-03-05
#   [14:30] nvda_rsi: NVDA RSI at 72...
#   [14:25] btc_support: BTC holding $65K...

# 4. Graph exploration - follow links
mem.explore("/memory/private/trader/nvda.md", depth=2)
# ## Starting from: .../nvda.md
# ### Hop 1:
#   [related] .../macd_analysis.md
# ### Hop 2:
#   [derived] .../trading_signal.md
```

**Workflow:** topics() → browse() → explore() → recall()

## Configuration

```yaml
# config.yaml
providers:
  # HTTP API
  - pattern: "/live/prices/{symbol}"
    handler: http
    config:
      url: "https://api.example.com/prices/${symbol}"
      headers:
        Authorization: "Bearer ${API_KEY}"
    ttl: 60

  # Script
  - pattern: "/system/status"
    handler: script
    config:
      command: "uptime"

  # Plugin
  - pattern: "/live/indicators/*"
    handler: plugin
    config:
      plugin: "my_plugins.talib"

permissions:
  - pattern: "/memory/*"
    access: rw
  - pattern: "/live/*"
    access: ro

default_access: ro
```

### Handlers

| Handler | Description |
|---------|-------------|
| `file` | Local filesystem |
| `http` | REST API calls |
| `script` | Execute commands |
| `plugin` | Python plugins |
| `sqlite` | Database queries |
| `index` | Structured index with status tracking |

### Index Handler (CLI/MCP only)

Track project files and extract code signatures:

```bash
# Via CLI
avm index scan myapp /path/to/project
avm index status myapp
avm index sigs myapp
```

> Note: Index handler not exposed via FUSE mount, use CLI or MCP.

### Custom Handlers

```python
from avm import BaseHandler, register_handler

class RedisHandler(BaseHandler):
    def read(self, path, context):
        return self.redis.get(path)

register_handler('redis', RedisHandler)
```

## Virtual Nodes

Access metadata via special suffixes:

| Suffix | Read | Write |
|--------|------|-------|
| `:meta` | JSON metadata | Update metadata |
| `:links` | Related nodes | Add links |
| `:tags` | Tags (comma-separated) | Set tags |
| `:shared` | Shared-with agents | Set agents |
| `:ttl` | Time remaining | Set expiration (5m/2h/1d/never) |
| `:history` | Change history (version, time, type) | - |
| `:path` | Relative path | - |
| `:info` | Available suffixes | - |
| `:data` | Raw content | - |
| `:list` | Directory listing | - |
| `:list?limit=N&offset=M` | Paginated listing | - |
| `:list?q=keyword` | Search + list | - |
| `:list?tag=xxx` | Filter by tag | - |
| `:changes?minutes=N` | Recently modified files | - |
| `:delta` | Diff since last read (auto-marks) | - |
| `:mark` | Read position (version) | Update marker |
| `:stats` | Statistics | - |
| `:search?q=` | Search results | - |
| `:recall?q=` | Token-aware recall | - |
| `:inbox` | Unread messages | Mark all read |

## Cross-Agent Messaging (Tell)

Send important messages to other agents:

```bash
# Send urgent message (injected into recipient's next read)
echo "DB schema changed!" > /mnt/avm/tell/kearsarge?priority=urgent

# Send normal message
echo "FYI: New API deployed" > /mnt/avm/tell/kearsarge

# Broadcast to all agents
echo "Team meeting at 3pm" > /mnt/avm/tell/@all

# Check your inbox
cat /mnt/avm/:inbox

# Mark all as read
cat "/mnt/avm/:inbox?mark=read"
```

**Priority levels:**
- `urgent` - Injected into next file read (any file)
- `normal` - Shown in `:inbox`
- `low` - Only shown when explicitly reading `:inbox`

## Two-Phase Retrieval

For large result sets, use two-pe retrieval to save tokens:

```bash
# Phase 1: Get paths + summaries (~200 tokens)
cat "/mnt/avm/memory/:search?q=NVDA"
# → [0.85] /memory/market/NVDA.md
# →     RSI overbought warning...
# → [0.72] /memory/lessons/nvda_q4.md
# →     Down 15% after Q4 earnings...

# Phase 2: Get selected content (~300 tokens)
cat /mnt/avm/memory/market/NVDA.md

# Total: 500 tokens vs 2000 tokens (75% saved)
```

## Linux-Style Permissions

```python
avm.init_permissions({
    "users": {
        "akashi": {
            "groups": ["trading", "admin"],
            "capabilities": ["search_all", "write", "sudo"]
        },
        "guest": {
            "groups": [],
            "capabilities": []
        }
    }
})

# Check permissions
user = avm.get_user("akashi")
avm.check_permission(user, "/memory/private/akashi/note.md", "write")

# API keys for skills
key = avm.create_api_key(user, paths=["/memory/*"], actions=["read"])
```

## Multi-Bot Architecture

```
┌─────────────────────────────────────────┐
│           Application                   │
├─────────────────────────────────────────┤
│ Akashi → avm-mcp --user akashi ─┐       │
│ Yuze   → avm-mcp --user yuze   ─┼─→ DB  │
│ Laffey → avm-mcp --user laffey ─┘       │
└─────────────────────────────────────────┘
```

- Each bot  its own MCP process
- Shared database for cross-bot memory
- Auth at startup, no token per request

## Database

Default location: `~/.local/share/avm/avm.db`

Override:
```bash
avm --db /path/to/custom.db read /memory/note.md
XDG_DATA_HOME=/custom/path avm read /memory/note.md
```

## Versions

- **v0.9.0** - Rename to AVM, FUSE mount with virtual nodes
- **v0.8.0** - Two-pe retrieval (browse + fetch)
- **v0.7.0** - Linux-style permissions, MCP server
- **v0.6.0** - Advanced features (sync, tags, export)
- **v0.5.0** - Multi-agent support
- **v0.4.0** - Agent Memory (token-aware recall)
- **v0.3.0** - Linked Retrieval + Document Synthesis
- **v0.2.0** - Config-driven providers/permissions
- **v0.1.0** - Core VFS

## License

MIT
