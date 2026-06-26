# Email Configuration

The email script reads credentials from environment variables so secrets do not need to be stored in skill files.

Required variables:

- `EMAIL_HOST`: SMTP host, such as `smtp.example.com`.
- `IMAP_HOST`: IMAP host, such as `imap.example.com`.
- `EMAIL_USER`: mailbox username and sender address.
- `EMAIL_PASSWORD`: mailbox password or app password.

Compatible SMTP-style aliases:

- `SMTP_HOST`: SMTP host.
- `SMTP_PORT`: SMTP port.
- `SMTP_USER`: mailbox username.
- `SMTP_PASS`: mailbox password or app password.
- `SMTP_FROM`: fallback sender address when `SMTP_USER` is absent.
- `SMTP_SECURE`: `true` for SMTP SSL, `false` for STARTTLS.

Optional variables:

- `EMAIL_PORT`: SMTP port. Defaults to `465`.
- `EMAIL_USE_SSL`: defaults to `true`. Use `false` for STARTTLS.
