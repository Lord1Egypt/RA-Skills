---
name: dingtalk-bot
description: DingTalk Bot integration for messaging, group management, approval workflows, and attendance. Send messages, manage groups, handle approvals, and automate notifications via DingTalk Open API.
tags:
  - dingtalk
  - bot
  - messaging
  - approval
  - attendance
  - automation
version: 1.0.0
author: chenq
---

# DingTalk Bot

Complete DingTalk bot integration for AI agents.

## Features

### 1. Messaging
- Send text, markdown, link, and action card messages
- Send to groups via webhook or API
- At mentions and notifications

### 2. Group Management
- Create groups
- Add/remove members
- Group robot management

### 3. Approval Workflows
- Create approval instances
- Query approval status
- Approval callbacks

### 4. Attendance
- Get attendance records
- Query employee attendance
- Vacation balance

## Prerequisites

1. Create a DingTalk Corp at https://open.dingtalk.com
2. Create a Custom Robot in group settings
3. Get Webhook URL and Secret (for signature verification)
4. For advanced features, create an internal app and get AppKey/AppSecret

## Configuration

Set environment variables:
```bash
# For webhook-based bots
export DINGTALK_WEBHOOK_URL="https://oapi.dingtalk.com/robot/send?access_token=xxx"
export DINGTALK_SECRET="SECxxx"

# For API-based bots
export DINGTALK_APP_KEY="ding_xxx"
export DINGTALK_APP_SECRET="xxx"
export DINGTALK_AGENT_ID="xxx"
```

## Usage

### Send Text Message (Webhook)
```python
from dingtalk_bot import DingTalkBot

# Webhook mode
bot = DingTalkBot(webhook_url="YOUR_WEBHOOK_URL", secret="YOUR_SECRET")

# Send text
bot.send_text("Hello from bot!")

# Send with at mentions
bot.send_text("Hello @all", at_mobiles=["13800138000"])
```

### Send Markdown Message
```python
bot.send_markdown(
    title="Daily Report",
    text="## Sales Report\n- Today: $10,000\n- Week: $50,000"
)
```

### Send Action Card
```python
bot.send_action_card(
    title="Approval Request",
    text="Please approve the following request",
    buttons=[
        {"title": "Approve", "action_url": "https://.../approve"},
        {"title": "Reject", "action_url": "https://.../reject"}
    ]
)
```

### Create Group (API Mode)
```python
# API mode with authentication
bot = DingTalkBot(app_key="xxx", app_secret="xxx", agent_id="xxx")

group = bot.create_group(name="Project Team", owner_user_id="manager123")
print(group["open_conversation_id"])
```

### Approval Workflow
```python
# Create approval
approval = bot.create_approval(
    process_code="PROC-xxx",
    originator_user_id="user123",
    form_values={"title": "Leave Request", "days": 3}
)

# Get status
status = bot.get_approval_instance(approval["process_instance_id"])
```

### Attendance Query
```python
records = bot.get_attendance_records(
    work_date="2024-03-15",
    user_ids=["user123", "user456"]
)
print(records)
```

## API Reference

### Webhook Methods
| Method | Description |
|--------|-------------|
| `send_text(text, at_mobiles=None, at_user_ids=None)` | Send text message |
| `send_markdown(title, text)` | Send markdown message |
| `send_link(title, text, message_url, pic_url)` | Send link message |
| `send_action_card(title, text, buttons)` | Send action card |
| `send_feed_card(links)` | Send feed card |

### API Methods
| Method | Description |
|--------|-------------|
| `create_group(name, owner_user_id, user_ids)` | Create group |
| `add_group_members(chat_id, user_ids)` | Add members |
| `remove_group_members(chat_id, user_ids)` | Remove members |
| `create_approval(process_code, originator_user_id, form_values)` | Create approval |
| `get_approval_instance(process_instance_id)` | Get approval status |
| `get_attendance_records(work_date, user_ids)` | Get attendance |
| `get_vacation_balance(user_id)` | Get vacation balance |

## Signature Generation

For webhook security, generate signature:
```python
import hmac
import hashlib
import base64
import time

timestamp = str(round(time.time() * 1000))
secret = "YOUR_SECRET"

string_to_sign = f'{timestamp}\n{secret}'
sign = hmac.new(string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
signature = base64.b64encode(sign).decode('utf-8')
```

## Error Handling

Common errors:
- `400031`: Invalid signature - check secret
- `400035`: Missing parameters - verify request body
- `400036`: Invalid approval process - check process_code
- `400037`: Duplicate approval - instance already exists

## Links

- [DingTalk Open Platform](https://open.dingtalk.com)
- [API Documentation](https://open.dingtalk.com/document/)
- [Robot Development](https://open.dingtalk.com/document/robot)
