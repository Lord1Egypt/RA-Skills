# BounceBan Email Verification Skill

A [Claude Code](https://claude.com/claude-code) / agent skill for verifying email addresses with the [BounceBan API](https://bounceban.com/public/doc/api.html). BounceBan specializes in accept-all (catch-all) emails and emails protected by Secure Email Gateways — it identifies which accept-all emails are actually deliverable instead of marking them all as risky.

## What it does

Once installed, the agent can:

- **Verify a single email** — synchronously (waterfall endpoint, waits up to 80 s) or asynchronously (submit, then poll or receive a webhook).
- **Verify email lists in bulk** — up to ~500k emails per task via JSON, or a CSV file up to 25 MB; poll progress, fetch paginated results, or export to a CSV download link.
- **Run quick checks** — free / disposable / role / syntax detection without an SMTP handshake (`GET /v1/check`).
- **Manage the account** — check credit balance and live rate limits (`GET /v1/account`).
- **Handle webhooks** — payload formats and event types for async notifications.

The skill also encodes credit-saving rules (never resubmit while a verification is in flight, retry waterfall timeouts for free, polling caps) and a full HTTP error-handling table, so the agent doesn't waste credits or misread API responses.

## Setup

1. Get an API key at <https://bounceban.com/app/api/settings>.
2. Export it as an environment variable:

   ```bash
   export BOUNCEBAN_API_KEY="your-api-key"
   ```

3. Make sure `curl` is available (it is on virtually every system).

The key is sent in the `Authorization` header **without** a `Bearer` prefix. Each verification costs 1 credit.

## Installation

Copy this directory into your skills folder, e.g. for Claude Code:

```bash
# Personal (all projects)
cp -r skill-email-verification ~/.claude/skills/bounceban

# Or per project
cp -r skill-email-verification .claude/skills/bounceban
```

Then just ask naturally: *"verify jane@acme.com"*, *"clean this email list"*, *"is this a disposable address?"* — the skill triggers on email-verification tasks.

## Quick example

Verify one email and wait for the result:

```bash
curl -s "https://api-waterfall.bounceban.com/v1/verify/single?email=someone@example.com" \
  -H "Authorization: $BOUNCEBAN_API_KEY"
```

Result fields:

- `result` — `deliverable` | `risky` | `undeliverable` | `unknown`
- `score` — 0–100 deliverability confidence (for `risky`, higher is better)
- Flags — `is_disposable`, `is_accept_all`, `is_role`, `is_free`, plus `mx_records` and `smtp_provider`

## Structure

```
SKILL.md                              # Entry point: endpoint routing table, quick recipes, critical rules
references/
  introduction.md                     # Auth, credits, result enums, rate limits
  single-verification.md              # Sync (waterfall) and async single verification
  bulk-verification.md                # Bulk tasks: create, status, dump, export, destroy
  check.md                            # Fast free/disposable/role/syntax check (no SMTP)
  account.md                          # Credits balance and rate limits
  webhooks.md                         # Webhook payloads and event types
```

The agent reads `SKILL.md` first and loads the matching reference file before calling an endpoint, keeping context usage small.

## Rate limits

| Endpoint | Limit |
| --- | --- |
| `/verify/single` | 25 req/s |
| `/verify/bulk` | 3 req/s |
| Others | 25 req/s |

Live values are returned by `GET /v1/account`.

## Links

- [BounceBan API documentation](https://bounceban.com/public/doc/api.html)
- [Get an API key](https://bounceban.com/app/api/settings)
- [Pricing](https://bounceban.com/pricing)
