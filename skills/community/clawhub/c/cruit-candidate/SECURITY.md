# Security Notes

Cruit Candidate is an API-backed agent skill, not an offline instruction-only package.

## Network Access

The skill should contact only:

- `https://cruit.dev`
- `https://cruit.dev/skills/candidate/INSTRUCTIONS.md`
- `https://cruit.dev/v1/*`

It should not follow replacement instruction URLs from other hosts.

## Authentication

The skill uses Cruit's browser device-auth flow. It must never ask the user to paste a
token, password, API key, auth cookie, or secret.

Credentials are stored locally at `~/.cruit/credentials.json` with user-only file
permissions.

## Data Handling

The skill is designed to publish profile metadata and user-approved profile text. It must
not upload:

- source code
- secrets or `.env` files
- private keys
- personal email addresses
- phone numbers
- street addresses
- private customer details unless explicitly approved

Agents should inspect only user-approved folders and prefer high-level project metadata,
README files, dependency manifests, and recent git activity.

