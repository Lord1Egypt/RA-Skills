# email-suite (imap+smtp)

A professional email CLI with **local caching** for lightning-fast inbox checks. Unified `mail.js` command for AI agents — outputs Markdown tables that are easy to parse and integrate.

## What Makes This Stand Out

| Feature | Others | This Suite |
|---------|--------|------------|
| Inbox check | 3-7s every time | **~0.2s** from cache |
| Search | 5+ seconds | **~0.2s** from cache |
| Output format | ANSI colors | **Markdown tables** |
| New message detection | Manual refresh | **Auto-detected** on sync |
| Attachments | Where downloaded? | **`.cache/attachments/`** |
| Search filters | Basic | **Multi-filter AND logic** |
| Time/date filters | None | **`--since 7d`, `--before date`** |
| Agent guidance | None | **Action hints after each email** |
| Reply/Forward | None | **`mail.js reply <uid>`** |
| Email stats | None | **`mail.js stats`** |

## What It Does

This is a standard **IMAP/SMTP email client** - the same protocol that Thunderbird, Outlook, and all email apps use.

```
.env credentials  →  IMAP server (receive emails)
.env credentials  →  SMTP server (send emails)
IMAP server      →  Local disk (download attachments)
Local disk       →  SMTP server (send attachments)
```

**Exactly like:** Thunderbird, Outlook, Apple Mail - just CLI-based with caching for AI agents.

## Quick Start

```bash
# Run setup (checks dependencies, installs packages, creates .env)
bash setup.sh

# Or manual setup:
npm install
cp .env.example.txt .env   # Edit with your credentials

# First sync
node scripts/mail.js check     # View inbox
node scripts/mail.js --help    # Show all commands
```

### Setup Script

The `setup.sh` script will:
1. Check for Node.js and npm
2. Install npm dependencies
3. Prompt for your email provider (Gmail, Outlook, Hostinger, Custom)
4. Create `.env` with your credentials
5. Optionally configure display name and email signature
6. Test IMAP and SMTP connections

```bash
bash setup.sh
```

**Provider presets:**
- **Gmail** - Requires App Password (2FA must be enabled)
- **Outlook** - Requires App Password
- **Hostinger** - Uses your email password
- **Custom** - Enter your own IMAP/SMTP settings

**Gmail Setup:** Enable 2FA, then generate an App Password at [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

## Features

### Speed - Local Caching
- **Inbox check: ~0.2s** (vs 3-7s without cache)
- **Search: ~0.2s** (vs 5s+ server search)
- Cache syncs in background, results are instant

### Agent-Friendly Output
- Markdown tables - easy to parse
- Clear status indicators (📎 attachments, `unread` flags)
- Actionable command hints after reading each email

### Time/Date Search
```bash
mail.js search --since 7d              # Last 7 days
mail.js search --since 1m              # Last month
mail.js search --before 2026-03-01    # Before date
mail.js search --from "paypal" --since 30d
mail.js search --since 2026-03-01 --before 2026-03-15  # Range
```

### Unified Command
```bash
node scripts/mail.js check           # Inbox
node scripts/mail.js fetch <uid>    # Read
node scripts/mail.js search --from x # Search
node scripts/mail.js send --to x     # Send
```
(Old commands still work: `node scripts/imap.js check`, `node scripts/smtp.js send`)

### Organized Storage
- Attachments auto-saved to `.cache/attachments/`
- Inbox cache in `.cache/inbox.json`
- Clear cache anytime with `clear-cache`

### Professional Email
- **Markdown to HTML** - write emails in markdown, send as styled HTML
- **Automatic signatures** - HTML and plain text
- **Display names** - "Your Company" instead of raw email
- **Multiple attachments** - with proper MIME types

## Mail Commands

```bash
# Inbox
node scripts/mail.js check                   # Fast, from cache
node scripts/mail.js check --all            # Show all messages
node scripts/mail.js sync                   # Check server for new messages

# Read
node scripts/mail.js fetch <uid>

# Search (fast from cache)
node scripts/mail.js search --from "sender"
node scripts/mail.js search --subject "invoice"
node scripts/mail.js search --to "boss@company.com"
node scripts/mail.js search --unseen         # Unread only
node scripts/mail.js search --server         # Server search (slower)

# Time/Date filters
node scripts/mail.js search --since 7d
node scripts/mail.js search --before 2026-03-01
node scripts/mail.js search --from "paypal" --since 30d

# Manage
node scripts/mail.js mark-read <uid> [uid2...] # Multiple IDs supported
node scripts/mail.js seen <uid>              # Alias: mark as read
node scripts/mail.js mark-unread <uid>
node scripts/mail.js unseen <uid>            # Alias: mark as unread
node scripts/mail.js delete <uid> [uid2...]  # Delete (alias: del) — multiple IDs supported
node scripts/mail.js download <uid>          # Download attachments
node scripts/mail.js list-mailboxes          # Show all folders
```

#### Agent Action Hints
After reading an email, the CLI shows **actionable commands** for the agent:
```
## Email #352
...email content...

```bash
# Download attachment:
node scripts/mail.js download 352
# Mark as read:
node scripts/mail.js seen 352
# Delete email:
node scripts/mail.js delete 352
```
```

## SMTP Commands

```bash
node scripts/mail.js test                            # Test connection
node scripts/mail.js send --to a@b.com --subject "Hello" --body "World"

# Markdown emails (auto-converted to HTML)
node scripts/mail.js send --to a@b.com --subject "Report" --body-file report.md

# Attachments
node scripts/mail.js send --to a@b.com --attach file.pdf --attach image.jpg
```

## Configuration

```bash
# .env (copy and edit these values)

# IMAP (receiving emails)
IMAP_HOST=imap.gmail.com
IMAP_PORT=993
IMAP_USER=your@gmail.com
IMAP_PASS=app_password
IMAP_TLS=true
IMAP_REJECT_UNAUTHORIZED=true      # Set false for self-signed certs
IMAP_MAILBOX=INBOX

# SMTP (sending emails)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false                   # true for port 465, false for 587
SMTP_USER=your@gmail.com
SMTP_PASS=app_password
SMTP_FROM=your@gmail.com            # Default sender (optional)
SMTP_REJECT_UNAUTHORIZED=true       # Set false for self-signed certs

# Display name shown to recipients
FROM_NAME="Your Name"

# Email signatures (optional)
EMAIL_SIGNATURE="<p><br>--<br><strong>Your Name</strong><br><a href='mailto:you@email.com'>you@email.com</a></p>"
EMAIL_SIGNATURE_TEXT="--\nYour Name\nyou@email.com"
```

## Gmail Setup

Gmail requires **App Password** (not your regular password):

1. Enable 2-Step Verification
2. [Generate App Password](https://myaccount.google.com/apppasswords)
3. Use the 16-char password in `IMAP_PASS` and `SMTP_PASS`

## Security

- **Never commit `.env`** - contains credentials
- **Use App Passwords** for Gmail/2FA accounts
- **Permissions:** `chmod 600 .env`

## Architecture

```
scripts/
├── mail.js              # Unified entry point (preferred)
└── utils/
    ├── index.js         # Re-exports all utils
    ├── args.js          # parseArgs()
    ├── format.js        # formatDate(), printMessagesTable(), etc.
    ├── env.js           # dotenv loading
    ├── mail.js          # Command dispatcher
    ├── imap.js          # IMAP handler exports
    └── smtp.js          # SMTP handler exports
.cache/
  inbox.json           # Local cache
  attachments/          # Downloaded attachments
.env                   # Credentials (not committed)
```

## Performance

| Action | Without Cache | With Cache |
|--------|---------------|------------|
| `check` | 3-7s | **0.2s** |
| `search` | 5s | **0.2s** |
| `fetch` | 1-2s | 1-2s (server) |


clawhub update email-suite-imap-smtp --no-input