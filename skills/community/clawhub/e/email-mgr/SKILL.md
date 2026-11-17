---
name: email-manager
description: Read, search, compose, and manage email. Inbox, search, compose, threading, status. JSON-based email store. Zero external dependencies.
---

# Email Manager 📧

**Stop checking email manually. Start managing it through the agent.**

## The Problem

Email is the #1 source of important information the agent misses. No integration means no awareness of deadlines, alerts, or messages that need action.

Email Manager provides the foundation for email integration with local JSON storage.

## ⚠️ Important Warnings

### Plaintext Email Storage
Emails imported or composed via Email Manager are stored in plaintext JSON under `memory/email/emails.json`. This includes sender, recipient, subject, body, and all metadata. Anyone with filesystem access can read the full contents.

### SMTP Credentials in settings.json
SMTP credentials (username, password) for outbound sending are stored in plaintext in `memory/email/settings.json`. Treat this file as sensitive as a password manager.

### Irreversible Outbound Sending
`--send` dispatches email via SMTP. Once sent, email delivery cannot be recalled. Always review the recipient, subject, and body before confirming. The `--dry-run` flag previews without sending.

## Quick Start

### Show inbox

```bash
node skills/email-manager/email-manager.js --inbox
```

Shows last 10 emails. Add count: `--inbox 20`

### Show unread emails

```bash
node skills/email-manager/email-manager.js --inbox --unread
```

### Search emails

```bash
node skills/email-manager/email-manager.js --search "project deadline"
```

Searches from, to, subject, and body.

### Compose a draft

```bash
node skills/email-manager/email-manager.js --compose james@example.com "Meeting Notes" "Here are the notes..."
```

### Send immediately

```bash
node skills/email-manager/email-manager.js --compose --send james@example.com "Meeting Notes" "Here are the notes..."
```

### View email thread

```bash
node skills/email-manager/email-manager.js --thread thread-id-123
```

### Mark as read

```bash
node skills/email-manager/email-manager.js --inbox --read email-id
```

### Delete email

```bash
node skills/email-manager/email-manager.js --inbox --delete email-id
```

### Status overview

```bash
node skills/email-manager/email-manager.js --status
```

## Features

### Inbox Management

- Sorted by date (newest first)
- Unread filtering
- Preview snippets (first 80 chars)
- Read/unread status tracking

### Search

- Searches from, to, subject, and body
- Case-insensitive matching
- Returns up to 20 results

### Compose & Send

- Draft mode (saves to emails.json)
- Send mode (would integrate with SMTP/API)
- Configurable sender address

### Thread View

- Groups messages by thread ID
- Chronological ordering
- Shows full message history

### Status Tracking

- Total email count
- Unread count with warning
- Draft and sent counts

## Configuration

Data files stored in: `memory/email/`

- `emails.json` — Email storage (inbox, drafts, sent)
- `settings.json` — Sender address and preferences

Override data directory:
```bash
--dir /path/to/data
```

## Agent Protocol

For email-aware operations:

1. **Check inbox** — `--inbox` during heartbeats for urgent items
2. **Search proactively** — `--search` for keywords related to active projects
3. **Compose drafts** — `--compose` for email drafts, review before sending
4. **Send with confirmation** — `--compose --send` requires user approval
5. **Thread context** — `--thread` for ongoing email conversations

## Integration Notes

- Email store is JSON-based (local only)
- SMTP/API integration required for real email delivery
- Add email integration by connecting to IMAP/SMTP or an email API (Gmail API, SendGrid, etc.)
- Settings file configures sender address

## Heartbeat Integration

Add to your `HEARTBEAT.md`:

```markdown
### 📧 Email Check

- Run `node skills/email-manager/email-manager.js --inbox --unread`
- Only alert if urgent emails detected (look for "urgent", "deadline", "action required")
```

## Security Notes

- Emails stored as plain JSON — ensure file permissions are restrictive
- Sender address in settings.json — protect this file
- No email content encryption (add if needed for sensitive data)

## Comparison

| Approach | Inbox | Search | Compose | Threading |
|----------|-------|--------|---------|-----------|
| Manual | ✅ | ✅ | ✅ | ✅ |
| Email Client | ✅ | ✅ | ✅ | ✅ |
| **Email Manager** | **✅** | **✅** | **✅** | **✅** |

**Email Manager gives you inbox + search + compose + threading with zero external dependencies.**

## Design Principles

1. **Zero setup** — Works immediately, no config needed
2. **No dependencies** — Pure Node.js, no npm packages
3. **Extensible** — JSON store makes integration straightforward
4. **Transparent** — Everything is visible in the JSON store
5. **Agent-first** — Designed for agent-driven email workflows
