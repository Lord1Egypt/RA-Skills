# Chat and Notifications

Use this file for messenger dialogs, chats, history, notifications, and file delivery into chats.

> **Important:** The methods below (`im.message.add`, `im.disk.file.commit`, etc.) are for managing chats on behalf of the webhook user — e.g., sending a message to an employee or posting a file to a group chat. Do **not** use them to reply to the user in the current conversation. Replies and file delivery to the user are handled automatically by the channel plugin.

> **Channels** (каналы / объявления) — see `references/channels.md`. Channels use the same `im.*` methods but with `ENTITY_TYPE=ANNOUNCEMENT` and `type: openChannel`.

## Separate `im.*` From `imbot.*`

Use `im.*` for normal IM REST methods (webhook-compatible):

- `im.message.add` — send message
- `im.message.update` / `im.message.delete`
- `im.message.share` — create entity (task/event/post) from a message
- `im.chat.add` / `im.chat.get` / `im.chat.update`
- `im.chat.user.add` / `im.chat.user.delete` / `im.chat.user.list`
- `im.dialog.get` / `im.dialog.messages.get`
- `im.dialog.messages.search` — search messages in a specific chat
- `im.dialog.users.list` — list dialog participants
- `im.dialog.read.all` — mark all chats as read
- `im.recent.list` / `im.recent.get`
- `im.dialog.writing` — typing indicator

Use `imbot.*` for bot scenarios (requires `CLIENT_ID`):

- `imbot.message.add` / `imbot.message.update` / `imbot.message.delete`
- `imbot.chat.add` / `imbot.dialog.get`
- `imbot.chat.sendTyping`

Do not mix `im.*` and `imbot.*` — pick the family that matches the integration.

## Notifications

- `im.notify.system.add` — system notification (app context only)
- `im.notify.personal.add` — personal notification (app context only)
- `im.notify.read` — mark notification as read

Important: `im.notify.system.add` and `im.notify.personal.add` work only through an application, not plain webhooks. If you get auth errors, this is likely the reason.

## Dialog Addressing

- `123` — direct dialog with user 123
- `chat456` — group chat 456
- `sg789` — group or project chat

## Common Use Cases

### Send a message to a chat

```bash
python3 scripts/bitrix24_call.py im.message.add \
  --param 'DIALOG_ID=chat42' \
  --param 'MESSAGE=Hello team' \
  --json
```

### Read dialog history

```bash
python3 scripts/bitrix24_call.py im.dialog.messages.get \
  --param 'DIALOG_ID=chat42' \
  --param 'LIMIT=20' \
  --json
```

### Send a Disk file to another chat

Use this to send a file to a specific chat on behalf of the webhook user (not for replying to the current conversation — the channel plugin handles that automatically).

```bash
python3 scripts/bitrix24_call.py im.disk.file.commit \
  --param 'CHAT_ID=42' \
  --param 'FILE_ID[]=5249' \
  --param 'MESSAGE=Project files' \
  --json
```

### Create a group chat

```bash
python3 scripts/bitrix24_call.py im.chat.add \
  --param 'TYPE=CHAT' \
  --param 'TITLE=Project discussion' \
  --param 'USERS[]=1' \
  --param 'USERS[]=2' \
  --json
```

### Search messages in a chat

```bash
python3 scripts/bitrix24_call.py im.dialog.messages.search \
  --param 'CHAT_ID=42' \
  --param 'SEARCH_MESSAGE=contract' \
  --param 'LIMIT=20' \
  --json
```

Supports date filters: `DATE_FROM`, `DATE_TO` (ISO 8601), `DATE` (single day).
Search string must be longer than 2 characters. Returns messages, users, and files.

### Create task from a chat message

```bash
python3 scripts/bitrix24_call.py im.message.share \
  --param 'MESSAGE_ID=34261' \
  --param 'DIALOG_ID=chat42' \
  --param 'TYPE=TASK' \
  --json
```

`TYPE` values: `TASK` (task), `CALEND` (calendar event), `POST` (feed post), `CHAT` (forward to chat).
Get `MESSAGE_ID` from `im.dialog.messages.get` or `im.dialog.messages.search`.

### Mark all chats as read

```bash
python3 scripts/bitrix24_call.py im.dialog.read.all --json
```

No parameters needed. Marks all dialogs as read for the current user.

## `CLIENT_ID` for Bots

For `imbot.*` methods:

- Provide `CLIENT_ID` when registering the bot
- Persist it and reuse in every `imbot.*` call
- Treat `CLIENT_ID` as a secret

## Formatting

Bitrix24 chat uses BB-code. Do not double-convert if Markdown is already converted to BB-code.

## Good MCP Queries

- `im message add chat`
- `im message share`
- `im dialog messages search`
- `im dialog read all`
- `imbot message`
- `im dialog messages get`
- `im disk file commit`
