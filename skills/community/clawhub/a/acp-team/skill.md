---
name: acp-team
description: Team coordination layer for multi-agent workflows with mailbox, task board, and lease-based task management. Use when users need to coordinate multiple AI agents, manage shared task boards, send messages between agents, or set up team-based workflows. Triggers on "spawn agent", "team", "task board", "multi-agent", "agent coordination", "message agent", "inbox".
---

# acp-team: Multi-Agent Team Coordination

Team coordination layer for [acpx](https://github.com/openclaw/acpx) - mailbox, task board, and multi-agent workflows.

## When to Use This Skill

Use this skill when the user:

- Wants to coordinate multiple AI agents working together
- Needs a shared task board with claim/lease mechanics
- Wants agents to communicate via message inboxes
- Asks about spawning team members with different roles
- Needs task assignment and status tracking across agents

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    acp-team                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  TaskStore  │  │ MessageBus  │  │  TeamStore  │     │
│  │  .tasks/    │  │ .team/inbox │  │ .team/config│     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│         │                │                │             │
│         └────────────────┼────────────────┘             │
│                          │                              │
│                    Coordinator                          │
│                          │                              │
│                          ▼                              │
│                   acpx sessions                         │
└─────────────────────────────────────────────────────────┘
```

## Installation

```bash
npm install -g acp-team
```

Requires `acpx` to be installed:
```bash
npm install -g acpx
```

## Quick Start

```bash
# Initialize team in your project
acp-team init --name my-project

# Create tasks
acp-team task create "Fix authentication bug"
acp-team task create "Write unit tests"

# Spawn a team member
acp-team spawn alice -r coder -p "Fix the auth bug in task #1"

# Check status
acp-team status

# Send messages
acp-team msg send alice "How's the bug fix going?"
acp-team msg inbox alice
```

## Commands Reference

### Team Management

| Command | Description |
|---------|-------------|
| `acp-team init [--name <team>]` | Initialize team in project |
| `acp-team status` | Show team and task status |
| `acp-team spawn <name> -r <role> -p <prompt>` | Spawn a team member with acpx |
| `acp-team shutdown <member>` | Request member shutdown |

### Task Board

| Command | Description |
|---------|-------------|
| `acp-team task create <subject>` | Create a new task |
| `acp-team task list` | List all tasks |
| `acp-team task unclaimed` | List unclaimed tasks |
| `acp-team task claim <id> [-o <owner>]` | Claim a task |
| `acp-team task assign <id> <member>` | Assign task to member |
| `acp-team task done <id>` | Mark task as done |

### Task Lease System

| Command | Description |
|---------|-------------|
| `acp-team task claim-lease <id> -o <owner> -d <ms>` | Claim with lease (default 60s) |
| `acp-team task heartbeat <id> -t <token>` | Renew lease |
| `acp-team task release-expired` | Release all expired leases |

### Messaging

| Command | Description |
|---------|-------------|
| `acp-team msg send <to> <message>` | Send direct message |
| `acp-team msg broadcast <message>` | Broadcast to all members |
| `acp-team msg inbox [name]` | Read inbox (drains messages) |
| `acp-team msg peek [name]` | Peek inbox (without draining) |

## Task State Machine

```
pending → claimed → running → blocked → completed
                                 ↓           ↓
                            cancelled    failed
                                 ↓           ↓
                                     timed_out
```

## Message Envelope Format

```json
{
  "schema_version": "1.0",
  "message_id": "uuid",
  "trace_id": "...",
  "sender": "alice",
  "recipient": "bob",
  "type": "message",
  "content": "...",
  "created_at": 1234567890,
  "priority": 1
}
```

## File Structure

```
.team/
├── config.json          # Team configuration
└── inbox/
    ├── alice.jsonl      # Alice's inbox
    ├── bob.jsonl        # Bob's inbox
    └── lead.jsonl       # Lead's inbox

.tasks/
├── task_1.json          # Task #1
├── task_2.json          # Task #2
└── ...
```

## Workflow Example

```bash
# 1. Initialize
acp-team init --name feature-dev

# 2. Create tasks
acp-team task create "Design API schema"
acp-team task create "Implement backend"
acp-team task create "Write tests"

# 3. Spawn designer
acp-team spawn designer -r architect -p "Design the API schema for task #1" -a claude

# 4. After design is done, spawn implementer
acp-team spawn coder -r backend -p "Implement the API based on the design"

# 5. Monitor progress
acp-team status
acp-team msg inbox lead

# 6. Spawn tester
acp-team spawn tester -r qa -p "Write tests for the new API"
```

## Resources

- npm: https://www.npmjs.com/package/acp-team
