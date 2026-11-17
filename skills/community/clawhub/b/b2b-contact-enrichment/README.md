# 📧 B2B Contact Enrichment

A Claude Code / OpenClaw skill that finds verified professional email addresses, powered by the [FinalScout API](https://finalscout.com).

## Features

Three ways to find an email, each available as single lookup or bulk batch:

| You have | Method |
|----------|--------|
| A LinkedIn profile URL (incl. Sales Navigator) | LinkedIn find |
| A full name + company domain | Professional find |
| A news article URL (find its author) | Author find |

- **Single lookup** — one blocking call via FinalScout's waterfall endpoints (no polling), with submit-and-poll as fallback
- **Bulk lookup** — process any number of contacts from a CSV, list, table, or JSON, with progress reporting, paginated result collection, and optional CSV export
- **Verification status** — each result is marked `Valid`, `Risky`, `Invalid`, or `Unknown`, with a 0–100 deliverability score and catch-all detection
- **Enrichment** — results include title, company, location, LinkedIn URL, industry, and company details when available
- **Optional extras** — personal/generic email fallback (LinkedIn method), contact tagging, custom `meta_data` passthrough for CRM correlation, and webhook notifications
- **Account awareness** — credit balance and per-endpoint rate limits via the account API; remaining credits shown after each operation

## Requirements

| Requirement | Details |
|-------------|---------|
| FinalScout account | Sign up at [finalscout.com](https://finalscout.com) |
| API key | Get yours at [finalscout.com/app/api/settings](https://finalscout.com/app/api/settings) |
| `curl` | Used for all API calls |

## Setup

1. Install the skill (e.g. clone this repo into your skills directory):

   ```bash
   git clone <repo-url> ~/.claude/skills/b2b-contact-enrichment
   ```

2. Set your API key as an environment variable:

   ```bash
   export FINALSCOUT_API_KEY="your-api-key"
   ```

## Usage

Just ask in natural language. Examples:

**Single lookup**

> Find the email address of Bill Gates at microsoft.com

> Get the email for https://www.linkedin.com/in/satyanadella

> Find the author's email for this article: https://www.forbes.com/sites/...

**Bulk lookup**

> Find emails for these people:
> Bill Gates, microsoft.com
> Elon Musk, tesla.com

> Find emails for all the LinkedIn URLs in leads.csv and export the results as a CSV

You can paste a CSV, a table, or JSON. Results come back as a table:

| Name | Input | Email | Type | Status | Score |
|------|-------|-------|------|--------|-------|
| Bill Gates | microsoft.com | bill@microsoft.com | Work email | Valid | 95 |

**Options** — mention them in your request and the skill will pass them through:

- Include personal emails (Gmail, etc.) or generic emails (info@, support@) — LinkedIn method
- Deep-verify professional lookups when you're sure the domain is right
- Tag contacts in your FinalScout account
- Attach custom metadata (e.g. CRM ids) that comes back with each result
- Send results to a webhook instead of polling
- Check your credit balance and rate limits

## How it works

1. Picks the find method (`linkedin` / `professional` / `author`) from your input
2. Single lookups use the waterfall API (`api-waterfall.finalscout.com`) — one long-polling call that returns the finished result; falls back to submit + status polling on `api.finalscout.com`
3. Bulk lookups submit a task (`/v1/find/*/bulk`), poll `/v1/find/bulk/status` with progress updates, then page through `/v1/find/bulk/dump` — or generate a downloadable CSV via `/v1/find/bulk/export`
4. Presents results with verification status and a summary (`X / Y emails found, Z credits consumed`)

## Pricing

Each email **successfully found** costs 1 FinalScout credit. No charge when no email is found.

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| 401 | Invalid API key | Check `FINALSCOUT_API_KEY` and the IP whitelist in API settings |
| 403 | Insufficient credits | Top up your FinalScout account |
| 405 | Account blocked | Contact dev@finalscout.com |
| 408 | Waterfall timeout | The task is still running — the skill resubmits automatically |
| 429 | Rate limited | The skill retries automatically |

## License

MIT
