# Feishu Cards

Send interactive cards to Feishu (飞书) directly via Feishu Open API.

## When to Use

- User wants to send rich interactive messages in Feishu
- Need buttons, forms, or dropdown menus in messages
- Want beautifully formatted messages with colors

## Installation

```bash
clawhub install feishu-cards
```

## Usage

### CLI

```bash
# Basic card
feishu-cards --to "ou_xxx" --title "标题" --content "内容"

# With buttons
feishu-cards --to "ou_xxx" --title "任务" --content "有新任务" --buttons "处理,稍后"

# Custom color
feishu-cards --to "ou_xxx" --title "警告" --content "注意" --template "red"

# To chat
feishu-cards --to "oc_xxx" --type "chat_id" --title "群通知" --content "大家好"
```

### As Python Module

```python
from feishu_card_sender import FeishuCardSender

sender = FeishuCardSender()
result = sender.send(
    recipient_id="ou_xxx",
    title="任务提醒",
    content="你有一个新任务",
    buttons=["立即处理", "稍后提醒"],
    template="blue"
)
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--to` | Recipient ID (user or chat) | Required |
| `--type` | ID type: open_id, user_id, chat_id | open_id |
| `--title` | Card title | Required |
| `--content` | Card content text | Required |
| `--buttons` | Comma-separated buttons | None |
| `--template` | Color: blue, green, red, yellow, grey | blue |
| `--note` | Optional note | None |

## Card Elements

- **Header** - Title with color template
- **Content** - Main text (plain text format)
- **Buttons** - Interactive buttons (primary/default types)
- **Note** - Additional info with icon

## Button Types

- `primary` - Blue button (first button)
- `default` - Gray button (other buttons)

## Examples

### Task Notification

```bash
python3 feishu_card_sender.py \
  --to "ou_9d00de9a95a2fb69c425f0a39930c67a" \
  --title "📋 任务通知" \
  --content "你有一个新任务待处理" \
  --buttons "立即处理,稍后提醒" \
  --template "blue"
```

### Alert Card

```bash
python3 feishu_card_sender.py \
  --to "ou_xxx" \
  --title "⚠️ 警告" \
  --content "账户存在异常登录" \
  --template "red" \
  --buttons "查看详情"
```

## Requirements

- Python 3.7+
- requests library

Install: `pip install requests`

## Configuration

Credentials are read from environment variables (optional):
- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`

Defaults to OpenClaw's configured Feishu app.

## Notes

- Cards work in Direct Messages and group chats
- Buttons open URLs (configure your callback server for full interactivity)
- Maximum card size: 45KB

---

*Made for ClawHub*
