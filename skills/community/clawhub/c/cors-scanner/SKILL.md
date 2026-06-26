---
name: cors-scanner
description: Scan web endpoints for CORS misconfigurations. Detect origin reflection, wildcard policies, null origin acceptance, credential leaks, subdomain trust, HTTP origin trust on HTTPS, preflight issues, and private network access. Assign A-F security grades. Use when asked to check CORS, test cross-origin policy, audit CORS headers, scan for CORS vulnerabilities, or check if an API has safe CORS configuration. Triggers on "CORS", "cross-origin", "CORS misconfiguration", "CORS scan", "Access-Control-Allow-Origin", "origin reflection".
---

# CORS Misconfiguration Scanner

Scan web endpoints for dangerous Cross-Origin Resource Sharing policies. Detect misconfigurations that could allow attackers to steal data cross-origin.

## Quick Scan

```bash
python3 scripts/cors_scan.py https://api.example.com
```

## Batch Scan

```bash
python3 scripts/cors_scan.py https://api1.com https://api2.com https://api3.com
```

## Output Formats

```bash
# Text (default)
python3 scripts/cors_scan.py <url>

# JSON
python3 scripts/cors_scan.py <url> --format json

# Markdown report
python3 scripts/cors_scan.py <url> --format markdown
```

## CI/CD Integration

```bash
# Fail if any URL grades below C
python3 scripts/cors_scan.py https://api.example.com --min-grade C
echo $?  # 0 = pass, 1 = fail
```

## What It Checks (13 checks)

| Check | Severity | Description |
|-------|----------|-------------|
| Origin reflection | Critical/High | Server reflects arbitrary Origin back as ACAO |
| Credentials + wildcard | Critical | ACAO: * with ACAC: true (browser-blocked but misconfigured) |
| Null origin accepted | High/Medium | Origin: null trusted (exploitable via sandboxed iframes) |
| HTTP origin on HTTPS | High | HTTPS endpoint trusts HTTP origins (MitM risk) |
| Subdomain wildcard | High | Trusts any subdomain (*.domain.com) |
| Third-party origin | High | Confirms reflection with different attacker domain |
| Private network access | High | Allows external sites to reach internal network |
| Wildcard origin (*) | Medium | ACAO: * on potentially sensitive endpoints |
| Sensitive headers exposed | Medium | Exposes auth/session headers cross-origin |
| Wildcard methods | Medium | ACAM: * allows any HTTP method |
| Wildcard headers | Medium | ACAH: * allows any custom header |
| Missing max-age | Low | No preflight caching, increased latency |
| Clean | Info | No misconfigurations detected |

## Grading

| Grade | Meaning |
|-------|---------|
| A | No CORS issues detected |
| B | Minor issues (low severity) |
| C | Moderate issues (medium severity) |
| D | Serious issues (high severity or multiple medium) |
| F | Critical misconfigurations (origin reflection + credentials) |

## Requirements

- Python 3.6+
- No external dependencies (stdlib only)

## Examples

```
$ python3 scripts/cors_scan.py https://httpbin.org/get
CORS Scan: https://httpbin.org/get
Grade: A
Findings: 0
============================================================

⚪ [INFO] No CORS misconfigurations detected
  The scanned endpoint does not appear to have dangerous CORS policies.
```
