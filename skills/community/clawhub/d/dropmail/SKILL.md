---
name: dropmail
description: Manage disposable email addresses using GuerrillaMail. Use when a user wants to create a temporary/throwaway email address, check a disposable inbox for messages, or avoid sharing their real email with untrusted services. Triggers on phrases like "temp email", "disposable email", "temporary email", "throwaway email", "create a burner email", or any dropmail command.
---

# DropMail Skill

Create and manage disposable email addresses via GuerrillaMail API. Emails expire after 60 minutes. All data is stored locally in SQLite at `~/.dropmail/dropmail.db`.

## Installation

Create a symlink to `dropmail.py` on your PATH:

```bash
# System-wide
ln -s <skill-dir>/scripts/dropmail.py /usr/local/bin/dropmail

# User-local
ln -s <skill-dir>/scripts/dropmail.py ~/.local/bin/dropmail
```

Data is stored at `~/.dropmail/` (auto-created on first run). Requires Python 3.7+, no extra dependencies.

## Commands

```
dropmail new                            # Get a new disposable email
dropmail list                           # List all tracked emails with expiry status
dropmail <email> inbox                  # Show all messages in inbox
dropmail <email> inbox -c 3             # Show last 3 messages only
dropmail <email> refresh                # Fetch new messages from GuerrillaMail API
dropmail <email> read <id>              # Read full body of a message
dropmail <email> remove                 # Remove email + all messages from local DB
dropmail <email> expire                 # Show time remaining before expiry
```

## Typical Workflow

1. `dropmail new` — get a fresh email
2. Share the email address with the untrusted service
3. `dropmail <email> refresh` - pull new messages from the server
4. `dropmail <email> inbox` - browse received messages
5. `dropmail <email> read <id>` - read a specific message
6. `dropmail <email> remove` - clean up when done

## Notes

- **Data location:** All data stored in `~/.dropmail/` (DB + sessions). Auto-created on first run.
- **Sessions:** Per-email PHPSESSID cookies stored in `~/.dropmail/sessions.json`. Expire after ~18 min of API inactivity.
- **Offline inbox:** Messages are cached locally. `inbox` reads from cache; `refresh` syncs from server.
- **403 errors:** GuerrillaMail blocks non-browser User-Agents. The script uses `Mozilla/5.0` by default. If blocked, check `references/api.md`.
- **Expiry:** Emails last 60 minutes. After expiry, old messages are still accessible by calling `set_email_user` via `refresh`.

## API Reference

For full GuerrillaMail API details, see `references/api.md`. Load it when:
- Debugging API call failures
- Adding new API features (extend, delete messages, forget)
- Understanding session/cookie handling
