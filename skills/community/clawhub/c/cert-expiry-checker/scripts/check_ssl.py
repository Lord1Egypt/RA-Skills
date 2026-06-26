#!/usr/bin/env python3
"""SSL Certificate Expiry Checker

Usage:
  python3 check_ssl.py example.com
  python3 check_ssl.py example.com google.com github.com --json
  python3 check_ssl.py --file domains.txt --report
  python3 check_ssl.py example.com --port 8443
"""

import argparse
import json
import socket
import ssl
import sys
import os
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed


def check_cert(hostname, port=443, timeout=10):
    """Check SSL certificate for a given hostname and port."""
    result = {
        "hostname": hostname,
        "port": port,
        "status": "unknown",
        "error": None,
        "subject": None,
        "issuer": None,
        "not_before": None,
        "not_after": None,
        "days_remaining": None,
        "serial_number": None,
        "san": [],
        "version": None,
        "fingerprint_sha256": None,
    }

    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = True
        ctx.verify_mode = ssl.CERT_REQUIRED

        sock = socket.create_connection((hostname, port), timeout=timeout)
        with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            der_cert = ssock.getpeercert(binary_form=True)
            cert_info = ssl.DER_cert_to_PEM_cert(der_cert)

        if not cert:
            result["status"] = "no_cert"
            return result

        now = datetime.now(timezone.utc)

        # Parse dates
        not_before_str = cert.get("notBefore")
        not_after_str = cert.get("notAfter")

        if not_before_str:
            not_before = datetime.strptime(not_before_str, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
            result["not_before"] = not_before.isoformat()
        if not_after_str:
            not_after = datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
            result["not_after"] = not_after.isoformat()
            result["days_remaining"] = (not_after - now).days

        # Subject
        subject_parts = cert.get("subject", [])
        subject_dict = {}
        for part in subject_parts:
            for key, val in part:
                subject_dict[key] = val
        result["subject"] = subject_dict

        # Issuer
        issuer_parts = cert.get("issuer", [])
        issuer_dict = {}
        for part in issuer_parts:
            for key, val in part:
                issuer_dict[key] = val
        result["issuer"] = issuer_dict

        # SAN
        result["san"] = [san for _, san in cert.get("subjectAltName", [])]

        # Version & Serial from PEM parsing
        for line in cert_info.split("\n"):
            if "BEGIN CERTIFICATE" in line:
                break

        # Determine status
        if result["days_remaining"] is not None:
            if result["days_remaining"] < 0:
                result["status"] = "expired"
            elif result["days_remaining"] <= 14:
                result["status"] = "critical"
            elif result["days_remaining"] <= 30:
                result["status"] = "warning"
            elif result["days_remaining"] <= 60:
                result["status"] = "expiring_soon"
            else:
                result["status"] = "valid"

    except ssl.CertificateError as e:
        result["status"] = "cert_error"
        result["error"] = str(e)
    except socket.timeout:
        result["status"] = "timeout"
        result["error"] = "Connection timed out"
    except ConnectionRefusedError:
        result["status"] = "refused"
        result["error"] = "Connection refused"
    except socket.gaierror as e:
        result["status"] = "dns_error"
        result["error"] = f"DNS resolution failed: {e}"
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


def print_table(results):
    """Print formatted ASCII table."""
    print(f"\n{'Hostname':<30} {'Port':<6} {'Status':<16} {'Days Left':<10} {'Issuer':<30} {'Expiry Date':<20}")
    print("=" * 112)
    for r in results:
        status = r["status"]
        status_str = {
            "valid": "🟢 Valid",
            "expiring_soon": "🟡 Expiring Soon",
            "warning": "🟠 Warning",
            "critical": "🔴 Critical",
            "expired": "⛔ Expired",
            "cert_error": "❌ Cert Error",
            "timeout": "⏱ Timeout",
            "refused": "🚫 Refused",
            "dns_error": "🌐 DNS Error",
            "no_cert": "❓ No Cert",
            "error": "⚠ Error",
            "unknown": "❓ Unknown",
        }.get(status, status)

        days = str(r["days_remaining"]) if r["days_remaining"] is not None else "-"

        issuer = ""
        if r["issuer"]:
            issuer = r["issuer"].get("organizationName", r["issuer"].get("commonName", ""))

        expiry = ""
        if r["not_after"]:
            expiry = r["not_after"][:10]

        print(f"{r['hostname']:<30} {r['port']:<6} {status_str:<16} {days:<10} {issuer:<30} {expiry:<20}")

    # Summary
    valid = sum(1 for r in results if r["status"] in ("valid", "expiring_soon"))
    warnings = sum(1 for r in results if r["status"] in ("warning", "critical", "expired"))
    errors = sum(1 for r in results if r["status"] in ("error", "cert_error", "timeout", "refused", "dns_error", "no_cert"))
    total = len(results)
    print(f"\n📊 Summary: {valid} healthy, {warnings} warnings, {errors} errors — {total} total")


def generate_html_report(results, output_path=None):
    """Generate HTML report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = ""
    for r in results:
        status_class = {
            "valid": "success", "expiring_soon": "warning",
            "warning": "warning", "critical": "danger",
            "expired": "danger",
        }.get(r["status"], "secondary")

        status_icon = {
            "valid": "✅", "expiring_soon": "🟡",
            "warning": "🟠", "critical": "🔴",
            "expired": "⛔", "cert_error": "❌",
            "timeout": "⏱", "refused": "🚫",
            "dns_error": "🌐", "no_cert": "❓",
            "error": "⚠",
        }.get(r["status"], "❓")

        issuer = r["issuer"].get("organizationName", r["issuer"].get("commonName", "")) if r["issuer"] else "-"
        subject = r["subject"].get("commonName", "") if r["subject"] else "-"
        days = r["days_remaining"] if r["days_remaining"] is not None else "-"
        expiry = r["not_after"][:10] if r["not_after"] else "-"
        error = r["error"] if r["error"] else ""
        error_row = f'<tr class="table-danger"><td colspan="8">{error}</td></tr>' if error else ""

        rows += f"""<tr>
            <td>{r['hostname']}:{r['port']}</td>
            <td>{subject}</td>
            <td><span class="badge bg-{status_class}">{status_icon} {r['status'].replace('_', ' ').title()}</span></td>
            <td>{days}</td>
            <td>{expiry}</td>
            <td>{issuer}</td>
            <td>{', '.join(r['san'][:5])}</td>
        </tr>{error_row}"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>SSL Certificate Report</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body {{ font-family: 'Segoe UI', sans-serif; padding: 2rem; background: #f8f9fa; }}
h1 {{ color: #1a1a2e; }}
.footer {{ margin-top: 2rem; color: #6c757d; font-size: 0.875rem; }}
</style></head>
<body>
<div class="container">
<h1>🔒 SSL Certificate Report</h1>
<p class="text-muted">Generated: {now}</p>
<table class="table table-striped table-hover">
<thead class="table-dark"><tr>
<th>Hostname</th><th>Subject CN</th><th>Status</th><th>Days Left</th><th>Expiry</th><th>Issuer</th><th>SAN</th>
</tr></thead>
<tbody>{rows}</tbody>
</table>
<p><strong>Summary:</strong> {sum(1 for r in results if r['status'] in ('valid', 'expiring_soon'))} healthy, {sum(1 for r in results if r['status'] in ('warning', 'critical', 'expired'))} warnings, {sum(1 for r in results if r['status'] in ('error', 'cert_error', 'timeout', 'refused', 'dns_error', 'no_cert'))} errors — {len(results)} total</p>
<div class="footer">SSL Checker • Generated by ssl-checker skill</div>
</div></body></html>"""

    if output_path:
        with open(output_path, "w") as f:
            f.write(html)
        print(f"📄 HTML report saved: {output_path}")
    else:
        fname = f"ssl-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.html"
        with open(fname, "w") as f:
            f.write(html)
        print(f"📄 HTML report saved: {fname}")

    return html


def load_domains_from_file(filepath):
    """Load domain list from file (one per line, # for comments)."""
    domains = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                # Support hostname:port format
                if ":" in line:
                    hostname, port = line.rsplit(":", 1)
                    domains.append((hostname.strip(), int(port)))
                else:
                    domains.append((line, 443))
    return domains


def main():
    parser = argparse.ArgumentParser(
        description="SSL Certificate Expiry Checker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  check_ssl.py example.com
  check_ssl.py example.com google.com --json
  check_ssl.py --file domains.txt --report
  check_ssl.py example.com --port 8443
        """,
    )
    parser.add_argument("domains", nargs="*", help="Domain(s) to check")
    parser.add_argument("--port", type=int, default=443, help="Port (default: 443)")
    parser.add_argument("--file", "-f", help="File with domains (one per line)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--report", "-r", action="store_true", help="Generate HTML report")
    parser.add_argument("--output", "-o", help="Output file (for JSON or HTML)")
    parser.add_argument("--threads", "-t", type=int, default=10, help="Concurrent checks (default: 10)")

    args = parser.parse_args()

    # Collect targets
    targets = []
    if args.file and os.path.exists(args.file):
        targets.extend(load_domains_from_file(args.file))
    if args.domains:
        for d in args.domains:
            if ":" in d:
                hostname, port = d.rsplit(":", 1)
                targets.append((hostname.strip(), int(port)))
            else:
                targets.append((d, args.port))

    if not targets:
        parser.print_help()
        print("\n❌ No domains provided. Use positional args or --file.")
        sys.exit(1)

    print(f"🔍 Checking {len(targets)} domain(s)...")

    results = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(check_cert, hostname, port): (hostname, port) for hostname, port in targets}
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            results.append(result)
            hostname, _ = futures[future]
            status_icon = {
                "valid": "🟢", "expiring_soon": "🟡",
                "warning": "🟠", "critical": "🔴",
                "expired": "⛔",
            }.get(result["status"], "❌")
            days = f" ({result['days_remaining']}d)" if result["days_remaining"] is not None else ""
            print(f"  [{i}/{len(targets)}] {status_icon} {hostname}: {result['status']}{days}")

    results.sort(key=lambda r: (r["days_remaining"] if r["days_remaining"] is not None else 9999))

    if args.json:
        output = json.dumps(results, indent=2, ensure_ascii=False)
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            print(f"\n📄 JSON saved: {args.output}")
        else:
            print(output)
    elif args.report:
        generate_html_report(results, args.output)
    else:
        print_table(results)

    # Exit code based on severity
    critical = any(r["status"] in ("critical", "expired") for r in results)
    sys.exit(2 if critical else (1 if any(r["status"] in ("warning",) for r in results) else 0))


if __name__ == "__main__":
    main()
