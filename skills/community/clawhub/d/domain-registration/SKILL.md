---
name: Domain Registration
slug: domain-registration
version: 1.0.0
homepage: https://clawic.com/skills/domain-registration
description: Register, transfer, renew, and secure domains across major provider APIs and dashboards with provider-specific workflows and rollback-safe execution.
changelog: Initial release with cross-provider registration playbooks for major registrar APIs, dashboards, transfer flows, and post-purchase security controls.
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["curl","jq","dig","whois"]},"os":["linux","darwin","win32"],"configPaths":["~/domain-registration/"]}}
---

## Setup

On first use, read `setup.md` to align activation boundaries, provider preferences, and approval rules before any registration, transfer, or renewal action.

## When to Use

Use this skill when the user needs domain registration operations across major providers and must choose between API automation and dashboard execution.

Use this for first-time registration, transfer planning, renewals, ownership checks, DNS handoff, and registrar security hardening where billing and service continuity are high impact.

## Architecture

Memory lives in `~/domain-registration/`. See `memory-template.md` for structure and status values.

```text
~/domain-registration/
|-- memory.md              # Provider preferences, risk boundaries, and approval model
|-- inventory.md           # Domain inventory, provider, expiry, and lock status
|-- changes.md             # Registration, transfer, and renewal action log
|-- providers.md           # Account aliases, API readiness, and dashboard access notes
`-- incidents.md           # Failed transfers, renewal misses, and mitigation history
```

## Quick Reference

Use the smallest file needed for the current task.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory structure and status model | `memory-template.md` |
| Provider API and dashboard matrix | `provider-matrix.md` |
| New registration workflows by provider | `registration-playbooks.md` |
| Transfer and renewal execution patterns | `transfer-renewal.md` |
| DNS and account security controls | `dns-security-controls.md` |

## Provider Coverage

This skill covers API and dashboard workflows for major domain providers.

| Provider | API Coverage | Dashboard Coverage | Primary Use Notes |
|----------|--------------|--------------------|-------------------|
| GoDaddy | Public Domains API | Yes | Broad retail registrar operations |
| Namecheap | XML API | Yes | Domain lifecycle plus full DNS replace patterns |
| Route 53 Domains (AWS) | AWS Route53Domains API | Yes | Enterprise workflows via IAM-scoped automation |
| Cloudflare Registrar | DNS and zone API + registrar-adjacent ops | Yes | Registration lifecycle mostly dashboard-driven |
| Google Cloud Domains | Cloud Domains API | Yes | Portfolio management in Google Cloud projects |
| Squarespace Domains | No public registrar API | Yes | Dashboard-only lifecycle for Google Domains migrations |
| Dynadot | Public API | Yes | Cost-efficient registration and renewal workflows |
| Porkbun | Public JSON API | Yes | Fast API-first retail and small portfolio use |
| Name.com | Public REST API | Yes | Programmatic registration and transfer actions |
| Gandi | Public v5 API | Yes | EU-focused registrar and DNS lifecycle controls |
| OVHcloud Domains | Public API | Yes | Regional portfolio with API-backed operations |
| Tucows OpenSRS / Enom | Reseller APIs | Yes (reseller panels) | Reseller and wholesale portfolio operations |

## Core Rules

### 1. Classify Provider and Interface Before Planning
- Identify registrar, account context, and whether the operation should run via API or dashboard.
- If API support is partial, split execution clearly: API for read/validation, dashboard for billing-sensitive writes.

### 2. Run Registration Preflight Every Time
- Validate domain availability from the target registrar directly, then confirm TLD rules, premium status, and renewal price.
- Confirm legal/trademark risk and required contact profile before submitting payment actions.

### 3. Choose the Lowest-Risk Execution Path
- Prefer API for repeatable bulk operations with audit logs; prefer dashboard when provider APIs do not expose required lifecycle steps.
- For first-time provider usage, run one-domain pilot before any batch purchase or transfer.

### 4. Gate Billing and Ownership Actions with Explicit Confirmation
- Registration, transfer, auto-renew changes, and WHOIS contact writes need explicit user confirmation.
- Confirm domain list, years, currency impact, and ownership target before execution.

### 5. Preserve Rollback State Before Mutating DNS or Nameservers
- Snapshot current DNS and nameserver state before transfer or registrar migration.
- Keep rollback-ready records so the prior state can be restored quickly if propagation or ownership validation fails.

### 6. Enforce Registrar Security Baseline Post-Registration
- Enable account 2FA, registrar lock, and renewal monitoring immediately after successful purchase or transfer.
- Add DNSSEC only after authoritative DNS compatibility is confirmed for the target provider.

### 7. Verify Outcomes and Log Durable Context
- Verify success with provider API/dashboard confirmation plus resolver-level checks (`dig`, WHOIS status, nameserver visibility).
- Update `~/domain-registration/` memory files with provider choice, lifecycle dates, and known edge cases.

## Common Traps

- Treating all providers as API-equivalent -> missing lifecycle steps because some registrars are dashboard-only for critical actions.
- Skipping premium renewal checks -> surprise annual billing that exceeds initial purchase assumptions.
- Running batch registration without one-domain pilot -> multiplied failures from bad contact, tax, or payment configuration.
- Forgetting 60-day transfer lock rules -> transfer plans fail despite valid auth codes.
- Replacing DNS records without full snapshot -> incomplete rollback during cutover incidents.
- Enabling DNSSEC before DS/zone readiness -> domain resolution failures after migration.
- Leaving domains without renewal monitoring -> avoidable expiration and brand abuse risk.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://api.godaddy.com | Domain queries, registration and management payloads | GoDaddy API lifecycle operations |
| https://sso.godaddy.com | Authenticated account actions | GoDaddy dashboard operations |
| https://api.namecheap.com/xml.response | Domain and DNS XML parameters | Namecheap API actions |
| https://ap.www.namecheap.com | Account and billing interactions | Namecheap dashboard operations |
| https://route53domains.us-east-1.amazonaws.com | Domain lifecycle API payloads via AWS signatures | Route 53 Domains automation |
| https://console.aws.amazon.com | Account and domain dashboard actions | AWS console execution and validation |
| https://api.cloudflare.com | Zone and registrar-adjacent configuration payloads | Cloudflare DNS and registrar workflow support |
| https://dash.cloudflare.com | Registrar and account dashboard actions | Cloudflare registrar lifecycle tasks |
| https://domains.googleapis.com | Cloud Domains API requests | Google Cloud Domains operations |
| https://console.cloud.google.com | Cloud Domains dashboard actions | Google Cloud portfolio management |
| https://account.squarespace.com | Account and domain dashboard interactions | Squarespace Domains lifecycle actions |
| https://api.dynadot.com | Domain command parameters | Dynadot API operations |
| https://porkbun.com/api/json/v3 | Domain and DNS JSON payloads | Porkbun API lifecycle operations |
| https://api.name.com | Domain, DNS, and transfer payloads | Name.com API actions |
| https://api.gandi.net | Domain and DNS JSON payloads | Gandi v5 API operations |
| https://api.ovh.com | Domain lifecycle API payloads | OVHcloud domain operations |
| https://api.opensrs.com | Reseller domain payloads | Tucows OpenSRS operations |
| https://reseller.enom.com/interface.asp | Reseller panel interactions | Enom dashboard and reseller lifecycle actions |

No other data is sent externally.

## Security & Privacy

Data that leaves your machine:
- Registrar API requests and dashboard session traffic needed for domain lifecycle operations.
- Domain names, contact metadata, and operation parameters required by selected providers.

Data that stays local:
- Operational preferences and provider context in `~/domain-registration/`.
- Change history, rollback state references, and incident notes.

This skill does NOT:
- Execute undeclared endpoints.
- Approve billing-impacting domain actions without explicit confirmation.
- Store credentials in skill files.
- Bypass provider security or anti-abuse controls.

## Trust

This skill can send domain lifecycle data to third-party registrar services when the user approves execution.
Only install if you trust the selected providers and local credential handling practices.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `dns` - DNS records, propagation behavior, and incident troubleshooting
- `api` - API request design, authentication, and failure handling
- `hosting` - Hosting cutovers coordinated with domain and DNS transitions
- `ssl` - Certificate validation and HTTPS recovery after DNS or registrar changes
- `infrastructure` - Environment architecture and operations runbooks

## Feedback

- If useful: `clawhub star domain-registration`
- Stay updated: `clawhub sync`
