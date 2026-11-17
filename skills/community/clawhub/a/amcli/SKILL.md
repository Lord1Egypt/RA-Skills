---
name: amcli
description: Read and send Apple Messages (iMessage, SMS) from the command line on macOS. List chats with unread counts, read a conversation, search all messages, and send, with JSON output for agent use.
author: gopaljigaur
license: MIT
platform: macOS
requires:
  binaries: [amcli]
  install: "npm install -g @gopaljigaur/amcli"
tags: [messages, imessage, sms, macos, apple]
---

# amcli: Apple Messages CLI

`amcli` reads `~/Library/Messages/chat.db` read-only and sends through Messages.app. Every command takes `--json`. Exit codes: 0 success, 1 runtime error, 2 validation error, 10 Full Disk Access missing.

**First run:** reading needs Full Disk Access for the terminal app (System Settings > Privacy & Security > Full Disk Access). On `NOT_AUTHORIZED`, tell the user to grant it; do not try to work around it.

## Chats

```bash
amcli chats [--unread] [--limit <n>] [--json]
```

Newest first. Each chat has `id`, `guid`, `name`, `identifier`, `service`, `group`, `participants`, `lastMessageAt`, `unread`.

## Show a chat

```bash
amcli show <chat> [--limit <n>] [--since <when>] [--json]
```

`<chat>` is the chat `id`, its `guid`, or the phone or email it is keyed on. Returns `{ chat, messages }`, the newest `limit` messages (default 20) in chronological order.

## Search

```bash
amcli search <text> [--chat <chat>] [--since <when>] [--limit <n>] [--json]
```

Case-insensitive substring match, newest first. Each message adds `chat` (the chat name).

## Send

```bash
amcli send --to <phone|email|chat guid> [text] [--service sms] [--dry-run] [-y] [--json]
```

Text comes from the argument or stdin. Asks for confirmation; without a terminal it refuses unless `-y`. `--dry-run` returns `{ dryRun: true, wouldSend }` and sends nothing.

## Message fields

`id`, `guid`, `chatId`, `date` (ISO 8601), `fromMe`, `sender` (handle, null when from me), `service`, `text`, `attachments` (file names).

## --since

`YYYY-MM-DD`, an ISO datetime, or relative: `30m`, `12h`, `7d`.

## Agent Best Practices

- Always use `--json`, and check `ok: false` before proceeding
- Never send without the user's explicit go-ahead for that exact text and recipient; show a `--dry-run` first
- Read the least needed: `--limit` and `--since` keep private conversations out of context
- Use the chat `guid` from `amcli chats` to reply into a group
- Names are not resolved from Contacts; use `apcli search` to map a handle to a person
- macOS only

## Error Codes

| Code | Meaning |
|------|---------|
| `NOT_AUTHORIZED` | Terminal lacks Full Disk Access |
| `NO_DATABASE` | No Messages database on this Mac |
| `CHAT_NOT_FOUND` | No chat matches the id, guid or handle |
| `SEND_FAILED` | Messages.app refused the send |
| `MISSING_REQUIRED` | Required argument missing, or `--yes` needed without a terminal |
| `INVALID_ARGUMENT` | Invalid flag value |
