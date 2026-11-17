#!/usr/bin/env python3
"""Free Model Auditor — reusable live-test harness.

Provides three operations used by SKILL.md:
  probe   : VPN / connectivity check against overseas hosts
  catalog : fetch a provider's /v1/models catalog
  test    : live chat-completion test of one candidate model

Stdlib only. Honors HTTPS_PROXY / HTTP_PROXY so tests route through the user's
VPN/proxy when active. Importable: `from test_harness import probe_connectivity,
fetch_catalog, chat_test`.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

TIMEOUT = 120


def _opener():
    """Build an opener that respects HTTP(S)_PROXY env (Clash etc.)."""
    http = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy") or ""
    https = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or ""
    if http or https:
        proxies = {"http": http or https, "https": https or http}
        return urllib.request.build_opener(urllib.request.ProxyHandler(proxies))
    return urllib.request.build_opener()


def _models_url(base_url):
    u = base_url.rstrip("/")
    if u.endswith("/chat/completions"):
        u = u[: -len("/chat/completions")]
    return u + "/models"


def _chat_url(base_url):
    u = base_url.rstrip("/")
    if u.endswith("/chat/completions"):
        return u
    return u + "/chat/completions"


def probe_connectivity(hosts, timeout=8):
    """Return {host: bool} — True if a TCP/TLS connection succeeds (VPN on)."""
    op = _opener()
    out = {}
    for h in hosts:
        url = h if h.startswith("http") else "https://" + h
        req = urllib.request.Request(url, method="GET")
        try:
            op.open(req, timeout=timeout)
            out[h] = True
        except urllib.error.HTTPError:
            out[h] = True  # connection succeeded, just an HTTP error
        except Exception:
            out[h] = False
    return out


def fetch_catalog(base_url, api_key, timeout=TIMEOUT):
    """GET {base}/models; return list of model dicts (empty on failure)."""
    url = _models_url(base_url)
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + api_key})
    try:
        with _opener().open(req, timeout=timeout) as r:
            data = json.load(r)
        return data.get("data") or []
    except Exception as e:
        print(f"[catalog ERROR] {url}: {e}", file=sys.stderr)
        return []


def chat_test(base_url, api_key, model, prompt="用一句话介绍你自己。",
              max_tokens=120, timeout=TIMEOUT):
    """POST chat/completions. Return dict with status/ok/content/reasoning/error."""
    url = _chat_url(base_url)
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
    }).encode("utf-8")
    req = urllib.request.Request(
        url, data=body,
        headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"},
    )
    try:
        with _opener().open(req, timeout=timeout) as r:
            status = r.status
            data = json.load(r)
        msg = (data.get("choices") or [{}])[0].get("message") or {}
        content = (msg.get("content") or "").strip()
        reasoning = (msg.get("reasoning_content") or msg.get("reasoning") or "").strip()
        return {
            "model": model, "status": status, "ok": bool(content),
            "content": content[:200], "reasoning": bool(reasoning), "error": None,
        }
    except urllib.error.HTTPError as e:
        return {"model": model, "status": e.code, "ok": False,
                "content": "", "reasoning": False, "error": e.read().decode()[:200]}
    except Exception as e:
        return {"model": model, "status": 0, "ok": False,
                "content": "", "reasoning": False, "error": repr(e)[:200]}


def chat_burst(base_url, api_key, model, count=5, gap=1.0, prompt="用一句话介绍你自己。",
               max_tokens=120, timeout=TIMEOUT):
    """Send `count` sequential chat requests with `gap` seconds between calls.

    Operationalizes the availability criterion: a free model that survives a single
    request may still collapse under WorkBuddy's multi-request conversation pattern
    (first sentence OK, then 429). Returns success count and per-request statuses.
    """
    results = []
    for i in range(count):
        results.append(chat_test(base_url, api_key, model, prompt, max_tokens, timeout))
        if i < count - 1:
            time.sleep(gap)
    ok = sum(1 for r in results if r.get("ok"))
    return {
        "model": model, "total": count, "ok": ok,
        "statuses": [r.get("status") for r in results],
        "first_error": next((r.get("error") for r in results if not r.get("ok")), None),
        "pass": ok == count,
    }


def _cli():
    p = argparse.ArgumentParser(description="Free Model Auditor test harness")
    sub = p.add_subparsers(dest="cmd", required=True)

    pp = sub.add_parser("probe", help="connectivity probe for overseas hosts")
    pp.add_argument("hosts", nargs="+")

    pc = sub.add_parser("catalog", help="fetch /v1/models")
    pc.add_argument("url")
    pc.add_argument("api_key")

    pt = sub.add_parser("test", help="live chat-completion test")
    pt.add_argument("url")
    pt.add_argument("api_key")
    pt.add_argument("model")
    pt.add_argument("--prompt", default="用一句话介绍你自己。")
    pt.add_argument("--max-tokens", type=int, default=120)

    pb = sub.add_parser("burst", help="sequential multi-request availability test")
    pb.add_argument("url")
    pb.add_argument("api_key")
    pb.add_argument("model")
    pb.add_argument("--count", type=int, default=5)
    pb.add_argument("--gap", type=float, default=1.0)
    pb.add_argument("--prompt", default="用一句话介绍你自己。")
    pb.add_argument("--max-tokens", type=int, default=120)

    args = p.parse_args()
    if args.cmd == "probe":
        res = probe_connectivity(args.hosts)
        for h, ok in res.items():
            print(f"[{'OK' if ok else 'DOWN'}] {h}")
        sys.exit(0 if all(res.values()) else 1)
    if args.cmd == "catalog":
        models = fetch_catalog(args.url, args.api_key)
        print(json.dumps([m.get("id") for m in models], ensure_ascii=False, indent=2))
        sys.exit(0)
    if args.cmd == "test":
        r = chat_test(args.url, args.api_key, args.model, args.prompt, args.max_tokens)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        sys.exit(0 if r["ok"] else 1)
    if args.cmd == "burst":
        r = chat_burst(args.url, args.api_key, args.model, args.count, args.gap,
                       args.prompt, args.max_tokens)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        sys.exit(0 if r["pass"] else 1)


if __name__ == "__main__":
    _cli()
