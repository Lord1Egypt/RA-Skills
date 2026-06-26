#!/usr/bin/env python3
"""SkillPay.me billing for finance-radar."""

import json, sys, argparse, os
import urllib.request, urllib.error

API = "https://skillpay.me/api/v1"
SKILL_ID = "3529d76e-2c8c-42bc-b3d4-34f650c623ce"


def _key(o=None):
    return o or os.environ.get("SKILLPAY_API_KEY")


def _post(path, body, key):
    req = urllib.request.Request(f"{API}{path}", data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "X-API-Key": key}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())


def _get(path, key):
    req = urllib.request.Request(f"{API}{path}", headers={"X-API-Key": key})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())


def charge(uid, amount=0.001, key=None):
    k = _key(key)
    if not k: return {"success": False, "error": "SKILLPAY_API_KEY not set"}
    d = _post("/billing/charge", {"user_id": uid, "skill_id": SKILL_ID, "amount": amount,
        "currency": "USDT", "description": "Finance Radar"}, k)
    if d.get("success"): return {"success": True, "charged": amount, "data": d}
    return {"success": False, "needs_payment": bool(d.get("payment_url")),
        "payment_url": d.get("payment_url", ""), "balance": d.get("balance", 0),
        "message": d.get("message", "charge failed")}


def balance(uid, key=None):
    k = _key(key)
    if not k: return {"success": False, "error": "SKILLPAY_API_KEY not set"}
    return {"success": True, "data": _get(f"/billing/balance?user_id={uid}", k)}


def payment_link(uid, amount=5.0, key=None):
    k = _key(key)
    if not k: return {"success": False, "error": "SKILLPAY_API_KEY not set"}
    return {"success": True, "data": _post("/billing/payment-link",
        {"user_id": uid, "skill_id": SKILL_ID, "Amount": amount}, k)}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--user-id", required=True)
    p.add_argument("--amount", type=float, default=0.001)
    p.add_argument("--api-key", default=None)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--charge", action="store_true", default=True)
    g.add_argument("--balance", action="store_true")
    g.add_argument("--payment-link", action="store_true")
    a = p.parse_args()
    if a.balance: r = balance(a.user_id, a.api_key)
    elif a.payment_link: r = payment_link(a.user_id, a.amount or 5.0, a.api_key)
    else: r = charge(a.user_id, a.amount, a.api_key)
    print(json.dumps(r, indent=2, ensure_ascii=False))
    sys.exit(0 if r.get("success") else 1)
