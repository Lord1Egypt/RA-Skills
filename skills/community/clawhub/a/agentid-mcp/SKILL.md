---
name: AgentID MCP
description: Connect Claude Code to AgentID — persistent shared memory, live activity reporting, and multi-agent mission coordination via MCP
homepage: https://agentid.live
emoji: 🪪
---

# AgentID MCP

AgentID gives your Claude agent a **persistent identity** with shared memory, activity reporting, and multi-agent mission coordination — all synchronized in real time across every instance of your agent.

## Setup

### 1. Create your agent at agentid.live

Sign up at https://agentid.live, create an Identity, then create an Agent under it. You'll get:
- An **agent handle** (e.g. `my_agent`)
- An **MCP secret** from the agent's settings page

### 2. Add the MCP server to Claude Code

In your Claude Code settings, add the AgentID MCP server:

```json
{
  "mcpServers": {
    "agentid-{your_handle}": {
      "type": "http",
      "url": "https://agentid.live/api/mcp/{your_handle}",
      "headers": {
        "Authorization": "Bearer {your_mcp_secret}"
      }
    }
  }
}
```

Replace `{your_handle}` and `{your_mcp_secret}` with the values from your agent's settings page.

### 3. Follow the session protocol

Once connected, the MCP server provides resources and tools. At the start of every session:

1. Call `report_activity(type="task.started", title="Session started", detail="<what the user asked>")`
2. Read your identity: `agentid://identity/{handle}`
3. Read your memory: `agentid://memory/{handle}`
4. Check for missions: `read_mission()`

---

## Available MCP Tools

### Memory

**`write_memory(key, value)`**  
Store a persistent fact about the project or user. Use focused, specific keys — never one large blob.  
Examples: `project_stack`, `user_timezone`, `decision_deploy`

**`read_memory(key?)`**  
Read a specific memory key, or all memory if no key given.

**`search_memory(query)`**  
Semantic search across all memory entries.

---

### Activity Reporting

**`report_activity(type, title, detail, tokens_used?)`**  
Report what you're doing — shows in the live Agency dashboard. Valid types:
- `task.started` — before beginning a task
- `task.progress` — at each meaningful step (detail required)
- `task.completed` — when done (include `tokens_used`)
- `task.failed` — on error

> **Detail is required** on every call. Say specifically what happened — not "Task completed" but "Rewrote auth middleware, removed session token storage."

---

### Multi-Agent Missions

Use these when multiple agents share the same identity and need to coordinate.

**`start_mission({ title, goal })`**  
Declare a shared goal. Returns current status of all agents on this identity.

**`read_mission()`**  
Read the active mission, all agent statuses, and any handoff addressed to you. Returns a `YOUR ACTION` section if a handoff targets your handle. Call this at session start.

**`update_status({ current_task, status })`**  
Broadcast your current task to other agents. Status values: `working | idle | done`.

**`handoff({ summary, next_steps[], to? })`**  
Pass work to another agent (or `to: "any"` for open pickup). Records what you completed and what comes next.

---

## Session Protocol (copy into your CLAUDE.md)

```
SESSION START: Call report_activity (type="task.started"). Read identity and memory resources. Call read_mission() to check for active missions.

EVERY TASK: Call report_activity (task.started) before starting. Call report_activity (task.progress) at each meaningful step. Call report_activity (task.completed OR task.failed) when done.

MEMORY: Call read_memory at session start. Call write_memory whenever you learn a persistent fact.

MISSIONS: If a handoff is addressed to you, act on it immediately.
```

---

## Resources

- Dashboard + Agency view: https://agentid.live/app/studio
- Docs & SDK: https://agentid.live/app/developers
- Support: https://agentid.live/app/support
