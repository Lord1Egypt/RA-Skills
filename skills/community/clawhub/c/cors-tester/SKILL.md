---
name: cors-tester
description: Test and debug CORS (Cross-Origin Resource Sharing) configurations on live URLs. Use when checking if a server returns correct CORS headers, debugging CORS errors, testing preflight OPTIONS requests, verifying allowed origins/methods/headers, or auditing CORS security posture. Also use when generating CORS configurations for Apache, Nginx, Express, or other frameworks.
---

# cors-tester

Test, debug, and generate CORS configurations from the command line.

## Quick Start

```bash
# Test CORS headers on a URL
python3 scripts/cors_tester.py test https://api.example.com/data --origin https://myapp.com

# Test preflight (OPTIONS) request
python3 scripts/cors_tester.py preflight https://api.example.com/data --origin https://myapp.com --method POST --header "Content-Type"

# Generate CORS config for a framework
python3 scripts/cors_tester.py config --framework nginx --origins "https://myapp.com,https://staging.myapp.com" --methods "GET,POST,PUT,DELETE"

# Audit CORS security
python3 scripts/cors_tester.py audit https://api.example.com/data
```

## Commands

### `test`
Send a request with an Origin header and inspect the CORS response headers.

```bash
python3 scripts/cors_tester.py test <url> --origin <origin> [--method GET]
```

Options:
- `--origin <url>` — Origin to test (required)
- `--method <method>` — HTTP method (default: GET)
- `--verbose` — Show all response headers

Output shows:
- `Access-Control-Allow-Origin` — Whether the origin is allowed
- `Access-Control-Allow-Credentials` — Whether credentials are supported
- `Access-Control-Expose-Headers` — Which headers are exposed

### `preflight`
Send an OPTIONS preflight request to test if a cross-origin request would be allowed.

```bash
python3 scripts/cors_tester.py preflight <url> --origin <origin> [--method POST] [--header Content-Type]
```

Options:
- `--origin <url>` — Origin to test (required)
- `--method <method>` — Method to request (default: POST)
- `--header <name>` — Custom header to request (repeatable)

Output shows:
- `Access-Control-Allow-Methods` — Allowed methods
- `Access-Control-Allow-Headers` — Allowed headers
- `Access-Control-Max-Age` — Preflight cache duration

### `audit`
Check a URL for common CORS misconfigurations and security issues.

```bash
python3 scripts/cors_tester.py audit <url>
```

Checks for:
- Wildcard origin (`*`) with credentials
- Origin reflection (server echoes any origin back)
- Missing `Vary: Origin` header
- Overly permissive allowed methods
- Missing preflight cache (`Access-Control-Max-Age`)

### `config`
Generate CORS configuration snippets for common frameworks.

```bash
python3 scripts/cors_tester.py config --framework <name> --origins <origins> [--methods <methods>] [--headers <headers>] [--credentials]
```

Options:
- `--framework <name>` — Target: `nginx`, `apache`, `express`, `flask`, `fastapi`, `rails`
- `--origins <csv>` — Comma-separated allowed origins
- `--methods <csv>` — Comma-separated methods (default: `GET,POST,OPTIONS`)
- `--headers <csv>` — Comma-separated allowed headers (default: `Content-Type,Authorization`)
- `--credentials` — Allow credentials
- `--max-age <seconds>` — Preflight cache (default: 86400)
