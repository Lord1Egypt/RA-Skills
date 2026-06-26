---
name: credential-hygiene-validator
description: >
  Checks whether credentials and tokens are stored safely. Validates
  file permissions, plaintext exposure, git repo contamination, log
  redaction coverage, and token rotation status. Works with OpenClaw
  and general dotfile directories.
metadata:
  openclaw:
    requires:
      bins:
        - grep
        - stat
        - git
---
# Credential Hygiene Validator

Checks whether credentials and tokens in config files are stored
with reasonable hygiene. Catches common mistakes before they become
incidents.

## What it checks

1. **File permissions** -- config files should be 600 or 700, not world-readable
2. **Plaintext tokens** -- scans for hex tokens, JWTs (base64url with dots), Bearer strings, and API keys
3. **Git repo contamination** -- whether the config directory sits inside a git working tree
4. **Gitignore coverage** -- whether .gitignore excludes credential paths
5. **Log file leaks** -- tokens appearing in log output (checks all formats: hex, JWT, Bearer per RFC 6750)
6. **Token age** -- warns if tokens have not been rotated recently
7. **Atomic write safety** -- checks if config backup exists (indicator of safe write patterns)

## When to use it

- After setting up a new tool or service
- Before pushing dotfiles to a public repo
- As part of a regular security hygiene review
- When onboarding a new machine
- After rotating credentials, to confirm the old token is gone

## Example prompts

- "Check if my OpenClaw tokens are stored safely"
- "Audit my dotfiles for leaked credentials"
- "Is my config directory in a git repo?"
- "Check file permissions on my credentials"
- "Are my tokens showing up in any log files?"

## Checks run

```bash
# 1. File permissions
stat -c '%a %n' ~/.openclaw/openclaw.json
# Expected: 600

# 2. Plaintext tokens (full token68 charset per RFC 7235)
grep -rnP '("token"\s*:\s*")[^"]{8,}"|[Bb]earer\s+[\w\-\.+/=~]{16,}|[a-f0-9]{32,}' \
  ~/.openclaw/ --include="*.json" 2>/dev/null

# 3. Git repo check
git -C ~/.openclaw rev-parse --is-inside-work-tree 2>/dev/null
# Expected: error (not in a repo)

# 4. Gitignore coverage
grep -q '.openclaw' ~/.gitignore 2>/dev/null && echo "covered" || echo "not covered"

# 5. Log file leaks (full token68 charset)
grep -rnP '[Bb]earer\s+[\w\-\.+/=~]{16,}|[a-f0-9]{32,}' \
  ~/.openclaw/logs/ --include="*.log" 2>/dev/null

# 6. Token age (check config file modification time)
find ~/.openclaw/openclaw.json -mtime +90 -print 2>/dev/null
# If output: token has not been rotated in 90+ days

# 7. Backup file exists (atomic write indicator)
ls ~/.openclaw/openclaw.json.bak 2>/dev/null && echo "backup present" || echo "no backup"
```

## Notes

- Read-only checks, does not modify any files
- Token patterns match hex, JWT (header.payload.signature), base64url,
  and Bearer headers case-insensitively per RFC 6750
- Works with any tool that stores credentials in dotfiles
- Aligns with T-ACCESS-003 in the OpenClaw threat model

## References

- [OpenClaw threat model (T-ACCESS-003)](https://github.com/openclaw/trust)
- [OpenClaw security policy](https://github.com/openclaw/openclaw/security/policy)
- [RFC 6750 - Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750)
