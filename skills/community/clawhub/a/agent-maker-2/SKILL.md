---
name: agent-maker
description: Create autonomous AI agents for OpenClaw with guided discovery — clarifies purpose, personality, skills, channels, automation, and security before generating a fully configured agent workspace.
---

# Agent Maker

Create autonomous AI agents for OpenClaw through an intelligent guided process.

## How This Skill Works

When the user wants to create a new agent, you MUST follow the **Discovery Flow** below to gather requirements before running any creation scripts. Do NOT immediately ask for all parameters at once — guide the user through a natural conversation to understand what they truly need.

## Discovery Flow

### Phase 1: Purpose & Identity

Start by understanding the agent's core purpose. Ask ONE question at a time and build on answers:

**1. What problem does this agent solve?**
- What tasks will it handle?
- Who will interact with it? (the user directly, other agents, external contacts)
- Is it a specialist (deep in one domain) or generalist?

**2. Derive identity from purpose:**
- **Name**: Suggest a memorable name that reflects the role
- **ID**: Lowercase, hyphenated (e.g., `research-bot`, `health-tracker`)
- **Emoji**: Choose one that represents the agent's function
- **Specialty**: One-line description of what the agent does

**3. Choose the right model based on workload:**

| Use Case | Recommended Model | Why |
|----------|------------------|-----|
| Deep research, complex reasoning, coding | `anthropic/claude-opus-4-6` | Most capable, best for complex tasks |
| General tasks, balanced cost/quality | `anthropic/claude-sonnet-4-6` | Good balance of speed and capability |
| Fast responses, simple tasks, high volume | `anthropic/claude-haiku-4-5` | Fastest and cheapest |
| Image generation/understanding | `google/gemini-2.5-flash` | Strong multimodal capabilities |
| Budget-friendly, coding-focused | `deepseek/deepseek-chat` | Cost-effective for code tasks |

Ask the user about their priorities (quality vs cost vs speed) to recommend the right model.

### Phase 2: Personality & Behavior

**4. Define personality traits:**
- Communication style (formal/casual/technical/friendly)
- Proactivity level (waits for instructions vs takes initiative)
- Verbosity (concise vs detailed responses)
- Any specific persona or character?

**5. Define boundaries:**
- What should this agent NEVER do?
- When should it escalate to a human or main agent?
- What level of autonomy? (Tier 1: read-only/draft, Tier 2: can act, Tier 3: fully proactive)

### Phase 3: Workflow & Tools

**6. What is the agent's main workflow?**
Walk through a typical interaction:
- What triggers the agent? (user message, cron job, heartbeat, other agent)
- What steps does it take?
- What output does it produce?
- Where does it store results?

**7. What tools does this agent need?**

Available built-in tools:
- `read`, `write`, `edit`, `apply_patch` — file operations
- `exec` — shell command execution
- `browser` — web browsing and automation
- `web_search` — search the web (multiple providers)
- `web_fetch` — fetch URL content
- `image_generate` — create images
- `image` — analyze/understand images
- `memory_search`, `memory_get` — semantic memory recall
- `sessions_list`, `sessions_send`, `sessions_history` — inter-agent communication
- `sessions_spawn` — spawn sub-agent tasks
- `canvas` — display UI on mobile nodes
- `nodes`, `nodes.run` — execute on connected devices
- `cron_list`, `cron_add`, `cron_remove` — manage scheduled tasks

Should any tools be **denied** for security? (e.g., deny `exec`, `write` for a read-only agent)

**8. Does this agent need specific skills?**
- Any existing skills from ClawHub or `~/.openclaw/skills/`?
- Need custom workspace-level skills?
- Will this agent have its own `<workspace>/skills/` directory?

### Phase 4: Communication & Channels

**9. How will users interact with this agent?**

Options:
- **Direct chat** via OpenClaw sessions (default)
- **WhatsApp** — needs a WhatsApp account/number
- **Telegram** — needs a Telegram bot token
- **Discord** — needs a Discord bot token
- **Slack**, **iMessage**, **Signal**, etc.
- **WebChat** — browser-based interface
- **API only** — no direct channel, coordinated by other agents

**10. Multi-agent coordination:**
- Will this agent be coordinated by a main/orchestrator agent?
- Will it communicate with other agents? Which ones?
- Should agent-to-agent messaging be enabled?

If channels are needed, you'll need to set up **bindings** to route messages to this agent. Example:
```json5
{
  bindings: [
    { agentId: "agent-id", match: { channel: "telegram", accountId: "agent-bot" } }
  ]
}
```

### Phase 5: Automation & Memory

**11. Does this agent need scheduled tasks?**

Two options — explain the difference:

| Feature | Heartbeat | Cron |
|---------|-----------|------|
| Runs in | Main session (shared context) | Isolated or main session |
| Timing | Periodic interval (e.g., every 30m) | Exact schedule (cron expression) |
| Best for | Monitoring, checking inbox, context-aware tasks | Reports, reminders, exact-time tasks |
| Cost | Lower (batched checks) | Per-job cost |

**Heartbeat setup** (recommended for monitoring agents):
- What should the agent check periodically?
- How often? (default: 30m)
- Active hours? (e.g., 08:00-22:00)
- Where to deliver alerts? (last channel, specific channel, none)

**Cron setup** (recommended for scheduled tasks):
- What tasks need exact timing?
- What schedule? (daily at 7am, every Monday, etc.)
- What timezone?
- Isolated session or main session?
- Should results be announced to a channel?

**12. Memory configuration:**
- Daily memory logs are automatic (`memory/YYYY-MM-DD.md`)
- Does the agent need `MEMORY.md` for long-term curated memory?
- Should memory be private or shared with other agents?
- Set up a daily memory consolidation cron job?

### Phase 6: Security & Sandbox

**13. Security posture:**

| Mode | Description | Use Case |
|------|-------------|----------|
| `off` | No sandboxing, full host access | Trusted personal agents |
| `non-main` | Sandbox non-main sessions only | Mixed trust environments |
| `all` | Full sandbox for all sessions | Untrusted inputs, shared agents |

- Does this agent handle untrusted input? (e.g., messages from groups, external contacts)
- Should file access be restricted?
- Should tools be restricted? (allow/deny lists)

## Agent Creation

After gathering all requirements, create the agent using this process:

### Step 1: Create agent via CLI

```bash
openclaw agents add <agent-id>
```

This creates the proper directory structure under `~/.openclaw/agents/<agent-id>/`.

### Step 2: Create workspace & files

Run the creation script with gathered parameters:

```bash
{baseDir}/scripts/create-agent.sh \
  --name "Agent Name" \
  --id "agent-id" \
  --emoji "🤖" \
  --specialty "What this agent does" \
  --model "provider/model-name" \
  --workspace "/path/to/workspace" \
  --personality "Communication style and traits" \
  --boundaries "What the agent should not do" \
  --workflow "Step-by-step workflow description" \
  --tools-allow "tool1,tool2,tool3" \
  --tools-deny "tool4,tool5" \
  --autonomy "tier1|tier2|tier3" \
  --heartbeat-every "30m" \
  --heartbeat-target "last" \
  --heartbeat-active-hours "08:00-22:00" \
  --sandbox "off|non-main|all"
```

The script creates these workspace files:
- **SOUL.md** — Personality, purpose, and behavioral guidelines (tailored to specialty)
- **AGENTS.md** — Operating instructions, rules, priorities
- **HEARTBEAT.md** — Periodic checklist (if heartbeat enabled)
- **IDENTITY.md** — Name, emoji, vibe
- **TOOLS.md** — Tool usage notes and conventions
- **USER.md** — User context (who the agent serves)
- **memory/** — Daily memory directory

### Step 3: Update gateway config

The script automatically:
- Adds the agent to `agents.list` in gateway config
- Configures model, identity, sandbox, and tool policies
- Sets up heartbeat configuration if requested
- Restarts the gateway to apply changes

### Step 4: Configure bindings (if channels needed)

If the agent needs channel routing, apply a config patch:

```bash
openclaw gateway config.patch --raw '{
  "bindings": [
    {
      "agentId": "<agent-id>",
      "match": { "channel": "<channel>", "accountId": "<account>" }
    }
  ]
}'
```

### Step 5: Set up cron jobs (if needed)

```bash
openclaw cron add \
  --name "<Job Name>" \
  --cron "<cron expression>" \
  --tz "<timezone>" \
  --session "<agent-id>" \
  --system-event "<instruction>" \
  --wake now
```

### Step 6: Set up skills (if needed)

For agent-specific skills, create them in `<workspace>/skills/`:
```bash
mkdir -p <workspace>/skills/<skill-name>
# Create SKILL.md in the skill directory
```

For shared skills:
```bash
openclaw skills install <skill-slug>
```

### Step 7: Verify & test

```bash
# Verify agent is registered
openclaw agents list --bindings

# Check gateway status
openclaw gateway status

# Test the agent
openclaw agent --agent <agent-id> --message "Hello! Introduce yourself."

# Or via session tools
sessions_send({ label: "<agent-id>", message: "Hello!" })
```

## Post-Creation Customization

After the agent is created, help the user refine:

1. **SOUL.md** — Review and refine personality, add specific instructions
2. **AGENTS.md** — Add standing orders, red lines, specific rules
3. **HEARTBEAT.md** — Fine-tune periodic checklist
4. **TOOLS.md** — Document tool-specific conventions
5. **Workspace skills** — Create agent-specific skills if needed

## Example Discovery Conversations

### Example 1: Research Agent

**User:** "I want an agent that does deep research for me"

**Discovery:**
- Purpose: Deep research, competitive analysis, summarization
- Model: `anthropic/claude-opus-4-6` (needs complex reasoning)
- Personality: Thorough, analytical, cites sources
- Autonomy: Tier 2 (can search web, write reports)
- Tools: `web_search`, `web_fetch`, `browser`, `read`, `write`, `memory_search`
- Tools denied: `exec`, `image_generate`
- Channels: Coordinated by main agent via `sessions_send`
- Automation: Daily memory cron at 23:00
- Sandbox: `off` (trusted personal agent)

### Example 2: Family Group Bot

**User:** "I need a bot for my family WhatsApp group"

**Discovery:**
- Purpose: Answer questions, share fun facts, help with planning
- Model: `anthropic/claude-sonnet-4-6` (balanced cost/quality)
- Personality: Friendly, casual, family-appropriate
- Autonomy: Tier 1 (read-only, suggest but don't act)
- Tools allowed: `read`, `web_search`, `sessions_list`
- Tools denied: `write`, `edit`, `exec`, `browser`, `apply_patch`
- Channels: WhatsApp group with mention-based activation
- Sandbox: `all` (handles untrusted group messages)
- Heartbeat: Off (only responds when mentioned)

### Example 3: Health Tracker

**User:** "I want an agent to track my health and remind me of medications"

**Discovery:**
- Purpose: Health tracking, medication reminders, wellness monitoring
- Model: `anthropic/claude-sonnet-4-6`
- Personality: Caring, encouraging, precise
- Autonomy: Tier 3 (proactive reminders)
- Tools: `read`, `write`, `memory_search`, `cron_add`
- Channels: WhatsApp DM or Telegram
- Automation: Heartbeat every 2h during active hours + medication cron jobs
- Sandbox: `off` (personal trusted agent)
- Memory: Daily health logs + curated MEMORY.md for long-term patterns

## Inter-Agent Coordination

After creating an agent, explain how it fits into the user's multi-agent system:

### List agents
```typescript
sessions_list({ kinds: ["agent"], limit: 10, messageLimit: 3 })
```

### Send tasks to agents
```typescript
sessions_send({
  label: "agent-id",
  message: "Your task description here"
})
```

### Spawn isolated sub-agent work
```typescript
sessions_spawn({
  agentId: "agent-id",
  task: "Complex task description",
  model: "anthropic/claude-opus-4-6",
  runTimeoutSeconds: 3600,
  cleanup: "delete"
})
```

### Check agent history
```typescript
sessions_history({ sessionKey: "agent-session-key", limit: 50 })
```

## Troubleshooting

**"Agent not appearing after creation"**
- Run `openclaw gateway restart`
- Check `openclaw agents list --bindings`

**"Agent not responding to messages"**
- Verify bindings are correct: `openclaw gateway config.get --format json | jq '.bindings'`
- Check agent session: `openclaw sessions list --agent <agent-id>`

**"Model errors"**
- Verify model format: `provider/model-name`
- Check model availability: `openclaw models list`
- Ensure API key is configured for the provider

**"Heartbeat not running"**
- Check config: `openclaw gateway config.get --format json | jq '.agents'`
- Verify active hours and timezone settings
- Check HEARTBEAT.md exists and has content (empty files skip execution)

**"Cron job not firing"**
- List jobs: `openclaw cron list`
- Check timezone: ensure IANA timezone format
- Verify session target exists

## Requirements

- OpenClaw installed and configured
- `jq` for JSON processing
- Node.js/npm via nvm (for OpenClaw)
- Python 3.6+ (standard library only)
