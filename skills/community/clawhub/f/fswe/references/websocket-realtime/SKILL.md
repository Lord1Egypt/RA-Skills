# WebSocket & Realtime

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| language | string | en | en, id |
| depth | string | standard | quick, standard, deep |
| transport | string | websocket | websocket, sse, polling |

## Checklist

### WebSocket
- [ ] Authenticate on connect (token in query or first message)
- [ ] Implement heartbeat/ping-pong (30s interval)
- [ ] Handle reconnection with exponential backoff
- [ ] Use channels/rooms for pub/sub
- [ ] Validate all incoming messages (JSON schema)
- [ ] Set max message size limit
- [ ] Track connection count per user
- [ ] Graceful shutdown — close connections on server stop

### Server-Sent Events (SSE)
- [ ] Use for server → client only (no client push needed)
- [ ] Set `Content-Type: text/event-stream`
- [ ] Send `心跳` every 30s to keep connection alive
- [ ] Handle `Last-Event-ID` for reconnection
- [ ] Implement retry logic with `retry:` field

### Pub/Sub Pattern
```typescript
// Channel-based pub/sub
class EventBus {
  private channels = new Map<string, Set<Function>>();

  subscribe(channel: string, handler: Function) {
    if (!this.channels.has(channel)) {
      this.channels.set(channel, new Set());
    }
    this.channels.get(channel)!.add(handler);
    return () => this.channels.get(channel)?.delete(handler);
  }

  publish(channel: string, data: unknown) {
    this.channels.get(channel)?.forEach(handler => handler(data));
  }
}
```

### Connection Management
- [ ] Limit concurrent connections per user
- [ ] Clean up on disconnect (remove from rooms, clear timers)
- [ ] Store connection metadata (userId, rooms, connectedAt)
- [ ] Handle unexpected disconnections gracefully
- [ ] Implement connection pooling for high-traffic

### Security
- [ ] Authenticate every connection
- [ ] Authorize channel/room joins
- [ ] Rate limit messages per connection
- [ ] Validate message format before processing
- [ ] Sanitize broadcast data (no PII leaks)

## When to Use What

| Use Case | Transport | Why |
|----------|-----------|-----|
| Chat/messaging | WebSocket | Bidirectional, low latency |
| Live notifications | SSE | Simple, auto-reconnect |
| Real-time dashboard | WebSocket | Multiple data streams |
| Event feed | SSE | Server-push, replay support |
| Collaborative editing | WebSocket | Conflict resolution needed |
| Progress updates | SSE | One-way, simple |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| No heartbeat | Add ping/pong every 30s |
| No auth on connect | Verify token before accepting |
| Broadcast to all | Use channels/rooms |
| No message validation | Schema-validate all input |
| Memory leaks on disconnect | Always clean up handlers |
