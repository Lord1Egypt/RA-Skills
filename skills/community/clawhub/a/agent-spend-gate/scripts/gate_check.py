#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Agent Spend Gate — ASPL v0.1 CLI.

Evaluate a payment intent against the user's spend policy, with a local
hash-chained audit trail. Privacy: everything stays in ~/.paycensus-gate/.
Read-only policy evaluation; no wallet access.

Usage:
  gate_check.py --init
  gate_check.py --agent agent:me:main --amount 0.01 \
                --resource https://api.example.com/x402/data \
                [--rail x402] [--payto 0xABC...] [--policy PATH]
  gate_check.py --approve <eventHash> --approver alice
"""
import argparse
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, REPO)

HOME = os.path.join(os.path.expanduser("~"), ".paycensus-gate")
POLICY_PATH = os.path.join(HOME, "policy.json")
AUDIT_PATH = os.path.join(HOME, "audit.jsonl")
APPROVALS_PATH = os.path.join(HOME, "approvals.json")
RANK_CACHE = os.path.join(HOME, "cache", "rank.json")
RANK_URL = "https://agent.paycensus.com/data/rank.json"
RANK_TTL = 3600

DEFAULT_POLICY = {
    "apiVersion": "aspl/v0.1",
    "kind": "SpendPolicy",
    "metadata": {"name": "starter", "org": "my-org"},
    "subjects": [
        {"agent": "agent:my-org:main", "note": "edit: your agent identity"}
    ],
    "budgets": [
        {"scope": "agent:my-org:main", "currency": "USD", "monthly": 5.0,
         "alertAt": 0.8}
    ],
    "allowlists": [
        {
            "scope": "agent:my-org:main",
            "rails": ["x402", "mpp"],
            "merchants": {
                "pinned": [],
                "trustRank": {"min": 0.5}
            }
        }
    ],
    "thresholds": {"autoApproveBelow": 0.01, "requireApprovalAbove": 1.0},
    "keys": {"paymentSign": {"source": "external",
                             "note": "signing happens in your wallet, outside this policy check"}},
    "audit": {"chain": "hashlinked", "retention": "7y"}
}


def ensure_rank(policy):
    """Fetch/cache Trust Rank JSON only when a floor is configured."""
    need = False
    for al in policy.get("allowlists", []):
        if (al.get("merchants") or {}).get("trustRank"):
            need = True
            break
    if not need:
        return None
    fresh = (os.path.exists(RANK_CACHE)
             and time.time() - os.path.getmtime(RANK_CACHE) < RANK_TTL)
    if not fresh:
        req = urllib.request.Request(
            RANK_URL, headers={"User-Agent": "agent-spend-gate/1.0"})
        os.makedirs(os.path.dirname(RANK_CACHE), exist_ok=True)
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        tmp = RANK_CACHE + ".tmp"
        with open(tmp, "wb") as f:
            f.write(data)
        os.replace(tmp, RANK_CACHE)
    return RANK_CACHE


def main():
    ap = argparse.ArgumentParser(
        description="Agent Spend Gate - ASPL v0.1 policy evaluation (local, private)")
    ap.add_argument("--init", action="store_true",
                    help="create ~/.paycensus-gate/ with a starter policy")
    ap.add_argument("--agent", help="agent identity, e.g. agent:org:name")
    ap.add_argument("--amount", type=float, help="payment amount in USD")
    ap.add_argument("--resource", help="payment resource URL")
    ap.add_argument("--rail", default="x402", help="payment rail (default x402)")
    ap.add_argument("--payto", default=None, help="payTo address, 0x…")
    ap.add_argument("--policy", default=None, help="policy file path (default ~/.paycensus-gate/policy.json)")
    ap.add_argument("--approve", metavar="EVENTHASH", help="mark an evaluated intent approved")
    ap.add_argument("--approver", default=None, help="human approver name (with --approve)")
    a = ap.parse_args()

    os.makedirs(HOME, exist_ok=True)
    os.environ["GATE_POLICY"] = a.policy or POLICY_PATH
    os.environ["GATE_AUDIT"] = AUDIT_PATH
    os.environ["GATE_APPROVALS"] = APPROVALS_PATH

    if a.init:
        if os.path.exists(POLICY_PATH):
            print(json.dumps({"result": "exists", "policy": POLICY_PATH,
                              "note": "edit it, then evaluate with --agent/--amount/--resource"}))
            sys.exit(0)
        with open(POLICY_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_POLICY, f, indent=2)
        print(json.dumps({"result": "created", "policy": POLICY_PATH,
                          "note": "EDIT: agent identity, budget, pinned merchants, "
                                  "trustRank floor, thresholds. Spec: https://gate.paycensus.com/spec/"}))
        sys.exit(0)

    from engine import gate_policy as gp  # env-configured import

    if a.approve:
        if not a.approver:
            ap.error("--approve requires --approver")
        ev = gp._find_intent(a.approve, AUDIT_PATH)
        if not ev:
            print(json.dumps({"result": "error",
                              "reason": "event not found: %s" % a.approve[:22]}))
            sys.exit(2)
        intent = {"agent": ev.get("agent"),
                  "resource": (ev.get("intent") or {}).get("resource"),
                  "amountUsd": (ev.get("intent") or {}).get("amountUsd")}
        gp.set_approval(a.approve, "approved", a.approver, intent)
        print(json.dumps({"result": "approved", "eventHash": a.approve,
                          "approver": a.approver}))
        sys.exit(0)

    if not (a.agent and a.amount is not None and a.resource):
        ap.error("evaluate requires --agent, --amount, --resource "
                 "(or use --init / --approve)")

    try:
        with open(os.environ["GATE_POLICY"], "r", encoding="utf-8") as f:
            policy = json.load(f)
    except (OSError, ValueError) as ex:
        print(json.dumps({"allow": False, "status": "rejected",
                          "reason": "policy unreadable: %s - run --init first" % str(ex)[:80],
                          "eventHash": None}))
        sys.exit(1)

    rank_path = ensure_rank(policy)
    os.environ["GATE_RANK"] = rank_path or ""
    gp.RANK_PATH = rank_path or ""  # engine reads this global at evaluate-time

    dec = gp.evaluate(agent=a.agent, resource=a.resource,
                      amount_usd=float(a.amount), rail=a.rail,
                      pay_to=a.payto, policy=policy, audit_path=AUDIT_PATH)
    dec["note"] = ("proceed only if allow=true; pending = ask the human, then "
                   "re-evaluate after --approve")
    print(json.dumps(dec, indent=1))
    sys.exit(0 if dec.get("allow") else 1)


if __name__ == "__main__":
    main()
