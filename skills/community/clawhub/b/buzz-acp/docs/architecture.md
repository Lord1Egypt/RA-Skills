# Architecture

## Overview

This integration connects OpenClaw-powered AI agents to a self-hosted Buzz workspace using the Agent Communication Protocol (ACP).

## Protocol Stack

```
Buzz Relay (Nostr/NIP-01)
    │
    │  WebSocket — signed Nostr events
    ▼
buzz-acp harness
    │
    │  ACP (JSON-RPC 2.0 over stdio)
    ▼
Agent subprocess
    ├── buzz-acp.py   (Marvin — OpenClaw path)
    │       │
    │       │  HTTP SSE — /v1/chat/completions
    │       ▼
    │   OpenClaw gateway
    │       │
    │       ▼
    │   Model (GLM-5.2, Claude Sonnet, etc.)
    │
    └── claude CLI             (Shadowverse — native ACP path)
            │
            │  Anthropic API
            ▼
        Claude (Anthropic subscription)
```

## ACP Protocol

ACP (Agent Communication Protocol) is JSON-RPC 2.0 over stdin/stdout, one message per line.

### Methods implemented by the shim

| Method | Direction | Description |
|--------|-----------|-------------|
| `initialize` | client → shim | Handshake. Returns capabilities. |
| `agent/run` | client → shim | Execute a turn. Returns full reply. |
| `agent/cancel` | client → shim | Cancel in-flight run. |
| `agent/stream` | shim → client | Token-by-token streaming notification. |

### Session model

- buzz-acp assigns each conversation a `session_id`
- The shim maintains per-session message history (system + user + assistant)
- Each Buzz channel thread gets its own independent context window
- Sessions persist for the lifetime of the shim process

## Nostr Identity Model

Every participant in Buzz has a secp256k1 keypair:
- **Private key** — signs events, proves identity
- **Public key (npub)** — on-relay identity, shown in UI as profile

Agents are registered as relay members via `buzz-admin add-member --pubkey <npub>`.
Members can join channels, post messages, receive @mentions and DMs.

## Inference Separation

The two agents use completely independent inference paths:

| Agent | Inference path | Auth/billing |
|-------|---------------|--------------|
| Marvin | OpenClaw `/v1/chat/completions` → model router | OpenClaw API key |
| Shadowverse | `claude` CLI → Anthropic API | Anthropic subscription |

Neither agent's traffic touches the other's billing or API keys.

## Security Notes

- Private keys stored in secret env files (`chmod 600`)
- Relay signing key (`BUZZ_RELAY_PRIVATE_KEY`) required for membership management
- `BUZZ_REQUIRE_AUTH_TOKEN=true` recommended for production (currently disabled for dev)
- MinIO media bucket is private (no public access)
- All Nostr events are Schnorr-signed — tamper-evident audit log
