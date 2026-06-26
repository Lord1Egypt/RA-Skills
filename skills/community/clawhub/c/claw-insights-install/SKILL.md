---
name: claw-insights-install
description: 'Install and run Claw Insights, a read-only observability dashboard that monitors your OpenClaw agent with zero intrusion — no code changes, no cloud dependency, data never leaves your machine. Full session transcript replay, per-turn token and tool tracking, and shareable PNG/SVG status cards. One command to install, auto-discovers your running gateway, lightweight SQLite storage. Use when setting up claw-insights for the first time, upgrading versions, configuring auth or port, managing the service, or troubleshooting startup failures.'
---

# Install Claw Insights

**Announce at start:** "I'm setting up Claw Insights — a read-only observability dashboard for your OpenClaw agent."

## What is Claw Insights?

A read-only observability dashboard for OpenClaw agents. One command installs it, auto-connects to your running gateway — no configuration needed.

- **Zero intrusion** — pure sidecar that reads logs and CLI output only; no code changes, no cloud calls, data stays on your machine
- **Full session replay** — complete transcript timeline with role separation, tool calls, and per-turn token tracking
- **Shareable snapshots** — generate PNG/SVG status cards with themes, languages, and detail levels via REST API

Runs locally with SQLite. Requires Node.js ≥ 22.5 and a running OpenClaw gateway.

## Install

```bash
# One-line install (recommended)
curl -fsSL https://claw-insights.com/install.sh | sh

# Or via npm
npm install -g claw-insights
```

## Run

```bash
claw-insights start             # Default port 41041, opens browser
claw-insights start --port 8080 # Custom port
claw-insights start --no-auth   # Disable authentication
claw-insights stop              # Stop the service
claw-insights restart           # Restart
```

## Verify

```bash
curl http://127.0.0.1:41041/health
# → {"status":"ok",...}
```

## Upgrade

```bash
npm update -g claw-insights
# Or re-run the install script
curl -fsSL https://claw-insights.com/install.sh | sh
```

## Quick Config

| Variable                           | Default                       | Description                 |
| ---------------------------------- | ----------------------------- | --------------------------- |
| `CLAW_INSIGHTS_SERVER_PORT`        | `41041`                       | Server port                 |
| `CLAW_INSIGHTS_API_TOKEN`          | _(auto)_                      | Auth token (min 32 chars)   |
| `CLAW_INSIGHTS_NO_AUTH`            | `false`                       | Disable auth entirely       |
| `CLAW_INSIGHTS_DB`                 | `~/.claw-insights/metrics.db` | SQLite database path        |
| `CLAW_INSIGHTS_RAW_RETENTION_DAYS` | `7`                           | Raw metric retention (days) |

Full configuration reference: See [references/configuration.md](references/configuration.md)

## Troubleshooting

| Symptom                     | Cause                        | Fix                                                |
| --------------------------- | ---------------------------- | -------------------------------------------------- |
| `EADDRINUSE`                | Port already in use          | `claw-insights stop` then retry, or use `--port`   |
| `Cannot connect to gateway` | OpenClaw gateway not running | Start gateway: `openclaw gateway start`            |
| `401 Unauthorized`          | Token mismatch               | Check `CLAW_INSIGHTS_API_TOKEN` or use `--no-auth` |
| `Node.js version error`     | Node.js < 22.5               | Upgrade Node.js to ≥ 22.5                          |

More troubleshooting: See [references/troubleshooting.md](references/troubleshooting.md)

## Next Step

Use the `claw-insights-snapshot` skill to generate and share visual status cards via REST API.
