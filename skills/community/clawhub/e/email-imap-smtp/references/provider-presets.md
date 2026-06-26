# Provider Presets

Use these defaults when the user does not provide custom host/port values.

## Built-in presets

- `qq`: IMAP `imap.qq.com:993`, SMTP `smtp.qq.com:465` (SSL), auth: password/app-code
- `163`: IMAP `imap.163.com:993`, SMTP `smtp.163.com:465` (SSL), auth: password/app-code
- `126`: IMAP `imap.126.com:993`, SMTP `smtp.126.com:465` (SSL), auth: password/app-code
- `gmail`: IMAP `imap.gmail.com:993`, SMTP `smtp.gmail.com:465` (SSL), auth: password + OAuth2
- `outlook`: IMAP `outlook.office365.com:993`, SMTP `smtp.office365.com:587` (STARTTLS), auth: password + OAuth2
- `yahoo`: IMAP `imap.mail.yahoo.com:993`, SMTP `smtp.mail.yahoo.com:465` (SSL), auth: password + OAuth2
- `aol`: IMAP `imap.aol.com:993`, SMTP `smtp.aol.com:465` (SSL), auth: password + OAuth2
- `icloud`: IMAP `imap.mail.me.com:993`, SMTP `smtp.mail.me.com:587` (STARTTLS), auth: password/app-specific
- `zoho`: IMAP `imap.zoho.com:993`, SMTP `smtp.zoho.com:465` (SSL), auth: password + OAuth2

## OAuth2 authorization endpoints (preset defaults)

- `gmail`: `https://accounts.google.com/o/oauth2/v2/auth`
- `outlook`: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`
- `yahoo`: `https://api.login.yahoo.com/oauth2/request_auth`
- `aol`: `https://api.login.yahoo.com/oauth2/request_auth`
- `zoho`: `https://accounts.zoho.com/oauth/v2/auth`

## OAuth2 token endpoints (preset defaults)

- `gmail`: `https://oauth2.googleapis.com/token`
- `outlook`: `https://login.microsoftonline.com/common/oauth2/v2.0/token`
- `yahoo`: `https://api.login.yahoo.com/oauth2/get_token`
- `aol`: `https://api.login.yahoo.com/oauth2/get_token`
- `zoho`: `https://accounts.zoho.com/oauth/v2/token`

## OAuth2 scope defaults used by auth-url/token

- `gmail`: `https://mail.google.com/`
- `outlook`: `offline_access https://outlook.office.com/IMAP.AccessAsUser.All https://outlook.office.com/SMTP.Send`
- `yahoo`: `openid mail-r mail-w`
- `aol`: `openid mail-r mail-w`

## Recommended env vars for OAuth2

- `EMAIL_AUTH_MODE=oauth2`
- `EMAIL_ACCESS_TOKEN=<access_token>` or
- `EMAIL_REFRESH_TOKEN=<refresh_token>` + `EMAIL_TOKEN_ENDPOINT` + `EMAIL_CLIENT_ID` (+ `EMAIL_CLIENT_SECRET` if needed)

## Compatibility notes

- Most mainstream mailboxes can be added even without preset by passing custom `--imap-host/--smtp-host` and ports.
- For Gmail/Outlook/Yahoo/AOL/Zoho, prefer OAuth2 for long-term stability.
- iCloud usually uses app-specific password with IMAP/SMTP.
- Some enterprise tenants require tenant-specific token endpoints or extra scopes; override via CLI/env vars.
