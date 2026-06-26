# Carbium Endpoints, Authentication & Pricing

## Endpoints

| Product | URL | Protocol |
|---|---|---|
| RPC | `https://rpc.carbium.io/?apiKey=KEY` | JSON-RPC 2.0 over HTTPS |
| Standard WebSocket | `wss://wss-rpc.carbium.io/?apiKey=KEY` | JSON-RPC 2.0 over WebSocket |
| gRPC (WebSocket) | `wss://grpc.carbium.io/?apiKey=KEY` | JSON-RPC 2.0 over WebSocket |
| gRPC (HTTP/2) | `https://grpc.carbium.io` | Yellowstone protobuf (header: `x-token: KEY`) |
| Swap API | `https://api.carbium.io/api/v2` | REST (header: `X-API-KEY: KEY`) |
| DEX App | `https://app.carbium.io` | Web UI |
| Docs | `https://docs.carbium.io` | Web |

## API Keys

### Two Separate Keys

| Key | Signup | Covers |
|---|---|---|
| RPC Key | [rpc.carbium.io/signup](https://rpc.carbium.io/signup) | RPC + Standard WebSocket + gRPC |
| Swap API Key | [api.carbium.io/login](https://api.carbium.io/login) | All `/api/v1/*` and `/api/v2/*` endpoints |

Programmatic key provisioning is not yet available. Keys are created via dashboards (free to start).

### Authentication Methods

**RPC / WebSocket / gRPC:**

| Method | Format |
|---|---|
| Query parameter (recommended) | `?apiKey=YOUR_RPC_KEY` |
| Header | `X-API-KEY: YOUR_RPC_KEY` |
| gRPC HTTP/2 header | `x-token: YOUR_RPC_KEY` |

**Swap API:**

| Method | Format |
|---|---|
| Header (required) | `X-API-KEY: YOUR_API_KEY` |

### Environment Variables

```bash
export CARBIUM_RPC_KEY="your-rpc-key"
export CARBIUM_API_KEY="your-swap-api-key"
```

### Security Rules

- Never embed keys in frontend/client-side code
- Never commit keys to version control
- Use environment variables only
- Rotate immediately if exposed
- Keep server-side only
- Restrict endpoints by domain/IP in the RPC dashboard

## Pricing Tiers

| Tier | Price | Credits/mo | Max RPS | gRPC | WebSocket |
|---|---|---|---|---|---|
| Free | $0 | 500K | 10 | No | Yes |
| Developer | $32/mo | 10M | 50 | No | Yes |
| Business | $320/mo | 100M | 200 | Yes | Yes |
| Professional | $640/mo | 200M | 500 | Yes | Yes |
| Enterprise | Custom | Custom | Custom | Yes | Yes |

### Rate Limiting

- **Short-term limit:** Requests per second (RPS) — varies by tier
- **Long-term limit:** Monthly credit allocation
- HTTP 429 signals rate limit exceeded — back off immediately
- Separate dev/staging/prod keys to isolate traffic

### Dashboard

- **RPC Dashboard:** [rpc.carbium.io](https://rpc.carbium.io) — usage monitoring, credit tracking, endpoint restrictions
- **Swap API Dashboard:** [api.carbium.io](https://api.carbium.io) — key management
