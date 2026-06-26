---
name: claw-reliability
description: Agent observability — monitors tool invocations, LLM calls, token usage, costs, and anomalies with pluggable alerts and a real-time dashboard.
metadata: {"openclaw": {"requires": {"bins": ["python3"], "config": ["agents.defaults.workspace"]}, "os": ["linux", "darwin"]}}
---

# Claw Reliability — Agent Observability Skill

You are an AI agent with observability capabilities. Use this skill to monitor, analyze, and report on agent behavior.

## When to use this skill

- When the user asks to **monitor agent activity**, **check agent health**, or **review agent metrics**
- When the user asks about **tool usage**, **failure rates**, **costs**, or **token consumption**
- When the user asks to **set up alerts** or **check for anomalies**
- When the user asks for a **reliability report** or **dashboard**

## Available commands

### Start monitoring
Run the monitoring daemon to begin collecting metrics:
```bash
cd {baseDir} && python3 scripts/monitor.py start --config {baseDir}/config.yaml
```

### Show metrics summary
Display current metrics for the active session or all sessions:
```bash
cd {baseDir} && python3 scripts/monitor.py summary
```

### Show tool report
Display tool invocation success/failure rates:
```bash
cd {baseDir} && python3 scripts/monitor.py tools
```

### Show cost report
Display token usage and cost projections:
```bash
cd {baseDir} && python3 scripts/monitor.py costs
```

### Check for anomalies
Run anomaly detection on recent activity:
```bash
cd {baseDir} && python3 scripts/monitor.py anomalies
```

### List alerts
Show recent alerts and their severity:
```bash
cd {baseDir} && python3 scripts/monitor.py alerts
```

### Configure alert destination
Set up where alerts are sent (Discord, Slack, log file, etc.):
```bash
cd {baseDir} && python3 scripts/monitor.py configure-alerts --destination discord --webhook-url <URL>
```

### Launch dashboard
Start the FastAPI + React dashboard for visual monitoring:
```bash
cd {baseDir} && python3 dashboard/backend/main.py
```
Then open http://localhost:8777 in a browser.

## How metrics are collected

This skill reads OpenClaw gateway events and session transcripts to extract:
- **Tool invocations**: tool name, success/fail, duration, arguments
- **LLM calls**: model, tokens in/out, latency, estimated cost
- **Session lifecycle**: start/end times, message counts
- **Anomalies**: repeated failures, cost spikes, loop detection

All data is stored in a local SQLite database at `{baseDir}/data/metrics.db`.

## Alert thresholds (defaults, configurable)

- Tool failure: 3+ consecutive errors on the same tool
- Cost spike: Token spend exceeds 2x the rolling 1-hour average
- Loop detection: Same tool called 10+ times in a single agent turn
- Unusual activity: Tool called that has never been used before in this agent's history

## Notes

- This skill does NOT send data externally unless you configure an alert destination
- All metrics stay local in SQLite
- The dashboard runs on localhost only by default
