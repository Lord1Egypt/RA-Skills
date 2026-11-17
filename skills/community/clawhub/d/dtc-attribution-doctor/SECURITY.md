# Security Policy

## Reporting A Vulnerability

Do not open a public issue for:

- Exposed or reusable API credentials
- Unauthorized access to customer or account data
- Authentication or authorization bypasses
- Cross-account data access
- Request forwarding that can reach unintended hosts
- Logs or model outputs that disclose sensitive data

Use GitHub's **Private vulnerability reporting** feature for this repository.
If that feature is not enabled, contact the repository owner privately before
sharing technical details. Do not include a real API key or customer payload in
the report; use redacted reproduction data.

## Supported Versions

Until the first stable release, security fixes are provided only for the latest
commit on the default branch.

## Credential Handling

- Store `CONVBOX_API_KEY` only in the process environment or an approved secret
  manager.
- Never commit `.env`, key files, request dumps, or customer API responses.
- Rotate a key immediately if it appears in a commit, issue, log, or model
  conversation.
- Treat ad account IDs and raw performance exports as sensitive customer data.

## Scope Boundary

This policy covers the files in this repository. Security issues in the hosted
Convbox service may follow a separate disclosure and response process.

