---
name: network-diag
description: Network diagnostics: ping, DNS, port check, traceroute
---

# network-diag

Run network diagnostics including ping, DNS resolution, port checks, and traceroute.

## Usage

```bash
# Quick connectivity check
python3 scripts/netdiag.py check google.com

# Check if a port is open
python3 scripts/netdiag.py port example.com 443

# DNS resolution
python3 scripts/netdiag.py dns example.com

# Full diagnostic report
python3 scripts/netdiag.py full example.com
```

## Commands

- `check <host>` — Ping-style connectivity check
- `port <host> <port>` — Check if a TCP port is open
- `dns <host>` — Resolve DNS for a hostname
- `full <host>` — Run all diagnostics on a host
