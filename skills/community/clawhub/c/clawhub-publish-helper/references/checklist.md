# Audit Checklist

Use this when preparing a skill for publishing.

## Secrets Scan

- [ ] No API keys, tokens, or passwords in any file
- [ ] No private keys or certificates
- [ ] No `.env` files or credential references

## PII Scan

- [ ] No absolute paths with real usernames (`/home/username/`, `/Users/name/`)
- [ ] No Discord IDs (channel, user, guild, message)
- [ ] No real names, emails, or phone numbers
- [ ] No personal health data (medication names, conditions, dosages)
- [ ] No internal IP addresses or private URLs
- [ ] No user-specific identifiers (custom labels, project codenames)

## Generalization

- [ ] Hardcoded paths → env vars with `~` or sensible defaults
- [ ] Hardcoded timezones → env vars with UTC fallback
- [ ] Hardcoded channel/user IDs → removed or env vars
- [ ] Personal config → empty/editable sections with instructions
- [ ] `now()`/`utc_now()` fallbacks removed — require explicit timestamps
- [ ] Shell scripts use relative path resolution (`dirname "$0"`)
- [ ] Dead code and unused references removed

## Frontmatter

- [ ] `env:` block declares all required/optional env vars
- [ ] `description` is generic and useful
- [ ] `version` is correct
- [ ] `name` is set

## Verification

- [ ] Final grep across all files confirms no sensitive content
- [ ] README.md exists with setup instructions
- [ ] .gitignore exists
- [ ] Git initialized with clean commit
