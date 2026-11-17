#!/usr/bin/env python3
"""Weigh an x402 endpoint locally: free, read-only, no keys, no payment.

What it does: makes the UNPAID request, decodes the 402 challenge, checks the v2 shape, reads the
origin's discovery documents and prints a verdict per check (PASS / FAIL / ERROR). It never signs,
never pays and never reads a secret. For a signed, timestamped document that a third party can
re-check offline, use the hosted arena (see SKILL.md).

Usage:
  python3 weigh_x402_endpoint.py https://seller.example/paid/route
  python3 weigh_x402_endpoint.py https://seller.example/paid/route --method POST --json
  python3 weigh_x402_endpoint.py https://seller.example/paid/route --out ./weigh

Exit codes: 0 verdict payable | 2 needs_fix or not_a_402_endpoint | 1 refused, unreachable or usage error.
"""
import argparse
import base64
import ipaddress
import json
import os
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "xh-agents-weighbridge-local/1"
MAX_BODY = 65536
MAX_REQUESTS = 8
TIMEOUT = 12
NETWORK = "eip155:8453"
ASSET = "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"


def guard_url(url, allow_any_host=False):
    """Single place where a destination is judged. Returns None when allowed, else a refusal reason."""
    try:
        p = urllib.parse.urlparse(url)
    except Exception:
        return "unparsable url"
    if p.scheme != "https":
        return "scheme must be https"
    host = p.hostname or ""
    if not host:
        return "missing host"
    if not allow_any_host and host.lower() in ("localhost", "localhost.localdomain"):
        return "loopback host refused"
    try:
        infos = socket.getaddrinfo(host, None)
    except Exception:
        return "cannot resolve %s" % host
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved or ip.is_multicast:
            return "target resolves to a private/loopback address"
    return None


class Counter:
    def __init__(self, limit=MAX_REQUESTS):
        self.left = limit

    def take(self):
        if self.left <= 0:
            raise RuntimeError("request budget exhausted")
        self.left -= 1


def fetch(url, method="GET", body=None, counter=None, timeout=TIMEOUT, redirects=3):
    """One request, redirects re-checked hop by hop, body capped. Never raises for transport."""
    counter = counter or Counter()
    started = time.time()
    for _ in range(redirects + 1):
        bad = guard_url(url)
        if bad:
            return {"status": 0, "headers": {}, "body": "", "ms": 0, "error": "refused: %s" % bad}
        try:
            counter.take()
        except RuntimeError as e:
            return {"status": 0, "headers": {}, "body": "", "ms": 0, "error": str(e)}
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, method=method if data is None or method != "GET" else "POST",
                                    headers={"User-Agent": UA, "Accept": "application/json, text/plain, */*",
                                             "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                text = r.read(MAX_BODY).decode("utf-8", "replace")
                return {"status": r.status, "headers": dict(r.headers), "body": text,
                        "ms": round((time.time() - started) * 1000, 1), "error": None}
        except urllib.error.HTTPError as e:
            text = e.read(MAX_BODY).decode("utf-8", "replace")
            return {"status": e.code, "headers": dict(e.headers), "body": text,
                    "ms": round((time.time() - started) * 1000, 1), "error": None}
        except Exception as e:
            return {"status": 0, "headers": {}, "body": "", "ms": round((time.time() - started) * 1000, 1),
                    "error": "%s: %s" % (type(e).__name__, str(e)[:160])}
    return {"status": 0, "headers": {}, "body": "", "ms": 0, "error": "too many redirects"}


def header(headers, name):
    for k, v in headers.items():
        if k.lower() == name.lower():
            return (v or "").strip()
    return None


def decode_challenge(header_value, body_text):
    if header_value:
        try:
            raw = header_value.strip()
            return json.loads(base64.b64decode(raw + "=" * (-len(raw) % 4))), "header"
        except Exception:
            pass
    try:
        d = json.loads(body_text)
        if isinstance(d, dict) and ("accepts" in d or "x402Version" in d):
            return d, "body"
    except Exception:
        pass
    return None, None


def weigh(url, method="auto"):
    checks = []
    cap = Counter()

    def add(cid, status, detail):
        checks.append({"id": cid, "status": status, "detail": detail})

    verbs = ["GET", "POST"] if method not in ("GET", "POST") else [method]
    probed, chosen = [], None
    for verb in verbs:
        res = fetch(url, verb, {"probe": True} if verb == "POST" else None, cap)
        probed.append({"verb": verb, "status": res["status"], "ms": res["ms"], "error": res["error"]})
        if res["status"] == 402 and chosen is None:
            chosen = (verb, res)
    if probed and all(p["status"] == 0 for p in probed):
        add("reachable", "ERROR", "no answer: %s" % (probed[0]["error"] or "transport error"))
        return {"target": url, "checks": checks, "verbs_probed": probed, "verdict": "unreachable"}
    add("reachable", "PASS", "verbs: " + ", ".join("%s->%s" % (p["verb"], p["status"]) for p in probed))
    add("verb_report", "PASS", "challenge answered on %s" % (chosen[0] if chosen else "no verb"))
    if chosen is None:
        add("challenge_on_the_paid_verb", "FAIL", "no 402 on the probed verb(s)")
        for cid in ("challenge_is_v2", "accepts_shape", "payer_can_sign"):
            add(cid, "ERROR", "not measurable without a 402")
        return {"target": url, "checks": checks, "verbs_probed": probed, "verdict": "not_a_402_endpoint"}

    verb, res = chosen
    add("challenge_on_the_paid_verb", "PASS", "402 with PAYMENT-REQUIRED on %s" % verb)
    raw = header(res["headers"], "payment-required") or header(res["headers"], "x-payment-required")
    challenge, source = decode_challenge(raw, res["body"])
    if challenge is None:
        add("challenge_is_v2", "FAIL", "challenge is not decodable JSON")
        add("accepts_shape", "ERROR", "not measurable")
        add("payer_can_sign", "ERROR", "not measurable")
    else:
        fails = []
        if challenge.get("x402Version") != 2:
            fails.append("x402Version=%r" % challenge.get("x402Version"))
        r = challenge.get("resource")
        rurl = r.get("url") if isinstance(r, dict) else r
        if not isinstance(r, dict):
            fails.append("resource is not the v2 object form")
        elif not str(rurl or "").startswith("https://"):
            fails.append("resource.url is not absolute https")
        elif str(rurl).rstrip("/") != url.rstrip("/"):
            fails.append("resource.url does not match the route")
        add("challenge_is_v2", "FAIL" if fails else "PASS", "; ".join(fails) if fails else "v2 shape, url matches")
        accepts = challenge.get("accepts") or []
        afails = []
        if not accepts:
            afails.append("accepts[] is empty")
        for i, a in enumerate(accepts):
            if a.get("network") != NETWORK:
                afails.append("accepts[%d].network=%r" % (i, a.get("network")))
            if str(a.get("asset", "")).lower() != ASSET:
                afails.append("accepts[%d].asset=%r" % (i, a.get("asset")))
            amt = a.get("amount")
            if not isinstance(amt, str) or not amt.isdigit():
                afails.append("accepts[%d].amount=%r (v2 wants a decimal string)" % (i, amt))
            if "maxAmountRequired" in a:
                afails.append("accepts[%d] still carries v1 maxAmountRequired" % i)
        add("accepts_shape", "FAIL" if afails else "PASS",
            "; ".join(afails) if afails else "%d accept entry(ies) conform" % len(accepts))
        pfails = ["accepts[%d] extra missing name/version" % i for i, a in enumerate(accepts)
                  if not ((a.get("extra") or {}).get("name") and (a.get("extra") or {}).get("version"))]
        add("payer_can_sign", "FAIL" if pfails else ("PASS" if accepts else "ERROR"),
            "; ".join(pfails) if pfails else ("EIP-712 domain present" if accepts else "no accepts[] to judge"))

    p = urllib.parse.urlparse(url)
    origin = "%s://%s" % (p.scheme, p.netloc)
    man = fetch(origin + "/.well-known/x402", "GET", None, cap)
    lists = None
    if man["status"] == 200:
        try:
            d = json.loads(man["body"])
            keys = set()
            for r in (d.get("resources") or []):
                keys.add(str(r.get("url") if isinstance(r, dict) else r).rstrip("/"))
            for e in (d.get("entries") or []):
                rr = e.get("resource")
                keys.add(str(rr.get("url") if isinstance(rr, dict) else rr).rstrip("/"))
            lists = url.rstrip("/") in keys
        except Exception:
            lists = None
    add("discovery_manifest", "PASS" if lists is True else ("FAIL" if lists is False else "ERROR"),
        "%s/.well-known/x402 -> %s%s" % (origin, man["status"], "" if lists is None else
                                         ("; route listed" if lists else "; route NOT listed")))
    oa = fetch(origin + "/openapi.json", "GET", None, cap)
    add("openapi_present", "PASS" if oa["status"] == 200 else ("FAIL" if oa["status"] else "ERROR"),
        "openapi.json -> %s" % oa["status"])

    judged = [c["status"] for c in checks if c["id"] != "verb_report"]
    if any(c["id"] == "challenge_on_the_paid_verb" and c["status"] == "FAIL" for c in checks):
        verdict = "not_a_402_endpoint"
    elif "FAIL" in judged:
        verdict = "needs_fix"
    elif judged and all(s == "ERROR" for s in judged):
        verdict = "unknown"
    else:
        verdict = "payable"
    return {"target": url, "checks": checks, "verbs_probed": probed, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser(description="Read-only x402 endpoint weighing (no payment, no keys).")
    ap.add_argument("url")
    ap.add_argument("--method", default="auto", choices=["auto", "GET", "POST"])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out")
    args = ap.parse_args()

    bad = guard_url(args.url)
    if bad:
        print("refused: %s" % bad)
        return 1

    doc = weigh(args.url, args.method)
    if args.out:
        os.makedirs(args.out, exist_ok=True)
        safe = args.url.replace("https://", "").replace("/", "_")[:80]
        path = os.path.join(args.out, "weigh_%s.json" % safe)
        json.dump(doc, open(path, "w"), indent=2)
        print("written %s" % path)
    if args.json:
        print(json.dumps(doc, indent=2))
    else:
        print("target : %s" % doc["target"])
        for c in doc["checks"]:
            print("  %-26s %-6s %s" % (c["id"], c["status"], c["detail"][:110]))
        print("verdict: %s" % doc["verdict"])
    return 0 if doc["verdict"] == "payable" else (2 if doc["verdict"] in ("needs_fix", "not_a_402_endpoint") else 1)


if __name__ == "__main__":
    sys.exit(main())
