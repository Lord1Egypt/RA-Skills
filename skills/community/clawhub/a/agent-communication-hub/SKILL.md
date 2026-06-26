---
name: agent-communication-hub
description: Provide agent-to-agent communication for OpenClaw skills with direct messaging, broadcast delivery, pub/sub events, session tracking, offline queues, and SQLite-backed persistence. Use when agents need reliable message exchange, event fan-out, subscription filtering, or communication history.
---

# Agent Communication Hub

Use this skill when multiple agents need a shared communication layer with durable delivery and session awareness.

## What It Provides

- Point-to-point, private, and broadcast messaging
- Event publish/subscribe with subscription filters
- Agent registration, presence tracking, and session history
- Offline message queueing, persistence, and acknowledgements
- SQLite-backed audit history for messages and events

## Project Layout

- `src/CommunicationHub.ts`: Main entry point that coordinates messaging, storage, queueing, and acknowledgements
- `src/EventBus.ts`: Event publish/subscribe, replay, and filter evaluation
- `src/SessionManager.ts`: Agent lifecycle, presence, and session history
- `tests/`: Vitest coverage for messaging, sessions, queueing, and events
- `examples/`: Minimal runnable example

## Workflow

1. Create a `CommunicationHub` with a SQLite database path.
2. Register agents through `SessionManager`.
3. Connect or disconnect agents to update presence state.
4. Send direct, private, or broadcast messages through `CommunicationHub`.
5. Subscribe agents to event types through `EventBus`.
6. Publish events and replay history when needed.
7. Acknowledge delivered messages to complete queue processing.

## Notes

- Broadcast delivery fans out to all registered agents except the sender.
- Offline direct messages remain queued until the recipient connects or explicitly drains the queue.
- Event filters use exact key/value matching against event payload fields.
- Message and event payloads are stored as JSON for flexible schemas.
