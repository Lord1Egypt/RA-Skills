# claw-observability

> Zero-config, real-time observability for Claude Code multi-agent workflows. See every agent light up, every task complete, every error surface — without writing a single line of reporting code.

**[Live Demo](https://claw.ia.br)** &nbsp;|&nbsp; **[Dashboard Screenshots](#what-you-get)** &nbsp;|&nbsp; **[Install in 2 minutes](#installation)**

---

## The Problem

You're running Claude Code with the Task tool — orchestrating backend agents, frontend agents, security reviewers, database specialists — all working in parallel. But you have **zero visibility** into what's happening:

- Which agents are active right now?
- Did that security review finish or fail?
- How long did the database migration task take?
- Are two agents stuck waiting on each other?

You're flying blind. The only signal you get is the final response.

## The Solution

**CLAW Observability** uses Claude Code hooks to automatically intercept every agent lifecycle event and report it to a real-time visual dashboard. No curl commands. No agent instructions. No manual reporting. Just install, set two env vars, and every Task tool invocation becomes a visible, trackable, replayable event.

```
User sends message → Hook fires → Dashboard updates in real-time
Agent spawns task  → Hook fires → Sub-agent lights up in organogram
Task completes     → Hook fires → Agent dims, timeline records event
Task fails         → Hook fires → Agent turns red, error logged
```

**The agent never knows CLAW exists.** Hooks operate at the shell level, outside the LLM context. Your agents keep working normally while you get full operational visibility.

## What You Get

### Interactive Agent Organogram
A live React Flow graph that visualizes your entire agent hierarchy. Agents glow when active, pulse on errors, and dim on completion. Powered by SSE — updates in under 200ms.

### Real-Time Event Feed
Every status change, every task start/stop, every error — streamed live via Server-Sent Events. Filter by agent, status, or time range.

### Execution Timeline
Chronological trace of every agent activation with timestamps, durations, and task grouping. Replay any session to understand exactly what happened.

### Analytics Dashboard
Error rates, agent utilization heatmaps, activity over time. Identify bottlenecks before they become problems.

### Multi-Machine Support
Each machine gets its own API key. Monitor agents across multiple workstations, CI runners, or team members from a single dashboard.

## How It Works

This skill installs **5 Claude Code hooks** that fire on shell-level lifecycle events:

| Hook Event | What Gets Reported |
|---|---|
| `UserPromptSubmit` | Root orchestrator → `running` |
| `PreToolUse` (Task) | Sub-agent → `running` (mapped from `subagent_type`) |
| `PostToolUse` (Task) | Sub-agent → `success` |
| `PostToolUseFailure` (Task) | Sub-agent → `error` |
| `Stop` | Root orchestrator → `success` |

The hook script reads `subagent_type` from the Task tool input, maps it to a named agent in your CLAW dashboard, and fires an async HTTP request. Total overhead: **< 50ms per event** (non-blocking, fire-and-forget).

### Subagent Type Mapping

The hook script automatically maps your Task tool `subagent_type` values to named dashboard agents:

| subagent_type | Dashboard Agent | Role |
|---|---|---|
| `anakin` | Anakin | Orchestrator |
| `chewie-backend` | Chewbacca | Backend |
| `leia-frontend` | Leia Organa | Frontend |
| `obi-wan` | Obi-Wan Kenobi | Database |
| `han-architect` | Qui-Gon Jinn | Architect |
| `darth-maul` | Darth Maul | Security |
| `r2-devops-platform` | R2-D2 | DevOps |
| `forge` | Forge | Containers |
| `c3po-quality-guardian` | C-3PO | Quality |
| `yoda` | Yoda | Product |
| `luke-project-execution` | Luke Skywalker | Execution |
| `rey-delivery-governance` | Rey | Delivery |
| `padme-lgpd-compliance` | Padme Amidala | Compliance |
| `Explore` / `general-purpose` | Anakin | General |
| Any unknown type | Anakin | Fallback |

Don't use these agent names? No problem — the mapping is a simple bash `case` statement in `hooks/claw-hooks.sh`. Edit it to match your team's naming convention in under a minute.

## Installation

### 1. Create your CLAW account

Go to **[claw.ia.br](https://claw.ia.br)**, create an account, then navigate to **Machines → Create Machine**. Copy your API key (format: `claw_xxxx...`).

### 2. Set environment variables

Add to your shell profile (`~/.zshrc`, `~/.bashrc`, or `~/.config/fish/config.fish`):

```bash
export CLAW_API_KEY="claw_your_api_key_here"
export CLAW_BASE_URL="https://claw.ia.br"
```

Reload your shell: `source ~/.zshrc`

### 3. Run setup

```bash
bash setup.sh
```

This will:
- Install the hook handler to `~/.claude/hooks/claw/`
- Register hooks in `~/.claude/settings.json` (preserves your existing hooks)
- Test the connection to your CLAW server

### 4. Bootstrap agents (optional)

To pre-populate your dashboard with the full 21-agent hierarchy:

```bash
bash bootstrap.sh
```

This registers every agent in the organogram so they're visible before the first real session.

### 5. Restart Claude Code

Hooks are loaded on startup. Restart Claude Code, send a message, and watch your dashboard light up.

## Example Flow

**User:** "Implement the payment module with backend, frontend, and security review"

**What happens automatically (zero agent involvement):**

1. `UserPromptSubmit` → Sheev Palpatine lights up (root orchestrator)
2. Agent spawns 3 parallel Tasks → Chewbacca, Leia, Darth Maul all light up simultaneously
3. Darth Maul finishes first → dims to success
4. Chewbacca finishes → dims to success
5. Leia finishes → dims to success
6. Agent spawns C-3PO for tests → lights up, then dims on success
7. `Stop` → Sheev Palpatine dims

**Total reporting code written by the agent: zero.** Everything flows through hooks.

## Requirements

| Requirement | Why |
|---|---|
| `curl` | HTTP requests to CLAW API |
| `python3` | JSON parsing in hook scripts (available by default on macOS/Linux) |
| `CLAW_API_KEY` | Authenticates your machine |
| `CLAW_BASE_URL` | Points to your CLAW server |

## Directory Structure

```
claw-observability/
├── SKILL.md              # Skill definition (loaded into agent context)
├── README.md             # This file
├── setup.sh              # One-time hook installer
├── bootstrap.sh          # Optional: pre-populate agent hierarchy
├── clawhub.json          # ClawHub registry metadata
├── CHANGELOG.md          # Version history
├── .clawhubignore        # Excluded files
├── hooks/
│   └── claw-hooks.sh     # Hook handler (all events)
└── examples/
    ├── basic-usage.md    # Single-agent flow
    ├── multi-agent.md    # Parallel agents
    └── error-handling.md # Error and recovery
```

## Performance

- **Hook execution time:** < 50ms (non-blocking `curl` with `&`)
- **Dashboard update latency:** < 200ms (SSE push)
- **Rate limit:** 300 events/minute per API key
- **Zero impact on agent performance:** hooks run in background subshells
- **Graceful degradation:** if CLAW is unreachable, hooks silently exit (no error, no retry, no block)

## Security

- API keys are scoped per machine (not per user)
- All events are tenant-isolated by user account
- No sensitive data transmitted — only agent names, statuses, and task descriptions
- HTTPS enforced in production
- Rate limiting prevents abuse (300 req/min)
- Webhook-level auth with API key headers

## Troubleshooting

**Hooks not firing?**
- Run `claude /hooks` to verify hook configuration
- Check `~/.claude/settings.json` for CLAW hook entries
- Restart Claude Code (hooks load on startup)

**Events not appearing?**
- Verify env vars: `echo $CLAW_API_KEY $CLAW_BASE_URL`
- Test manually: `echo '{"hook_event_name":"Stop","session_id":"test"}' | bash ~/.claude/hooks/claw/claw-hooks.sh`
- Check API health: `curl -s "$CLAW_BASE_URL/api/health"`

**Dashboard shows agents but no updates?**
- SSE connection may have dropped — refresh the page
- Check browser DevTools → Network → EventSource for SSE connection status

## API Reference

### POST /api/v1/events

```json
{
  "agent_id": "chewbacca",
  "agent_name": "Chewbacca",
  "agent_type": "backend",
  "parent_agent_id": "anakin",
  "status": "running",
  "message": "Implementing payment module",
  "task_id": "implement-payment-module",
  "run_id": "session-abc123"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `agent_id` | string | Yes | Agent identifier |
| `agent_name` | string | Yes | Display name |
| `agent_type` | string | Yes | Role (orchestrator, backend, frontend, etc.) |
| `parent_agent_id` | string | No | Creates hierarchy in organogram |
| `status` | string | Yes | `running` · `thinking` · `waiting` · `success` · `error` · `idle` |
| `message` | string | Yes | Activity description (max 500 chars) |
| `task_id` | string | No | Groups events by task |
| `run_id` | string | No | Groups events by session |

### POST /api/v1/heartbeat

```json
{ "hostname": "my-machine" }
```

## License

MIT

## Links

- **Platform:** [claw.ia.br](https://claw.ia.br)
- **Issues:** [GitHub Issues](https://github.com/rdmss/claw-observability/issues)
