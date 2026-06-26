# Configuration Reference

> This is a quick reference covering the most common settings. For the full configuration reference (including logging, NODE_ENV defaults, and advanced tuning), see [docs/configuration.md](../../../configuration.md).

All variables use the `CLAW_INSIGHTS_` prefix. For backward compatibility, `OPENCLAW_` prefix is also accepted (lower priority).

## Core

| Variable                    | Default            | Description                                                                      |
| --------------------------- | ------------------ | -------------------------------------------------------------------------------- |
| `CLAW_INSIGHTS_SERVER_PORT` | `41041`            | GraphQL API + web server port                                                    |
| `CLAW_INSIGHTS_WEB_PORT`    | `41042`            | Vite dev server port (development only)                                          |
| `CLAW_INSIGHTS_API_TOKEN`   | _(auto-generated)_ | Fixed Bearer token (minimum 32 characters). Empty = auto-generate on fresh start |
| `CLAW_INSIGHTS_NO_AUTH`     | `false`            | Disable authentication entirely (`true` or `1`)                                  |
| `CLAW_INSIGHTS_SERVER_ONLY` | `false`            | Run API server without serving web UI                                            |

## Session Rotation

| Variable                                         | Default    | Description                              |
| ------------------------------------------------ | ---------- | ---------------------------------------- |
| `CLAW_INSIGHTS_TOKEN_ROTATION_ENABLED`           | `true`     | Enable rotating session-cookie key-ring  |
| `CLAW_INSIGHTS_TOKEN_ROTATION_INTERVAL_MS`       | `86400000` | Rotation interval (24h)                  |
| `CLAW_INSIGHTS_TOKEN_GRACE_MS`                   | `43200000` | Previous-key grace window (12h)          |
| `CLAW_INSIGHTS_TOKEN_ROTATION_CHECK_INTERVAL_MS` | `300000`   | Background rotation check cadence (5min) |
| `CLAW_INSIGHTS_TOKEN_MAX_PREVIOUS`               | `2`        | Max retained previous keys in key-ring   |

## Data Sources

| Variable                      | Default                                          | Description                   |
| ----------------------------- | ------------------------------------------------ | ----------------------------- |
| `CLAW_INSIGHTS_DB`            | `~/.claw-insights/metrics.db`                    | SQLite database path          |
| `CLAW_INSIGHTS_SESSIONS_PATH` | `~/.openclaw/agents/main/sessions/sessions.json` | OpenClaw sessions file        |
| `CLAW_INSIGHTS_LOG_DIR`       | `/tmp/openclaw/`                                 | OpenClaw log directory        |
| `CLAW_INSIGHTS_CRON_PATH`     | `~/.openclaw/cron/jobs.json`                     | OpenClaw cron jobs file       |
| `CLAW_INSIGHTS_DIR`           | `~/.openclaw`                                    | OpenClaw base directory       |
| `CLAW_INSIGHTS_CLI`           | _(auto-detected)_                                | Path to `openclaw` CLI binary |

## Data Retention

| Variable                           | Default     | Description                                                |
| ---------------------------------- | ----------- | ---------------------------------------------------------- |
| `CLAW_INSIGHTS_RAW_RETENTION_DAYS` | `7`         | Days to keep raw metric data                               |
| `CLAW_INSIGHTS_HOURLY_RETENTION`   | `permanent` | Hourly aggregate retention (`permanent` or number of days) |

## Config File

Path: `~/.claw-insights/config.json`

Supports a subset of configuration keys in camelCase (without the `CLAW_INSIGHTS_` prefix). Environment variables take precedence over config file values. Unknown keys are logged as warnings and ignored.

Supported keys: `serverPort`, `webPort`, `apiToken`, `noAuth`, `dbPath`, `logLevel`, `serverOnly`, `tokenRotationEnabled`, `tokenRotationIntervalMs`, `tokenGraceMs`, `tokenMaxPrevious`, `rawRetentionDays`, `hourlyRetention`, `transcriptsDir`, `deviceJsonPath`, `sessionHierarchyMode`, and logging/pressure-related keys. See `knownKeys` in `config.ts` for the complete list.

Example:

```json
{
  "serverPort": 41041,
  "noAuth": false,
  "rawRetentionDays": 7
}
```
