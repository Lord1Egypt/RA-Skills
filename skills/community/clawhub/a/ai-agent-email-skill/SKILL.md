---
name: aaes
description: This skill provides script-based email operations for an agent. It includes functionalities for managing mailboxes, reading/searching emails, sending/replying/forwarding emails, and managing attachments, allowing agents to perform comprehensive email-related tasks programmatically.
metadata:
  openclaw:
    requires:
      env:
        - EMAIL_PASSWORD
        - EMAIL_USERNAME
      config:
        - ./scripts/config.toml
    primaryEnv: EMAIL_PASSWORD
---

# AI Agent Email Skill (aaes)

## Overview

This skill provides script-based email operations for an agent. It includes functionalities for managing mailboxes, reading/searching emails, sending/replying/forwarding emails, and managing attachments, allowing agents to perform comprehensive email-related tasks programmatically.

## Features

- **IMAP operations**: Read, list, mark, move, delete, copy emails
- **SMTP operations**: Send, reply, forward emails with attachments
- **Folder management**: Create, delete, rename, list mailboxes
- **Dual-format bodies**: Supports both plain-text and HTML, with automatic fallback generation
- **Attachment handling**: Supports base64-encoded attachments
- **Multi-account support**: Configure multiple accounts
- **Authentication**: Password or OAuth2 via environment variables (auto-detected)
- **Signatures**: Automatic signature appending to outgoing emails
- **Thread support**: Proper In-Reply-To and References header handling

## When to use

Use this skill when you need an agent to:

- Check inbox for new emails and summarize them
- Read specific emails and extract content
- Send new emails with attachments
- Reply to or forward emails
- Organize emails by moving/copying between folders
- Create or manage mailbox folders
- Mark emails as read/unread, flagged, spam, or junk

## Requirements

- Python 3.14+
- IMAP/SMTP access to your email provider
- Network access to email servers

## Configuration

### Basic Setup

Configure this skill with `./scripts/config.toml`:

1. Copy `./config.default.toml` to `./scripts/config.toml`.
2. Edit `./scripts/config.toml` - fill in email address and server addresses.

### Authentication Setup

Only one authentication method is required, configured via environment variables. 

**Password-based authentication**

| Variable         | Description                           |
| ---------------- | ------------------------------------- |
| `EMAIL_USERNAME` | Login username (required)             |
| `EMAIL_PASSWORD` | User password or app password         |

```bash
# Linux/Mac
export EMAIL_USERNAME="me"
export EMAIL_PASSWORD="my-password"

# Windows (PowerShell)
$env:EMAIL_USERNAME="me"
$env:EMAIL_PASSWORD="my-password"

# Windows (CMD)
set EMAIL_USERNAME=me
set EMAIL_PASSWORD=my-password
```

**OAuth2 authentication**

| Variable                     | Description               |
| ---------------------------- | ------------------------- |
| `EMAIL_OAUTH2_CLIENT_ID`     | OAuth2 client ID          |
| `EMAIL_OAUTH2_CLIENT_SECRET` | OAuth2 client secret      |
| `EMAIL_OAUTH2_REFRESH_TOKEN` | OAuth2 refresh token      |
| `EMAIL_OAUTH2_TOKEN_URL`     | OAuth2 token endpoint URL |

```bash
# Linux/Mac
export EMAIL_OAUTH2_CLIENT_ID="xxx"
export EMAIL_OAUTH2_CLIENT_SECRET="xxx"
export EMAIL_OAUTH2_REFRESH_TOKEN="xxx"
export EMAIL_OAUTH2_TOKEN_URL="https://oauth2.example.com/token"

# Windows (PowerShell)
$env:EMAIL_OAUTH2_CLIENT_ID="xxx"
$env:EMAIL_OAUTH2_CLIENT_SECRET="xxx"
$env:EMAIL_OAUTH2_REFRESH_TOKEN="xxx"
$env:EMAIL_OAUTH2_TOKEN_URL="https://oauth2.example.com/token"

# Windows (CMD)
set EMAIL_OAUTH2_CLIENT_ID=xxx
set EMAIL_OAUTH2_CLIENT_SECRET=xxx
set EMAIL_OAUTH2_REFRESH_TOKEN=xxx
set EMAIL_OAUTH2_TOKEN_URL="https://oauth2.example.com/token"
```

### Test

```bash
# Linux/Mac
echo '{"requestId":"test","schemaVersion":"1.0","data":{"maxResults":5}}' | python3 scripts/mail_list.py

# Windows (PowerShell)
echo '{"requestId":"test","schemaVersion":"1.0","data":{"maxResults":5}}' | python scripts/mail_list.py

# Windows (CMD)
echo "{\"requestId\":\"test\",\"schemaVersion\":\"1.0\",\"data\":{\"maxResults\":5}}" | python scripts/mail_list.py
```

## Data Exchange Contract

### Overview

All scripts follow the same JSON-over-stdin contract:

1. Agent sends one JSON object to stdin
2. Script writes one JSON object to stdout
3. Logs and diagnostics are written to stderr

### Request Schema

```json
{
  "requestId": "optional-trace-id",
  "schemaVersion": "1.0",
  "account": "optional-account-name-in-config",
  "data": {}
}
```

### Success Response Schema

```json
{
  "ok": true,
  "requestId": "same-as-request",
  "schemaVersion": "1.0",
  "data": {}
}
```

### Error Response Schema

```json
{
  "ok": false,
  "requestId": "same-as-request",
  "schemaVersion": "1.0",
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {}
  }
}
```

| Error Code             | Description                            |
| ---------------------- | -------------------------------------- |
| `VALIDATION_ERROR`     | Invalid input data or parameters       |
| `CONFIG_ERROR`         | Configuration file missing or invalid  |
| `AUTH_ERROR`           | Authentication failed                  |
| `NETWORK_ERROR`        | Network connection failed              |
| `MAIL_OPERATION_ERROR` | IMAP/SMTP operation failed             |
| `MAILBOX_ERROR`        | Mailbox selection or management failed |
| `INTERNAL_ERROR`       | Unexpected internal error              |

## Scripts

### `folder_create.py`

Create mailbox folder.

| Request fields |                  |
| -------------- | ---------------- |
| `name`         | string, required |

| Response fields |                     |
| --------------- | ------------------- |
| `account`       | Account name used   |
| `name`          | Folder name created |
| `created`       | `true` on success   |

### `folder_delete.py`

Delete mailbox folder.

| Request fields |                  |
| -------------- | ---------------- |
| `name`         | string, required |

| Response fields |                     |
| --------------- | ------------------- |
| `account`       | Account name used   |
| `name`          | Folder name deleted |
| `deleted`       | `true` on success   |

### `folder_list.py`

List mailbox folders.

| Request fields |     |
| -------------- | --- |
| (none)         |     |

| Response fields |                         |
| --------------- | ----------------------- |
| `account`       | Account name used       |
| `mailboxes`     | Array of folder objects |

### `folder_rename.py`

Rename mailbox folder.

| Request fields |                  |
| -------------- | ---------------- |
| `oldName`      | string, required |
| `newName`      | string, required |

| Response fields |                      |
| --------------- | -------------------- |
| `account`       | Account name used    |
| `oldName`       | Original folder name |
| `newName`       | New folder name      |
| `renamed`       | `true` on success    |

### `mail_copy.py`

Copy email(s) between folders.

| Request fields |                                    |
| -------------- | ---------------------------------- |
| `uids`         | string[] or comma-separated string |
| `sourceFolder` | optional, default `INBOX`          |
| `targetFolder` | required                           |

| Response fields |                   |
| --------------- | ----------------- |
| `account`       | Account name used |
| `uids`          | UIDs copied       |
| `sourceFolder`  | Source folder     |
| `targetFolder`  | Target folder     |
| `copied`        | `true` on success |

### `mail_delete.py`

Delete email(s).

| Request fields |                                    |
| -------------- | ---------------------------------- |
| `uids`         | string[] or comma-separated string |
| `folder`       | optional, default `INBOX`          |
| `expunge`      | boolean, default `false`           |

| Response fields |                        |
| --------------- | ---------------------- |
| `account`       | Account name used      |
| `uids`          | UIDs deleted           |
| `folder`        | Folder name            |
| `deleted`       | `true` on success      |
| `expunged`      | `true` if hard deleted |

### `mail_forward.py`

Forward email with optional additions.

| Request fields |                                          |
| -------------- | ---------------------------------------- |
| `uid`          | string, required                         |
| `folder`       | optional, default `INBOX`                |
| `to`           | string or string[], required             |
| `cc`           | optional                                 |
| `bcc`          | optional                                 |
| `bodyText`     | optional, prepended to forwarded content |
| `bodyHtml`     | optional                                 |
| `attachments`  | optional                                 |

| Response fields |                    |
| --------------- | ------------------ |
| `account`       | Account name used  |
| `forwarded`     | `true` on success  |
| `uid`           | Original email UID |
| `to`            | Recipients         |
| `cc`            | CC recipients      |
| `subject`       | Forwarded subject  |

Automatically includes original email and attachments.

### `mail_mark.py`

Mark email(s) with flags.

| Request fields |                                                                                    |
| -------------- | ---------------------------------------------------------------------------------- |
| `uids`         | string[] or comma-separated string, required                                       |
| `markType`     | `read`, `unread`, `flag`, `unflag`, `spam`, `notspam`, `junk`, `notjunk`, required |
| `folder`       | optional, default `INBOX`                                                          |

| Response fields |                   |
| --------------- | ----------------- |
| `account`       | Account name used |
| `uids`          | UIDs marked       |
| `markType`      | Mark type applied |
| `marked`        | `true` on success |

### `mail_move.py`

Move email(s) between folders.

| Request fields |                                    |
| -------------- | ---------------------------------- |
| `uids`         | string[] or comma-separated string |
| `sourceFolder` | optional, default `INBOX`          |
| `targetFolder` | required                           |

| Response fields |                   |
| --------------- | ----------------- |
| `account`       | Account name used |
| `uids`          | UIDs moved        |
| `sourceFolder`  | Source folder     |
| `targetFolder`  | Target folder     |
| `moved`         | `true` on success |

### `mail_read.py`

Read email content and metadata.

| Request fields |                           |
| -------------- | ------------------------- |
| `uid`          | string, required          |
| `folder`       | optional, default `INBOX` |

| Response fields |                           |
| --------------- | ------------------------- |
| `account`       | Account name used         |
| `uid`           | Email UID                 |
| `subject`       | Email subject             |
| `from`          | Sender                    |
| `to`            | Recipients                |
| `cc`            | CC recipients             |
| `date`          | Email date                |
| `bodyText`      | Plain text body           |
| `bodyHtml`      | HTML body                 |
| `attachments`   | Attachment list           |
| `tags`          | Combined flags and labels |

Marks message as read after fetch.

### `mail_reply.py`

Reply to email.

| Request fields |                           |
| -------------- | ------------------------- |
| `uid`          | string, required          |
| `folder`       | optional, default `INBOX` |
| `bodyText`     | optional                  |
| `bodyHtml`     | optional                  |
| `replyAll`     | boolean, default `false`  |
| `priority`     | `high`, `normal`, `low`   |
| `attachments`  | optional                  |

| Response fields   |                                          |
| ----------------- | ---------------------------------------- |
| `account`         | Account name used                        |
| `uid`             | Original email UID                       |
| `folder`          | Original email folder                    |
| `sent`            | `true` on success                        |
| `to`              | Reply recipients                         |
| `cc`              | CC recipients                            |
| `attachmentCount` | Number of attachments                    |
| `priority`        | Priority level (`high`, `normal`, `low`) |
| `readReceipt`     | `true` if read receipt requested         |
| `inReplyTo`       | In-Reply-To message ID                   |
| `references`      | References header value                  |
| `subject`         | Reply subject                            |

### `mail_list.py`

List emails using IMAP search.

| Request fields |                            |
| -------------- | -------------------------- |
| `query`        | optional, default `UNSEEN` |
| `folder`       | optional, default `INBOX`  |
| `maxResults`   | optional, default `10`     |

| Response fields |                        |
| --------------- | ---------------------- |
| `account`       | Account name used      |
| `folder`        | Folder searched        |
| `query`         | Search query           |
| `uids`          | Matching UIDs          |
| `count`         | Results returned       |
| `totalCount`    | Total matches          |
| `hasMore`       | More results available |
| `summary`       | Email summaries        |

| Query                   | Description      |
| ----------------------- | ---------------- |
| `UNSEEN`                | Unread messages  |
| `FROM user@example.com` | From sender      |
| `SUBJECT "keyword"`     | Subject contains |
| `SINCE 2024-01-01`      | Since date       |
| `ALL`                   | All messages     |

### `mail_send.py`

Send new email.

| Request fields |                              |
| -------------- | ---------------------------- |
| `to`           | string or string[], required |
| `subject`      | string, required             |
| `bodyText`     | optional                     |
| `bodyHtml`     | optional                     |
| `cc`           | optional                     |
| `bcc`          | optional                     |
| `priority`     | `high`, `normal`, `low`      |
| `attachments`  | optional                     |

| Response fields   |                                          |
| ----------------- | ---------------------------------------- |
| `account`         | Account name used                        |
| `sent`            | `true` on success                        |
| `to`              | Recipients                               |
| `cc`              | CC recipients                            |
| `bccCount`        | Number of BCC recipients                 |
| `attachmentCount` | Number of attachments                    |
| `priority`        | Priority level (`high`, `normal`, `low`) |
| `readReceipt`     | `true` if read receipt requested         |
| `inReplyTo`       | In-Reply-To message ID                   |
| `references`      | References header value                  |
| `subject`         | Sent subject                             |

## Examples

### List new emails

```bash
echo '{"requestId":"test","schemaVersion":"1.0","data":{"maxResults":10}}' | python3 scripts/mail_list.py
```

### Read email by UID

```json
{ "requestId": "read", "schemaVersion": "1.0", "data": { "uid": "123" } }
```

### List from sender

```json
{
  "requestId": "search",
  "schemaVersion": "1.0",
  "data": { "query": "FROM boss@example.com" }
}
```

### Send email

```json
{
  "requestId": "send",
  "schemaVersion": "1.0",
  "data": {
    "to": ["user@example.com"],
    "subject": "Hello",
    "bodyText": "Hello world!"
  }
}
```

### Reply to email

```json
{
  "requestId": "reply",
  "schemaVersion": "1.0",
  "data": { "uid": "123", "bodyText": "Thanks!" }
}
```

### Mark and move

```json
{"requestId":"mark","schemaVersion":"1.0","data":{"uids":"123","markType":"read"}}
{"requestId":"move","schemaVersion":"1.0","data":{"uids":"123","targetFolder":"Archive"}}
```

## Troubleshooting

### AUTH_ERROR

- If password auth: Ensure both `EMAIL_USERNAME` and `EMAIL_PASSWORD` are set
- If OAuth2 auth: All four variables required: `EMAIL_OAUTH2_CLIENT_ID`, `EMAIL_OAUTH2_CLIENT_SECRET`, `EMAIL_OAUTH2_REFRESH_TOKEN`, `EMAIL_OAUTH2_TOKEN_URL`
- For 2FA accounts, use app password for `EMAIL_PASSWORD`
- OAuth2 takes priority if all four `EMAIL_OAUTH2_*` variables are set

### NETWORK_ERROR

- Verify IMAP port 993 (SSL) or 143 (STARTTLS)
- Verify SMTP port 465 (SSL) or 587 (STARTTLS)
- Check firewall settings

### CONFIG_ERROR

- Ensure `config.toml` exists and is valid TOML
- Check `email`, `imap.host`, `smtp.host` are configured

### Security Warnings

⚠️ **SSL Verification**: Setting `ssl_verify = false` in config disables certificate validation and exposes connections to man-in-the-middle attacks. Only disable for local development/testing.

⚠️ **IMAP Injection Protection**: User-provided search queries are validated against a whitelist of safe commands. Custom queries containing `()";` characters will be rejected.

### Debugging

Check stderr for detailed error logs with `code`, `message`, and `details`.
