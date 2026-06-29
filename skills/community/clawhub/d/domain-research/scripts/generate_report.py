#!/usr/bin/env python3
"""
Domain Research Report Generator
================================
Generates an interactive HTML visualization report from domain research JSON data.
Consumes output from domain_lookup.py and produces a self-contained HTML report.

Usage:
    python generate_report.py research_result.json [--output report.html]
    python generate_report.py --stdin [--output report.html]
"""

import json
import sys
import argparse
from datetime import datetime


def _status_badge(value: bool, positive: str = "Yes", negative: str = "No") -> str:
    if value:
        return f'<span class="badge badge-green">{positive}</span>'
    return f'<span class="badge badge-red">{negative}</span>'


def _severity_color(days: int) -> str:
    if days <= 7:
        return "#e74c3c"
    elif days <= 30:
        return "#f39c12"
    return "#27ae60"


def build_report(data: dict) -> str:
    """Build complete HTML report from research data."""
    domain = data.get("domain", "Unknown")
    summary = data.get("summary", {})
    availability = data.get("availability", {})
    rdap = data.get("rdap", {})
    whois = data.get("whois", {})
    dns = data.get("dns", {})
    dns_multi = data.get("dns_multi", {})
    ssl = data.get("ssl", {})
    subdomains = data.get("subdomains", {})

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{domain} — Domain Research Report</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; background: #f5f7fa; color: #2c3e50; line-height: 1.6; }}
.container {{ max-width: 1100px; margin: 0 auto; padding: 24px; }}
.header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); color: white; padding: 36px 40px; border-radius: 16px; margin-bottom: 24px; }}
.header h1 {{ font-size: 28px; margin-bottom: 8px; }}
.header .domain {{ font-size: 18px; color: #a8b2d1; font-family: "SF Mono", "Fira Code", monospace; }}
.header .meta {{ margin-top: 12px; font-size: 13px; color: #8892b0; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; margin-bottom: 20px; }}
.card {{ background: white; border-radius: 12px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
.card h3 {{ font-size: 16px; color: #1a1a2e; margin-bottom: 16px; padding-bottom: 10px; border-bottom: 2px solid #e2e8f0; display: flex; align-items: center; gap: 8px; }}
.card h3 .icon {{ font-size: 20px; }}
.card-full {{ grid-column: 1 / -1; }}
.badge {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }}
.badge-green {{ background: #d4edda; color: #155724; }}
.badge-red {{ background: #f8d7da; color: #721c24; }}
.badge-yellow {{ background: #fff3cd; color: #856404; }}
.badge-blue {{ background: #d1ecf1; color: #0c5460; }}
.badge-purple {{ background: #e8daef; color: #6c3483; }}
.record-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
.record-table th {{ text-align: left; padding: 8px 12px; background: #f8f9fa; border-bottom: 2px solid #dee2e6; font-weight: 600; color: #495057; }}
.record-table td {{ padding: 8px 12px; border-bottom: 1px solid #e9ecef; }}
.record-table tr:hover {{ background: #f8f9fa; }}
.record-list {{ list-style: none; }}
.record-list li {{ padding: 6px 0; border-bottom: 1px solid #f0f0f0; font-size: 13px; font-family: "SF Mono", "Fira Code", monospace; word-break: break-all; }}
.record-list li:last-child {{ border-bottom: none; }}
.key-value {{ margin-bottom: 8px; font-size: 13px; }}
.key-value .key {{ color: #6c757d; margin-right: 8px; }}
.key-value .value {{ font-weight: 500; }}
.highlight-card {{ padding: 12px 16px; border-radius: 8px; margin-bottom: 8px; font-size: 13px; }}
.highlight-warning {{ background: #fff3cd; border-left: 4px solid #f39c12; }}
.highlight-danger {{ background: #f8d7da; border-left: 4px solid #e74c3c; }}
.highlight-info {{ background: #d1ecf1; border-left: 4px solid #17a2b8; }}
.ssl-meter {{ width: 100%; height: 8px; background: #e9ecef; border-radius: 4px; overflow: hidden; margin: 8px 0; }}
.ssl-meter-fill {{ height: 100%; border-radius: 4px; transition: width 0.5s; }}
.subdomain-grid {{ display: flex; flex-wrap: wrap; gap: 6px; }}
.subdomain-tag {{ background: #e8f4fd; color: #0c5460; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-family: "SF Mono", monospace; }}
.empty-state {{ color: #adb5bd; font-style: italic; font-size: 13px; padding: 12px 0; }}
.resolver-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; }}
.resolver-item {{ padding: 10px; border-radius: 8px; background: #f8f9fa; text-align: center; font-size: 13px; }}
.resolver-item .name {{ font-weight: 600; color: #1a1a2e; }}
.resolver-item .records {{ font-family: "SF Mono", monospace; color: #27ae60; margin-top: 4px; }}
.resolver-item.unreachable {{ opacity: 0.5; }}
.resolver-item.unreachable .records {{ color: #e74c3c; }}
.tabs {{ display: flex; gap: 4px; margin-bottom: 0; }}
.tab-btn {{ padding: 8px 16px; border: none; background: #e9ecef; border-radius: 8px 8px 0 0; cursor: pointer; font-size: 13px; font-weight: 500; color: #6c757d; }}
.tab-btn.active {{ background: white; color: #1a1a2e; font-weight: 600; }}
.tab-content {{ display: none; padding: 16px; background: white; border-radius: 0 8px 8px 8px; }}
.tab-content.active {{ display: block; }}
.footer {{ text-align: center; padding: 40px 0 20px; color: #adb5bd; font-size: 12px; }}
</style>
</head>
<body>
<div class="container">

<!-- Header -->
<div class="header">
    <h1>Domain Research Report</h1>
    <div class="domain">{domain}</div>
    <div class="meta">Generated: {data.get('generated_at', 'N/A')}</div>
</div>

<!-- Highlights -->
{_build_highlights(summary)}

<!-- Key Metrics Grid -->
<div class="grid">
    <div class="card">
        <h3><span class="icon">&#128204;</span> Registration Status</h3>
        <div style="font-size:18px;margin-bottom:8px;">
            {_status_badge(not availability.get('likely_available', True), "Registered", "Likely Available")}
        </div>
        {_build_availability_indicators(availability)}
    </div>

    <div class="card">
        <h3><span class="icon">&#128273;</span> SSL Certificate</h3>
        {_build_ssl_card(ssl)}
    </div>

    <div class="card">
        <h3><span class="icon">&#127758;</span> DNS Resolution</h3>
        {_build_dns_summary_card(dns)}
    </div>

    <div class="card">
        <h3><span class="icon">&#128231;</span> MX / Email</h3>
        {_build_mx_card(dns)}
    </div>
</div>

<!-- Detailed Tabs -->
<div class="tabs">
    <button class="tab-btn active" onclick="showTab('dns-tab', this)">DNS Records</button>
    <button class="tab-btn" onclick="showTab('rdap-tab', this)">RDAP</button>
    <button class="tab-btn" onclick="showTab('whois-tab', this)">WHOIS</button>
    <button class="tab-btn" onclick="showTab('ssl-tab', this)">SSL Details</button>
    <button class="tab-btn" onclick="showTab('subdomain-tab', this)">Subdomains</button>
    <button class="tab-btn" onclick="showTab('resolver-tab', this)">DNS Resolvers</button>
</div>

<div class="tab-content active" id="dns-tab">
    {_build_dns_records(dns)}
</div>
<div class="tab-content" id="rdap-tab">
    {_build_rdap_section(rdap)}
</div>
<div class="tab-content" id="whois-tab">
    {_build_whois_section(whois)}
</div>
<div class="tab-content" id="ssl-tab">
    {_build_ssl_details(ssl)}
</div>
<div class="tab-content" id="subdomain-tab">
    {_build_subdomains(subdomains)}
</div>
<div class="tab-content" id="resolver-tab">
    {_build_resolvers(dns_multi)}
</div>

<div class="footer">
    Domain Research Tool — Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC
</div>
</div>

<script>
function showTab(tabId, btn) {{
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(tabId).classList.add('active');
}}
</script>

</body>
</html>"""


def _build_highlights(summary: dict) -> str:
    highlights = summary.get("highlights", [])
    if not highlights:
        return ""
    items = "".join(f'<div class="highlight-card highlight-warning">{h}</div>' for h in highlights)
    return f'<div style="margin-bottom:20px;">{items}</div>'


def _build_availability_indicators(availability: dict) -> str:
    indicators = availability.get("indicators", [])
    if not indicators:
        return '<div class="empty-state">No indicators available</div>'
    rows = ""
    for ind in indicators:
        suggestion = ind.get("suggests", "unknown")
        badge_class = "badge-green" if suggestion == "registered" else "badge-red" if suggestion == "available" else "badge-yellow"
        rows += f"""
        <tr>
            <td>{ind.get('source', '')}</td>
            <td>{ind.get('finding', '')}</td>
            <td><span class="badge {badge_class}">{suggestion.title()}</span></td>
        </tr>"""
    return f"""<table class="record-table">
        <thead><tr><th>Source</th><th>Finding</th><th>Indicates</th></tr></thead>
        <tbody>{rows}</tbody>
    </table>"""


def _build_ssl_card(ssl_data: dict) -> str:
    if not ssl_data.get("success"):
        return f'<div class="empty-state">{ssl_data.get("error", "SSL check failed")}</div>'
    d = ssl_data["data"]
    days = d.get("days_remaining", 0)
    pct = max(0, min(100, days / 365 * 100)) if days > 0 else 0
    color = _severity_color(days)
    status = "Valid" if not d.get("is_expired") else "EXPIRED"
    badge_class = "badge-red" if d.get("is_expired") else "badge-green"
    return f"""
    <div style="font-size:14px;margin-bottom:8px;">
        Status: <span class="badge {badge_class}">{status}</span>
    </div>
    <div class="key-value"><span class="key">Days Remaining:</span><span class="value" style="color:{color};font-size:22px;font-weight:700;">{days}</span></div>
    <div class="ssl-meter"><div class="ssl-meter-fill" style="width:{pct}%;background:{color};"></div></div>
    <div class="key-value"><span class="key">Expires:</span><span class="value">{d.get('not_after', 'N/A')}</span></div>
    <div class="key-value"><span class="key">Issuer:</span><span class="value">{d.get('issuer', {}).get('commonName', d.get('issuer', {}).get('organizationName', 'N/A'))}</span></div>
    """


def _build_dns_summary_card(dns_data: dict) -> str:
    records = dns_data.get("records", {})
    a_records = records.get("A", [])
    if a_records:
        ips = ", ".join(a_records[:3])
        if len(a_records) > 3:
            ips += f" (+{len(a_records) - 3} more)"
    else:
        ips = "No A records"
    has_aaaa = bool(records.get("AAAA"))
    has_ns = bool(records.get("NS"))
    return f"""
    <div class="key-value"><span class="key">A (IPv4):</span><span class="value" style="font-family:monospace;">{ips}</span></div>
    <div class="key-value"><span class="key">AAAA (IPv6):</span><span class="value">{_status_badge(has_aaaa, "Configured", "None")}</span></div>
    <div class="key-value"><span class="key">NS:</span><span class="value">{_status_badge(has_ns, f"{len(records.get('NS', []))} servers", "None")}</span></div>
    """


def _build_mx_card(dns_data: dict) -> str:
    mx = dns_data.get("records", {}).get("MX", [])
    if not mx:
        return '<div class="empty-state">No MX records found</div>'
    items = "".join(f'<li><span class="badge badge-blue">MX</span> {r}</li>' for r in mx)
    return f'<ul class="record-list">{items}</ul>'


def _build_dns_records(dns_data: dict) -> str:
    records = dns_data.get("records", {})
    errors = dns_data.get("errors", [])

    if not records and errors:
        return "".join(f'<div class="highlight-card highlight-danger">{e}</div>' for e in errors)

    rows = ""
    for rtype in ["A", "AAAA", "NS", "MX", "CNAME", "TXT", "SOA", "CAA", "SRV", "PTR"]:
        vals = records.get(rtype)
        if vals is None and rtype == "A":
            rows += f'<tr><td><span class="badge badge-purple">{rtype}</span></td><td colspan="2">NXDOMAIN — domain does not exist</td></tr>'
            break
        if vals is None:
            continue
        if vals:
            display = vals[:3]
            extra = f" (+{len(vals) - 3} more)" if len(vals) > 3 else ""
            rows += f"""
            <tr>
                <td><span class="badge badge-purple">{rtype}</span></td>
                <td><span class="badge badge-green">{len(vals)} record(s)</span></td>
                <td style="font-family:monospace;font-size:12px;">{", ".join(display)}{extra}</td>
            </tr>"""
        else:
            rows += f"""
            <tr>
                <td><span class="badge badge-purple">{rtype}</span></td>
                <td><span class="badge" style="background:#f0f0f0;">—</span></td>
                <td style="color:#adb5bd;">No records</td>
            </tr>"""

    return f"""
    <table class="record-table">
        <thead><tr><th>Type</th><th>Count</th><th>Values</th></tr></thead>
        <tbody>{rows}</tbody>
    </table>"""


def _build_rdap_section(rdap_data: dict) -> str:
    if not rdap_data.get("success"):
        return f'<div class="highlight-card highlight-warning">RDAP query failed: {rdap_data.get("error", "Unknown error")}<br><small>Server: {rdap_data.get("rdap_server", "N/A")}</small></div>'

    d = rdap_data["data"]
    parts = []

    # Domain status
    if d.get("status"):
        statuses = " ".join(f'<span class="badge badge-blue">{s}</span>' for s in d["status"])
        parts.append(f'<div class="key-value"><span class="key">Status:</span>{statuses}</div>')

    # Handle
    if d.get("handle"):
        parts.append(f'<div class="key-value"><span class="key">Handle:</span><span class="value">{d["handle"]}</span></div>')

    # Events (dates)
    for event in d.get("events", []):
        action = event.get("action", "").replace("_", " ").title()
        date = event.get("date", "N/A")
        color = "#27ae60" if "registration" in str(event.get("action", "")) else "#3498db" if "expir" in str(event.get("action", "")) else "#6c757d"
        parts.append(f'<div class="key-value"><span class="key">{action}:</span><span class="value" style="color:{color};">{date}</span></div>')

    # Nameservers
    if d.get("nameservers"):
        ns_items = "".join(f'<li>{ns["name"]}</li>' for ns in d["nameservers"])
        parts.append(f'<div class="key-value"><span class="key">Nameservers:</span></div><ul class="record-list">{ns_items}</ul>')

    # Entities (registrant, admin, tech)
    if d.get("entities"):
        parts.append('<h4 style="margin:16px 0 8px;font-size:14px;">Entities</h4>')
        for entity in d["entities"]:
            roles = ", ".join(entity.get("roles", [])).title()
            name = entity.get("name", entity.get("organization", "")) or entity.get("handle", "N/A")
            parts.append(f"""
            <div class="highlight-card highlight-info" style="margin-bottom:6px;">
                <strong>{roles}</strong>: {name}
                {f'<br><small>Email: {entity["email"]}</small>' if entity.get("email") else ''}
                {f'<br><small>Org: {entity["organization"]}</small>' if entity.get("organization") else ''}
            </div>""")

    # Server info
    if rdap_data.get("rdap_server"):
        parts.append(f'<div style="margin-top:12px;font-size:12px;color:#adb5bd;">RDAP Server: {rdap_data["rdap_server"]}</div>')

    return "".join(parts)


def _build_whois_section(whois_data: dict) -> str:
    if not whois_data.get("success"):
        return f'<div class="highlight-card highlight-warning">WHOIS query failed: {whois_data.get("error", "Unknown error")}</div>'

    d = whois_data["data"]
    if not d:
        return '<div class="empty-state">No WHOIS data returned</div>'

    # Ordered fields
    key_order = [
        ("domain_name", "Domain"),
        ("registrar", "Registrar"),
        ("whois_server", "WHOIS Server"),
        ("creation_date", "Created"),
        ("expiration_date", "Expires"),
        ("updated_date", "Updated"),
        ("name_servers", "Nameservers"),
        ("status", "Status"),
        ("emails", "Contact Emails"),
        ("name", "Registrant"),
        ("org", "Organization"),
        ("address", "Address"),
        ("city", "City"),
        ("state", "State"),
        ("zipcode", "ZIP"),
        ("country", "Country"),
    ]

    rows = ""
    for key, label in key_order:
        val = d.get(key)
        if val is None:
            continue
        if isinstance(val, list):
            val = ", ".join(str(v) for v in val)
        rows += f'<tr><td style="font-weight:600;width:160px;">{label}</td><td style="font-family:monospace;">{val}</td></tr>'

    # Any remaining fields
    shown = set(k for k, _ in key_order)
    for key, val in d.items():
        if key in shown or val is None:
            continue
        if isinstance(val, list):
            val = ", ".join(str(v) for v in val)
        rows += f'<tr><td style="font-weight:600;">{key}</td><td style="font-family:monospace;">{val}</td></tr>'

    return f'<table class="record-table">{rows}</table>'


def _build_ssl_details(ssl_data: dict) -> str:
    if not ssl_data.get("success"):
        return f'<div class="highlight-card highlight-danger">{ssl_data.get("error", "SSL check failed")}</div>'
    d = ssl_data["data"]
    sans = d.get("subject_alt_names", [])
    sans_html = "".join(f'<span class="subdomain-tag">{s}</span>' for s in sans[:20]) if sans else 'None'

    return f"""
    <table class="record-table">
        <tr><td style="font-weight:600;width:200px;">Subject CN</td><td>{d.get('subject', {}).get('commonName', 'N/A')}</td></tr>
        <tr><td style="font-weight:600;">Issuer</td><td>{d.get('issuer', {}).get('commonName', d.get('issuer', {}).get('organizationName', 'N/A'))}</td></tr>
        <tr><td style="font-weight:600;">Serial Number</td><td style="font-family:monospace;">{d.get('serial_number', 'N/A')}</td></tr>
        <tr><td style="font-weight:600;">Valid From</td><td>{d.get('not_before', 'N/A')}</td></tr>
        <tr><td style="font-weight:600;">Valid Until</td><td>{d.get('not_after', 'N/A')}</td></tr>
        <tr><td style="font-weight:600;">SHA-256 Fingerprint</td><td style="font-family:monospace;font-size:11px;">{d.get('fingerprint_sha256', 'N/A')}</td></tr>
        <tr><td style="font-weight:600;">Days Remaining</td><td style="color:{_severity_color(d.get('days_remaining', 0))};font-weight:700;">{d.get('days_remaining', 0)}</td></tr>
        <tr><td style="font-weight:600;">Version</td><td>{d.get('version', 'N/A')}</td></tr>
    </table>
    <div style="margin-top:12px;">
        <strong>Subject Alternative Names ({len(sans)}):</strong>
        <div class="subdomain-grid" style="margin-top:6px;">{sans_html}</div>
    </div>
    """


def _build_subdomains(sub_data: dict) -> str:
    if isinstance(sub_data, str) or sub_data.get("error"):
        return f'<div class="empty-state">{sub_data.get("error", str(sub_data))}</div>'
    discovered = sub_data.get("discovered", [])
    total = sub_data.get("total_tested", 0)
    if not discovered:
        return f'<div class="empty-state">No subdomains discovered (tested {total} common names)</div>'

    tags = ""
    for sub in discovered:
        ips = ", ".join(sub.get("records", []))
        tags += f'<div class="subdomain-tag" title="{ips}">{sub["subdomain"]}</div>'

    return f"""
    <p style="margin-bottom:12px;font-size:13px;color:#6c757d;">Found {len(discovered)} subdomains out of {total} tested</p>
    <div class="subdomain-grid">{tags}</div>
    """


def _build_resolvers(resolver_data: dict) -> str:
    resolvers = resolver_data.get("resolvers", {})
    if not resolvers:
        return '<div class="empty-state">No resolver data available</div>'

    items = ""
    for name, info in resolvers.items():
        records = ", ".join(info.get("a_records", []))
        reachable = info.get("reachable", False)
        cls = "" if reachable else "unreachable"
        record_display = records if records else ("Unreachable" if not reachable else "No records")
        items += f"""
        <div class="resolver-item {cls}">
            <div class="name">{name}</div>
            <div style="font-size:11px;color:#adb5bd;">{info.get('ip', '')}</div>
            <div class="records">{record_display}</div>
        </div>"""

    return f'<div class="resolver-grid">{items}</div>'


def main():
    parser = argparse.ArgumentParser(description="Generate HTML domain research report")
    parser.add_argument("input", nargs="?", help="JSON file from domain_lookup.py")
    parser.add_argument("--stdin", action="store_true", help="Read JSON from stdin")
    parser.add_argument("--output", "-o", default=None, help="Output HTML file path")
    args = parser.parse_args()

    if args.stdin:
        data = json.load(sys.stdin)
    elif args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        print("Error: provide input file or --stdin", file=sys.stderr)
        sys.exit(1)

    html = build_report(data)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Report saved to {args.output}", file=sys.stderr)
    else:
        print(html)


if __name__ == "__main__":
    main()
