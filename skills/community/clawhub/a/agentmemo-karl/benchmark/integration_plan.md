# agentMemo Integration Plan

> Which agents should integrate agentMemo, in what order, and how.

---

## 1. Agent Priority Matrix

| Priority | Agent | Use Case | Memory Schema | Expected Impact | Effort |
|----------|-------|----------|---------------|-----------------|--------|
| 🔴 P0 | **OpenClaw Main Agent (牧牧)** | Decision memory, preference recall, project state | namespace=`openclaw`, tags=`[decision, preference, project, correction]` | High — eliminates repeat Q&A | Low (client already exists) |
| 🔴 P0 | **Cron/Heartbeat Agents** | State tracking across runs, dedup | namespace=`cron_{job_id}`, tags=`[state, checkpoint]` | High — prevents repeated work | Low |
| 🟡 P1 | **Coding Sub-Agents** | Context carry-over between file edits, architecture decisions | namespace=`coding_{repo}`, tags=`[arch, decision, bug, pattern]` | Medium — reduces re-explanation | Medium |
| 🟡 P1 | **RAG Knowledge Agent** | Cache expensive lookups, track query patterns | namespace=`rag_cache`, tags=`[query, source, stale]` | Medium — faster repeat queries | Medium |
| 🟢 P2 | **Discord/Chat Agents** | User preference memory, conversation threading | namespace=`chat_{user_id}`, tags=`[pref, topic, context]` | Medium — personalization | Medium |
| 🟢 P2 | **Research/Report Agents** | Source tracking, finding dedup, insight accumulation | namespace=`research_{topic}`, tags=`[source, finding, insight]` | Low-Medium — better reports | High |

## 2. Memory Schema Design

### Universal Fields
```json
{
  "text": "The actual memory content",
  "namespace": "{agent_type}_{scope}",
  "importance": 0.0-1.0,
  "half_life_hours": 168,
  "tags": ["category", "subcategory"],
  "metadata": {
    "source": "agent_id or channel",
    "session_id": "for traceability",
    "confidence": 0.0-1.0
  }
}
```

### Importance Scoring Guide
| Importance | Use For | Half-life |
|------------|---------|-----------|
| 0.9-1.0 | User corrections, explicit preferences | 720h (30d) |
| 0.7-0.9 | Architecture decisions, project milestones | 336h (14d) |
| 0.5-0.7 | Task status, meeting notes | 168h (7d) |
| 0.3-0.5 | Temporary context, search cache | 72h (3d) |
| 0.1-0.3 | Debug info, one-off references | 24h (1d) |

### Namespace Convention
```
{agent_type}_{scope}
├── openclaw_main          # Main agent global memory
├── openclaw_preferences   # User preferences
├── cron_morning_brief     # Morning brief state
├── cron_goal_progress     # Goal tracking state
├── coding_agentmemo      # agentMemo repo context
├── coding_babastory       # Babastory repo context
├── rag_ai_knowledge       # AI knowledge cache
├── chat_karl              # Karl's chat preferences
└── research_llm_trends    # LLM research accumulation
```

## 3. Integration Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Agent A     │     │  Agent B     │     │  Agent C     │
│  (OpenClaw)  │     │  (Cron)      │     │  (Coding)    │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       │  store/search      │  store/search      │  store/search
       │                    │                    │
       ▼                    ▼                    ▼
┌──────────────────────────────────────────────────────────┐
│                    agentMemo Server                      │
│  ┌─────────────┐  ┌───────────────┐  ┌────────────────┐ │
│  │ Memory CRUD │  │ Hybrid Search │  │ Event Bus      │ │
│  │ + Versions  │  │ (Sem+KW+RRF)│  │ (SSE + WS)    │ │
│  └──────┬──────┘  └──────┬────────┘  └───────┬────────┘ │
│         │                │                    │          │
│  ┌──────▼────────────────▼────────────────────▼────────┐ │
│  │  SQLite (WAL) + HNSW Index + Embedding Cache       │ │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

## 4. Integration Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Memory pollution (bad data stored) | Agent answers based on wrong info | Importance decay + TTL auto-expire + version rollback |
| Latency overhead in hot paths | Slows agent responses | Budget-token search, cache, HNSW approximate search |
| Storage growth (unbounded) | Disk/memory pressure | TTL + decay pruning (auto every 60s), namespace-scoped retention |
| Embedding model memory (~500MB) | RAM pressure on Mac Mini | Shared server (already running), singleton model |
| Single point of failure | All agents lose memory | SQLite WAL is crash-safe, add periodic DB backup to cron |
| Cross-agent memory leaks | Agent A reads Agent B's private data | RBAC namespace isolation (API keys per agent) |

### Rollback Strategy
1. Each agent integration is behind a feature flag (env var `AGENTMEMO_ENABLED=1`)
2. If issues found: set `AGENTMEMO_ENABLED=0` → agent falls back to stateless
3. Memory data preserved in SQLite — can re-enable without data loss
4. Version history allows rollback of individual corrupted memories

## 5. Two-Week Rollout Plan

### Week 1: Foundation
| Day | Task | Deliverable |
|-----|------|-------------|
| D1-D2 | OpenClaw main agent integration | `AGENTMEMO_ENABLED` flag + store/recall in main session |
| D3 | Cron agent memory (heartbeat state) | Replace `heartbeat-state.json` with agentMemo |
| D4 | Add DB backup cron (daily export to JSON) | `cron_backup_vault` job |
| D5 | Integration tests + monitoring | `/metrics` dashboard in daily brief |

### Week 2: Extension
| Day | Task | Deliverable |
|-----|------|-------------|
| D6-D7 | Coding sub-agent memory | Architecture decision recall in code agents |
| D8-D9 | RAG cache integration | Dedup repeated queries, source tracking |
| D10 | Cross-agent event bus | Agents notified of relevant memory changes |

### Success Criteria (End of Week 2)
- [ ] Main agent answers 90%+ context questions without re-asking
- [ ] Cron jobs don't repeat completed work across restarts
- [ ] Coding agents recall architecture decisions from prior sessions
- [ ] No regression in agent response time (P95 < 200ms overhead)
- [ ] DB backup running daily, storage < 100MB

## 6. When to Enable / Disable agentMemo

### Enable When:
- Agent has multi-session workflows (cron, long tasks, project tracking)
- User expects personalization (preferences, coding style)
- Decisions need to be consistent across sessions
- Errors/corrections should persist

### Disable (or skip) When:
- One-shot tasks with no follow-up (single web search, calculation)
- Latency-critical paths where <5ms matters
- Privacy-sensitive data that shouldn't be persisted
- Agent runs < 10 sessions total (not enough memory value)

### Decision Threshold
```
IF (session_count > 10 AND repeated_context_requests > 3):
    ENABLE agentMemo
ELSE:
    Keep stateless (the overhead isn't worth it yet)
```
