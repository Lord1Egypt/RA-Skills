# A2A Protocol Overview

> Reference: https://a2a-protocol.org/latest/specification/

## What is A2A?

The Agent2Agent (A2A) protocol is an **open specification** enabling AI agents built on
different frameworks by different vendors, running on separate servers, to communicate
and collaborate — as agents, not just as tools.

A2A provides a common language for agents, fostering a more interconnected AI ecosystem.

## Key Goals

| Goal | Description |
|------|-------------|
| **Break Down Silos** | Connect agents across different ecosystems and frameworks |
| **Enable Complex Collaboration** | Allow specialized agents to work together on tasks a single agent cannot handle alone |
| **Promote Open Standards** | Community-driven approach to agent communication |
| **Preserve Opacity** | Agents collaborate without exposing internal memory, proprietary logic, or tool implementations |

## Core Concepts

### Agent

An AI application that:
- Exposes capabilities via an **AgentCard**
- Communicates via A2A operations (SendMessage, GetTask, etc.)
- Can act as A2A **server** (receives tasks), **client** (sends tasks), or both

### AgentCard

A JSON document at `/.well-known/agent.json` that declares:
- Agent name, version, description
- Capabilities (streaming, push notifications, authentication)
- Skills (specific capabilities exposed)
- Endpoints and auth requirements

### Task

The central unit of work in A2A:
- Has a unique `taskId`
- Has a full lifecycle: `submitted` → `working` → `completed`/`failed`/`canceled`
- Carries a `Message` (the work to be done)
- Produces `Artifact[]` (results, as `Part[]`)

### Message

A `Message` contains a `role` (user/agent) and `parts[]` — the actual content blocks.

### Part

The content unit. Types:
- `TextPart` — plain text
- `DataPart` — structured JSON data
- `FilePart` — file with inline bytes or remote URL

### Artifact

A collection of related parts forming a deliverable output (e.g., a report document,
a generated image, a data table).

## A2A vs MCP

| Aspect | A2A | MCP |
|--------|-----|-----|
| **Purpose** | Agent-to-agent collaboration | Agent-to-tool/resource connectivity |
| **Focus** | Task delegation, status tracking, multi-agent workflows | Tool invocation, resource access |
| **State** | Long-running tasks with full lifecycle | Stateless tool calls |
| **Communication** | Rich messages, artifacts, streaming events | JSON-RPC request/response |
| **Discovery** | AgentCard at `/.well-known/agent.json` | MCP server registry |

**Use both together**: MCP connects an agent to tools and resources; A2A connects
agents to each other.

## Protocol Binding

A2A supports multiple wire protocols:
- **JSON-RPC 2.0 over HTTP** — most common, agents `POST tasks/send`
- **gRPC** — for high-performance agent interop
- **HTTP+REST/JSON** — for simple integrations

## Task Lifecycle

```
[Client]                    [Server/Remote Agent]
   |                              |
   |--- tasks/send -------------->| (submit task)
   |<-- taskId + status=submitted -|
   |                              |
   |<-- streaming events (SSE) ----| (working, partial artifacts)
   |                              |
   |<-- tasks/get -----------------| (poll for completion)
   |--> task with status=completed|
   |                              |
   |--> artifacts[].parts -------->| (result delivered)
```

## A2A and Enterprise

A2A is enterprise-ready with:
- Authentication schemes: API key, HTTP Bearer, OAuth2, mTLS, OpenID Connect
- Push notifications via web hooks
- AgentCard signing for trusted discovery
- Version negotiation between agents