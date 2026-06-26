---
name: "bitchat"
description: "Bitchat integration skill for OpenClaw"
version: "0.1.2"
tags: ["beta"]
user-invocable: false
---

# Bitchat

This skill enables decentralized messaging using the Bitchat protocol within OpenClaw.

## Features
- Send and receive messages over mesh or peer-to-peer Bitchat networks.
- Node-based integration for scriptable console usage.
- CLI commands to configure network peers, encryption, and channels.
- Relies on `bitchat-node` (npm) for the underlying BLE or other mesh transport.

## Security & Dependencies
- Bitchat uses local BLE or LAN for discovery and connectivity.
- The skill does not automatically connect to arbitrary external URLs.
- All network connections are user-initiated and require local config.
- We have pruned unneeded dependencies. Only `bitchat-node` is included.

## Usage
1. Install the skill from ClawHub: `clawhub install bitchat`
2. Add or configure your Bitchat node/peers.
3. Use OpenClaw commands to dispatch or read messages.

```bash
# example
openclaw bitchat start
openclaw bitchat send --to=peerID --message="Hello"
```

## Implementation Details
- TypeScript-based, compiles to dist/.
- Exposes integration points so OpenClaw can manage channels.
- Minimizes third-party dependencies to reduce security surface area.

## Future Plans
- Enhanced encryption and key management.
- Multi-network bridging beyond BLE.

## Release Notes
- **0.1.2**: Points to bitchat-node@0.1.2, further pruned dist dependencies, updated skill doc.
