---
name: message
description: Send a message to Jarvis by typing "/message" followed by your text. Works as a text command - triggers when you type "/message" in chat.
---

# Message Command

## Usage

Type `/message` followed by your message:

```
/message What's the weather today?
/message Turn on my PC
/message Remind me to call mom at 5pm
```

## How It Works

When you type `/message` as text:
1. OpenClaw detects the `/message` prefix
2. Routes the text after it to Jarvis
3. Jarvis responds with a **public** message

## Notes

- Works in any channel where Jarvis is present
- Response is public (not ephemeral)
- No need to @mention the bot