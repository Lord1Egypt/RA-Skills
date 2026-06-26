---
name: email-imap-smtp
description: Connect to mainstream email providers and perform reliable send/receive workflows through IMAP and SMTP with password or OAuth2 authentication. Use when a user asks to add mailbox accounts, test login, list unread/recent emails, read message bodies, search emails by sender/subject/date, refresh OAuth2 tokens, or send emails (with optional HTML and attachments).
---

# Email IMAP/SMTP

Use this skill to automate email operations with standard IMAP/SMTP protocols using local scripts.

## Workflow

1. Confirm provider and auth mode (`password` or `oauth2`).
2. Run connection checks first.
3. List/search emails before reading full content.
4. Send email only after previewing key fields (to/subject/body/attachments).

## Security Rules

- Prefer app passwords over account login passwords in password mode.
- Prefer OAuth2 tokens for Gmail, Outlook, Yahoo, AOL, and Zoho.
- Do not print secrets in terminal output.
- Load credentials from environment variables whenever possible.
- Avoid storing real credentials in repository files.

## Required Inputs

- Email address (login username)
- Authentication:
  - Password mode: app password / authorization code
  - OAuth2 mode: access token, or refresh token + client info
- IMAP host/port
- SMTP host/port

Use `references/provider-presets.md` for common provider host/port defaults.

## Script

Run:

```bash
python scripts/email_ops.py --help
```

Subcommands:

- `check`: Verify IMAP/SMTP login connectivity.
- `list`: List recent/unread email summaries.
- `read`: Read one email by UID.
- `send`: Send an email with optional HTML and attachments.
- `token`: Resolve OAuth2 access token (masked output by default).
- `auth-url`: Build OAuth2 browser login URL for authorization code flow.

## Common Commands

Check mailbox connectivity:

```bash
python scripts/email_ops.py check --provider qq --email you@qq.com
```

Check connectivity with OAuth2 (Gmail):

```bash
python scripts/email_ops.py check --provider gmail --email you@gmail.com --auth-mode oauth2 --access-token "<ACCESS_TOKEN>"
```

List unread emails:

```bash
python scripts/email_ops.py list --provider qq --email you@qq.com --unseen --limit 20
```

Read one email:

```bash
python scripts/email_ops.py read --provider qq --email you@qq.com --uid 12345
```

Send email:

```bash
python scripts/email_ops.py send --provider qq --email you@qq.com --to friend@example.com --subject "Test" --body "Hello from Codex"
```

Resolve a new OAuth2 token from refresh token:

```bash
python scripts/email_ops.py token --provider outlook --email you@outlook.com --auth-mode oauth2 --refresh-token "<REFRESH_TOKEN>" --client-id "<CLIENT_ID>" --client-secret "<CLIENT_SECRET>"
```

Build OAuth2 authorization URL (Gmail example):

```bash
python scripts/email_ops.py --provider gmail --client-id "<CLIENT_ID>" --redirect-uri "http://localhost:8080/callback" auth-url
```

## Environment Variables

- `EMAIL_ADDRESS`: Login email address.
- `EMAIL_PROVIDER`: Provider preset key (for example `qq`, `gmail`, `outlook`, `yahoo`, `aol`, `zoho`, `icloud`).
- `EMAIL_AUTH_MODE`: `auto`/`password`/`oauth2`.
- `EMAIL_APP_PASSWORD` or `EMAIL_PASSWORD`: Password mode credential.
- `EMAIL_ACCESS_TOKEN`: OAuth2 access token.
- `EMAIL_REFRESH_TOKEN`: OAuth2 refresh token.
- `EMAIL_TOKEN_ENDPOINT`: OAuth2 token endpoint.
- `EMAIL_AUTH_ENDPOINT`: OAuth2 authorization endpoint.
- `EMAIL_CLIENT_ID`: OAuth2 client id.
- `EMAIL_CLIENT_SECRET`: OAuth2 client secret.
- `EMAIL_REDIRECT_URI`: OAuth2 redirect URI for auth-url.
- `EMAIL_SCOPE`: Optional scope for refresh request.
- `EMAIL_IMAP_HOST`, `EMAIL_IMAP_PORT`: Override IMAP endpoint.
- `EMAIL_SMTP_HOST`, `EMAIL_SMTP_PORT`: Override SMTP endpoint.
- `EMAIL_SMTP_SSL`: `true`/`false`, default from provider preset.

## Troubleshooting

- Authentication failed in password mode: confirm app password and IMAP/SMTP permissions are enabled.
- Authentication failed in OAuth2 mode: confirm token has IMAP/SMTP scopes and token endpoint/client info are correct.
- SSL/TLS handshake failed: verify host/port pair and whether SMTP SSL is enabled.
- Empty list results: switch mailbox folder (`--mailbox`) or remove filters.
