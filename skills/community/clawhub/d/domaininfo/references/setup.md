# Skill Setup Notes (Non-invasive)

This file intentionally avoids copy/paste installation commands.

## Required system binaries

- `whois` (WHOIS lookups)
- `dig` (DNS queries)
- `openssl` (TLS certificate checks)

## Optional screenshot support

The skill should only take a screenshot if screenshot tooling is already available:

- Prefer OpenClaw's `browser` tool if the runtime provides it.
- Alternatively, the bundled Node script `scripts/domain-screenshot.js` can be used **only if** Node + Playwright + a Chromium runtime are already present.

If screenshot tooling is not available, the skill must skip the screenshot and still return the rest of the report.
