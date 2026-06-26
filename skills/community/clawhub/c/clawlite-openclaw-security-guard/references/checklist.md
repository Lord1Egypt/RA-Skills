# Security Guard Checklist

Use this skill as a **preflight filter**, not as proof of safety.

## High-risk patterns worth blocking
- prompt injection / instruction override
- dangerous shell execution chains
- SSRF / localhost / metadata endpoints
- path traversal / sensitive files
- hardcoded secrets
- exfiltration utilities and outbound secret posting

## Typical publish-time red flags
- `curl ... | bash`
- `wget ... | sh`
- `rm -rf`, `mkfs`, `dd`, `chmod -R 777`
- posting to unknown webhooks / Discord webhooks / pastebins
- embedded tokens / API keys / JWTs / private keys
- scripts that auto-modify shell startup files without clear user intent

## Typical install-time red flags
- hidden postinstall scripts
- fetching remote code during install without pinning / checksum
- unbounded exec on user-supplied content
- scanning or uploading `~/.ssh`, `.env`, `/etc/*`, keychain dumps

## Decision rule
- `ALLOW`: proceed if context is low risk
- `WARN`: review lines manually before proceeding
- `BLOCK`: do not install/publish/run until resolved
