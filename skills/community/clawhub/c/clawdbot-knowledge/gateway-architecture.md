# Gateway Architecture Reference

## Overview

The Gateway is the central nervous system of CLAWD, controlling all messaging platforms through a single, persistent daemon. This document provides comprehensive details about Gateway architecture, protocols, and management.

## Core Architecture

### Single Gateway Principle
- **One Gateway per Host**: Controls a single Baileys session
- **Central Control**: All messaging platforms managed through one daemon
- **WebSocket API**: Typed API for all client communication
- **Port Configuration**: Default WebSocket bind host 127.0.0.1:18789, Canvas host default 18793

### Component Breakdown

#### Gateway Daemon
**Purpose**: Maintains provider connections and provides typed WS API

**Responsibilities:**
- Connection management to messaging providers
- WebSocket API endpoint serving
- Request validation using JSON schema
- Event generation (agent, chat, presence, health, heartbeat, cron)
- Authentication and authorization

**Protocol Flow:**
```
Client Gateway
| |
|---- req:connect -------->|
|<------ res (ok) ---------| (or res error + close)
| (payload=hello-ok carries snapshot: presence + health)
| |
|<------ event:presence ---|
|<------ event:tick -------|
| |
|------- req:agent ------->|
|<------ res:agent --------| (ack: {runId,status:"accepted"})
|<------ event:agent ------| (streaming)
|<------ res:agent --------| (final: {runId,status,summary})
| |
```

#### Clients (Mac App / CLI / Web-Admin)
**Purpose**: User interfaces for Gateway interaction

**Characteristics:**
- One WS connection per client
- Send requests: health, status, send, agent, system-presence
- Subscribe to events: tick, agent, presence, shutdown
- Can be local or remote (via SSH/Tailscale tunnel)

**Request Format:**
```json
{
  "type": "req",
  "id": "unique-request-id",
  "method": "agent|health|status|send|system-presence",
  "params": { /* method-specific parameters */ }
}
```

**Response Format:**
```json
{
  "type": "res", 
  "id": "matching-request-id",
  "ok": true|false,
  "payload": { /* response data */ }|{ /* error details */ }
}
```

#### Nodes (macOS / iOS / Android / Headless)
**Purpose**: Specialized clients with device-specific capabilities

**Requirements:**
- Must connect with `role: node`
- Must provide device identity at connect
- Pairing is device-based (role node) with approval in device pairing storage
- Must expose commands like canvas.*, camera.*, screen.record, location.get

**Capabilities Declaration:**
```json
{
  "type": "req",
  "id": "connect",
  "method": "connect",
  "params": {
    "role": "node",
    "deviceId": "unique-device-identifier",
    "capabilities": ["camera.*", "screen.record", "location.get"],
    "auth": {
      "token": "device-token-if-paired"
    }
  }
}
```

#### WebChat
**Purpose**: Static user interface using Gateway WS API

**Features:**
- Uses same Gateway WS API for chat history and messages
- For remote setups, connects via same SSH/Tailscale tunnel as other clients
- Real-time message updates
- File attachment support

## Wire Protocol Specification

### Transport
- **Protocol**: WebSocket
- **Frame Type**: Text frames with JSON payloads
- **First Frame**: Must be `connect` type
- **Authentication**: If OPENCLAW_GATEWAY_TOKEN (or --token) is set, connect.params.auth.token must match

### Frame Types

#### Connect Frame (Required First)
```json
{
  "type": "connect",
  "id": "connect-1",
  "method": "connect",
  "params": {
    "role": "client|node",
    "deviceId": "device-identifier",
    "capabilities": ["capability1", "capability2"],
    "auth": {
      "token": "authentication-token",
      "challenge": "signed-challenge-for-remote"
    }
  }
}
```

#### Request Frame
```json
{
  "type": "req",
  "id": "unique-request-id",
  "method": "method-name",
  "params": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

#### Response Frame
```json
{
  "type": "res",
  "id": "matching-request-id",
  "ok": true,
  "payload": {
    "data": "response-data"
  }
}
```

#### Event Frame
```json
{
  "type": "event",
  "event": "event-name",
  "payload": {
    "event-data": "event-payload"
  },
  "seq": 42,
  "stateVersion": 1
}
```

## Authentication & Security

### Device Identity
- **All WS Clients**: Must include device identity at connect
- **New Device IDs**: Require pairing approval
- **Device Token**: Gateway issues device token for subsequent connections after pairing
- **Local Connections**: Can be auto-approved to ensure smooth user experience on same host
- **Remote Connections**: Must sign connect.challenge and require explicit approval

### Gateway Authentication
- Applies to all connections, both local and remote
- Token-based authentication
- Challenge-response for remote connections
- Session management and timeout

### Idempotency
- **Methods with Side Effects**: Require idempotency keys for safe retry
- **Server**: Maintains short-lived deduplication cache
- **Purpose**: Prevents duplicate operations on network issues

## Connection Lifecycle

### 1. Handshake
```
Client → Gateway: Connect frame
Gateway → Client: Response (success/error + close)
```

### 2. Session Establishment
```
Client → Gateway: Request frames
Gateway → Client: Response frames
Gateway → Client: Event streams
```

### 3. Event Subscription
```
Client → Gateway: Subscribe to events (tick, agent, presence, shutdown)
Gateway → Client: Continuous event stream
```

### 4. Graceful Shutdown
```
Client → Gateway: Close frame or disconnect
Gateway → Client: Final events, connection close
```

## Error Handling

### Connection Errors
- **Invalid First Frame**: Hard connection abort (must be JSON connect type)
- **Authentication Failure**: Connection close with error response
- **Device Not Paired**: Connection close with pairing required response

### Request Errors
- **Invalid Method**: Error response with method not found
- **Invalid Parameters**: Error response with validation details
- **Authentication Expired**: Error response requiring re-authentication

### System Errors
- **Gateway Overload**: Error response with retry suggestion
- **Provider Connection Lost**: Event notification with reconnect guidance
- **Configuration Error**: Error response with configuration details

## Monitoring & Health

### Health Check
```json
{
  "type": "req",
  "id": "health-1", 
  "method": "health",
  "params": {}
}
```

**Response:**
```json
{
  "type": "res",
  "id": "health-1",
  "ok": true,
  "payload": {
    "status": "healthy",
    "uptime": 86400,
    "connections": {
      "whatsapp": "connected",
      "telegram": "connected", 
      "discord": "disconnected"
    },
    "performance": {
      "cpu": "15%",
      "memory": "45%",
      "sessions": 3
    }
  }
}
```

### Events for Monitoring
- **presence**: System and user presence changes
- **health**: System health status updates
- **agent**: Agent execution lifecycle events
- **tick**: Regular heartbeat events
- **shutdown**: System shutdown notifications

## Remote Access

### Tailscale (Preferred)
```bash
# Connect to remote Gateway via Tailscale
tailscale up
# Gateway accessible via Tailscale IP
```

### SSH Tunnel
```bash
# Create SSH tunnel to remote Gateway
ssh -N -L 18789:127.0.0.1:18789 user@host
# Connect to local 127.0.0.1:18789 (proxies to remote)
```

### TLS Configuration
- TLS + optional pinning for WS in remote setups
- Certificate management and rotation
- Secure connection establishment

## Configuration

### Gateway Configuration (openclaw.json)
```json
{
  "gateway": {
    "bindHost": "127.0.0.1",
    "port": 18789,
    "canvasHost": "127.0.0.1",
    "canvasPort": 18793,
    "auth": {
      "token": "gateway-auth-token",
      "challengeRequired": true
    }
  }
}
```

### Environment Variables
- `OPENCLAW_GATEWAY_TOKEN`: Gateway authentication token
- `OPENCLAW_BIND_HOST`: Gateway bind host override
- `OPENCLAW_PORT`: Gateway port override
- `OPENCLAW_CANVAS_PORT`: Canvas host port override

## Deployment

### Systemd Service
```ini
[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
User=openclaw
ExecStart=/usr/local/bin/openclaw gateway
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Launchd (macOS)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.gateway</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/openclaw</string>
        <string>gateway</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim
RUN pip install openclaw
EXPOSE 18789 18793
CMD ["openclaw", "gateway"]
```

## Troubleshooting

### Common Issues

#### Connection Refused
- **Cause**: Gateway not running
- **Solution**: Start Gateway service
- **Check**: `systemctl status openclaw-gateway`

#### Authentication Failed
- **Cause**: Invalid token or device not paired
- **Solution**: Check token, pair device
- **Check**: Gateway logs for auth details

#### WebSocket Timeout
- **Cause**: Network issues or Gateway overload
- **Solution**: Check network, restart Gateway
- **Check**: System resources, connection limits

### Debug Commands
```bash
# Check Gateway status
openclaw gateway status

# Start Gateway in foreground for debugging
openclaw gateway --verbose

# Check configuration
openclaw doctor

# View logs
journalctl -u openclaw-gateway -f
```