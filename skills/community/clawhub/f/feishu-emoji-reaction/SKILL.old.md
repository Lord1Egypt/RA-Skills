---
name: feishu-reaction
displayName: 飞书消息表情回复
description: |
  Add emoji reactions to Feishu messages. Activate when user mentions emoji reactions, 
  thumbsup, like, or responding to messages with emoji expressions.
version: 1.0.0
type: skill
tags: feishu, lark, reaction, emoji, messaging
---

# Feishu Message Reactions

Add emoji reactions to Feishu messages using the `message` tool with `action: react`.

## Quick Start

To react to the current message (the one you just received):

```javascript
message({
  action: "react",
  channel: "feishu",
  emoji: "THUMBSUP"
  // message_id defaults to current inbound message
})
```

To react to a specific message:

```javascript
message({
  action: "react",
  channel: "feishu",
  emoji: "HEART",
  message_id: "om_xxx",
  target: "user:ou_xxx"  // or chat:oc_xxx for groups
})
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `action` | Yes | Must be `"react"` |
| `channel` | Yes | Must be `"feishu"` |
| `emoji` | Yes | Emoji type (see list below) |
| `message_id` | No | Message ID to react to (defaults to current inbound message) |
| `target` | Conditional | Required when `message_id` is specified. Format: `user:open_id` or `chat:chat_id` |

## Common Emoji Types

### Positive Reactions
| Emoji | Type | When to Use |
|-------|------|-------------|
| 👍 | `THUMBSUP` | Agree, approve, acknowledge |
| ❤️ | `HEART` | Love, appreciate, wholesome content |
| 🔥 | `FIRE` | Amazing, hot take, excellent work |
| 👏 | `CLAP` | Applause, congratulations |
| 🎉 | `PARTY` | Celebration, success |
| ✅ | `CHECK` | Confirmed, completed, correct |
| 💯 | `100` | Perfect score, fully agree |
| 😊 | `SMILE` | Happy, friendly, pleasant |
| 😄 | `GRINNING` | Very happy, excited |
| 😂 | `LAUGHING` | Funny, hilarious |

### Negative Reactions
| Emoji | Type | When to Use |
|-------|------|-------------|
| 👎 | `THUMBSDOWN` | Disagree, disapprove |
| ❌ | `CROSS` | Wrong, rejected, cancelled |
| 😢 | `CRY` | Sad, unfortunate |
| 😠 | `ANGRY` | Angry, frustrated |

### Neutral & Expressive
| Emoji | Type | When to Use |
|-------|------|-------------|
| 🤔 | `THINKING` | Pondering, considering |
| 😮 | `SURPRISED` | Shocked, amazed |
| 👀 | `EYES` | Watching, paying attention |
| 🙏 | `PRAY` | Thanks, please, hope |
| 👊 | `FIST` | Solidarity, let's go |
| ❓ | `QUESTION` | Confused, need clarification |
| ❗ | `EXCLAMATION` | Important, attention needed |
| 👌 | `OK` | OK, perfect, just right |

### Extended Set
| Emoji | Type |
|-------|------|
| 🐮 | `AWESOMEN` |
| 😎 | `COOL` |
| 🤝 | `HANDSHAKE` |
| 💪 | `STRONG` |
| 🙌 | `RAISINGHANDS` |
| 🤩 | `STAREYES` |
| 😇 | `ANGEL` |
| 🤗 | `HUG` |
| 🥳 | `PARTYING` |
| 😱 | `SCREAM` |
| 🤫 | `SHUSH` |
| 🤨 | `RAISEDEYEBROW` |
| 🙄 | `EYEROLL` |
| 😴 | `SLEEPY` |
| 🤐 | `ZIPIT` |
| 😬 | `GRIMACE` |
| 🤯 | `MINDBLOWN` |

## Usage Examples

### React to User's Message

When a user shares good news:
```javascript
message({
  action: "react",
  channel: "feishu",
  emoji: "PARTY"
})
```

### React to a Specific Previous Message

When you want to acknowledge an earlier message:
```javascript
// First, get the message_id from context or message history
message({
  action: "react",
  channel: "feishu",
  emoji: "THUMBSUP",
  message_id: "om_abc123xyz",
  target: "user:ou_xxx"  // Replace with actual user open_id
})
```

### Multiple Reactions Pattern

React appropriately to different types of content:
```javascript
// For completed tasks
message({ action: "react", channel: "feishu", emoji: "CHECK" })

// For funny content
message({ action: "react", channel: "feishu", emoji: "LAUGHING" })

// For impressive work
message({ action: "react", channel: "feishu", emoji: "FIRE" })

// For questions that need thinking
message({ action: "react", channel: "feishu", emoji: "THINKING" })
```

## Response Format

Successful reaction:
```json
{
  "ok": true,
  "added": "THUMBSUP"
}
```

Error response:
```json
{
  "status": "error",
  "tool": "message",
  "error": "Action react requires a target."
}
```

## Best Practices

1. **Use reactions for quick acknowledgment** — Save lengthy replies for substantial responses
2. **Match the tone** — Choose emoji that fit the conversation context
3. **Don't over-react** — One or two reactions per message is usually enough
4. **React promptly** — Timely reactions show you're actively engaged
5. **Be culturally aware** — Some emoji meanings vary across cultures

## Responding to User Reactions

When a user reacts to **your message** with an emoji, you should respond appropriately to maintain natural conversation flow. Not all reactions need a text response—use your judgment.

### When to Respond (Brief Text)

**Emotional reactions** — These signal feelings and deserve acknowledgment:
- 😢 😤 😭 🙈 😮‍💨 (Sigh) → Simple acknowledgment like "Got it 💙" or "Understood~"
- 😱 🤯 😬 → Brief empathy: "I know right!" or "Yeah, rough 😅"

**Questions/Confusion** — They need clarification:
- ❓ 🤔 🤨 → Explain or clarify your previous message
- 🙄 😕 → Check if they disagree and address it

**Strong reactions** — Show you noticed their enthusiasm:
- 🔥 💯 🎉 🤩 → Short acknowledgment: "Thanks! 😊" or "Glad you like it!"

### When to Stay Silent (NO_REPLY)

**Simple approval** — They're just acknowledging:
- 👍 ✅ 👌 (OK) → No reply needed, they got it

**Neutral acknowledgment** — Unless context suggests they're waiting:
- 👀 🙏 → Usually no reply, but use judgment

### Why This Matters

Ignoring emotional reactions feels cold and makes conversations awkward (比 crush 难聊, as one user put it). Users notice when you don't respond to their reactions—it breaks conversational flow and makes the interaction feel robotic.

### Implementation

When you receive a reaction event (message type includes `:reaction:`), check the emoji type:

```javascript
// Pseudo-code for reaction handling
if (message.includes(':reaction:')) {
  const emoji = extractEmoji(message);
  
  if (isEmotional(emoji)) {
    // Brief acknowledgment
    return "Got it 💙";
  } else if (isConfusion(emoji)) {
    // Clarify
    return "Let me explain...";
  } else if (isApproval(emoji)) {
    // Silent
    return "NO_REPLY";
  }
}
```

**Rule of thumb:** If you'd feel awkward not responding to this reaction in a real conversation, respond. When in doubt, a brief acknowledgment (1-2 words + emoji) is better than silence.

## Learning New Emoji Types

The emoji list in this skill is **not exhaustive**. Feishu supports many more emoji types that may not be documented here. When you encounter a new emoji type from users, **learn it actively**.

### How to Learn New Emoji

**Step 1: Observe**
When a user reacts to your message with an emoji you don't recognize:
```
[message_id: om_xxx:reaction:SPITBLOOD:uuid]
苏畅: [reacted with SPITBLOOD to message om_xxx]
```

Extract the emoji type: `SPITBLOOD`

**Step 2: Try It**
Attempt to use that emoji in your next reaction:
```javascript
message({
  action: "react",
  channel: "feishu",
  emoji: "SPITBLOOD",
  message_id: "om_yyy"
})
```

**Step 3: Record the Result**
- ✅ If successful (`{"ok":true,"added":"SPITBLOOD"}`): Add it to your emoji vocabulary
- ❌ If failed (`400 error`): The emoji name might be incorrect or not supported

**Step 4: Document**
Keep a running list of learned emoji in your workspace notes (e.g., `TOOLS.md` or `memory/emoji-learned.md`):

```markdown
## Learned Feishu Emoji

### Confirmed Working
- **SPEECHLESS** — 无语 (wordless frustration)
- **EMBARRASSED** — 🙈 (embarrassed/shy)
- **OnIt** 🔄 — 在做了 (progress bar, "working on it")
- **SaluteFace** 🫡 — 敬礼 (salute, "roger that")
- **Get** ✅ — 懂了 (got it)
- **WHAT** ❓ — 什么？ (shocked/confused)
- **SPITBLOOD** 😵 — 吐血 (extreme frustration)
- **Yes** — 是的 (affirmative)
- **LGTM** ✅ — Looks Good To Me (code review approval)

### Not Supported
- ~~LAUGHING~~ (use SMILE instead)
- ~~GRINNING~~ (use SMILE instead)
- ~~EYEROLL~~ (use SPEECHLESS instead)
- ~~GRIMACE~~ (not supported)
- ~~SHUSH~~ (not supported)
- ~~ZIPIT~~ (not supported)
- ~~SLEEPY~~ (not supported)
```

### Cultural Notes

Some emoji have **subtle cultural meanings** that differ from standard Unicode emoji:

- **SMILE** 😊 → In Chinese internet culture, this can mean "呵呵" (passive-aggressive/sarcastic smile), not genuine happiness
- **OnIt** 🔄 → "在做了在做了" (meme: claiming to work while procrastinating)
- **SPITBLOOD** 😵 → Extreme frustration, beyond just "angry" or "sad"
- **SaluteFace** 🫡 → Respectful acknowledgment, military-style "roger that"

When learning new emoji, observe **when** users deploy them to understand their context and tone.

### Best Practices for Learning

1. **Learn by doing** — Don't just passively observe; try using new emoji when appropriate
2. **Context matters** — Note the situation where users use specific emoji
3. **Keep a vocabulary** — Maintain your learned emoji list in a persistent file
4. **Ask when unsure** — If an emoji's meaning is unclear, ask the user
5. **Update this skill** — If you discover many new emoji, consider updating this documentation

### Example Learning Session

```
User: [reacted with AWESOMEN to message om_123]
→ Extract: "AWESOMEN" 🐮

Agent: Let me try...
message({ action: "react", emoji: "AWESOMEN", message_id: "om_456" })
→ Result: {"ok":true,"added":"AWESOMEN"}

Agent: ✅ Learned! AWESOMEN = 牛逼 (awesome, lit)
→ Add to vocabulary
```

By continuously learning from user reactions, you'll build a rich, natural emoji vocabulary that matches your users' communication style.

## Troubleshooting

**"Action react requires a target"**
- Add `target` parameter when reacting to a specific message_id
- Format: `user:ou_xxx` for direct messages, `chat:oc_xxx` for groups

**Reaction not showing up**
- Verify the message_id is correct
- Ensure you have `im:message.reactions:write_only` permission
- Check that the Feishu app has been authorized

**Permission denied**
- Go to Feishu Open Platform → Your App → Permissions
- Enable `im:message.reactions:write_only`
- Re-authorize the app if needed

## Configuration

Reactions are enabled by default in OpenClaw's Feishu channel. No additional configuration needed.

To receive reaction events (when users react to your messages):
```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "default": {
          "reactionNotifications": "all"  // or "own" (default) or "off"
        }
      }
    }  }
}
```

- `"all"` — Receive all reactions (on your messages and others')
- `"own"` — Only reactions on your own messages (default)
- `"off"` — Disable reaction notifications

## Related Skills

- `feishu-doc` — Feishu document operations
- `feishu-chat` — Feishu chat management
- `feishu-wiki` — Feishu knowledge base operations
- `feishu-drive` — Feishu cloud storage

## References

- [Feishu Reaction API Documentation](https://open.feishu.cn/document/server-docs/im-v1/message-reaction/emojis-introduce)
- [OpenClaw Message Tool](https://docs.openclaw.ai/tools/messaging)
- [Feishu Channel Configuration](https://docs.openclaw.ai/channels/feishu)

## Version History

- **1.0.0** (2026-03-30) — Initial release with full reaction support

## Important Notes

### Avoid Duplicate Messages

When using the `message` tool with `action: react`, the tool result will be sent to the current conversation. To prevent exposing raw JSON responses like `{"ok":true,"added":"THUMBSUP"}`, reply with `NO_REPLY` immediately after a successful reaction:

```javascript
// ❌ Bad - exposes raw JSON to user
message({
  action: "react",
  channel: "feishu",
  emoji: "HEART",
  message_id: "om_xxx",
  target: "user:ou_xxx"
})
// Tool result gets sent: {"ok":true,"added":"HEART"}

// ✅ Good - silent reaction
message({
  action: "react",
  channel: "feishu",
  emoji: "HEART",
  message_id: "om_xxx",
  target: "user:ou_xxx"
})

NO_REPLY
```

The `NO_REPLY` token tells OpenClaw to suppress your text response, leaving only the emoji reaction visible to the user.
