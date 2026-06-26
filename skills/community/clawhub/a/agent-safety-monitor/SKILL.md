---
name: agent-safety-monitor
description: Real-time AI agent safety monitoring, anomaly detection, and constraint enforcement. Use when building agent guardrails, detecting unsafe behaviors, enforcing action limits, or creating safety dashboards for autonomous AI systems. Covers behavior logging, rule engines, alert systems, and compliance tracking.
---

# Agent Safety Monitor

Monitor AI agent behavior in real-time, detect anomalies, and enforce safety constraints.

## Quick Start

Run the monitor against an agent log stream:

```bash
python3 scripts/monitor.py --config safety_rules.yaml --input agent_logs/
```

## Architecture

```
Agent Actions → Event Stream → Rule Engine → Alerts → Dashboard
                                   ↓
                              Anomaly Detector
                                   ↓
                              Auto-Pause/Kill
```

## Safety Rule Types

1. **Rate limits**: Max N actions per minute/hour
2. **Action allowlists**: Only permit specific tool calls
3. **Content filters**: Block PII exfiltration, harmful outputs
4. **Budget caps**: Stop when cost exceeds threshold
5. **Scope limits**: Restrict file/API/network access
6. **Behavioral anomalies**: Flag unusual patterns (tool call frequency spikes, repetitive loops)

## Rule Configuration

See `references/rules-reference.md` for the YAML schema.

## Alert Channels

- Console (default)
- Webhook (Slack, Discord)
- File log
- Dashboard (HTTP server)

## Dashboard

Launch the monitoring dashboard:

```bash
python3 scripts/dashboard.py --port 8080
```
