#!/usr/bin/env python3
"""CORS Misconfiguration Scanner — detect dangerous CORS policies on web endpoints."""

import argparse
import json
import sys
import urllib.request
import urllib.error
import ssl
from urllib.parse import urlparse

__version__ = "1.0.0"

# --- CORS checks ---

CHECKS = [
    "wildcard_origin",
    "origin_reflection",
    "null_origin",
    "credentials_with_wildcard",
    "subdomain_wildcard",
    "http_origin_trusted",
    "third_party_origin",
    "preflight_missing",
    "expose_headers_excessive",
    "max_age_missing",
    "methods_wildcard",
    "headers_wildcard",
    "private_network_access",
]

SEVERITY = {
    "critical": 4,
    "high": 3,
    "medium": 2,
    "low": 1,
    "info": 0,
}

TEST_ORIGINS = [
    "https://evil.com",
    "https://attacker.example.com",
    "null",
    "http://localhost",
    "https://sub.{domain}",
    "http://{domain}",
]


def make_request(url, origin=None, method="GET", timeout=10):
    """Send HTTP request with optional Origin header, return headers dict."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    headers = {"User-Agent": "CORS-Scanner/1.0"}
    if origin:
        headers["Origin"] = origin

    req = urllib.request.Request(url, headers=headers, method=method)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        resp_headers = {k.lower(): v for k, v in resp.getheaders()}
        return resp.getcode(), resp_headers
    except urllib.error.HTTPError as e:
        resp_headers = {k.lower(): v for k, v in e.headers.items()}
        return e.code, resp_headers
    except Exception as e:
        return None, {"error": str(e)}


def get_domain(url):
    parsed = urlparse(url)
    return parsed.hostname or ""


def scan_cors(url, timeout=10, verbose=False):
    """Run all CORS checks against a URL. Returns list of findings."""
    findings = []
    domain = get_domain(url)

    def add(check_id, severity, title, detail, evidence=""):
        findings.append({
            "check": check_id,
            "severity": severity,
            "title": title,
            "detail": detail,
            "evidence": evidence,
        })

    # 1. Baseline request (no Origin)
    code_base, h_base = make_request(url, timeout=timeout)
    if code_base is None:
        add("connection_error", "critical", "Connection failed",
            f"Could not connect to {url}: {h_base.get('error', 'unknown')}")
        return findings

    acao_base = h_base.get("access-control-allow-origin", "")

    # 2. Check wildcard origin (*)
    if acao_base == "*":
        acac = h_base.get("access-control-allow-credentials", "").lower()
        if acac == "true":
            add("credentials_with_wildcard", "critical",
                "Credentials allowed with wildcard origin",
                "Access-Control-Allow-Origin: * combined with Access-Control-Allow-Credentials: true. "
                "Browsers block this, but it indicates a misconfigured server that may accept credentials with reflected origins.",
                f"ACAO: {acao_base}, ACAC: {acac}")
        else:
            add("wildcard_origin", "medium",
                "Wildcard Access-Control-Allow-Origin",
                "Server returns Access-Control-Allow-Origin: * which allows any website to read responses. "
                "This is acceptable for public APIs but dangerous if the endpoint returns user-specific data.",
                f"ACAO: {acao_base}")

    # 3. Test origin reflection (evil.com)
    evil_origin = "https://evil.com"
    code_evil, h_evil = make_request(url, origin=evil_origin, timeout=timeout)
    if code_evil:
        acao_evil = h_evil.get("access-control-allow-origin", "")
        acac_evil = h_evil.get("access-control-allow-credentials", "").lower()
        if acao_evil == evil_origin:
            sev = "critical" if acac_evil == "true" else "high"
            add("origin_reflection", sev,
                "Origin reflection detected",
                f"Server reflects arbitrary Origin header back as Access-Control-Allow-Origin. "
                f"Any website can read responses from this endpoint."
                f"{' WITH credentials — full account takeover possible.' if acac_evil == 'true' else ''}",
                f"Sent Origin: {evil_origin} → ACAO: {acao_evil}, ACAC: {acac_evil}")

    # 4. Test null origin
    code_null, h_null = make_request(url, origin="null", timeout=timeout)
    if code_null:
        acao_null = h_null.get("access-control-allow-origin", "")
        acac_null = h_null.get("access-control-allow-credentials", "").lower()
        if acao_null == "null":
            sev = "high" if acac_null == "true" else "medium"
            add("null_origin", sev,
                "Null origin accepted",
                "Server allows Origin: null, which can be triggered from sandboxed iframes, "
                "data: URIs, and local files. Attackers can exploit this to bypass CORS restrictions.",
                f"Sent Origin: null → ACAO: {acao_null}, ACAC: {acac_null}")

    # 5. Test HTTP (non-HTTPS) origin trust
    if url.startswith("https://"):
        http_origin = f"http://{domain}"
        code_http, h_http = make_request(url, origin=http_origin, timeout=timeout)
        if code_http:
            acao_http = h_http.get("access-control-allow-origin", "")
            if acao_http == http_origin:
                add("http_origin_trusted", "high",
                    "HTTP origin trusted by HTTPS endpoint",
                    "HTTPS endpoint trusts an HTTP origin, enabling MitM attacks "
                    "where an attacker on the network can inject scripts via HTTP and steal data from HTTPS.",
                    f"Sent Origin: {http_origin} → ACAO: {acao_http}")

    # 6. Test subdomain wildcard pattern
    sub_origin = f"https://evil.{domain}"
    code_sub, h_sub = make_request(url, origin=sub_origin, timeout=timeout)
    if code_sub:
        acao_sub = h_sub.get("access-control-allow-origin", "")
        if acao_sub == sub_origin:
            add("subdomain_wildcard", "high",
                "Subdomain-based origin accepted",
                f"Server trusts any subdomain origin (*.{domain}). If any subdomain is compromised "
                f"(XSS, takeover), the attacker can read cross-origin responses.",
                f"Sent Origin: {sub_origin} → ACAO: {acao_sub}")

    # 7. Test third-party origin (attacker.example.com)
    third_origin = "https://attacker.example.com"
    code_third, h_third = make_request(url, origin=third_origin, timeout=timeout)
    if code_third:
        acao_third = h_third.get("access-control-allow-origin", "")
        if acao_third == third_origin and acao_third != evil_origin:
            add("third_party_origin", "high",
                "Third-party origin accepted",
                "Server reflects a different attacker-controlled origin. "
                "Confirms origin reflection is not just for evil.com.",
                f"Sent Origin: {third_origin} → ACAO: {acao_third}")

    # 8. Preflight check (OPTIONS)
    code_opt, h_opt = make_request(url, origin=evil_origin, method="OPTIONS", timeout=timeout)
    if code_opt:
        acam = h_opt.get("access-control-allow-methods", "")
        acah = h_opt.get("access-control-allow-headers", "")
        acao_opt = h_opt.get("access-control-allow-origin", "")
        acma = h_opt.get("access-control-max-age", "")

        if acam == "*" or "*, " in acam:
            add("methods_wildcard", "medium",
                "Wildcard methods in preflight",
                "Access-Control-Allow-Methods includes wildcard (*). "
                "This allows any HTTP method including PUT, DELETE, PATCH.",
                f"ACAM: {acam}")

        if acah == "*" or "*, " in acah:
            add("headers_wildcard", "medium",
                "Wildcard headers in preflight",
                "Access-Control-Allow-Headers includes wildcard (*). "
                "This allows any custom header to be sent cross-origin.",
                f"ACAH: {acah}")

        if not acma and acao_opt:
            add("max_age_missing", "low",
                "No Access-Control-Max-Age",
                "Preflight responses should include Access-Control-Max-Age to cache preflight results. "
                "Without it, browsers send a preflight for every cross-origin request, increasing latency.",
                "ACMA: (not set)")

    # 9. Check exposed headers
    aceh = h_base.get("access-control-expose-headers", "")
    if aceh:
        exposed = [h.strip() for h in aceh.split(",")]
        sensitive = [h for h in exposed if h.lower() in (
            "authorization", "set-cookie", "x-api-key", "x-csrf-token",
            "x-auth-token", "cookie", "x-session-id")]
        if sensitive:
            add("expose_headers_excessive", "medium",
                "Sensitive headers exposed cross-origin",
                f"Access-Control-Expose-Headers includes sensitive headers: {', '.join(sensitive)}. "
                "This allows cross-origin scripts to read these values.",
                f"ACEH: {aceh}")

    # 10. Private Network Access
    pna = h_base.get("access-control-allow-private-network", "")
    if pna.lower() == "true":
        add("private_network_access", "high",
            "Private network access allowed",
            "Access-Control-Allow-Private-Network: true allows external websites to make "
            "requests to internal network resources through the user's browser.",
            f"ACAPN: {pna}")

    # Add info if no issues found
    if not findings:
        add("clean", "info", "No CORS misconfigurations detected",
            "The scanned endpoint does not appear to have dangerous CORS policies. "
            "No origin reflection, wildcard, or null origin acceptance was detected.", "")

    return findings


def grade_findings(findings):
    """Assign A-F grade based on findings severity."""
    if not findings or (len(findings) == 1 and findings[0]["check"] == "clean"):
        return "A"

    max_sev = max(SEVERITY.get(f["severity"], 0) for f in findings)
    count = len([f for f in findings if f["severity"] != "info"])

    if max_sev >= 4 or count >= 4:
        return "F"
    elif max_sev >= 3 and count >= 2:
        return "D"
    elif max_sev >= 3:
        return "D"
    elif max_sev >= 2 and count >= 3:
        return "D"
    elif max_sev >= 2:
        return "C"
    elif max_sev >= 1 and count >= 2:
        return "C"
    elif max_sev >= 1:
        return "B"
    return "A"


def format_text(url, findings, grade):
    """Format results as human-readable text."""
    lines = []
    lines.append(f"CORS Scan: {url}")
    lines.append(f"Grade: {grade}")
    lines.append(f"Findings: {len([f for f in findings if f['severity'] != 'info'])}")
    lines.append("=" * 60)

    severity_order = ["critical", "high", "medium", "low", "info"]
    sorted_findings = sorted(findings, key=lambda f: severity_order.index(f["severity"]))

    for f in sorted_findings:
        sev_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵", "info": "⚪"}.get(f["severity"], "⚪")
        lines.append(f"\n{sev_icon} [{f['severity'].upper()}] {f['title']}")
        lines.append(f"  {f['detail']}")
        if f["evidence"]:
            lines.append(f"  Evidence: {f['evidence']}")

    lines.append("")
    return "\n".join(lines)


def format_json(url, findings, grade):
    """Format results as JSON."""
    return json.dumps({
        "url": url,
        "grade": grade,
        "findings_count": len([f for f in findings if f["severity"] != "info"]),
        "findings": findings,
    }, indent=2)


def format_markdown(url, findings, grade):
    """Format results as Markdown."""
    lines = []
    lines.append(f"# CORS Scan Report: {url}")
    lines.append(f"\n**Grade:** {grade}")
    lines.append(f"**Issues Found:** {len([f for f in findings if f['severity'] != 'info'])}")
    lines.append("")

    severity_order = ["critical", "high", "medium", "low", "info"]
    sorted_findings = sorted(findings, key=lambda f: severity_order.index(f["severity"]))

    if sorted_findings:
        lines.append("## Findings\n")
        for f in sorted_findings:
            sev_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵", "info": "⚪"}.get(f["severity"], "⚪")
            lines.append(f"### {sev_icon} {f['title']} ({f['severity'].upper()})\n")
            lines.append(f"{f['detail']}\n")
            if f["evidence"]:
                lines.append(f"**Evidence:** `{f['evidence']}`\n")

    lines.append("## Remediation\n")
    lines.append("- Never reflect arbitrary Origin headers without validation")
    lines.append("- Use an explicit allowlist of trusted origins")
    lines.append("- Avoid `Access-Control-Allow-Origin: *` on authenticated endpoints")
    lines.append("- Never combine `*` with `Access-Control-Allow-Credentials: true`")
    lines.append("- Don't trust `null` origin")
    lines.append("- Set `Access-Control-Max-Age` to reduce preflight overhead")
    lines.append("- HTTPS endpoints should not trust HTTP origins")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="CORS Misconfiguration Scanner — detect dangerous CORS policies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 cors_scan.py https://api.example.com
  python3 cors_scan.py https://api.example.com/v1/users --format json
  python3 cors_scan.py https://a.com https://b.com --format markdown
  python3 cors_scan.py https://api.example.com --min-grade C""")

    parser.add_argument("urls", nargs="+", help="URL(s) to scan")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds")
    parser.add_argument("--min-grade", choices=["A", "B", "C", "D", "F"],
                        help="Exit with code 1 if any URL grades below this")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show all test details")
    parser.add_argument("--version", action="version", version=f"cors-scanner {__version__}")

    args = parser.parse_args()

    all_results = []
    worst_grade = "A"
    grade_rank = {"A": 0, "B": 1, "C": 2, "D": 3, "F": 4}

    for url in args.urls:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        findings = scan_cors(url, timeout=args.timeout, verbose=args.verbose)
        grade = grade_findings(findings)

        if grade_rank.get(grade, 0) > grade_rank.get(worst_grade, 0):
            worst_grade = grade

        if args.format == "json":
            all_results.append({"url": url, "grade": grade, "findings": findings})
        elif args.format == "markdown":
            print(format_markdown(url, findings, grade))
        else:
            print(format_text(url, findings, grade))

    if args.format == "json":
        if len(all_results) == 1:
            print(format_json(all_results[0]["url"], all_results[0]["findings"], all_results[0]["grade"]))
        else:
            print(json.dumps({"scans": [
                {"url": r["url"], "grade": r["grade"],
                 "findings_count": len([f for f in r["findings"] if f["severity"] != "info"]),
                 "findings": r["findings"]}
                for r in all_results
            ]}, indent=2))

    # CI-friendly exit code
    if args.min_grade and grade_rank.get(worst_grade, 0) > grade_rank.get(args.min_grade, 0):
        sys.exit(1)


if __name__ == "__main__":
    main()
