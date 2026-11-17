# Faivelo REST API

Base URL: `https://faivelo.com/api/v1`. Auth: `Authorization: Bearer fvl_live_...`.
OpenAPI spec: https://faivelo.com/api/v1/openapi.json.
Every response is `{ "success": true, "data": ... }` or
`{ "success": false, "error": "..." }`.

## Send an email

```bash
curl https://faivelo.com/api/v1/emails \
  -H "Authorization: Bearer $FAIVELO_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: welcome-42" \
  -d '{
    "from": "Acme <hello@acme.com>",
    "to": "user@example.com",
    "subject": "Welcome",
    "html": "<p>Hi!</p>"
  }'
```

Body fields: `from` (address on a verified domain, bare or `"Name <address>"`),
`fromName` (optional; wins over a name in `from`), `to` (string or up to 50),
`cc`, `bcc`, `subject` (required unless `templateAlias`), `html` and/or
`text`, `replyTo`, `templateAlias` + `variables` (a template designed in the
dashboard), `attachments` (`[{ filename, content: <base64>, contentType? }]`,
up to 10, 10 MB total). `Idempotency-Key` header: up to 256 characters; a
repeat returns the first result instead of sending again.

With no name in the request, the From name is that address's mailbox name,
else the domain default; with none at all the response carries a `hint`.

Returns `data.id`. Check delivery with `GET /emails/{id}` (`status`: sent,
delivered, bounced, complained, failed; plus `events`).

## Mailboxes

| Method and path | Does |
| --- | --- |
| `GET /mailboxes?domain=` | List mailboxes |
| `POST /mailboxes` `{ domain, localPart, displayName?, password? }` | Create one; returns IMAP/SMTP credentials once |
| `GET /mailboxes/{address}` | One mailbox |
| `PATCH /mailboxes/{address}` `{ active?, displayName? }` | Update; `displayName` is the From name recipients see |
| `POST /mailboxes/{address}/reset-password` | New password, shown once |
| `POST /mailboxes/{address}/send` `{ to, subject, html/text, fromName?, inReplyTo?, sendAt? }` | Send as that mailbox (lands in its Sent folder, threads replies); `fromName` is for this message only |
| `GET /mailboxes/{address}/messages?folder=&page=&limit=` | List messages |
| `GET /mailboxes/{address}/messages/{uid}` | Read one (html, text, attachments) |
| `GET /mailboxes/{address}/messages/{uid}/thread` | Whole conversation |
| `GET /mailboxes/{address}/search?q=&from=&subject=` | Search |

## Domains and DNS

| Method and path | Does |
| --- | --- |
| `GET /domains` | List domains and verification state |
| `GET /domains/{domain}` | One domain |
| `GET /domains/{domain}/dns/records` | Live DNS records (where the DNS host is connected) |
| `POST /domains/{domain}/dns/records` | Add a record |
| `PUT` / `DELETE /domains/{domain}/dns/records/{id}` | Edit / remove; mail-critical records need `force: true` |

## Aliases and usage

`GET/POST /aliases`, `DELETE /aliases/{address}`, `GET /usage` (plan and
sending quota left).

## Scopes

Keys carry scopes: `mail:read`, `mail:send`, `mail:write`, `mailboxes:read`,
`mailboxes:write`, `dns:read`, `dns:write`, `domains:read`, `domains:write`,
`aliases:read`, `aliases:write`, `drive:read`. A missing scope answers 403.

## Limits

120 requests a minute per key; 10 mailbox creations per key per 24 hours;
sending rate and monthly allowance depend on the plan
(https://faivelo.com/docs/developers/ai-agents/?via=clawhub#rate-limits). A `429` says how
long to wait.
