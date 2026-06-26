---
name: dyagil-supabase-security-audit
description: Audit a Supabase + Vercel project for RLS coverage, privilege escalation, cross-customer data leaks, anonymous exposure, magic-link flow correctness, and HTTP security headers — and apply hotfix templates when issues are found. Use whenever the user asks about security / RLS / audits, after any migration that touches `profiles`-like tables or auth, or before exposing a new customer-facing surface.
version: 1.0.0
license: MIT
author: dyagil
---

# Supabase Security Audit

Run the audit, read the findings, apply hotfixes. The script is tuned for projects that use Supabase + Vercel and a `profiles` table with `role in ('admin','agent','customer')` (or similar), but its individual probes are independent — single-table projects benefit too.

## When to Run

- User asks "are we secure?" / "security audit" / "RLS check".
- After any migration that touches `profiles`, RLS policies, or auth triggers.
- Before sending the first real magic link to a customer.
- After rotating credentials or changing Site URL / Redirect URLs.
- Before exposing a new surface (portal, CRM, admin tool) to real users.

## Prerequisites

Credentials file at `~/.openclaw/credentials/supabase/credentials.env` (override path with `--cred`) containing:

```
SUPABASE_URL=https://<ref>.supabase.co
SUPABASE_PROJECT_REF=<ref>
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_ROLE_KEY=...
SUPABASE_DB_PASSWORD=...
```

The `pg` Node package must be reachable. The script auto-discovers it from `/tmp/sb-tools/node_modules/pg`. If missing:

```bash
mkdir -p /tmp/sb-tools && (cd /tmp/sb-tools && npm i pg)
```

## Workflow

### 1. Run the audit

```bash
node <skills-dir>/supabase-security-audit/scripts/audit.js \
  --probe-uid <existing-customer-uid> \
  --target-uid <another-customer-uid> \
  --site https://example.com
```

- `--probe-uid` / `--target-uid` are **optional** but unlock the live privilege-escalation probe and the cross-customer data-leak probe. Both probes run inside a transaction that is always rolled back — they do not mutate the database.
- `--site` adds a HEAD request to check security headers (CSP, HSTS, etc.).
- `--public-tables` overrides the default list checked for anonymous reads (defaults to `profiles,deals,documents,invoices,inquiries,customer_events,tax_engagements`).

Exit code is `0` if no critical findings, `1` if any.

### 2. Read the findings

Output is grouped: RLS coverage → anonymous exposure → UPDATE policies → live privilege escalation → cross-customer leaks → HTTP headers → summary.

Severity icons:

- 🚨 `crit` — exploitable now, fix today.
- 🟡 `warn` — best-practice gap or audit step skipped (e.g. no `--probe-uid`).
- ✅ `ok`   — passed.

### 3. Map findings to fixes

For each 🚨 finding, look it up in [references/threat-patterns.md](references/threat-patterns.md) — every common pattern in that file has a detection query, an impact statement, and a fix.

The most common critical finding is **"UPDATE policy lacks WITH CHECK on role/email — privilege escalation risk"**. That has a turn-key SQL template:

```bash
# Edit the table name in the file first if it isn't `public.profiles`
node <project>/deploy/run-migration.cjs \
  <skills-dir>/supabase-security-audit/scripts/hotfix-role-lock.sql
```

Then re-run `audit.js` to confirm the finding flipped to ✅.

### 4. Document the audit

Append a one-paragraph summary to your project's memory or change-log file under a dated heading, including which findings were fixed and any deferred items.

## What This Skill Does NOT Cover

- **DDoS / rate-limit checks.** Supabase + Vercel handle the basics; for finer control add Cloudflare or Supabase's Pro plan rate limiting.
- **Application-level CSRF.** Supabase auth uses Bearer tokens, not cookies, so CSRF is not a concern for the auth flow itself — but custom session cookies (e.g. an internal dashboard's `mc_session`) must be audited separately.
- **Penetration testing of business logic** (e.g. "can a customer call `/api/send-portal-link` for another customer's id?"). Spot-check those manually by tracing each `api/*.js` endpoint's auth check.

## References

- [references/threat-patterns.md](references/threat-patterns.md) — exploitable patterns with detection queries and fixes.
- [scripts/audit.js](scripts/audit.js) — the audit runner.
- [scripts/hotfix-role-lock.sql](scripts/hotfix-role-lock.sql) — turnkey fix for the privilege-escalation pattern.
