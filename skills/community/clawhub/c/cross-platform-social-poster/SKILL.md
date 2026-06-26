---
name: social-media-poster
description: Cross-platform social media posting for X (Twitter), Telegram, and Discord. Post content simultaneously to multiple platforms, format messages for each platform's requirements, and manage multi-channel social media presence. Use when sharing updates, announcements, or content across Twitter, Telegram channels/groups, and Discord servers.
---

# Social Media Poster - X, Telegram, Discord

Post content simultaneously across X (Twitter), Telegram, and Discord with platform-specific formatting.

## Platform Requirements

### X (Twitter) Setup
Use `xurl` CLI or direct API calls:
```bash
# Install xurl
npm i -g xurl

# Authenticate
xurl auth
```

### Telegram Bot Setup
1. Create bot via @BotFather on Telegram
2. Get your bot token
3. Get chat ID (channel or group)

Required: Bot token + Chat ID

### Discord Webhook Setup
1. Go to Server Settings → Integrations → Webhooks
2. Create new webhook
3. Copy webhook URL

Required: Webhook URL

---

## Quick Start: Post to All Three Platforms

### Bash Script Template
```bash
#!/bin/bash
# cross_post.sh - Post to X, Telegram, Discord simultaneously

MESSAGE="Your message content here"
IMAGE_PATH=""  # Optional: path to image

# X (Twitter)
xurl post "$MESSAGE" ${IMAGE_PATH:+--media "$IMAGE_PATH"}

# Telegram
curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
  -d chat_id="$TELEGRAM_CHAT_ID" \
  -d text="$MESSAGE" \
  -d parse_mode="Markdown"

# Discord
curl -s -X POST "$DISCORD_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "{\"content\": \"$MESSAGE\"}"
```

---

## Platform-Specific Formatting

### X (Twitter) Best Practices
- **Character limit:** 280 characters
- **Hashtags:** 2-3 relevant hashtags at the end
- **Mentions:** @username for mentions
- **Links:** Automatically shortened
- **Media:** Up to 4 images, 1 GIF, or 1 video

```bash
# Post with xurl
xurl post "Check out our new update! 🚀 #AI #Tech"

# Post with image
xurl post "New feature demo" --media ./screenshot.png

# Reply to tweet
xurl reply <tweet_id> "Thanks for the mention!"
```

### Telegram Best Practices
- **Markdown/HTML support** for rich formatting
- **No character limit** (for all practical purposes)
- **Supports:** images, documents, polls, keyboards
- **Channels:** Use @channelusername or numeric chat ID

```bash
# Send text message
curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
  -d chat_id="$CHAT_ID" \
  -d text="*Bold* _Italic_ [Link](https://example.com)" \
  -d parse_mode="MarkdownV2"

# Send photo
curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendPhoto" \
  -F chat_id="$CHAT_ID" \
  -F photo="@./image.jpg" \
  -F caption="Photo caption"
```

### Discord Best Practices
- **Embeds** for rich messages
- **Webhook username/avatar** customization
- **Max 2000 characters** per message
- **Supports:** attachments, embeds, reactions

```bash
# Simple message via webhook
curl -s -X POST "$DISCORD_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Hello from webhook!",
    "username": "MyBot",
    "avatar_url": "https://example.com/avatar.png"
  }'

# Rich embed message
curl -s -X POST "$DISCORD_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "embeds": [{
      "title": "Announcement",
      "description": "New release is out!",
      "color": 5814783,
      "fields": [
        {"name": "Version", "value": "2.0", "inline": true},
        {"name": "Date", "value": "2026-01-15", "inline": true}
      ]
    }]
  }'
```

---

## Multi-Platform Posting Workflow

### 1. Prepare Content
```bash
# Base content
TITLE="Big Announcement"
BODY="We just launched something amazing. Check it out!"
LINK="https://example.com/news"
IMAGE="./announcement.png"
```

### 2. Platform-Specific Versions
```bash
# X (Twitter) - Concise
TWEET="$TITLE: $BODY $LINK #News #Launch"

# Telegram - Detailed with markdown
TG_MSG="*$TITLE*\n\n$BODY\n\n[Read more]($LINK)"

# Discord - Rich embed format
DISCORD_JSON=$(cat <<EOF
{
  "content": "",
  "embeds": [{
    "title": "$TITLE",
    "description": "$BODY",
    "url": "$LINK",
    "color": 3447003
  }]
}
EOF
)
```

### 3. Post in Parallel
```bash
# Post to all three platforms (background for speed)
xurl post "$TWEET" --media "$IMAGE" &
curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendPhoto" \
  -F chat_id="$CHAT_ID" -F photo="@$IMAGE" -F caption="$TG_MSG" &
curl -s -X POST "$DISCORD_WEBHOOK" \
  -H "Content-Type: application/json" -d "$DISCORD_JSON" &
wait
echo "Posted to all platforms!"
```

---

## Environment Variables Setup

Create `.env` file:
```bash
# X/Twitter
X_API_KEY=your_api_key
X_API_SECRET=your_api_secret

# Telegram
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_CHAT_ID=@yourchannel

# Discord
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

Load with:
```bash
source .env
```

---

## Common Use Cases

### Product Launch
- **X:** Short announcement + hashtags + image
- **Telegram:** Detailed announcement + images + buttons
- **Discord:** Embed with details + @everyone mention if appropriate

### Blog Post Promotion
- **X:** Title + excerpt + link + 2 hashtags
- **Telegram:** Full snippet + link + formatted
- **Discord:** Embed with author, thumbnail, description

### Live Stream Announcement
- **X:** "Going live now!" + link + image
- **Telegram:** Pin message with reminder
- **Discord:** @here + embed with countdown

---

## Tips for Effective Cross-Posting

1. **Tailor per platform**: Don't just copy-paste identically
2. **Timing matters**: Post when each platform's audience is active
3. **Use platform features**: Threads on X, pins on Telegram, embeds on Discord
4. **Track engagement**: Use platform analytics to see what works
5. **Handle errors gracefully**: If one platform fails, others should still post
