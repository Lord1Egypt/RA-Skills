#!/usr/bin/env python3
"""Gate — ASPL v0.1 policy evaluator (v2: Trust Rank floor + approval flow).

Evaluates a payment intent against an Agent Spend Policy and appends a
hash-linked audit event. Policy file is JSON (same fields as the YAML spec
at https://gate.paycensus.com/spec/). Read-only: the caller proceeds only when
decision.allow is true; signing happens externally.

Merchant risk (honest tiering):
  - pinned merchants        -> always allowed, no external data needed
  - stablecoin rails        -> Trust Rank score from real settlement behaviour
                               (local cached rank.json from public census)
  - no rank data            -> rejected when a trustRank floor is configured

Decision statuses:
  auto-approved  (amount <= autoApproveBelow)
  approved       (human approval found for this intent)
  pending        (between thresholds, awaiting approval)
  rejected       (policy violation or above hard cap)
"""
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from urllib.parse import urlparse

_LOCAL = os.path.join(os.path.expanduser("~"), ".paycensus-gate")
POLICY_PATH = os.environ.get("GATE_POLICY", os.path.join(_LOCAL, "policy.json"))
AUDIT_PATH = os.environ.get("GATE_AUDIT", os.path.join(_LOCAL, "audit.jsonl"))
APPROVALS_PATH = os.environ.get("GATE_APPROVALS", os.path.join(_LOCAL, "approvals.json"))
RANK_PATH = os.environ.get("GATE_RANK", "")


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_policy(path=POLICY_PATH):
    try:
        with open(path) as f:
            return json.load(f)
    except OSError:
        return None


def _rank_maps():
    """addr -> score, domain -> score (normalized 0-1) from Trust Rank."""
    addr, dom = {}, {}
    try:
        with open(RANK_PATH) as f:
            for e in json.load(f).get("ranked", []):
                s = float(e.get("score") or 0) / 100.0
                if e.get("addr"):
                    addr[e["addr"].lower()] = s
                if e.get("domain"):
                    dom[e["domain"].lower()] = s
    except (OSError, ValueError):
        pass
    return addr, dom


def _load_approvals():
    try:
        with open(APPROVALS_PATH) as f:
            return json.load(f)
    except (OSError, ValueError):
        return []


def _approval_for(agent, resource, amount_usd):
    """An approved entry matching this exact intent?"""
    for a in _load_approvals():
        if (a.get("state") == "approved"
                and a.get("agent") == agent
                and a.get("resource") == resource
                and abs(float(a.get("amountUsd") or 0) - amount_usd) < 1e-9):
            return a
    return None


def _month_spend(audit_path, scope):
    m = time.strftime("%Y-%m")
    total = 0.0
    try:
        with open(audit_path) as f:
            for line in f:
                try:
                    ev = json.loads(line)
                except ValueError:
                    continue
                if (ev.get("type") == "payment.evaluated"
                        and ev.get("decision", {}).get("allow")
                        and ev.get("eventMonth") == m
                        and scope in (ev.get("decision", {}).get("scopes") or [])):
                    total += float(ev.get("intent", {}).get("amountUsd") or 0)
    except OSError:
        pass
    return total


def _prev_hash(audit_path):
    last = ""
    try:
        with open(audit_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        last = json.loads(line).get("hash", last)
                    except ValueError:
                        pass
    except OSError:
        pass
    return last


def _merchant_check(resource, pay_to, alists):
    """Returns (matched, reason). matched=True means allow this stage."""
    dom = urlparse(resource).netloc.lower()
    floor = None
    for al in alists:
        tr = (al.get("merchants") or {}).get("trustRank")
        if tr:
            floor = float(tr.get("min", 0))
        for m in (al.get("merchants") or {}).get("pinned", []):
            if m.get("domain", "").lower() == dom or m.get("resource") == resource:
                return True, "merchant pinned: %s" % dom
    addr_map, dom_map = _rank_maps()
    score = addr_map.get((pay_to or "").lower()) or dom_map.get(dom)
    if score is not None:
        if floor is None or score >= floor:
            return True, "trustRank %.2f %s (floor %.2f)" % (
                score, ">= floor" if floor is not None else "(no floor)", floor or 0)
        return False, "trustRank %.2f < floor %.2f for %s" % (score, floor, dom)
    if floor is not None:
        return False, "no trust data for merchant %s (floor %.2f configured)" % (dom, floor)
    return False, "merchant %s not pinned and no trustRank floor configured" % dom


def evaluate(agent, resource, amount_usd, rail="x402", pay_to=None,
             policy=None, audit_path=AUDIT_PATH):
    pol = policy or load_policy()
    if not pol:
        return _finish(agent, resource, amount_usd, rail, "auto-approved",
                       "no policy loaded - allow (bootstrap)", [], audit_path, pay_to)
    reasons = []
    scopes = []

    # rail permission
    ok = True
    status = None
    for al in pol.get("allowlists", []):
        scopes.append(al.get("scope"))
        rails = al.get("rails")
        if rails and rail not in rails:
            ok = False
            status = "rejected"
            reasons.append("rail %s not permitted" % rail)

    # merchant allowlist / trust rank
    if ok:
        ok, reason = _merchant_check(resource, pay_to,
                                     pol.get("allowlists", []))
        status = None if ok else "rejected"
        reasons.append(reason)

    # budgets (month-to-date from our own audit stream)
    if ok:
        for b in pol.get("budgets", []):
            monthly = float(b.get("monthly", 0))
            if monthly <= 0:
                continue
            spent = _month_spend(audit_path, b.get("scope"))
            if spent + amount_usd > monthly:
                ok = False
                status = "rejected"
                reasons.append("budget exceeded for %s: %.2f+%.4f > %.2f"
                               % (b.get("scope"), spent, amount_usd, monthly))
            else:
                reasons.append("budget ok for %s: %.4f/%.2f"
                               % (b.get("scope"), spent + amount_usd, monthly))

    # approval thresholds
    if ok:
        th = pol.get("thresholds", {})
        auto = float(th.get("autoApproveBelow", 0.01))
        require = float(th.get("requireApprovalAbove", auto))
        if amount_usd <= auto:
            status = "auto-approved"
            reasons.append("amount %.4f <= autoApprove %.2f" % (amount_usd, auto))
        elif amount_usd > require:
            ok = False
            status = "rejected"
            reasons.append("amount %.4f above hard cap %.2f" % (amount_usd, require))
        else:
            apr = _approval_for(agent, resource, amount_usd)
            if apr:
                status = "approved"
                reasons.append("approved by %s at %s" % (apr.get("approver", "?"),
                                                         apr.get("ts", "?")))
            else:
                ok = False
                status = "pending"
                reasons.append("amount %.4f between %.2f and %.2f - approval required"
                               % (amount_usd, auto, require))

    return _finish(agent, resource, amount_usd, rail,
                   status or ("auto-approved" if ok else "rejected"),
                   "; ".join(reasons) or "policy empty", scopes, audit_path, pay_to)


def _finish(agent, resource, amount_usd, rail, status, reason, scopes,
            audit_path, pay_to=None):
    allow = status in ("auto-approved", "approved")
    ev = {
        "v": "aspl/v0.1",
        "type": "payment.evaluated",
        "ts": _now(),
        "eventMonth": time.strftime("%Y-%m"),
        "agent": agent,
        "intent": {"resource": resource, "amountUsd": round(amount_usd, 6),
                   "rail": rail, "payTo": pay_to},
        "decision": {"allow": allow, "status": status, "reason": reason,
                     "scopes": scopes},
    }
    ev["prevHash"] = _prev_hash(audit_path)
    canon = json.dumps(ev, sort_keys=True, separators=(",", ":"))
    ev["hash"] = hashlib.sha256(canon.encode()).hexdigest()
    os.makedirs(os.path.dirname(audit_path), exist_ok=True)
    with open(audit_path, "a") as f:
        f.write(json.dumps(ev, sort_keys=True) + "\n")
    out = dict(ev["decision"])
    out["eventHash"] = ev["hash"]
    return out


def set_approval(event_hash, state, approver, intent=None):
    """Mark an evaluated intent approved/rejected (human decision)."""
    aps = _load_approvals()
    entry = {"eventHash": event_hash, "state": state, "approver": approver,
             "ts": _now()}
    if intent:
        entry.update(intent)
    aps = [a for a in aps if a.get("eventHash") != event_hash] + [entry]
    os.makedirs(os.path.dirname(APPROVALS_PATH), exist_ok=True)
    with open(APPROVALS_PATH, "w") as f:
        json.dump(aps, f, indent=1)
    return entry


def pending_intents(audit_path=AUDIT_PATH):
    """Latest pending evaluated intent per (agent, resource, amount)."""
    pend = {}
    try:
        with open(audit_path) as f:
            for line in f:
                try:
                    ev = json.loads(line)
                except ValueError:
                    continue
                d = ev.get("decision", {})
                if d.get("status") == "pending":
                    key = (ev.get("agent"), ev.get("intent", {}).get("resource"),
                           ev.get("intent", {}).get("amountUsd"))
                    pend[key] = ev
    except OSError:
        pass
    # drop intents already decided via approvals (pending view only)
    decided = {a.get("eventHash") for a in _load_approvals()}
    return [ev for ev in pend.values() if ev.get("hash") not in decided]


def verify_chain(audit_path=AUDIT_PATH):
    prev = ""
    n = 0
    with open(audit_path) as f:
        for line in f:
            ev = json.loads(line)
            h = ev.get("hash")
            p = ev.get("prevHash")
            canon = json.dumps({k: v for k, v in ev.items() if k != "hash"},
                               sort_keys=True, separators=(",", ":"))
            if hashlib.sha256(canon.encode()).hexdigest() != h:
                return False, "hash mismatch at event %d" % n
            if p != prev:
                return False, "chain break at event %d" % n
            prev = h
            n += 1
    return True, "chain ok: %d events" % n


def _find_intent(event_hash, audit_path):
    try:
        with open(audit_path) as f:
            for line in f:
                ev = json.loads(line)
                if ev.get("hash", "").startswith(event_hash):
                    return ev
    except OSError:
        pass
    return None


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "eval":
        d = evaluate(sys.argv[2], sys.argv[3], float(sys.argv[4]),
                     sys.argv[5] if len(sys.argv) > 5 else "x402")
        print(json.dumps(d, indent=1))
    elif cmd == "approve":
        h, who = sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else "ops")
        ev = _find_intent(h, AUDIT_PATH)
        if not ev:
            print("event not found:", h[:22])
        else:
            intent = {"agent": ev["agent"],
                      "resource": ev["intent"]["resource"],
                      "amountUsd": ev["intent"]["amountUsd"]}
            set_approval(ev["hash"], "approved", who, intent)
            print("approved:", ev["agent"], ev["intent"]["resource"],
                  ev["intent"]["amountUsd"])
    elif cmd == "reject":
        h, who = sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else "ops")
        set_approval(h, "rejected", who)
        print("rejected:", h[:22])
    elif cmd == "pending":
        evs = pending_intents()
        print("pending:", len(evs))
        for ev in evs:
            print(" ", ev["hash"][:22], ev["agent"], ev["intent"]["resource"],
                  "$%s" % ev["intent"]["amountUsd"])
    elif cmd == "verify":
        ok, msg = verify_chain()
        print(("PASS " if ok else "FAIL ") + msg)
    else:
        print("usage: gate_policy.py eval <agent> <resource> <amount_usd> [rail] |"
              " approve <hash> [who] | reject <hash> | pending | verify")
