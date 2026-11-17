#!/usr/bin/env python3
"""Backup 3-2-1 Auditor — real data-loss risk audit for normal people.

Stdlib only. Registry is a local JSON file next to the skill.

Commands:
  add     --asset NAME --copies "c1,c2,..." --value CLASS   register/update
  list                                                           registry view
  audit                                                          3-2-1 verdicts
  blast                                                          ransomware reach
  price                                                          recovery pricing
  plan                                                           minimum-cost fixes
  drill   --asset NAME --result "..." | --due                   restore-test log
"""
import argparse
import datetime
import json
import pathlib
import sys

REG = pathlib.Path(__file__).resolve().parent.parent / "backup-registry.json"

VALUE_CLASSES = {"irreplaceable", "painful", "recreate-cheap"}

# Copy classifier: substring -> (class, media, offsite, ransomware-proof)
# media: disk/nas/cloud/optical/remote-repo ; offsite True/False
COPY_TYPES = {
    "icloud": ("live-sync", "cloud", True, False),
    "google drive": ("live-sync", "cloud", True, False),
    "dropbox": ("live-sync", "cloud", True, False),
    "onedrive": ("live-sync", "cloud", True, False),
    "cloud sync": ("live-sync", "cloud", True, False),
    "versioned cloud": ("versioned-cloud", "cloud", True, True),
    "cloud versioned": ("versioned-cloud", "cloud", True, True),
    "backblaze": ("versioned-cloud", "cloud", True, True),
    "snapshot": ("versioned-cloud", "nas", False, True),
    "nas": ("offline-attached", "nas", False, False),
    "time machine": ("offline-attached", "disk", False, False),
    "external": ("offline-attached", "disk", False, False),
    "hdd": ("offline-attached", "disk", False, False),
    "ssd": ("offline-attached", "disk", False, False),
    "drawer": ("offline-rotated", "disk", False, True),
    "unplugged": ("offline-rotated", "disk", False, True),
    "safe deposit": ("offsite-physical", "disk", True, True),
    "relative": ("offsite-physical", "disk", True, True),
    "bank": ("offsite-physical", "disk", True, True),
    "office": ("offsite-physical", "disk", True, True),
    "github": ("remote-repo", "remote-repo", True, True),
    "gitlab": ("remote-repo", "remote-repo", True, True),
    "laptop": ("primary", "disk", False, False),
    "phone": ("primary", "disk", False, False),
    "pc": ("primary", "disk", False, False),
    "workstation": ("primary", "disk", False, False),
    "computer": ("primary", "disk", False, False),
}


def classify_copy(desc):
    d = desc.lower()
    for key, val in COPY_TYPES.items():
        if key in d:
            return val
    return ("unknown", "unknown", False, False)


def load():
    if REG.exists():
        return json.loads(REG.read_text())
    return {"assets": [], "drills": []}


def save(reg):
    REG.write_text(json.dumps(reg, indent=2, ensure_ascii=False))


def asset_verdict(asset):
    copies = [c.strip() for c in asset["copies"].split(",") if c.strip()]
    info = [classify_copy(c) for c in copies]
    # effective copy count: primaries+backups, dedup by device class
    n_copies = len(copies)
    media = {i[1] for i in info if i[1] != "unknown"}
    n_media = len(media)
    offsite = any(i[2] for i in info)
    versioned = any(i[0] == "versioned-cloud" or i[0] == "remote-repo" for i in info)
    air_gapped = any(i[3] and i[0] in {"offline-rotated", "offsite-physical"} for i in info)
    survivable = sum(1 for i in info if i[3])
    ok3 = n_copies >= 3
    ok2 = n_media >= 2
    ok1 = offsite
    if ok3 and ok2 and ok1:
        verdict = "PASS"
    elif n_copies >= 2:
        verdict = "FRAGILE"
    else:
        verdict = "FAIL"
    return dict(copies=copies, info=info, n_copies=n_copies, n_media=n_media,
                offsite=offsite, versioned=versioned, air_gapped=air_gapped,
                survivable=survivable, ok3=ok3, ok2=ok2, ok1=ok1, verdict=verdict)


def cmd_add(args):
    reg = load()
    value = args.value.lower()
    if value not in VALUE_CLASSES:
        print(f"--value must be one of {sorted(VALUE_CLASSES)}")
        return 1
    for a in reg["assets"]:
        if a["name"].lower() == args.asset.lower():
            a["copies"] = args.copies
            a["value"] = value
            save(reg)
            print(f"updated: {args.asset}")
            return 0
    reg["assets"].append({"name": args.asset, "copies": args.copies, "value": value})
    save(reg)
    print(f"added: {args.asset}")
    return 0


def cmd_list(args):
    reg = load()
    if not reg["assets"]:
        print("Registry empty. Add assets with the add command.")
        return 0
    for a in reg["assets"]:
        v = asset_verdict(a)
        print(f"{a['name']}  [{a['value']}]  -> {v['verdict']}")
        print(f"   copies: {', '.join(v['copies'])}")
    return 0


def cmd_audit(args):
    reg = load()
    if not reg["assets"]:
        print("Registry empty.")
        return 1
    failures = 0
    for a in reg["assets"]:
        v = asset_verdict(a)
        print(f"ASSET: {a['name']} [{a['value']}]")
        print(f"  copies: {', '.join(v['copies'])}")
        print(f"  3 copies: {'PASS' if v['ok3'] else 'FAIL'} ({v['n_copies']})"
              f"   2 media: {'PASS' if v['ok2'] else 'FAIL'} ({v['n_media']})"
              f"   offsite: {'PASS' if v['ok1'] else 'FAIL'}")
        if not v["versioned"]:
            print("  rollback/versioning: NONE — sync-only copies mirror deletions/encryption")
        if a["value"] == "irreplaceable" and v["verdict"] != "PASS":
            failures += 1
            print("  VERDICT: FAIL for irreplaceable data — fix before anything else")
        else:
            print(f"  VERDICT: {v['verdict']}")
        print()
    print(f"irreplaceable assets failing 3-2-1: {failures}")
    return 0


def cmd_blast(args):
    reg = load()
    print("RANSOMWARE BLAST RADIUS (assume main machine compromised NOW)\n")
    for a in reg["assets"]:
        v = asset_verdict(a)
        print(f"ASSET: {a['name']}")
        for c, i in zip(v["copies"], v["info"]):
            fate = "SURVIVES" if i[3] else "DIES (reachable/synced)"
            print(f"  [{fate:22}] {c}  ({i[0]})")
        if v["survivable"] == 0:
            print("  !! zero independent copies — ransomware = total loss")
        print()
    return 0


PRICING = {
    "irreplaceable": "recovery lab $300-3000, ~40% success (media intact); often unrecoverable",
    "painful": "days-weeks of rebuilding via agencies/banks; some originals gone forever",
    "recreate-cheap": "minutes-hours (clone/reinstall); $0 marginal",
}


def cmd_price(args):
    reg = load()
    print("HONEST RECOVERY PRICING\n")
    for a in reg["assets"]:
        print(f"{a['name']} [{a['value']}]: {PRICING[a['value']]}")
    return 0


def cmd_plan(args):
    reg = load()
    print("MINIMUM-COST REDUNDANCY PLAN\n")
    for a in reg["assets"]:
        v = asset_verdict(a)
        name, val = a["name"], a["value"]
        recs = []
        if not v["ok3"]:
            recs.append("add a 3rd copy")
        if not v["ok2"]:
            recs.append("put it on a second media class (external HDD vs SSD/cloud)")
        if not v["ok1"]:
            recs.append("one offsite leg (versioned cloud OR drive at relative/bank)")
        if not v["versioned"]:
            recs.append("make one copy VERSIONED (rollback) — plain sync mirrors damage")
        if v["survivable"] == 0:
            recs.append("add an AIR-GAPPED copy (rotated unplugged drive) — currently nothing survives ransomware")
        if val == "irreplaceable" and not v["air_gapped"]:
            recs.append("estate rule: one copy needing NO account (physical drive)")
        if recs:
            print(f"{name}: " + "; ".join(recs))
        else:
            print(f"{name}: PASS — keep drills quarterly")
    last = reg["drills"][-1] if reg["drills"] else None
    if last:
        print(f"\nlast restore drill: {last['date']} ({last['asset']})")
    print("NEXT DRILL DUE: " + str(next_drill_due(reg)))
    return 0


def next_drill_due(reg):
    if not reg["drills"]:
        return "now (never done)"
    last = datetime.date.fromisoformat(reg["drills"][-1]["date"])
    return (last + datetime.timedelta(days=90)).isoformat()


def cmd_drill(args):
    reg = load()
    if args.due:
        print(f"drill due: {next_drill_due(reg)}")
        print("restore 3 RANDOM files from a BACKUP copy (not primary), OPEN them, log result")
        return 0
    if not (args.asset and args.result):
        print("need --asset and --result (or --due)")
        return 1
    reg["drills"].append({
        "date": datetime.date.today().isoformat(),
        "asset": args.asset,
        "result": args.result,
    })
    save(reg)
    print(f"drill logged: {args.asset} @ {reg['drills'][-1]['date']}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--asset", required=True)
    a.add_argument("--copies", required=True, help="comma-separated copy locations")
    a.add_argument("--value", required=True, help="irreplaceable|painful|recreate-cheap")
    a.set_defaults(func=cmd_add)
    l = sub.add_parser("list")
    l.set_defaults(func=cmd_list)
    u = sub.add_parser("audit")
    u.set_defaults(func=cmd_audit)
    b = sub.add_parser("blast")
    b.set_defaults(func=cmd_blast)
    p = sub.add_parser("price")
    p.set_defaults(func=cmd_price)
    pl = sub.add_parser("plan")
    pl.set_defaults(func=cmd_plan)
    d = sub.add_parser("drill")
    d.add_argument("--asset")
    d.add_argument("--result")
    d.add_argument("--due", action="store_true")
    d.set_defaults(func=cmd_drill)
    args = ap.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
