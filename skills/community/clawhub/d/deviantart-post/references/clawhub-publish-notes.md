# ClawHub publishing notes

## Before publishing

- Remove machine-specific paths from the skill.
- Avoid bundling personal credentials, tokens, usernames, or test URLs.
- Keep setup instructions generic and portable.
- Prefer environment variables or user-local default paths over hardcoded absolute paths.
- Verify scripts compile.
- Package the `.skill` and validate it first.

## Public-skill expectations

This skill assumes the user will:
- create their own DeviantArt developer app
- provide their own `client_id`
- choose a localhost redirect URI
- store credentials locally in `~/.openclaw/`

This skill should not assume:
- one specific username
- one specific Windows home directory
- pre-existing tokens
- one platform only

## Safe wording

Use phrasing like:
- "a user's DeviantArt account"
- "local credentials file"
- "default token path"

Avoid phrasing like:
- "your saved token at C:\\Users\\..."
- references to one user's account or published tests
