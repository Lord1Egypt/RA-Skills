---
name: ClawText Ingest
description: Multi-source memory ingestion with Discord support, automatic deduplication, and agent-ready patterns
keywords: discord, memory, ingestion, rag, agents, deduplication, cli
---

# ClawText Ingest — Production-Ready Memory Ingestion

**Version:** 1.3.0 | **License:** MIT | **Status:** Production ✅  
**Author:** ragesaq | **Category:** Memory & Knowledge Management  
**GitHub:** https://github.com/ragesaq/clawtext-ingest  

---

## 🎯 What It Does

ClawText Ingest transforms external data (Discord forums, files, URLs, JSON, text) into structured, deduplicated memories for AI agents.

### The Problem It Solves

- ❌ **Manual ingestion** — Tedious, error-prone, no metadata
- ❌ **Duplicate memories** — Same data ingested multiple times
- ❌ **Unstructured data** — No hierarchy, no context preservation
- ❌ **One-time imports** — No recurring/scheduled ingestion
- ❌ **Discord-specific gaps** — Can't preserve forum post↔reply structure

### The Solution

✅ **One command** imports from Discord, files, URLs, or JSON  
✅ **100% idempotent** — Run 1000x, zero duplicates  
✅ **Automatic metadata** — YAML frontmatter with date, project, type, entities  
✅ **6 agent patterns** — Autonomous workflows documented and ready  
✅ **Discord-native** — Forum hierarchy preserved, progress bars, auto-batch mode  

---

## ✨ Key Features

### 🎯 Discord Integration (New in v1.3.0)
- **Forum + Channel + Thread** support
- **Hierarchy preservation** — Post↔reply structure in metadata
- **Real-time progress** — Live feedback for large ingestions
- **Auto-batch mode** — <500 posts: full, ≥500 posts: streaming
- **One-command setup** — 5-minute bot creation

### 📁 Multi-Source Ingestion
- **Files** — Glob patterns (Markdown, text, etc.)
- **URLs** — Single or bulk URL ingestion
- **JSON** — Chat exports, API responses
- **Raw text** — Quick knowledge capture
- **Batch operations** — Unified ingestion from multiple sources

### 🔄 Deduplication & Safety
- **SHA1-based** — Cryptographic hash matching
- **100% idempotent** — Safe for repeated runs
- **Configurable** — `checkDedupe: true/false` per operation
- **Zero data loss** — Failed items tracked, fallback per-item ingestion
- **Hash persistence** — `.ingest_hashes.json` for cross-session tracking

### 🤖 Agent-Ready
- **6 documented patterns** — Direct API, Discord Agent, CLI, Cron, Batch, Thread
- **Working code examples** — Copy-paste ready
- **Real-world patterns** — GitHub sync, Discord monitoring, team decisions
- **Error handling** — Comprehensive error recovery
- **Progress callbacks** — Track ingestion in real-time

### 🛠️ Developer-Friendly
- **CLI tool** — `clawtext-ingest` + `clawtext-ingest-discord` commands
- **Node.js API** — Simple imports for programmatic use
- **TypeScript-ready** — Clear method signatures
- **Extensible** — Custom transforms, field mapping
- **Well-documented** — 11 guides, 20+ examples

### 🔗 ClawText Integration
- **Automatic cluster indexing** — New memories indexed after rebuild
- **RAG injection** — Relevant context injected into agent prompts
- **Project routing** — Organize memories by project/source
- **Entity linking** — Auto-extract and link related entities

---

## 🚀 Quick Start

### Installation

```bash
# Via npm
npm install clawtext-ingest

# Via OpenClaw
openclaw install clawtext-ingest
```

### Discord Ingestion (5 minutes)

```bash
# 1. Set up Discord bot (see DISCORD_BOT_SETUP.md)
# 2. Get bot token, set DISCORD_TOKEN env var

# 3. Inspect forum
clawtext-ingest-discord describe-forum --forum-id FORUM_ID --verbose

# 4. Ingest with progress
DISCORD_TOKEN=xxx clawtext-ingest-discord fetch-discord --forum-id FORUM_ID

# 5. Rebuild ClawText clusters
clawtext-ingest rebuild
```

### File Ingestion

```bash
clawtext-ingest ingest-files --input="docs/*.md" --project="docs"
```

### Node.js API

```javascript
import { ClawTextIngest } from 'clawtext-ingest';

const ingest = new ClawTextIngest();

// Ingest files
await ingest.fromFiles(['docs/**/*.md'], { project: 'docs', type: 'fact' });

// Ingest JSON
await ingest.fromJSON(chatArray, { project: 'team' }, {
  keyMap: { contentKey: 'message', dateKey: 'timestamp', authorKey: 'user' }
});

// Rebuild clusters for RAG injection
await ingest.rebuildClusters();
```

---

## 🤖 Agent Integration (6 Patterns)

### Pattern 1: Direct API
**For:** In-agent code  
**Use when:** Agents need to ingest as part of workflow

```javascript
const ingest = new ClawTextIngest();
await ingest.fromFiles(['docs/**/*.md'], { project: 'docs' });
```

### Pattern 2: Discord Agent
**For:** Autonomous Discord ingestion  
**Use when:** Agents need to fetch Discord forums

```javascript
const runner = new DiscordIngestionRunner(ingest);
await runner.ingestForumAutonomous({
  forumId, mode: 'batch', token: process.env.DISCORD_TOKEN
});
```

### Pattern 3: CLI Subprocess
**For:** Agents executing commands  
**Use when:** Simpler CLI-based execution needed

```javascript
await execAsync('clawtext-ingest-discord fetch-discord --forum-id ID');
```

### Pattern 4: Cron/Scheduled
**For:** Recurring tasks  
**Use when:** Daily/hourly ingestion needed

```javascript
cron.schedule('0 * * * *', () => agentIngest());
```

### Pattern 5: Batch Multi-Source
**For:** Unified ingestion  
**Use when:** Multiple sources in one operation

```javascript
await ingest.ingestAll([
  { type: 'files', data: ['docs/**/*.md'], metadata: {...} },
  { type: 'json', data: chatExport, metadata: {...} }
]);
```

### Pattern 6: Discord Thread
**For:** Thread-specific ingestion  
**Use when:** Single thread fetch needed

```javascript
await runner.ingestThread(threadId);
```

**→ See [AGENT_GUIDE.md](https://github.com/ragesaq/clawtext-ingest/blob/main/AGENT_GUIDE.md) for complete examples**

---

## 📊 Real-World Examples

### Example 1: Daily Documentation Sync

```javascript
async function syncDocsDaily() {
  const ingest = new ClawTextIngest();
  const result = await ingest.ingestAll([
    { type: 'files', data: ['docs/**/*.md'], metadata: { project: 'docs' } },
    { type: 'urls', data: ['https://docs.example.com/api'], metadata: { project: 'api-docs' } }
  ]);
  await ingest.rebuildClusters();
  return result;
}
```

### Example 2: Discord Forum Monitoring

```javascript
async function monitorDiscordForum(forumId) {
  const ingest = new ClawTextIngest();
  const runner = new DiscordIngestionRunner(ingest);
  
  const result = await runner.ingestForumAutonomous({
    forumId,
    mode: 'batch',
    token: process.env.DISCORD_TOKEN,
    onProgress: (p) => console.log(`${p.percent}% complete...`)
  });
  
  return result;
}
```

### Example 3: Team Decisions Ingestion

```javascript
async function ingestTeamDecisions() {
  const ingest = new ClawTextIngest();
  
  const result = await ingest.ingestAll([
    { type: 'files', data: ['decisions/adr/**/*.md'], metadata: { type: 'adr' } },
    { type: 'json', data: slackThread, metadata: { type: 'decision', source: 'slack' } }
  ]);
  
  await ingest.rebuildClusters();
  return result;
}
```

---

## 🛒 CLI Commands

### `clawtext-ingest` — File/URL/JSON/Text Ingestion

```bash
clawtext-ingest ingest-files --input="docs/*.md" --project="docs" --verbose
clawtext-ingest ingest-urls --input="https://example.com" --project="research"
clawtext-ingest ingest-json --input=messages.json --source="slack"
clawtext-ingest ingest-text --input="Finding: X is better than Y" --project="findings"
clawtext-ingest batch --config=sources.json
clawtext-ingest rebuild
clawtext-ingest status
```

### `clawtext-ingest-discord` — Discord Integration

```bash
# Inspect forum
clawtext-ingest-discord describe-forum --forum-id FORUM_ID --verbose

# Fetch & ingest
DISCORD_TOKEN=xxx clawtext-ingest-discord fetch-discord \
  --forum-id FORUM_ID \
  --mode batch \
  --batch-size 100 \
  --verbose
```

---

## 📚 Documentation

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **[README.md](https://github.com/ragesaq/clawtext-ingest#readme)** | Overview + quick start | 5 min |
| **[QUICKSTART.md](https://github.com/ragesaq/clawtext-ingest/blob/main/QUICKSTART.md)** | 5-minute setup | 5 min |
| **[AGENT_GUIDE.md](https://github.com/ragesaq/clawtext-ingest/blob/main/AGENT_GUIDE.md)** | 6 autonomous patterns | 10 min |
| **[API_REFERENCE.md](https://github.com/ragesaq/clawtext-ingest/blob/main/API_REFERENCE.md)** | Complete API docs | 15 min |
| **[PHASE2_CLI_GUIDE.md](https://github.com/ragesaq/clawtext-ingest/blob/main/PHASE2_CLI_GUIDE.md)** | CLI commands | 10 min |
| **[DISCORD_BOT_SETUP.md](https://github.com/ragesaq/clawtext-ingest/blob/main/DISCORD_BOT_SETUP.md)** | Bot creation | 5 min |
| **[CLAYHUB_GUIDE.md](https://github.com/ragesaq/clawtext-ingest/blob/main/CLAYHUB_GUIDE.md)** | Publication | 5 min |
| **[INDEX.md](https://github.com/ragesaq/clawtext-ingest/blob/main/INDEX.md)** | Documentation index | 2 min |

---

## 🎯 Who Should Use This

- ✅ **AI/Agent developers** — Building knowledge-aware agents
- ✅ **RAG engineers** — Populating memory for context injection
- ✅ **Teams using Discord** — Leveraging Discord as knowledge base
- ✅ **DevOps/MLOps** — Automated knowledge ingestion pipelines
- ✅ **Researchers** — Structuring unstructured data sources

---

## ⚡ Performance

| Operation | Speed | Notes |
|-----------|-------|-------|
| Ingest 100 files | ~5 sec | With SHA1 dedup check |
| Ingest 1000 JSON items | ~15 sec | Batch processing |
| Small forum (<100 msgs) | ~10 sec | Full mode |
| Large forum (1000+ msgs) | ~2 min | Auto-batch, streaming |
| Rebuild clusters | ~5-30 sec | Depends on total memories |

---

## ✅ Quality Metrics

| Metric | Value |
|--------|-------|
| **Tests** | 22/22 passing ✅ |
| **Code** | 1,254 production lines |
| **Documentation** | 92 KB across 11 guides |
| **Examples** | 20+ working examples |
| **Coverage** | 100% critical paths |

---

## 🔗 Integration with ClawText

1. **Ingest** data → Creates memories with YAML metadata
2. **Rebuild** clusters → ClawText indexes new memories
3. **RAG layer** → Relevant context injected on next prompt
4. **Agent response** — Enhanced with contextual information

```bash
# Complete workflow
clawtext-ingest-discord fetch-discord --forum-id ID  # Step 1
clawtext-ingest rebuild                               # Step 2
# Step 3-4 automatic (ClawText + Agent)
```

---

## 🆘 Support

- **Documentation:** See [INDEX.md](https://github.com/ragesaq/clawtext-ingest/blob/main/INDEX.md) for navigation
- **Issues:** https://github.com/ragesaq/clawtext-ingest/issues
- **Examples:** 20+ examples in documentation
- **Troubleshooting:** Built into each guide

---

## 📦 Installation & Requirements

**Requirements:**
- Node.js ≥ 18.0.0
- OpenClaw (for agent patterns)
- ClawText ≥ 1.2.0 (for RAG integration)

**Installation:**
```bash
npm install clawtext-ingest
# or
openclaw install clawtext-ingest
```

**Binaries:**
- `clawtext-ingest` — File/URL/JSON ingestion
- `clawtext-ingest-discord` — Discord integration

---

## 🚀 Why This Over Alternatives

| Feature | ClawText-Ingest | Manual | Generic Importer | API Tool |
|---------|---|---|---|---|
| Discord native | ✅ | ❌ | ❌ | ❌ |
| Deduplication | ✅ | ❌ | Partial | ❌ |
| Agent patterns | ✅ | ❌ | ❌ | ❌ |
| Metadata auto | ✅ | ❌ | Partial | ❌ |
| ClawText integration | ✅ | ❌ | ❌ | ❌ |
| Idempotent | ✅ | ❌ | ❌ | Partial |

---

## 📄 License

MIT — Use freely, open source, community supported

---

## 🙌 Contributing

Contributions welcome! See GitHub issues for current priorities.

---

**Ready to ingest? Start with [QUICKSTART.md](https://github.com/ragesaq/clawtext-ingest/blob/main/QUICKSTART.md) (5 min) or [AGENT_GUIDE.md](https://github.com/ragesaq/clawtext-ingest/blob/main/AGENT_GUIDE.md) if you're building agents.**
