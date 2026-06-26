# Configuration Reference

Config file: `config.yaml` in the installation directory.

Copy from `config.example.yaml` to create your config.

## Full Config Example

```yaml
server:
  host: "127.0.0.1"     # Listen address
  port: 9090             # Listen port

session:
  ttl: 1800              # Session TTL in seconds (default: 30 min)

concurrency:
  max: 5                 # Max concurrent CLI processes
  maxQueued: 50          # Queue limit; excess returns 429

timeout: 300000          # CLI process timeout in milliseconds (default: 5 min)

defaultModel: "gemini"   # Default model when request omits model field

cli:
  gemini: ""             # Path to gemini binary (empty = use PATH)
  claude: ""             # Path to claude binary (empty = use PATH)

models:
  gemini:
    provider: "gemini"
    model: "gemini-2.5-flash"
  gemini-pro:
    provider: "gemini"
    model: "gemini-2.5-pro"
  claude:
    provider: "claude"
    model: "sonnet"
  claude-opus:
    provider: "claude"
    model: "opus"
```

## Environment Variable Overrides

| Variable | Overrides | Example |
|----------|-----------|---------|
| `CLI_AI_HOST` | `server.host` | `127.0.0.1` (default; do not change without a reverse proxy) |
| `CLI_AI_PORT` | `server.port` | `8080` |
| `GEMINI_CLI_PATH` | `cli.gemini` | `/usr/local/bin/gemini` |
| `CLAUDE_CLI_PATH` | `cli.claude` | `/usr/local/bin/claude` |

## Config Fields

### server

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `host` | string | `"127.0.0.1"` | Bind address. **Keep at `127.0.0.1`.** The proxy has no authentication, so binding to `0.0.0.0` exposes it to any host that can reach your machine. Only change this behind a reverse proxy that enforces auth. |
| `port` | number | `9090` | TCP port to listen on. |

### session

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `ttl` | number | `1800` | Session idle timeout in seconds. Expired sessions are cleaned up automatically. |

### concurrency

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `max` | number | `5` | Maximum number of CLI processes that can run simultaneously. |
| `maxQueued` | number | `50` | Maximum requests waiting in queue. Excess requests get HTTP 429. |

### timeout

| Type | Default | Description |
|------|---------|-------------|
| number | `300000` | Per-request CLI process timeout in milliseconds. Timed-out processes are killed and return HTTP 504. |

### defaultModel

| Type | Default | Description |
|------|---------|-------------|
| string | `"gemini"` | Model used when the request omits the `model` field. Must match a key in `models`. |

### cli

Maps provider names to CLI binary paths. Leave empty to use the system PATH.

### models

Maps model aliases to provider configurations.

Each entry:
```yaml
model-alias:
  provider: "gemini"  # or "claude"
  model: "model-name" # passed to CLI --model flag
```

You can add custom aliases:
```yaml
models:
  fast:
    provider: "gemini"
    model: "gemini-2.5-flash"
  smart:
    provider: "claude"
    model: "opus"
  gpt-4:
    provider: "claude"
    model: "opus"
```
