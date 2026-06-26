---
name: agentpulse
description: AI-powered infrastructure monitoring — thin agent, smart cloud. One-command install, real-time alerts, baseline learning, auto-remediation.
tags:
  - monitoring
  - infrastructure
  - devops
  - alerts
  - remediation
  - agent
  - saas
category: devops
---

# AgentPulse — AI Infrastructure Monitoring

## What It Does

AgentPulse monitors your servers with a thin, open-source agent and a smart cloud API. It learns your infrastructure's normal behavior over time, alerts you when something's wrong, and can auto-remediate issues with your approval.

**Architecture: Dumb Agent, Smart Cloud**
- The client agent is thin and open-source — ships metrics to the API, does zero analysis
- The cloud API receives metrics, runs analysis, stores history, sends alerts, handles remediation
- The moat is baseline learning (per-server norms over time) and accumulated intelligence

## Quick Start

### 1. Register Your Server

```bash
curl -X POST https://api.agentpulse.io/v1/servers \
  -H "Content-Type: application/json" \
  -d '{"hostname": "my-server", "plan": "starter"}'
```

Save the returned `server_id` and `api_key`.

### 2. Install the Agent

One-liner install:

```bash
curl -fsSL https://agentpulse.io/install.sh | bash -s -- --api-key YOUR_API_KEY --server-id YOUR_SERVER_ID
```

Or manual install:

```bash
# Download
wget -O /usr/local/bin/agentpulse-agent https://agentpulse.io/downloads/agent_client.py
chmod +x /usr/local/bin/agentpulse-agent

# Configure
cat > /etc/agentpulse.conf << 'EOF'
API_KEY=your_api_key_here
SERVER_ID=your_server_id_here
API_URL=https://api.agentpulse.io
EOF

# Run a quick health check
agentpulse-agent --quick
```

### 3. Set Up Cron

```bash
# Quick check every 5 minutes
*/5 * * * * /usr/local/bin/agentpulse-agent --quick

# Full report every 30 minutes
*/30 * * * * /usr/local/bin/agentpulse-agent --full

# Daily deep report at 8am UTC
0 8 * * * /usr/local/bin/agentpulse-agent --full
```

### 4. Get Alerts

Alerts are delivered via Telegram, email, or webhook. Configure your notification channels in the dashboard at https://agentpulse.io/dashboard.

## What Gets Monitored

### Critical Services (immediate alert if down)
- SSH, Docker, Nginx, your custom services

### System Metrics
- CPU, memory, disk usage with trend analysis
- Process counts and zombie detection
- Load average and uptime tracking

### Network
- Listening ports (unexpected changes flagged)
- Active connections
- DNS resolution health

### Baseline Learning (after 24h)
- Per-server normal ranges for all metrics
- Anomaly detection when values deviate from learned norms
- Trend alerts before thresholds are breached

## Alert Levels

| Level | Meaning | Action |
|-------|---------|--------|
| Healthy | All clear | No action |
| Warning | Something's off | Review when convenient |
| Critical | Service down or resource exhausted | Immediate attention |
| Error | Agent can't report | Check the agent |

## Auto-Remediation (Pro + Business)

When a critical alert fires, AgentPulse can suggest or execute remediation actions:

- Restart crashed services
- Clear disk space (logs, caches)
- Rotate logs automatically
- Scale resources

All auto-remediation requires your approval via Telegram buttons or dashboard confirmation.

## Pricing

| Plan | Price | Servers | Features |
|------|-------|---------|----------|
| Starter | $29/mo | 1 | Alerts + dashboard |
| Pro | $99/mo | 5 | Alerts + auto-remediation |
| Business | $299/mo | Unlimited | Priority remediation, daily reports, API access |

## API Reference

### Submit a Report
```
POST /api/v1/report
Headers: X-API-Key: your_api_key
Body: { "server_id": "...", "metrics": {...} }
```

### Get Server Status
```
GET /api/v1/servers/{server_id}/status
Headers: X-API-Key: your_api_key
```

### Get Alert History
```
GET /api/v1/servers/{server_id}/alerts?limit=50
Headers: X-API-Key: your_api_key
```

### Health Check
```
GET /health
```

## Requirements

- Linux server (Ubuntu 20.04+, Debian 11+, CentOS 8+)
- Python 3.8+
- curl or wget
- Cron (for scheduled reports)

## Support

- Docs: https://agentpulse.io/docs
- Telegram: @agentpulse_support
- Email: support@agentpulse.io
