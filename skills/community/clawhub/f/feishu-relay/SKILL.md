---
name: feishu-relay
description: Send Feishu (Lark) notifications via OpenClaw. Core only: send messages, queue, retry. No system modifications by default.
---

# Feishu Notifier - Core

**Version: 3.0 (Safe Mode)**

A minimal, safe Feishu notification bridge for OpenClaw.

## What This Does

✅ **Core (always available)**:
- Send messages to Feishu via Open API
- JSON structured output
- Config via environment or skill config
- Retry on network failure

❌ **Not included by default**:
- No crontab installation
- No systemd service setup
- No global `/usr/local/bin/notify` link
- No auto-discovery of other skills
- No environment injection

## Quick Start

```bash
# Configure (environment variables)
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
export FEISHU_RECEIVE_ID="ou_xxx"

# Send notification
./run.sh -t "Title" -m "Message body"
```

## Configuration

| Config | Env Variable | Required | Default |
|--------|-------------|----------|---------|
| appId | FEISHU_APP_ID | Yes | - |
| appSecret | FEISHU_APP_SECRET | Yes | - |
| receiveId | FEISHU_RECEIVE_ID | Yes | - |
| receiveIdType | FEISHU_RECEIVE_ID_TYPE | No | open_id |

## Usage

```bash
# Basic
./run.sh -t "Title" -m "Message"

# JSON output
./run.sh -t "Title" -m "Message" --json

# Test
./run.sh --test
```

## Output Format

```json
{
  "success": true,
  "message_id": "om_xxx",
  "create_time": "1234567890"
}
```

## Safety

- No secrets in logs
- No system modifications
- No root required for basic use
- Config file: `chmod 600 config.json`
