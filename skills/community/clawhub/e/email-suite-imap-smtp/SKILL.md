# email-suite

Email CLI: `node scripts/mail.js <cmd>`. Works with Gmail, Outlook, Hostinger, any IMAP/SMTP server.

## Setup

### Automated (recommended)
```bash
bash setup.sh
```
Runs: Node.js check → npm install → provider menu → credentials → display name → signature → summary → connection test

### Manual
```bash
npm install
cp env.example.txt .env   # Edit with your credentials
```

## .env Configuration

### Required
```bash
# IMAP (receiving)
IMAP_HOST=imap.gmail.com
IMAP_PORT=993
IMAP_USER=your@email.com
IMAP_PASS=your_app_password

# SMTP (sending)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_SECURE=false          # true for port 465, false for 587
SMTP_USER=your@email.com
SMTP_PASS=your_app_password
```

### Optional
```bash
SMTP_FROM=your@email.com  # Default sender
FROM_NAME="Your Name"      # Display name shown to recipients
IMAP_REJECT_UNAUTHORIZED=false  # For self-signed certs
SMTP_REJECT_UNAUTHORIZED=false  # For self-signed certs
```

### Provider Presets
| Provider | IMAP Host | Port | SMTP Host | Port | Secure |
|----------|-----------|------|-----------|------|--------|
| Gmail | imap.gmail.com | 993 | smtp.gmail.com | 587 | false |
| Outlook | outlook.office365.com | 993 | smtp.office365.com | 587 | false |
| Hostinger | imap.hostinger.com | 993 | smtp.hostinger.com | 465 | true |

### Gmail/Outlook: Use App Password
Not your regular password — generate a 16-char App Password:
- Gmail: [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
- Outlook: Account → Security → App passwords

## Essential Commands

| Command | Description |
|---------|-------------|
| `check` | Inbox from cache (~0.2s). Shows sync time. `--all` for read+unread combined. |
| `sync` | Fetch NEW messages only. Updates cache. |
| `fetch <uid>` | Read email. Shows action hints. Marks as read, updates cache. |
| `send --to x --subject "S" --body "B"` | Send email |
| `search --from "x" --since 7d` | Search cache. `--server` for full search. |
| `delete <uid>` | Delete permanently |

## Flags
- `--all` — All messages (read + unread, combined chronological)
- `--limit N` — Limit results
- `--since 7d` — Time filter (7d, 1m, YYYY-MM-DD)
- `--before YYYY-MM-DD` — Before date

## Multi-ID
```bash
delete <uid1> <uid2>   # Delete multiple
mark-read <uid1> <uid2> # Mark multiple read
```

## Send Options
- `--body-file x.md` — Markdown auto-converted to HTML
- `--attach file.pdf` — Attachments
- `reply <uid> --body "T"` — Reply (auto Re: prefix)
- `forward <uid> --to x` — Forward

## Cache
- `.cache/inbox.json` — Local cache for fast checks
- `sync` = incremental (new msgs only)
- `fetch` = always server, marks read, updates cache
- `delete` / `clear-cache` = clears cache

## Security
- Never commit `.env` to git
- `chmod 600 .env` to protect credentials
- Use App Passwords for Gmail/Outlook (2FA required)