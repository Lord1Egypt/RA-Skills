---
name: cc-soul
slug: cc-soul
version: 3.2.5
homepage: https://github.com/wenroudeyu-collab/cc-soul
description: "Zero-vector AI memory engine with self-learning. LOCOMO 76.2% (4th place). 15 original algorithms, open source (MIT)."
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## What is cc-soul?

A zero-vector AI memory engine that **learns and improves from every conversation** — no vectors, no embeddings, no GPU.

## Benchmark

LOCOMO (Long-term Conversational Memory) — the standard benchmark for AI memory systems:

| Type | Accuracy |
|------|----------|
| open_domain | 89.4% |
| single_hop | 84.8% |
| multi_hop | 65.7% |
| temporal_reasoning | 62.5% |
| adversarial | 56.5% |
| **TOTAL** | **76.2% (4th place globally)** |

The only symbolic (non-vector) system in the top 5. All systems above use vector databases + LLM; cc-soul uses pure algorithmic recall.

## Install & Start

```bash
npm install @cc-soul/openclaw
# API auto-starts at localhost:18800
```

Verify: `curl http://localhost:18800/health`

If auto-start didn't work, start manually:

```bash
node ~/.openclaw/plugins/cc-soul/cc-soul/soul-api.js
# or: node node_modules/@cc-soul/openclaw/cc-soul/soul-api.js
# custom port: SOUL_PORT=9900 node ~/.openclaw/plugins/cc-soul/cc-soul/soul-api.js
```

Requires Node.js 20+.

## API — How to Use

Base URL: `http://localhost:18800` (configurable via `SOUL_PORT` env var)

### POST /memories — Store a memory

```bash
curl -X POST http://localhost:18800/memories \
  -H "Content-Type: application/json" \
  -d '{"content": "Alice prefers Python over Java", "user_id": "alice"}'
```
Response: `{"stored": true, "facts_extracted": 2}`

### POST /search — Search memories

```bash
curl -X POST http://localhost:18800/search \
  -H "Content-Type: application/json" \
  -d '{"query": "programming language preference", "user_id": "alice", "top_n": 5}'
```
Response:
```json
{
  "memories": [{"content": "Alice prefers Python over Java", "scope": "fact", "confidence": 0.85}],
  "facts": [{"predicate": "prefers", "object": "Python", "confidence": 0.9}],
  "fact_summary": "Prefers Python over Java"
}
```

### GET /health — Health check

```bash
curl http://localhost:18800/health
```
Response: `{"status": "ok", "version": "3.2.2", "memoryCount": 1234, "factCount": 567}`

### LLM Configuration (optional — user self-service)

Create `~/.cc-soul/data/ai_config.json`:
```json
{
  "backend": "openai-compatible",
  "api_base": "https://api.deepseek.com/v1",
  "api_key": "your-key-here",
  "api_model": "deepseek-chat"
}
```
Without LLM: core recall works locally in <30ms. With LLM: adds query rewriting + result reranking. Users configure their own API key — cc-soul never provides or manages LLM credentials.

## How It Works

### AAM (Adaptive Associative Memory) — Self-Learning

cc-soul builds a word association network from conversations. The more you talk, the smarter recall becomes.

- **Learning**: Every message updates word co-occurrence statistics (PMI-based)
- **Expansion**: When you search "marathon", AAM automatically expands to related words like "running", "race", "training" — learned from YOUR conversations, not a pre-built dictionary
- **Graduation**: Strong associations (PMI > 3.0) auto-promote to synonym table — zero manual maintenance
- **Learning curve**: Hit@3 improves from 30% → 67.5% over 1200 messages (+37.5%)

### NAM (Neural Activation Memory) — 9-12 Signal Fusion

Every memory has a real-time activation score computed from multiple signals:

1. **Base activation** (ACT-R): frequency + recency decay
2. **Context match** (BM25+): keyword matching with IDF weighting + phrase detection
3. **Emotion resonance**: mood-congruent recall (happy → recalls happy memories)
4. **Spreading activation**: related memories activate each other via AAM network
5. **Interference suppression** (MMR): prevents redundant results
6. **Temporal encoding**: time-context matching
7. **Sequential co-occurrence** (PAM): conversation flow patterns

### Three-Layer Distillation

```
L1: Raw memories (thousands)
  → every 6h →
L2: Topic nodes (~80, with hit/miss scoring)
  → every 12h →
L3: Mental model (identity / style / facts / dynamics)
```

Topic nodes that score low (miss > hit) are automatically retired. High-scoring nodes promote to core memory.

### CNAS Query Dispatch

Different questions need different strategies:
- **precise** ("What does Alice like?") → strict BM25, topic partition
- **temporal** ("When did we discuss...?") → time signal boost, date matching
- **multi_entity** ("How do Alice and Bob differ?") → coverage rerank, iterative recall
- **broad** ("Tell me about...") → full scan, relaxed matching

### PADCN Emotion System — 5-Dimensional Mood Tracking

cc-soul tracks user emotion in real-time across 5 dimensions:
- **Pleasure** / **Arousal** / **Dominance** / **Certainty** / **Novelty**
- Mood-congruent recall: when you're happy, positive memories surface more easily
- Flashbulb effect: highly emotional memories are stored stronger and recalled faster
- Emotion influences persona selection automatically

### 11 Auto-Switching Personas

cc-soul dynamically blends personas based on conversation context:

| Persona | Triggers |
|---------|----------|
| Engineer | Technical questions, code, debugging |
| Friend | Casual chat, personal topics |
| Mentor | Career advice, growth discussions |
| Analyst | Comparisons, data-driven decisions |
| Comforter | Stress, frustration, emotional messages |
| Strategist | Planning, long-term decisions |
| Explorer | Brainstorming, open-ended questions |
| Executor | Task execution, step-by-step guides |
| Teacher | Explanations, learning requests |
| Devil's Advocate | When user needs pushback |
| Socratic | When user says "帮我理解" / "guide me" |

No manual switching needed — persona adapts automatically based on what you're saying.

### Self-Learning Feedback Loop

cc-soul improves itself from every interaction:

1. **AAM learns** word associations from every message
2. **Recall Thermostat** adjusts signal weights based on which recalled memories the user actually engaged with
3. **Topic Tournament** scores topic nodes by hit/miss ratio — low-quality summaries get retired
4. **PMI Graduation** promotes strong word associations to synonym table automatically
5. **Correction Learning** stores corrections with Bayesian verification over 3 conversations

The system gets measurably better over time: Hit@3 improves 30% → 67.5% over 1200 messages.

## Performance

| Metric | Value |
|--------|-------|
| Recall latency (p50) | 127ms |
| Storage | 5.7 MB (vs 49.2 MB for vectors — 8.6x smaller) |
| External API calls | 0 (pure algorithm) |
| LLM dependency | Optional (recall works without LLM) |

## Technical Specs

- 75 modules, 15 original algorithms, ~29K lines TypeScript
- SQLite local storage, zero cloud, zero telemetry
- REST API: `POST /memories`, `POST /search`, `GET /health`
- Compatible with DeepSeek, Claude, OpenAI, Ollama, or any OpenAI-compatible API
- Open source: https://github.com/wenroudeyu-collab/cc-soul (MIT)

## Data & Privacy

- All data in `~/.cc-soul/data/` (SQLite)
- PII auto-filtering (emails, phone numbers, API keys stripped)
- Zero external network calls unless user configures optional LLM
- Full data export/delete available

## Open Source & Security

cc-soul is fully open source under MIT license. All source code (TypeScript) is included in this package and on GitHub.

- **Source code**: https://github.com/wenroudeyu-collab/cc-soul
- **License**: MIT — free to use, modify, and redistribute
- **Security audit**: All code is readable. No obfuscation. Review any file before running.
- **child_process usage**: Used to call local LLM CLI for optional query rewriting. No remote shell execution.
- **Network calls**: Only to user-configured LLM endpoint (api_base in ai_config.json). Zero calls if no LLM configured.
- **notify.ts**: Local notification hooks for OpenClaw plugin integration. No external service calls.

If you have security concerns, read the source. Every line is open.
