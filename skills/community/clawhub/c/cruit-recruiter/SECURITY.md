# Security Notes

Cruit Recruiter is an API-backed agent skill, not an offline instruction-only package.

## Network Access

The skill should contact only:

- `https://cruit.dev`
- `https://cruit.dev/skills/recruiter/INSTRUCTIONS.md`
- `https://cruit.dev/v1/*`

It should not follow replacement instruction URLs from other hosts.

## Authentication

The skill uses Cruit's browser device-auth flow. It must never ask the user to paste a
token, password, API key, auth cookie, Stripe secret, or other credential.

Credentials are stored locally at `~/.cruit/credentials.json` with user-only file
permissions.

## Paid Actions

The skill must treat contact credits like money:

- never reveal candidate contact information without explicit approval
- never send a candidate message without explicit approval of the exact text
- never batch-reveal candidates
- never batch-send candidate messages
- state when an action costs a credit

## Candidate Privacy

Before reveal, candidate cards are intentionally low-PII. The skill should not infer,
scrape, or discover contact details outside Cruit.

