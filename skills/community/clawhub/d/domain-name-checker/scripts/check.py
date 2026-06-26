#!/usr/bin/env python3
# /// script
# dependencies = ["rich", "httpx"]
# ///
"""
domain-name-checker — check domain availability and brainstorm names.
Usage:
    python check.py eagerbots
    python check.py eagerbots.ai
    python check.py eagerbots clawbay openclaw
    python check.py --brainstorm "a tool for checking eBay prices"
"""

import argparse
import socket
import subprocess
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from rich.console import Console
from rich.table import Table
from rich import box
from rich.text import Text

console = Console()

DEFAULT_TLDS = [".com", ".net", ".org", ".io", ".ai", ".co", ".app", ".dev", ".xyz"]

PREFIXES = ["get", "use", "try", "go", "my"]
SUFFIXES = ["app", "hq", "ai", "io"]


def dns_check(domain: str, timeout: int = 3) -> str:
    """Return 'available', 'taken', or 'unknown'. Uses dig subprocess for reliable timeout."""
    try:
        result = subprocess.run(
            ["dig", "+short", "+time=2", "+tries=1", domain, "A"],
            capture_output=True, text=True, timeout=timeout + 1
        )
        out = result.stdout.strip()
        if out:
            return "taken"
        # dig returned empty — could be NXDOMAIN or no A record, check stderr/return code
        err = result.stderr.lower()
        if "nxdomain" in err or result.returncode == 0:
            return "available"
        return "unknown"
    except subprocess.TimeoutExpired:
        return "unknown"
    except FileNotFoundError:
        # dig not available, fall back to socket
        try:
            socket.setdefaulttimeout(timeout)
            socket.getaddrinfo(domain, None)
            return "taken"
        except socket.gaierror as e:
            msg = str(e).lower()
            if any(x in msg for x in ["name or service not known", "nodename nor servname", "nxdomain", "non-existent"]):
                return "available"
            return "unknown"
        except Exception:
            return "unknown"
        finally:
            socket.setdefaulttimeout(None)
    except Exception:
        return "unknown"


def whois_check(domain: str) -> str | None:
    """Optional whois cross-check. Returns 'available', 'taken', or None if whois unavailable."""
    try:
        result = subprocess.run(
            ["whois", domain],
            capture_output=True, text=True, timeout=8
        )
        output = result.stdout.lower()
        if any(x in output for x in ["no match", "not found", "no entries found", "available", "status: free"]):
            return "available"
        if any(x in output for x in ["registrar:", "registrant:", "creation date:", "registered on"]):
            return "taken"
        return None
    except Exception:
        return None


def check_domain(domain: str) -> tuple[str, str]:
    """Returns (domain, status)."""
    status = dns_check(domain, timeout=2)
    return domain, status


def namecheap_url(domain: str) -> str:
    return f"https://www.namecheap.com/domains/registration/results/?domain={domain}"


def status_cell(status: str) -> Text:
    if status == "available":
        return Text("✅ Available", style="bold green")
    elif status == "taken":
        return Text("❌ Taken", style="bold red")
    else:
        return Text("⚠️  Unknown", style="bold yellow")


def check_name(name: str, tlds: list[str] = DEFAULT_TLDS) -> list[tuple[str, str]]:
    """Check a base name across all TLDs. Returns list of (domain, status)."""
    domains = [name + tld for tld in tlds]
    results = {}
    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = {ex.submit(check_domain, d): d for d in domains}
        for f in as_completed(futures):
            domain, status = f.result()
            results[domain] = status
    return [(d, results[d]) for d in domains]


def check_full_domain(domain: str) -> list[tuple[str, str]]:
    """Check a fully qualified domain."""
    _, status = check_domain(domain)
    return [(domain, status)]


def suggest_alternatives(base: str) -> list[str]:
    """Generate alternative domain names."""
    alts = []
    for p in PREFIXES:
        alts.append(f"{p}{base}.com")
        alts.append(f"{p}-{base}.com")
    for s in SUFFIXES:
        alts.append(f"{base}{s}.com")
        alts.append(f"{base}-{s}.com")
    return alts[:10]  # limit


def print_results_table(results: list[tuple[str, str]], title: str = "Domain Availability"):
    table = Table(title=title, box=box.ROUNDED, show_header=True, header_style="bold cyan")
    table.add_column("Domain", style="white", min_width=25)
    table.add_column("Status", min_width=16)
    table.add_column("Register", style="dim blue")

    for domain, status in results:
        link = namecheap_url(domain) if status in ("available", "unknown") else ""
        table.add_row(domain, status_cell(status), link)

    console.print(table)


def brainstorm_names(description: str) -> list[str]:
    """Use OpenRouter LLM to brainstorm candidate domain base names."""
    import httpx
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        console.print("[red]OPENROUTER_API_KEY not set. Cannot brainstorm.[/red]")
        sys.exit(1)

    prompt = (
        f"Generate 10 short, memorable, brandable domain name base words (no TLD) for: {description}\n"
        "Rules: lowercase, no hyphens, max 12 chars each, one per line, no explanation."
    )

    try:
        resp = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": "anthropic/claude-haiku-4-5",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 200,
            },
            timeout=20,
        )
        resp.raise_for_status()
        text = resp.json()["choices"][0]["message"]["content"]
        names = [line.strip().lower() for line in text.strip().splitlines() if line.strip()]
        # strip any accidental TLDs or numbering
        cleaned = []
        for n in names:
            n = n.lstrip("0123456789.-) ")
            n = n.split(".")[0]
            if n:
                cleaned.append(n)
        return cleaned[:10]
    except Exception as e:
        console.print(f"[red]LLM call failed: {e}[/red]")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="domain-name-checker: check domain availability")
    parser.add_argument("names", nargs="*", help="Domain name(s) or full domains to check")
    parser.add_argument("--brainstorm", metavar="DESCRIPTION", help="Brainstorm names from a description (requires OPENROUTER_API_KEY)")
    args = parser.parse_args()

    if args.brainstorm:
        console.print(f"\n[bold cyan]🧠 Brainstorming names for:[/bold cyan] {args.brainstorm}\n")
        names = brainstorm_names(args.brainstorm)
        console.print(f"[dim]Generated {len(names)} candidates: {', '.join(names)}[/dim]\n")
        for name in names:
            results = check_name(name)
            print_results_table(results, title=f"[bold]{name}[/bold]")
        return

    if not args.names:
        parser.print_help()
        sys.exit(1)

    for raw in args.names:
        raw = raw.lower().strip()
        # Detect if it's a full domain (has a dot and a known TLD pattern)
        if "." in raw:
            results = check_full_domain(raw)
            print_results_table(results, title=f"[bold]{raw}[/bold]")
        else:
            results = check_name(raw)
            print_results_table(results, title=f"[bold]{raw}[/bold] — TLD sweep")

            # If .com is taken, show alternatives
            com_status = next((s for d, s in results if d == raw + ".com"), "unknown")
            if com_status == "taken":
                console.print(f"\n[yellow].com is taken. Checking alternatives for [bold]{raw}[/bold]...[/yellow]\n")
                alt_domains = suggest_alternatives(raw)
                alt_results = {}
                with ThreadPoolExecutor(max_workers=10) as ex:
                    futures = {ex.submit(check_domain, d): d for d in alt_domains}
                    for f in as_completed(futures):
                        domain, status = f.result()
                        alt_results[domain] = status
                alt_list = [(d, alt_results[d]) for d in alt_domains]
                print_results_table(alt_list, title=f"[bold]{raw}[/bold] — Alternatives")


if __name__ == "__main__":
    main()
