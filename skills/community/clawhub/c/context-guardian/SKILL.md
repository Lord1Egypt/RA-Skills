---
name: context-guardian
version: 1.0.1
description: Proactive context monitoring with smart 3-level alerts. Know when to restart before quality degrades.
author: brucey0017
tags: [monitoring, context, alerts, proactive, quality]
---

# Context Guardian 🛡️

**Your context guardian. Alerts before errors happen.**

Proactive context monitoring that warns you at 60%, 70%, and 85% usage — before context pollution causes errors and hallucinations.

---

## Why You Need This

**The Problem:**
- Long conversations lead to context pollution
- Quality degrades silently as context fills up
- You don't know when to restart until it's too late
- Errors and hallucinations increase after ~70% usage

**The Solution:**
- Continuous monitoring of context usage
- Smart 3-level alerts (⚠️ 60%, 🟠 70%, 🔴 85%)
- Actionable suggestions at each level
- Prevents duplicate alerts

---

## Quick Start

### For Agents: Heartbeat Integration

When you receive a heartbeat poll, include this check:

1. Call `session_status` tool to get current context usage
2. Parse the context percentage from the output
3. Compare against thresholds: 60% (warning), 70% (danger), 85% (critical)
4. If threshold exceeded and not a duplicate alert, display the appropriate alert message
5. Update state file to track alert history

**Implementation:**

```
During heartbeat:
1. Get context usage from session_status
2. Check if usage >= 60%, 70%, or 85%
3. Load state from memory/context-guardian-state.json
4. Determine if alert should be sent (prevent duplicates)
5. If yes, display alert and update state
```

### For Users: Enable in HEARTBEAT.md

Add to your `HEARTBEAT.md`:

```markdown
## Context Monitoring
- Check context usage
- Alert if thresholds exceeded (60%, 70%, 85%)
```

The agent will automatically handle the rest.

---

## How It Works

### Monitoring

The skill calls `session_status` to check your current context usage percentage.

### Alert Levels

**⚠️ Warning (60%)**
```
⚠️ Context: 60%
Getting full. Consider wrapping up or starting fresh soon.
```

**🟠 Danger (70%)**
```
🟠 Context: 70%
Pollution risk rising. Recommend:
• Finish current task
• Start new session for next task
• Or compress with context-optimizer
```

**🔴 Critical (85%)**
```
🔴 Context: 85% - CRITICAL
High error risk. STRONGLY recommend:
• Save work
• Start new session NOW
• Quality degradation likely
```

### Smart Duplicate Prevention

The skill tracks alert history and only alerts when:
1. First time reaching a threshold
2. Alert level upgrades (60% → 70% → 85%)
3. Usage drops below threshold then rises again

---

## Configuration

Edit `config/default.json` or create `config/user.json`:

```json
{
  "enabled": true,
  "checkInterval": "heartbeat",
  "thresholds": {
    "warning": 60,
    "danger": 70,
    "critical": 85
  },
  "alertMethod": "message",
  "alertStyle": "emoji",
  "preventDuplicates": true,
  "trackHistory": true,
  "suggestions": {
    "autoSuggest": true,
    "suggestCompression": true,
    "suggestRestart": true
  }
}
```

### Options

**checkInterval:**
- `"heartbeat"` - Check during heartbeat polls (default)
- `"cron"` - Independent cron job (future)
- `number` - Check every N minutes (future)

**thresholds:**
- Customize alert levels (default: 60, 70, 85)

**alertMethod:**
- `"message"` - Send as message (default)
- `"log"` - Log only
- `"notification"` - System notification (future)

**alertStyle:**
- `"emoji"` - Emoji + concise text (default)
- `"text"` - Plain text
- `"detailed"` - Full explanation

---

## Manual Check

You can manually check context status:

```bash
bash {baseDir}/scripts/check.sh
```

---

## Integration with Other Skills

### context-optimizer

When you reach 70%, the skill suggests using `context-optimizer` to compress your context instead of restarting.

### context-recovery

After context recovery, the skill automatically resumes monitoring.

---

## Implementation Guide for Agents

### Step-by-Step Process

**1. Get Context Usage**

Call `session_status` tool and parse the output:

```
Example output: "Context: 54k/200k (27%)"
Extract: 27
```

**2. Determine Alert Level**

```javascript
if (usage >= 85) level = "critical"
else if (usage >= 70) level = "danger"
else if (usage >= 60) level = "warning"
else level = null
```

**3. Load State**

Read `{workspace}/memory/context-guardian-state.json`:

```json
{
  "lastCheck": 1709452800,
  "lastUsage": 54,
  "lastAlertLevel": "warning",
  "lastAlertTime": 1709452500,
  "history": [...]
}
```

**4. Check if Should Alert**

Prevent duplicate alerts:

```javascript
shouldAlert = false

// First time reaching threshold
if (!lastAlertLevel && level) shouldAlert = true

// Level upgrade (warning → danger → critical)
if (levelNum[level] > levelNum[lastAlertLevel]) shouldAlert = true

// Usage dropped below threshold and rose again
if (lastUsage < threshold - 5 && usage >= threshold) shouldAlert = true
```

**5. Send Alert**

If `shouldAlert`, display the appropriate message:

```
⚠️ Context: 60%
Getting full. Consider wrapping up or starting fresh soon.
```

**6. Update State**

Save new state to `memory/context-guardian-state.json`:

```json
{
  "lastCheck": <current_timestamp>,
  "lastUsage": <current_usage>,
  "lastAlertLevel": <level_if_alerted>,
  "lastAlertTime": <timestamp_if_alerted>,
  "history": [..., {"timestamp": <now>, "usage": <usage>}]
}
```

### Alert Messages

**Warning (60%):**
```
⚠️ Context: 60%
Getting full. Consider wrapping up or starting fresh soon.
```

**Danger (70%):**
```
🟠 Context: 70%
Pollution risk rising. Recommend:
• Finish current task
• Start new session for next task
• Or compress with context-optimizer
```

**Critical (85%):**
```
🔴 Context: 85% - CRITICAL
High error risk. STRONGLY recommend:
• Save work
• Start new session NOW
• Quality degradation likely
```

---

## State Management

State is stored in `{workspace}/memory/context-guardian-state.json`:

```json
{
  "lastCheck": 1709452800,
  "lastUsage": 54,
  "lastAlertLevel": null,
  "lastAlertTime": null,
  "history": [
    {"timestamp": 1709452800, "usage": 54}
  ]
}
```

---

## Troubleshooting

**No alerts appearing:**
- Check that `HEARTBEAT.md` includes context monitoring
- Verify heartbeat is running
- Check state file for errors

**Too many alerts:**
- Increase thresholds in config
- Check `preventDuplicates` is enabled

**Alerts not accurate:**
- Verify `session_status` is working
- Check OpenClaw version compatibility

---

## Examples

### Heartbeat Integration

Add to `HEARTBEAT.md`:

```markdown
## Context Monitoring
- Check context usage
- Alert if thresholds exceeded
```

### Custom Thresholds

Create `config/user.json`:

```json
{
  "thresholds": {
    "warning": 50,
    "danger": 65,
    "critical": 80
  }
}
```

---

## Technical Details

**Dependencies:**
- OpenClaw 2026.2.0+
- `session_status` tool
- Bash

**Performance:**
- Zero overhead (only checks during heartbeat)
- Minimal state storage (~1KB)

**Privacy:**
- All data stored locally
- No external calls
- No telemetry

---

## Roadmap

**v1.1.0:**
- Historical trend tracking
- Usage prediction
- Independent cron mode

**v1.2.0:**
- Auto-trigger context-optimizer
- Visual trend graphs
- Multi-session monitoring

---

## Contributing

Found a bug? Have a suggestion? Open an issue or PR on GitHub.

---

## License

MIT
