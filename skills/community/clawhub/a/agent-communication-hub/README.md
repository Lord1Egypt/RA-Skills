# agent-communication-hub

`agent-communication-hub` is an OpenClaw skill and TypeScript library for agent-to-agent communication. It provides durable messaging, pub/sub events, session presence, and offline queue handling backed by SQLite.

## Features

- Direct, private, and broadcast messaging
- Event publish/subscribe with payload filtering
- Agent registration, online state, and session history
- Offline message queueing with delivery acknowledgement
- SQLite persistence for audit and replay

## Installation

```bash
npm install
```

## Usage

```ts
import { CommunicationHub } from "./src/CommunicationHub.js";

const hub = new CommunicationHub({ dbPath: "./agent-hub.sqlite" });

hub.sessions.registerAgent({ id: "planner" });
hub.sessions.registerAgent({ id: "worker" });

hub.sessions.connectAgent({ agentId: "planner" });

const message = hub.sendDirectMessage({
  senderId: "planner",
  recipientId: "worker",
  payload: { taskId: "task-1" },
});

console.log(message.status); // pending when worker is offline
```

## API Overview

### `CommunicationHub`

- `sendDirectMessage()`: send a point-to-point message
- `sendPrivateMessage()`: send a private message with the same delivery semantics as direct messaging
- `broadcastMessage()`: fan out a message to all registered agents except the sender
- `getPendingMessages()`: inspect offline queue state
- `drainOfflineQueue()`: deliver queued messages after reconnect
- `acknowledgeMessage()`: mark a delivered message as processed
- `listMessages()`: query message history

### `SessionManager`

- `registerAgent()`: register or update agent metadata
- `connectAgent()`: mark an agent online and create a session record
- `disconnectAgent()`: mark an agent offline and close live sessions
- `listAgents()`: inspect known agents
- `getSessionHistory()`: review past sessions

### `EventBus`

- `subscribe()`: subscribe an agent to an event type with exact-match payload filters
- `unsubscribe()`: remove a subscription
- `publish()`: persist an event and resolve matching recipients
- `replay()`: query historical events for tracing or recovery

## Development

```bash
npm run build
npm test
npm run example
```
