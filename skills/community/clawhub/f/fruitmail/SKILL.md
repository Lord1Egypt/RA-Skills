---
name: apple-mail-search
description: "Fast Apple Mail search via SQLite on macOS. Search emails by subject, sender, date, body, threads, attachments — results in ~50ms vs 8+ minutes with AppleScript. Use when asked to find, search, read, or list emails."
metadata:
  openclaw:
    emoji: "📬"
    os:
      - darwin
    requires:
      bins:
        - sqlite3
        - python3
---

# Apple Mail Search

Search Apple Mail.app emails instantly via SQLite. **~50ms** vs 8+ minutes with AppleScript.

## Why This Exists

Apple Mail's AppleScript bridge enumerates every message object in memory before doing anything. At 100K+ emails, it just hangs — indefinitely. This has been broken for years and Apple hasn't fixed it.

| Method | Time for 110K emails |
|--------|---------------------|
| AppleScript iteration | Hangs forever |
| Spotlight/mdfind | Broken since Big Sur (emlx importer removed) |
| **SQLite (this tool)** | **~50ms** |

## Setup

Follow the instructions in `references/install.md` to install the `mail-search` script to your PATH. The script source is embedded there for portability.

Requires Full Disk Access for Terminal/shell to read `~/Library/Mail/`.

## Usage

```bash
mail-search subject "invoice"              # Search subjects
mail-search sender "@amazon.com"           # Search by sender email
mail-search from "John"                    # Search by sender display name
mail-search to "recipient@example.com"     # Search sent mail
mail-search unread                         # List unread emails
mail-search recent 7                       # Last 7 days
mail-search date-range 2025-01-01 2025-01-31  # Date range
mail-search attachments                    # Emails with attachments
mail-search thread 12345                   # Full conversation thread
mail-search body 12345                     # Read email body text
mail-search open 12345                     # Open email in Mail.app
mail-search stats                          # Database statistics
```

## Options

```
-n, --limit N    Max results (default: 20)
-j, --json       Output as JSON
-c, --csv        Output as CSV
-q, --quiet      No headers
--db PATH        Override database path
--no-copy        Query live DB (faster, slight risk if Mail.app writes simultaneously)
```

## Examples

```bash
# Morning inbox check — unread as JSON for cron processing
mail-search unread --json | jq '.[].subject'

# Find supplier emails
mail-search sender "@example.com" -n 50

# Read the actual email body
mail-search body 116519

# Thread view — see full conversation
mail-search thread 116519

# Export last month to CSV
mail-search date-range 2026-02-01 2026-02-28 --csv > feb_emails.csv

# Quick stats
mail-search stats
```

## How It Works

Queries Mail.app's internal `Envelope Index` SQLite database directly at:
```
~/Library/Mail/V{9,10,11}/MailData/Envelope Index
```

**Safety:** By default, copies the DB to a temp file before querying so there's no risk of corruption while Mail.app is running. Use `--no-copy` to skip this if you need raw speed.

**Epoch detection:** Auto-detects whether your DB uses Unix epoch or Apple CoreData epoch (offset by 978307200 seconds). Works correctly on both.

**Body reading:** The `body` command finds the `.emlx` file on disk and extracts plain text (falls back to stripped HTML). Requires `python3`.

## Key Tables

- `messages` — Email metadata (dates, flags, read status, foreign keys)
- `subjects` — Subject lines
- `addresses` — Email addresses and display names
- `recipients` — TO/CC/BCC mappings
- `attachments` — Attachment filenames and types
- `mailboxes` — Folder/mailbox structure

## Limitations

- **Read-only** — cannot compose or send (use AppleScript for that; single-message sends work fine)
- **Metadata + body** — bodies require the `.emlx` file to exist on disk (may be purged by Mail.app for old messages)
- **Apple Mail only** — doesn't read Outlook, Spark, etc.
- **macOS only** — requires `~/Library/Mail/` directory structure

## Advanced: Raw SQL

For custom queries beyond what the CLI offers:

```bash
sqlite3 -header -column ~/Library/Mail/V10/MailData/Envelope\ Index "
SELECT m.ROWID, s.subject, a.address,
       datetime(m.date_sent, 'unixepoch') as date
FROM messages m
JOIN subjects s ON m.subject = s.ROWID
LEFT JOIN addresses a ON m.sender = a.ROWID
WHERE s.subject LIKE '%your query%'
ORDER BY m.date_sent DESC
LIMIT 20;
"
```

## Credits

Inspired by [steipete](https://github.com/steipete)'s original apple-mail-search concept and [tyler6204](https://github.com/tyler6204)'s safe-copy approach. This version adds body reading, thread support, epoch auto-detection, sent mail search, and bundles the actual executable script.

## License

MIT
