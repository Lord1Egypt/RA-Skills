---
name: feishu-bot
description: Feishu (Lark) Bot integration for messaging, group management, and approval workflows. Send messages, manage groups, handle approvals, and automate notifications via Feishu Open Platform API.
tags:
  - feishu
  - lark
  - bot
  - messaging
  - automation
version: 1.0.0
author: chenq
---

# Feishu Bot

Complete Feishu/Lark bot integration for AI agents.

## Features

### 1. Messaging
- Send text, rich text, and card messages
- Send to users, groups, or via webhook
- Reply to messages
- Upload and send files/images

### 2. Group Management
- Create groups
- Add/remove members
- Update group info
- Bot group management

### 3. Approval Workflows
- Create approval instances
- Query approval status
- Cancel approvals
- Approval notifications

## Prerequisites

1. Create a Feishu App at https://open.feishu.cn/app
2. Get App ID and App Secret
3. Configure permissions:
   - `im:message` - Send messages
   - `im:message:send_as_bot` - Send as bot
   - `contact:user.base:readonly` - Read user info
   - `im:chat` - Manage groups
   - `approval:approval` - Approval workflows

## Configuration

Set environment variables:
```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
```

Or configure in OpenClaw settings.

## Usage

### Send Text Message
```python
from feishu_bot import FeishuBot

bot = FeishuBot()

# Send to user
bot.send_text("user_id", "Hello from bot!")

# Send to group
bot.send_text("chat_id", "Group message", is_chat=True)
```

### Send Card Message
```python
card = {
    "type": "template",
    "data": {
        "template_id": "xxx",
        "template_variable": {"title": "Notification"}
    }
}
bot.send_card("chat_id", card)
```

### Create Group
```python
group = bot.create_group(
    name="Project Team",
    user_ids=["ou_xxx", "ou_yyy"]
)
print(group["chat_id"])
```

### Approval Workflow
```python
# Create approval
approval = bot.create_approval(
    approval_code="xxx",
    user_id="ou_xxx",
    form={"field1": "value1"}
)

# Query status
status = bot.get_approval_instance(approval["instance_id"])
```

## API Reference

| Method | Description |
|--------|-------------|
| `send_text(target, text, is_chat=False)` | Send text message |
| `send_card(target, card, is_chat=False)` | Send card message |
| `send_image(target, image_key, is_chat=False)` | Send image |
| `send_file(target, file_key, is_chat=False)` | Send file |
| `create_group(name, user_ids)` | Create group |
| `add_group_members(chat_id, user_ids)` | Add members |
| `remove_group_members(chat_id, user_ids)` | Remove members |
| `create_approval(approval_code, user_id, form)` | Create approval |
| `get_approval_instance(instance_id)` | Get approval status |

## Error Handling

Common errors:
- `99991663`: Token expired - refresh tenant token
- `99991664`: Permission denied - check app permissions
- `99991661`: User not found - verify user_id

## Links

- [Feishu Open Platform](https://open.feishu.cn)
- [API Documentation](https://open.feishu.cn/document)
- [Bot Development Guide](https://open.feishu.cn/document/home/introduction-to-feishu-platform/bot-development-odyssey)
