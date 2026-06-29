---
name: claw-ecosystem-monitor
description: Monitor public OpenClaw ecosystem sources with source-quality checks, metadata-only collection, and trust-first reporting.
version: 0.1.0
owner: marsloting
status: public-free-skill
---

# OpenClaw Ecosystem Monitor

This skill collects metadata-only signals from public OpenClaw ecosystem sources and reports freshness, dependency, and trust signals with canonical source links.

## Use Cases

- Track OpenClaw-related npm package freshness.
- Track public GitHub repository metadata and small contribution candidates.
- Track OpenClaw docs and ClawHub availability/freshness.
- Produce source-linked summaries without copying full issue bodies, README files, docs pages, or package tarballs.

## Data Discipline

Before collecting any source, read `sources/source_quality.yaml`.

Hard rules:

- Use official APIs when available.
- Store only normalized metadata, short summaries, hashes, timestamps, and canonical source URLs.
- Do not store secrets, cookies, access tokens, account IDs, or private user data.
- Do not bulk mirror package tarballs, docs pages, README files, or issue bodies.
- Stop on 403, 429, robots disallow, DMCA/abuse signal, or platform warning.

## Run

From this skill directory:

```bash
node scripts/collect-openclaw-ecosystem.mjs
node scripts/render-demo-report.mjs
```

The collector writes a local JSON snapshot under `data/YYYY-MM-DD/`. The renderer writes a Markdown report under `reports/`.

## Local Runtime

The OpenClaw computer can run this skill without an agent/model turn through:

- `ops/run-openclaw-ecosystem-monitor.sh`

That wrapper only runs the local scripts. It does not post messages, publish reports, call models, or use secrets.

## Trust Requirements

This skill includes the trust and distribution-review docs:

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

## Monetization Boundary

This skill is free/distribution-first. It has no payment code, no checkout, and no paid ClawHub assumption.

No hosted API, checkout, paid listing, invoice flow, or donation link is included.
