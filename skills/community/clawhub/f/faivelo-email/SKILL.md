---
name: faivelo-email
description: Set up and use email on a custom domain with Faivelo. Use when the user needs mailboxes on their own domain (hello@, support@, team inboxes), wants their app to send transactional email (receipts, password resets, notifications) from their domain, needs to receive replies or inbound mail as webhooks, or wants an AI agent to read and send mail through an inbox (MCP or REST). Covers the `npx faivelo init` CLI, the `faivelo` SDKs for Node and Python, the REST API, signed webhooks and the hosted MCP server.
homepage: https://faivelo.com/docs/developers/coding-agents/
license: MIT
metadata:
  openclaw:
    primaryEnv: FAIVELO_API_KEY
    emoji: "✉️"
---

# Faivelo email

Faivelo is email hosting for a custom domain: mailboxes, a send API, inbound
webhooks and a hosted MCP server, on one account. Pick the path that matches
what the user asked for. You can combine them.

| The user wants | Do this |
| --- | --- |
| Mailboxes on their domain (hello@, support@) | Run `npx faivelo init <domain>` |
| Their app to send email from their domain | API key + SDK or `POST /api/v1/emails` |
| To get replies / inbound mail into their app | Webhook on `message.received` |
| You (or another agent) to read and send their mail | Connect the MCP server |

Costs: forwarding-only is free; mailboxes, the send API and SMTP/IMAP need a
paid plan (from $6/month, flat, unlimited mailboxes); MCP is included from
Growth; webhooks from Pro. New accounts get a free trial without a card.
Plans: https://faivelo.com/docs/billing/plans/?via=clawhub. Tell the user before anything
that needs a plan or a payment. Never pick a plan or enter payment details
for them.

## 1. Set up email on a domain

```bash
npx faivelo init example.com
```

Interactive. It opens a browser for the user to sign in or create an account
and approve a pairing code, checks the domain, writes the DNS records
(one click on Cloudflare, Vercel, Netlify, DigitalOcean and Google Cloud DNS;
API key for GoDaddy, Namecheap, Route 53, Porkbun and others; copy-ready
values otherwise), waits for DNS, and creates the first mailbox. It prints the
mailbox password and IMAP/SMTP settings once and can write `SMTP_*` and
`IMAP_*` into `.env`.

- The user has to approve the browser step. Hand it to them; do not try to
  automate their sign-in.
- Over SSH or in a container: `npx faivelo init example.com --no-open` prints
  the link instead.
- Re-running is safe; it resumes. `npx faivelo status example.com` checks DNS
  live. `npx faivelo dns example.com --zone` prints a BIND zone file.
- When setup is done and the Faivelo MCP server is connected, call its
  `get_setup_summary` tool and give the user the summary it returns: what
  was set up, what is still pending, and where to manage it.
- If the domain already receives mail somewhere else, the CLI says so before
  changing anything. Do not move a domain's MX without the user agreeing.

## 2. Send email from an app

The user creates an API key at https://faivelo.com/settings/developers?via=clawhub (starts
with `fvl_live_`, shown once). Keep it in an environment variable, e.g.
`FAIVELO_API_KEY`, never in source.

`from` must be an address on a domain verified in their account (no mailbox
needed for that address). Write it as `"Name <address>"` (or pass `fromName`)
so recipients see a name, not only the address.

Node (`npm install faivelo`):

```ts
import { Faivelo } from 'faivelo'

const faivelo = new Faivelo(process.env.FAIVELO_API_KEY!)
const email = await faivelo.emails.send({
  from: 'Acme <hello@acme.com>',
  to: 'user@example.com',
  subject: 'Your receipt',
  html: '<p>Thanks for your order.</p>',
  idempotencyKey: `receipt-${orderId}`, // a retry never sends twice
})
// email.id → faivelo.emails.get(email.id) for delivery status
```

Python (`pip install faivelo`):

```python
from faivelo import Faivelo

client = Faivelo()  # reads FAIVELO_API_KEY
email = client.emails.send(
    from_="Acme <hello@acme.com>",
    to="user@example.com",
    subject="Your receipt",
    html="<p>Thanks for your order.</p>",
    idempotency_key=f"receipt-{order_id}",
)
```

Any language: see [references/rest-api.md](references/rest-api.md).

## 3. Receive mail and replies

Webhooks (Pro and Business) POST a signed event when mail arrives. The user
adds the endpoint at https://faivelo.com/settings/developers/webhooks?via=clawhub and
copies its signing secret (`whsec_...`). Verify every request against the
RAW body before trusting it. Details and payloads:
[references/webhooks.md](references/webhooks.md).

To read the full message, call
`GET /api/v1/mailboxes/{address}/messages/{message_id}` with the event's
`data.message_id`.

## 4. Give an agent an inbox (MCP)

Hosted server: `https://faivelo.com/api/mcp` (streamable HTTP). Interactive
clients sign in with OAuth and the user ticks which mailboxes the agent may
use. Headless agents send `Authorization: Bearer fvl_live_...` instead.

```bash
claude mcp add --transport http faivelo https://faivelo.com/api/mcp
```

Other clients and the full tool list: [references/mcp.md](references/mcp.md).

Give every mailbox a name: `displayName` on `create_mailbox`, or
`update_mailbox` later. Without one, mail shows only the bare address (a
send's response then carries a `hint`). `send_message` also takes
`from: "Support Bot <bot@acme.com>"` for a one-message name.

When you finish setting something up for the user, call `get_setup_summary`
(read-only) and hand them the markdown it returns, so they have a record of
what you did.

For an autonomous agent, recommend an **agent key** (Settings → Developers →
kind: agent): it only reaches mailboxes it created or was granted, and cannot
touch domains, billing or other inboxes.

## Errors

Error responses are JSON with an HTTP status:

```json
{ "success": false, "error": "Missing or malformed API key", "code": "missing_api_key",
  "fix": "Send the key as \"Authorization: Bearer fvl_live_...\" ...",
  "docs": "https://faivelo.com/docs/developers/errors#missing_api_key" }
```

Branch on `code`, follow `fix`, and read `docs` for details. Validation
errors also carry `param` (the field at fault). A `429` comes with a
`Retry-After` header: wait that long, then retry. A `409` on a DNS edit means
the record is mail-critical; repeat with `force: true` only if the user
really means it. Every code: https://faivelo.com/docs/developers/errors

## Links

- Docs: https://faivelo.com/docs/?via=clawhub
- API reference: https://faivelo.com/docs/api
- OpenAPI: https://faivelo.com/api/v1/openapi.json
- Docs for agents: https://faivelo.com/docs/llms.txt
