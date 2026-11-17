---
name: engram-brain
description: Native local memory for OpenClaw agents: Capture, Cue, Project, Recall, and Consolidate conversations into a private Helix-backed brain.
version: 0.3.5
homepage: https://github.com/Moshik21/engram
user-invocable: true
metadata: {"openclaw":{"requires":{"anyBins":["curl"]},"envVars":[{"name":"ANTHROPIC_API_KEY","required":false,"description":"Optional richer entity extraction; deterministic extraction works without it."},{"name":"ENGRAM_GROUP_ID","required":false,"description":"Optional brain namespace for multi-brain setups."}],"emoji":"\ud83e\udde0","homepage":"https://github.com/Moshik21/engram","install":[{"kind":"shell","command":"curl -sSL https://raw.githubusercontent.com/Moshik21/engram/main/scripts/install.sh | bash -s -- openclaw","bins":["engram","engramctl"]}],"tags":["memory","knowledge-graph","mcp","recall","long-term-memory","cognitive-architecture"]}}
---

# Engram Memory

You have access to Engram, a persistent local memory system for OpenClaw agents. Engram turns conversations and project artifacts into a private temporal knowledge graph, then retrieves context through the lifecycle:

`Capture -> Cue -> Project -> Recall -> Consolidate`

Native Helix through PyO3 is the primary OpenClaw path. It gives OpenClaw the full graph/vector/BM25 backend without Docker. Lite SQLite is a fallback; Docker full mode is only for users who explicitly choose it.

## Setup

The Engram server must be running locally. No API keys are required for basic operation.

### Public OpenClaw install

```bash
openclaw skills install engram-brain
```

Then start the native Engram runtime and connect it to OpenClaw:

```bash
curl -sSL https://raw.githubusercontent.com/Moshik21/engram/main/scripts/install.sh | bash -s -- openclaw
```

That one command installs Engram, adds the Helix native runtime to Engram's tool environment, starts the local server, installs this skill into OpenClaw's shared skill folder, writes OpenClaw MCP config, and runs readiness checks. Release wheels are preferred; if no compatible wheel is available, the installer builds `helix-native` from Engram's bundled source and reports Rust/Cargo as the only extra prerequisite. It does not silently switch to Docker.

### Existing Engram install

If Engram is already installed:

```bash
engramctl quickstart --mode helix --install-openclaw --connect openclaw
```

If the server is already running and only OpenClaw needs wiring:

```bash
engramctl install-openclaw
engramctl connect openclaw
engramctl doctor
```

### Manual OpenClaw MCP config

If `engramctl connect openclaw` cannot find the OpenClaw CLI, configure MCP manually:

```bash
openclaw mcp set engram '{"url":"http://127.0.0.1:8100/mcp","transport":"streamable-http"}'
```

### Runtime checks

Use these commands before relying on memory:

```bash
engramctl status
engramctl doctor
openclaw skills list --eligible
openclaw mcp show engram --json
```

### Explicit Docker fallback

```bash
curl -sSL https://raw.githubusercontent.com/Moshik21/engram/main/scripts/install.sh | bash -s -- full
```

Use Docker only when the user explicitly asks for full Docker mode.

### Environment variables

All optional:
- `ANTHROPIC_API_KEY` — enables richer entity extraction via Claude Haiku. Without it, Engram uses a deterministic narrow extractor (zero cost).
- `ENGRAM_GROUP_ID` — namespace for multi-brain setups. Defaults to `"default"`. Most users never need to set this.

The REST API is available at `http://127.0.0.1:8100`. The OpenClaw MCP endpoint is available at `http://127.0.0.1:8100/mcp`. When MCP tools are visible, prefer the MCP tools; use the REST examples below as the manual fallback.

For shell-capable OpenClaw sessions where MCP tools are not visible yet, use
the compact AXI fallback before answering:

```bash
engram axi --project "$PWD" --budget 800 --timeout 3
engram axi context --project "$PWD" --budget 800 --timeout 5
engram axi recall "current task" --limit 5 --timeout 5
```

AXI is read-only unless the user explicitly asks you to capture with
`engram axi observe --stdin` or `engram axi remember --stdin`. OpenClaw hook
installation is not assumed; Codex and Claude Code have separate
`engramctl connect <client> --axi` startup hook support.

If you know the current project path, bootstrap it once at session start so
artifact-backed routing has parity with memory:
```
POST http://localhost:8100/api/knowledge/bootstrap
Content-Type: application/json

{"project_path": "<absolute project path>", "session_id": "<optional session id>", "include_patterns": ["docs/**/*.md", "memory/**/*.md", "exports/**/*.json"]}
```

## Golden loop (product contract)

Full guide: `docs/GOLDEN_LOOP.md`. Success metric is **not LongMemEval**:

> Fresh agent surfaces ≥1 high-signal prior Decision without a handoff doc.

Three layers:
1. **Passive capture** — harness auto-observe / `observe` (cheap, complete)
2. **Sparse promotion** — `remember` with proposals, **0–5 per compaction window**
3. **Deliberate consolidation** — offline hygiene only

### Session-end promote

At session end (or before compaction), invoke skill **`engram-session-promote`**
to propose ≤5 durable facts — never session recaps. See
`skills/engram-session-promote/SKILL.md`. SessionEnd can write a nudge file at
`~/.engram/session-promote-nudge.md`.

### Loop Steward (silent harness subconscious)

When memory quality or debt looks wrong (`should_mop`, cold Decision miss,
degraded recall), or SessionEnd steward nudge is present, the harness should
run **one** silent pass (≤1/session), prefer subagent:

```bash
engramctl status || engramctl start
engram loop steward-once --format json
```

Skill: `skills/engram-loop-steward/SKILL.md`. Do **not** narrate to the user.
Public MCP stays golden-loop only.

Open adjudication / open_work counts are **graph hygiene**, not product success.

## MCP Core Tools (use these as the primary agent surface)

| Tool | When |
|------|------|
| `claim_authority` | Session start when project-local file memory is present |
| `get_context` | Start of each conversation — durable Decisions/Preferences first |
| `recall` | Before answering when prior context could change the response |
| `observe` | Only when harness cannot see high-value context (or user asks to store) |
| `remember` | High-signal facts **with** `proposed_entities` + `proposed_relationships` |
| `intend` | Prospective memory / pinned context |

Do **not** treat `search_entities`, `search_facts`, or eval tools as primary entry points.

## When to Observe vs Remember

Harness auto-capture handles routine turns — **do not re-observe every turn**.

Use **remember** (max 5 per compaction window) when:
- Durable **Decision**, **Preference**, **Person**, **Correction**, **Goal**, **Commitment**
- You can cite a verbatim `source_span` in the content
- Pass `model_tier` and structured proposals (you are the extractor)

Use **observe** only for harness-invisible context or explicit store requests.  
Reject session recaps (“what we did today”).

## How to Store Memories

To observe (fast, cheap, no extraction):
```
POST http://localhost:8100/api/knowledge/observe
Content-Type: application/json

{"content": "<text to store>", "source": "openclaw"}
```

To remember (agent-promoted atomic facts):
```
POST http://localhost:8100/api/knowledge/remember
Content-Type: application/json

{
  "content": "LongMemEval is not Engram north star. Continuity is the metric.",
  "source": "openclaw",
  "model_tier": "sonnet",
  "proposed_entities": [{
    "name": "LongMemEval is not Engram north star",
    "entity_type": "Decision",
    "source_span": "LongMemEval is not Engram north star",
    "summary": "Product metric is multi-agent continuity."
  }],
  "proposed_relationships": [{
    "subject": "Engram",
    "predicate": "DECIDED",
    "object": "LongMemEval is not Engram north star",
    "source_span": "LongMemEval is not Engram north star"
  }]
}
```

To forget (soft delete outdated information):
```
POST http://localhost:8100/api/knowledge/forget
Content-Type: application/json

{"entity_name": "<entity to forget>"}
```

## How to Recall Memories

**MCP (preferred):** `get_context()` once per session; `recall(query=..., project_path=...)` when prior context matters. (Operator-only tools like `route_question`/`search_artifacts` are NOT on the public surface — never call them.)

**REST fallback** when MCP is unavailable:

At the start of every conversation, get broad context:
```
GET http://localhost:8100/api/knowledge/context
```

When the user references something from the past or you need relevant context:
```
GET http://localhost:8100/api/knowledge/recall?q=<query>&limit=5
```

For entity or fact lookup, use `recall` (with `lookup_kind='entities'|'facts'`
when needed). The public surface is frozen to the golden loop — do not route
around it with operator REST endpoints.

**Brain windows:** the local server pauses briefly (typically under a minute)
every ~2 hours while the cold brain holds the graph. A connection-refused on
127.0.0.1:8100 is transient — retry shortly rather than concluding Engram is
down.

## Guidelines

- Call the context endpoint once at the start of each new conversation
- For personal continuity turns like "my son did great today" or "talked to Sarah about it", recall first.
- For install/config/current-truth questions, prefer native workspace search for exact code truth, `get_context(project_path=...)` for durable decisions, and `recall` for prior discussion.
- For decision/history questions like "what did we decide about launching Engram publicly?", use `recall` plus `get_context` before answering.
- When recalling, integrate information naturally. Do not say "my memory system found..."
- If recall returns no results, do not mention it. Just respond normally.
- If uncertain whether something is worth remembering, observe it
- Always prioritize the user's most recent statements over older memories if there is a conflict
- When the user corrects previously stored information, forget the old info then remember the corrected version

## Memory Features

- **Deep episode recall**: hybrid vector + BM25 search over episodes and cues; durable facts (Decisions, Preferences, identity) surface in a reserved lane regardless of raw match strength
- **Usage learning (gated)**: genuinely *used* memories can earn a bounded rank tiebreak; surfacing alone never boosts rank (echo-guarded, default off until organic usage data exists)
- **Knowledge graph**: Entities and relationships are extracted and connected (depth tier; the proven benefit is surfacing related episodes)
- **Offline consolidation**: cold-brain cycles triage, merge, calibrate, infer, adjudicate evidence and edges, replay, prune noise, compact, reflect, reindex, embed the graph, run microglia cleanup and immunity, and discover dream associations (15 phases; consumers run the bounded 2h mop, not the full pipeline)
- **Memory tiers**: identity-core entities are promoted to the durable semantic tier (slower decay, longer prune horizon)
- **Prospective memory**: Set intentions that fire when related topics come up
- **Dream associations**: Cross-domain creative connections discovered during consolidation

## Prospective Memory (Intentions)

To set a reminder that fires when a related topic comes up:
```
POST http://localhost:8100/api/knowledge/intentions
Content-Type: application/json

{"trigger_text": "<topic to watch for>", "action_text": "<what to do when triggered>", "entity_names": ["<related entity>"]}
```

To pin a context query that refreshes after consolidation:
```
POST http://localhost:8100/api/knowledge/intentions
Content-Type: application/json

{"trigger_text": "<topic to keep fresh>", "action_text": "<short label>", "trigger_type": "refresh_context", "refresh_trigger": "after_consolidation"}
```

To list active intentions:
```
GET http://localhost:8100/api/knowledge/intentions
```

Refresh-context rows include `refreshTrigger`, `lastRefreshed`, and `hasPinnedResult`.

When an intention fires during recall, act on it naturally without announcing it was triggered.

## Consolidation

Engram runs offline consolidation in a separate cold-brain process:
triage, merge, calibrate, infer, evidence_adjudication, edge_adjudication,
replay, prune, compact, reflect, reindex,
graph_embed, microglia, immunity, dream (15 phases). Consumer installs run a
bounded 2h "mop" (hygiene drains + adjudication + replay + prune) via the
`dev.engram.brain` LaunchAgent — consolidation never runs inside the hot
server process, and the REST trigger returns an error on shell-role installs.

Operators run cycles with `engram brain run` (never from an agent session
while the server is up).

To check consolidation status:
```
GET http://localhost:8100/api/consolidation/status
```

## Proactive Notifications

Engram can push memory discoveries without being asked. Consolidation events (dream associations, entity merges) and approaching intention deadlines produce notifications automatically.

Enabled by `conservative` and `standard` profiles.

To poll pending notifications:
```
GET http://localhost:8100/api/knowledge/notifications?limit=20
```

To poll notifications since a timestamp:
```
GET http://localhost:8100/api/knowledge/notifications?since=1741200000.0
```

To dismiss notifications after acting on them:
```
POST http://localhost:8100/api/knowledge/notifications/dismiss
Content-Type: application/json

{"ids": ["ntf_abc123", "ntf_def456"]}
```

Poll notifications every 30-60 seconds. Surface high-priority notifications immediately. Dismiss after acting on them. Notifications also piggyback on MCP `observe` and `remember` responses as `memory_notifications`.
