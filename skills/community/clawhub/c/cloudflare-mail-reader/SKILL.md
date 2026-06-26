---
name: cloudflare-mail-reader
description: Read one mailbox's messages or a paginated mail list from a Cloudflare temporary mail system through the `/admin/mails` admin API and return structured results. Use when Codex is asked to fetch or read emails through the backend instead of opening the web UI, including requests such as "read mails for t2@suilong.online", "show the latest 20 emails", "export mailbox messages", or "use the Cloudflare mail admin API to fetch messages".
---

# Cloudflare Mail Reader

Use this skill to read mailbox messages through `https://mail-api.suilong.online/admin/mails`.

## Follow This Workflow

1. Collect or infer `address`, `limit`, and `offset`.
2. Default `limit` to `20` and `offset` to `0` when the user does not specify them.
3. Never store real credentials in the skill. Pass runtime credentials with CLI flags or environment variables.
4. Run [scripts/read_mails.py](scripts/read_mails.py) to fetch and normalize the response.
5. The normalized result includes `verification_code` when a code can be extracted from subject/text/html content.
6. Return the script's JSON output directly unless the user asks for a reformatted summary.
7. Use `--output-format csv` and optionally `--output-file <path>` when the user asks for exportable results.
8. Preserve the normalized statuses: `ok`, `auth_error`, `error`.
9. Use `--include-raw` only when the user explicitly wants the full original payload for debugging.

## Run The Script

Read one mailbox:

```powershell
C:\Users\sl\AppData\Local\Python\bin\python.exe scripts/read_mails.py `
  --address t2@suilong.online `
  --limit 20 `
  --offset 0 `
  --admin-auth $env:CLOUDFLARE_MAIL_ADMIN_AUTH
```

Read recent mails without an address filter:

```powershell
C:\Users\sl\AppData\Local\Python\bin\python.exe scripts/read_mails.py `
  --limit 20 `
  --offset 0 `
  --admin-auth $env:CLOUDFLARE_MAIL_ADMIN_AUTH
```

Export messages as CSV:

```powershell
C:\Users\sl\AppData\Local\Python\bin\python.exe scripts/read_mails.py `
  --address t2@suilong.online `
  --limit 20 `
  --output-format csv `
  --output-file .\mail-results.csv `
  --admin-auth $env:CLOUDFLARE_MAIL_ADMIN_AUTH
```

## Runtime Credentials

Prefer environment variables for secrets:

- `CLOUDFLARE_MAIL_ADMIN_AUTH`
- `CLOUDFLARE_MAIL_BEARER_TOKEN`
- `CLOUDFLARE_MAIL_CUSTOM_AUTH`
- `CLOUDFLARE_MAIL_FINGERPRINT`
- `CLOUDFLARE_MAIL_LANG`
- `CLOUDFLARE_MAIL_USER_TOKEN`
- `CLOUDFLARE_MAIL_MAILS_API_URL`

## Read More Only When Needed

- Read [references/api.md](references/api.md) for the endpoint contract and normalization rules.
- Read [references/examples.md](references/examples.md) for example prompts and outputs.
