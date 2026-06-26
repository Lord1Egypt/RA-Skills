# 🦞 claw-reliability

**Agent Observability for OpenClaw** — Monitor tool invocations, LLM costs, anomalies, and get real-time alerts.

OpenClaw gives AI agents hands. claw-reliability gives them a nervous system.

## What it does

- **Tracks every tool invocation** — success/failure rates, latency, error messages
- **Monitors LLM costs** — token usage per model, estimated spend, cost projections
- **Detects anomalies** — repeated tool failures, cost spikes, agent loops, unusual activity
- **Sends alerts** — pluggable: Discord, log file, extend with Slack/email/Telegram
- **Visual dashboard** — FastAPI + React UI for real-time monitoring

## Quick Start

```bash
# Install
clawhub install claw-reliability

# Set up Python environment
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Start monitoring
python3 scripts/monitor.py start

# Configure Discord alerts
python3 scripts/monitor.py configure-alerts --destination discord --webhook-url <YOUR_URL>

# Launch dashboard
python3 dashboard/backend/main.py
# Open http://localhost:8777
```

## Architecture

```
┌───────────────────────────────────────────┐
│            OpenClaw Gateway                │
│   (agent loop, tool calls, LLM calls)     │
└──────────────┬────────────────────────────┘
               │ session transcripts (.jsonl)
               ▼
┌───────────────────────────────────────────┐
│          claw-reliability                  │
│  Parser → Store (SQLite) → Analyzer       │
│                              │             │
│              ┌───────────────┼──────┐      │
│              ▼               ▼      ▼      │
│         Discord           Log    [Extend]  │
│         Webhook           File    Slack..  │
│                                            │
│  Dashboard: FastAPI + React                │
│  http://localhost:8777                     │
└───────────────────────────────────────────┘
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `monitor.py start` | Start monitoring daemon |
| `monitor.py summary` | Metrics summary |
| `monitor.py tools` | Tool invocation report |
| `monitor.py costs` | Cost report by model |
| `monitor.py anomalies` | Run anomaly detection |
| `monitor.py alerts` | List recent alerts |
| `monitor.py configure-alerts` | Set up alert destinations |
| `monitor.py test-alerts` | Test all destinations |

## Alert Types

| Alert | Trigger | Severity |
|-------|---------|----------|
| Tool Failure | 3+ consecutive errors | ⚠️/🚨 |
| Cost Spike | Hourly spend > 2x avg | ⚠️ |
| Loop Detected | Same tool 10+ times | 🚨 |
| Unusual Activity | First-ever tool use | ℹ️ |

## Custom Alert Destinations

```python
from scripts.alerts import BaseAlerter, Alert

class SlackAlerter(BaseAlerter):
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_alert(self, alert: Alert) -> bool:
        # POST to Slack webhook
        return True
```

## Compatibility

- OpenClaw 2026.3.x+
- NemoClaw sandboxed environments
- Linux, macOS, WSL2

## Security Notes

- **Session data stays local.** This skill reads OpenClaw session transcripts that may contain sensitive data — tool arguments, error messages, file paths. All metrics are stored in a local SQLite database and never transmitted unless you configure an external alert destination.
- **External alert destinations receive sanitized text only.** Alert messages and details are redacted before being sent to Discord or other webhook endpoints — API keys, tokens, and home directory paths are stripped. Only use trusted webhook URLs; treat any external endpoint as a potential data recipient.
- **The dashboard loads React and Babel from public CDNs.** For air-gapped or high-security setups, download those assets and serve them locally instead of from `unpkg.com` / `cdnjs`.

## Author

Built by Fiddy
