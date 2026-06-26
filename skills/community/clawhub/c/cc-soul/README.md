# cc-soul

> Zero-vector AI memory engine that learns from every conversation.
> LOCOMO benchmark: **4th place (76.2%)** — the only symbolic system in the top 5.

```bash
npm install @cc-soul/openclaw
```

100% local memory. Zero cloud upload. Zero telemetry. Zero vectors. Zero embeddings. Zero GPU. **Open source (MIT).**

---

## Why cc-soul?

| | cc-soul | ChatGPT Memory | Google Gemini |
|---|---------|---------------|---------------|
| **Data location** | Your device (SQLite) | OpenAI cloud | Google cloud |
| **Upload** | Never | Always | Always |
| **GDPR compliance** | By design | Fined €15M (Italy) | Requires opt-in (EU) |
| **Works offline** | Yes | No | No |
| **Memory engine** | 17 original algorithms (cognitive science) | Vector search | Vector search |
| **Recall latency** | <30ms (local) | Network-dependent | Network-dependent |
| **Vendor lock-in** | None — works with any AI | OpenAI only | Google only |
| **User data training** | Impossible (no server) | Opt-out required | Opt-out required |

---

## How It Works — No Vectors, No Embeddings, No Cloud

cc-soul doesn't use vector databases or embedding models. Instead, it's built on **cognitive science** — memories aren't "searched", they surface automatically, like the human brain.

**Five core systems:**

**1. AAM (Adaptive Associative Memory) — Self-Learning**

cc-soul builds a word association network from your conversations. The more you talk, the smarter recall becomes.
- Every message updates word co-occurrence statistics (PMI-based)
- Search "marathon" → AAM auto-expands to "running", "race", "training" — learned from YOUR data
- Strong associations auto-promote to synonym table (zero manual maintenance)
- Learning curve: Hit@3 improves 30% → 67.5% over 1200 messages (+37.5%)

**2. NAM (Neural Activation Memory) — 9-12 Signal Fusion**

Each memory has a real-time activation score computed from: base activation (ACT-R), context match (BM25+), emotion resonance, spreading activation, interference suppression (MMR), temporal encoding, and sequential co-occurrence (PAM).

**3. Three-Layer Distillation**

Raw memories (L1) cluster into topic nodes with hit/miss scoring (L2), which distill into a 4-section mental model (L3: identity / style / facts / dynamics). Low-scoring topics auto-retire. High-scoring ones promote to core memory.

**4. PADCN Emotion System — 5-Dimensional Mood Tracking**

Tracks user emotion across Pleasure / Arousal / Dominance / Certainty / Novelty. Mood-congruent recall: happy → recalls happy memories. Flashbulb effect: highly emotional memories stored stronger. Emotion drives persona selection automatically.

**5. 11 Auto-Switching Personas**

Dynamically blends personas based on context: engineer, friend, mentor, analyst, comforter, strategist, explorer, executor, teacher, devil's advocate, socratic. No manual switching — adapts automatically.

**Self-Learning Feedback Loop**: AAM learns from every message → Recall Thermostat adjusts signal weights → Topic Tournament retires bad summaries → PMI Graduation promotes strong associations → Correction Learning verifies over 3 conversations. The system gets measurably better over time.

**Zero-LLM Recall** — Memory retrieval needs no AI model. Core recall runs in <30ms on pure algorithms. LLM is optional (adds query rewriting + reranking).

---

## Quick Start

```bash
npm install @cc-soul/openclaw
# API starts at localhost:18800
```

---

## API — Just Two Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/memories` | Store a memory |
| `POST` | `/search` | Search memories |
| `GET` | `/health` | Health check |

That's it. Store and retrieve. Everything else (learning, distillation, decay, dedup) happens automatically in the background.

### POST /memories — Store

```bash
curl -X POST http://localhost:18800/memories \
  -H "Content-Type: application/json" \
  -d '{"content": "I deployed on AWS us-east-1, port 8080, Python 3.11", "user_id": "alice"}'
```

Response:
```json
{"stored": true, "facts_extracted": 3}
```

Facts are automatically extracted and indexed. AAM learns word associations. No extra calls needed.

### POST /search — Retrieve

```bash
curl -X POST http://localhost:18800/search \
  -H "Content-Type: application/json" \
  -d '{"query": "server config", "user_id": "alice"}'
```

Response:
```json
{
  "memories": [
    {"content": "I deployed on AWS us-east-1, port 8080, Python 3.11", "scope": "fact", "ts": 1712534400, "confidence": 0.85}
  ],
  "facts": [
    {"predicate": "deployed_on", "object": "AWS us-east-1", "confidence": 0.9}
  ],
  "fact_summary": "Deployed on AWS us-east-1 with Python 3.11",
  "_meta": {"reranked": false, "query_rewritten": false}
}
```

Parameters:
- `query` — what to search for (required)
- `user_id` — user identifier (default: "default")
- `top_n` / `limit` — number of results (default: 5)

### GET /health

```bash
curl http://localhost:18800/health
# → {"status": "ok", "version": "2.9.2", "memoryCount": 5231, "factCount": 892, "llm": {"configured": true}}
```

---

## LLM Configuration (Optional)

cc-soul works **without any LLM** — NAM recall runs purely on local algorithms (<30ms). If you add an LLM, you get two bonus features:

- **Query Rewrite** — abstract queries ("What are my habits?") get expanded with specific keywords before search
- **LLM Rerank** — NAM recalls 4x candidates, LLM picks the most relevant ones

### Setup

After install, cc-soul auto-creates a config template at `~/.cc-soul/data/ai_config.json`. Just fill in three fields:

```json
{
  "backend": "openai-compatible",
  "api_base": "https://api.deepseek.com/v1",
  "api_key": "sk-xxx",
  "api_model": "deepseek-chat"
}
```

Any OpenAI-compatible API works:

| Provider | api_base | api_model |
|----------|----------|-----------|
| DeepSeek | `https://api.deepseek.com/v1` | `deepseek-chat` |
| OpenAI | `https://api.openai.com/v1` | `gpt-4o-mini` |
| Claude | `https://api.anthropic.com/v1` | `claude-sonnet-4-20250514` |
| Ollama (local) | `http://localhost:11434/v1` | `qwen2.5:7b` |

Config is hot-reloaded — save the file and cc-soul picks it up automatically, no restart needed.

---

## How to Integrate

### Python

```python
import requests

API = "http://localhost:18800"

# Store memories from conversations
requests.post(f"{API}/memories", json={
    "content": "User prefers Python over Java, deployed on AWS",
    "user_id": "alice"
})

# Later: retrieve relevant memories
results = requests.post(f"{API}/search", json={
    "query": "what language does alice prefer?",
    "user_id": "alice"
}).json()

# Feed memories to your AI
from openai import OpenAI
client = OpenAI()
memory_context = "\n".join([m["content"] for m in results["memories"]])
reply = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": f"User context:\n{memory_context}"},
        {"role": "user", "content": "What language should I use for this project?"}
    ]
).choices[0].message.content
```

### JavaScript / Node.js

```javascript
const API = "http://localhost:18800"

// Store
await fetch(`${API}/memories`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ content: "Likes spicy food, lives in Berlin", user_id: "bob" })
})

// Search
const res = await fetch(`${API}/search`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ query: "food preferences", user_id: "bob" })
})
const { memories, facts } = await res.json()
```

### cURL

```bash
# Store
curl -X POST http://localhost:18800/memories \
  -H "Content-Type: application/json" \
  -d '{"content": "Meeting with John next Tuesday at 3pm", "user_id": "alice"}'

# Search
curl -X POST http://localhost:18800/search \
  -H "Content-Type: application/json" \
  -d '{"query": "upcoming meetings", "user_id": "alice"}'

# Health
curl http://localhost:18800/health
```

---

## What Happens Automatically

You only call two endpoints. Behind the scenes, cc-soul runs a full cognitive pipeline:

```
POST /memories → store → dedup → fact extraction → AAM association learning
                                                          ↓
                          ┌─────────── background ───────────────┐
                          │ every minute:  memory decay           │
                          │ every hour:    FSRS consolidation     │
                          │ every 6h:     L1→L2 topic clustering  │
                          │ every 12h:    L2→L3 mental model      │
                          │ every 24h:    full L3 refresh         │
                          └──────────────────────────────────────┘
                                                          ↓
POST /search  → NAM 7-signal activation → MMR dedup → coverage rerank
                (+ LLM rewrite & rerank if configured)
```

---

## Core Scenarios

### 1. Proactive Expansion + Association Chain

```
You:  "Fix this connection timeout error"
AI:   Fixes the error. Then:
      "I noticed 3 related issues:
       1. Your connection pool is 5 but you run 20 workers — bottleneck
       2. No retry logic on transient failures
       3. The timeout is 3s but your DB query p99 is 2.8s"
```

cc-soul doesn't just answer — it recalls your past context and anticipates what you'll need next. It expands across 22 tech domains and 11 life domains.

### 2. Socratic Teaching

```
You:  "帮我理解 what is a closure?"
AI:   Doesn't give the answer. Instead:
      "When a function returns another function, what happens
       to the variables in the outer scope? Try this:
       function outer() { let x = 1; return () => x; }
       What do you think outer()() returns, and why?"
```

Trigger words: `帮我理解`, `引导我`, `教我`, `别告诉我答案`, `guide me`, `help me understand`

### 3. Correction Verification

```
You:  "Python's GIL was removed in 3.11. Update your knowledge."
AI:   "I'm not going to update that — it's not accurate.
       PEP 703 shipped in Python 3.13, not 3.11. Even in 3.13,
       the GIL is still the default. I verify corrections
       before accepting them."
```

When you say "that's wrong", cc-soul checks facts first. If you're right, it learns. If you're wrong, it counters with evidence. Rules are verified over 3 conversations before becoming permanent (Bayesian hypothesis testing).

### 4. Persistent Memory

```
You:  "I deployed the backend on AWS us-east-1, port 8080, Python 3.11"
AI:   Stored.

[3 weeks later]

You:  "What server did I set up?"
AI:   "AWS us-east-1, port 8080, Python 3.11 — about 3 weeks ago."
```

10,000+ memories with auto-dedup, contradiction detection, 3-tier time decay (HOT/WARM/COLD), and smart forget (Weibull survival + ACT-R activation).

### 5. Emotion + 11 Personas

```
You:  "This code keeps segfaulting"
AI:   [engineer mode] Analyzes the crash, suggests fixes.

You:  "I'm stressed about the deadline"
AI:   [comforter mode] Acknowledges feelings, offers practical help.

You:  "Should I use Redis or Memcached?"
AI:   [analyst mode] Compares both with pros/cons.
```

5-dimension emotion model (Pleasure/Arousal/Dominance/Certainty/Novelty). 11 personas auto-switch by context: engineer, friend, mentor, analyst, comforter, strategist, explorer, executor, teacher, devil's advocate, socratic.

### 6. Life Assistant

```
You:  "打卡 exercise"          → "Exercise: Day 12 streak!"
You:  "新目标 Launch MVP by April" → Goal created with progress tracking.
You:  "提醒 09:00 standup"      → Daily reminder set.
You:  "晨报"                   → Morning briefing with goals, reminders, mood.
You:  "周报"                   → Weekly review with trends and insights.
```

---

## What's Running Behind the Scenes (43 always-on features)

All automatic. No setup, no toggles. Works from the first message.

**Memory (NAM Engine)**
- Every message auto-extracted for facts, preferences, events
- NAM 7-signal activation field — memories surface by relevance, not keyword match
- Contradiction detection — catches when you contradict yourself
- Smart decay (Weibull + ACT-R) — unused memories fade, important ones strengthen
- Memory compression — 90-day+ memories distilled into summaries
- WAL protocol — key facts persisted before AI replies (crash-safe)
- DAG archive — lossless archival replaces hard deletion
- Associative recall — one memory activates related ones
- Predictive recall — pre-warms memories based on conversation patterns

**Understanding**
- 7-dimension deep understanding — temporal patterns, growth trajectory, cognitive load, stress fingerprint, say-do gap, unspoken needs, dynamic profile
- Theory of mind — tracks your beliefs, knowledge gaps, frustrations
- Decision causal recording — stores WHY you chose, not just what
- Value conflict learning — tracks which values you prioritize in tradeoffs
- Social context adaptation — adjusts tone when you mention boss vs friend
- Person model — identity, thinking style, communication decoder ("算了" → "换个角度")
- Expression fingerprint — learns your argument style and certainty level

**Personality & Emotion**
- 11 personas auto-blend by context — like a friend who adjusts their tone naturally
- Emotion tracking — senses your mood from messages, adapts in real time
- Your mood affects AI's mood — just like talking to a real person
- Late night = concise replies, Monday morning = gentle start

**Proactive Intelligence**
- Proactive expansion — adds related pitfalls after answering
- Absence detection — notices topics you stopped mentioning
- Behavior prediction — warns when you're about to repeat a past mistake
- Proactive questioning — asks about knowledge gaps it detects
- Follow-up tracking — "I'll do it tomorrow" → next day reminder
- Soul moments — naturally references shared history at milestones

**Infrastructure**
- Knowledge graph — entities and relationships auto-extracted
- Context compression — long conversations auto-compressed to save tokens
- Quality scoring — learns which response style works for you
- LLM batch queue — non-urgent tasks queued for off-hours
- Habit/goal/reminder tracking
- Cost tracking — token usage per conversation

**6 optional features** (user can toggle): `auto_daily_review` · `self_correction` · `memory_session_summary` · `absence_detection` · `behavior_prediction` · `auto_mood_care`

---

## Privacy & Security

All data stored locally in `~/.cc-soul/data/` (SQLite). Auto-detected, auto-created. Nothing ever leaves your machine. No telemetry.

- **Privacy mode** — say `隐私模式` to pause all memory storage
- **PII filtering** — auto-strips emails, phone numbers, API keys, IPs
- **Prompt injection detection** — 9 pattern filters
- **Immutable audit log** — SHA256 chain-linked operation history
- **MCP rate limiting** — prevents abuse from external agents
- **Full data export** — `导出全部` exports everything to a single JSON you own

See SECURITY.md for full details.

---

## Commands (48 total)

### Memory
| Command | What it does |
|---------|-------------|
| `我的记忆` / `my memories` | View recent memories |
| `搜索记忆 <词>` / `search memory <kw>` | Search memories |
| `删除记忆 <词>` / `delete memory <kw>` | Remove matching memories |
| `pin 记忆 <词>` / `pin memory <kw>` | Pin memory (never decays) |
| `unpin 记忆 <词>` | Unpin memory |
| `恢复记忆 <词>` / `restore memory <kw>` | Restore deleted memory |
| `记忆时间线 <词>` / `memory timeline <kw>` | Timeline view of a topic |
| `记忆链路 <词>` / `memory chain <kw>` | Show association chain |
| `记忆健康` / `memory health` | Memory health stats |
| `记忆审计` / `memory audit` | Memory audit report |
| `共享记忆 <词>` / `share memory <kw>` | Mark memory as shared |
| `私有记忆 <词>` / `private memory <kw>` | Mark memory as private |
| `别记这个` / `don't remember` | Skip storing next message |
| `隐私模式` / `privacy mode` | Pause all memory storage |
| `可以了` / `关闭隐私` | Resume memory storage |

### Import / Export
| Command | What it does |
|---------|-------------|
| `导出全部` / `export all` | Full backup to JSON |
| `导入全部 <路径>` / `import all <path>` | Restore from backup |
| `导出lorebook` / `export lorebook` | Export lorebook |
| `导出进化` / `export evolution` | Export evolution data |
| `导入进化 <路径>` / `import evolution <path>` | Import evolution data |
| `摄入文档 <路径>` / `ingest <path>` | Import document to memory |

### Context & Topics
| Command | What it does |
|---------|-------------|
| `保存话题` / `save topic` | Save current topic |
| `切换话题 <名>` / `switch topic <name>` | Switch to saved topic |
| `话题列表` / `topic list` | List saved topics |
| `对话摘要` / `conversation summary` | Summarize current conversation |
| `当聊到X时提醒我Y` | Context-triggered reminder |

### Insights
| Command | What it does |
|---------|-------------|
| `时间旅行 <词>` / `time travel <kw>` | Explore memory history |
| `推理链` / `reasoning chain` | Show reasoning chain |
| `情绪锚点` / `emotion anchors` | Show emotional anchor points |
| `记忆图谱 html` / `memory map html` | Visual knowledge graph |

### Status & Analytics
| Command | What it does |
|---------|-------------|
| `help` / `帮助` | Full command guide |
| `stats` | Dashboard — messages, memories, quality, mood |
| `soul state` / `灵魂状态` | AI energy, mood, emotion vector |
| `情绪周报` / `mood report` | 7-day emotional trend |
| `能力评分` / `capability score` | Domain confidence scores |
| `我的技能` / `my skills` | Skill assessment |
| `metrics` / `监控` | Runtime metrics |
| `cost` / `成本` | Token usage statistics |
| `dashboard` / `仪表盘` | Web dashboard |

### Persona & Identity
| Command | What it does |
|---------|-------------|
| `人格列表` / `personas` | List all 11 personas |
| `价值观` / `values` | Show value priorities |
| `我是 <名字>` | Set your identity |
| `灵魂模式` | Enter soul reply mode |

### Advanced
| Command | What it does |
|---------|-------------|
| `功能状态` / `features` | View feature toggles |
| `开启 <X>` / `关闭 <X>` | Enable/disable feature |
| `开始实验 <描述>` | Start an experiment |
| `安装向量` / `vector status` | Vector search status |

---

---

## Benchmark — LOCOMO Leaderboard

cc-soul is the **only symbolic (non-vector) system** in the top 5.

| Rank | System | Score | Architecture |
|------|--------|-------|-------------|
| 1 | Backboard | 90.0% | Vector + LLM |
| 2 | Hindsight | 89.6% | Vector + LLM |
| 3 | ENGRAM | 77.6% | Vector + LLM |
| **4** | **cc-soul** | **76.2%** | **Symbolic (no vectors)** |
| 5 | Memobase | 75.8% | Vector + LLM |
| 6 | Zep | 75.1% | Vector + LLM |
| 7 | Letta | 74.0% | Vector + LLM |
| 8 | Mem0-Graph | 68.4% | Vector + Graph |
| 9 | Mem0 | 66.9% | Vector + LLM |

### Breakdown by Question Type

| Type | Accuracy |
|------|----------|
| open_domain | 89.4% |
| single_hop | 84.8% |
| multi_hop | 65.7% |
| temporal_reasoning | 62.5% |
| adversarial | 56.5% |
| **TOTAL** | **76.2%** |

### Performance

| Metric | Value |
|--------|-------|
| Recall latency (p50) | 127ms |
| Storage size | 5.7 MB (vs 49.2 MB for vectors — 8.6x smaller) |
| External API calls | 0 (pure algorithm) |
| LLM dependency | Optional (recall works without LLM) |

### Learning Curve (1200 messages)

| Metric | Start | End | Improvement |
|--------|-------|-----|-------------|
| Hit@3 | 30.0% | 67.5% | +37.5% |
| Top-1 | 22.5% | 60.0% | +37.5% |

---

## Technical Specs

| | |
|---|---|
| Modules | 75 |
| Original algorithms | 15 |
| Codebase | 29K+ lines |
| Dependencies | Zero vectors, zero embeddings, zero GPU |
| Storage | SQLite (local) |
| LLM support | DeepSeek / Claude / any OpenAI-compatible API |
| Minimum requirements | Standard CPU, 8GB RAM |

---

**NAM memory engine · 15 original algorithms · 127ms p50 recall · works with or without LLM · 100% local**

[npm](https://www.npmjs.com/package/@cc-soul/openclaw) · [GitHub](https://github.com/wenroudeyu-collab/cc-soul) · wenroudeyu@gmail.com · MIT License

*Your AI remembers everything — and tells no one.*
