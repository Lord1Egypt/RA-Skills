# Skill: Email MCP (email-mcp-helper)

## Overview
This skill provides access to a self-hosted email MCP server built on `@codefuturist/email-mcp`. It exposes 47 tools covering full email lifecycle management — reading, searching, sending, replying, forwarding, scheduling, folder management, labels, bulk operations, threading, attachments, analytics, and health checks — across multiple IMAP/SMTP accounts simultaneously.

This skill is a **tool reference only**. It does not define how the agent should handle, triage, or respond to emails — that is defined in a separate email management skill that depends on this one as a prerequisite.

Clawhub will mark this as a risk because its tools for email that doesnt tell the agent how to use them and because it provides a link to the actual email mcp server this skill was made to help your agent understand how to use.  It makes no sense to lock the actual email handling skill down to a single mcp email tool - the skills dont belong together so Clawhub wil always mark this package dangerous.  All Clawhub really does is get users used to acccepting security risks without looking because they label everything a security risk, many times without even citing why. Use at your own risk, or dont use it, I dont care, its for me and I share - and I am tired of fighting clawhub who clearly doesnt care about the actual security risk they create by desensitizing people to security ratings that make no sense, lack evidence, misfire fire over ridiculous things, say there isa virus finding while total virus says there is none, and in general overall, cause most users to ignore them.  You should be having your agent always check any skill before installing & using it to make sure it isnt siphoning data, running actual real commands that could compromise your system and or otherwise maintain skills aligned with the overarching skill set. Dont rely on Clawhub, DYOR always!
---

## Infrastructure Notes

This MCP server runs as a standalone docker or Kubernetes deployment **separate from the OpenClaw container**. It is NOT bundled with or managed by OpenClaw. You must setup this MCP server yourself, have your agent help you.

**Source code:** https://github.com/codefuturist/email-mcp

**Key infrastructure requirements (outside this skill's scope):**
- The `email-mcp` image (`ghcr.io/codefuturist/email-mcp:latest`) is stdio-only — it has no built-in HTTP server
- A **MCP proxy** (e.g. `sparfenyuk/mcp-proxy`) must be installed alongside it to expose the server over HTTP/SSE — without the proxy the server cannot be reached over a network
- Accounts are configured via a `config.toml` file mounted into the container — credentials are managed outside this skill
- The proxy and server are deployed together in a single custom Docker image

**This skill assumes the server is already running and reachable. If the server is unreachable, this skill cannot function.**

---

## Connection

| Property | Value |
|----------|-------|
| URL | `https://mcp-server-addres.com/mcp` |
| Transport | SSE |
| Auth | API key via `X-API-Key` header (managed by infrastructure) |

---

## Configured Accounts

Accounts are configured server-side. Always call `list_accounts` to get the current account names — never hardcode them. The `account` parameter in every tool must match the exact name returned by `list_accounts`.

---

## Prerequisites Before Using Any Tool

1. Call `list_accounts` to get valid account names
2. Call `list_mailboxes(account)` before any operation involving folder paths — paths are provider-specific and must be exact

---

## Rules

- The `account` parameter is always the account **name** (e.g. `shawnroy`), never the email address
- `emailId` is the IMAP UID string — always obtained from `list_emails` or `search_emails`, never guessed
- `mailbox` must be an exact path from `list_mailboxes` — never guess folder names
- `get_email` and `get_emails` are **non-destructive by default** — they use IMAP PEEK and do NOT mark emails as read unless `markRead: true` is explicitly set
- `delete_email` moves to Trash by default — only set `permanent: true` when explicitly instructed
- `find_email_folder` must be used before `move_email` or `delete_email` when the email was discovered via a virtual folder (e.g. Gmail "All Mail")
- Never call `delete_mailbox` without explicit user instruction — it is irreversible and destroys all contents

---

## Tools Reference

### Account & Health

#### `list_accounts`
List all configured email accounts and their names.
- No parameters required
- Returns: account names, email addresses, provider info

#### `list_mailboxes`
List all folders for an account with unread counts and special-use flags.
- `account` (string, required) — account name from `list_accounts`
- Returns: folder paths, total messages, unread counts, special-use flags (Inbox, Sent, Trash, etc.)

#### `check_health`
Check IMAP/SMTP connection health, latency, quota, and server capabilities.
- `account` (string, required)

---

### Reading Email

#### `list_emails`
Paginated email list with metadata. Returns read/unread 🔵, flagged ⭐, replied ↩️, attachment 📎, and label 🏷️ indicators.
- `account` (string, required)
- `mailbox` (string, default: `INBOX`)
- `page` (int, default: 1)
- `pageSize` (int, default: 20, max: 100)
- `since` (ISO 8601 string, optional) — emails after this date
- `before` (ISO 8601 string, optional) — emails before this date
- `from` (string, optional) — filter by sender
- `subject` (string, optional) — filter by subject keyword
- `seen` (boolean, optional) — `true` = read only, `false` = unread only
- `flagged` (boolean, optional) — `true` = flagged only
- `has_attachment` (boolean, optional)
- `answered` (boolean, optional) — `true` = replied, `false` = not yet replied

#### `get_email`
Full content of a single email. Non-destructive by default (IMAP PEEK).
- `account` (string, required)
- `emailId` (string, required) — UID from `list_emails`
- `mailbox` (string, default: `INBOX`)
- `format` (enum, default: `full`) — `full` = raw, `text` = plain text (strips HTML), `stripped` = plain text without quoted replies or signatures
- `maxLength` (int, optional) — truncate body at this many characters
- `markRead` (boolean, default: `false`) — set `true` to explicitly mark as read

#### `get_emails`
Fetch full content of up to 20 emails in a single call. More efficient than looping `get_email`. Non-destructive.
- `account` (string, required)
- `ids` (array of strings, required, max 20) — UIDs from `list_emails`
- `mailbox` (string, default: `INBOX`)
- `format` (enum, default: `text`) — same options as `get_email`
- `maxLength` (int, optional)

#### `get_email_status`
Read/flag/label state only — no body fetched. Very cheap, use when you only need to check state.
- `account` (string, required)
- `emailId` (string, required)
- `mailbox` (string, default: `INBOX`)

#### `search_emails`
Search by keyword across subject, sender, and body with optional filters. Omit `query` to use as a pure filter.
- `account` (string, required)
- `query` (string, optional) — keyword search
- `mailbox` (string, default: `INBOX`)
- `page` (int, default: 1)
- `pageSize` (int, default: 20, max: 100)
- `to` (string, optional) — filter by recipient
- `has_attachment` (boolean, optional)
- `larger_than` (number, optional) — minimum size in KB
- `smaller_than` (number, optional) — maximum size in KB
- `answered` (boolean, optional)

#### `get_thread`
Reconstruct a full conversation thread via References/In-Reply-To headers.
- `account` (string, required)
- `emailId` (string, required) — any email in the thread

#### `find_email_folder`
Discover which real folder(s) an email actually lives in. Required before `move_email` or `delete_email` when email was found via a virtual folder.
- `account` (string, required)
- `emailId` (string, required)

#### `extract_contacts`
Extract unique contacts from recent email headers.
- `account` (string, required)
- `mailbox` (string, optional)
- `limit` (int, optional)

#### `get_email_stats`
Email analytics — volume, top senders, daily trends.
- `account` (string, required)

#### `download_attachment`
Download a specific email attachment.
- `account` (string, required)
- `emailId` (string, required)
- `mailbox` (string, default: `INBOX`)
- `filename` (string, required) — exact filename from `get_email` attachment metadata

---

### Sending Email

#### `send_email`
Send a new email. Plain text or HTML.
- `account` (string, required)
- `to` (array of email strings, required, min 1)
- `subject` (string, required)
- `body` (string, required)
- `cc` (array of email strings, optional)
- `bcc` (array of email strings, optional)
- `html` (boolean, default: `false`) — set `true` to send as HTML

#### `reply_email`
Reply with proper threading (In-Reply-To & References headers). Call `get_email` first to read the original.
- `account` (string, required)
- `emailId` (string, required) — email to reply to
- `mailbox` (string, default: `INBOX`)
- `body` (string, required)
- `replyAll` (boolean, default: `false`)
- `html` (boolean, default: `false`)

#### `forward_email`
Forward with original content quoted below.
- `account` (string, required)
- `emailId` (string, required)
- `mailbox` (string, default: `INBOX`)
- `to` (array of email strings, required)
- `body` (string, optional) — additional message above forwarded content
- `cc` (array of email strings, optional)

#### `save_draft`
Save email to Drafts without sending.
- `account` (string, required)
- `to` (array of email strings, optional)
- `subject` (string, optional)
- `body` (string, optional)
- `html` (boolean, default: `false`)

#### `send_draft`
Send an existing draft and remove it from Drafts.
- `account` (string, required)
- `emailId` (string, required) — draft email ID

#### `schedule_email`
Schedule an email for future delivery.
- `account` (string, required)
- `to` (array of email strings, required)
- `subject` (string, required)
- `body` (string, required)
- `sendAt` (ISO 8601 string, required) — scheduled send time

#### `list_scheduled`
List scheduled emails by status.
- `account` (string, required)
- `status` (enum, optional) — `pending`, `sent`, `failed`

#### `cancel_scheduled`
Cancel a pending scheduled email.
- `account` (string, required)
- `emailId` (string, required)

---

### Managing Email

#### `move_email`
Move email to a different folder. Source must be a real folder — use `find_email_folder` first if discovered via a virtual folder.
- `account` (string, required)
- `emailId` (string, required)
- `sourceMailbox` (string, required) — current folder
- `destinationMailbox` (string, required) — target folder (verify with `list_mailboxes`)

#### `delete_email`
Delete an email. Moves to Trash by default.
- `account` (string, required)
- `emailId` (string, required)
- `mailbox` (string, default: `INBOX`)
- `permanent` (boolean, default: `false`) — ⚠️ set `true` only when explicitly instructed — irreversible

#### `mark_email`
Change email flags.
- `account` (string, required)
- `id` (string, required) — email UID
- `mailbox` (string, default: `INBOX`)
- `action` (enum, required) — `read`, `unread`, `flag`, `unflag`

#### `bulk_action`
Batch operation on up to 100 emails.
- `account` (string, required)
- `ids` (array of strings, required, max 100)
- `action` (enum, required) — `move`, `delete`, `read`, `unread`, `flag`, `unflag`
- `destinationMailbox` (string) — required when action is `move`

---

### Folders

#### `create_mailbox`
Create a new folder. Use `/` for nested folders.
- `account` (string, required)
- `path` (string, required) — e.g. `Archive/2026` or `Projects`

#### `rename_mailbox`
Rename an existing folder.
- `account` (string, required)
- `path` (string, required) — current path
- `new_path` (string, required) — new path

#### `delete_mailbox`
⚠️ Permanently delete a folder and ALL its contents. Irreversible.
- `account` (string, required)
- `path` (string, required)

---

### Labels

#### `list_labels`
Discover available labels. Provider-aware — handles Gmail, ProtonMail, and standard IMAP keywords differently.
- `account` (string, required)

#### `add_label`
Add a label to an email.
- `account` (string, required)
- `emailId` (string, required)
- `mailbox` (string, required)
- `label` (string, required)

#### `remove_label`
Remove a label from an email.
- `account` (string, required)
- `emailId` (string, required)
- `mailbox` (string, required)
- `label` (string, required)

#### `create_label`
Create a new label.
- `account` (string, required)
- `name` (string, required)

#### `delete_label`
Delete a label.
- `account` (string, required)
- `name` (string, required)

---

### Templates

#### `list_templates`
List available email templates.
- `account` (string, required)

#### `apply_template`
Apply a template with variable substitution and send or save as draft.
- `account` (string, required)
- `templateName` (string, required)
- `variables` (object, optional) — key/value pairs for substitution
- `to` (array of email strings, optional) — required to send, optional for draft
- `action` (enum, default: `draft`) — `send` or `draft`

---

### Analytics & Contacts

#### `get_email_stats`
Email analytics — volume, top senders, daily trends.
- `account` (string, required)

#### `extract_contacts`
Extract unique contacts from recent email headers.
- `account` (string, required)
- `mailbox` (string, optional)
- `limit` (int, optional)

---

## Common Call Sequences

### List unread inbox emails
```
list_accounts()
→ list_emails(account, mailbox="INBOX", seen=false, pageSize=20)
```

### Read a specific email
```
list_emails(account, mailbox="INBOX")
→ get_email(account, emailId, format="stripped")
```

### Reply to an email
```
list_emails(account) → get emailId
→ get_email(account, emailId) → read content
→ reply_email(account, emailId, body="...", replyAll=false)
```

### Send a new email
```
send_email(account, to=["someone@example.com"], subject="...", body="...")
```

### Move email to folder
```
list_mailboxes(account) → verify destination path
→ move_email(account, emailId, sourceMailbox="INBOX", destinationMailbox="Archive")
```

### Search with filters
```
search_emails(account, query="invoice", has_attachment=true, mailbox="INBOX")
```

### Batch read for triage
```
list_emails(account, seen=false, pageSize=20) → collect ids
→ get_emails(account, ids=[...], format="stripped")
```
