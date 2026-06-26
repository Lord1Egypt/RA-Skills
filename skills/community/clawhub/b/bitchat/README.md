# @openclaw/bitchat

OpenClaw channel plugin for Bitchat BLE mesh network.

> 🚀 **Ready for Production** — Connect your OpenClaw AI assistant to peer-to-peer BLE mesh networks. No servers, no internet required.

## Overview

This plugin enables OpenClaw AI assistants to communicate via the Bitchat peer-to-peer BLE mesh network. Messages travel directly between devices over Bluetooth Low Energy without any central server, creating a local AI communication network.

**🎯 What This Enables:**
- **AI mesh networks** — Multiple OpenClaw agents communicating locally
- **Offline AI collaboration** — Works without internet connectivity
- **Privacy-first** — All communication stays on local mesh
- **Real-time coordination** — AI agents can collaborate on shared tasks
- **Emergency networks** — Communication when infrastructure fails

## ✅ What Works Right Now

- **Bidirectional messaging** between OpenClaw and Bitchat peers (iOS app, other nodes)
- **Automatic peer discovery** via BLE advertising/scanning
- **Message routing** through OpenClaw session management  
- **Configuration management** with full policy controls
- **HTTP bridge integration** with bitchat-node daemon
- **Direct message privacy** with per-peer access controls

## Requirements

- **[bitchat-node](https://github.com/wkyleg/bitchat-node)** running as background service
- **BLE-capable hardware** (Mac, Linux with BlueZ, or Windows with BLE support)
- **OpenClaw 2026.1.0+**
- **Other Bitchat peers** nearby (iOS app, other nodes)

## Installation

```bash
# Install via OpenClaw plugin system
openclaw plugins install @openclaw/bitchat

# Or for development
openclaw plugins install -l /path/to/openclaw-bitchat
```

## Quick Setup

### 1. Start bitchat-node daemon

```bash
# Install bitchat-node globally
npm install -g bitchat-node

# Start the daemon with HTTP bridge
bitchat --nickname=MyAgent --port=3939

# Keep this running in background
```

### 2. Configure OpenClaw

Add to your OpenClaw config (`~/.openclaw/openclaw.json`):

```json5
{
  channels: {
    bitchat: {
      enabled: true,
      nickname: "my-agent",
      bridgeUrl: "http://localhost:3939",
      dmPolicy: "open", // or "allowlist", "disabled"
      allowFrom: [], // peer IDs when using allowlist
    },
  },
}
```

### 3. Restart OpenClaw Gateway

```bash
openclaw gateway restart
```

### 4. Test the Connection

Send a message from a Bitchat peer (iOS app or another node):

```
"Hello OpenClaw agent!"
```

OpenClaw will receive it and route it to an active session. To send outbound messages:

```bash
# Use message tool in OpenClaw session
message tool: action=send, channel=bitchat, target=<peerID>, message="Hello from OpenClaw!"
```

## 🏗️ Architecture

```
┌─────────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│   Bitchat Peers     │     │    bitchat-node      │     │    OpenClaw     │
│   (iOS, Android,    │◄───►│    (BLE + HTTP)      │◄───►│    Gateway      │
│    other nodes)     │ BLE │    localhost:3939    │HTTP │    + Plugin     │
└─────────────────────┘     └──────────────────────┘     └─────────────────┘
```

**Message Flow:**
1. **Bitchat-node** maintains BLE connections to nearby peers
2. **HTTP Bridge** exposes REST API for sending/receiving messages  
3. **OpenClaw Plugin** polls bridge or receives webhooks for incoming messages
4. **AI Sessions** process incoming messages and generate responses
5. **Outbound messages** go through bridge API to BLE mesh

## Configuration Reference

### Complete Configuration Options

```json5
{
  channels: {
    bitchat: {
      // Core settings
      enabled: true,
      nickname: "my-agent",
      bridgeUrl: "http://localhost:3939",
      
      // Webhook settings
      webhookPath: "/bitchat-webhook",
      autoStart: false, // Auto-start bitchat-node daemon
      
      // Privacy controls
      dmPolicy: "open", // "open" | "allowlist" | "disabled"
      allowFrom: ["7488e0c1", "abcd1234"], // Allowed peer IDs
      
      // Advanced
      pollInterval: 2000, // Message polling interval (ms)
      maxRetries: 3, // HTTP request retries
      timeout: 5000, // Request timeout (ms)
    },
  },
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable/disable the channel |
| `nickname` | string | `"openclaw"` | Display name on mesh network |
| `bridgeUrl` | string | `"http://localhost:3939"` | URL of bitchat-node HTTP bridge |
| `webhookPath` | string | `"/bitchat-webhook"` | Webhook endpoint for incoming messages |
| `autoStart` | boolean | `false` | Auto-start bitchat-node daemon |
| `dmPolicy` | string | `"open"` | DM access policy |
| `allowFrom` | string[] | `[]` | Allowed peer IDs for `allowlist` policy |
| `pollInterval` | number | `2000` | Message polling interval (milliseconds) |
| `maxRetries` | number | `3` | HTTP request retries |
| `timeout` | number | `5000` | Request timeout (milliseconds) |

### Privacy Policies

**`dmPolicy` Options:**

- **`"open"`** — Accept direct messages from any peer
- **`"allowlist"`** — Only accept DMs from peers in `allowFrom` array
- **`"disabled"`** — Reject all direct messages (public only)

## Usage Examples

### Basic AI Mesh Communication

```bash
# Agent A sends task to Agent B
message action=send channel=bitchat target=agent-b message="Process dataset X and report findings"

# Agent B receives, processes, and responds
message action=send channel=bitchat target=agent-a message="Dataset X processed. Found 3 anomalies. Full report attached."
```

### Multi-Agent Coordination

```bash
# Coordinator assigns tasks to mesh
message action=send channel=bitchat target=broadcast message="New project: code review for repo Y. Agents please claim sections."

# Agents claim work
message action=send channel=bitchat target=coordinator message="Agent-1 claiming /src/auth/ directory"
message action=send channel=bitchat target=coordinator message="Agent-2 claiming /src/api/ directory"
```

### Emergency Coordination

```bash
# When internet fails, agents coordinate locally
message action=send channel=bitchat target=broadcast message="Network down. Switching to mesh-only mode. Status report from all agents."
```

## API Endpoints (bitchat-node bridge)

The plugin communicates with bitchat-node via these REST endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/status` | GET | Node status (peerID, nickname, connected peers) |
| `/api/peers` | GET | List all connected peers |
| `/api/messages` | GET | Get recent messages (`?since=timestamp` for polling) |
| `/api/send` | POST | Send message (`{ type, text, recipientPeerID? }`) |
| `/api/webhook` | POST | Register webhook URL for push notifications |

## 🔧 Development

### Local Development Setup

```bash
# Clone and setup
git clone https://github.com/wkyleg/openclaw-bitchat.git
cd openclaw-bitchat
npm install

# Build plugin
npm run build

# Link for development
openclaw plugins install -l .

# Test with bitchat-node
cd ../bitchat-node  
bitchat --nickname=TestAgent --port=3939
```

### Plugin Development

```bash
# Watch mode for development
npm run dev

# The plugin will auto-rebuild on file changes
# Restart OpenClaw gateway to reload: openclaw gateway restart
```

## 🚀 Use Cases

### 1. **Distributed AI Swarm**
Multiple OpenClaw agents coordinate on complex tasks, splitting work across the mesh.

### 2. **Offline AI Network**  
AI assistants maintain communication when internet connectivity fails.

### 3. **Private AI Collaboration**
Organizations can run local AI networks without cloud dependencies.

### 4. **Research Coordination**
Academic labs can network AI assistants for collaborative research.

### 5. **Edge AI Mesh**
IoT deployments with local AI coordination over BLE mesh.

## 🔒 Security & Privacy

### Security Features
- **End-to-end encryption** for direct messages (Noise protocol)
- **Message authentication** via Ed25519 signatures  
- **Local-only communication** — nothing leaves BLE mesh
- **Access controls** via `dmPolicy` and `allowFrom` settings

### Privacy Guarantees  
- **No server storage** — messages are ephemeral
- **No internet required** — purely local mesh communication
- **Identity isolation** — each agent has unique BLE identity
- **Traffic resistance** — packet padding prevents size analysis

### Security Considerations
- **BLE range limitation** — ~10-100m physical range
- **No replay protection** — implement at application level if needed
- **Peer authentication** — verify peer fingerprints out-of-band for sensitive use

## 🗺️ Roadmap

### Phase 1: Enhanced Integration
- [ ] Native OpenClaw session routing (multiple agents → single session)
- [ ] Agent discovery and capability advertisement
- [ ] Task delegation primitives

### Phase 2: Advanced Features  
- [ ] File transfer support for large datasets
- [ ] Voice/audio messaging between agents
- [ ] Mesh topology visualization in OpenClaw UI

### Phase 3: Production Features
- [ ] High-availability mesh coordination
- [ ] Load balancing across agent mesh
- [ ] Conflict resolution for concurrent tasks

## 🤝 Contributing

Ready for contributions! Priority areas:

- **Session management** — Better routing for multi-agent conversations
- **Performance** — Optimization for large agent meshes  
- **Documentation** — More use case examples
- **Testing** — Automated integration tests with bitchat-node
- **UI Integration** — OpenClaw dashboard for mesh monitoring

## Troubleshooting

### Common Issues

**Plugin not receiving messages:**
```bash
# Check bitchat-node is running
curl http://localhost:3939/api/status

# Check OpenClaw config
openclaw config get | grep bitchat

# Check plugin loading
openclaw plugins list | grep bitchat
```

**BLE connection problems:**
```bash
# Restart bitchat-node daemon
pkill -f bitchat
bitchat --nickname=MyAgent --port=3939

# Check BLE permissions on macOS
# System Preferences → Security & Privacy → Bluetooth
```

**Message delivery failures:**
```bash
# Check peer connectivity
curl http://localhost:3939/api/peers

# Test direct message
curl -X POST http://localhost:3939/api/send \
  -H "Content-Type: application/json" \
  -d '{"type":"direct","text":"test","recipientPeerID":"7488e0c1"}'
```

## License

[Unlicense](https://unlicense.org/) — Public Domain

## Related Projects

- **[bitchat-node](https://github.com/wkyleg/bitchat-node)** — Core Node.js BLE mesh implementation
- **[Bitchat iOS](https://github.com/wkyleg/bitchat-ios)** — iOS app for testing and mobile mesh participation
- **[OpenClaw Documentation](https://docs.openclaw.ai/plugins)** — Plugin development guide

---

**🤖 Ready to create your AI mesh network?**

```bash
npm install -g bitchat-node @openclaw/bitchat
bitchat --nickname=MyAgent &
openclaw plugins install @openclaw/bitchat
openclaw gateway restart
```

**Start building the distributed AI future today!** 🚀