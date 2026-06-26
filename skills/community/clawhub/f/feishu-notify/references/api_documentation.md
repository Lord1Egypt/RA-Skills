# Feishu Webhook API Documentation

## API Overview

Feishu (Lark) provides webhook API for sending messages to groups or chats. Webhooks allow external systems to send messages without authentication (except the webhook URL itself).

### Base Configuration

- **Webhook URL Format**: `https://open.feishu.cn/open-apis/bot/v2/hook/{webhook_key}`
- **Method**: POST
- **Content-Type**: `application/json`

## Authentication

Feishu webhooks use the webhook URL itself as authentication. No additional headers or tokens are required.

### Authentication Method

- The webhook URL contains a unique key that identifies the bot and the target group/chat
- Anyone with the webhook URL can send messages to the group
- Keep webhook URLs secure and do not share them publicly

## Message Types

### 1. Text Message

Simple text-only messages.

#### Request Format

```json
{
  "msg_type": "text",
  "content": {
    "text": "Your message here"
  }
}
```

#### Example

```bash
curl -X POST "https://open.feishu.cn/open-apis/bot/v2/hook/your-webhook-key" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "text",
    "content": {
      "text": "Hello, this is a text message!"
    }
  }'
```

### 2. Post (Rich Text) Message

Messages with rich formatting including text, links, @mentions, images, and more.

#### Request Format

```json
{
  "msg_type": "post",
  "content": {
    "post": {
      "zh_cn": {
        "title": "Message Title",
        "content": [
          [
            {
              "tag": "text",
              "text": "Paragraph text here"
            },
            {
              "tag": "a",
              "text": "Link text",
              "href": "https://example.com"
            },
            {
              "tag": "at",
              "user_id": "ou_xxxxx",
              "user_name": "User Name"
            }
          ]
        ]
      }
    }
  }
}
```

#### Content Elements

| Tag | Description | Required Fields |
|-----|-------------|-----------------|
| text | Plain text | text |
| a | Hyperlink | text, href |
| at | @mention user | user_id, user_name |
| img | Image | image_key |
| emoji | Emoji | emoji_type, emoji_id |

#### Example

```json
{
  "msg_type": "post",
  "content": {
    "post": {
      "zh_cn": {
        "title": "Deployment Notification",
        "content": [
          [
            {
              "tag": "text",
              "text": "Deployment to production completed successfully!\n"
            },
            {
              "tag": "at",
              "user_id": "ou_xxxxx",
              "user_name": "DevOps Team"
            }
          ],
          [
            {
              "tag": "a",
              "text": "View Deployment Details",
              "href": "https://dashboard.example.com/deployment/123"
            }
          ]
        ]
      }
    }
  }
}
```

### 3. Interactive Card Message

Rich cards with structured content, buttons, images, and interactive elements.

#### Request Format

```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": {
        "tag": "plain_text",
        "content": "Card Title"
      },
      "template": "blue"
    },
    "elements": [
      {
        "tag": "div",
        "text": {
          "tag": "lark_md",
          "content": "Card content using markdown"
        }
      },
      {
        "tag": "hr"
      },
      {
        "tag": "action",
        "actions": [
          {
            "tag": "button",
            "text": {
              "tag": "plain_text",
              "content": "Button Text"
            },
            "type": "primary",
            "url": "https://example.com"
          }
        ]
      }
    ]
  }
}
```

#### Header Templates

| Template | Color | Use Case |
|----------|-------|----------|
| red | Red | Alerts, errors, critical |
| orange | Orange | Warnings |
| yellow | Yellow | Important notices |
| green | Green | Success, completion |
| blue | Blue | Information, notifications |
| grey | Grey | Neutral messages |

#### Card Elements

| Tag | Description |
|-----|-------------|
| div | Text container |
| hr | Horizontal line |
| action | Button group |
| img | Image |
| note | Note box |

#### Example: Alert Card

```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": {
        "tag": "plain_text",
        "content": "Server Alert"
      },
      "template": "red"
    },
    "elements": [
      {
        "tag": "div",
        "text": {
          "tag": "lark_md",
          "content": "**Server:** prod-server-01\n**Error:** Connection timeout\n**Time:** 2026-03-17 14:30:00"
        }
      },
      {
        "tag": "hr"
      },
      {
        "tag": "action",
        "actions": [
          {
            "tag": "button",
            "text": {
              "tag": "plain_text",
              "content": "View Logs"
            },
            "type": "danger",
            "url": "https://logs.example.com/prod-server-01"
          },
          {
            "tag": "button",
            "text": {
              "tag": "plain_text",
              "content": "Restart Server"
            },
            "type": "primary",
            "url": "https://dashboard.example.com/restart/prod-server-01"
          }
        ]
      }
    ]
  }
}
```

### 4. Image Message

Send image messages using image_key or image_url.

#### Request Format (using image_key)

```json
{
  "msg_type": "image",
  "content": {
    "image_key": "img_v2_xxxxx-xxxxx"
  }
}
```

#### Request Format (using image_url)

```json
{
  "msg_type": "image",
  "content": {
    "image_url": "https://example.com/image.jpg"
  }
}
```

## Response Format

### Successful Response (Code 0)

```json
{
  "code": 0,
  "msg": "success",
  "data": {}
}
```

### Error Response

```json
{
  "code": 19001,
  "msg": "param invalid: content.text is empty"
}
```

## Error Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 19001 | Invalid parameter |
| 19002 | Webhook URL is invalid or expired |
| 19003 | Message size exceeds limit (200KB) |
| 19004 | Unknown message type |
| 19005 | Card format error |

## Configuration

### Webhook URL Configuration

Store webhook URLs in `~/.openclaw/skills/feishu-notify/config.json`:

```json
{
  "webhooks": {
    "default": "https://open.feishu.cn/open-apis/bot/v2/hook/your-default-webhook-key",
    "alerts": "https://open.feishu.cn/open-apis/bot/v2/hook/your-alerts-webhook-key",
    "notifications": "https://open.feishu.cn/open-apis/bot/v2/hook/your-notifications-webhook-key",
    "devops": "https://open.feishu.cn/open-apis/bot/v2/hook/your-devops-webhook-key",
    "finance": "https://open.feishu.cn/open-apis/bot/v2/hook/your-finance-webhook-key"
  }
}
```

### Getting Webhook URLs

1. Open Feishu (Lark) and go to the group where you want to add a bot
2. Click on group settings
3. Select "Group Robot" (群机器人)
4. Click "Add Robot" (添加机器人)
5. Choose "Custom Robot" (自定义机器人)
6. Configure the robot name and avatar
7. Copy the webhook URL
8. Add the webhook URL to your config file

## Usage Examples

### Command Line Usage

```bash
# Send text message to default webhook
python scripts/send_message.py default --message "Hello from command line!"

# Send alert to alerts webhook
python scripts/send_message.py alerts --type interactive \
  --template templates/card_alert.json \
  --var title="Server Alert" \
  --var message="Server prod-01 is down" \
  --var color="red"

# Send task update
python scripts/send_message.py notifications \
  --template templates/card_task.json \
  --var title="Task Completed" \
  --var task_id="123" \
  --var status="Done" \
  --var assignee="John Doe" \
  --var due_date="2026-03-20" \
  --var description="Task completed successfully"
```

### Python Usage

```python
from scripts.send_message import send_message, load_config, load_template, fill_template

# Load config
webhooks = load_config()
webhook_url = webhooks['default']

# Simple text message
message = {
    "msg_type": "text",
    "content": {
        "text": "Hello from Python!"
    }
}
result = send_message(webhook_url, message)

# Using template
template = load_template('templates/card_alert.json')
variables = {
    'title': 'Server Alert',
    'message': 'Server is down',
    'color': 'red',
    'time': '2026-03-17 14:30:00',
    'source': 'Monitoring System'
}
message = fill_template(template, variables)
result = send_message(webhook_url, message)
```

## Template System

Templates are JSON files with placeholder variables in the format `{{variable_name}}`.

### Template Variables

Common template variables:
- `{{title}}` - Message title
- `{{message}}` - Main message content
- `{{color}}` - Card header color template
- `{{time}}` - Timestamp
- `{{source}}` - Message source
- `{{link}}` - URL for buttons
- `{{task_id}}` - Task ID
- `{{status}}` - Task status
- `{{assignee}}` - Task assignee
- `{{due_date}}` - Task due date
- `{{description}}` - Task description

### Template Directory Structure

```
templates/
├── text_simple.json        # Simple text template
├── post_rich.json          # Rich text template
├── card_alert.json         # Alert card template
├── card_notification.json  # Notification card template
└── card_task.json          # Task card template
```

## Limitations

- **Message size**: Maximum 200KB per message
- **Rate limiting**: 100 messages per minute per webhook
- **Rich text elements**: Maximum 500 elements per message
- **Card elements**: Maximum 50 elements per card
- **Webhook expiration**: Webhooks can expire after 90 days if not used

## Best Practices

1. **Use named webhooks** for different purposes (alerts, notifications, etc.)
2. **Choose appropriate message types** for the content
3. **Use templates** for consistent message formatting
4. **Handle errors** gracefully and provide user feedback
5. **Keep webhook URLs secure** and do not commit to version control
6. **Test webhooks** before deploying to production
7. **Use markdown** in card content for better formatting
8. **Add time and source information** for better traceability

## Security Considerations

- Webhook URLs are sensitive - keep them secret
- Anyone with the webhook URL can send messages
- Consider implementing additional validation in your systems
- Use environment variables or encrypted config for production deployments
- Rotate webhook URLs periodically for enhanced security
- Monitor webhook usage for suspicious activity
