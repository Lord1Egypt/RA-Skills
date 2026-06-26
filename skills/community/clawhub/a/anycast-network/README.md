# anycast-network (ClawHub Skill)

An OpenClaw skill that connects AI assistants to the [Anycast agent network](https://agents.anycast.com). Enables listing agents, querying cross-environment connectors (databases, APIs, monitoring), sending messages to remote agents, and checking fleet status.

## Install

```bash
clawhub install anycast-network
```

## Setup

Set these environment variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `ANYCAST_API_TOKEN` | Yes | Agent token from the Anycast portal (starts with `agt_`) |
| `ANYCAST_PORTAL_URL` | No | API base URL (default: `https://agents.anycast.com`) |

Get a token at [agents.anycast.com](https://agents.anycast.com) under Agents > Tokens.

## What it does

- **List agents** — see all agents in your fleet with status, version, and last seen time
- **Send messages** — interrupt a remote agent with a question or command
- **Query connectors** — run SQL, search logs, list devices across PostgreSQL, MySQL, MongoDB, Slack, GitHub, LibreNMS, and more
- **Fleet status** — total agents, online count, connections, bytes transferred
- **Memory** — store and retrieve key-value data scoped to your tenant

## Supported connectors

PostgreSQL, MySQL, MongoDB, ClickHouse, Redis, Kubernetes, Slack, GitHub, Confluence, Jira, PagerDuty, Loki, Discord, Grafana, LibreNMS, HTTP.

## Publishing

```bash
clawhub login
clawhub publish packages/openclaw-skill --version 0.1.0
```

## License

MIT-0
