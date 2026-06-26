---
name: supercraft-game-servers
description: Order, configure and manage dedicated game servers (20+ games) via Supercraft REST API
homepage: https://claws.supercraft.host
license: MIT
user-invocable: true
---

You can manage dedicated game servers through the Supercraft Agentic API. This is a REST API — no additional binaries or MCP servers are needed, just HTTP requests with a Bearer JWT token.

## API Base

```
https://claws.supercraft.host
```

## Authentication

All `/servers/*` endpoints require a Bearer JWT token in the `Authorization` header.

To get a token, use the login-link flow:

1. `POST /auth/login-link` with `{"email": "user@example.com"}` — sends a magic link email
2. User clicks the link, which contains a magic token
3. `GET /auth/claim?magic=<token>` — poll this until it returns a JWT

```bash
# After obtaining the JWT:
curl -H "Authorization: Bearer <JWT>" https://claws.supercraft.host/servers
```

## Available Endpoints

### Server Management (requires auth)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/servers` | List all user's servers with status |
| GET | `/servers/{id}` | Detailed server info with live status |
| POST | `/servers/{id}/start` | Start the server |
| POST | `/servers/{id}/stop` | Stop the server |
| POST | `/servers/{id}/restart` | Restart the server |
| GET | `/servers/{id}/config` | Get current server configuration |
| PUT | `/servers/{id}/config` | Update server configuration |
| GET | `/servers/{id}/config/schema` | Get config field definitions (types, ranges) |
| GET | `/servers/{id}/connection` | Get connection details (IP, port, password) |
| POST | `/servers/{id}/console` | Send RCON/console command |
| GET | `/servers/{id}/logs` | Get recent server log lines |

### Catalog (no auth needed)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/catalog/games` | List all available games |
| GET | `/catalog/games/{code}` | Game details with plans and pricing |
| GET | `/catalog/regions` | Available server regions |

### Purchasing (no auth needed)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/orders/purchase` | Purchase a new server plan (returns checkout URL) |

## Purchase & Login Flow — CRITICAL

When generating a `checkout_url` (via `POST /orders/purchase`) or `login_url` (via `POST /auth/login-link`), you **MUST send the link to the user as a message BEFORE calling any tools** (curl, exec, cron). If you call a tool first, the message with the link gets blocked and the user never sees it.

Correct sequence:
1. **Reply to the user** with the `checkout_url` or `login_url`
2. **After the reply**, set up a cron (every 30s) to poll `GET /auth/claim?magic=...`
3. When claim returns `status: "ready"`, save the JWT token securely

Do NOT use `while`/`sleep` loops — use a cron job or poll on the user's next message.

## Supported Games

ARK: Survival Ascended, Counter-Strike 2, Enshrouded, Factorio, HumanitZ, Hytale, Necesse, Palworld, Project Zomboid, Rust, Satisfactory, Sons of the Forest, Terraria, Unturned, V Rising, Valheim, and Vintage Story.

## Example Usage

When the user asks about their game server, follow this pattern:

1. List servers (`GET /servers`) to find the right deployment
2. Check status (`GET /servers/{id}`) before taking action
3. Confirm destructive operations (restart, config changes) before executing

**Check server status:**
```bash
curl -H "Authorization: Bearer $TOKEN" https://claws.supercraft.host/servers
```

**Start a server:**
```bash
curl -X POST -H "Authorization: Bearer $TOKEN" https://claws.supercraft.host/servers/42/start
```

**Update config:**
```bash
curl -X PUT -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"max_players": 20}' \
  https://claws.supercraft.host/servers/42/config
```

**Send console command:**
```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"command": "say Hello everyone!"}' \
  https://claws.supercraft.host/servers/42/console
```

**Browse available games:**
```bash
curl https://claws.supercraft.host/catalog/games
```

## Documentation

- [Getting Started Guide](https://claws.supercraft.host/documentation-for-agents/getting-started.md)
- [OpenAPI Reference](https://claws.supercraft.host/docs)
- [Machine-readable discovery](https://supercraft.host/llms.txt)
- Per-game API guides: `https://claws.supercraft.host/{game-slug}-server-api`
