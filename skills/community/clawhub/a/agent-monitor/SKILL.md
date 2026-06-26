---
name: agent-monitor
description: Agent work status monitoring and automatic activation system. Triggers when monitoring subagent runtime status, detecting prolonged unresponsive "stalled" states, and automatically activating them to resume operation. Suitable for long-running task monitoring, automated operations, agent health checks, and similar scenarios.
---

# Agent Monitor - Agent Work Status Monitoring

## Overview

This skill provides subagent work status monitoring and automatic activation capabilities:

1. **Status Monitoring** - Real-time monitoring of agent runtime status
2. **Stall Detection** - Detecting "stalled" states where an agent has been unresponsive for over 5 minutes
3. **Automatic Activation** - Automatically sending activation messages to resume agent operation

## Core Capabilities

### 1. Monitor Agent Status

Use the `subagents` tool to obtain a list of currently running agents:

```python
# List recently running agents
subagents(action="list", recentMinutes=30)
```

### 2. Detect Stalled Status

Detection logic:
- Obtain the agent's last activity time
- Calculate the difference from the current time
- If over 5 minutes (300 seconds) with no activity → Determine as "stalled"

### 3. Automatically Activate Agents

Use the `steer` action of the `subagents` tool to send an activation message:

```python
# Send an activation message to a specified agent
subagents(action="steer", target="<agent-id>", message="Continue working")
```

## Workflow

```
┌─────────────────────┐
│  Get Agent List     │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Check Each Agent's  │
│  Last Activity Time │
└──────────┬──────────┘
           ▼
      ┌────────┐
      │ >5min? ├──No──┐
      └────┬───┘      │
          Yes│         │
           ▼          │
┌─────────────────────┐│
│  Determine as       ││
│  Stalled Status     ││
└──────────┬──────────┘│
           ▼           │
┌─────────────────────┐│
│  Send Activation    ││
│  Message to Resume  ││
└─────────────────────┘│
           │           │
           └───────────┘
                 ▼
        ┌─────────────────┐
        │ Continue Monitoring│
        └─────────────────┘
```

## Usage Examples

### Example 1: Monitor All Agents

```python
# 1. Get agent list
result = subagents(action="list", recentMinutes=30)

# 2. Check each agent's status
for agent in result.agents:
    idle_time = calculate_idle_time(agent.lastActivity)
    if idle_time > 300:  # Over 5 minutes
        # 3. Automatically activate
        subagents(action="steer", target=agent.id, message="Please continue executing the task")
```

### Example 2: Monitor a Specific Agent

```python
# Monitor an agent with a specified ID
agent_id = "builder-agent-001"
result = subagents(action="list", recentMinutes=10)

# Find the target agent
for agent in result.agents:
    if agent.id == agent_id:
        if is_stalled(agent, threshold=300):
            activate_agent(agent_id)
```

## Script Tool

### monitor_agents.py

Located at `scripts/monitor_agents.py`, provides complete monitoring functionality:

```bash
# Monitor and automatically activate stalled agents
python scripts/monitor_agents.py --threshold 300 --auto-activate

# Detect only, without automatic activation
python scripts/monitor_agents.py --threshold 300 --dry-run

# Monitor a specific agent
python scripts/monitor_agents.py --target agent-id-001
```

Parameter descriptions:
- `--threshold`: Stall determination threshold (seconds), default 300 (5 minutes)
- `--auto-activate`: Automatically activate stalled agents
- `--dry-run`: Detect only, do not execute activation
- `--target`: Specify a specific agent ID to monitor

## Integration into Scheduled Tasks

The monitoring script can be integrated into cron scheduled tasks for continuous monitoring:

```bash
# Check every 2 minutes
*/2 * * * * python /path/to/monitor_agents.py --auto-activate
```

## Notes

1. **Threshold Setting**: Adjust the stall determination threshold based on the task type; complex tasks may require longer thresholds
2. **Activation Message**: Activation messages sent should be concise and clear, prompting the agent to continue working
3. **Avoid False Activation**: Ensure the agent is genuinely stalled before activating to avoid interfering with normal thought processes
4. **Logging**: It is recommended to log each detection and activation operation for subsequent analysis