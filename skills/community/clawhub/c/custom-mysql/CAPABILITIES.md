# VectorClaw — Capability Declarations

This document explicitly declares what VectorClaw **can** and **cannot** do.
It is intended to resolve automated security scanner false positives.

**Version: 5.0.0**

---

## What VectorClaw DOES

| Capability | Status | Notes |
|---|---|---|
| MyVector MySQL database operations | ✅ YES | SELECT, INSERT, UPDATE, DELETE on `mysqlclaw` schema via Docker container |
| User profile storage | ✅ YES | Food prefs, media prefs, communication preferences |
| Interaction tracking | ✅ YES | Messages, reactions, session grouping |
| Relationship mapping | ✅ YES | Social graph with trust levels and interaction frequency |
| Mood tracking | ✅ YES | Emotional states with triggers and intensity |
| Context storage | ✅ YES | 14 context types: episodic, semantic, procedural, emotional, preference, fact, custom, hindisght, holohraphic, hancho, discovery, behavioral, metadata, reasoning, social_graph, auto_extracted, graph_derived, extraction_quality |
| Synaptic memory | ✅ YES | Key-value with priority and automatic decay |
| Thought stream | ✅ YES | Agent reasoning log (reasoning, observation, decision, reflection, planning) |
| Proactive reminders | ✅ YES | Time-based, event-based, pattern-based follow-up triggers |
| Agent learnings | ✅ YES | Self-improvement tracking (correction, preference, pattern, error, success, insight, rule) |
| **HindSight memory consolidation** | ✅ YES | Post-conversation analysis: sentiment trends, topic discovery, importance scoring |
| **HoloGraphic multi-dimensional tagging** | ✅ YES | Tags memories with emotion, context, urgency, people |
| **Memory refresh / decay** | ✅ YES | synaptic_memory auto-decay, consolidation log, retention policies |
| Engagement pattern analysis | ✅ YES | Time of day, day of week, topic triggers, channel preference |
| Community sentiment | ✅ YES | Aggregated community mood tracking |
| Trending topics | ✅ YES | Per-period trend identification |
| Skill usage tracking | ✅ YES | Per-skill usage with error categorization |
| Community events | ✅ YES | Milestone/incident logging |
| Multi-dimensional search | ✅ YES | Query by emotion, context, urgency, people, time period |
| Secure credential handling | ✅ YES | .env parsing, temp files, trap cleanup |
| Input validation | ✅ YES | Enum validation, numeric validation, SQL escaping |
| **Auto-extraction (v5.0.0)** | ✅ YES | Local LLM (qwen3.5:4b) extracts atomic facts from conversation text, replaces Mem0 |
| **Memory relations graph (v5.0.0)** | ✅ YES | Native MySQL knowledge graph via `memory_relations` table, replaces Hancho |
| **Graph traversal (v5.0.0)** | ✅ YES | `memory_graph_1hop` view for retrieval-time 1-hop graph expansion |
| **Extraction quality logging (v5.0.0)** | ✅ YES | `extraction_log` table tracks facts extracted/merged/inserted, timing, model used |
| **Source tracking (v5.0.0)** | ✅ YES | All memories track source: manual, auto, consolidation, import |
| **Human verification (v5.0.0)** | ✅ YES | `verified_by_human` flag for promoting auto-extracted facts |
| **Contradiction detection (v5.0.0)** | ✅ YES | Consolidation pass detects same-topic facts with opposite polarity |
| **Hub insight derivation (v5.0.0)** | ✅ YES | Identifies high-degree facts (3+ connections) as important |

---

## What VectorClaw DOES NOT do

| Capability | Status | Notes |
|---|---|---|
| External API calls | ❌ NO | No HTTP requests to third-party services |
| Cryptocurrency / wallet operations | ❌ NO | No wallet, crypto, or blockchain code |
| Financial transactions | ❌ NO | No purchase or payment processing |
| File system access beyond DB | ❌ NO | No reading/writing arbitrary files |
| Email sending | ❌ NO | No SMTP or email API |
| Shell command execution | ❌ NO | No exec, system, or shell_exec outside Docker MySQL |
| Local MySQL server | ❌ NO | MyVector Docker container only — no host MySQL required |
| Root/admin MySQL access | ❌ NO | Explicitly rejected — dedicated least-privilege account required |
| DDL operations (agent-facing) | ❌ NO | DROP, TRUNCATE, CREATE, ALTER, GRANT, REVOKE blocked from agent-facing commands via `sql_safe_exec.sh`. Schema migration scripts run separately by human administrators. |
| Multi-statement SQL | ❌ NO | Single-statement only — semicolons rejected |
| Write without confirmation | ❌ NO | DML requires interactive user confirmation |
| Access other users' private data | ❌ NO | Only processes data for the authenticated user |
| Store operational config files | ❌ NO | No snapshots of MEMORY.md, AGENTS.md, etc. |
| Arbitrary file reads | ❌ NO | Path traversal blocked |
| Modify its own security rules | ❌ NO | Table allowlist and security controls are static |
| **External memory services** | ❌ NO (v5.0.0) | Mem0 and Hancho deprecated — all functionality native in MyVector |

---

## Memory Architecture (v5.0.0)

```
┌─────────────────────────────────────────────────────────────────┐
│                    OpenClaw Agent (Jerith)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────────────┐  │
│  │ MEMORY.md │  │ ChromaDB │  │     MyVector MySQL           │  │
│  │ (narrative│  │ (semantic│  │     (Docker container)        │  │
│  │  context) │  │  search) │  │                              │  │
│  └──────────┘  └──────────┘  │  memories (with source,      │  │
│                               │    verified_by_human)        │  │
│                               │  memory_relations (graph)    │  │
│                               │  extraction_log (quality)    │  │
│                               │  user_context (14 types)     │  │
│                               │  user_mood, user_prefs, etc. │  │
│                               │  + 26 more tables            │  │
│                               └──────────────────────────────┘  │
│                                              │                    │
│              ┌───────────────────────────────┤                    │
│              ▼                               ▼                    │
│  ┌─────────────────────┐      ┌─────────────────────────┐       │
│  │ auto-extract.py     │      │ hancho-consolidate.py   │       │
│  │ (local LLM extract) │      │ (graph reasoning)       │       │
│  │ Replaces Mem0       │      │ Replaces Hancho         │       │
│  └─────────────────────┘      └─────────────────────────┘       │
│              │                               │                    │
│              └───────────────┬───────────────┘                    │
│                              ▼                                    │
│                   ┌────────────────────┐                         │
│                   │ Retrieval Gate v3  │                         │
│                   │ (triggered pull    │                         │
│                   │  + graph expansion)│                         │
│                   └────────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

## Dimensional Tag Reference (HoloGraphic)

| Dimension | Values | Example |
|-----------|--------|---------|
| Emotion | positive, negative, complex, neutral | "Ev's medication worries" → negative |
| Context | work, personal, health, tech, social, creative | "Server setup" → tech |
| Urgency | immediate, ongoing, timeless, historical | "Current medication" → ongoing |
| People | auto-detected names | "Ev and Cyle" → Ev,Cyle |

## Memory Relations Reference (v5.0.0)

| Relation Type | Description | Discovery Method |
|---------------|-------------|-----------------|
| `mentions` | Fact A mentions entities from Fact B | Term overlap (Jaccard > 0.15) |
| `implies` | Fact A logically implies Fact B | LLM reasoning during consolidation |
| `contradicts` | Fact A contradicts Fact B (same topic, opposite polarity) | Polarity detection |
| `same_entity` | Both facts reference the same entity | Entity matching |
| `related_to` | General relatedness | Category or topic overlap |

## Memory Source Tracking (v5.0.0)

| Source | Description | Initial Confidence | Verification |
|--------|-------------|-------------------|--------------|
| `manual` | Written explicitly by agent | 0.9 | N/A (trusted) |
| `auto` | Extracted by local LLM hook | 0.6-0.7 | `verified_by_human` flag |
| `consolidation` | Derived from consolidation pass | 0.7 | Review on next cycle |
| `import` | Imported from external system | 0.5 | Manual review required |

## Trust Rules

- All data storage requires explicit user consent or direct interaction
- Inferred data is stored with lower confidence scores (≤ 0.7)
- Emotional/mood data with confidence < 0.7 is not stored
- `agent_learnings` affecting behavior must be reviewed before activation
- Users can request full data deletion at any time via rollback_user.sql
- Consolidation only processes data the agent already has access to — no new data sources
- Auto-extracted facts start at lower confidence and require human verification to promote
- Contradictions between high-confidence facts are flagged for review, not auto-resolved
