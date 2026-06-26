# How Feishu Group Thread Reply Works

## Background

By default, openclaw-lark plugin replies to group chat messages in the main chat stream.
This causes noise in busy groups. The fix forces all bot replies in group chats into threads.

## Feishu Reply API

Feishu's reply API (`POST /open-apis/im/v1/messages/{message_id}/reply`) has a boolean
parameter `reply_in_thread`:

- `reply_in_thread: true` → reply goes into the message's thread (auto-creates thread if none)
- `reply_in_thread: false` (default) → reply appears as a quote-reply in main chat

**Only the bot reply API is needed** — no extra permissions like `im:message.send_as_user`.

## What Gets Patched

### 1. openclaw-lark plugin (`dispatch.js` + `dispatch-commands.js`)

**Location**: `~/.openclaw/extensions/openclaw-lark/src/messaging/inbound/`

**Original code**:
```js
replyInThread: dc.isThread,
// dc.isThread = isGroup && Boolean(ctx.threadId)
// Only true when the INCOMING message is already in a thread
```

**Patched code**:
```js
replyInThread: dc.isGroup || dc.isThread,
// Now true for ALL group messages, not just thread-originating ones
```

**Files affected**:
- `dispatch.js` — 3 occurrences (main dispatch, i18n card, i18n error)
- `dispatch-commands.js` — 2 occurrences (command dispatch, command error)

### 2. feishu-live-card watcher (`watcher.py`)

**Location**: `~/.openclaw/skills/feishu-live-card/watcher.py`

**Original code**:
```python
def reply_card(self, reply_to_message_id: str, card: Dict) -> Optional[str]:
    body = {
        "msg_type": "interactive",
        "content": json.dumps(card),
    }
```

**Patched code**:
```python
def reply_card(self, reply_to_message_id: str, card: Dict, reply_in_thread: bool = True) -> Optional[str]:
    body = {
        "msg_type": "interactive",
        "content": json.dumps(card),
        "reply_in_thread": reply_in_thread,
    }
```

## Why Patches Get Overwritten

The openclaw-lark plugin is installed via npm (`@larksuite/openclaw-lark`). Running
`openclaw update` or upgrading the plugin replaces all files in:
```
~/.openclaw/extensions/openclaw-lark/
```

The live-card watcher is a local skill and won't be overwritten unless manually replaced.

## Config Note

The `replyMode` config field (`channels.feishu.replyMode`) only accepts `auto | static | streaming`.
It controls **rendering mode** (plain text vs streaming card), NOT reply placement.
Setting `replyMode: "thread"` is an **invalid value** that gets silently ignored.
