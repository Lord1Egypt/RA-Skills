---
name: activity-notifier
description: "Broadcast agent activity status to Discord channel (thinking, tool use, web search, coding, done, error). Use for transparency so users know agent is working."
metadata: { "openclaw": { "emoji": "📢", "requires": { "config": ["channels.discord.token"] } } }
allowed-tools: ["message"]
---

# Activity Notifier

Broadcast real-time agent activity to Discord channel.

## When to Use

✅ **USE this skill when:**
- Starting a long-running task (installing skills, downloading files, etc.)
- Waiting for rate limits or external APIs
- Running multiple sequential operations
- User might think you're stuck or buggy

## Activity Types

| Status | Emoji | When |
|--------|-------|------|
| 🤔 Thinking | 🤔 | Starting to think/plan |
| 🔧 Working | 🔧 | Using tools |
| 🌐 Web | 🌐 | Searching/fetching from web |
| 💻 Coding | 💻 | Writing/editing code |
| ⏳ Waiting | ⏳ | Waiting for rate limit/API |
| ✅ Done | ✅ | Task completed |
| ❌ Error | ❌ | Something went wrong |

## Usage Examples

```javascript
// Send activity update
message({
  action: "send",
  channel: "discord",
  to: "channel:1477516155655688306",
  message: "⏳ **Activity Update**\n\nInstalling 6 skills... (waiting for rate limit)"
})
```

## Guidelines

- **Be concise** — short updates, not novels
- **Use emoji** — visual scanning is faster
- **Include progress** — "3/6 installed" is better than "installing..."
- **Don't spam** — only for tasks >5 seconds
- **Final summary** — always send completion message

## Configuration

Optional: Set `ACTIVITY_CHANNEL_ID` in environment to override default channel.
