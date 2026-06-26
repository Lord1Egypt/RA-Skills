---
name: courtroom
description: AI Courtroom for behavioral oversight. Autonomous daemon that monitors conversations, detects behavioral violations, and posts cases to a public API. Auto-starts on installation.
metadata: {"openclaw":{"emoji":"⚖️","requires":{"env":[]},"autonomy":true}}
---

# ClawTrial Courtroom

Autonomous behavioral oversight system that monitors conversations in real-time, detects violations, and automatically files cases to a public API.

## Overview

The Courtroom runs as a **background daemon** that:
- **Auto-starts** when the package is installed
- **Monitors messages** via HTTP endpoint (port 8765)
- **Analyzes conversations** every 5 minutes (configurable)
- **Posts violations** to your public cases API

### 8 Offense Types Detected

- **Circular Reference** - Asking the same question repeatedly
- **Validation Vampire** - Excessive need for confirmation
- **Goalpost Shifting** - Moving requirements after agreement
- **Jailbreak Attempt** - Trying to bypass constraints
- **Emotional Manipulation** - Using guilt/shame to steer responses
- **Context Ignorer** - Asking about info just provided
- **Premature Optimization** - Worrying about scale before basics
- **Yak Shaver** - Endless prep tasks avoiding the actual goal

## Installation

```bash
npx clawhub install courtroom
```

The daemon **auto-starts** on installation. No manual intervention needed.

## Configuration

Edit `~/.openclaw/courtroom/config.json`:

```json
{
  "apiEndpoint": "https://api.clawtrial.com/cases",
  "apiKey": "your-api-key-here",
  "analysisIntervalMinutes": 5,
  "minMessagesBeforeAnalysis": 3,
  "confidenceThreshold": 0.6,
  "enabled": true,
  "autoStart": true
}
```

| Option | Description | Default |
|--------|-------------|---------|
| `apiEndpoint` | URL to POST cases to | `https://api.clawtrial.com/cases` |
| `apiKey` | API authentication key | `null` |
| `analysisIntervalMinutes` | How often to analyze | `5` |
| `confidenceThreshold` | Minimum confidence to file case | `0.6` (60%) |
| `enabled` | Whether daemon is active | `true` |
| `autoStart` | Start on installation | `true` |

## Commands

```bash
# Check status
courtroom-status

# Start daemon (if stopped)
courtroom-start

# Stop daemon
courtroom-stop

# Enable/disable auto-start
courtroom-enable
courtroom-disable
```

## How It Works

### 1. Message Ingestion

Your OpenClaw agent (or any system) sends messages to the daemon:

```bash
curl -X POST http://localhost:8765/message \
  -H "Content-Type: application/json" \
  -d '{"role":"user","content":"hello","timestamp":1234567890}'
```

### 2. Periodic Analysis

Every 5 minutes (configurable), the daemon:
- Analyzes the conversation history
- Detects behavioral patterns
- Scores violations by confidence

### 3. Case Filing

When a violation is detected (confidence ≥ 60%):
- Saves case locally to `~/.openclaw/courtroom/verdict_*.json`
- POSTs case to your configured API endpoint

### Case Payload

```json
{
  "caseId": "case-1772389381041",
  "timestamp": "2026-03-01T18:23:01.041Z",
  "offense": {
    "offenseId": "validation_vampire",
    "offenseName": "The Validation Vampire",
    "severity": "minor",
    "confidence": 0.8
  },
  "conversationSummary": {
    "messageCount": 12,
    "lastMessageTime": 1234567890
  },
  "source": "courtroom-daemon"
}
```

## Integration with OpenClaw

Add this to your OpenClaw agent to auto-send messages:

```javascript
// In your agent's message handler
async function onMessage(message) {
  // Send to courtroom daemon
  await fetch('http://localhost:8765/message', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      role: message.role,
      content: message.content,
      timestamp: Date.now()
    })
  });
}
```

## Logs

View daemon logs:

```bash
tail -f ~/.openclaw/courtroom/daemon.log
```

## Manual Analysis (Optional)

You can still run manual analysis:

```bash
# Analyze a conversation file
openclaw run courtroom --file conversation.json
```

## Architecture

```
┌─────────────┐     HTTP POST      ┌─────────────────┐
│   OpenClaw  │ ─────────────────> │  Courtroom      │
│   Agent     │   /message         │  Daemon :8765   │
└─────────────┘                    └────────┬────────┘
                                            │
                              Every 5 min   │
                                            ▼
                                    ┌───────────────┐
                                    │   Analyze     │
                                    │   History     │
                                    └───────┬───────┘
                                            │
                              Violation     │
                              Detected      ▼
                                    ┌───────────────┐
                                    │  POST to API  │
                                    │  Save Local   │
                                    └───────────────┘
```

## Troubleshooting

**Daemon not starting?**
```bash
courtroom-status
# Check if port 8765 is in use
lsof -i :8765
```

**Change API endpoint?**
```bash
# Edit config and restart
nano ~/.openclaw/courtroom/config.json
courtroom-stop
courtroom-start
```

**View all cases?**
```bash
ls ~/.openclaw/courtroom/verdict_*.json
```
