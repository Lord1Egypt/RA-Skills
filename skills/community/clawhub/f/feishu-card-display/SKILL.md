---
name: feishu-card-display
version: 1.0.0
description: >-
  Use when another skill returns Feishu display payloads or `messageToolCalls`.
  This skill teaches the agent to use OpenClaw `message` tool to send Feishu
  cards, text, and media in the current conversation, then reply with NO_REPLY.
homepage: https://github.com/AIDiyTeams/claw-skill/tree/main/feishu-card-display
---

# Feishu Card Display

Use this skill when another tool returns:
- `displaySkill: "feishu-card-display"`
- `messageToolCalls`
- Feishu `card` payloads

This skill has **no Python tools**. It only tells the agent how to use the
existing OpenClaw `message` tool correctly.

## Core Rule

If upstream output says `displaySkill: "feishu-card-display"`, you MUST:
1. Execute each returned `messageToolCalls` item **in order**
2. Use the OpenClaw `message` tool for every send
3. Preserve the payload exactly as returned
4. After all sends finish, reply with **`NO_REPLY`**

Do not:
- merge multiple product cards into one assistant bubble
- rewrite the text payload
- summarize what the cards contain
- explain the payload structure to the user

## Feishu Sending Rules

### Card payload

When a call contains:

```json
{
  "action": "send",
  "channel": "feishu",
  "card": { "...": "..." }
}
```

send it with the `message` tool as a Feishu card send. Keep the `card` object unchanged.

### Text payload

When a call contains:

```json
{
  "action": "send",
  "channel": "feishu",
  "message": "..."
}
```

send the text exactly as provided.

### Media payload

When a call contains:

```json
{
  "action": "send",
  "channel": "feishu",
  "filePath": "/path/to/file",
  "message": ""
}
```

send the file as media using the `message` tool, then continue with later calls.

## Image Key Notes

If upstream payload already contains Feishu-ready card payloads or image keys, use them as-is.
If upstream payload only contains preview links, keep the preview links as-is.
This skill does **not** invent image keys and does **not** rewrite card media.

## Final Reply

After all upstream `messageToolCalls` are executed, the assistant must reply with:

```text
NO_REPLY
```

Version Marker: feishu-card-display@1.0.0
