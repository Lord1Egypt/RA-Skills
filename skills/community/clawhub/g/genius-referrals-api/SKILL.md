---
name: "genius-referrals-api"
description: "Official Genius Referrals skill for building a referral program with AI. Launch your referral marketing automation by integrating the Genius Referrals API directly into OpenClaw. This is the ultimate referral program skill for managing referral tracking, advocate growth, and reward payouts. Easily create advocates, link referrals, automate bonuses, and run referral reports. Perfect for businesses needing reliable referral software and automated referral program management with AI agents."
---

# Genius Referrals API

Use this procedure for Genius Referrals API inspection, reporting, authentication tests, or changes.

1. Classify the request as read/report, create/update, payout or redemption, delete, or documentation lookup. Identify the target environment and account slug; stop if either is needed but unclear.
2. Use the configured API base URL and an approved credential source. Send the token in `X-Auth-Token`, never in a URL or stored skill content.
3. Verify authentication with `GET /test-authentication` before an account-scoped change. Stop and report the authentication result if it fails.
4. For reads, use the narrowest documented endpoint and report only relevant fields. Common read endpoints include `/accounts`, `/accounts/{account_slug}`, advocates, bonuses, redemption requests, and `/reports/*` with required account and date filters.
5. For a change, prepare a dry-run summary with method, path, account slug, payload keys, expected impact, and rollback or cleanup option. Obtain explicit confirmation before production writes, payouts, redemption updates, forced bonuses, or deletes.
6. Execute only the confirmed request. Common changes include creating or updating advocates, linking referrals, forcing a bonus, and updating a redemption request.
7. Report the status code, endpoint, resource identifiers, and next action. Confirm that the stated environment and account slug match the completed request.

## Filters

Where the documented endpoint accepts `filter`, separate clauses with `|` and field/value with `::`. Use only fields documented for that endpoint.

## Completion

Finish only after authentication was checked for API work, every mutation has a method/path/payload summary, high-impact work has explicit approval evidence, and the returned status and identifiers are recorded.
