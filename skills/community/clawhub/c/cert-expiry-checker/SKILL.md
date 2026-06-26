---
name: ssl-checker
description: "SSL/TLS certificate expiry checker and domain health monitor. Check certificate expiration, issuer details, SAN entries, and chain validity for one or multiple domains. Use when Codex needs to: (1) Check SSL cert expiry dates, (2) Monitor multiple domains for upcoming certificate renewal, (3) Generate HTML certificate status reports, (4) Validate SSL configuration on non-standard ports, (5) Audit domain security posture before deployment."
---

# SSL Certificate Checker (ssl-checker)

Check SSL/TLS certificate status for any domain with concurrent scanning, HTML reports, and JSON output.

## Quick start

```bash
python3 skills/ssl-checker/scripts/check_ssl.py example.com
```

Output:
```
🔍 Checking 1 domain(s)...
  [1/1] 🟢 example.com: valid (87d)

Hostname       Port   Status        Days Left   Issuer              Expiry Date
========================================================================================================
example.com    443    🟢 Valid      87          Let's Encrypt       2026-08-10

📊 Summary: 1 healthy, 0 warnings, 0 errors — 1 total
```

## Commands

| Command | Description |
|---------|-------------|
| `python3 check_ssl.py example.com` | Check one domain |
| `python3 check_ssl.py domain1.com domain2.com` | Check multiple domains |
| `python3 check_ssl.py --file domains.txt` | Check domains from file |
| `python3 check_ssl.py example.com --port 8443` | Custom port |
| `python3 check_ssl.py example.com --json` | JSON output |
| `python3 check_ssl.py example.com --report` | HTML report |
| `python3 check_ssl.py --output report.html --report` | Custom output path |
| `python3 check_ssl.py --threads 20` | Concurrent checks (default: 10) |

### Domains file format

```
# domains.txt
example.com
google.com
mysite.io:8443
```

## Status levels

| Level | Days Remaining | Badge |
|-------|---------------|-------|
| ✅ Valid | > 60 days | 🟢 |
| 🟡 Expiring Soon | 31–60 days | 🟡 |
| 🟠 Warning | 15–30 days | 🟠 |
| 🔴 Critical | ≤ 14 days | 🔴 |
| ⛔ Expired | < 0 days | ⛔ |

## Exit codes

- **0**: All healthy
- **1**: Any warnings
- **2**: Any critical or expired (useful for CI/CD gating)

## HTML Reports

Generates a styled Bootstrap report with status badges, SAN details, and issuer info:

```bash
python3 skills/ssl-checker/scripts/check_ssl.py --file domains.txt --report
# Creates: ssl-report-20260515-090500.html
```

## JSON Output

For programmatic consumption and monitoring integrations:

```bash
python3 skills/ssl-checker/scripts/check_ssl.py example.com --json
```

## Requirements

- Python 3.6+ (stdlib only — no pip required)
- Network access to target domains
- Works on Linux, macOS, Windows
