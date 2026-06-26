# Credential Config Example

Use these examples when the user wants a reusable local config for `$auto-login-assistant`.

## JSON file example

```json
{
  "site": "gmail",
  "login_url": "https://accounts.google.com/",
  "email": "user@example.com",
  "password": "REPLACE_ME",
  "otp_email": "user@example.com",
  "otp_mode": "manual-first",
  "notes": "Use only for inbox triage tasks."
}
```

## Environment variable example

Store a single JSON blob in an env var and point the skill at that variable name:

```bash
export GMAIL_AGENT_LOGIN='{"site":"gmail","email":"user@example.com","password":"REPLACE_ME","otp_mode":"manual-first"}'
```

Then tell the agent:

```text
Use env var GMAIL_AGENT_LOGIN for this login.
```

## Supported fields

- `site`: Short site label for confirmation
- `login_url`: Optional canonical login URL
- `username`: Username if the site does not use email
- `email`: Email-based login identifier
- `phone`: Phone-based login identifier
- `password`: Password or app password
- `otp_email`: Mailbox to watch for verification codes if the user explicitly authorizes it
- `otp_mode`: `manual-first`, `email-assisted`, or `manual-only`
- `notes`: Human hints such as tenant name or account scope

## Recommended defaults

- Prefer `otp_mode: "manual-first"`
- Keep one config per site or tenant
- Do not commit configs to source control
- Use app passwords where the provider supports them
