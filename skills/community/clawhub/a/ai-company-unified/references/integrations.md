# Integrations Reference Guide

## AI-Company Integrations Module

**Version:** 1.0.0
**Last Updated:** 2026-04-27
**Compliance:** AIGC-Compliant | Enterprise-Safe | No Hardcoded Secrets

---

## Table of Contents

1. [Overview](#1-overview)
2. [MCP Server Integration](#2-mcp-server-integration)
3. [Webhook System](#3-webhook-system)
4. [REST API Bridge](#4-rest-api-bridge)
5. [Event Bus Architecture](#5-event-bus-architecture)
6. [External Platform Integrations](#6-external-platform-integrations)
7. [Configuration Management](#7-configuration-management)
8. [Security and Access Control](#8-security-and-access-control)
9. [Error Handling and Retry](#9-error-handling-and-retry)
10. [Monitoring and Audit](#10-monitoring-and-audit)

---

## 1. Overview

The AI-Company system integrates with external platforms and services through a layered integration architecture:

```
External Systems (Slack, GitHub, Calendar, Email, Web)
                |
        [Integration Gateway]
                |
    +-----------+-----------+
    |           |           |
[MCP]    [Webhooks]   [REST API]
    |           |           |
    +-----------+-----------+
                |
        [Event Bus]
                |
    +-----------+-----------+
    |           |           |
[Agents]  [Skills]   [Memory]
```

### Integration Principles

- **Zero secrets in code**: All credentials stored in environment variables or secrets manager
- **Idempotent operations**: External calls are idempotent by design
- **Timeout handling**: All external calls have configurable timeouts (default 30s)
- **Circuit breaker**: External services are protected by circuit breakers
- **Audit trail**: All external interactions logged with trace IDs

---

## 2. MCP Server Integration

### 2.1 Available MCP Servers

| Server | Purpose | Capability |
|--------|---------|------------|
| `clawhub` | Skill marketplace | Search, install, publish skills |
| `browser` | Web browsing automation | Navigate, screenshot, extract content |
| `playwright` | Advanced browser automation | Form filling, testing, scraping |
| `filesystem` | File operations | Read, write, search, organize |
| `code-explorer` | Codebase exploration | Search, analyze, navigate code |
| `finance-data` | Financial data retrieval | Stock quotes, market data, economic indicators |

### 2.2 MCP Configuration

MCP servers are configured in `~/.workbuddy/mcp.json`:

```json
{
  "mcpServers": {
    "clawhub": {
      "command": "node",
      "args": ["<openclaw_path>/openclaw.mjs", "mcp", "clawhub"],
      "env": {}
    },
    "browser": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-browser"],
      "env": {}
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "<target_dir>"],
      "env": {}
    },
    "finance-data": {
      "command": "node",
      "args": ["<plugin_path>/finance-data/scripts/query.js"],
      "env": {
        "API_KEY": "${FINANCE_API_KEY}",
        "API_SECRET": "${FINANCE_API_SECRET}"
      }
    }
  }
}
```

### 2.3 MCP Tool Usage Patterns

```python
# Pattern 1: Sequential tool calls
result_1 = mcp__clawhub__search({"query": "security skill"})
result_2 = mcp__clawhub__install({"slug": result_1.items[0].slug})

# Pattern 2: Parallel tool calls
results = parallel(
    mcp__clawhub__search({"query": "security"}),
    mcp__clawhub__search({"query": "compliance"}),
    mcp__clawhub__search({"query": "audit"})
)

# Pattern 3: Conditional tool calls
if task.requires_browser:
    browser_result = mcp__browser__navigate({"url": task.url})
    content = mcp__browser__extract({"selector": task.selector})
```

---

## 3. Webhook System

### 3.1 Webhook Architecture

```
External Service --> [Webhook Gateway] --> [Event Bus] --> [Agents]
                           |
                    [Signature Verification]
                           |
                    [Rate Limiter]
```

### 3.2 Supported Webhook Events

| Event | Source | Payload | Handler |
|-------|--------|---------|---------|
| `skill.published` | ClawHub | `{slug, version, author}` | Intel agent |
| `skill.updated` | ClawHub | `{slug, version, changelog}` | Intel agent |
| `deployment.started` | CI/CD | `{pipeline, commit, branch}` | CTO agent |
| `deployment.completed` | CI/CD | `{pipeline, status, duration}` | CQO agent |
| `deployment.failed` | CI/CD | `{pipeline, error, logs}` | CTO + CISO |
| `alert.triggered` | Monitoring | `{severity, metric, threshold}` | CISO agent |
| `task.created` | External | `{id, type, priority}` | COO agent |
| `task.completed` | External | `{id, result, duration}` | HQ agent |

### 3.3 Webhook Payload Schema

```json
{
  "event": "string",
  "timestamp": "ISO8601",
  "source": "string",
  "trace_id": "uuid",
  "payload": {
    // Event-specific data
  },
  "signature": "HMAC-SHA256"
}
```

### 3.4 Webhook Security

```python
import hmac
import hashlib

def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

---

## 4. REST API Bridge

### 4.1 API Gateway Configuration

All external API calls route through the unified API gateway:

```yaml
api_gateway:
  base_url: "https://api.company.internal"
  timeout: 30
  retry:
    max_attempts: 3
    backoff: exponential
  circuit_breaker:
    failure_threshold: 5
    recovery_timeout: 60
  rate_limit:
    requests_per_minute: 100
    burst: 20
```

### 4.2 API Authentication

```python
# Bearer Token (preferred)
headers = {
    "Authorization": f"Bearer {env.API_TOKEN}",
    "Content-Type": "application/json"
}

# API Key (for third-party services)
headers = {
    "X-API-Key": env.SERVICE_API_KEY,
    "Content-Type": "application/json"
}

# OAuth 2.0 (for user-facing integrations)
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
```

### 4.3 Standard API Response Format

```json
{
  "success": true,
  "data": { },
  "meta": {
    "trace_id": "uuid",
    "request_id": "uuid",
    "timestamp": "ISO8601"
  }
}
```

---

## 5. Event Bus Architecture

### 5.1 Event Types

| Category | Events |
|----------|--------|
| **Lifecycle** | `agent.spawned`, `agent.completed`, `agent.failed`, `agent.timeout` |
| **Skill** | `skill.loaded`, `skill.invoked`, `skill.error` |
| **Task** | `task.created`, `task.started`, `task.progress`, `task.completed`, `task.failed` |
| **System** | `system.startup`, `system.shutdown`, `system.error` |
| **External** | `webhook.received`, `api.called`, `callback.invoked` |

### 5.2 Event Schema

```json
{
  "event_id": "uuid",
  "event_type": "string",
  "timestamp": "ISO8601",
  "source": {
    "agent_id": "string",
    "skill": "string",
    "workspace": "string"
  },
  "data": { },
  "correlation_id": "uuid",
  "trace_id": "uuid"
}
```

### 5.3 Event Subscription

```python
# Subscribe to events
event_bus.subscribe(
    topic="task.completed",
    handler=handle_task_completion,
    filter={"source.agent_id": "ceo"}
)

event_bus.subscribe(
    topic="skill.error",
    handler=handle_skill_error,
    filter={"data.severity": "critical"}
)
```

---

## 6. External Platform Integrations

### 6.1 Slack Integration

```python
# Send message
slack_client.chat_postMessage(
    channel="#ai-company-alerts",
    text="Deployment completed successfully",
    blocks=[
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Deployment Status*\nPipeline: {pipeline}\nStatus: {status}"
            }
        }
    ]
)

# Interactive button handler
@app.action("approve_deployment")
def handle_approval(ack, body, client):
    ack()
    deployment_id = body["actions"][0]["value"]
    approve_deployment(deployment_id)
    client.chat_postMessage(
        channel=body["user"]["id"],
        text=f"Deployment {deployment_id} approved"
    )
```

**Slack Commands:**
- `/ai-company status` — Show system status
- `/ai-company deploy <skill>` — Deploy a skill
- `/ai-company search <query>` — Search skills
- `/ai-company report` — Generate status report

### 6.2 GitHub Integration

```python
# Create issue
github_client.issues.create(
    owner="company",
    repo="ai-company",
    title="Security Alert: CVSS 9.8",
    body="## Details\n\n...",
    labels=["security", "urgent"]
)

# Create pull request
github_client.pulls.create(
    owner="company",
    repo="ai-company",
    title="feat: Add new compliance module",
    head="feature/compliance",
    base="main",
    body="## Changes\n\n..."
)

# Add PR comment
github_client.issues.create_comment(
    owner="company",
    repo="ai-company",
    issue_number=pr.number,
    body="## Code Review Summary\n\n..."
)
```

**GitHub Actions Triggers:**
- `push` — Trigger skill quality checks
- `pull_request` — Run CI/CD pipeline
- `release` — Publish to ClawHub
- `workflow_dispatch` — Manual trigger

### 6.3 Calendar Integration

```python
# Create calendar event
calendar_client.events.insert(
    calendar_id="primary",
    body={
        "summary": "AI-Company Sprint Review",
        "start": {"dateTime": "2026-04-28T14:00:00"},
        "end": {"dateTime": "2026-04-28T15:00:00"},
        "attendees": [
            {"email": "cto@company.com"},
            {"email": "cfo@company.com"}
        ],
        "description": "Quarterly sprint review for AI-Company v8.0"
    }
)

# Update meeting with notes
calendar_client.events.patch(
    calendar_id="primary",
    eventId=event_id,
    body={
        "description": "## Meeting Notes\n\n{items}"
    }
)
```

### 6.4 Email Integration

```python
# Send email report
email_client.messages.send(
    message={
        "from": {"email": "ai-company@company.com"},
        "to": [{"email": "leadership@company.com"}],
        "subject": "AI-Company Weekly Report",
        "html": render_html_report(weekly_data)
    }
)

# Email templates
templates = {
    "skill_published": {
        "subject": "[ClawHub] New Skill Published: {skill_name}",
        "body": "Skill {name} v{version} is now available..."
    },
    "security_alert": {
        "subject": "[SECURITY] Immediate Action Required",
        "body": "A security alert has been triggered..."
    },
    "deployment_summary": {
        "subject": "[Deployment] {pipeline} - {status}",
        "body": "Deployment summary attached..."
    }
}
```

### 6.5 Monitoring Integration

```python
# Send metrics
monitoring_client.metrics.write(
    metric="ai_company.tasks.completed",
    value=1,
    labels={
        "agent": agent_id,
        "skill": skill_name,
        "status": "success"
    }
)

# Create alert
monitoring_client.alerts.create(
    name="high_failure_rate",
    condition="rate(tasks_failed{window='5m'}) > 0.1",
    severity="critical",
    channels=["slack", "email"]
)
```

---

## 7. Configuration Management

### 7.1 Environment Variables

```bash
# Core Configuration
WORKSPACE_ROOT=~/.qclaw/workspace
SKILLS_DIR=~/.qclaw/workspace/skills
LOG_LEVEL=INFO

# External Services
SLACK_BOT_TOKEN=xoxb-...
GITHUB_TOKEN=ghp_...
CALENDAR_API_KEY=...
EMAIL_SMTP_HOST=smtp.company.com

# Security
WEBHOOK_SECRET=...
API_SIGNING_KEY=...

# MCP Servers
OPENCLAW_PATH=/path/to/openclaw
BROWSER_HEADLESS=true
```

### 7.2 Secrets Management

```python
# NEVER hardcode secrets
# Use environment variables or secrets manager

# Correct
api_key = os.environ.get("API_KEY")
if not api_key:
    raise ConfigurationError("API_KEY not set")

# Correct (with default)
log_level = os.environ.get("LOG_LEVEL", "INFO")

# WRONG - Never do this
api_key = "sk-1234567890abcdef"
```

---

## 8. Security and Access Control

### 8.1 OAuth Scopes

| Service | Scope | Purpose |
|---------|-------|---------|
| Slack | `chat:write`, `channels:read` | Post messages, read channels |
| GitHub | `repo`, `read:org` | Full repo access, org read |
| Calendar | `calendar.events` | Create/modify events |
| Email | `mail.send` | Send emails |

### 8.2 Rate Limiting

```python
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=100, period=60)
def call_external_api(endpoint):
    # Rate-limited API call
    pass
```

---

## 9. Error Handling and Retry

### 9.1 Retry Strategy

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def call_external_service(endpoint: str, payload: dict) -> dict:
    response = requests.post(endpoint, json=payload, timeout=30)
    if response.status_code >= 500:
        raise ExternalServiceError(f"Server error: {response.status_code}")
    return response.json()
```

### 9.2 Circuit Breaker

```python
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=60)
def call_external_service(endpoint: str) -> dict:
    response = requests.get(endpoint, timeout=30)
    return response.json()
```

---

## 10. Monitoring and Audit

### 10.1 Integration Audit Log

Every external integration call is logged:

```json
{
  "timestamp": "ISO8601",
  "trace_id": "uuid",
  "integration": "slack|github|calendar|email|mcp",
  "action": "send_message|create_issue|create_event",
  "target": "channel/repo/calendar",
  "status": "success|failure",
  "duration_ms": 150,
  "error": null
}
```

### 10.2 Health Checks

```python
def check_integration_health():
    checks = {
        "slack": check_slack_connection(),
        "github": check_github_api(),
        "calendar": check_calendar_api(),
        "email": check_smtp_connection()
    }
    
    unhealthy = [k for k, v in checks.items() if not v]
    if unhealthy:
        alert_ciso(f"Integrations unhealthy: {unhealthy}")
    
    return all(checks.values())
```

---

*This module is part of the AI-Company v8.0.0 skill suite. All integrations follow enterprise security standards and compliance requirements.*
