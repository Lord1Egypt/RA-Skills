---
name: dns-records
description: Look up DNS records for any domain — A, AAAA, MX, NS, TXT, CNAME, SOA. Use when asked to check DNS records, find a domain's IP address, look up mail servers, check nameservers, or debug DNS configuration. Uses system dig command with Python socket fallback. Zero dependencies.
---

# dnscheck 🔍

DNS record lookup with multi-type support and JSON output.

## Commands

```bash
# Full DNS check (all common record types)
python3 scripts/dnscheck.py github.com openclaw.ai

# Specific record types only
python3 scripts/dnscheck.py -t A MX example.com

# JSON output for scripting
python3 scripts/dnscheck.py --json example.com
```

## Record Types
- **A** — IPv4 addresses
- **AAAA** — IPv6 addresses
- **MX** — Mail servers
- **NS** — Nameservers
- **TXT** — SPF, DKIM, verification records
- **CNAME** — Canonical name aliases
- **SOA** — Start of authority

## Features
- Queries all record types by default
- Uses `dig` when available, falls back to Python sockets for A/AAAA
- JSON output mode for automation
- Multiple domains in one command
