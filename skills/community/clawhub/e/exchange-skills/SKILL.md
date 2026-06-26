---
name: exchange-skills
description: "Full email, calendar, contacts, tasks, and notes management for Microsoft Exchange/Outlook. Use when Claude needs to list unread emails, read email content, reply to emails, mark emails as read, archive emails, view calendar events, search contacts, manage tasks, or access notes. Supports batch operations for external/internal emails. Triggers: check my email, unread emails, reply to email, archive external emails, mark as read, calendar, schedule, 行程, contacts, tasks, notes."
metadata:
  openclaw:
    requires:
      env:
        - EXCHANGE_SERVER
        - EXCHANGE_EMAIL
        - EXCHANGE_USERNAME
        - EXCHANGE_PASSWORD
      optional_env:
        - EXCHANGE_DOMAIN
    primaryEnv: EXCHANGE_PASSWORD
---

# Exchange Mail

Manage Microsoft Exchange/Outlook emails and calendar from terminal.

## Script Location

`scripts/exchange_mail.py` - Main CLI script

## Commands

```bash
# List unread (today, where you're To/CC)
python3 scripts/exchange_mail.py list

# List options
python3 scripts/exchange_mail.py list --days 3    # Last 3 days
python3 scripts/exchange_mail.py list --all       # All unread
python3 scripts/exchange_mail.py list --json      # JSON output

# Read email
python3 scripts/exchange_mail.py read <id>

# Reply
python3 scripts/exchange_mail.py reply <id> "Your message"

# Mark as read
python3 scripts/exchange_mail.py mark-read <id>
python3 scripts/exchange_mail.py mark-read --external
python3 scripts/exchange_mail.py mark-read --internal
python3 scripts/exchange_mail.py mark-read --all

# Archive
python3 scripts/exchange_mail.py archive <id>
python3 scripts/exchange_mail.py archive --external
python3 scripts/exchange_mail.py archive --internal --days 7

# Calendar (NEW!)
python3 scripts/exchange_mail.py calendar                 # Next 7 days
python3 scripts/exchange_mail.py calendar --today        # Today only
python3 scripts/exchange_mail.py calendar --days 30     # Next 30 days
python3 scripts/exchange_mail.py calendar --json        # JSON output

# Contacts (NEW!)
python3 scripts/exchange_mail.py contacts "name"         # Search contacts
python3 scripts/exchange_mail.py contacts "name" --limit 10  # Limit results
python3 scripts/exchange_mail.py contacts "name" --json  # JSON output

# Tasks (NEW!)
python3 scripts/exchange_mail.py tasks                  # List tasks
python3 scripts/exchange_mail.py tasks --days 30       # Next 30 days
python3 scripts/exchange_mail.py tasks --status pending  # Filter by status

# Notes (NEW!)
python3 scripts/exchange_mail.py notes                 # List notes
python3 scripts/exchange_mail.py notes --limit 10      # Limit results
```

**Note:** 
- Contact search requires access to Exchange contact folders. If no contacts are found, check folder permissions on the Exchange server.
- Tasks and Notes require the corresponding folders to exist in the Exchange account.

## Email IDs

Each email gets stable 8-char hex ID (e.g., `b7bc8d99`). Use for all commands.

## Output Format

```
📧 9 unread emails today:

━━━ Internal (4) ━━━
[b7bc8d99] [13:57] John Smith
        Re: Project Discussion

━━━ External (5) ━━━
[43e56cc9] [09:50] newsletter@company.com
        Weekly Update
```

## Batch Flags

- `--external` - Only external emails (outside your domain)
- `--internal` - Only internal emails (your domain)
- `--all` - All emails
- `--days N` - Look back N days (default: today only)

## Environment Variables

Required in shell config:
```bash
export EXCHANGE_SERVER="mail.company.com"
export EXCHANGE_EMAIL="user@company.com"
export EXCHANGE_USERNAME="username"
export EXCHANGE_PASSWORD="password"
```

Optional:
```bash
export EXCHANGE_DOMAIN="domain"  # Windows domain if required
export EXCHANGE_DISABLE_SSL_VERIFY=1  # Only if you need to disable SSL verification (not recommended)
```

**Note**: The script will also load environment variables from a `.env` file in the script directory (`skills/exchange-skills/scripts/.env`) if it exists.

## Workflow Examples

```bash
# Morning: check → read → reply → archive spam
python3 scripts/exchange_mail.py list
python3 scripts/exchange_mail.py read abc123
python3 scripts/exchange_mail.py reply abc123 "Thanks!"
python3 scripts/exchange_mail.py archive --external

# Weekly cleanup
python3 scripts/exchange_mail.py archive --external --days 7
```
