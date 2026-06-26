---
name: a2a-protocol
license: MIT
---

# a2a-protocol

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Version](https://img.shields.io/badge/version-1.0.0-blue)

> Use when building A2A-compliant agents, publishing an AgentCard for discovery, sending tasks
> to remote agents, or integrating the Agent2Agent protocol into an existing agent framework.

## What Problem This Solves

AI agents operate in silos. Even when they share infrastructure, they have no standard way to
discover peers, delegate tasks, track lifecycle, or exchange structured data across frameworks.

The A2A (Agent2Agent) protocol — an open standard maintained by Google and the a2aproject
community — solves agent interoperability. This skill makes an AI agent A2A-aware, guiding it
through discovery, task submission, streaming, push notifications, and multi-turn collaboration.

**When triggered:** When the user wants to connect agents, delegate tasks, build an A2A server,
publish an AgentCard, or understand the A2A/MCP relationship.

## Features

- **Protocol education** — full A2A overview, data model, and operation reference
- **AgentCard builder** — generate discovery-ready JSON identity documents
- **Task operations** — send, poll, stream, subscribe to remote agent tasks
- **Multi-turn support** — session and context threading across agent boundaries
- **Enterprise auth** — guidance on API key, Bearer, OAuth2, and mTLS schemes
- **Streaming events** — real-time TaskStatusUpdateEvent and TaskArtifactUpdateEvent handling

## Quick Start

### Installation

```bash
# Via ClawHub
clawhub install a2a-protocol

# Or manually
cp -r a2a-protocol/ ~/.openclaw/skills/
```

### Usage

```bash
# Learn A2A concepts
/a2a-protocol

# Build an AgentCard for discovery
/a2a-protocol build-card

# Send a task to a remote A2A agent
/a2a-protocol send-task

# Stream real-time task updates from a remote agent
/a2a-protocol stream-task

# Subscribe to push notifications from a remote agent
/a2a-protocol subscribe-task
```

### Example: Send a Task

```
/a2a-protocol send-task --agent https://target-agent/.well-known/agent.json --task "Analyze Q3 revenue"
```

## Directory Structure

```
a2a-protocol/
├── SKILL.md                    # Entry point (this skill)
├── LICENSE                    # MIT
├── README.md                  # This file
├── README_zh.md              # Chinese version
├── CONTRIBUTING.md           # Contribution guide
├── .gitignore
├── references/
│   ├── a2a-overview.md       # Protocol overview and key concepts
│   ├── data-model.md         # Core data model (Task, Message, Part, Artifact, AgentCard)
│   ├── operations.md         # All A2A operations reference
│   └── agent-card-template.md # AgentCard JSON schema with annotations
└── scripts/                  # (reserved for future helpers)
```

## References

- [A2A Protocol Specification](https://a2a-protocol.org/latest/specification/)
- [A2A on GitHub](https://github.com/a2aproject/A2A)
- [Python SDK (a2a-sdk)](https://github.com/a2aproject/a2a-python)

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

Powered by [MiniMax](https://minimax.io).