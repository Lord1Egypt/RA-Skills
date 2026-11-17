---
name: drin-email-best-practices
description: Get transactional email deliverability right with Drin — authenticate the sending domain (SPF/DKIM/DMARC), stay under bounce/complaint limits, honor suppressions, and include one-click unsubscribe where required. Use when setting up a sending domain, diagnosing why mail lands in spam or bounces, deciding sending volume/warmup, or reviewing an email program for compliance and reputation.
version: 1.0.0
---

# Email deliverability & compliance with Drin

Reputation is everything. One sloppy send can tank an entire domain's inbox
placement. Follow these before and during any sending program.

## 1. Authenticate the domain (do this first)

Email is only trusted when the sending domain is authenticated.

- Add the domain: `add_domain` / `POST /v1/domains` / dashboard. Drin returns the
  exact DNS records to publish.
- Publish **all** returned records:
  - **DKIM** — Drin signs with the domain's own key (records provided). This is
    what makes the mail cryptographically yours.
  - **SPF / MAIL FROM** — authorizes the sending path.
  - **DMARC** — start at `p=none` to monitor, then move to `p=quarantine` →
    `p=reject` once aligned and clean. Publish a `rua=` to receive reports.
- Confirm verification: `get_domain` / `GET /v1/domains/:id` and check each
  record's `verified: true`. Do not send real mail until the domain is verified.

Prefer a **subdomain** for sending (e.g. `mail.acme.com` / `notifications.acme.com`)
so transactional reputation is isolated from your root domain's other mail.

## 2. Stay under the hard limits

Mailbox providers (and Drin's own circuit breaker) watch these rates. Crossing
them throttles or suspends sending:

- **Bounce rate < 4%** (aim < 2%). High bounces = bad list hygiene.
- **Complaint (spam) rate < 0.1%** (aim < 0.05%). High complaints = unwanted mail.

Monitor continuously with `get_metrics` / `GET /v1/metrics`. If a rate climbs,
**stop and investigate** — don't keep sending.

## 3. Honor suppressions — never bypass them

Drin automatically suppresses an address after a hard bounce or a spam complaint,
and refuses (`409 suppressed`) further sends to it. This protects your
reputation. Rules for an agent:

- Never "retry around" a suppression or strip it to force a send.
- Treat unsubscribe / "stop emailing me" requests as `add_suppression`.
- Inspect with `list_suppressions`; only `remove_suppression` on a genuine,
  verified opt-back-in.

## 4. List hygiene & content

- Send to addresses that **opted in** or that you have a transactional
  relationship with. Don't email purchased/scraped lists.
- Validate addresses at capture time; don't send to obviously invalid ones.
- Keep a real `text` part, a clear `from` name, a truthful subject (no
  clickbait/ALL CAPS/excessive emoji), and a visible physical identity where
  required.
- Match the `from` domain to the brand the recipient expects (alignment).

## 5. Unsubscribe (bulk / marketing-adjacent mail)

For anything beyond strictly 1:1 transactional mail, include a working
unsubscribe. Drin supports RFC 8058 one-click unsubscribe and a hosted
`/unsubscribe` flow — include the unsubscribe link/headers and honor opt-outs
immediately (they become suppressions). Transactional receipts/OTPs/password
resets generally don't need an unsubscribe, but must not contain marketing.

## 6. Warm up new domains/volume

A brand-new domain has no reputation. Ramp gradually (start with low daily
volume to your most engaged recipients, increase over days/weeks) rather than
blasting from day one. Drin's per-tenant trust engine ramps new senders
automatically — don't try to defeat it; let reputation build.

## Quick checklist before a campaign or new integration

- [ ] Domain verified (`get_domain` shows DKIM/SPF/DMARC `verified: true`).
- [ ] DMARC at least `p=none` with `rua=` reporting.
- [ ] Sending from a subdomain dedicated to this mail stream.
- [ ] `text` part present; subject honest; from-name set.
- [ ] Recipients opted in / transactional; list cleaned.
- [ ] Unsubscribe present for non-1:1 mail.
- [ ] Baseline `get_metrics` captured; bounce/complaint alerts in mind.
