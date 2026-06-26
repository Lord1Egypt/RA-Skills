#!/usr/bin/env python3
"""Network diagnostics: ping, DNS, port check, traceroute."""

import argparse
import socket
import subprocess
import sys
import time


def check_host(host, count=4):
    """Ping-style connectivity check."""
    print(f"🏓 Checking connectivity to {host}...\n")

    try:
        ip = socket.gethostbyname(host)
        print(f"   Resolved: {host} → {ip}")
    except socket.gaierror:
        print(f"   ❌ Cannot resolve {host}")
        return False

    # Use system ping
    try:
        result = subprocess.run(
            ["ping", "-c", str(count), "-W", "2", host],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            # Extract stats
            for line in result.stdout.strip().split("\n"):
                if "packets transmitted" in line:
                    print(f"   ✅ {line.strip()}")
                elif "min/avg/max" in line or "rtt" in line:
                    print(f"   ⏱️  {line.strip()}")
            print(f"\n   ✅ {host} is reachable")
            return True
        else:
            print(f"   ❌ {host} is unreachable")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        # Fallback: try socket connect
        print("   ℹ️  ping not available, trying socket connect...")
        try:
            start = time.time()
            sock = socket.create_connection((host, 80), timeout=5)
            elapsed = (time.time() - start) * 1000
            sock.close()
            print(f"   ✅ TCP connect to {host}:80 succeeded ({elapsed:.0f}ms)")
            return True
        except Exception as e:
            print(f"   ❌ Connection failed: {e}")
            return False


def check_port(host, port):
    """Check if a TCP port is open."""
    print(f"🔌 Checking {host}:{port}...\n")

    try:
        ip = socket.gethostbyname(host)
        print(f"   Resolved: {host} → {ip}")
    except socket.gaierror:
        print(f"   ❌ Cannot resolve {host}")
        return False

    start = time.time()
    try:
        sock = socket.create_connection((host, port), timeout=5)
        elapsed = (time.time() - start) * 1000
        sock.close()
        print(f"   ✅ Port {port} is OPEN ({elapsed:.0f}ms)")
        return True
    except socket.timeout:
        print(f"   ⏰ Port {port} timed out (filtered or no response)")
        return False
    except ConnectionRefusedError:
        print(f"   ❌ Port {port} is CLOSED (connection refused)")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def dns_lookup(host):
    """Resolve DNS for a hostname."""
    print(f"🌐 DNS Lookup for {host}...\n")

    try:
        ip = socket.gethostbyname(host)
        print(f"   ✅ A record: {ip}")
    except socket.gaierror as e:
        print(f"   ❌ Resolution failed: {e}")
        return False

    # Try reverse lookup
    try:
        reverse = socket.gethostbyaddr(ip)
        print(f"   🔄 PTR record: {reverse[0]}")
    except socket.herror:
        print(f"   ℹ️  No reverse DNS found")

    # Try to get all addresses
    try:
        results = socket.getaddrinfo(host, None)
        addrs = sorted(set(r[4][0] for r in results))
        if len(addrs) > 1:
            print(f"\n   📋 All addresses:")
            for addr in addrs:
                print(f"      • {addr}")
    except Exception:
        pass

    return True


def traceroute(host):
    """Run traceroute to host."""
    print(f"🗺️  Traceroute to {host}...\n")

    try:
        result = subprocess.run(
            ["traceroute", "-m", "15", "-w", "2", host],
            capture_output=True, text=True, timeout=30
        )
        if result.stdout:
            for line in result.stdout.strip().split("\n"):
                print(f"   {line}")
        return result.returncode == 0
    except FileNotFoundError:
        print("   ℹ️  traceroute not available, trying mtr or pathping...")
        # Fallback: try to show route with Python
        try:
            ip = socket.gethostbyname(host)
            print(f"   Target IP: {ip}")
            # Basic hop detection via TTL
            print("   ℹ️  Install traceroute for full route info")
        except Exception:
            pass
        return False
    except subprocess.TimeoutExpired:
        print("   ⏰ Traceroute timed out")
        return False


def full_diagnostic(host):
    """Run all diagnostics on a host."""
    print(f"{'=' * 50}")
    print(f"  Full Diagnostic: {host}")
    print(f"{'=' * 50}\n")

    results = {}

    print("[1/4] DNS Resolution")
    print("─" * 30)
    results["dns"] = dns_lookup(host)
    print()

    print("[2/4] Connectivity Check")
    print("─" * 30)
    results["ping"] = check_host(host)
    print()

    print("[3/4] Common Port Check")
    print("─" * 30)
    for port, name in [(80, "HTTP"), (443, "HTTPS"), (22, "SSH")]:
        results[f"port_{port}"] = check_port(host, port)
        print()

    print("[4/4] Traceroute")
    print("─" * 30)
    results["traceroute"] = traceroute(host)

    print(f"\n{'=' * 50}")
    print("  Summary")
    print(f"{'=' * 50}")
    for name, ok in results.items():
        status = "✅" if ok else "❌"
        print(f"  {status} {name}")

    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"\n  {passed}/{total} checks passed")


def main():
    parser = argparse.ArgumentParser(description="🌐 Network Diagnostics")
    sub = parser.add_subparsers(dest="command")

    p_check = sub.add_parser("check", help="Ping-style connectivity check")
    p_check.add_argument("host", help="Hostname or IP to check")
    p_check.add_argument("--count", type=int, default=4, help="Number of pings")

    p_port = sub.add_parser("port", help="Check if a TCP port is open")
    p_port.add_argument("host", help="Hostname or IP")
    p_port.add_argument("port", type=int, help="Port number")

    p_dns = sub.add_parser("dns", help="DNS resolution")
    p_dns.add_argument("host", help="Hostname to resolve")

    p_full = sub.add_parser("full", help="Run all diagnostics")
    p_full.add_argument("host", help="Hostname or IP")

    args = parser.parse_args()

    if args.command == "check":
        check_host(args.host, args.count)
    elif args.command == "port":
        check_port(args.host, args.port)
    elif args.command == "dns":
        dns_lookup(args.host)
    elif args.command == "full":
        full_diagnostic(args.host)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
