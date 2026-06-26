# 🦅 Context-Hawk

> **AI Context Memory Guardian** — Stop losing track, start remembering what matters.

*Give any AI agent a memory that actually works — across sessions, across topics, across time.*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-2026.3%2B-brightgreen)](https://github.com/openclaw/openclaw)
[![ClawHub](https://img.shields.io/badge/ClawHub-context--hawk-blue)](https://clawhub.com)

**English** | [中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Italiano](README.it.md) | [Русский](README.ru.md) | [Português (Brasil)](README.pt-BR.md)

---

## What does it do?

Most AI agents suffer from **amnesia** — every new session starts from zero. Context-Hawk solves this with a production-grade memory management system that automatically captures what matters, lets noise fade away, and recalls the right memory at the right time.

**Without Context-Hawk:**
> "I already told you — I prefer concise replies!"
> (next session, the agent forgets again)

**With Context-Hawk:**
> (silently applies your communication preferences from session 1)
> ✅ Delivers concise, direct response every time

---

## ❌ Without vs ✅ With Context-Hawk

| Scenario | ❌ Without Context-Hawk | ✅ With Context-Hawk |
|----------|------------------------|---------------------|
| **New session starts** | Blank — knows nothing about you | ✅ Injects relevant memories automatically |
| **User repeats a preference** | "I told you before..." | Remembers from day 1 |
| **Long task runs for days** | Restart = start over | Task state persists via `hawk resume` |
| **Context gets large** | Token bill skyrockets, performance drops | 5 compression strategies keep it lean |
| **Duplicate info** | Same fact stored 10 times | SimHash dedup — stored once |
| **Memory recall** | All similar, redundant injection | MMR diverse recall — no repetition |
| **Memory management** | Everything piles up forever | 4-tier decay — noise fades, signal stays |
| **Self-improvement** | Repeats the same mistakes | Tracks importance + access_count → promotes what works |
| **Multi-agent team** | Each agent starts fresh, no shared context | Shared memory (via LanceDB) — all agents learn from each other |

---

## 😰 Pain Points & Solutions

| Pain Point | Impact | Context-Hawk Solution |
|------------|--------|----------------------|
| **AI forgets everything each session** | Users repeat themselves constantly | 4-tier memory decay — important stuff persists |
| **Long-running tasks lost on restart** | Work wasted, context gone | `hawk resume` — task state survives restarts |
| **Context window overflow** | Expensive tokens, slow responses | 5 injection strategies + 5 compression strategies |
| **Memory noise** | Important info buried in chat history | AI importance scoring — auto-discard low-value content |
| **Preferences ignored** | User has to re-explain rules every time | Importance ≥ 0.9 = permanent memory |

**The core value:** Context-Hawk gives your AI agent a memory that actually works — not just storing everything, but intelligently retaining what matters and letting go of what doesn't.

---

## 🎯 5 Core Problems It Solves

**Problem 1: Session context window limits**
Context has a token limit (e.g. 32k). Long history crowds out important content.
→ Context-Hawk compresses/archives old content, injects only the most relevant memories.

**Problem 2: AI forgets across sessions**
When a session ends, context disappears. Next conversation starts fresh.
→ Memories are stored persistently; `hawk recall` retrieves relevant ones for the next session.

**Problem 3: Multiple agents share nothing**
Agent A knows nothing about Agent B's context. Decisions made by one agent are invisible to others.
→ Shared LanceDB memory store (when used with hawk-bridge): all agents read/write to the same store. No silos.

**Problem 4: Context grows too large before sending to LLM**
Recall without optimization = large, repetitive context.
→ After compression + SimHash dedup + MMR: context is **much smaller** before LLM is called, saving tokens and cost.

**Problem 5: Memory never self-manages**
Without management: all messages pile up until context overflows.
→ Auto-extraction → importance scoring → 4-tier decay. Unimportant → delete. Important → promote to long-term.

---

## ✨ 12 Core Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Task State Persistence** | `hawk resume` — persist task state, resume after restart |
| 2 | **4-Tier Memory** | Working → Short → Long → Archive with Weibull decay |
| 3 | **Structured JSON** | Importance scoring (0-10), category, tier, L0/L1/L2 layers |
| 4 | **AI Importance Scoring** | Auto-score memories, discard low-value content |
| 5 | **5 Injection Strategies** | A(high-imp) / B(task) / C(recent) / D(top5) / E(full) |
| 6 | **5 Compression Strategies** | summarize / extract / delete / promote / archive |
| 7 | **Self-Introspection** | Checks task clarity, missing info, loop detection |
| 8 | **LanceDB Vector Search** | Optional — hybrid vector + BM25 retrieval, supports sentence-transformers local embedding |
| 9 | **Pure-Memory Fallback** | Works without LanceDB, JSONL file persistence |
| 10 | **Auto-Dedup** | SimHash-based dedup, removes duplicate memories |
| 11 | **MMR Recall** | Maximal Marginal Relevance — diverse recall, no repetition |
| 12 | **6-Category Extraction** | LLM-powered extraction: fact / preference / decision / entity / task / other |

---

## 🚀 Quick Install

```bash
# One-line install (recommended)
bash <(curl -fsSL https://raw.githubusercontent.com/relunctance/context-hawk/master/install.sh)

# Or via pip directly
pip install context-hawk

# With all features (including sentence-transformers)
pip install "context-hawk[all]"
```

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      Context-Hawk                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Working Memory  ←── Current session (recent 5-10 turns)       │
│       ↓ Weibull decay                                        │
│  Short-term      ←── 24h content, summarized                 │
│       ↓ access_count ≥ 10 + importance ≥ 0.7                │
│  Long-term       ←── Permanent knowledge, vector-indexed      │
│       ↓ >90 days or decay_score < 0.15                      │
│  Archive          ←── Historical, loaded on-demand              │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  Task State Memory  ←── Persistent across restarts (key!)     │
│  - Current task / next steps / progress / outputs           │
├──────────────────────────────────────────────────────────────┤
│  Injection Engine  ←── Strategy A/B/C/D/E decides recall     │
│  Self-Introspection ←── Every answer checks context         │
│  Auto-Trigger       ←── Every 10 rounds (configurable)       │
└──────────────────────────────────────────────────────────────┘
```

---

## 📦 Task State Memory (Most Valuable Feature)

Even after restart, power failure, or session switch, Context-Hawk resumes exactly where it left off.

```json
// memory/.hawk/task_state.jsonl
{
  "task_id": "task_20260329_001",
  "description": "Complete the API documentation",
  "status": "in_progress",
  "progress": 65,
  "next_steps": ["Review architecture template", "Report to user"],
  "outputs": ["SKILL.md", "constitution.md"],
  "constraints": ["Coverage must reach 98%", "APIs must be versioned"],
  "resumed_count": 3
}
```

```bash
hawk task "Complete the documentation"  # Create task
hawk task --step 1 done             # Mark step done
hawk resume                           # Resume after restart ← CORE!
```

---

## 🧠 Structured Memory

```json
{
  "id": "mem_20260329_001",
  "type": "task|knowledge|conversation|document|preference|decision",
  "content": "Full original content",
  "summary": "One-line summary",
  "importance": 0.85,
  "tier": "working|short|long|archive",
  "created_at": "2026-03-29T00:00:00+08:00",
  "access_count": 3,
  "decay_score": 0.92
}
```

### Importance Scoring

| Score | Type | Action |
|-------|------|--------|
| 0.9-1.0 | Decisions/rules/errors | Permanent, slowest decay |
| 0.7-0.9 | Tasks/preferences/knowledge | Long-term memory |
| 0.4-0.7 | Dialog/discussion | Short-term, decay to archive |
| 0.0-0.4 | Chat/greetings | **Discard, never store** |

---

## 🎯 5 Context Injection Strategies

| Strategy | Trigger | Saves |
|----------|---------|-------|
| **A: High-Importance** | `importance ≥ 0.7` | 60-70% |
| **B: Task-Related** | scope match | 30-40% ← default |
| **C: Recent** | last 10 turns | 50% |
| **D: Top5 Recall** | `access_count` top 5 | 70% |
| **E: Full** | no filter | 100% |

---

## 🔍 MMR — Diverse Memory Recall

**MMR (Maximal Marginal Relevance)** solves the "similar memories crowding out diverse ones" problem.

When recalling memories, naive vector search returns the most similar — but they may all be about the same topic. MMR balances:

```
MMR = λ × Relevance(q, doc) − (1−λ) × max(Similarity(doc, already_selected))

λ = 0.7: 70% relevance + 30% diversity
```

**Usage:**
```python
from hawk.similarity import MMR

mmr = MMR(lambda_param=0.7)
selected = mmr.select(query_vector, candidate_vectors, top_k=5)
```

---

## 🗜️ 5 Compression Strategies

`summarize` · `extract` · `delete` · `promote` · `archive`

### Strategy Overview

| Strategy | Trigger | Action |
|----------|---------|--------|
| **summarize** | text > 500 chars | Compress to concise summary via LLM |
| **extract** | any memory | Extract key facts/entities via LLM |
| **delete** | importance < 0.3 + idle > 7 days | Permanently delete |
| **promote** | importance ≥ 0.7 + access ≥ 5 | Upgrade short → long |
| **archive** | tier timeout exceeded | Move to archive tier |

### Usage

```python
from hawk.compression import MemoryCompressor

mc = MemoryCompressor()

# Single memory
mc.summarize("mem_id_abc")
mc.promote("mem_id_abc")

# Batch
mc.compress_all("archive")    # Archive all timed-out memories
mc.compress_all("delete")    # Delete all candidates

# Health report
report = mc.audit()
print(report["candidates"])
# {'to_summarize': [...], 'to_delete': [...], 'to_promote': [...], 'to_archive': [...]}
```

### Thresholds (Configurable)

| Rule | Threshold |
|------|-----------|
| Promote importance | ≥ 0.7 |
| Promote access count | ≥ 5 |
| Delete importance | < 0.3 |
| Delete idle | > 7 days |
| Archive working | > 24 hours |
| Archive short | > 30 days |
| Archive long | > 90 days |

---

## 🔔 4-Level Alert System

| Level | Threshold | Action |
|-------|-----------|--------|
| ✅ Normal | < 60% | Silent |
| 🟡 Watch | 60-79% | Suggest compression |
| 🔴 Critical | 80-94% | Pause auto-write, force suggestion |
| 🚨 Danger | ≥ 95% | Block writes, must compress |

---

## 🧬 SimHash — Auto-Dedup

**SimHash** provides fast duplicate detection for memories using Hamming distance.

- Compute 64-bit fingerprint for each memory text
- Two memories are duplicates if Hamming distance < 3
- O(1) comparison — no need for pairwise vector search

**How it works:**
```
Text → Tokenize → MD5 hash each token → Sum vectors → Fingerprint
```

**Usage:**
```python
from hawk.similarity import SimHash

sh = SimHash()
if sh.is_duplicate(new_text, existing_text, threshold=3):
    print("Duplicate detected, skipping store")
else:
    print("New content, store it")
```

---

## 🚀 Quick Start

```bash
# One-command install (recommended — auto-installs all dependencies)
bash <(curl -fsSL https://raw.githubusercontent.com/relunctance/context-hawk/master/install.sh)

# Activate skill
openclaw skills install ./context-hawk.skill

# Initialize
hawk init

# Core commands
hawk task "My task"    # Create task
hawk resume             # Resume last task ← MOST IMPORTANT
hawk status            # View context usage
hawk compress          # Compress memory
hawk strategy B        # Switch to task-related mode
hawk introspect         # Self-introspection report
```

---

## 📊 Embedding Providers & Graceful Degradation

Context-Hawk works **out of the box without any API key**, and scales up to cloud embeddings when you need higher quality.

### 🔄 Degradation Logic

Context-Hawk auto-detects what's available and degrades gracefully:

```
Has OLLAMA_BASE_URL?       → Full hybrid: vector + BM25 + RRF
Has USE_LOCAL_EMBEDDING=1? → sentence-transformers + BM25 + RRF
Has JINA_API_KEY?          → Jina embeddings + BM25 + RRF
Has MINIMAX_API_KEY?      → Minimax embeddings + BM25 + RRF
Nothing configured?        → BM25-only (pure keyword, no API calls)
```

**No API key = no crash.** It always works — even with zero configuration.

### 📊 Provider Comparison

| Provider | API Key | Quality | Speed | Best For |
|----------|---------|---------|-------|----------|
| **BM25-only** | ❌ | ⭐⭐ | ⚡⚡⚡ | Zero-config, offline |
| **sentence-transformers** | ❌ | ⭐⭐⭐ | ⚡⚡ | Local CPU, privacy-first |
| **Ollama** | ❌ | ⭐⭐⭐⭐ | ⚡⚡⚡⚡ | Local GPU, free |
| **Jina AI** | ✅ free | ⭐⭐⭐⭐ | ⚡⚡⚡⚡ | Free tier, good quality |
| **Minimax** | ✅ | ⭐⭐⭐⭐⭐ | ⚡⚡⚡⚡⚡ | Production, highest quality |

### 🔑 Jina API Key (Recommended Free Option)

Jina AI offers a **generous free tier** — 1M embedding tokens/month, no credit card required.

**Get Your Free Key:**
1. **Register** at https://jina.ai/ (GitHub login supported)
2. **Get Key**: https://jina.ai/settings/ → API Keys → Create API Key
3. **Copy**: starts with `jina_`

> ⚠️ **China users**: `api.jina.ai` is blocked. Set `HTTPS_PROXY` to your proxy URL.

**Configure:**
```bash
mkdir -p ~/.hawk
cat > ~/.hawk/config.json << 'EOF'
{
  "openai_api_key": "jina_YOUR_KEY_HERE",
  "embedding_model": "jina-embeddings-v3",
  "embedding_dimensions": 1024,
  "base_url": "https://api.jina.ai/v1",
  "proxy": "http://YOUR_PROXY_HOST:PORT"
}
EOF
```

> **Why "openai_api_key"?** Jina AI uses an OpenAI-compatible API format, so the config field is reused.

### Free Tier Limits

| | Free Tier |
|--|-----------|
| Embedding | 1M tokens/month |
| Reranker | 10k tokens/month |
|足够了 | ✅ Yes, for personal use |

---

## Auto-Trigger: Every N Rounds

Every **10 rounds** (default, configurable), Context-Hawk automatically:

1. Checks context water level
2. Evaluates memory importance
3. Reports status to user
4. Suggests compression if needed

```bash
# Config (in memory/.hawk/config.json)
{
  "auto_check_rounds": 10,          # check every N rounds
  "keep_recent": 5,                 # preserve last N turns
  "auto_compress_threshold": 70      # compress when > 70%
}
```

---

## File Structure

```
context-hawk/
├── SKILL.md
├── README.md
├── LICENSE
├── scripts/
│   └── hawk               # Python CLI tool
└── references/
    ├── memory-system.md           # 4-tier architecture
    ├── structured-memory.md      # Memory format & importance
    ├── task-state.md           # Task state persistence
    ├── injection-strategies.md  # 5 injection strategies
    ├── compression-strategies.md # 5 compression strategies
    ├── alerting.md             # Alert system
    ├── self-introspection.md   # Self-introspection
    ├── lancedb-integration.md  # LanceDB integration
    └── cli.md                  # CLI reference
```

---

## 🔌 Tech Specs

| | |
|---|---|
| **Persistence** | JSONL local files, no database required |
| **Vector Search** | LanceDB (optional) + sentence-transformers local embedding, auto-fallback to files |
| **Retrieval** | BM25 + ANN vector search + RRF fusion |
| **Embedding Providers** | Ollama / sentence-transformers / Jina AI / Minimax / OpenAI |
| **Cross-Agent** | Universal, no business logic, works with any AI agent |
| **Zero-Config** | Works out-of-the-box with smart defaults (BM25-only mode) |
| **Python** | 3.12+ |
- **Extensible**: Custom injection strategies, compression policies, scoring rules

---



## 🦅 Context-Hawk — Pure Python Memory Package

> **纯 Python 记忆包，零外部依赖，零 API Key，直接 import 就能用**

context-hawk 是一个独立的 Python 包，提供：
- 四层记忆衰减（MemoryManager）
- 向量语义检索（VectorRetriever）
- Markdown 文件导入（MarkdownImporter）
- 上下文压缩（ContextCompressor）
- 记忆提取（Extractor — 支持零 API 关键词模式）
- 自我反思（SelfImproving）
- 系统巡检（Governance）

**不需要 OpenClaw，不需要 API Key**，可嵌入任何 Python 项目。

```bash
pip install lancedb
python3.12 -c "from hawk.memory import MemoryManager; print('OK')"
```

详细文档见 [SKILL.md](SKILL.md)
