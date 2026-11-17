#!/usr/bin/env python3
"""elder_care.py — family care-circle coordination: roster, tasks, meds, events, briefs.

Offline, stdlib-only. State: care_state.json beside the script (or --state).
Commands: person | profile | task | med | event | today | visit-brief | visit-report
          | meeting | emergency-card | handoff
NOT a medical device: family logistics only. Clinicians own the clinical truth.
"""
import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

DEFAULT_STATE = Path(__file__).resolve().parent / "care_state.json"

DOW = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
REFILL_THRESHOLD = 7


def load(state):
    if Path(state).exists():
        return json.loads(Path(state).read_text())
    return {"people": [], "profile": {}, "tasks": [], "meds": [], "events": [],
            "visits": [], "questions": []}


def save(st, state):
    Path(state).write_text(json.dumps(st, indent=2))


def today_dow():
    return DOW[date.today().weekday()]


# ------------------------------------------------------------------ person
def cmd_person(a, st, state):
    if a.action == "add":
        p = {"name": a.name, "role": a.role or "", "phone": a.phone or "",
             "tz": a.tz or "", "notes": a.notes or "", "strengths": a.strengths or "",
             "limits": a.limits or ""}
        st["people"].append(p)
        save(st, state)
        print(f"person added: {p['name']} ({p['role']})")
    elif a.action == "list":
        if not st["people"]:
            print("(no people yet)")
        for p in st["people"]:
            print(f"  {p['name']:<12} {p['role']:<10} tz={p['tz']:<4} {p['phone']}")
            if p.get("strengths"):
                print(f"      strengths: {p['strengths']}")
            if p.get("limits"):
                print(f"      limits:    {p['limits']}")


def cmd_profile(a, st, state):
    changes = []
    for opt, key in [("conditions", "conditions"), ("allergies", "allergies"),
                     ("code_status", "code_status"), ("doctors", "doctors"),
                     ("pharmacy", "pharmacy"), ("insurance", "insurance"),
                     ("keys", "key_locations"), ("hospital", "preferred_hospital"),
                     ("baseline", "baseline_function")]:
        v = getattr(a, opt)
        if v:
            st["profile"][key] = v
            changes.append(f"{key}={v}")
    save(st, state)
    print("profile updated: " + (", ".join(changes) if changes else "(nothing)"))
    if st["profile"]:
        print(json.dumps(st["profile"], indent=2, ensure_ascii=False))


# ------------------------------------------------------------------ tasks
def cmd_task(a, st, state):
    if a.action == "add":
        t = {"title": a.title, "recur": a.recur, "owner": a.owner or "",
             "rotation": [x.strip() for x in a.rotation.split(",")] if a.rotation else [],
             "dow": a.dow, "due": a.due, "critical": a.critical,
             "done_dates": []}
        st["tasks"].append(t)
        save(st, state)
        own = t["owner"] or f"rotation: {', '.join(t['rotation'])}" or "UNASSIGNED"
        print(f"task added: {t['title']} [{t['recur']}] owner={own}")
    elif a.action == "list":
        for t in st["tasks"]:
            own = t["owner"] or (f"rot:{','.join(t['rotation'])}" if t["rotation"] else "UNASSIGNED")
            crit = " *CRIT" if t.get("critical") else ""
            print(f"  [{t['recur']:<8}] {t['title']:<30} owner={own}{crit}")
    elif a.action == "done":
        found = False
        for t in st["tasks"]:
            if a.title.lower() in t["title"].lower():
                t.setdefault("done_dates", []).append(date.today().isoformat())
                found = done = True
        save(st, state)
        print(f"marked done: {a.title}" if found else f"no task matching '{a.title}'")


def tasks_due_today(st):
    d = date.today()
    out = []
    for t in st["tasks"]:
        if t["recur"] == "daily":
            out.append((t, "today"))
        elif t["recur"] == "weekly" and t.get("dow") == today_dow():
            out.append((t, "today"))
        elif t["recur"] == "once" and t.get("due"):
            due = date.fromisoformat(t["due"])
            if due <= d:
                out.append((t, f"due {t['due']}" + (" OVERDUE" if due < d else "")))
    return out


def rotation_owner_today(t):
    if not t.get("rotation"):
        return t.get("owner", "")
    idx = date.today().toordinal() % len(t["rotation"])
    return f"{t['rotation'][idx]} (rot {idx + 1}/{len(t['rotation'])})"


# ------------------------------------------------------------------ meds
def cmd_med(a, st, state):
    if a.action == "add":
        m = {"name": a.name, "dose": a.dose or "", "refill_left": a.refill_left,
             "refill_note": a.refill_note or "", "times": a.times or ""}
        st["meds"].append(m)
        save(st, state)
        print(f"med added: {m['name']} {m['dose']}")
    elif a.action == "list":
        for m in st["meds"]:
            rl = f" refill {m.get('refill_left', '?')}d" if m.get("refill_left") is not None else ""
            print(f"  {m['name']:<20} {m['dose']:<12]}{rl}")
    elif a.action == "update":
        for m in st["meds"]:
            if m["name"].lower() == a.name.lower():
                if a.dose:
                    m["dose"] = a.dose
                if a.refill_left is not None:
                    m["refill_left"] = a.refill_left
                if a.note is not None:
                    m["refill_note"] = a.note
                save(st, state)
                print(f"med updated: {m['name']} -> {m}")
                return
        print(f"no med named '{a.name}'")


def refill_radar(st):
    out = []
    for m in st["meds"]:
        rl = m.get("refill_left")
        if rl is not None and rl <= REFILL_THRESHOLD:
            out.append(m)
    return out


# ------------------------------------------------------------------ events
def cmd_event(a, st, state):
    if a.action == "log":
        e = {"date": a.date or date.today().isoformat(), "text": a.text,
             "severity": a.severity, "tag": a.tag or ""}
        st["events"].append(e)
        st["events"].sort(key=lambda x: x["date"])
        save(st, state)
        print(f"event logged {e['date']} sev{e['severity']}: {e['text']}")
    elif a.action == "list":
        for e in st["events"][-20:]:
            print(f"  {e['date']} [sev{e['severity']}] {e['tag'] + ': ' if e['tag'] else ''}{e['text']}")


# ------------------------------------------------------------------ today
def cmd_today(a, st, state):
    d = date.today()
    on_call = []
    for t, why in tasks_due_today(st):
        own = rotation_owner_today(t)
        first = own.split()[0] if own.strip() else ""
        if first and first not in ("UNASSIGNED",):
            on_call.append(first)
    print(f"TODAY {d.strftime('%a %Y-%m-%d')} — coverage: {', '.join(dict.fromkeys(on_call)) or 'none scheduled'}")
    for t, why in tasks_due_today(st):
        own = rotation_owner_today(t)
        crit = " *CRIT" if t.get("critical") else ""
        print(f"  {t['title']:<45} [{own}]{crit}  ({why})")
    unassigned = [t for t in st["tasks"]
                  if not t.get("owner") and not t.get("rotation")
                  and (t["recur"] != "once" or (t.get("due") and date.fromisoformat(t["due"]) >= d))]
    if unassigned:
        print(f"  FLAG: {len(unassigned)} task(s) UNASSIGNED — assign or drop:")
        for t in unassigned:
            print(f"    - {t['title']}")
    radar = refill_radar(st)
    for m in radar:
        print(f"  refill radar: {m['name']} {m.get('refill_left')}d left"
              + (f" | {m.get('refill_note')}" if m.get("refill_note") else ""))
    # appointments (once tasks with future due) - next 7 days
    for t in st["tasks"]:
        if t["recur"] == "once" and t.get("due"):
            due = date.fromisoformat(t["due"])
            if d < due <= d + timedelta(days=7):
                print(f"  upcoming: {t['title']} {t['due']} [{t.get('owner') or 'UNASSIGNED'}]")
    print("  (emergencies: call local emergency services first)")


# ------------------------------------------------------------------ visits
def cmd_visit_brief(a, st, state):
    doc = a.doctor.lower()
    last = None
    for v in st["visits"]:
        if doc in v.get("doctor", "").lower():
            last = v
    print("=" * 60)
    print(f"VISIT BRIEF — {a.doctor} — prepared {date.today()}")
    print("=" * 60)
    print("\nMEDICATION LIST (family-maintained; reconcile with chart):")
    if not st["meds"]:
        print("  (none recorded)")
    for m in st["meds"]:
        print(f"  {m['name']} {m['dose']} {m.get('times', '')}".rstrip())
    if last:
        print(f"\nEVENTS SINCE LAST VISIT ({last['date']}):")
        shown = 0
        for e in st["events"]:
            if e["date"] > last["date"]:
                print(f"  {e['date']} [sev{e['severity']}] {e['text']}")
                shown += 1
        if not shown:
            print("  (none)")
        print(f"\nCHANGES SINCE LAST VISIT: {last.get('changes', '(not recorded)')}")
    else:
        print("\nEVENTS (all logged — no prior visit recorded):")
        for e in st["events"][-10:]:
            print(f"  {e['date']} [sev{e['severity']}] {e['text']}")
    print("\nQUESTIONS TO ASK:")
    if not st["questions"]:
        print("  (none accumulated)")
    for q in st["questions"]:
        if not q.get("asked"):
            print(f"  - {q['text']}")
    print("\nVISIT REPORT (fill in waiting room / car, file same day):")
    print("  date: ______  provider: ______")
    print("  what changed: ______")
    print("  med changes: ______ (if any -> update med list TODAY)")
    print("  follow-ups: ______  next appt: ______")


def cmd_visit_report(a, st, state):
    v = {"date": a.date or date.today().isoformat(), "doctor": a.doctor,
         "changes": a.changes or "", "meds_changed": a.meds_changed or "",
         "followups": a.followups or "", "next": a.next or ""}
    st["visits"].append(v)
    # mark relevant questions asked
    if a.questions_asked:
        for q in st["questions"]:
            if not q.get("asked") and q["text"].lower() in a.questions_asked.lower():
                q["asked"] = True
    save(st, state)
    print(f"visit filed: {v['doctor']} {v['date']}")
    if v["meds_changed"] and "no" not in v["meds_changed"].lower():
        print("  !! MEDS CHANGED — run med update NOW; then reprint emergency card")


def cmd_question(a, st, state):
    if a.action == "add":
        st["questions"].append({"text": a.text, "asked": False, "added": date.today().isoformat()})
        save(st, state)
        print(f"question queued for next visit: {a.text}")
    elif a.action == "list":
        for q in st["questions"]:
            mark = "x" if q.get("asked") else " "
            print(f"  [{mark}] {q['text']}")


# ------------------------------------------------------------------ meeting
def cmd_meeting(a, st, state):
    d = date.today()
    month_ago = (d - timedelta(days=30)).isoformat()
    print(f"MONTHLY CARE MEETING — {d}")
    print("=" * 50)
    overdue = []
    for t in st["tasks"]:
        if t["recur"] == "once" and t.get("due") and t["due"] < d.isoformat() and date.fromisoformat(t["due"]) >= date.fromisoformat("2020-01-01"):
            if t["due"] not in t.get("done_dates", []):
                overdue.append(t)
    if overdue:
        print("\n1. OVERDUE one-off tasks:")
        for t in overdue:
            print(f"   - {t['title']} due {t['due']} [{t.get('owner') or 'UNASSIGNED'}]")
    recent = [e for e in st["events"] if e["date"] >= month_ago]
    older = [e for e in st["events"] if e["date"] < month_ago and e["date"] >= (d - timedelta(days=60)).isoformat()]
    print(f"\n2. EVENT TREND: {len(recent)} events in last 30d vs {len(older)} in prior 30d")
    sev3 = [e for e in recent if e["severity"] >= 3]
    if sev3:
        print(f"   !! {len(sev3)} severity-3 (safety) events this month:")
        for e in sev3:
            print(f"      {e['date']} {e['text']}")
    if len(recent) > len(older):
        print("   trend UP — review events at next doctor visit")
    load_map = {}
    for t in st["tasks"]:
        owner = t.get("owner") or (t["rotation"][0] if t.get("rotation") else None)
        per = {"daily": 30, "weekly": 4, "monthly": 1}.get(t["recur"], 0)
        if owner:
            load_map[owner] = load_map.get(owner, 0) + per
    print("\n3. TASK LOAD (est. tasks/30d per person):")
    for who, n in sorted(load_map.items(), key=lambda kv: -kv[1]):
        print(f"   {who:<12} {n}")
    if load_map:
        vals = list(load_map.values())
        if max(vals) >= 2 * max(min(vals), 1):
            top = max(load_map, key=load_map.get)
            print(f"   -> IMBALANCE: {top} carries 2x+ the minimum — rebalance before resentment")
    print("\n4. REFILL / UPCOMING:")
    for m in st["meds"]:
        rl = m.get("refill_left")
        if rl is not None:
            print(f"   {m['name']}: {rl}d left")
    for t in st["tasks"]:
        if t["recur"] == "once" and t.get("due") and d < date.fromisoformat(t["due"]) <= d + timedelta(days=30):
            print(f"   upcoming: {t['title']} {t['due']}")
    print("\n5. DOCUMENTS CHECK: advance directive current? POA accessible? insurance valid?")
    print("6. RESPITE: who needs a weekend off next month? Book it now.")
    print("\n(observations over interpretations; clinicians own the truth)")


# ------------------------------------------------------------------ emergency card
def cmd_emergency_card(a, st, state):
    p = st["profile"]
    people = st["people"]
    print("=" * 46)
    print("EMERGENCY INFORMATION — KEEP WITH PATIENT".center(46))
    print("=" * 46)
    name = p.get("name", "________")
    print(f"Name: {name}   DOB: {p.get('dob', '____')}")
    print(f"Address: {p.get('address', '____')}")
    print()
    print("CALL IN ORDER:")
    for i, person in enumerate(people[:4], 1):
        print(f"  {i}. {person['name']} ({person['role']}) {person['phone']}")
    print()
    print(f"Conditions: {p.get('conditions', '____')}")
    print(f"Allergies: {p.get('allergies', '____')}")
    print()
    print("MEDICATIONS (family list, verify date):")
    for m in st["meds"]:
        print(f"  {m['name']} {m['dose']}")
    print()
    print(f"Doctors: {p.get('doctors', '____')}")
    print(f"Pharmacy: {p.get('pharmacy', '____')}")
    print(f"Insurance: {p.get('insurance', '____')}")
    print(f"Code status: {p.get('code_status', '____')}")
    print(f"Baseline: {p.get('baseline_function', '____')}")
    print(f"Preferred hospital: {p.get('preferred_hospital', '____')}")
    print(f"Keys/lockbox: {p.get('key_locations', '____')}")
    print()
    print(f"Generated {date.today()} — REPRINT after any med change / quarterly".center(46))
    print("=" * 46)


# ------------------------------------------------------------------ handoff
def cmd_handoff(a, st, state):
    print(f"CARE HANDOFF — prepared for {a.person} — {date.today()}")
    print("=" * 50)
    p = st["profile"]
    print("RECIPIENT PROFILE:")
    for k in ("conditions", "allergies", "code_status", "baseline_function"):
        if p.get(k):
            print(f"  {k}: {p[k]}")
    print("\nCARE CIRCLE:")
    for person in st["people"]:
        print(f"  {person['name']} ({person['role']}) {person['phone']} tz={person['tz']}")
        if person.get("notes"):
            print(f"    notes: {person['notes']}")
    print("\nROUTINE (recurring tasks):")
    for t in st["tasks"]:
        if t["recur"] != "once":
            own = t.get("owner") or "rot:" + ",".join(t.get("rotation", []))
            when = {"daily": "daily", "weekly": f"weekly {t.get('dow', '?')}"}.get(t["recur"], t["recur"])
            print(f"  {when:<14} {t['title']:<30} [{own}]")
    print("\nMEDS:")
    for m in st["meds"]:
        print(f"  {m['name']} {m['dose']} {m.get('times', '')}".rstrip())
        if m.get("refill_note"):
            print(f"    refill: {m['refill_note']}")
    print("\nNEXT 7 DAYS:")
    d = date.today()
    for t in st["tasks"]:
        if t["recur"] == "once" and t.get("due") and d <= date.fromisoformat(t["due"]) <= d + timedelta(days=7):
            print(f"  {t['due']} {t['title']} [{t.get('owner') or 'UNASSIGNED'}]")
    print("\nRECENT EVENTS (context):")
    for e in st["events"][-5:]:
        print(f"  {e['date']} [sev{e['severity']}] {e['text']}")
    print("\n(questions -> the coordinator, not the group chat)")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--state", default=str(DEFAULT_STATE))
    sub = p.add_subparsers(dest="cmd", required=True)

    pe = sub.add_parser("person")
    pe.add_argument("action", choices=["add", "list"])
    pe.add_argument("--name")
    pe.add_argument("--role")
    pe.add_argument("--phone")
    pe.add_argument("--tz")
    pe.add_argument("--notes")
    pe.add_argument("--strengths")
    pe.add_argument("--limits")

    pr = sub.add_parser("profile")
    pr.add_argument("--name", help="recipient name")
    pr.add_argument("--dob")
    pr.add_argument("--address")
    for opt in ("conditions", "allergies", "code-status", "doctors", "pharmacy",
                "insurance", "keys", "hospital", "baseline"):
        pr.add_argument(f"--{opt}")

    ta = sub.add_parser("task")
    ta.add_argument("action", choices=["add", "list", "done"])
    ta.add_argument("title", nargs="?")
    ta.add_argument("--recur", choices=["daily", "weekly", "monthly", "once"], default="once")
    ta.add_argument("--owner")
    ta.add_argument("--rotation", help="comma-separated names")
    ta.add_argument("--dow", choices=DOW)
    ta.add_argument("--due")
    ta.add_argument("--critical", action="store_true")

    me = sub.add_parser("med")
    me.add_argument("action", choices=["add", "list", "update"])
    me.add_argument("name", nargs="?")
    me.add_argument("--dose")
    me.add_argument("--times")
    me.add_argument("--refill-left", type=int)
    me.add_argument("--refill-note", dest="refill_note")
    me.add_argument("--note")

    ev = sub.add_parser("event")
    ev.add_argument("action", choices=["log", "list"])
    ev.add_argument("text", nargs="?")
    ev.add_argument("--date")
    ev.add_argument("--severity", type=int, default=1)
    ev.add_argument("--tag")

    sub.add_parser("today")
    vb = sub.add_parser("visit-brief")
    vb.add_argument("doctor")
    vr = sub.add_parser("visit-report")
    vr.add_argument("--doctor", required=True)
    vr.add_argument("--date")
    vr.add_argument("--changes")
    vr.add_argument("--meds-changed")
    vr.add_argument("--followups")
    vr.add_argument("--next")
    vr.add_argument("--questions-asked")

    qu = sub.add_parser("question")
    qu.add_argument("action", choices=["add", "list"])
    qu.add_argument("text", nargs="?")

    sub.add_parser("meeting")
    sub.add_parser("emergency-card")
    hf = sub.add_parser("handoff")
    hf.add_argument("person")

    a = p.parse_args()
    st = load(a.state)
    handlers = {
        "person": cmd_person, "profile": cmd_profile, "task": cmd_task, "med": cmd_med,
        "event": cmd_event, "today": cmd_today, "visit-brief": lambda a, st, s: cmd_visit_brief(a, st, s),
        "visit-report": cmd_visit_report, "question": cmd_question, "meeting": cmd_meeting,
        "emergency-card": cmd_emergency_card, "handoff": cmd_handoff,
    }
    handlers[a.cmd](a, st, a.state)


if __name__ == "__main__":
    main()
