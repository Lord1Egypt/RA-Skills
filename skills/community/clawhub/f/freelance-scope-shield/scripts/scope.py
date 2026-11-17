#!/usr/bin/env python3
"""scope.py — freelance scope registry, request classifier, change-order
pricing, creep-pattern detector, and polite decline/counter letters.

Subcommands:
  init          create a project registry (scope.json)
  deliverable   add an included/excluded deliverable
  classify      classify a client request against the registry
  changeorder   price a change order (week-based risk multiplier)
  record        log what happened to a request (feeds pattern stats)
  pattern       creep velocity, ratio, dispute rates by type/requester
  letter        decline / counter / escalate letter citing the registry
  clauses       the six anti-creep contract clauses

Stdlib only.
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

MULT = [(2, 1.0), (5, 1.15), (99, 1.3)]      # week -> multiplier ladder
POST_MULT = 1.5
REQ_TYPES = ["new-feature", "revision", "expansion", "format-change", "deadline-shift"]


def mult_for_week(week):
    for cap, m in MULT:
        if week <= cap:
            return m
    return POST_MULT


def load(project):
    p = Path(project) if str(project) != "." else Path(".")
    f = p / "scope.json"
    if not f.exists():
        print("No scope.json in %s — run init first." % p.resolve())
        sys.exit(2)
    return json.loads(f.read_text())


def save(project, data):
    p = Path(project) if str(project) != "." else Path(".")
    (p / "scope.json").write_text(json.dumps(data, indent=2) + "\n")


# ---------------------------------------------------------------- cmds

def cmd_init(args):
    d = Path(args.project)
    d.mkdir(parents=True, exist_ok=True)
    data = {
        "project": args.project_name,
        "rate": args.rate,
        "currency": args.currency,
        "created": dt.date.today().isoformat(),
        "deliverables": [],
        "requests": [],
    }
    save(args.project, data)
    print("Registry: %s/scope.json | rate %s %s/h" %
          (d.resolve(), args.rate, args.currency))
    print("Next: add deliverables (included AND excluded).")
    return 0


def cmd_deliverable(args):
    data = load(args.project)
    data["deliverables"].append({
        "name": args.name,
        "status": "included" if args.included else "excluded",
        "hours": args.hours,
        "note": args.note or "",
    })
    save(args.project, data)
    print("%s: %s (%dh) [%s]" %
          ("INCLUDED" if args.included else "EXCLUDED", args.name,
           args.hours, args.note or "-"))
    return 0


def cmd_classify(args):
    data = load(args.project)
    req = args.request.lower()
    hits = []
    for d in data["deliverables"]:
        words = [w for w in d["name"].lower().split() if len(w) > 3]
        overlap = sum(1 for w in words if w in req)
        if overlap and overlap >= max(1, len(words) // 2):
            hits.append(d)
    inc = [d for d in hits if d["status"] == "included"]
    exc = [d for d in hits if d["status"] == "excluded"]

    verdict, advice = None, None
    if inc:
        verdict = "IN-SCOPE"
        advice = "Already paid for ('%s'). Do it, log hours against it." % inc[0]["name"]
    elif exc:
        verdict = "OUT-OF-SCOPE"
        advice = ("Matches excluded item '%s'. Change order before work." % exc[0]["name"])
    elif hits:
        verdict = "AMBIGUOUS"
        advice = ("Partial overlap with '%s'. Send written clarification "
                  "before touching it." % hits[0]["name"])
    else:
        verdict = "OUT-OF-SCOPE"
        advice = "No registry match — new work. Change order before work."
    print("Request : %s" % args.request)
    print("Est hrs : %s" % args.hours)
    print("Verdict : %s" % verdict)
    print("Action  : %s" % advice)
    print("Ref     : use --title '%s' in record/letter" % (args.title,))
    data["requests"].append({
        "date": dt.date.today().isoformat(),
        "title": args.title,
        "request": args.request,
        "hours": args.hours,
        "type": args.type,
        "requester": args.requester,
        "verdict": verdict,
        "status": "classified",
    })
    save(args.project, data)
    return 0


def cmd_changeorder(args):
    data = load(args.project)
    m = mult_for_week(args.at_week)
    price = args.hours * data["rate"] * m
    print("CHANGE ORDER — %s" % args.title)
    print("Hours        : %d" % args.hours)
    print("Base rate    : %s %s/h" % (data["rate"], data["currency"]))
    print("Week of ask  : %d  -> risk multiplier x%.2f" % (args.at_week, m))
    print("PRICE        : %s %s  (%.1fh effective)" %
          (round(price), data["currency"], args.hours * m))
    print("\nRationale: late changes force rework + context switch +")
    print("schedule compression; the ladder is in the proposal.")
    return 0


def cmd_record(args):
    data = load(args.project)
    for r in data["requests"]:
        if r["title"] == args.title:
            r["status"] = args.status
            if args.hours:
                r["hours"] = args.hours
            save(args.project, data)
            print("Recorded: '%s' -> %s (%sh)" % (args.title, args.status, r.get("hours", 0)))
            return 0
    data["requests"].append({
        "date": dt.date.today().isoformat(),
        "title": args.title, "hours": args.hours or 0, "type": args.type,
        "requester": args.requester, "verdict": "OUT-OF-SCOPE",
        "status": args.status,
    })
    save(args.project, data)
    print("Recorded new: '%s' -> %s" % (args.title, args.status))
    return 0


def cmd_pattern(args):
    data = load(args.project)
    reqs = data["requests"]
    if not reqs:
        print("No requests logged yet.")
        return 0
    contracted = sum(d["hours"] for d in data["deliverables"]
                     if d["status"] == "included") or 1
    added = sum(r.get("hours", 0) for r in reqs
                if r.get("status") in ("approved", "waived-goodwill"))
    weeks = max(1, (dt.date.today() - dt.date.fromisoformat(data["created"])).days / 7)
    print("== CREEP PATTERN — %s ==\n" % data["project"])
    print("Contracted hours : %d" % contracted)
    print("Added hours      : %d (%.0f%% creep ratio)" % (added, 100 * added / contracted))
    print("Creep velocity   : %.1f h/week" % (added / weeks))
    by_status = {}
    for r in reqs:
        by_status[r.get("status", "?")] = by_status.get(r.get("status", "?"), 0) + 1
    print("Status counts    : %s" % by_status)
    disputes = [r for r in reqs if r.get("status") == "disputed"]
    if disputes:
        print("\nDisputed requests:")
        for r in disputes:
            print("  ! %s (%s, %sh)" % (r["title"], r.get("type"), r.get("hours", 0)))
    waived = sum(r.get("hours", 0) for r in reqs if r.get("status") == "waived-goodwill")
    if waived:
        print("\nGoodwill ledger : %dh waived = %s %s unbilled" %
              (waived, waived * data["rate"], data["currency"]))
    if added / weeks > 0.15 * contracted:
        print("\nWARNING: creep velocity >15%% of contracted hours/week —")
        print("reprice at renewal or decline; this client is structurally unprofitable.")
    return 0


LETTER_TMPL = {
    "decline": """Subject: {title} — outside our agreed scope

Hi {client},

Thanks for the idea — a {title} is a solid addition.

Checking our scope registry, it falls outside what we agreed for
{project} (registry: {registry_ref}). I'd be happy to take it on as a
separate engagement — I can send a quote this week if useful.

Everything currently in scope is on track and unaffected.

Best,
{name}
""",
    "counter": """Subject: {title} — change order

Hi {client},

Good idea — and it's outside our agreed scope for {project}, so here's
the change order per our proposal's pricing ladder:

  Work        : {title}
  Estimate    : {hours} hours
  Rate        : {rate} {cur}/h (week-{week} multiplier x{mult})
  Total       : {price} {cur}

Approve this and I'll slot it in starting Monday; the original timeline
shifts by {hours} working days.

Best,
{name}
""",
    "escalate": """Subject: {project} — scope realignment

Hi {client},

We've now had {n_req} requests beyond our agreed scope (registry
attached), of which {n_waived} were absorbed as goodwill — about
{waived_h}h / {waived_val} {cur} of unbilled work.

I want to keep working together, and to do that honestly I need us to
realign: either we restate the scope to what it has actually become
(I'll send a revised quote), or we return to the original registry and
route new ideas through change orders.

Which works better for you this week?

Best,
{name}
""",
}


def cmd_letter(args):
    data = load(args.project)
    reqs = data["requests"]
    target = next((r for r in reqs if r["title"] == args.title), {})
    week = args.at_week or 4
    m = mult_for_week(week)
    hours = target.get("hours", args.hours or 0)
    price = round(hours * data["rate"] * m)
    waived = [r for r in reqs if r.get("status") == "waived-goodwill"]
    body = LETTER_TMPL[args.mode].format(
        title=args.title, client=args.client or "there", project=data["project"],
        registry_ref="scope.json v of " + data["created"],
        hours=hours, rate=data["rate"], cur=data["currency"], week=week,
        mult=m, price=price, name=args.sender,
        n_req=len(reqs), n_waived=len(waived),
        waived_h=sum(r.get("hours", 0) for r in waived),
        waived_val=sum(r.get("hours", 0) for r in waived) * data["rate"],
    )
    if args.out:
        Path(args.out).write_text(body)
        print("Letter -> %s" % args.out)
    else:
        print(body)
    return 0


CLAUSES = """1. Change-order procedure: out-of-scope work starts only after a written
   change order (price + schedule impact) is approved.
2. Deliverable definition: page/feature counts, content source, 2 revision
   rounds; "revision" vs "new work" defined by the scope registry.
3. Acceptance window: delivered work is deemed accepted after 5 business
   days without written objections.
4. Revision cap with overflow rate: revisions beyond 2 rounds billed at
   the standard hourly rate.
5. Client dependency: input delays (content/approvals/access) shift the
   delivery date day-for-day; 10 business days of silence pauses the
   project.
6. Late-change pricing ladder: week 1-2 x1.0, week 3-5 x1.15, week 6+
   x1.3, post-delivery x1.5 — stated here, so change-order prices are
   pre-agreed mechanics, not negotiations.
"""


def cmd_clauses(args):
    print("THE SIX ANTI-CREEP CONTRACT CLAUSES\n")
    print(CLAUSES)
    print("Put #6 in the proposal itself; put all six in the contract/MSA.")
    return 0


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Freelance scope shield.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    i = sub.add_parser("init", help="create registry")
    i.add_argument("--project", default=".")
    i.add_argument("--project-name", dest="project_name", required=True)
    i.add_argument("--rate", type=float, required=True)
    i.add_argument("--currency", default="USD")
    i.set_defaults(func=cmd_init)

    d = sub.add_parser("deliverable", help="add deliverable")
    d.add_argument("--project", default=".")
    d.add_argument("--name", required=True)
    d.add_argument("--hours", type=int, default=0)
    g = d.add_mutually_exclusive_group(required=True)
    g.add_argument("--included", action="store_true")
    g.add_argument("--excluded", action="store_true")
    d.add_argument("--note", default="")
    d.set_defaults(func=cmd_deliverable)

    c = sub.add_parser("classify", help="classify a request")
    c.add_argument("--project", default=".")
    c.add_argument("--request", required=True)
    c.add_argument("--title", required=True,
                    help="short name for record/letter/changes")
    c.add_argument("--hours", type=int, default=0)
    c.add_argument("--type", default="new-feature", choices=REQ_TYPES)
    c.add_argument("--requester", default="client")
    c.set_defaults(func=cmd_classify)

    co = sub.add_parser("changeorder", help="price a change order")
    co.add_argument("--project", default=".")
    co.add_argument("--title", required=True)
    co.add_argument("--hours", type=int, required=True)
    co.add_argument("--at-week", dest="at_week", type=int, default=4)
    co.set_defaults(func=cmd_changeorder)

    r = sub.add_parser("record", help="log request outcome")
    r.add_argument("--project", default=".")
    r.add_argument("--title", required=True)
    r.add_argument("--status", required=True,
                   choices=["approved", "declined", "disputed", "waived-goodwill"])
    r.add_argument("--hours", type=int, default=0)
    r.add_argument("--type", default="new-feature", choices=REQ_TYPES)
    r.add_argument("--requester", default="client")
    r.set_defaults(func=cmd_record)

    p = sub.add_parser("pattern", help="creep pattern stats")
    p.add_argument("--project", default=".")
    p.set_defaults(func=cmd_pattern)

    l = sub.add_parser("letter", help="generate decline/counter/escalate")
    l.add_argument("--project", default=".")
    l.add_argument("--title", required=True)
    l.add_argument("--mode", required=True, choices=["decline", "counter", "escalate"])
    l.add_argument("--client", help="client first name")
    l.add_argument("--sender", default="Me")
    l.add_argument("--hours", type=int, default=0)
    l.add_argument("--at-week", dest="at_week", type=int, default=0)
    l.add_argument("--out", help="write to file")
    l.set_defaults(func=cmd_letter)

    cl = sub.add_parser("clauses", help="anti-creep contract clauses")
    cl.set_defaults(func=cmd_clauses)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
