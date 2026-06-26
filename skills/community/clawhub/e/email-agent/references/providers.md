# SMTP Providers

This repo ships a few provider presets so the demo works without hand-writing the host each time.

## Presets

The following values were taken from the blog post the user referenced:

- `126`: host `smtp.126.com`, default port `465`, SSL on
- `qq`: host `smtp.qq.com`, default port `465`, SSL on
- `sina`: host `smtp.sina.com`, default port `465`, SSL on
- `aliyun`: host `smtp.aliyun.com`, default port `465`, SSL on

## Authentication note

Per the referenced post:

- `126` and `qq` usually require an SMTP authorization code instead of the mailbox login password.
- `sina` and `aliyun` may accept the mailbox password directly.

This repo treats all of these as one secret field: `SMTP_PASSWORD`.

## Override behavior

Any preset can be overridden in `.env` by setting:

- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USE_SSL`
- `SMTP_USERNAME`
