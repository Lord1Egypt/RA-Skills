---
name: domain-checker
description: Check whether domain names are available for registration. Use when a user asks to verify domain availability, find unregistered domains, brainstorm project/brand names with domain checks, or any task involving "is this domain taken?". Supports .com, .net, .org, .io, .ai, .so, and other TLDs. Cross-verifies via whois + DNS NS + DNS A records for reliable results.
---

# Domain Checker

Check domain availability using `whois` + DNS cross-verification. Single source of truth for all domain availability queries.

## Quick Start

Run the Python script (no system dependencies — no `whois`/`dig` CLI needed):

```bash
python3 scripts/check_domains.py example.com myproject.io brand.ai
```

Or pipe a list:

```bash
echo "foo.com bar.ai baz.io" | python3 scripts/check_domains.py
```

Legacy bash script (requires `whois` + `dig` CLI):

```bash
bash scripts/check_domains.sh example.com myproject.io brand.ai
```

## Output Format

Each domain gets one of three verdicts:

| Symbol | Meaning | Confidence |
|--------|---------|-----------|
| ✅ AVAILABLE | whois says "not found" AND no DNS NS records | High |
| ❌ TAKEN | whois shows Creation Date OR DNS records exist | High |
| ⚠️ LIKELY TAKEN | Conflicting signals (whois unclear but DNS exists) | Medium |
| ❓ UNKNOWN | whois returned no data — verify manually | Low |

## How It Works

Three independent signals are cross-verified:

1. **whois Creation Date** — Most authoritative. If present, domain is taken.
2. **DNS NS records** — Registered domains almost always have nameservers.
3. **DNS A records** — Fallback signal for parked/active domains.

A domain is only marked AVAILABLE when whois explicitly says "not found" AND no DNS records exist. This eliminates false positives from unreliable whois web interfaces.

## Important Notes

- **Rate limiting**: The script waits 1 second between queries to avoid whois server throttling. For large batches (>50), consider splitting into multiple runs.
- **whois web interfaces are unreliable**: Sites like whois.com often return stale/incorrect data. This script uses the `whois` CLI directly.
- **.ai TLD quirk**: The .ai whois server sometimes returns sparse data. The script handles this by also checking DNS.
- **Premium/aftermarket domains**: A domain may be "available" in whois but listed at a premium price on registrars. The script cannot detect this — check the registrar for actual purchase price.
- **Python script**: No system dependencies — uses stdlib `socket` for whois (port 43) and DNS resolution.
- **Bash script** (legacy): Requires `whois` and `dig` CLI tools (pre-installed on most Linux/macOS systems).

## Batch Domain Brainstorming

When helping users brainstorm project names with domain checks, use this workflow:

1. Generate 15-30 candidate names based on user criteria
2. Run all candidates through the script in one batch
3. Present only the AVAILABLE results with analysis
4. Iterate on available candidates if needed

Example:

```bash
python3 scripts/check_domains.py myapp.com myapp.ai myapp.io coolname.com coolname.ai
```
