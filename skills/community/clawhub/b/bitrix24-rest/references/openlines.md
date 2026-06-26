# Open Lines (Открытые линии)

Use this file for Bitrix24 Open Lines — omnichannel customer communication (website chat, Telegram, WhatsApp, Facebook, VK, etc.). Open Lines connect external messaging channels to the portal and route incoming conversations to operators.

Scope: `imopenlines`. All methods require this scope in the webhook.

## Core Concepts

- **Line (config)** — an Open Line configuration: name, CRM binding, auto-actions, queue of operators
- **Session** — one conversation between a customer and operator(s), from first message to close
- **Operator** — a portal user who answers customer messages
- **Dialog** — the chat between operator and customer within a session
- **Connector** — external channel (Telegram, WhatsApp, Viber, Facebook, website widget, etc.)

## Line Management

### List all lines

```bash
python3 scripts/bitrix24_call.py imopenlines.config.list.get --json
```

With filter and queue info:

```bash
python3 scripts/bitrix24_call.py imopenlines.config.list.get \
  --param 'PARAMS[filter][ACTIVE]=Y' \
  --param 'PARAMS[select][]=ID' \
  --param 'PARAMS[select][]=LINE_NAME' \
  --param 'PARAMS[select][]=ACTIVE' \
  --param 'PARAMS[select][]=CRM' \
  --param 'OPTIONS[QUEUE]=Y' \
  --json
```

Supports pagination (`next`, `total`). Fields available for select/filter/order: see `imopenlines.config.add` docs.

### Get line by ID

```bash
python3 scripts/bitrix24_call.py imopenlines.config.get \
  --param 'CONFIG_ID=1' \
  --param 'WITH_QUEUE=Y' \
  --param 'SHOW_OFFLINE=Y' \
  --json
```

- `CONFIG_ID` (required) — line ID
- `WITH_QUEUE` — include operator queue (Y/N, default Y)
- `SHOW_OFFLINE` — include offline operators (Y/N, default Y)

### Create a line

```bash
python3 scripts/bitrix24_call.py imopenlines.config.add \
  --param 'PARAMS[LINE_NAME]=Support' \
  --json
```

Key fields in `PARAMS`: `LINE_NAME`, `CRM` (Y/N), `CRM_CREATE` (lead creation mode), `ACTIVE` (Y/N), and many others. Check MCP for full field list.

### Update a line

```bash
python3 scripts/bitrix24_call.py imopenlines.config.update \
  --param 'CONFIG_ID=1' \
  --param 'PARAMS[LINE_NAME]=New Name' \
  --param 'PARAMS[CRM]=Y' \
  --json
```

- `CONFIG_ID` (required) — line ID
- `PARAMS` — same fields as `imopenlines.config.add`

### Delete a line

```bash
python3 scripts/bitrix24_call.py imopenlines.config.delete \
  --param 'CONFIG_ID=1' \
  --json
```

### Get public page URL

```bash
python3 scripts/bitrix24_call.py imopenlines.config.path.get --json
```

Returns the URL of the portal's public Open Lines page.

## Operator Actions

Operators manage conversations via `CHAT_ID` — the chat identifier for the dialog.

### Accept a dialog

```bash
python3 scripts/bitrix24_call.py imopenlines.operator.answer \
  --param 'CHAT_ID=2024' \
  --json
```

Current operator takes the dialog.

### Skip a dialog

```bash
python3 scripts/bitrix24_call.py imopenlines.operator.skip \
  --param 'CHAT_ID=2024' \
  --json
```

Current operator skips — dialog goes back to queue.

### Transfer a dialog

```bash
python3 scripts/bitrix24_call.py imopenlines.operator.transfer \
  --param 'CHAT_ID=2024' \
  --param 'TRANSFER_ID=5' \
  --json
```

- `TRANSFER_ID` — user ID to transfer to an operator, OR `queue<LINE_ID>` to transfer to another line (e.g., `queue3`)

### Finish a dialog (own)

```bash
python3 scripts/bitrix24_call.py imopenlines.operator.finish \
  --param 'CHAT_ID=2024' \
  --json
```

### Finish another operator's dialog

```bash
python3 scripts/bitrix24_call.py imopenlines.operator.another.finish \
  --param 'CHAT_ID=2024' \
  --json
```

Errors: `ACCESS_DENIED`, `CHAT_TYPE` (not an open line), `CHAT_ID` (invalid).

### Intercept a dialog

```bash
python3 scripts/bitrix24_call.py imopenlines.session.intercept \
  --param 'CHAT_ID=2024' \
  --json
```

Current operator takes over a dialog that already has another operator.

## Session Management

### Start a session

```bash
python3 scripts/bitrix24_call.py imopenlines.session.start \
  --param 'CHAT_ID=2024' \
  --json
```

### Pin/unpin dialog to operator

```bash
# Pin
python3 scripts/bitrix24_call.py imopenlines.session.mode.pin \
  --param 'CHAT_ID=2024' \
  --param 'ACTIVATE=Y' \
  --json

# Unpin
python3 scripts/bitrix24_call.py imopenlines.session.mode.pin \
  --param 'CHAT_ID=2024' \
  --param 'ACTIVATE=N' \
  --json
```

### Pin/unpin all dialogs

```bash
# Pin all
python3 scripts/bitrix24_call.py imopenlines.session.mode.pinAll --json

# Unpin all
python3 scripts/bitrix24_call.py imopenlines.session.mode.unpinAll --json
```

Returns array of affected session IDs.

### Get session history

```bash
python3 scripts/bitrix24_call.py imopenlines.session.history.get \
  --param 'CHAT_ID=1982' \
  --param 'SESSION_ID=469' \
  --json
```

Returns full conversation: messages, users, chat metadata. Both `CHAT_ID` and `SESSION_ID` are required.

Response includes: `chatId`, `sessionId`, `message` (dict of messages), `users` (participants), `chat` (chat metadata with `entityType: LINES`).

## Dialog Info

```bash
python3 scripts/bitrix24_call.py imopenlines.dialog.get \
  --param 'CHAT_ID=2024' \
  --json
```

Can query by any ONE of: `CHAT_ID`, `DIALOG_ID` (e.g., `chat29`), `SESSION_ID`, or `USER_CODE` (e.g., `livechat|1|1373|211`).

Returns: dialog name, color, avatar, owner, `entity_type`, `entity_id`, `manager_list`, `date_create`, `message_type` (`L` = lines).

## Messaging

### Send message from Open Line to user

```bash
python3 scripts/bitrix24_call.py imopenlines.network.message.add \
  --param 'CODE=ab515f5d85a8b844d484f6ea75a2e494' \
  --param 'USER_ID=2' \
  --param 'MESSAGE=Hello from support' \
  --json
```

- `CODE` (required) — Open Line code (hash string from connector settings)
- `USER_ID` (required) — recipient user ID
- `MESSAGE` (required) — text with formatting support
- `ATTACH` — attachment object (max 30 KB)
- `KEYBOARD` — interactive keyboard (max 30 KB)
- `URL_PREVIEW` — Y/N, default Y

### Send message in CRM entity chat

```bash
python3 scripts/bitrix24_call.py imopenlines.crm.message.add \
  --param 'CRM_ENTITY_TYPE=deal' \
  --param 'CRM_ENTITY=288' \
  --param 'USER_ID=12' \
  --param 'CHAT_ID=8773' \
  --param 'MESSAGE=Follow-up message' \
  --json
```

- `CRM_ENTITY_TYPE` — `lead`, `deal`, `company`, `contact`
- `CRM_ENTITY` — CRM entity ID
- `USER_ID` — user or bot to add to chat
- `CHAT_ID` — chat ID
- `MESSAGE` — text

## CRM Integration

### Create lead from dialog

```bash
python3 scripts/bitrix24_call.py imopenlines.crm.lead.create \
  --param 'CHAT_ID=1988' \
  --json
```

Creates a CRM lead based on the dialog. Returns `true` on success.

## Network (External Lines)

### Join external Open Line

```bash
python3 scripts/bitrix24_call.py imopenlines.network.join \
  --param 'CODE=ab515f5d85a8b844d484f6ea75a2e494' \
  --json
```

Connects an external Open Line to the portal. Returns bot ID on success.

## Bot Integration

### Send auto-message from bot

```bash
python3 scripts/bitrix24_call.py imopenlines.bot.session.message.send \
  --param 'CHAT_ID=2' \
  --param 'MESSAGE=Welcome to our support' \
  --param 'NAME=WELCOME' \
  --json
```

- `NAME` — message type: `WELCOME` (greeting) or `DEFAULT` (regular)

## API Revision

```bash
python3 scripts/bitrix24_call.py imopenlines.revision.get --json
```

Returns current API revision numbers for REST, web, and mobile clients.

## Method Reference

### Line config
| Method | Description |
|--------|-------------|
| `imopenlines.config.list.get` | List all lines (with filter/select/order) |
| `imopenlines.config.get` | Get line by ID (with operator queue) |
| `imopenlines.config.add` | Create a new line |
| `imopenlines.config.update` | Update line settings |
| `imopenlines.config.delete` | Delete a line |
| `imopenlines.config.path.get` | Get public page URL |

### Operators
| Method | Description |
|--------|-------------|
| `imopenlines.operator.answer` | Accept dialog |
| `imopenlines.operator.skip` | Skip dialog (back to queue) |
| `imopenlines.operator.transfer` | Transfer to operator or line |
| `imopenlines.operator.finish` | Close own dialog |
| `imopenlines.operator.another.finish` | Close another operator's dialog |

### Sessions
| Method | Description |
|--------|-------------|
| `imopenlines.session.start` | Start a session |
| `imopenlines.session.intercept` | Take over dialog from another operator |
| `imopenlines.session.mode.pin` | Pin/unpin dialog to current operator |
| `imopenlines.session.mode.pinAll` | Pin all dialogs to current operator |
| `imopenlines.session.mode.unpinAll` | Unpin all dialogs from current operator |
| `imopenlines.session.history.get` | Get session conversation history |
| `imopenlines.session.join` | Join a session |
| `imopenlines.session.open` | Get chat ID by USER_CODE |
| `imopenlines.message.session.start` | Start session with message transfer |

### Dialog & messaging
| Method | Description |
|--------|-------------|
| `imopenlines.dialog.get` | Get dialog info (by CHAT_ID, DIALOG_ID, SESSION_ID, or USER_CODE) |
| `imopenlines.network.message.add` | Send message from Open Line to user |
| `imopenlines.crm.message.add` | Send message in CRM entity chat |
| `imopenlines.crm.lead.create` | Create CRM lead from dialog |

### Network & bot
| Method | Description |
|--------|-------------|
| `imopenlines.network.join` | Connect external Open Line to portal |
| `imopenlines.bot.session.message.send` | Send auto-message from bot |
| `imopenlines.bot.session.operator` | Switch to free operator |
| `imopenlines.bot.session.transfer` | Switch to specific operator |
| `imopenlines.bot.session.finish` | End current session (bot) |
| `imopenlines.revision.get` | Get API revision info |

## Known Limitations

- Open Lines require the `imopenlines` scope — standard `im` scope is not enough
- `imopenlines.network.message.add` requires the line's CODE (hash), not the line ID
- Attachment and keyboard objects are limited to 30 KB each
- Session history (`imopenlines.session.history.get`) requires both CHAT_ID and SESSION_ID
- There is no method to list all active sessions across all lines — you work with individual chats

For the latest API updates, check the MCP documentation server (`https://mcp-dev.bitrix24.tech/mcp`) using `bitrix-search` with queries like `imopenlines session`, `imopenlines operator`.

## Good MCP Queries

- `imopenlines config`
- `imopenlines operator transfer`
- `imopenlines session history`
- `imopenlines dialog get`
- `imopenlines crm message`
- `imopenlines network message`
- `imopenlines bot session`
