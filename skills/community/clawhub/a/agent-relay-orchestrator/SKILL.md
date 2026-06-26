---
name: agent-relay-orchestrator
description: Multi-worker orchestration for Claude Code with Notion visibility
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - NOTION_TOKEN
        - NOTION_PAGE_ID
      bins:
        - node
        - claude
    primaryEnv: NOTION_TOKEN
    emoji: "\U0001F500"
    homepage: https://github.com/TheAgentAcademy/agent-relay-orchestrator
    os:
      - macos
      - linux
    install:
      - kind: node
        package: "@notionhq/client"
        bins: []
      - kind: node
        package: "agent-relay"
        bins: []
      - kind: node
        package: "better-sqlite3"
        bins: []
---

# Agent Relay Orchestrator

Manage multiple Claude Code workers from a single control point. Spawn, route, suspend, and resume persistent AI sessions with full context preservation.

**Important:** This skill assumes the Agent Relay Orchestrator is running on `http://localhost:3890`. Start it with `npm start` in the repo directory before using these commands.

## Prerequisites

- Claude Code CLI installed and authenticated
- Node.js 20+
- The orchestrator repo cloned and configured (see [README](https://github.com/TheAgentAcademy/agent-relay-orchestrator))

## Setup

```bash
git clone https://github.com/TheAgentAcademy/agent-relay-orchestrator.git
cd agent-relay-orchestrator
npm install
cp .env.example .env
# Edit .env with your Notion credentials
npm start
```

## API Endpoints

The orchestrator exposes an HTTP API on port 3890 (configurable via `RELAY_PORT`).

### Health Check

```bash
curl http://localhost:3890/health
```

Returns service status, active workers, and ticker state.

### Spawn a Worker

```bash
curl -X POST http://localhost:3890/spawn \
  -H 'Content-Type: application/json' \
  -d '{"name": "ReviewWorker", "task": "You review pull requests and suggest improvements."}'
```

Optional: pass `"continueFrom": "<sessionId>"` to resume a previous session.

### Send a Message

```bash
curl -X POST http://localhost:3890/send \
  -H 'Content-Type: application/json' \
  -d '{"to": "CodeWorker", "text": "refactor the auth module to use JWT"}'
```

If the target worker is suspended, it auto-resumes. If it doesn't exist but has a profile, it spawns.

### List Active Workers

```bash
curl http://localhost:3890/workers
```

Returns name, status, label, project, and last message time for each active worker.

### List All Projects

```bash
curl http://localhost:3890/projects
```

Shows all workers (active + suspended) with session IDs and profile info.

### Suspend a Worker

```bash
curl -X DELETE http://localhost:3890/worker/ReviewWorker
```

Session is preserved for future resume. Add `?purge=true` to clear session permanently.

### Event Feed

```bash
# All events
curl http://localhost:3890/events

# Events since a timestamp
curl "http://localhost:3890/events?since=2026-01-01T00:00:00Z&limit=50"

# Events for a specific worker
curl http://localhost:3890/sessions/CodeWorker/events
```

### Stats

```bash
curl http://localhost:3890/stats
```

Returns total events, total sessions, events in last 24h, and average latency.

### Toggle Telegram Ticker

```bash
# Enable
curl -X POST http://localhost:3890/ticker \
  -H 'Content-Type: application/json' \
  -d '{"enabled": true}'

# Disable
curl -X POST http://localhost:3890/ticker \
  -d '{"enabled": false}'
```

## Example Workflows

### Parallel Task Execution

```bash
# Spawn specialized workers
curl -X POST http://localhost:3890/spawn -d '{"name": "TestWorker", "task": "You run tests and report results."}'
curl -X POST http://localhost:3890/spawn -d '{"name": "DocWorker", "task": "You write documentation."}'

# Send tasks in parallel
curl -X POST http://localhost:3890/send -d '{"to": "TestWorker", "text": "run the full test suite"}'
curl -X POST http://localhost:3890/send -d '{"to": "DocWorker", "text": "update the API docs for the new auth endpoints"}'

# Check progress
curl http://localhost:3890/workers
```

### Session Resume After Restart

```bash
# Worker state is persisted. After restarting the service:
npm start
# CodeWorker auto-resumes with full conversation context
```

## Full Documentation

See the [GitHub repo](https://github.com/TheAgentAcademy/agent-relay-orchestrator) for architecture docs, Notion setup guide, and worker lifecycle details.
