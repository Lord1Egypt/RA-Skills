#!/usr/bin/env python3
"""
Domain Research Tool — Unified RDAP / WHOIS / DNS Lookup Engine
===============================================================
Queries RDAP (RFC 7480-7484), WHOIS (legacy), and DNS records
for a given domain. Outputs structured JSON.

Usage:
    python domain_lookup.py <domain> [--type rdap|whois|dns|all|ssl] [--format json|text]
    python domain_lookup.py --batch domains.txt [--type all] [--output results.json]

Dependencies:
    pip install dnspython python-whois requests cryptography
"""

import argparse
import json
import socket
import ssl
import sys
import time
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── DNS ──────────────────────────────────────────────────
try:
    import dns.resolver
    import dns.reversename
    import dns.rdatatype
    HAS_DNSPYTHON = True
except ImportError:
    HAS_DNSPYTHON = False

# ── WHOIS ────────────────────────────────────────────────
try:
    import whois
    HAS_WHOIS = True
except ImportError:
    HAS_WHOIS = False

# ── HTTP (for RDAP) ──────────────────────────────────────
import urllib.request
import urllib.error


# ══════════════════════════════════════════════════════════
#  RDAP — Registration Data Access Protocol (RFC 7480-7484)
# ══════════════════════════════════════════════════════════

# IANA RDAP Bootstrap: TLD → RDAP server URL
# Major TLDs pre-configured; fallback uses IANA bootstrap
RDAP_SERVERS = {
    "com": "https://rdap.verisign.com/com/v1/",
    "net": "https://rdap.verisign.com/net/v1/",
    "org": "https://rdap.publicinterestregistry.org/rdap/",
    "info": "https://rdap.afilias.net/rdap/",
    "biz": "https://rdap.nic.biz/rdap/",
    "io": "https://rdap.nic.io/rdap/",
    "co": "https://rdap.nic.co/rdap/",
    "ai": "https://rdap.nic.ai/rdap/",
    "app": "https://rdap.nic.google/rdap/",
    "dev": "https://rdap.nic.google/rdap/",
    "xyz": "https://rdap.centralnic.com/xyz/rdap/",
    "online": "https://rdap.centralnic.com/online/rdap/",
    "shop": "https://rdap.centralnic.com/shop/rdap/",
    "top": "https://rdap.centralnic.com/top/rdap/",
    "cn": "https://rdap.cnnic.cn/rdap/",
    "de": "https://rdap.denic.de/rdap/",
    "uk": "https://rdap.nominet.uk/rdap/",
    "fr": "https://rdap.nic.fr/rdap/",
    "jp": "https://rdap.jprs.jp/rdap/",
    "ru": "https://rdap.tcinet.ru/rdap/",
    "br": "https://rdap.registro.br/rdap/",
    "in": "https://rdap.registry.in/rdap/",
    "ca": "https://rdap.cira.ca/rdap/",
    "au": "https://rdap.auda.org.au/rdap/",
    "eu": "https://rdap.eurid.eu/rdap/",
    "me": "https://rdap.centralnic.com/me/rdap/",
    "tv": "https://rdap.nic.tv/rdap/",
    "cc": "https://rdap.nic.cc/rdap/",
    "us": "https://rdap.nic.us/rdap/",
    "pw": "https://rdap.centralnic.com/pw/rdap/",
    "site": "https://rdap.centralnic.com/site/rdap/",
    "icu": "https://rdap.centralnic.com/icu/rdap/",
}


def _extract_tld(domain: str) -> str:
    """Extract TLD from domain name (handles ccTLDs like co.uk)."""
    parts = domain.lower().rstrip(".").split(".")
    # Known two-part TLDs
    two_part = {"co.uk", "co.jp", "co.kr", "co.in", "com.cn", "net.cn", "org.cn",
                "com.au", "net.au", "org.au", "co.nz", "net.nz", "org.nz",
                "com.br", "net.br", "org.br", "co.za", "web.za"}
    if len(parts) >= 3 and ".".join(parts[-2:]) in two_part:
        return ".".join(parts[-2:])
    return parts[-1]


def rdap_lookup(domain: str) -> dict:
    """Query RDAP for domain registration data. Falls back to IANA bootstrap."""
    tld = _extract_tld(domain)
    headers = {"Accept": "application/rdap+json, application/json"}
    result = {
        "protocol": "RDAP",
        "domain": domain,
        "tld": tld,
        "queried_at": datetime.now(timezone.utc).isoformat(),
        "success": False,
        "data": None,
        "error": None,
        "rdap_server": None,
    }

    # Try known RDAP server
    server_url = RDAP_SERVERS.get(tld)
    if server_url:
        url = f"{server_url.rstrip('/')}/domain/{domain}"
        result["rdap_server"] = server_url
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                result["success"] = True
                result["data"] = _summarize_rdap(data)
                return result
        except urllib.error.HTTPError as e:
            if e.code == 404:
                result["error"] = "Domain not found (404) — may be unregistered"
            else:
                result["error"] = f"HTTP {e.code}: {e.reason}"
        except Exception as e:
            result["error"] = str(e)

    # Fallback: IANA RDAP bootstrap
    try:
        iana_url = f"https://rdap.iana.org/rdap/domain/{domain}"
        req = urllib.request.Request(iana_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if "redirect" in str(data).lower() or data.get("links"):
                # Extract redirect URL from links
                for link in data.get("links", []):
                    if link.get("rel") == "self" and link.get("href"):
                        redirect_url = link["href"]
                        result["rdap_server"] = redirect_url.rsplit("/domain/", 1)[0]
                        req2 = urllib.request.Request(redirect_url, headers=headers)
                        with urllib.request.urlopen(req2, timeout=15) as resp2:
                            data2 = json.loads(resp2.read().decode("utf-8"))
                            result["success"] = True
                            result["data"] = _summarize_rdap(data2)
                            return result
    except Exception:
        pass

    if not result["error"]:
        result["error"] = "No RDAP server found for this TLD"

    return result


def _summarize_rdap(data: dict) -> dict:
    """Extract key fields from RDAP response."""
    summary = {
        "domain_name": data.get("ldhName"),
        "handle": data.get("handle"),
        "status": data.get("status", []),
        "nameservers": [],
        "entities": [],
        "events": [],
    }

    for ns in data.get("nameservers", []):
        summary["nameservers"].append({
            "name": ns.get("ldhName"),
            "ip_addresses": ns.get("ipAddresses", {}),
        })

    for entity in data.get("entities", []):
        vcard = entity.get("vcardArray", [[], []])
        info = {"roles": entity.get("roles", []), "handle": entity.get("handle")}
        if len(vcard) > 1:
            for item in vcard[1]:
                if len(item) >= 4:
                    kind = item[0]
                    if kind == "fn":
                        info["name"] = item[3]
                    elif kind == "org":
                        info["organization"] = item[3]
                    elif kind == "email":
                        info["email"] = item[3]
        summary["entities"].append(info)

    for event in data.get("events", []):
        summary["events"].append({
            "action": event.get("eventAction"),
            "date": event.get("eventDate"),
        })

    return summary


# ══════════════════════════════════════════════════════════
#  WHOIS — Legacy Domain Lookup
# ══════════════════════════════════════════════════════════

def whois_lookup(domain: str) -> dict:
    """Perform traditional WHOIS lookup."""
    result = {
        "protocol": "WHOIS",
        "domain": domain,
        "queried_at": datetime.now(timezone.utc).isoformat(),
        "success": False,
        "data": None,
        "error": None,
    }

    if not HAS_WHOIS:
        result["error"] = "python-whois not installed (pip install python-whois)"
        return result

    try:
        w = whois.whois(domain)
        # Convert to serializable dict
        data = {}
        for key, val in w.items():
            if val is None:
                data[key] = None
            elif isinstance(val, (datetime,)):
                data[key] = val.isoformat()
            elif isinstance(val, (list,)):
                data[key] = [v.isoformat() if isinstance(v, datetime) else str(v) for v in val]
            elif isinstance(val, (set,)):
                data[key] = [str(v) for v in val]
            else:
                data[key] = str(val)

        result["success"] = True
        result["data"] = data
    except whois.parser.PywhoisError as e:
        result["error"] = str(e)
    except Exception as e:
        result["error"] = str(e)

    return result


# ══════════════════════════════════════════════════════════
#  DNS — Record Queries
# ══════════════════════════════════════════════════════════

DNS_RECORD_TYPES = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "PTR", "CAA", "SRV"]
DEFAULT_DNS_TYPES = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]


def dns_lookup(domain: str, record_types: list = None) -> dict:
    """Query DNS records for a domain."""
    if record_types is None:
        record_types = DEFAULT_DNS_TYPES

    result = {
        "protocol": "DNS",
        "domain": domain,
        "queried_at": datetime.now(timezone.utc).isoformat(),
        "success": True,
        "records": {},
        "errors": [],
    }

    if not HAS_DNSPYTHON:
        result["success"] = False
        result["errors"].append("dnspython not installed (pip install dnspython)")
        return result

    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            records = []
            for answer in answers:
                records.append(str(answer))
            result["records"][rtype] = records
        except dns.resolver.NoAnswer:
            result["records"][rtype] = []
        except dns.resolver.NXDOMAIN:
            result["errors"].append(f"{rtype}: NXDOMAIN — domain does not exist")
            result["records"][rtype] = None
            break  # No point querying more if domain doesn't exist
        except dns.resolver.NoNameservers:
            result["errors"].append(f"{rtype}: No name servers available")
            result["records"][rtype] = []
        except Exception as e:
            result["errors"].append(f"{rtype}: {str(e)}")
            result["records"][rtype] = []

    return result


def dns_resolver_info(domain: str) -> dict:
    """Check DNS resolution across multiple public resolvers."""
    resolvers = {
        "Cloudflare": "1.1.1.1",
        "Google": "8.8.8.8",
        "Quad9": "9.9.9.9",
        "AliDNS": "223.5.5.5",
    }

    result = {
        "protocol": "DNS-MultiResolver",
        "domain": domain,
        "queried_at": datetime.now(timezone.utc).isoformat(),
        "resolvers": {},
    }

    original_resolver = dns.resolver.Resolver()
    for name, ip in resolvers.items():
        try:
            resolver = dns.resolver.Resolver(configure=False)
            resolver.nameservers = [ip]
            resolver.timeout = 5
            resolver.lifetime = 5
            answers = resolver.resolve(domain, "A")
            result["resolvers"][name] = {
                "ip": ip,
                "a_records": [str(a) for a in answers],
                "reachable": True,
            }
        except Exception as e:
            result["resolvers"][name] = {
                "ip": ip,
                "a_records": [],
                "reachable": False,
                "error": str(e),
            }

    return result


# ══════════════════════════════════════════════════════════
#  SSL Certificate Check
# ══════════════════════════════════════════════════════════

def ssl_check(domain: str, port: int = 443) -> dict:
    """Retrieve SSL/TLS certificate information."""
    result = {
        "protocol": "SSL",
        "domain": domain,
        "port": port,
        "queried_at": datetime.now(timezone.utc).isoformat(),
        "success": False,
        "data": None,
        "error": None,
    }

    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = True
        ctx.verify_mode = ssl.CERT_REQUIRED

        with socket.create_connection((domain, port), timeout=10) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                cert_bin = ssock.getpeercert(binary_form=True)
                result["success"] = True
                try:
                    result["data"] = _summarize_ssl(cert, cert_bin)
                except Exception as e:
                    result["success"] = False
                    result["error"] = f"SSL cert parsing failed: {e}"
    except ssl.SSLCertVerificationError as e:
        result["error"] = f"Certificate verification failed: {e.verify_message}"
    except socket.gaierror:
        result["error"] = f"DNS resolution failed for {domain}"
    except socket.timeout:
        result["error"] = f"Connection timed out on port {port}"
    except ConnectionRefusedError:
        result["error"] = f"Connection refused on port {port}"
    except Exception as e:
        result["error"] = str(e)

    return result


def _summarize_ssl(cert: dict, cert_bin: bytes) -> dict:
    """Extract key fields from SSL certificate."""
    from cryptography import x509
    from cryptography.hazmat.backends import default_backend

    parsed = x509.load_der_x509_certificate(cert_bin, default_backend())

    sans = []
    try:
        ext = parsed.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        sans = ext.value.get_values_for_type(x509.DNSName)
    except x509.ExtensionNotFound:
        pass

    return {
        "subject": dict(x[0] for x in cert.get("subject", [])),
        "issuer": dict(x[0] for x in cert.get("issuer", [])),
        "serial_number": format(parsed.serial_number, "x").upper(),
        "not_before": cert.get("notBefore"),
        "not_after": cert.get("notAfter"),
        "subject_alt_names": sans,
        "version": cert.get("version"),
        "fingerprint_sha256": parsed.fingerprint(x509.certificates.Number(4)).hex(":"),
        "days_remaining": _days_remaining(cert.get("notAfter")),
        "is_expired": _is_expired(cert.get("notAfter")),
    }


def _days_remaining(not_after: str) -> int:
    """Calculate days until certificate expiry."""
    if not not_after:
        return 0
    expiry = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
    return (expiry - datetime.now()).days


def _is_expired(not_after: str) -> bool:
    return _days_remaining(not_after) <= 0


# ══════════════════════════════════════════════════════════
#  Domain Availability Check
# ══════════════════════════════════════════════════════════

def check_availability(domain: str) -> dict:
    """Check if a domain is likely available (WHOIS + DNS heuristics)."""
    result = {
        "domain": domain,
        "queried_at": datetime.now(timezone.utc).isoformat(),
        "likely_available": None,
        "indicators": [],
    }

    # Heuristic 1: DNS resolution
    try:
        dns.resolver.resolve(domain, "A")
        result["indicators"].append({"source": "DNS", "finding": "Has A record", "suggests": "registered"})
    except dns.resolver.NXDOMAIN:
        result["indicators"].append({"source": "DNS", "finding": "NXDOMAIN", "suggests": "available"})
    except Exception:
        result["indicators"].append({"source": "DNS", "finding": "No resolution", "suggests": "unknown"})

    # Heuristic 2: RDAP 404
    rdap = rdap_lookup(domain)
    if rdap.get("error") and "404" in rdap["error"]:
        result["indicators"].append({"source": "RDAP", "finding": "404 Not Found", "suggests": "available"})
    elif rdap.get("success"):
        result["indicators"].append({"source": "RDAP", "finding": "Data found", "suggests": "registered"})

    # Heuristic 3: WHOIS
    if HAS_WHOIS:
        try:
            w = whois.whois(domain)
            if w.domain_name:
                result["indicators"].append({"source": "WHOIS", "finding": "Record exists", "suggests": "registered"})
            else:
                result["indicators"].append({"source": "WHOIS", "finding": "No record", "suggests": "available"})
        except Exception:
            result["indicators"].append({"source": "WHOIS", "finding": "Query failed", "suggests": "unknown"})

    # Aggregate
    registered_hints = sum(1 for i in result["indicators"] if i["suggests"] == "registered")
    available_hints = sum(1 for i in result["indicators"] if i["suggests"] == "available")
    result["likely_available"] = available_hints > registered_hints

    return result


# ══════════════════════════════════════════════════════════
#  Subdomain Enumeration
# ══════════════════════════════════════════════════════════

COMMON_SUBDOMAINS = [
    "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "ns2",
    "webdisk", "cpanel", "whm", "autodiscover", "autoconfig", "m", "mobile",
    "blog", "shop", "api", "dev", "staging", "test", "admin", "portal",
    "cdn", "media", "static", "images", "img", "assets", "docs", "support",
    "status", "monitor", "git", "wiki", "jira", "confluence", "jenkins",
    "vpn", "remote", "secure", "login", "sso", "auth", "account", "accounts",
    "app", "apps", "dashboard", "beta", "demo", "store", "pay", "billing",
    "calendar", "contact", "help", "info", "news", "jobs", "careers",
]


def enumerate_subdomains(domain: str, wordlist: list = None, max_workers: int = 20) -> dict:
    """Enumerate common subdomains via DNS resolution."""
    if wordlist is None:
        wordlist = COMMON_SUBDOMAINS

    result = {
        "domain": domain,
        "queried_at": datetime.now(timezone.utc).isoformat(),
        "total_tested": len(wordlist),
        "discovered": [],
        "errors": 0,
    }

    def _check(sub: str):
        fqdn = f"{sub}.{domain}"
        try:
            answers = dns.resolver.resolve(fqdn, "A")
            return {
                "subdomain": fqdn,
                "records": [str(a) for a in answers],
            }
        except Exception:
            return None

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_check, s): s for s in wordlist}
        for future in as_completed(futures):
            try:
                r = future.result()
                if r:
                    result["discovered"].append(r)
            except Exception:
                result["errors"] += 1

    result["discovered"].sort(key=lambda x: x["subdomain"])
    return result


# ══════════════════════════════════════════════════════════
#  Reverse IP / DNS
# ══════════════════════════════════════════════════════════

def reverse_dns(ip: str) -> dict:
    """Perform reverse DNS (PTR) lookup on an IP address."""
    result = {
        "ip": ip,
        "queried_at": datetime.now(timezone.utc).isoformat(),
        "hostnames": [],
        "error": None,
    }
    try:
        addr = dns.reversename.from_address(ip)
        answers = dns.resolver.resolve(addr, "PTR")
        result["hostnames"] = [str(a).rstrip(".") for a in answers]
    except Exception as e:
        result["error"] = str(e)
    return result


# ══════════════════════════════════════════════════════════
#  Full Research — Run All Checks
# ══════════════════════════════════════════════════════════

def full_research(domain: str) -> dict:
    """Run all domain research checks and return consolidated results."""
    report = {
        "domain": domain,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "availability": check_availability(domain),
        "rdap": rdap_lookup(domain),
        "whois": whois_lookup(domain),
        "dns": dns_lookup(domain),
        "dns_multi": dns_resolver_info(domain),
        "ssl": ssl_check(domain),
    }

    # Only enumerate subdomains if DNS is available
    if HAS_DNSPYTHON and report["dns"]["success"]:
        try:
            # Quick check if domain resolves before enumerating
            dns.resolver.resolve(domain, "A")
            report["subdomains"] = enumerate_subdomains(domain)
        except Exception:
            report["subdomains"] = {"error": "Domain does not resolve, skipping subdomain enumeration"}

    report["summary"] = _generate_summary(report)
    return report


def _generate_summary(report: dict) -> dict:
    """Generate a human-readable summary of findings."""
    domain = report["domain"]
    summary = {
        "domain": domain,
        "is_registered": not report["availability"]["likely_available"],
        "has_ssl": report["ssl"]["success"],
        "dns_resolves": bool(report["dns"]["success"] and report["dns"]["records"].get("A")),
        "nameservers": report["dns"]["records"].get("NS", []),
        "mx_records": report["dns"]["records"].get("MX", []),
        "highlights": [],
    }

    # Registration info
    if report["rdap"]["success"] and report["rdap"]["data"]:
        rd = report["rdap"]["data"]
        for event in rd.get("events", []):
            if event.get("action") == "registration":
                summary["registration_date"] = event.get("date")
            if event.get("action") == "expiration":
                summary["expiration_date"] = event.get("date")
        if rd.get("status"):
            summary["domain_status"] = rd["status"]
        if rd.get("entities"):
            org = next((e for e in rd["entities"] if "registrant" in [r.lower() for r in e.get("roles", [])]), None)
            if org:
                summary["registrant"] = org.get("name") or org.get("organization")

    # SSL highlights
    if report["ssl"]["success"] and report["ssl"]["data"]:
        ssl_data = report["ssl"]["data"]
        summary["ssl_days_remaining"] = ssl_data.get("days_remaining", 0)
        summary["ssl_expired"] = ssl_data.get("is_expired", False)
        if ssl_data.get("days_remaining", 0) < 30:
            summary["highlights"].append(f"SSL certificate expires in {ssl_data['days_remaining']} days!")
        if ssl_data.get("is_expired"):
            summary["highlights"].append("SSL certificate is EXPIRED")

    # DNS highlights
    if report["dns"]["success"]:
        records = report["dns"]["records"]
        if records.get("CNAME"):
            summary["has_cname"] = True
            summary["cname_target"] = records["CNAME"]

    # Subdomain highlights
    if "subdomains" in report and isinstance(report["subdomains"], dict):
        discovered = report["subdomains"].get("discovered", [])
        if discovered:
            summary["subdomains_found"] = len(discovered)
            summary["highlights"].append(f"Found {len(discovered)} active subdomains")

    return summary


# ══════════════════════════════════════════════════════════
#  CLI
# ══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Domain Research Tool — RDAP / WHOIS / DNS / SSL lookups",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python domain_lookup.py example.com
  python domain_lookup.py example.com --type rdap
  python domain_lookup.py example.com --type dns --dns-types A,MX,TXT
  python domain_lookup.py example.com --type ssl
  python domain_lookup.py example.com --type all --output report.json
  python domain_lookup.py --batch domains.txt --output batch_results.json
  python domain_lookup.py 1.1.1.1 --type reverse
  python domain_lookup.py example.com --type subdomains
        """
    )
    parser.add_argument("target", help="Domain name or IP address to research")
    parser.add_argument("--type", "-t", default="all",
                        choices=["rdap", "whois", "dns", "ssl", "all", "availability",
                                 "reverse", "subdomains", "multi-dns"],
                        help="Type of lookup to perform (default: all)")
    parser.add_argument("--dns-types", default=",".join(DEFAULT_DNS_TYPES),
                        help="Comma-separated DNS record types (default: A,AAAA,MX,NS,TXT,CNAME,SOA)")
    parser.add_argument("--batch", help="File with domains (one per line) for batch processing")
    parser.add_argument("--output", "-o", help="Output JSON file path")
    parser.add_argument("--format", "-f", default="json", choices=["json", "text"],
                        help="Output format (default: json)")

    args = parser.parse_args()

    # Batch mode
    if args.batch:
        with open(args.batch) as f:
            domains = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        results = []
        for domain in domains:
            r = full_research(domain)
            results.append(r)
            print(f"✓ {domain}", file=sys.stderr)

        output = json.dumps(results, indent=2, ensure_ascii=False)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"\nResults saved to {args.output}", file=sys.stderr)
        else:
            print(output)
        return

    # Single domain
    target = args.target.strip()
    lookup_type = args.type

    if lookup_type == "rdap":
        result = rdap_lookup(target)
    elif lookup_type == "whois":
        result = whois_lookup(target)
    elif lookup_type == "dns":
        dns_types = [t.strip() for t in args.dns_types.split(",")]
        result = dns_lookup(target, dns_types)
    elif lookup_type == "ssl":
        result = ssl_check(target)
    elif lookup_type == "availability":
        result = check_availability(target)
    elif lookup_type == "reverse":
        result = reverse_dns(target)
    elif lookup_type == "subdomains":
        result = enumerate_subdomains(target)
    elif lookup_type == "multi-dns":
        result = dns_resolver_info(target)
    elif lookup_type == "all":
        result = full_research(target)

    output = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Results saved to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
