#!/usr/bin/env python3
"""Test, debug, and generate CORS configurations."""

import argparse
import sys
import json
import urllib.request
import urllib.error
from textwrap import dedent

# ── Test ────────────────────────────────────────────────────────────────────

def cmd_test(args):
    url = args.url
    origin = args.origin
    method = args.method or "GET"

    headers = {"Origin": origin}
    req = urllib.request.Request(url, headers=headers, method=method)

    try:
        resp = urllib.request.urlopen(req, timeout=15)
    except urllib.error.HTTPError as e:
        resp = e
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    resp_headers = dict(resp.headers)

    print(f"URL: {url}")
    print(f"Origin: {origin}")
    print(f"Method: {method}")
    print(f"Status: {resp.status if hasattr(resp, 'status') else resp.code}")
    print()

    # CORS headers
    cors_keys = [
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Credentials",
        "Access-Control-Expose-Headers",
        "Access-Control-Allow-Methods",
        "Access-Control-Allow-Headers",
        "Access-Control-Max-Age",
        "Vary",
    ]

    found_any = False
    for key in cors_keys:
        val = resp_headers.get(key)
        if val:
            found_any = True
            print(f"  {key}: {val}")

    if not found_any:
        print("  ⚠ No CORS headers found in response.")
        print("  The server may not support CORS or doesn't allow this origin.")
    else:
        acao = resp_headers.get("Access-Control-Allow-Origin", "")
        if acao == "*":
            print("\n  ✓ Origin allowed (wildcard)")
        elif acao == origin:
            print(f"\n  ✓ Origin '{origin}' is explicitly allowed")
        elif acao:
            print(f"\n  ✗ Origin mismatch: server allows '{acao}', tested '{origin}'")
        else:
            print("\n  ✗ No Access-Control-Allow-Origin header — CORS will fail in browsers")

    if args.verbose:
        print("\n── All Response Headers ──")
        for k, v in sorted(resp_headers.items()):
            print(f"  {k}: {v}")


# ── Preflight ───────────────────────────────────────────────────────────────

def cmd_preflight(args):
    url = args.url
    origin = args.origin
    method = args.method or "POST"
    custom_headers = args.header or []

    req_headers = {
        "Origin": origin,
        "Access-Control-Request-Method": method,
    }
    if custom_headers:
        req_headers["Access-Control-Request-Headers"] = ", ".join(custom_headers)

    req = urllib.request.Request(url, headers=req_headers, method="OPTIONS")

    try:
        resp = urllib.request.urlopen(req, timeout=15)
    except urllib.error.HTTPError as e:
        resp = e
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    resp_headers = dict(resp.headers)
    status = resp.status if hasattr(resp, "status") else resp.code

    print(f"Preflight OPTIONS → {url}")
    print(f"Origin: {origin}")
    print(f"Requested Method: {method}")
    if custom_headers:
        print(f"Requested Headers: {', '.join(custom_headers)}")
    print(f"Status: {status}")
    print()

    acao = resp_headers.get("Access-Control-Allow-Origin", "")
    acam = resp_headers.get("Access-Control-Allow-Methods", "")
    acah = resp_headers.get("Access-Control-Allow-Headers", "")
    acma = resp_headers.get("Access-Control-Max-Age", "")
    acac = resp_headers.get("Access-Control-Allow-Credentials", "")

    results = []
    # Check origin
    if acao == "*" or acao == origin:
        results.append(("✓", f"Origin allowed: {acao}"))
    elif acao:
        results.append(("✗", f"Origin mismatch: {acao} (expected {origin})"))
    else:
        results.append(("✗", "No Access-Control-Allow-Origin header"))

    # Check method
    if acam:
        allowed_methods = [m.strip().upper() for m in acam.split(",")]
        if method.upper() in allowed_methods or "*" in allowed_methods:
            results.append(("✓", f"Method '{method}' allowed: {acam}"))
        else:
            results.append(("✗", f"Method '{method}' NOT in allowed: {acam}"))
    else:
        results.append(("⚠", "No Access-Control-Allow-Methods header"))

    # Check headers
    if custom_headers:
        if acah:
            allowed_h = [h.strip().lower() for h in acah.split(",")]
            for h in custom_headers:
                if h.lower() in allowed_h or "*" in allowed_h:
                    results.append(("✓", f"Header '{h}' allowed"))
                else:
                    results.append(("✗", f"Header '{h}' NOT in allowed: {acah}"))
        else:
            results.append(("⚠", "No Access-Control-Allow-Headers header"))

    if acma:
        results.append(("ℹ", f"Preflight cache: {acma}s"))
    if acac:
        results.append(("ℹ", f"Credentials: {acac}"))

    for symbol, msg in results:
        print(f"  {symbol} {msg}")


# ── Audit ───────────────────────────────────────────────────────────────────

def cmd_audit(args):
    url = args.url
    origins_to_test = [
        "https://evil.com",
        "https://attacker.example.com",
        "null",
    ]

    print(f"CORS Security Audit: {url}\n")
    issues = []

    for test_origin in origins_to_test:
        headers = {"Origin": test_origin}
        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            resp = urllib.request.urlopen(req, timeout=10)
        except urllib.error.HTTPError as e:
            resp = e
        except Exception as e:
            print(f"  ⚠ Could not reach {url}: {e}")
            return

        resp_headers = dict(resp.headers)
        acao = resp_headers.get("Access-Control-Allow-Origin", "")
        acac = resp_headers.get("Access-Control-Allow-Credentials", "")
        vary = resp_headers.get("Vary", "")

        if acao == test_origin:
            issues.append(f"CRITICAL: Server reflects arbitrary origin '{test_origin}' — origin reflection vulnerability")
            if acac and acac.lower() == "true":
                issues.append(f"CRITICAL: Credentials allowed with reflected origin '{test_origin}' — full CORS bypass")

        if acao == "*":
            if acac and acac.lower() == "true":
                issues.append("HIGH: Wildcard origin (*) with credentials — browsers will block but config is invalid")
            else:
                issues.append("INFO: Wildcard origin (*) — any site can read responses (no credentials)")

        if acao == "null":
            issues.append("HIGH: 'null' origin allowed — sandboxed iframes and data: URLs can access this resource")

    # Check preflight
    req = urllib.request.Request(url, headers={"Origin": "https://evil.com", "Access-Control-Request-Method": "PUT"}, method="OPTIONS")
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        resp_headers = dict(resp.headers)
        acam = resp_headers.get("Access-Control-Allow-Methods", "")
        acma = resp_headers.get("Access-Control-Max-Age", "")
        vary = resp_headers.get("Vary", "")

        if acam and ("*" in acam or len(acam.split(",")) > 5):
            issues.append(f"MEDIUM: Overly permissive methods: {acam}")
        if not acma:
            issues.append("LOW: No Access-Control-Max-Age — preflight requests on every call (performance)")
        if "Origin" not in vary and resp_headers.get("Access-Control-Allow-Origin", "") not in ("*", ""):
            issues.append("LOW: Missing 'Vary: Origin' — caching proxies may serve wrong CORS headers")
    except Exception:
        pass  # Preflight not supported is fine

    if issues:
        for issue in issues:
            severity = issue.split(":")[0]
            marker = {"CRITICAL": "✗", "HIGH": "✗", "MEDIUM": "⚠", "LOW": "ℹ", "INFO": "ℹ"}.get(severity, "·")
            print(f"  {marker} {issue}")
        print(f"\nFound {len(issues)} issue(s).")
    else:
        print("  ✓ No CORS security issues detected.")


# ── Config Generator ────────────────────────────────────────────────────────

CONFIGS = {
    "nginx": lambda o, m, h, c, ma: dedent(f"""\
        # Nginx CORS configuration
        location / {{
            if ($request_method = 'OPTIONS') {{
                add_header 'Access-Control-Allow-Origin' '{o}';
                add_header 'Access-Control-Allow-Methods' '{m}';
                add_header 'Access-Control-Allow-Headers' '{h}';
                {"add_header 'Access-Control-Allow-Credentials' 'true';" if c else ""}
                add_header 'Access-Control-Max-Age' {ma};
                add_header 'Content-Type' 'text/plain; charset=utf-8';
                add_header 'Content-Length' 0;
                return 204;
            }}
            add_header 'Access-Control-Allow-Origin' '{o}';
            {"add_header 'Access-Control-Allow-Credentials' 'true';" if c else ""}
        }}"""),

    "apache": lambda o, m, h, c, ma: dedent(f"""\
        # Apache .htaccess CORS configuration
        <IfModule mod_headers.c>
            Header set Access-Control-Allow-Origin "{o}"
            Header set Access-Control-Allow-Methods "{m}"
            Header set Access-Control-Allow-Headers "{h}"
            {"Header set Access-Control-Allow-Credentials true" if c else ""}
            Header set Access-Control-Max-Age "{ma}"
        </IfModule>"""),

    "express": lambda o, m, h, c, ma: dedent(f"""\
        // Express.js CORS middleware
        const cors = require('cors');
        app.use(cors({{
          origin: {json.dumps(o.split(',') if ',' in o else o)},
          methods: {json.dumps(m.split(','))},
          allowedHeaders: {json.dumps(h.split(','))},
          credentials: {json.dumps(c)},
          maxAge: {ma}
        }}));"""),

    "flask": lambda o, m, h, c, ma: dedent(f"""\
        # Flask-CORS configuration
        from flask_cors import CORS
        CORS(app, resources={{r"/*": {{
            "origins": {json.dumps(o.split(',') if ',' in o else [o])},
            "methods": {json.dumps(m.split(','))},
            "allow_headers": {json.dumps(h.split(','))},
            "supports_credentials": {'True' if c else 'False'},
            "max_age": {ma}
        }}}})"""),

    "fastapi": lambda o, m, h, c, ma: dedent(f"""\
        # FastAPI CORS middleware
        from fastapi.middleware.cors import CORSMiddleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins={json.dumps(o.split(',') if ',' in o else [o])},
            allow_methods={json.dumps(m.split(','))},
            allow_headers={json.dumps(h.split(','))},
            allow_credentials={'True' if c else 'False'},
            max_age={ma},
        )"""),

    "rails": lambda o, m, h, c, ma: dedent(f"""\
        # config/initializers/cors.rb
        Rails.application.config.middleware.insert_before 0, Rack::Cors do
          allow do
            origins {', '.join(f"'{x.strip()}'" for x in o.split(','))}
            resource '*',
              headers: :any,
              methods: [{', '.join(f':{x.strip().lower()}' for x in m.split(','))}],
              credentials: {'true' if c else 'false'},
              max_age: {ma}
          end
        end"""),
}

def cmd_config(args):
    framework = args.framework
    if framework not in CONFIGS:
        print(f"Error: Unknown framework '{framework}'. Available: {', '.join(CONFIGS.keys())}", file=sys.stderr)
        sys.exit(1)

    origins = args.origins or "*"
    methods = args.methods or "GET,POST,OPTIONS"
    headers = args.headers or "Content-Type,Authorization"
    credentials = args.credentials
    max_age = args.max_age or 86400

    output = CONFIGS[framework](origins, methods, headers, credentials, max_age)
    print(output)


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Test, debug, and generate CORS configurations.")
    sub = parser.add_subparsers(dest="command", help="Command")

    # test
    t = sub.add_parser("test", help="Test CORS headers on a URL")
    t.add_argument("url", help="URL to test")
    t.add_argument("--origin", required=True, help="Origin header to send")
    t.add_argument("--method", default="GET", help="HTTP method (default: GET)")
    t.add_argument("--verbose", action="store_true", help="Show all response headers")

    # preflight
    p = sub.add_parser("preflight", help="Send OPTIONS preflight request")
    p.add_argument("url", help="URL to test")
    p.add_argument("--origin", required=True, help="Origin header")
    p.add_argument("--method", default="POST", help="Method to request")
    p.add_argument("--header", action="append", help="Custom header (repeatable)")

    # audit
    a = sub.add_parser("audit", help="Audit CORS security")
    a.add_argument("url", help="URL to audit")

    # config
    c = sub.add_parser("config", help="Generate CORS config for a framework")
    c.add_argument("--framework", required=True, choices=list(CONFIGS.keys()), help="Target framework")
    c.add_argument("--origins", help="Comma-separated allowed origins")
    c.add_argument("--methods", help="Comma-separated methods")
    c.add_argument("--headers", help="Comma-separated allowed headers")
    c.add_argument("--credentials", action="store_true", help="Allow credentials")
    c.add_argument("--max-age", type=int, default=86400, help="Preflight cache seconds")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    {"test": cmd_test, "preflight": cmd_preflight, "audit": cmd_audit, "config": cmd_config}[args.command](args)


if __name__ == "__main__":
    main()
