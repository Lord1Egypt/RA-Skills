# Email Manager 📧

**Read, search, compose, and manage email — right from your terminal. Inbox, search, compose, threading, status.**

## Why Email Manager?

Email doesn't leave your system. No API keys, no cloud dependencies, no privacy risks. Email Manager works with a local JSON-based email store — test it, script it, integrate it.

- **Fully local** — JSON-backed, zero external API calls, zero network dependencies
- **Fast** — Reads and writes happen in milliseconds, not network round-trips
- **Testable** — Every operation is testable: create, read, search, thread, compose
- **Portable** — Your data is plain JSON. Migrate, version-control, or inspect it freely
- **Terminal-native** — Full CLI, no GUI needed. Script it, cron it, pipe it

---

## Installation

```bash
# Already included in OpenClaw workspace at skills/email-manager/
# No npm install needed — pure Node.js
```

---

## Quick Start

```bash
# List inbox
node skills/email-manager/email-manager.js --inbox

# Search emails
node skills/email-manager/email-manager.js --search "meeting notes"

# Compose a draft
node skills/email-manager/email-manager.js --compose

# Thread view
node skills/email-manager/email-manager.js --thread <thread-id>

# Show mailbox status
node skills/email-manager/email-manager.js --status
```

Default location: `memory/email/` under the workspace root. Override with `EMAIL_DIR`.

---

## Commands Reference

### Inbox

```bash
node skills/email-manager/email-manager.js --inbox
```

Lists emails in the inbox. Shows sender, subject, date, and read/unread status.

```
[email-manager] Inbox (3 unread of 14):
  [1] 📬 alice@co → Project update    2026-07-15
  [2] 📬 bob@co   → Meeting tomorrow   2026-07-16
  [3] 📖 Carol    → Build fix          2026-07-14
```

### Search

```bash
node skills/email-manager/email-manager.js --search <query>
```

Searches email body, subject, and sender. Supports partial and case-insensitive matching.

### Compose

```bash
node skills/email-manager/email-manager.js --compose
```

Interactive mode for composing a new email. Follow the prompts:
1. Enter recipient(s)
2. Enter subject
3. Enter message body
4. Review and confirm

### Thread

```bash
node skills/email-manager/email-manager.js --thread <thread-id>
```

Shows all messages in a thread, ordered chronologically.

### Status

```bash
node skills/email-manager/email-manager.js --status
```

```
[email-manager] Status:
  Total emails: 14
  Unread: 3
  Drafts: 1
  Threads: 8
```

---

## Programmatic API

```javascript
const EM = require('./skills/email-manager/email-manager.js');

// Initialize with a data directory
const store = EM.init('/path/to/email-store');

// Access operations
const inbox = EM.getInbox(store);
const results = EM.search(store, 'query');
const thread = EM.getThread(store, 'thread-id');
const status = EM.getStatus(store);
```

All operations work against a JSON-backed store. The store auto-saves on every mutation.

---

## Data Format

Emails are stored as JSON at `memory/email/emails.json`:

```json
{
  "emails": [
    {
      "id": "email_1",
      "threadId": "thread_1",
      "from": "alice@example.com",
      "to": "you@example.com",
      "subject": "Project update",
      "body": "The API is ready for review...",
      "date": "2026-07-15T10:30:00.000Z",
      "read": true,
      "draft": false
    }
  ]
}
```

Settings at `memory/email/settings.json`:
```json
{
  "sender": "you@example.com"
}
```

---

## Security

| Protection | Status |
|------------|--------|
| **No network access** | ✅ Fully local JSON store |
| **No shell injection** | ✅ Uses Node.js child_process with array args |
| **No external deps** | ✅ Zero npm dependencies |
| **No eval** | ✅ No dynamic code execution |
| **Path validation** | ✅ Email store confined to configured directory |

Email Manager uses `execSync` for CLI operations but passes all arguments through proper escaping. The data directory is isolated to `EMAIL_DIR` or the default `memory/email/` path.

---

## Testing

```bash
# Run full test suite (14 tests)
node skills/email-manager/tests/test-email-manager.js
```

Test coverage:
- **Inbox operations** — listing, filtering, read status
- **Search** — by sender, subject, body content
- **Compose** — draft creation, output formatting
- **Threads** — thread grouping, chronological order
- **Status** — counts, unread stats
- **Error handling** — missing threads, missing emails

---

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `EMAIL_DIR` | Override email store directory |

### Default Paths

| Resource | Path |
|----------|------|
| Email store | `<WORKSPACE>/memory/email/emails.json` |
| Settings | `<WORKSPACE>/memory/email/settings.json` |

---

## Examples

### Quick Email Search
```bash
# Find all emails about "deploy"
node skills/email-manager/email-manager.js --search deploy

# Find emails from a specific sender
node skills/email-manager/email-manager.js --search "alice@"
```

### Create a Draft
```bash
node skills/email-manager/email-manager.js --compose
```

### Check How Many Unread
```bash
node skills/email-manager/email-manager.js --status | grep Unread
```

### Pipe Search Results
```bash
node skills/email-manager/email-manager.js --search "urgent" | grep "subject" | wc -l
```

---

## License

MIT — Part of the OpenClaw skill ecosystem.

---

## Related Skills

- **Notification Triage** — Smart notification filtering and batching
- **Research Assistant** — Knowledge building and entity extraction
- **Secrets Manager** — Secure credential storage for email auth
