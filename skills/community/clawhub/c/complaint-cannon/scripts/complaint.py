#!/usr/bin/env python3
"""complaint-cannon — escalation-aware complaint engine.

Cases with incident timelines, escalation-ladder letters (complaint →
escalate → final → regulator), industry/country regulator routing,
statutory window flags, detonation sequencing plan, and follow-up tracking.
100% local, single JSON store, pure stdlib.

General information only — verify current law/rules for your jurisdiction
before filing; regulations move faster than software.
"""
import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

DB = Path("complaints.json")
REMEDY_DAYS = 14          # default remedy deadline in letters
RUNG_DAYS = {2: 7, 3: 14, 4: 21}   # ladder days after rung-1 letter

REGULATORS = {
    ("telecom", "US"): [("FCC", "Informal complaint — company must respond; escalation path to formal"),
                        ("State PUC", "Billing and service disputes; utilities-style enforcement")],
    ("telecom", "EU"): [("National regulator (Ofcom UK / BNetzA DE / Arcep FR)",
                         "Binding dispute resolution schemes; complaints are free")],
    ("airline", "US"): [("DOT Aviation Consumer Protection",
                         "Statutory answer obligation; refund enforcement for canceled flights")],
    ("airline", "EU"): [("National enforcement body (NEB) + EU261 statutory claim",
                         "€250-600 compensation for 3h+ delay/cancellation — claimable directly")],
    ("banking", "US"): [("CFPB", "Company must respond within 15 days by rule; published complaint"),
                        ("OCC / FDIC (bank-dependent)", "Supervisory escalation")],
    ("banking", "EU"): [("Financial Ombudsman (UK FOS) / national complaints units",
                         "Free binding decisions for consumers")],
    ("retail", "US"): [("State Attorney General consumer protection division",
                        "Mediation; pattern tracking across complainants")],
    ("retail", "EU"): [("European Consumer Centre (cross-border) / national consumer authority",
                        "Mediation; 14-day withdrawal + 2-year conformity enforcement")],
    ("utilities", "US"): [("State PUC", "Billing dispute freeze procedures")],
    ("utilities", "EU"): [("National energy regulator", "Billing dispute schemes")],
    ("privacy", "US"): [("State AG privacy unit / FTC", "Statutory privacy complaint")],
    ("privacy", "EU"): [("Data Protection Authority (GDPR Art.77)",
                         "Free, enforceable, must be investigated")],
}

STATUTORY = {
    "US": ["FCBA: written billing dispute within 60 days of statement forces investigation",
           "Chargeback windows: typically ~120 days from transaction or expected delivery (card network rules)",
           "DOT: refunds owed for canceled flights regardless of reason"],
    "EU": ["14-day distance-selling withdrawal right",
           "2-year minimum conforming-goods liability",
           "EU261: €250-600 for 3h+ delays / cancellations (verify distance bands)",
           "GDPR Art.15/17: access and erasure requests, DPA complaint right"],
    "UK": ["14-day withdrawal (Consumer Contracts Regs)",
           "6-year limit to claim; small claims court is cheap and effective",
           "FOS: free binding ombudsman for financial services"],
}


def load() -> dict:
    if DB.exists():
        return json.loads(DB.read_text())
    return {"cases": []}


def save(db: dict) -> None:
    DB.write_text(json.dumps(db, indent=2, ensure_ascii=False))


def get_case(db: dict, cid: str) -> dict:
    for c in db["cases"]:
        if c["id"] == cid:
            return c
    sys.exit(f"case {cid} not found")


def next_id(db: dict) -> str:
    return f"C{len(db['cases']) + 1:03d}"


def d(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def timeline_text(case: dict) -> str:
    lines = []
    for e in sorted(case["events"], key=lambda x: x["date"]):
        lines.append(f"  {e['date']}: {e['text']}")
    return "\n".join(lines)


def first_letter_date(case: dict):
    letters = [c for c in case["contacts"] if c.get("kind") == "letter"]
    return min((d(c["date"]) for c in letters), default=None)


def broken_promises(case: dict) -> int:
    return sum(1 for c in case["contacts"] if c.get("result", "").lower().startswith("promise broken"))


# ---------- case / event / contact ----------

def cmd_case(args, db):
    if args.action == "add":
        case = {
            "id": next_id(db),
            "title": args.title,
            "company": args.company,
            "industry": args.industry,
            "country": args.country,
            "amount": args.amount,
            "events": [],
            "contacts": [],
            "status": "open",
            "opened": date.today().isoformat(),
        }
        db["cases"].append(case)
        save(db)
        print(f"case {case['id']} opened: {case['title']} vs {case['company']} "
              f"(${case['amount']}, {case['industry']}/{case['country']})")
    elif args.action == "list":
        for c in db["cases"]:
            print(f"{c['id']:<5}{c['status']:<7}{c['company'][:18]:<19}"
                  f"${c['amount']:>7.2f}  {c['title'][:34]} ({c['opened']})")


def cmd_event(args, db):
    case = get_case(db, args.id)
    case["events"].append({"date": args.date, "text": args.text})
    save(db)
    print(f"event logged to {case['id']}: {args.date} — {args.text[:60]}")


def cmd_contact(args, db):
    case = get_case(db, args.id)
    rec = {"date": args.date, "channel": args.channel, "person": args.person or "",
           "result": args.result, "kind": "contact"}
    case["contacts"].append(rec)
    save(db)
    print(f"contact logged to {case['id']} ({args.channel}, {args.date})")


# ---------- letters ----------

LETTER_HEAD = """To: {company} — Customer Relations / Executive Complaints
Re: Formal complaint — case {cid}: {title}
Amount at issue: ${amount:.2f}
"""

def cmd_letter(args, db):
    case = get_case(db, args.id)
    tl = timeline_text(case)
    today = date.today()
    deadline = today + timedelta(days=REMEDY_DAYS)
    if args.kind == "complaint":
        body = (
            f"\nOn {today}, I am submitting a formal complaint regarding the following "
            f"documented events:\n\n{tl}\n\n"
            f"Remedy requested: refund/replacement of ${case['amount']:.2f} "
            f"(or equivalent correction), to be completed by {deadline}.\n"
            f"Absent a substantive response by that date, I will escalate this matter "
            f"through your executive office and the applicable regulatory channels.\n"
            f"\nThis letter and the timeline above constitute my complete, dated record.\n")
        title = "FORMAL COMPLAINT (rung 1)"
    elif args.kind == "escalate":
        body = (
            f"\nMy formal complaint of (see record) has not been adequately resolved. "
            f"The documented timeline:\n\n{tl}\n\n"
            f"I am escalating to your office because frontline support has exhausted "
            f"its usefulness. Remedy requested remains ${case['amount']:.2f} plus "
            f"correction of the underlying failure, by {deadline}.\n"
            f"If unresolved at that point, I will file with the relevant regulator and "
            f"publish the documented record.\n")
        title = "ESCALATION (rung 2)"
    elif args.kind == "final":
        body = (
            f"\nThis is my final notice before external action. Timeline:\n\n{tl}\n\n"
            f"Remedy: ${case['amount']:.2f} by {deadline}.\n"
            f"Upon expiry I will, without further correspondence: "
            f"(1) file with the regulators listed for {case['industry']}/{case['country']}, "
            f"(2) dispute the charge through my card issuer within the applicable window, "
            f"and (3) publish the full documented record.\n")
        title = "FINAL NOTICE BEFORE EXTERNAL ACTION (rung 3)"
    elif args.kind == "regulator":
        regs = REGULATORS.get((case["industry"], case["country"]), [])
        reg_names = ", ".join(r[0] for r in regs) or "the competent consumer authority"
        body = (
            f"\nTo the attention of: {reg_names}\n\n"
            f"Complaint against {case['company']} ({case['industry']}, "
            f"{case['country']}). Documented timeline:\n\n{tl}\n\n"
            f"I have completed the company's internal process: formal complaint, "
            f"escalation to the executive level, and final notice — all without "
            f"adequate remedy. Remedy sought: ${case['amount']:.2f} and correction "
            f"of the practice at issue.\n"
            f"I request your office's review and intervention.\n")
        title = "REGULATOR FILING (rung 4)"
    else:
        sys.exit("letter kind must be complaint|escalate|final|regulator")
    out = LETTER_HEAD.format(company=case["company"], cid=case["id"],
                             title=case["title"], amount=case["amount"]) + f"\n{title}\n" + body
    case["contacts"].append({"date": today.isoformat(), "channel": "letter",
                             "person": args.kind, "result": "generated", "kind": "letter"})
    save(db)
    print(out)
    print("--- letter generated and logged. Tone check: factual, specific, dated. ---")


# ---------- regulators / plan / status / due ----------

def cmd_regulators(args, db):
    case = get_case(db, args.id)
    regs = REGULATORS.get((case["industry"], case["country"]), [])
    print(f"REGULATOR LADDER — {case['industry']}/{case['country']}\n")
    if not regs:
        print("  no specific routing data — use the national general consumer authority")
        print("  (verify current name; regulators reorganize)")
    for i, (name, why) in enumerate(regs, 1):
        print(f"  {i}. {name}\n     {why}")
    print("\nStatutory windows to check (verify current rules):")
    for s in STATUTORY.get(case["country"], []):
        print(f"  • {s}")


def cmd_plan(args, db):
    case = get_case(db, args.id)
    fld = first_letter_date(case)
    if not fld:
        print("PLAN — no letter sent yet\n  rung 1 (day 0): send `letter complaint` NOW — "
              "the written trail must exist before anything else")
        return
    days = (date.today() - fld).days
    bp = broken_promises(case)
    rung = 4 if bp >= 2 else (3 if days >= RUNG_DAYS[3] else
                              2 if days >= RUNG_DAYS[2] else 1)
    print(f"PLAN — {case['id']} vs {case['company']} "
          f"({days} days since first letter, {bp} broken promise(s))\n")
    print(f"  current rung: {rung}" + ("  (accelerated by broken promises)" if bp >= 2 else ""))
    nexts = {1: f"rung 2 in max {RUNG_DAYS[2]-days}d: `letter escalate`",
             2: f"rung 3 in max {RUNG_DAYS[3]-days}d: `letter final`",
             3: "rung 4 NOW: `letter regulator` + public review + exec email TOGETHER",
             4: "execute rung 4: regulator filing, public record, card dispute if in window"}
    print(f"  next: {nexts[min(rung,4)] if rung < 4 else nexts[4]}")
    if case["country"] in STATUTORY:
        print("\n  statutory windows: verify chargeback window NOW if payment was by card "
              "(typical ~120 days from transaction); missed windows close quietly.")


def cmd_due(args, db):
    today = date.today()
    found = False
    for c in db["cases"]:
        if c["status"] != "open":
            continue
        for k in c["contacts"]:
            kd = d(k["date"])
            follow = kd + timedelta(days=5 if k.get("kind") == "contact" else 7)
            if follow <= today:
                found = True
                print(f"{c['id']} vs {c['company']}: follow up owed since "
                      f"{follow.isoformat()} (last contact {k['date']}: "
                      f"{k['result'][:40]})")
    if not found:
        print("no follow-ups owed — cadence clean")


def cmd_status(args, db):
    case = get_case(db, args.id)
    fld = first_letter_date(case)
    days = (date.today() - fld).days if fld else None
    print(f"STATUS — {case['id']}: {case['title']} [{case['status'].upper()}]")
    print(f"  company: {case['company']} ({case['industry']}/{case['country']})")
    print(f"  amount: ${case['amount']:.2f}   events: {len(case['events'])}   "
          f"contacts: {len(case['contacts'])}")
    if days is not None:
        print(f"  first letter: {fld} ({days} days ago)")
    bp = broken_promises(case)
    if bp:
        print(f"  ⚠ {bp} broken promise(s) — ladder acceleration applies")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("case")
    cs = p.add_subparsers(dest="action", required=True)
    pc = cs.add_parser("add")
    pc.add_argument("title"); pc.add_argument("--company", required=True)
    pc.add_argument("--industry", default="retail",
                    choices=["telecom", "airline", "banking", "retail", "utilities", "privacy"])
    pc.add_argument("--country", default="US", choices=["US", "EU", "UK"])
    pc.add_argument("--amount", type=float, required=True)
    cs.add_parser("list")

    p = sub.add_parser("event")
    ev = p.add_subparsers(dest="action", required=True)
    pea = ev.add_parser("add")
    pea.add_argument("id")
    pea.add_argument("--date", default=date.today().isoformat())
    pea.add_argument("--text", required=True)

    p = sub.add_parser("contact")
    co = p.add_subparsers(dest="action", required=True)
    pca = co.add_parser("add")
    pca.add_argument("id")
    pca.add_argument("--date", default=date.today().isoformat())
    pca.add_argument("--channel", required=True)
    pca.add_argument("--person"); pca.add_argument("--result", required=True)

    p = sub.add_parser("letter")
    p.add_argument("kind", choices=["complaint", "escalate", "final", "regulator"])
    p.add_argument("id")

    p = sub.add_parser("regulators"); p.add_argument("id")
    p = sub.add_parser("plan"); p.add_argument("id")
    p = sub.add_parser("due")
    p = sub.add_parser("status"); p.add_argument("id")

    args = ap.parse_args()
    db = load()

    if args.cmd == "case":
        cmd_case(args, db)
    elif args.cmd == "event":
        cmd_event(args, db)
    elif args.cmd == "contact":
        cmd_contact(args, db)
    elif args.cmd == "letter":
        cmd_letter(args, db)
    elif args.cmd == "regulators":
        cmd_regulators(args, db)
    elif args.cmd == "plan":
        cmd_plan(args, db)
    elif args.cmd == "due":
        cmd_due(args, db)
    elif args.cmd == "status":
        cmd_status(args, db)


if __name__ == "__main__":
    main()
