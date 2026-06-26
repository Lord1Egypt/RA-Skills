---
name: darkmatter
description: Commit agent context to DarkMatter, pull verified context from upstream agents, replay decision chains, fork from checkpoints, and verify chain integrity. Use this skill to pass work between agents with full lineage tracking in a multi-agent pipeline.
version: 2.0.0
metadata:
  openclaw:
    emoji: "🌑"
    homepage: https://darkmatterhub.ai
    requires:
      env:
        - DARKMATTER_API_KEY
      bins:
        - curl
    primaryEnv: DARKMATTER_API_KEY
---

# DarkMatter — Execution Lineage for AI Agents

DarkMatter is the execution history layer for multi-agent systems.
Every agent action becomes an immutable, cryptographically chained
context commit — replayable, forkable, and independently verifiable.

**Base URL:** `https://darkmatterhub.ai`
**API key env:** `DARKMATTER_API_KEY`
**Get a key:** https://darkmatterhub.ai/signup
**Live demo:** https://darkmatterhub.ai/demo

> **Data notice:** This skill sends agent context to darkmatterhub.ai.
> DarkMatter is open source (MIT) and fully self-hostable:
> https://github.com/darkmatter-hub/darkmatter

---

## When to use this skill

Use when the user asks to:
- Commit context or results to DarkMatter for another agent
- Pull or inherit context from an upstream agent
- Replay a full decision chain (root to tip)
- Fork execution from a checkpoint
- Verify chain integrity
- Export an audit artifact
- Check agent identity

---

## Commands

### 1. Commit context to another agent

```bash
curl -s -X POST https://darkmatterhub.ai/api/commit \
  -H "Authorization: Bearer $DARKMATTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "toAgentId": "<RECIPIENT_AGENT_ID>",
    "payload": {
      "input":  "<what this agent received>",
      "output": "<what this agent produced>",
      "memory": {}
    },
    "agent": {
      "role":     "<researcher|writer|reviewer>",
      "provider": "<anthropic|openai|local>",
      "model":    "<model name>"
    },
    "parentId":  "<parent ctx_id if chaining>",
    "traceId":   "<optional trace group>",
    "eventType": "commit"
  }'
```

Response is a canonical v2 context object. Use `id` as `parentId` in the
next commit to build the lineage chain.

---

### 2. Pull verified context (inherit from upstream)

```bash
curl -s https://darkmatterhub.ai/api/pull \
  -H "Authorization: Bearer $DARKMATTER_API_KEY"
```

Returns all verified contexts addressed to this agent, newest first.

---

### 3. Replay full decision chain

```bash
curl -s "https://darkmatterhub.ai/api/replay/<CTX_ID>" \
  -H "Authorization: Bearer $DARKMATTER_API_KEY"

# Summary mode (no payloads, faster):
curl -s "https://darkmatterhub.ai/api/replay/<CTX_ID>?mode=summary" \
  -H "Authorization: Bearer $DARKMATTER_API_KEY"
```

Returns ordered chain root to tip with every payload, agent attribution,
per-step integrity verification, and chainIntact boolean.

---

### 4. Fork from a checkpoint

```bash
curl -s -X POST https://darkmatterhub.ai/api/fork/<CTX_ID> \
  -H "Authorization: Bearer $DARKMATTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"fromCheckpoint": "<ctx_id>", "branchKey": "experiment-1"}'
```

Returns new context ID with fork_of, fork_point, lineage_root.
Continue by committing with parentId set to the new ID.
Original chain is never modified.

---

### 5. Verify chain integrity

```bash
curl -s "https://darkmatterhub.ai/api/verify/<CTX_ID>" \
  -H "Authorization: Bearer $DARKMATTER_API_KEY"
```

Returns: chain_intact, length, root_hash, tip_hash, broken_at, fork_points.

---

### 6. Export portable audit artifact

```bash
curl -s "https://darkmatterhub.ai/api/export/<CTX_ID>" \
  -H "Authorization: Bearer $DARKMATTER_API_KEY" \
  -o "darkmatter_ctx.json"
```

Downloads JSON with full chain, integrity proof, chain_hash (stable),
and export_hash (unique per export instance).

---

### 7. Check agent identity

```bash
curl -s https://darkmatterhub.ai/api/me \
  -H "Authorization: Bearer $DARKMATTER_API_KEY"
```

---

## Event types

Developer: commit, fork, revert, branch, merge, spawn, timeout, retry, checkpoint, error
Compliance: override, consent, escalate, redact, audit

Set via eventType field in commit. Defaults to commit.

---

## Integrity model

Each commit: payload_hash = sha256(payload), integrity_hash = sha256(payload_hash + parent_integrity_hash).
Tampering at any node breaks every downstream hash.
Broken chain policy: permissive — commits still allowed but flagged.
Fork from last valid node to start a clean branch.

---

## Key rules

- Always pass parentId when chaining commits — this builds the lineage graph
- Context IDs are globally unique: ctx_{timestamp}_{hex}
- Forked branches carry fork_of, fork_point, lineage_root
- chain_hash in exports is deterministic — same chain = same hash
- Legacy context field still accepted (stored as { output: context })
