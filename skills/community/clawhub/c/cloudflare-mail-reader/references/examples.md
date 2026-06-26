# Example Prompts

## Natural Language

- `Read mails for t2@suilong.online`
- `Show the latest 20 emails for alice@suilong.online`
- `Fetch mailbox messages from my Cloudflare temp mail backend`
- `Export the last 50 emails as CSV`

## Script Examples

Read one mailbox:

```powershell
$env:CLOUDFLARE_MAIL_ADMIN_AUTH = "your-admin-auth"
C:\Users\sl\AppData\Local\Python\bin\python.exe scripts/read_mails.py `
  --address t2@suilong.online `
  --limit 20 `
  --offset 0
```

Read with extra headers:

```powershell
$env:CLOUDFLARE_MAIL_ADMIN_AUTH = "your-admin-auth"
$env:CLOUDFLARE_MAIL_FINGERPRINT = "your-fingerprint"
$env:CLOUDFLARE_MAIL_LANG = "zh"
C:\Users\sl\AppData\Local\Python\bin\python.exe scripts/read_mails.py `
  --address t2@suilong.online `
  --limit 20
```

Export to CSV:

```powershell
$env:CLOUDFLARE_MAIL_ADMIN_AUTH = "your-admin-auth"
C:\Users\sl\AppData\Local\Python\bin\python.exe scripts/read_mails.py `
  --address t2@suilong.online `
  --limit 20 `
  --output-format csv `
  --output-file .\mail-results.csv
```

## Example Success Output

```json
{
  "status": "ok",
  "query": {
    "address": "t2@suilong.online",
    "limit": 20,
    "offset": 0
  },
  "summary": {
    "count": 1,
    "limit": 20,
    "offset": 0
  },
  "results": [
    {
      "id": 16,
      "message_id": "<tencent_647C4AA407879B224CB1EA31@qq.com>",
      "address": "t2@suilong.online",
      "source": "jcwang@suilongkeji.com",
      "from": "noreply@example.com",
      "to": "t2@suilong.online",
      "subject": "Verification code",
      "date": "2026-03-25 07:01:55",
      "preview": "Your verification code is 123456.",
      "text": "Your verification code is 123456.",
      "html": null,
      "verification_code": "123456"
    }
  ]
}
```
