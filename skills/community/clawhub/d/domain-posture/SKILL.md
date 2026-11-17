---
name: domain-posture
description: Audit a domain's email and DNS security posture (SPF, DMARC, DKIM, MX, DNSSEC, CAA, MTA-STS, TLS-RPT, exposed records) and produce a scored, prioritized hardening report. Use when asked to check domain security, email spoofing risk, DMARC/SPF/DKIM setup, or DNS hygiene for any domain.
---

# Domain Posture Audit

Audits the public email/DNS security posture of one or more domains. Pure DNS —
no API keys, no third-party services, no intrusive scanning. Read-only and safe
to run against any domain you own or are authorized to assess.

## What it checks

| Area | Records / signals |
|---|---|
| Email auth | SPF (existence, ~all/-all/all, lookup count, +all), DMARC (p=, sp=, pct, rua/ruf, fo), DKIM on common selectors (google, selector1/selector2, default, mail, s1/s2) |
| Transport | MX (provider detection, dangling/subdomain MX), MTA-STS (_mta-sts policy + mta-sts TXT), TLS-RPT (_smtp._tls) |
| DNS integrity | DNSSEC (DS + RRSIG presence), CAA (issuers, accounturl/critical flags), zone NS diversity |
| Exposure signals | Common sensitive subdomains from a wordlist pass (staging, dev, vpn, admin, gitlab, jenkins...), wildcard DNS detection, dangling CNAME to unclaimed buckets/CDNs (basic heuristic) |

## How to run

```bash
python3 scripts/domain_posture.py example.com [more.domains ...]
```

Requirements: Python 3.9+, `dnspython` (`pip install dnspython`). The script
falls back to `dig` if dnspython is missing, but installing it is recommended.

Options:
- `--json` — machine-readable output
- `--wordlist path` — custom subdomain wordlist (default bundled shortlist)
- `--no-subdomains` — skip the subdomain pass (faster, quieter)

## Output

A per-domain report with:
- **Score 0-100** across four pillars (Email Auth, Transport, DNS Integrity, Exposure)
- **Findings**, each tagged `critical` / `warning` / `info`
- **Prioritized fix list** — cheapest highest-impact fixes first, with the exact
  record to publish

## Rules

- Only audit domains you own or are explicitly authorized to test. This does
  passive DNS lookups only — no brute force, no scanning, no sending email.
- Never hardcode secrets. This skill needs none.
- If the user asks you to "fix" findings, draft the DNS records for them to
  publish; do not claim changes were applied — DNS is read-only from here.

## Interpreting the score

- 90-100: tight. Look at `info` items only.
- 70-89: standard gaps. Fix `warning` items first.
- <70: spoofable or misconfigured email, or DNSSEC/CAA missing on a domain
  that should have them. Start with every `critical`.
