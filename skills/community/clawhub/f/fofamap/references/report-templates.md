# Report Templates

Use this reference when the user wants a polished deliverable, a persuasive analyst write-up, or a report that matches a specific hunt style.

The helper script supports:

- `--report-profile standard`
- `--report-profile attack-infrastructure`
- `--report-profile abnormal-exposure`
- `--report-profile takeover-risk`

If the user does not specify a profile, infer one from the mission. The templates below are not rigid prose blocks. They are evidence structures that should shape how the report is framed.

## Standard

Use for:

- routine asset delivery
- broad recon handoff
- baseline project exports

The report should answer:

- what was searched
- what was found
- which ownership, geography, and service signals matter most
- what the next operator should validate

Good structure:

1. mission and scope
2. exposure snapshot
3. ownership and stack signals
4. evidence sample
5. recommended next actions

## Attack Infrastructure

Use for:

- suspicious infrastructure tracking
- campaign clustering
- offensive tooling discovery
- repeated cloud-hosted operator surface

The report should answer:

- why these assets may belong to a coordinated infrastructure set
- which cloud, ASN, certificate, title, or service patterns repeat
- whether the evidence looks like tooling, staging, redirectors, proxies, or administration surface
- what should be validated before escalation

Good structure:

1. mission and hunt hypothesis
2. clustering signals
3. suspicious surface evidence
4. infrastructure concentration by org, ASN, port, and title
5. validation priorities and caveats

Strong writing moves:

- separate "campaign-style hints" from "confirmed attribution"
- call out repeat patterns, not just raw counts
- treat cloud concentration as a clustering lead, not proof

## Abnormal Exposure

Use for:

- unusual internet-facing surface
- admin panel review
- storage or file leakage
- API and middleware overexposure
- unexpected management or database ports

The report should answer:

- what looks operationally unusual
- which ports, titles, products, or body artifacts make the exposure worth attention
- whether the issue is likely misconfiguration, stale index noise, or true public exposure
- what should be validated first

Good structure:

1. mission and abnormality criteria
2. high-signal ports and products
3. leak-like or admin-like artifacts
4. representative evidence table
5. triage order

Strong writing moves:

- lead with why the exposure is unusual, not only that it exists
- distinguish admin, middleware, database, and storage exposure classes
- keep the validation path concrete and short

## Takeover Risk

Use for:

- dangling domain review
- abandoned platform discovery
- misbound web edge
- placeholder pages and not-found platform errors

The report should answer:

- why the asset may be abandoned or weakly owned
- which platform signals point to an unclaimed or broken deployment
- whether the evidence reflects a real takeover candidate or only a weak hint
- which DNS, CNAME, certificate, or platform checks should follow

Good structure:

1. mission and ownership hypothesis
2. platform-default or placeholder evidence
3. concentration by provider, domain, and hostname pattern
4. candidate table
5. validation workflow

Strong writing moves:

- preserve the exact platform message or title that triggered suspicion
- keep "suspected takeover" separate from "verified takeover condition"
- recommend DNS and platform-control validation before any severity call

## Mode Mapping

- `search` and `search-next`: good for a one-shot report with one profile
- `project-run`: best when the user wants a multi-query deliverable bundle
- `monitor-run`: use the same profile, but emphasize drift, new assets, removed assets, and changed evidence
- `host`: useful when the report is about one node and its likely role
- `stats`: useful when the report is about concentration, spread, and prioritization

## Example Commands

```bash
python3 scripts/fofa_recon.py search \
  --query 'asn="45102" && body="login"' \
  --report-output infra_report.md \
  --report-profile attack-infrastructure

python3 scripts/fofa_recon.py project-run \
  --query 'domain="example.com" && body="ListBucketResult"' \
  --query 'domain="example.com" && title="Site not found · GitHub Pages"' \
  --report-profile takeover-risk

python3 scripts/fofa_recon.py monitor-run \
  --query 'org="Example Corp"' \
  --state-dir results/monitor_example \
  --report-profile abnormal-exposure \
  --report-output results/monitor_example/latest_report.md
```

## Writing Rules

- Make the main judgment short and evidence-backed.
- Separate FOFA indexed evidence from anything that still needs live validation.
- Prefer one strong hypothesis with caveats over five weak claims.
- Keep tables representative, not exhaustive.
- End with a concrete next step list the next operator can actually execute.
