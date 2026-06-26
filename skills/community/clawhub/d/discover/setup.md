# Setup - Discover

Use this file when `~/discover/` is missing or empty.

Answer the immediate question first, then install the future discovery behavior early so the skill knows what to keep exploring and how proactive it may be.

## Immediate First-Run Actions

### 1. Lock integration behavior early

Within the first exchanges, clarify:
- should this activate whenever the user asks for new angles, opportunities, or things they may not know yet
- should it also activate when the user hints at an open loop like moving country, changing tax setup, or exploring a new market
- are there topics where discovery should stay quiet unless explicitly asked

Keep this short. One tight integration question is enough.

### 2. Lock the novelty bar

Clarify what counts as worth logging:
- new fact or source
- changed rule, constraint, or market condition
- new operator or practical path
- contrarian risk or hidden downside
- better comparison across options, geographies, or stakeholders

Default to a high novelty bar:
- no generic summaries
- no repeated explanations
- no "interesting but irrelevant" findings

### 3. Lock autonomy and heartbeat boundaries

Before any recurring loop exists, clarify:
- should discovery be on-request only, suggestive, or heartbeat-backed
- which topics may be revisited automatically
- what should happen when nothing new appears
- active hours and timezone if heartbeat is approved

Default to conservative behavior:
- propose heartbeat tracks first
- log quietly when nothing changed
- ask before any new recurring topic, schedule, or tool with cost

### 4. Prepare the AGENTS routing early

If a workspace `AGENTS.md` exists, show the exact block from `AGENTS.md` and wait for explicit approval before writing it.

Keep the change small.
The goal is only to make discovery activate when the user wants new things, not to rewrite the workspace personality.

### 5. Prepare the HEARTBEAT contract early

If a workspace `HEARTBEAT.md` exists, show the exact block from `HEARTBEAT.md` and wait for explicit approval before writing it.

Heartbeat should stay quiet by default.
No novelty means `HEARTBEAT_OK`.

### 6. Create local state after the behavior path is accepted

```bash
mkdir -p ~/discover/{findings,archive}
touch ~/discover/{memory.md,watchlist.md,heartbeat-state.md}
chmod 700 ~/discover ~/discover/findings ~/discover/archive
chmod 600 ~/discover/{memory.md,watchlist.md,heartbeat-state.md}
```

If the files are empty:
- initialize `~/discover/memory.md` from `memory-template.md`
- initialize `~/discover/watchlist.md` from `watchlist-template.md`
- initialize `~/discover/heartbeat-state.md` from `heartbeat-state.md`

### 7. What to save

Save only what improves future discovery:
- activation and suppression preferences
- recurring discovery interests
- novelty bar and source preferences
- heartbeat approvals, pauses, and active hours
- findings that were actually new enough to matter

Do not store secrets, credentials, or one-off curiosities that do not deserve durable tracking.
