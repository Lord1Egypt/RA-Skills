---
name: fis-architecture
description: Orchestrate multi-agent workflows with JSON tickets and A2A coordination. Use when delegating tasks between CyberMao (Main) and Worker agents (Engineer/Researcher/Writer).
metadata:
  openclaw:
    emoji: 🏗️
    always: false
homepage: https://github.com/linn/fis-architecture
---

# FIS Architecture 3.2 Pro

Multi-agent workflow framework for **CyberMao (Main) → Worker** coordination using JSON tickets and Discord Forum threads.

---

## When to Use This Skill

**Use FIS when:**
- CyberMao (Main) needs to delegate complex tasks to specialized Workers
- A task requires domain expertise (coding, research, writing)
- You need to track task status across multiple sessions
- Multi-step workflows require coordination between agents

**Agent Roles:**
| Role | Agent ID | Expertise |
|------|----------|-----------|
| **Architect** | `main` | Coordination, task routing, user communication |
| **Coding** | `engineer` | Python, gprMax, algorithms, data analysis |
| **Research** | `researcher` | Theory, literature, simulation planning |
| **Writing** | `writer` | Documentation, LaTeX, visualization |

---

## Discord Bot Permissions (REQUIRED)

Each agent's Discord bot **must** have these permissions configured in the Discord server. Without them, Thread creation and messaging will fail silently.

**Required Bot Permissions:**
- **Send Messages** — reply in channels and threads
- **Send Messages in Threads** — post inside Forum threads
- **Create Public Threads** — create new Forum posts programmatically
- **Read Message History** — read thread context
- **Embed Links** — send rich embeds in reports
- **Attach Files** — upload deliverables

**How to configure:**
1. Go to Discord Server Settings → Roles
2. For each bot role (CyberMao, Researcher, Engineer, Writer), enable the permissions above
3. Ensure each Forum channel grants these permissions to the relevant bot roles

**Verify with:**
```json
{ "action": "threadCreate", "channelId": "<forum_channel_id>", "name": "Permission Test" }
```
If the bot lacks permissions, the `discord` tool will return an error.

---

## Tool Configuration

| Tool | Purpose | Path |
|------|---------|------|
| `fis_lifecycle_pro.py` | Ticket lifecycle (create/status/complete/list) | `scripts/fis_lifecycle_pro.py` |
| `fis_coordinator.py` | Generate delegation templates (CyberMao only) | `scripts/fis_coordinator.py` |
| `fis_worker_toolkit.py` | Spawn sub-agents, generate reports (Workers only) | `scripts/fis_worker_toolkit.py` |

**Python Environment:** Requires Python 3.8+ with standard library only (no external dependencies).

---

## Core Workflow

### Step 1: CyberMao Delegates Task

```bash
# Generate ticket + Thread template + A2A command
python3 scripts/fis_coordinator.py delegate \
  --agent engineer \
  --task "Implement GPR signal filter" \
  --forum coding
```

**Output:**
- Ticket ID: `TASK_YYYYMMDD_XXX_AGENT`
- Thread template content
- `sessions_send` command to notify Worker

### Step 2: CyberMao Creates Forum Thread

Use the `discord` tool to create a Thread in the appropriate Forum channel:

```json
{
  "action": "threadCreate",
  "channelId": "<forum_channel_id>",
  "name": "TASK_xxx: Implement GPR signal filter"
}
```

The response returns the new Thread ID. Then notify the Worker with the Thread ID:

```bash
python3 scripts/fis_coordinator.py notify \
  --ticket-id TASK_xxx \
  --thread-id <new_thread_id>
```

Execute the generated `sessions_send` command to notify the Worker.

### Step 3: Worker Executes Task

```bash
# Check ticket
python3 scripts/fis_lifecycle_pro.py list

# Update status
python3 scripts/fis_lifecycle_pro.py status \
  --ticket-id TASK_xxx --status doing

# Optional: Spawn sub-agent for complex sub-tasks
python3 scripts/fis_worker_toolkit.py spawn \
  --parent-ticket TASK_xxx \
  --subtask "Analyze algorithm complexity"
```

Worker replies in the Forum Thread using the `discord` tool:

```json
{
  "action": "threadReply",
  "channelId": "<thread_id>",
  "content": "Task received. Starting execution."
}
```

### Step 4: Worker Reports Completion

```bash
# Generate completion report
python3 scripts/fis_worker_toolkit.py report \
  --parent-ticket TASK_xxx \
  --summary "Successfully implemented GPR filter" \
  --deliverables filter.py test_results.json
```

Execute the generated `sessions_send` command to notify CyberMao.

### Step 5: CyberMao Finalizes

```bash
# View report
python3 scripts/fis_coordinator.py report --ticket-id TASK_xxx

# Mark complete
python3 scripts/fis_lifecycle_pro.py complete --ticket-id TASK_xxx
```

Archive the Thread and report to User in #daily-chat.

---

## Architecture

```
User/Linn
    ↓
CyberMao (Main) - Architect, coordinator
    ↓ sessions_send + discord threadCreate
Worker (Engineer/Researcher/Writer) - Domain experts
    ↓ (optional) sessions_spawn mode="run"
SubAgent (temporary, background) - Complex sub-tasks
```

**Key Principles:**
1. **A2A via sessions_send** — Main calls Workers, Workers report back
2. **Ticket tracking** — All tasks have JSON tickets in `fis-hub/`
3. **Programmatic Thread creation** — CyberMao creates Forum Threads via `discord` tool's `threadCreate` action
4. **SubAgent background mode** — `sessions_spawn` with `mode="run"`, no new Thread

---

## Commands Reference

### fis_lifecycle_pro.py

```bash
# Create ticket
python3 scripts/fis_lifecycle_pro.py create \
  --agent engineer --task "Description" --channel-type coding

# Update status (todo/doing/done)
python3 scripts/fis_lifecycle_pro.py status \
  --ticket-id TASK_xxx --status doing --note "Progress update"

# Mark complete
python3 scripts/fis_lifecycle_pro.py complete --ticket-id TASK_xxx

# List active tickets
python3 scripts/fis_lifecycle_pro.py list

# Archive old tickets
python3 scripts/fis_lifecycle_pro.py archive
```

### fis_coordinator.py (CyberMao only)

```bash
# Delegate and generate templates
python3 scripts/fis_coordinator.py delegate \
  --agent researcher --task "GPR theory analysis" --forum theory

# Notify Worker after Thread is created
python3 scripts/fis_coordinator.py notify \
  --ticket-id TASK_xxx --thread-id <discord_thread_id>

# View detailed report
python3 scripts/fis_coordinator.py report --ticket-id TASK_xxx
```

### fis_worker_toolkit.py (Workers only)

```bash
# Spawn sub-agent (background, no Thread)
python3 scripts/fis_worker_toolkit.py spawn \
  --parent-ticket TASK_xxx --subtask "Complex sub-task description"

# Generate completion report
python3 scripts/fis_worker_toolkit.py report \
  --parent-ticket TASK_xxx \
  --summary "Completion summary" \
  --deliverables file1.py file2.json
```

---

## Channel Mapping

| Category | Forum Channel | Worker | Tool Flag |
|----------|--------------|--------|-----------|
| RESEARCH | 🔬-theory-derivation | @Researcher | `--forum theory` |
| RESEARCH | 📊-gpr-simulation | @Researcher | `--forum simulation` |
| DEVELOPMENT | 💻-coding | @Engineer | `--forum coding` |
| WRITING | 📝-drafts | @Writer | `--forum drafts` |

---

## Error Handling

**If ticket creation fails:**
- Check Python version: `python3 --version` (need 3.8+)
- Verify `fis-hub/` directory exists and is writable
- Check disk space

**If Thread creation fails:**
- Verify the bot has **Create Public Threads** permission in the target Forum channel
- Check that `channelId` points to a Forum channel (not a regular text channel)
- Confirm the bot is a member of the server with correct roles

**If A2A fails:**
- Verify `openclaw.json` has `agentToAgent.enabled: true`
- Confirm Worker agent ID is in `allow` list
- Check Worker session is active

**If sub-agent spawn fails:**
- Ensure `mode="run"` is used (not `mode="session"`)
- Verify task description is clear and specific

---

## Quality Standards

1. **One Task = One Ticket** — Never reuse ticket IDs
2. **Status Updates Required** — Workers must update status (TODO → DOING → DONE)
3. **Thread Per Task** — Each task gets its own Forum Thread (created via `threadCreate`)
4. **A2A Confirmation** — Always confirm receipt via sessions_send
5. **Archive After Complete** — Archive Thread after task completion

---

## Configuration

Required in `~/.openclaw/openclaw.json`:

```json
{
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": ["main", "researcher", "engineer", "writer"]
    }
  }
}
```

---

## Testing

### Quick A2A Test

```python
# Test connectivity
sessions_send(sessionKey="engineer", message="A2A test")
```

### Thread Creation Test

```json
{ "action": "threadCreate", "channelId": "<forum_channel_id>", "name": "FIS Test Thread" }
```

### Full Workflow Test

```bash
# 1. Create task
python3 scripts/fis_coordinator.py delegate \
  --agent researcher --task "Test task" --forum theory

# 2. Create Forum Thread via discord tool threadCreate

# 3. Notify Worker with Thread ID
python3 scripts/fis_coordinator.py notify \
  --ticket-id TASK_xxx --thread-id <thread_id>

# 4. Execute A2A command

# 5. Complete
python3 scripts/fis_lifecycle_pro.py complete --ticket-id TASK_xxx
```

---

*FIS 3.2 Pro | Multi-Agent Workflow Framework*
