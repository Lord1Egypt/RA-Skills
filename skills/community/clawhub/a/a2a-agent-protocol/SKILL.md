---
name: a2a-protocol
description: >
  Use when (1) building an AI agent that needs to communicate with other agents over the
  Agent2Agent (A2A) protocol, (2) publishing an AgentCard for discovery, (3) acting
  as an A2A client or server, or (4) integrating A2A capabilities into an existing
  agent framework. Solves agent isolation — enabling discovery, capability negotiation,
  task delegation, and structured data exchange across different frameworks and vendors.
license: MIT
metadata:
  version: "1.0"
  category: dev-tools
  author: wangjipeng
  sources:
    - https://a2a-protocol.org/latest/specification/
    - https://github.com/a2aproject/A2A
    - https://github.com/a2aproject/a2a-python
---

# A2A Protocol Skill

An AI agent skill for building, connecting, and operating A2A-compliant agents.
This skill is the definitive guide for agents participating in the Agent2Agent protocol ecosystem.

## Core Position

This skill is **NOT** a general API wrapper — it is a protocol education and implementation guide.
It teaches agents what A2A is, how to structure AgentCards for discovery, which operations to
perform in which order, and how to handle the multi-turn task lifecycle.

This skill is **NOT** framework-specific. It guides agents regardless of whether they are built
with LangGraph, BeeAI, Google ADK, or custom code. The A2A protocol is language-agnostic.

This skill covers the JSON-RPC 2.0 over HTTP binding (the most common) plus key concepts for
gRPC and HTTP+REST bindings.

## What Problem This Solves

AI agents today operate in silos. Even when they share the same infrastructure, they have no
standard way to:
- Discover what capabilities other agents expose
- Send a task to a remote agent and track its lifecycle
- Handle streaming updates or push notifications from a remote agent
- Exchange files, structured data, or multi-part messages

The A2A protocol solves all of the above. This skill makes an AI agent A2A-aware.

## Modes

### `/a2a-protocol`

Default mode. Learn A2A concepts, data structures, and operation semantics.

**Preferred opening:** *"The A2A protocol enables agents to discover each other and collaborate
without exposing internal state. Here is the protocol overview:"*

Use it when:
- The user asks what A2A is, how it works, or why it matters
- You need to explain the difference between A2A and MCP
- You want to understand the AgentCard structure and discovery mechanism
- You need to understand the full task lifecycle (submitted → working → completed)

### `/a2a-protocol build-card`

Generate an AgentCard JSON for the agent. The AgentCard is the public identity document that
other agents use to discover capabilities, auth requirements, and connection endpoints.

**Preferred opening:** *"To publish this agent in the A2A ecosystem, I will generate an AgentCard
at `/.well-known/agent.json` declaring: name, version, capabilities, and auth requirements."*

Use it when:
- You are building an A2A server agent and need to publish its capabilities
- You need a starting-point AgentCard template to customize
- The user wants to register an agent in the A2A ecosystem

**Output:** Writes `agent-card.json` to the workspace with the complete AgentCard.

### `/a2a-protocol send-task`

Send a task to a remote A2A agent via `tasks/send`. Includes building the request, interpreting
the response (synchronous or task ID for async), and handling errors.

**Preferred opening:** *"To delegate this task to the remote agent, I will: (1) fetch its AgentCard,
(2) validate capability compatibility, (3) construct a SendMessageRequest and POST it."*

Use it when:
- You need to delegate a subtask to another agent
- You are acting as an A2A client initiating work on a remote agent
- The user says "send this task to the X agent" or "delegate to agent Y"

**Output:** Resolves to `artifacts[].parts` from the completed Task.

### `/a2a-protocol stream-task`

Set up streaming task delivery via `tasks/sendSubscribe` with SSE (Server-Sent Events), receive
incremental `TaskStatusUpdateEvent` and `TaskArtifactUpdateEvent` blocks, and reassemble the
final artifact.

**Preferred opening:** *"This remote task will take time. I will subscribe via SSE to receive
real-time status transitions and partial artifacts as they arrive."*

Use it when:
- A remote agent's task will take time and you want real-time progress updates
- You need to stream partial results as they become available
- The user says "track the task progress" or "watch for updates"

**Output:** Reassembles the final `Artifact` from accumulated streaming events.

### `/a2a-protocol subscribe-task`

Subscribe to a task's push notification channel via `tasks/subscribe`, using either SSE
streaming or webhook delivery to receive final results.

**Preferred opening:** *"I will register a push notification subscription so the remote agent
delivers the result to our callback endpoint rather than requiring us to poll."*

Use it when:
- You want the remote agent to push results back to you rather than polling
- You need asynchronous result delivery to a callback URL
- The user says "notify me when done" or "push results to this endpoint"

**Output:** Receives and validates the push payload; extracts `taskId` + `artifacts`.

### `/a2a-protocol mock-server`

Start a local mock A2A server for experimentation. The mock server is a fully functional A2A agent that serves its own AgentCard, accepts tasks via all supported operations, and responds with realistic simulated results.

**Preferred opening:** *"To experiment with A2A locally, I will start a mock A2A server on a free port. This gives us a real A2A endpoint to practice against."*

Use it when:
- You want to test A2A interactions without a real remote agent
- You need a safe sandbox to practice `send-task`, `stream-task`, or `subscribe-task`
- You want to verify that the agent correctly implements the A2A protocol before deploying
- The user says "try it out", "test A2A", "run locally", or "experiment"


**Output:** Starts an HTTP server at `http://localhost:<port>/a2a/` with a ready AgentCard.


> This mode is a no-op for agents without Python execution capability. If the host cannot run Python scripts, skip this mode.

## Execution Steps

### Mode: `/a2a-protocol` (Learn)

1. **You** read the A2A spec overview from `references/a2a-overview.md`
2. **You** review the data model objects from `references/data-model.md`
3. **You** answer the user's question using the reference material
4. If the user asks for a specific operation, **you** switch to the appropriate mode

### Mode: `/a2a-protocol build-card`

1. **You** read `references/agent-card-template.md` for the full AgentCard schema
2. **You** determine which capabilities the agent exposes (text, forms, media, streaming)
3. **You** determine auth scheme (none, API key, OAuth2, mTLS)
4. **You** determine push notification support (SSE, webhook, both, neither)
5. **You** generate a completed AgentCard JSON and write it to `agent-card.json`
6. **You** confirm the agent card URL path (default: `/.well-known/agent.json`)

### Mode: `/a2a-protocol send-task`

1. **You** read `references/operations.md` — SendMessage operation details
2. **You** identify the target agent's URL (from its AgentCard or given address)
3. **You** check the target agent's auth requirements (from its AgentCard)
4. **You** construct a `SendMessageRequest` with `taskId`, `sessionId`, `message`, and `context`
5. **You** send POST JSON-RPC 2.0 request to the target agent's A2A endpoint
6. **You** handle the response: immediate result (synchronous) or `taskId` for async polling
7. If async: **you** use `tasks/get` to poll for completion or `tasks/sendSubscribe` for streaming
8. On completion: **you** extract `artifacts[].parts` from the task result and return them

### Mode: `/a2a-protocol stream-task`

1. **You** read `references/operations.md` — SendStreamingMessage operation + streaming events
2. **You** construct a `SendMessageRequest` and set `stream: true` in configuration
3. **You** send `tasks/sendSubscribe` POST to the target agent's A2A endpoint
4. **You** receive SSE stream of `TaskStatusUpdateEvent` (status transitions) and
   `TaskArtifactUpdateEvent` (partial artifact updates)
5. **You** accumulate events until `TaskStatusUpdateEvent` with `state: completed`/`failed`/`canceled`
6. **You** close the SSE stream and extract the final artifact from accumulated data

### Mode: `/a2a-protocol subscribe-task`

1. **You** read `references/operations.md` — SubscribeToTask operation + push notification setup
2. **You** determine delivery mode: SSE stream (server-push via `tasks/sendSubscribe`) or
   webhook push (agent registers a callback URL via `tasks/sendSubscribe` with `pushConfig`)
3. For webhook mode: **you** register `PushNotificationConfig` with the target's
   `tasks/sendSubscribe` including `pushConfig.url` and `pushConfig.authentication`
4. **You** wait for delivery; validate the incoming `tasks/push` payload using the `AuthenticationInfo`
5. **You** extract `taskId` and `artifacts` from the validated push payload and return them

### Mode: `/a2a-protocol mock-server`


1. **You** locate `scripts/mock_a2a_server.py` in the skill directory
2. **You** start the server: `python3 scripts/mock_a2a_server.py --port <PORT> --name <NAME> --skills <SKILLS>`
3. **You** fetch the AgentCard from `http://localhost:<PORT>/.well-known/agent.json` to confirm it started
4. **You** optionally run `scripts/validate_agent_card.py` against the fetched AgentCard
5. **You** use `send-task`, `stream-task`, or `subscribe-task` against the local endpoint to test interactions
6. When done: **you** stop the server (Ctrl+C or SIGTERM)

## Mandatory Rules

### Do not

- **Do not** hardcode any AgentCard endpoint URLs — always use the supplied or discovered URL
- **Do not** assume unauthenticated access — always check the target agent's `AgentCard.authentication`
- **Do not** send a task without a `sessionId` if the operation requires multi-turn context
- **Do not** discard `TaskStatusUpdateEvent` blocks — they signal working/progress states
- **Do not** treat A2A as a replacement for MCP — A2A is for agent-to-agent collaboration,
  MCP is for agent-to-tool/resource connectivity; use both together
- **Do not** expose the agent's internal memory, tool implementations, or proprietary state
  in the AgentCard or in task payloads — A2A preserves agent opacity
- **Do not** return the raw `task` object — always extract and return `artifacts[].parts`
- **Do not** close an SSE stream before receiving `final: true` on a `TaskStatusUpdateEvent`

### Do

- Always validate capability compatibility before sending a task
  (check `targetAgent.capabilities.streaming` and `pushNotifications`)
- Always handle streaming with proper event accumulation — never treat partial events as final
- Always close SSE streams when the task reaches a terminal state
- Always use idempotent task IDs when retrying a failed `tasks/send`
- Always include `context.contextId` to thread multi-turn conversations across agents
- Always return structured output (`artifacts[].parts`) not raw JSON-RPC responses

## Quality Bar

A good A2A interaction **must** satisfy all of:
- AgentCard fetched from `/.well-known/agent.json` (HTTP 200, valid JSON, has required fields)
- JSON-RPC 2.0 request has `jsonrpc: "2.0"`, `method`, `params.taskId` (or server-generated), and `id`
- Task state machine transitions are followed: no `completed` before a `working` signal received
- Streaming: `TaskStatusUpdateEvent.final: true` received before closing stream
- Artifact extraction: `parts[].text` or `parts[].data` returned, not raw `task` object
- Auth: correct scheme used (Bearer token → `Authorization: Bearer`, API key → `X-API-Key`, etc.)
- Error handling: JSON-RPC error codes `-32700`/`-32600`/`-32603` recognized and surfaced as errors

A bad A2A interaction exhibits any of:
- No capability check before sending (assumes all agents accept all tasks)
- SSE stream closed before receiving `final: true` on the terminal status event
- Raw `task` object returned instead of extracted `artifacts[].parts`
- Wrong HTTP method used (GET instead of POST, or wrong path for the operation)
- Auth credentials omitted when `AgentCard.authentication.credentials: "required"`

## Good vs. Bad Examples

### Good: Sending a task with full capability check

```
1. Fetch AgentCard from https://target-agent/.well-known/agent.json
2. Verify capabilities.streaming or dataStreamingSupported matches our needs
3. Check authentication.schemes and prepare credentials if credentials: "required"
4. Construct SendMessageRequest: taskId=uuid(), sessionId, message with parts
5. POST to https://target-agent/a2a/tasks/send with Authorization header
6. Receive { task: { taskId: "abc123", status: { state: "submitted" } } }
7. Poll tasks/get until status.state === "completed"
8. Return artifacts[0].parts[0].text  ← structured output
```

### Bad: Sending a task without discovery

```
1. POST to https://target-agent/a2a/tasks/send with hardcoded payload
2. Assume success without checking status.state
3. Return raw task object instead of artifacts[].parts
```

### Good: AgentCard with complete capability declaration

```json
{
  "name": "data-analysis-agent",
  "description": "Specialized in financial data extraction and reporting",
  "version": "1.0",
  "capabilities": {
    "streaming": "SUPPORTED",
    "pushNotifications": "SUPPORTED",
    "agentPrivilege": false,
    "signedAgentCard": false
  },
  "skills": [
    { "id": "financial-data", "name": "Financial Data Extraction", "description": "..." }
  ],
  "authentication": {
    "schemes": ["httpBearer"],
    "credentials": "required"
  }
}
```

### Bad: Generic AgentCard without capability detail

```json
{
  "name": "agent",
  "description": "An AI agent"
}
```

## References

- `references/a2a-overview.md` — A2A protocol overview, key goals, A2A vs MCP comparison
- `references/data-model.md` — Core data model (Task, Message, Part, Artifact, AgentCard, streaming events)
- `references/operations.md` — All A2A operations reference (send, get, subscribe, push, cancel, list)
- `references/agent-card-template.md` — AgentCard JSON schema with full annotated example
- `references/quickstart.md` — Full end-to-end example: AgentCard → discovery → send → streaming → result
- `scripts/mock_a2a_server.py` — Start a local mock A2A agent for experimentation and testing