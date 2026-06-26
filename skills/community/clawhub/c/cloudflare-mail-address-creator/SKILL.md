---
name: cloudflare-mail-address-creator
description: Create one or many ordinary email addresses in a Cloudflare temporary mail system through the `/admin/new_address` admin API and return structured results. Use when Codex is asked to create mailbox addresses through the backend instead of clicking the web UI, including requests such as "create t2@suilong.online", "create 10 mailboxes", "add a mailbox in my Cloudflare temp mail system", or "use the Cloudflare mail admin API to create addresses".
---

# Cloudflare Mail Address Creator

Use this skill to create ordinary mailbox addresses through `https://mail-api.suilong.online/admin/new_address`.

## Follow This Workflow

1. Collect or infer `name`, `domain`, and `enablePrefix`.
2. Default `enablePrefix` to `true` when the user does not specify it.
3. If the user gives a full address such as `t2@suilong.online`, split it into `name=t2` and `domain=suilong.online`.
4. Never store real credentials in the skill. Pass runtime credentials with CLI flags or environment variables.
5. Run [scripts/create_address.py](scripts/create_address.py) for single or batch creation.
6. Return the script's JSON output directly unless the user asks for a reformatted summary.
7. Preserve the normalized statuses: `created`, `already_exists`, `auth_error`, `error`.
8. If validation fails locally, fix the input before attempting the API call again.
9. Use `--output-format csv` and optionally `--output-file <path>` when the user asks for exportable results.

## Run The Script

Single address:

```powershell
C:\Users\sl\AppData\Local\Python\bin\python.exe scripts/create_address.py `
  --name t2 `
  --domain suilong.online `
  --admin-auth $env:CLOUDFLARE_MAIL_ADMIN_AUTH
```

Batch addresses from a comma-separated list:

```powershell
C:\Users\sl\AppData\Local\Python\bin\python.exe scripts/create_address.py `
  --names alice,bob,charlie `
  --domain suilong.online `
  --enable-prefix true `
  --admin-auth $env:CLOUDFLARE_MAIL_ADMIN_AUTH
```

Batch addresses from a file:

```powershell
C:\Users\sl\AppData\Local\Python\bin\python.exe scripts/create_address.py `
  --names-file .\names.txt `
  --domain suilong.online `
  --admin-auth $env:CLOUDFLARE_MAIL_ADMIN_AUTH
```

Export batch results as CSV:

```powershell
C:\Users\sl\AppData\Local\Python\bin\python.exe scripts/create_address.py `
  --names alice,bob,charlie `
  --domain suilong.online `
  --output-format csv `
  --output-file .\created-addresses.csv `
  --admin-auth $env:CLOUDFLARE_MAIL_ADMIN_AUTH
```

## Runtime Credentials

Prefer environment variables for secrets:

- `CLOUDFLARE_MAIL_ADMIN_AUTH`
- `CLOUDFLARE_MAIL_BEARER_TOKEN`
- `CLOUDFLARE_MAIL_FINGERPRINT`
- `CLOUDFLARE_MAIL_LANG`
- `CLOUDFLARE_MAIL_USER_TOKEN`
- `CLOUDFLARE_MAIL_API_URL`

## Read More Only When Needed

- Read [references/api.md](references/api.md) for the endpoint contract and error mapping.
- Read [references/examples.md](references/examples.md) for example prompts and outputs.
