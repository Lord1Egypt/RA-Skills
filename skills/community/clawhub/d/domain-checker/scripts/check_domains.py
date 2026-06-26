#!/usr/bin/env python3
"""Domain availability checker — no system dependencies (no whois/dig CLI needed).

Uses:
- socket.getaddrinfo() for DNS A record check (stdlib)
- HTTP whois API fallback via urllib (stdlib)
- Direct whois protocol via socket (port 43, stdlib)

Usage:
    python3 check_domains.py domain1.com domain2.com ...
    echo "domain1.com domain2.com" | python3 check_domains.py
"""

import socket
import sys
import time

# WHOIS servers by TLD
WHOIS_SERVERS = {
    "com": "whois.verisign-grs.com",
    "net": "whois.verisign-grs.com",
    "org": "whois.pir.org",
    "io": "whois.nic.io",
    "ai": "whois.nic.ai",
    "so": "whois.nic.so",
    "dev": "whois.nic.google",
    "app": "whois.nic.google",
    "me": "whois.nic.me",
    "co": "whois.nic.co",
    "cc": "ccwhois.verisign-grs.com",
    "xyz": "whois.nic.xyz",
    "tech": "whois.nic.tech",
    "info": "whois.afilias.net",
}

NOT_FOUND_PATTERNS = [
    "no match for",
    "not found",
    "no data found",
    "no object found",
    "no entries found",
    "is available",
    "status: free",
    "domain not found",
]

CREATED_PATTERNS = [
    "creation date:",
    "created:",
    "registration time:",
    "registered on:",
    "domain registration date:",
]


def whois_query(domain: str) -> str:
    """Direct whois protocol query via TCP port 43."""
    tld = domain.rsplit(".", 1)[-1].lower()
    server = WHOIS_SERVERS.get(tld)

    if not server:
        # Try whois.nic.{tld} as fallback
        server = f"whois.nic.{tld}"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((server, 43))
        sock.sendall((domain + "\r\n").encode())

        response = b""
        while True:
            try:
                data = sock.recv(4096)
                if not data:
                    break
                response += data
            except socket.timeout:
                break
        sock.close()
        return response.decode("utf-8", errors="replace")
    except Exception:
        return ""


def dns_check(domain: str) -> tuple[bool, bool]:
    """Check DNS A records via stdlib socket. Returns (has_a_record, has_any_record)."""
    has_a = False
    try:
        results = socket.getaddrinfo(domain, None, socket.AF_INET, socket.SOCK_STREAM)
        has_a = len(results) > 0
    except (socket.gaierror, socket.herror, OSError):
        pass

    has_v6 = False
    try:
        results = socket.getaddrinfo(domain, None, socket.AF_INET6, socket.SOCK_STREAM)
        has_v6 = len(results) > 0
    except (socket.gaierror, socket.herror, OSError):
        pass

    return has_a, has_a or has_v6


def check_domain(domain: str) -> str:
    """Check a single domain. Returns verdict string."""
    domain = domain.strip().lower()

    # Step 1: whois query
    whois_text = whois_query(domain)
    whois_lower = whois_text.lower()

    has_created = any(p in whois_lower for p in CREATED_PATTERNS)
    has_not_found = any(p in whois_lower for p in NOT_FOUND_PATTERNS)

    # Extract creation date for display
    created_line = ""
    if has_created:
        for line in whois_text.splitlines():
            ll = line.lower().strip()
            if any(p in ll for p in CREATED_PATTERNS):
                created_line = line.strip()
                break

    # Step 2: DNS check
    has_a, has_any_dns = dns_check(domain)

    # Step 3: Cross-verify
    if has_created:
        return f"❌ {domain:<30s} TAKEN    {created_line}"
    elif has_not_found and not has_any_dns:
        return f"✅ {domain:<30s} AVAILABLE"
    elif has_not_found and has_any_dns:
        return f"⚠️  {domain:<30s} LIKELY TAKEN (has DNS records)"
    elif has_any_dns:
        return f"⚠️  {domain:<30s} LIKELY TAKEN (has DNS records)"
    elif whois_text.strip():
        # Got whois response but no clear signal
        return f"❓ {domain:<30s} UNKNOWN  (whois unclear — check manually)"
    else:
        return f"❓ {domain:<30s} UNKNOWN  (whois server unreachable — check manually)"


def main():
    domains = []

    if len(sys.argv) > 1:
        domains = sys.argv[1:]
    elif not sys.stdin.isatty():
        for line in sys.stdin:
            domains.extend(line.strip().split())

    if not domains:
        print("Usage: python3 check_domains.py domain1.com domain2.com ...")
        print("   or: echo 'domain1.com domain2.com' | python3 check_domains.py")
        sys.exit(1)

    print(f"Checking {len(domains)} domain(s)...")
    print("Method: whois (port 43) + DNS cross-verification (pure Python, no system deps)")
    print("─" * 56)

    available = taken = unknown = 0

    for d in domains:
        result = check_domain(d)
        print(result)

        if "AVAILABLE" in result:
            available += 1
        elif "TAKEN" in result:
            taken += 1
        else:
            unknown += 1

        # Rate limit
        if len(domains) > 1:
            time.sleep(1)

    print("─" * 56)
    print(f"Summary: {len(domains)} checked — ✅ {available} available, ❌ {taken} taken, ❓ {unknown} unknown")


if __name__ == "__main__":
    main()
