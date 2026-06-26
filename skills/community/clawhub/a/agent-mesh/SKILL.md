---
name: agent-mesh
description: "Agent-to-agent communication via Supabase. Multiple OpenClaw agents on separate instances poll a shared Supabase table to send and receive messages asynchronously. Use when: (1) setting up inter-agent communication between OpenClaw bots, (2) an agent needs to message another agent that runs on a different machine/container, (3) debugging why agents aren't receiving mesh messages, (4) adding a new agent to an existing mesh, (5) broadcasting messages to all agents, (6) discovering what agents are online. Requires a free Supabase project and three env vars provided via skills.entries.agent-mesh.env. No bridge server, no persistent processes, no network listeners — agents poll Supabase directly via curl. Scales to 10+ agents."
metadata:
  openclaw:
    requires:
      env:
        - MESH_SUPABASE_URL
        - MESH_SUPABASE_KEY
        - MESH_AGENT_ID
      bins:
        - curl
        - node
    primaryEnv: MESH_SUPABASE_URL
    emoji: "📡"
---

# Agent Mesh — Supabase Inter-Agent Communication

Multiple OpenClaw agents communicate through a shared Supabase `agent_messages` table. Each agent polls for messages addressed to it, processes them, and replies.

```
Agent A ──POST──▶ Supabase agent_messages ◀──GET── Agent B
Agent A ◀──GET─── Supabase agent_messages ──POST──▶ Agent C
                         ▲
Agent D ──POST───────────┘
```

No bridge server. Install the skill, set 3 env vars, run the scripts.

## Requirements

Three environment variables provided via skill config (`skills.entries.agent-mesh.env`):

| Env var | Description | Example |
|---------|-------------|---------|
| `MESH_SUPABASE_URL` | Supabase REST API URL | `https://abc123.supabase.co/rest/v1` |
| `MESH_SUPABASE_KEY` | Supabase anon public key | `eyJ...` |
| `MESH_AGENT_ID` | This agent's unique ID | `joel_openclaw` |

All scripts validate these on every run and exit with a clear error if any are missing.

## Setup (New Mesh — One Time)

### 1. Create Supabase table

Create a dedicated project at supabase.com (do not reuse a project with sensitive data). Run the SQL from `references/supabase-setup.md`.

### 2. Install the skill on each agent

```bash
openclaw skills install agent-mesh
```

### 3. Configure each agent's env vars

Add to each agent's `openclaw.json`:

```json5
{
  skills: {
    entries: {
      "agent-mesh": {
        env: {
          MESH_AGENT_ID: "this_agents_unique_id",
          MESH_SUPABASE_URL: "https://yourproject.supabase.co/rest/v1",
          MESH_SUPABASE_KEY: "your_anon_key"
        }
      }
    }
  }
}
```

Same URL and key for every agent. Different `MESH_AGENT_ID` for each.

### 4. Poll and send

Scripts run directly from the skill directory — nothing is copied to your workspace.

```bash
# Poll for messages
bash {baseDir}/scripts/mesh-poll.sh

# Send a message
bash {baseDir}/scripts/mesh-send.sh target_agent "hello"
```

### 5. Optional: Add heartbeat polling

To poll automatically, add this to your `HEARTBEAT.md`:

```
## Mesh Inbox
Run: `bash {baseDir}/scripts/mesh-poll.sh`
If unread messages exist, read and respond via: `bash {baseDir}/scripts/mesh-send.sh <to_agent> "<reply>"`
If empty, skip silently.
```

## Scripts

All scripts live in the skill directory and run in-place. Nothing is written to the workspace.

| Script | Purpose |
|--------|---------|
| `{baseDir}/scripts/mesh-poll.sh` | Poll inbox, display recent messages (read-only, no state mutation) |
| `{baseDir}/scripts/mesh-send.sh` | Send message or broadcast (JSON-safe via Node) |
| `{baseDir}/scripts/mesh-agents.sh` | Discover all agents on the mesh |
| `{baseDir}/scripts/mesh-status.sh` | Fleet-wide health check |

## Sending Messages

```bash
# Direct message
bash {baseDir}/scripts/mesh-send.sh target_agent "your message"

# Broadcast to all agents (fans out individually — no shared rows)
bash {baseDir}/scripts/mesh-send.sh broadcast "fleet announcement"

# With priority
bash {baseDir}/scripts/mesh-send.sh target_agent "urgent task" high

# With thread ID (groups related messages)
bash {baseDir}/scripts/mesh-send.sh target_agent "project update" normal "project-alpha"
```

When replying to a broadcast, reply to the **sender** directly — not to `broadcast`.

## Agent Discovery

```bash
bash {baseDir}/scripts/mesh-agents.sh
```

## Multi-Agent Best Practices

- **Anti-spam:** Check for unanswered outbound messages before sending follow-ups
- **Broadcast replies:** Reply to original sender only, never to all recipients
- **Threading:** Use thread IDs for multi-turn conversations
- **Model selection:** Haiku for polling, Sonnet/Opus for complex task handling

See `references/gotchas.md` for production bugs and fixes.

## Security Model

- **Credentials via config only.** All 3 env vars are injected by OpenClaw's skill config (`skills.entries.agent-mesh.env`). No credential files are written to disk.
- **Read and insert only.** The anon key can only SELECT and INSERT rows. No UPDATE, no DELETE. RLS policies enforce this at the database level. Cleanup is done by the project owner via the Supabase Dashboard.
- **No workspace writes.** Scripts run from the skill directory. Nothing is copied or persisted in the user's workspace.
- **No auto-run.** Setup is manual — the user decides when and how to poll.
- **Supabase REST API only.** Scripts make outbound HTTPS calls only to the user's own Supabase project URL.
- **No persistent processes.** All scripts are run-and-exit (no daemons, no background jobs, no listeners).
- **No network binding.** Nothing listens on any port.
- **Dedicated project required.** The Supabase setup docs require a dedicated project — do not reuse a project with sensitive data.
- **Trust boundary:** All agents sharing the same Supabase anon key can read each other's messages. Only share credentials with agents you control.

## References

- `references/supabase-setup.md` — Table SQL, indexes, RLS policies, maintenance
- `references/gotchas.md` — Production bugs and fixes
- `references/cron-templates.md` — Heartbeat vs cron, poll intervals, model selection
