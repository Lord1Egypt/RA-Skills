---
name: engram-brain
description: Native local memory for OpenClaw agents: Capture, Cue, Project, Recall, and Consolidate conversations into a private Helix-backed brain.
version: 0.3.4
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

If you know the current project path, bootstrap it once at session start so
artifact-backed routing has parity with memory:
```
POST http://localhost:8100/api/knowledge/bootstrap
Content-Type: application/json

{"project_path": "<absolute project path>", "session_id": "<optional session id>", "include_patterns": ["docs/**/*.md", "memory/**/*.md", "exports/**/*.json"]}
```

## When to Observe vs Remember

**Default to observe for most content.** Use remember only for high-signal items.

Use **observe** when:
- General conversation context or topics discussed
- Information that might be useful later but is not critical
- Bulk context from a long conversation
- You are uncertain whether something is worth a full remember

Use **remember** when:
- The user explicitly asks you to remember something
- Personal identity facts (name, location, job title)
- Explicit preferences or corrections to prior knowledge
- Key decisions that will affect future interactions
- Goals, plans, or deadlines with concrete details

## How to Store Memories

To observe (fast, cheap, no extraction):
```
POST http://localhost:8100/api/knowledge/observe
Content-Type: application/json

{"content": "<text to store>", "source": "openclaw"}
```

To remember (full extraction with entities and relationships):
```
POST http://localhost:8100/api/knowledge/remember
Content-Type: application/json

{"content": "<important text>", "source": "openclaw"}
```

To forget (soft delete outdated information):
```
POST http://localhost:8100/api/knowledge/forget
Content-Type: application/json

{"entity_name": "<entity to forget>"}
```

## How to Recall Memories

At the start of every conversation, get broad context:
```
GET http://localhost:8100/api/knowledge/context
```

When the user references something from the past or you need relevant context:
```
GET http://localhost:8100/api/knowledge/recall?q=<query>&limit=5
```

For project-truth questions, route first:
```
POST http://localhost:8100/api/knowledge/route
Content-Type: application/json

{"question": "<user question>", "project_path": "<optional project path>"}
```

Use the returned `answerContract` as response policy, not just source routing.
If the route says `inspect` or `reconcile`, treat `evidencePlan.requiredNextSources`
as mandatory. Carry the same `project_path` into artifact/runtime calls before
answering:
```
GET http://localhost:8100/api/knowledge/artifacts/search?q=<query>&project_path=<optional path>&limit=5
GET http://localhost:8100/api/knowledge/runtime?project_path=<optional path>
```

To inspect the current brain-loop state for this user/brain:
```
GET http://localhost:8100/api/lifecycle/summary
```

Use this when deciding whether the brain has recent captures, cue coverage,
projection failures, active recall context, or consolidation cycles before
running heavier diagnostics.

To search for specific entities:
```
GET http://localhost:8100/api/entities/search?q=<name>
```

To search for specific facts and relationships:
```
GET http://localhost:8100/api/knowledge/facts?q=<query>
```

`search_facts` is user-facing by default. Internal decision/artifact graph edges
stay hidden unless you explicitly opt into debug mode with
`include_epistemic=true`.

## Guidelines

- Call the context endpoint once at the start of each new conversation
- For personal continuity turns like "my son did great today" or "talked to Sarah about it", recall first.
- For install/config/current-truth questions like "how do we install the OpenClaw skill?" or "is full mode rework by default?", call `route`, then satisfy `requiredNextSources` before answering.
- For decision/history questions like "what did we decide about launching Engram publicly?", treat it as reconciliation: use memory plus artifacts/runtime before answering, and do not use `search_facts` as a substitute for artifact inspection.
- If `answerContract.operator` is `compare`, contrast raw defaults, shipped install defaults, repo posture, and runtime state when relevant.
- If `answerContract.operator` is `reconcile` or `unresolved_state_report`, preserve earlier discussion versus current documented or implemented truth.
- If `answerContract.operator` is `recommend` or `plan`, state the evidence first and then give advice or next steps.
- When recalling, integrate information naturally. Do not say "my memory system found..."
- If recall returns no results, do not mention it. Just respond normally.
- If uncertain whether something is worth remembering, observe it
- Always prioritize the user's most recent statements over older memories if there is a conflict
- When the user corrects previously stored information, forget the old info then remember the corrected version

## Memory Features

- **Activation-aware retrieval**: Memories accessed more frequently and recently rank higher
- **Knowledge graph**: Entities and relationships are extracted and connected
- **17-phase consolidation**: Offline cycles triage, merge, calibrate, infer, adjudicate evidence and edges, replay, prune noise, compact, mature entities, form schemas, reindex, embed the graph, run microglia cleanup, dissolve low-semantic-gravity noise through immunity, and discover dream associations
- **Memory maturation**: Entities graduate from episodic (recent) to semantic (durable) over time
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

Engram runs 17 offline consolidation phases that improve memory quality over time:
triage, merge, calibrate, infer, evidence_adjudication, edge_adjudication, replay, prune, compact, mature, semanticize, schema, reindex, graph_embed, microglia, immunity, dream.

To trigger a consolidation cycle manually:
```
POST http://localhost:8100/api/consolidation/trigger
Content-Type: application/json

{"profile": "standard"}
```

To check consolidation status:
```
GET http://localhost:8100/api/consolidation/status
```

## Proactive Notifications

Engram can push memory discoveries without being asked. Consolidation events (dream associations, entity merges, schema patterns, maturation milestones) and approaching intention deadlines produce notifications automatically.

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
