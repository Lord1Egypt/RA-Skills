# Sanitized Demo Report

Status: local distribution-review sample.

This demo shows the report shape without private data, credentials, payment data, KYC data, cookies, full issue bodies, README bodies, docs pages, package tarballs, or release files.

## Snapshot

| Signal | Example |
|---|---|
| Repository | OpenClaw public GitHub metadata |
| Package freshness | public npm package version and timestamp metadata |
| Candidate review | issue number, title, timestamp, and source URL only |
| Source quality | status code, robots result, timestamp, and canonical URL |

## Example Output Shape

```text
OpenClaw Ecosystem Monitor

- Repository signal: public stars/forks/issues/subscribers
- Package signal: public versions, timestamps, and weekly download counts
- Candidate signal: source-linked issue metadata for human review
- Warnings: none, or a pause trigger such as 403/429/robots disallow
```

## Redaction Rules

- Keep source links.
- Keep short metadata and timestamps.
- Do not copy full source text.
- Do not include private accounts, tokens, cookies, emails, payment data, KYC data, or raw user content.
- Stop and review before any public listing or hosted monetization.
