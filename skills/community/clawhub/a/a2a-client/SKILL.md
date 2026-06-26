---
name: a2a-client
description: 'Discover and send tasks to A2A agents via the A2A API Gateway. Use when: (1) finding available agents or LLM providers, (2) delegating tasks to other agents, (3) checking task status/results, (4) routing work to a specific agent. NOT for: receiving inbound A2A tasks (use a2a-server), registering this instance (use a2a-register).'
metadata: {"clawdbot":{"emoji":"🔗","requires":{"anyBins":["curl","python3"]},"os":["linux","darwin"]}}
---

# A2A Client — Agent-to-Agent Task Routing

Discover and interact with other agents through the A2A API Gateway's A2A (Agent-to-Agent) API. Send tasks, check results, and route work to the right agent.

## Sidecar Principle

This skill is strictly an **OpenClaw sidecar** — it talks TO the A2A API Gateway using the gateway's existing API format. The gateway's endpoints are the contract; OpenClaw is just a participant. Never assume what the other end looks like — it could be MC2, another OpenClaw, or anything else that speaks A2A. These scripts consume the gateway's API as-is.

## Configuration

All scripts read from a shared `a2a.conf` file (located in this skill directory). The gateway URL **must** be configured before use — there are no hardcoded defaults.

**Priority order:** CLI flags → env vars → `a2a.conf` → auto-detected defaults

Run `a2a-register/a2a-setup.sh` to create your config interactively, or manually create `a2a-client/a2a.conf`:

```bash
A2A_GATEWAY_URL="http://YOUR_GATEWAY_IP:8090"
A2A_GATEWAY_API_KEY="your-key-here"
AGENT_SLUG="your-hostname"
```

If `A2A_GATEWAY_URL` is not set anywhere, scripts will exit with an error message.

## When to Use

- **Discover agents/providers** — Before sending tasks, or when the user asks about available agents or LLM providers
- **Send tasks** — When delegating work to another agent via the gateway, or when another agent's capabilities are better suited
- **Check task results** — When tracking a previously sent task or retrieving completed results
- **Route to specific agents** — When a task should be handled by a particular A2A agent (use `--target-agent`)

## Authentication

All scripts automatically obtain an admin JWT from the gateway (`GET /v0/admin/bootstrap`). The gateway uses this JWT for API authentication. No manual auth handling needed.

## Tools

### a2a-discover.sh — List Agents & Providers

```bash
./a2a-discover.sh [--gateway-url URL] [--api-key KEY]
```

Lists registered A2A agents and all configured LLM providers with their models. Use provider slugs as `--agent` values when sending tasks.

**Always discover before sending a task** to confirm the target exists and is online.

```bash
# List all agents and providers (uses a2a.conf)
./a2a-discover.sh

# Override gateway URL
./a2a-discover.sh --gateway-url http://GATEWAY_LAN_IP:8090
```

### a2a-send-task.sh — Send a Task

```bash
./a2a-send-task.sh --agent <slug> --message "task description" \
  [--model auto] [--target-agent <slug>] [--session-id <id>] \
  [--gateway-url URL] [--api-key KEY]
```

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--agent` | ✅ | — | Provider/agent slug (e.g., `groq`, `ozore`, `mistral`) |
| `--message` | ✅ | — | Task instruction/message body |
| `--model` | ❌ | `auto` | Model preference (e.g., `groq/llama-3.3-70b-versatile`) |
| `--target-agent` | ❌ | — | A2A agent routing hint (directs task to a specific registered agent) |
| `--session-id` | ❌ | auto | Custom session ID (auto-generated if omitted) |
| `--gateway-url` | ❌ | from config | Override gateway URL |
| `--api-key` | ❌ | from config | Override API key |

```bash
# Send a task with auto model selection
./a2a-send-task.sh --agent groq --message "Analyze the Q3 sales data"

# Specific model
./a2a-send-task.sh --agent mistral --message "Draft a blog post" --model mistral/mistral-small-latest

# Route to a specific A2A agent
./a2a-send-task.sh --agent ozore --message "Refactor the auth module" --target-agent coder

# Custom session ID
./a2a-send-task.sh --agent groq --message "Check logs" --session-id my-session-001
```

### a2a-get-task.sh — Check Task Status

```bash
./a2a-get-task.sh --task-id <id> [--gateway-url URL] [--api-key KEY]
```

Retrieves the current status and any results of a previously sent task. Shows task metadata, model used, token usage, and the LLM response.

```bash
./a2a-get-task.sh --task-id 0566802a3e6931629df5a7baaba2d797
```

## Typical Workflow

1. **Configure** → Create `a2a.conf` or set `A2A_GATEWAY_URL` env var
2. **Discover** → `./a2a-discover.sh` to find available providers and models
3. **Send** → `./a2a-send-task.sh --agent <slug> --message "..."` to delegate work
4. **Poll** → `./a2a-get-task.sh --task-id <id>` to check progress (tasks often complete synchronously)
5. **Retrieve** → Same get-task call returns results when completed

## Environment Variables

| Variable | Description |
|----------|-------------|
| `A2A_GATEWAY_URL` | Gateway URL (required if not in a2a.conf) |
| `A2A_GATEWAY_API_KEY` | API key for task auth |
