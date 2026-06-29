# OpenClaw Ecosystem Monitor

Monitor public OpenClaw ecosystem freshness and trust signals with source-linked, metadata-only reports.

Status: free public skill  
Spend: $0  
Public side effects: read-only network requests only

## What It Produces

- A JSON snapshot for local review.
- A Markdown report with source links, freshness notes, and pause-trigger warnings.
- A small candidate list for manual review before any public contribution.

## What It Monitors

- OpenClaw GitHub repository metadata.
- Open documentation-related issue candidates.
- OpenClaw-related npm package freshness.
- OpenClaw docs sitemap volume.
- ClawHub and docs robots status.

## Trust Boundary

This skill stores metadata only:

- source URL,
- request status,
- hash,
- timestamp,
- short issue/package metadata,
- short report summaries.

It does not store full issue bodies, README bodies, docs pages, tarballs, cookies, secrets, payment data, invoices, or KYC data.

Distribution review docs:

- `trust/permission-manifest.md`
- `trust/no-secret-policy.md`
- `trust/test-fixture.md`
- `trust/rollback.md`
- `trust/privacy.md`
- `trust/threat-model.md`
- `trust/external-services.md`
- `trust/pricing-boundary.md`
- `publish/sanitized-demo-report.md`
- `CHANGELOG.md`

## Run Once

Collect a snapshot:

```bash
node scripts/collect-openclaw-ecosystem.mjs
```

Render a Markdown demo report from the latest snapshot:

```bash
node scripts/render-demo-report.mjs
```

Outputs:

- `data/YYYY-MM-DD/openclaw-ecosystem-snapshot.json`
- `reports/YYYY-MM-DD-openclaw-ecosystem-report.md`

## Optional Local Schedule

You can run this skill through the included no-model wrapper:

- script: `ops/run-openclaw-ecosystem-monitor.sh`
- interval: 6 hours
- log: `~/.openclaw/logs/earn-money-openclaw-monitor.log`

This schedule only runs the collector and report renderer. It does not call an LLM, post publicly, send messages, or use secrets.

## Pause Triggers

Pause collection for a source if any of these occur:

- HTTP 403,
- HTTP 429,
- robots disallow,
- DMCA or abuse warning,
- platform warning.

## Monetization Boundary

No payment code exists in this skill.
No hosted API, checkout, paid listing, invoice flow, or donation link is included.
