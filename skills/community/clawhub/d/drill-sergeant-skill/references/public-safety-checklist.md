# Public Safety Checklist (Pre-Publish)

This skill package must stay vendor-neutral and public-safe.

## Must NOT include
- Personal names, user IDs, emails, phone numbers
- Private channel IDs or internal room IDs
- API keys, tokens, secrets, credentials
- Webhook endpoints (inbound/outbound)
- Internal IPs, hostnames, or infrastructure fingerprints
- Customer/prospect PII

## Allowed
- Generic placeholders (e.g., `<owner>`, `<channel>`)
- Abstract policy logic and workflow steps
- Reusable templates with no environment identifiers

## Final gate
Before GitHub/ClawHub publish:
1. Grep for sensitive patterns (IDs, tokens, URLs, IPs).
2. Replace any environment-specific content with placeholders.
3. Confirm no callback/webhook/API dependency is required.
4. Re-read SKILL.md for neutral wording and no private context.
