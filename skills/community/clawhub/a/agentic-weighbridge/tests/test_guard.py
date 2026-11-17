#!/usr/bin/env python3
"""Table-driven test for the one guard that judges every destination (ASCII only, stdlib only).

Run from the package root:  python3 tests/test_guard.py
Exit 0 when every case behaves as the table says.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "scripts", "weigh_x402_endpoint.py")
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import weigh_x402_endpoint as w  # noqa: E402

# url, substring that must appear in the refusal
REFUSED = [
    ("http://seller.example/paid", "https"),
    ("ftp://seller.example/paid", "https"),
    ("https://127.0.0.1/paid", "private/loopback"),
    ("https://localhost/paid", "loopback"),
    ("https://10.0.0.5/paid", "private/loopback"),
    ("https://169.254.169.254/latest/meta-data", "private/loopback"),
    ("https://[::1]/paid", "private/loopback"),
    ("https://192.168.1.1/admin", "private/loopback"),
    ("https://", "missing host"),
    ("not a url", "https"),
    ("https://host-that-does-not-resolve-xyz.invalid/paid", "cannot resolve"),
]

# urls that must be allowed through the guard
ALLOWED = ["https://xhagents.xyz/api/x402-trust"]

# strings that would mean a payment path exists in the read-only weigher
FORBIDDEN = ["eth_account", "X-PAYMENT", "x402Client", "private_key", "send_transaction", "sign_transfer"]


def main():
    fails = 0
    total = 0
    for url, want in REFUSED:
        total += 1
        got = w.guard_url(url)
        ok = got is not None and want in got
        print(("OK   " if ok else "FAIL ") + "%-52s -> %s" % (url, got))
        fails += 0 if ok else 1
    for url in ALLOWED:
        total += 1
        got = w.guard_url(url)
        ok = got is None
        print(("OK   " if ok else "FAIL ") + "%-52s -> %s" % (url, got or "allowed"))
        fails += 0 if ok else 1
    total += 1
    src = open(SCRIPT, encoding="utf-8").read()
    hits = [f for f in FORBIDDEN if f in src]
    print(("OK   " if not hits else "FAIL ") + "no payment path in the script -> %s" % (hits or "none"))
    fails += 0 if not hits else 1
    total += 1
    nonascii = [c for c in src if ord(c) > 126]
    print(("OK   " if not nonascii else "FAIL ") + "script is ASCII-only -> %s" % (set(nonascii) or "yes"))
    fails += 0 if not nonascii else 1
    print("\n%d/%d LULUS" % (total - fails, total))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
