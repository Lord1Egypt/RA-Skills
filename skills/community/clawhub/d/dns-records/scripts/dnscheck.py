#!/usr/bin/env python3
"""dnscheck — DNS record lookup tool. Zero dependencies."""
import socket, subprocess, sys, argparse, json, re

def dig(domain, rtype="A"):
    """Use system dig if available, fall back to socket."""
    try:
        out = subprocess.run(
            ["dig", "+short", "+timeout=5", rtype, domain],
            capture_output=True, text=True, timeout=10
        )
        lines = [l.strip() for l in out.stdout.strip().split("\n") if l.strip()]
        return lines if lines else []
    except (FileNotFoundError, subprocess.TimeoutExpired):
        if rtype == "A":
            try:
                return [r[4][0] for r in socket.getaddrinfo(domain, None, socket.AF_INET)]
            except Exception:
                return []
        elif rtype == "AAAA":
            try:
                return [r[4][0] for r in socket.getaddrinfo(domain, None, socket.AF_INET6)]
            except Exception:
                return []
        return []

def check_domain(domain, rtypes=None):
    if rtypes is None:
        rtypes = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]
    result = {"domain": domain, "records": {}}
    for rt in rtypes:
        records = dig(domain, rt)
        if records:
            result["records"][rt] = records
    return result

def main():
    p = argparse.ArgumentParser(prog="dnscheck", description="DNS record lookup")
    p.add_argument("domains", nargs="+", help="Domains to look up")
    p.add_argument("-t", "--type", nargs="+", default=None, help="Record types (A, AAAA, MX, NS, TXT, CNAME, SOA)")
    p.add_argument("--json", action="store_true", help="JSON output")
    args = p.parse_args()

    results = []
    for domain in args.domains:
        r = check_domain(domain, args.type)
        results.append(r)
        if not args.json:
            print(f"\n🔍 {domain}")
            if not r["records"]:
                print("  ❌ No records found")
                continue
            for rt, vals in r["records"].items():
                for v in vals[:5]:
                    print(f"  {rt:>6}  {v}")
    
    if args.json:
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
