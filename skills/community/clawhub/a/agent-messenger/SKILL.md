---
name: agent-messenger
description: Send batch messages to OpenClaw agents across Telegram, Discord, or other channels with delivery tracking and retry logic. Use when: (1) Broadcasting messages to multiple agents simultaneously, (2) Need delivery confirmation/ACK, (3) Want to trigger agent workflows via messages, (4) Require scheduled or triggered message campaigns. Supports templating, conditional routing, and fallback delivery.
---

# Agent Messenger

Send coordinated messages to OpenClaw agents with full delivery tracking.

## Quick Start

### Send to all agents (one-shot)
```bash
python3 scripts/send_telegram_direct.py "Tout le monde va bien ?" --agents all
```

### Send to specific agents
```bash
python3 scripts/send_telegram_direct.py "Test message" --agents cybercodeur snake picsou
```

### Send heartbeat (wait for manual ACKs)
```bash
bash scripts/heartbeat_check.sh "Heartbeat: Tout le monde là?" 10
# Waits 10 seconds for agents to react with ✅ on Telegram
```

### Schedule heartbeat every 30 minutes
```bash
bash scripts/install_heartbeat_cron.sh "*/30"
```

Checks crontab:
```bash
crontab -l
tail -f /tmp/heartbeat.log
```

## Use Cases

**Broadcast health checks**: Send "Are you alive?" to all agents, get ACK responses
**Trigger workflows**: Send commands like "/health" to activate agent skills  
**Update notifications**: Push configuration changes to all agents
**Scheduled messages**: Combine with cron for periodic check-ins

## Core Patterns

### Pattern 1: Direct API Telegram (no chat resolution needed)
Uses bot tokens + user ID directly. Bypasses OpenClaw chat resolution issues.
```bash
curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
  -d "chat_id=<USER_ID>&text=<MESSAGE>"
```

### Pattern 2: Agent Batching
Extract all agents from `openclaw.json`, build message list, send in parallel.

### Pattern 3: Delivery Verification
Store sent message IDs, poll for ACK reactions, track delivery rate.

## Files

- **scripts/send_telegram_direct.py** - Core: Send messages via Telegram API
- **scripts/heartbeat_check.sh** - Send heartbeat, wait for manual ACKs (RECOMMENDED)
- **scripts/install_heartbeat_cron.sh** - Automate heartbeat via cron job
- **scripts/send_agent_msg.sh** - Legacy: Bash-only batch sender

## Troubleshooting

**"Chat not found"** → Use Pattern 1 (direct API) or ensure user ID matches
**No responses** → Check agent model is running, token is valid
**Rate limit** → Implement exponential backoff (auto in v2+)

## Next Steps

- Add Discord/Slack handlers (references/slack-adapter.md)
- Implement ACK tracking (scripts/track_acks.py)
- Build message queue with retries (scripts/message_queue.py)
