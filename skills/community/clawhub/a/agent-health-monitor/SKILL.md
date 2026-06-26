---
name: agent-health-monitor
description: |
  Monitors agent health status and detects failures for fault-tolerant agent systems.
  
  **Trigger scenarios:**
  - User asks about agent health or status
  - User mentions "check agents", "agent failure", "health check"
  - System needs to detect unresponsive agents
  - Fault tolerance monitoring required
---

# Agent Health Monitor

Monitors agent and session health to detect failures and ensure system reliability.

## Usage

```javascript
const monitor = require('./skills/agent-health-monitor');

// Check all agents health
const health = await monitor.checkHealth();

// Get failed agents
const failed = await monitor.getFailedAgents();

// Monitor continuously
monitor.startMonitoring(30000); // Check every 30s
```

## Features

- **Session Status Check**: Verifies active sessions
- **Agent Liveness Detection**: Detects unresponsive agents
- **Resource Monitoring**: Tracks CPU/memory usage
- **Failure Alerts**: Notifies on detected failures

## Output

Returns a health report with:
- Total agents/sessions count
- Healthy vs unhealthy count
- Failed agents list
- Resource usage summary
