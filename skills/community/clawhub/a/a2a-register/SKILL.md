---
name: a2a-register
description: 'Register, deregister, and manage this OpenClaw instance as an A2A agent in the A2A API Gateway. Use when: (1) registering this instance so other agents can discover and route tasks to it, (2) deregistering when going offline, (3) sending heartbeat to signal liveness, (4) checking registration status. NOT for: sending tasks to other agents (use a2a-client), receiving tasks (use a2a-server).'
metadata: {"clawdbot":{"emoji":"📝","requires":{"anyBins":["curl","python3"]},"os":["linux","darwin"]}}
---

# A2A Register — Agent Registration Management

Register and manage this OpenClaw instance as an A2A agent in the A2A API Gateway. Other agents discover this instance through the gateway registry, so registration is required before receiving inbound tasks.

## Sidecar Principle

This skill is strictly an **OpenClaw sidecar** — it uses the A2A API Gateway's existing admin API to register, deregister, heartbeat, and check status. The gateway's admin endpoints are the contract; OpenClaw is just a participant. Never assume what other registered agents look like or how they connect — they could be MC2, another OpenClaw, or anything else that speaks A2A. These scripts call the gateway's admin API as-is.

## Configuration

All scripts read from a shared `a2a.conf` file (located in the `a2a-client` skill directory). The gateway URL **must** be configured — there are no hardcoded defaults.

**Priority order:** CLI flags → env vars → `a2a.conf` → auto-detected defaults

| Setting | Auto-detected Default | Description |
|---------|-----------------------|-------------|
| Gateway URL | *none — required* | A2A API Gateway URL (`A2A_GATEWAY_URL`) |
| Agent Name | `hostname -s` (lowercase) | Display name (`AGENT_NAME`) |
| Agent Slug | `hostname -s` (lowercase) | URL-safe identifier (`AGENT_SLUG`) |
| Agent URL | `http://{Tailscale IP}:{port}` | Agent endpoint (`AGENT_URL`) |
| Capabilities | `chat,code,research` | Comma-separated (`AGENT_CAPABILITIES`) |
| Auth Type | `bearer` | Auth method (`AGENT_AUTH_TYPE`) |
| API Key | *empty* | For listener auth (`A2A_GATEWAY_API_KEY`) |

### Quick Setup

```bash
# Interactive setup — creates a2a.conf for you
./a2a-setup.sh

# Non-interactive (env vars required)
A2A_GATEWAY_URL=http://GATEWAY_IP:8090 A2A_GATEWAY_API_KEY=your-key ./a2a-setup.sh --non-interactive
```

## When to Use

- **Setup** — First time configuring this instance for A2A
- **Register** — When this OpenClaw instance needs to be discoverable by other A2A agents
- **Deregister** — When going offline or removing this instance from the gateway
- **Heartbeat** — Periodically signal that this instance is alive and reachable
- **Status** — Check whether this instance is registered and view its current configuration

## Tools

### a2a-setup.sh — Interactive Configuration

```bash
./a2a-setup.sh [--non-interactive] [--conf PATH]
```

Creates or updates the shared `a2a.conf` file. In interactive mode, prompts for all values with auto-detected defaults. In non-interactive mode, reads from environment variables.

```bash
# Interactive (recommended first time)
./a2a-setup.sh

# Non-interactive (for scripting)
A2A_GATEWAY_URL=http://GATEWAY_IP:8090 \
A2A_GATEWAY_API_KEY=your-key \
AGENT_SLUG=my-agent \
./a2a-setup.sh --non-interactive
```

### register.sh — Register This Agent

```bash
./register.sh [--gateway-url URL] [--name NAME] [--slug SLUG] [--url URL] [--capabilities CAPS]
```

Registers this OpenClaw instance in the A2A API Gateway. The script:

1. Obtains a JWT via `GET /v0/admin/bootstrap`
2. Checks if the agent slug already exists (`GET /v0/admin/agents`)
3. If new → `POST /v0/admin/agents` to create it
4. If exists → `PUT /v0/admin/agents/{id}` to update it

Idempotent — safe to run multiple times.

```bash
# Register with defaults (from a2a.conf / auto-detected)
./register.sh

# Override specific values
./register.sh --name "My Agent" --slug my-agent --url http://MY_IP:8100

# Override gateway URL
./register.sh --gateway-url http://GATEWAY_LAN_IP:8090
```

### deregister.sh — Remove This Agent

```bash
./deregister.sh [--gateway-url URL] [--slug SLUG]
```

Removes this OpenClaw instance from the gateway registry. Other agents will no longer be able to discover or route tasks to it.

```bash
./deregister.sh
```

### heartbeat.sh — Send Liveness Signal

```bash
./heartbeat.sh [--gateway-url URL] [--slug SLUG]
```

Sends a heartbeat to the gateway (`PATCH /v0/admin/agents/{id}/heartbeat`) to signal that this instance is alive and reachable. Useful for cron jobs or periodic health checks.

```bash
# One-time heartbeat
./heartbeat.sh

# In a cron (every 5 minutes)
*/5 * * * * /path/to/skills/a2a-register/heartbeat.sh
```

### status.sh — Check Registration Status

```bash
./status.sh [--gateway-url URL] [--slug SLUG]
```

Checks whether this OpenClaw instance is registered in the gateway and shows its current configuration (URL, capabilities, status).

```bash
./status.sh
```

## Typical Workflow

1. **Setup** → `./a2a-setup.sh` to create your `a2a.conf`
2. **Register** → `./register.sh` to add this instance to the gateway
3. **Start listener** → Use `a2a-server` skill's `start.sh` to begin receiving tasks
4. **Heartbeat** → Run `./heartbeat.sh` periodically (or set up a cron)
5. **Status** → `./status.sh` to verify registration
6. **Deregister** → `./deregister.sh` when going offline

## Gateway API

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v0/admin/bootstrap` | GET | Obtain admin JWT |
| `/v0/admin/agents` | GET | List all registered agents |
| `/v0/admin/agents` | POST | Register a new agent |
| `/v0/admin/agents/{id}` | PUT | Update an existing agent |
| `/v0/admin/agents/{id}` | DELETE | Remove an agent |
| `/v0/admin/agents/{id}/heartbeat` | PATCH | Signal liveness |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `A2A_GATEWAY_URL` | Gateway URL (required if not in a2a.conf) |
| `A2A_GATEWAY_API_KEY` | API key for listener auth |
| `AGENT_NAME` | Agent display name |
| `AGENT_SLUG` | Agent identifier |
| `AGENT_URL` | Agent endpoint URL |
| `AGENT_CAPABILITIES` | Comma-separated capabilities |
| `LISTENER_PORT` | Listener port (default: 8100) |
