#!/usr/bin/env python3
"""breakup-buddy — cohabitation untangler.

Catalog shared items, run fair splits, audit shared accounts against
renewal traps, settle shared expenses to one net payment, and generate
a dated move-out plan. 100% local, single JSON store, pure stdlib.
"""
import argparse
import json
import random
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

DEFAULT_DB = "untangle.json"


# ---------- storage ----------

def load(db_path: Path) -> dict:
    if db_path.exists():
        return json.loads(db_path.read_text())
    return {
        "parties": {"A": "Party A", "B": "Party B"},
        "items": [],          # shared physical items
        "accounts": [],       # shared accounts/subscriptions/services
        "expenses": [],       # shared expenses for settle-up
        "decisions": {},      # item id -> {action, to, price}
        "moveout": None,
        "created": date.today().isoformat(),
    }


def save(db_path: Path, data: dict) -> None:
    db_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))


# ---------- helpers ----------

def parse_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def depreciate(price: float, purchased: date, as_of: date, rate: float = 0.15, floor: float = 0.15) -> float:
    years = max(0.0, (as_of - purchased).days / 365.25)
    return round(price * max(floor, 1 - rate * years), 2)


def equity(item: dict, as_of: date) -> float:
    """Current value used by splits."""
    return depreciate(item["price"], parse_date(item["date"]), as_of)


def next_id(seq: list, prefix: str) -> str:
    return f"{prefix}{len(seq) + 1:03d}"


def contributions(item: dict) -> dict:
    """Return {party: contribution_fraction} from --payer (A/B/both)."""
    payer = item.get("payer", "both")
    if payer in ("A", "B"):
        return {payer: 1.0}
    return {"A": 0.5, "B": 0.5}


# ---------- items ----------

def cmd_item(args, db, dbp):
    if args.action == "add":
        item = {
            "id": next_id(db["items"], "IT"),
            "name": args.name,
            "price": args.price,
            "date": args.date,
            "payer": args.payer,
            "user": args.user,
            "sentimental": args.sentimental,
            "note": args.note or "",
        }
        db["items"].append(item)
        save(dbp, db)
        print(f"added {item['id']}: {item['name']} (${item['price']}, payer={item['payer']}, "
              f"user={item['user']}, sentimental={item['sentimental']})")
    elif args.action == "list":
        as_of = date.today()
        if not db["items"]:
            print("no items cataloged — `item add` first")
            return
        print(f"{'ID':<5}{'NAME':<24}{'PAID':>8}{'EQUITY':>9}  PAYER USER  SENT  DECISION")
        for it in db["items"]:
            eq = equity(it, as_of)
            dec = db["decisions"].get(it["id"], {})
            dec_s = dec.get("action", "—")
            if dec.get("to"):
                dec_s += f"→{dec['to']}"
            print(f"{it['id']:<5}{it['name'][:23]:<24}{it['price']:>8.2f}{eq:>9.2f}  "
                  f"{it['payer']:>5} {it['user']:>4}  {it['sentimental']:>4}  {dec_s}")
    elif args.action == "edit":
        for it in db["items"]:
            if it["id"] == args.id:
                if args.to:
                    db["decisions"][it["id"]] = {"action": "manual", "to": args.to,
                                                 "price": equity(it, date.today())}
                if args.note is not None:
                    it["note"] = args.note
                save(dbp, db)
                print(f"{it['id']} updated")
                return
        sys.exit(f"item {args.id} not found")


# ---------- splits ----------

def cmd_split(args, db, dbp):
    if args.action == "list":
        as_of = date.today()
        bundle = {"A": 0.0, "B": 0.0}
        rows = []
        for it in db["items"]:
            dec = db["decisions"].get(it["id"])
            if not dec:
                continue
            eq = equity(it, as_of)
            owner = dec.get("to", dec.get("owner"))
            if owner in bundle:
                bundle[owner] += eq
            rows.append((it["id"], it["name"], eq, dec.get("action"), owner,
                         dec.get("cash", 0.0)))
        for r in rows:
            print(f"{r[0]:<5}{r[1][:23]:<24}{r[2]:>9.2f}  {r[3]:<8} → {r[4] or '?'}  cash {r[5]:.2f}")
        print(f"\nbundle equity: A=${bundle['A']:.2f}  B=${bundle['B']:.2f}  "
              f"Δ=${abs(bundle['A'] - bundle['B']):.2f}")
        return

    as_of = date.today()
    splittable = [it for it in db["items"] if it["sentimental"] == "no"]
    sentimental = [it for it in db["items"] if it["sentimental"] == "yes"]
    if sentimental:
        print("sentimental items EXCLUDED from automation (resolve with `item edit --to`):")
        for it in sentimental:
            print(f"  {it['id']}: {it['name']}")
    if not splittable:
        sys.exit("no splittable items")

    if args.action == "draft":
        rng = random.Random(args.seed)
        first = rng.choice(["A", "B"])
        ranked = sorted(splittable, key=lambda i: equity(i, as_of), reverse=True)
        turn = first
        print(f"coin flip (seed {args.seed}): {first} picks first\n")
        for it in ranked:
            db["decisions"][it["id"]] = {"action": "draft", "to": turn,
                                         "price": equity(it, as_of)}
            print(f"{it['id']:<5}{it['name'][:23]:<24}{equity(it, as_of):>9.2f}  → {turn}")
            turn = "B" if turn == "A" else "A"
        save(dbp, db)
        print("\nrun `split list` for bundle totals")

    elif args.action == "buyout":
        ratio = args.ratio
        for it in splittable:
            eq = equity(it, as_of)
            owner = it["user"] if it["user"] in ("A", "B") else "A"
            share = eq * ratio
            db["decisions"][it["id"]] = {"action": "buyout", "to": owner, "price": eq,
                                         "cash": round(share, 2)}
            print(f"{it['id']:<5}{it['name'][:23]:<24}{eq:>9.2f}  → {owner} "
                  f"(pays other ${share:.2f})")
        save(dbp, db)
        print(f"\nbuyout share = {int(ratio*100)}% of current equity")

    elif args.action == "sellsplit":
        total = sum(equity(it, as_of) for it in splittable)
        ratio = args.ratio
        for it in splittable:
            db["decisions"][it["id"]] = {"action": "sell", "to": None,
                                         "price": equity(it, as_of)}
        save(dbp, db)
        print(f"expected proceeds (depreciated): ${total:.2f}")
        print(f"A receives ${total*(1-ratio):.2f}, B receives ${total*ratio:.2f}")
        print("list items on a marketplace; record actual sale prices with `item edit`")


# ---------- accounts ----------

def cmd_account(args, db, dbp):
    if args.action == "add":
        acc = {
            "id": next_id(db["accounts"], "AC"),
            "name": args.name,
            "type": args.type,
            "owner": args.owner,
            "renews": args.renews,
            "action": args.action_flag or "undecided",
            "cost": args.cost or 0.0,
            "note": args.note or "",
        }
        db["accounts"].append(acc)
        save(dbp, db)
        print(f"added {acc['id']}: {acc['name']} ({acc['type']}, owner={acc['owner']}, "
              f"renews={acc['renews']}, action={acc['action']})")
    elif args.action == "list":
        due_cutoff = date.today() + timedelta(days=args.due)
        und = 0
        for a in db["accounts"]:
            flag = ""
            if a["renews"]:
                rd = parse_date(a["renews"])
                days = (rd - date.today()).days
                if days <= args.due and a["action"] == "undecided":
                    flag = f"  ⚠ RENEWS IN {days}d — NO ACTION DECIDED"
                    und += 1
            print(f"{a['id']:<5}{a['name'][:23]:<24}{a['type']:<14}{a['owner']:>5}  "
                  f"{a['action']:<10} renews={a['renews'] or '—'}{flag}")
        print(f"\n{und} account(s) renewing within {args.due} days with no action" if und
              else f"\nall clear — no undecided renewals within {args.due} days")


# ---------- expenses / settle ----------

def cmd_expense(args, db, dbp):
    if args.action == "add":
        exp = {
            "id": next_id(db["expenses"], "EX"),
            "what": args.what,
            "amount": args.amount,
            "payer": args.payer,
            "shared_with": args.shared_with,
            "date": args.date,
            "share": args.share or "50/50",
        }
        db["expenses"].append(exp)
        save(dbp, db)
        print(f"added {exp['id']}: {exp['what']} ${exp['amount']:.2f} paid by {exp['payer']}")
    elif args.action == "settle":
        owed = {"A": 0.0, "B": 0.0}   # how much each has effectively lent the pair
        for e in db["expenses"]:
            try:
                sa, sb = [float(x) for x in e["share"].split("/")]
            except ValueError:
                sa, sb = 50.0, 50.0
            tot = sa + sb
            payer = e["payer"] if e["payer"] in ("A", "B") else "A"
            other = "B" if payer == "A" else "A"
            frac_other = sb / tot if payer == "A" else sa / tot
            owed[payer] += e["amount"] * frac_other
        net = owed["A"] - owed["B"]
        if abs(net) < 0.01:
            print("settled — no payment needed")
        elif net > 0:
            print(f"B pays A ${net:.2f} — one payment, then this chapter is closed")
        else:
            print(f"A pays B ${-net:.2f} — one payment, then this chapter is closed")
        print(f"(A lent the pair ${owed['A']:.2f}, B lent ${owed['B']:.2f})")


# ---------- moveout ----------

def cmd_moveout(args, db, dbp):
    move = parse_date(args.move_date)
    notice_deadline = move - timedelta(days=args.notice_days)
    plan = {
        "move_date": move.isoformat(),
        "notice_deadline": notice_deadline.isoformat(),
        "steps": [
            (notice_deadline.isoformat(), "give written notice to landlord (keep proof)"),
            ((move - timedelta(days=14)).isoformat(), "schedule movers / van; confirm handoff list"),
            ((move - timedelta(days=7)).isoformat(), "utilities: schedule shutoff/transfer at old address; open at new"),
            ((move - timedelta(days=2)).isoformat(), "deep clean + photo-document condition of unit"),
            (move.isoformat(), "move out; final meter readings (photo); return ALL keys/access devices — get receipt"),
            ((move + timedelta(days=1)).isoformat(), "file mail forwarding (postal + banks + subscriptions)"),
            ((move + timedelta(days=14)).isoformat(), "demand deposit return in writing if not received (itemized deductions only)"),
        ],
    }
    db["moveout"] = plan
    save(dbp, db)
    print(f"MOVE-OUT PLAN (move date {move}, notice {args.notice_days}d)\n")
    for d, step in plan["steps"]:
        late = "  ← ALREADY PAST" if parse_date(d) < date.today() else ""
        print(f"{d}  {step}{late}")


# ---------- report ----------

def cmd_report(args, db, dbp):
    as_of = date.today()
    print("=" * 62)
    print(f"UNTANGLING REPORT — {as_of}")
    print("=" * 62)
    decided = sum(1 for it in db["items"] if it["id"] in db["decisions"])
    print(f"\nITEMS: {decided}/{len(db['items'])} decided")
    bundle = {"A": 0.0, "B": 0.0}
    for it in db["items"]:
        dec = db["decisions"].get(it["id"])
        if dec and dec.get("to") in bundle:
            bundle[dec["to"]] += equity(it, as_of)
    print(f"bundle equity: A=${bundle['A']:.2f}  B=${bundle['B']:.2f}")

    pend = [a for a in db["accounts"] if a["action"] == "undecided"]
    print(f"\nACCOUNTS: {len(db['accounts'])} total, {len(pend)} pending action")
    for a in pend:
        print(f"  {a['id']}: {a['name']} (renews {a['renews'] or '—'})")

    if db["expenses"]:
        owed = {"A": 0.0, "B": 0.0}
        for e in db["expenses"]:
            payer = e["payer"] if e["payer"] in ("A", "B") else "A"
            owed[payer] += e["amount"] / 2
        net = owed["A"] - owed["B"]
        who = "B→A" if net > 0 else "A→B"
        print(f"\nEXPENSES: {len(db['expenses'])} recorded, net settle {who} ${abs(net):.2f}")

    if db["moveout"]:
        print(f"\nMOVE-OUT: {db['moveout']['move_date']} "
              f"(notice deadline {db['moveout']['notice_deadline']})")

    blockers = len(pend) + (len(db["items"]) - decided)
    print(f"\nBLOCKERS TO DONE: {blockers} "
          f"({len(pend)} account actions, {len(db['items']) - decided} item decisions)")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default=DEFAULT_DB)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("item")
    item_sub = p.add_subparsers(dest="action", required=True)
    pi = item_sub.add_parser("add")
    pi.add_argument("name"); pi.add_argument("--price", type=float, required=True)
    pi.add_argument("--date", required=True); pi.add_argument("--payer", default="both",
                   choices=["A", "B", "both"])
    pi.add_argument("--user", default="both"); pi.add_argument("--sentimental", default="no",
                   choices=["yes", "no"])
    pi.add_argument("--note")
    item_sub.add_parser("list")
    pe = item_sub.add_parser("edit")
    pe.add_argument("id"); pe.add_argument("--to", choices=["A", "B"])
    pe.add_argument("--note")

    p = sub.add_parser("split")
    sp = p.add_subparsers(dest="action", required=True)
    sp.add_parser("list")
    pd = sp.add_parser("draft"); pd.add_argument("--seed", type=int, default=None)
    pb = sp.add_parser("buyout"); pb.add_argument("--ratio", type=float, default=0.5)
    ps = sp.add_parser("sellsplit"); ps.add_argument("--ratio", type=float, default=0.5)

    p = sub.add_parser("account")
    acc_sub = p.add_subparsers(dest="action", required=True)
    pa = acc_sub.add_parser("add")
    pa.add_argument("name"); pa.add_argument("--type", default="subscription")
    pa.add_argument("--owner", default="both"); pa.add_argument("--renews")
    pa.add_argument("--action-flag", dest="action_flag",
                   choices=["keep-mine", "transfer", "cancel", "rename", "dispute"])
    pa.add_argument("--cost", type=float); pa.add_argument("--note")
    pl = acc_sub.add_parser("list")
    pl.add_argument("--due", type=int, default=90)

    p = sub.add_parser("expense")
    ex_sub = p.add_subparsers(dest="action", required=True)
    px = ex_sub.add_parser("add")
    px.add_argument("what"); px.add_argument("amount", type=float)
    px.add_argument("--payer", required=True, choices=["A", "B"])
    px.add_argument("--shared-with", dest="shared_with", required=True, choices=["A", "B"])
    px.add_argument("--date", default=date.today().isoformat())
    px.add_argument("--share", help="e.g. 50/50 or 60/40")
    ex_sub.add_parser("settle")

    p = sub.add_parser("moveout")
    p.add_argument("--move-date", dest="move_date", required=True)
    p.add_argument("--notice-days", dest="notice_days", type=int, default=30)

    sub.add_parser("report")

    args = ap.parse_args()
    dbp = Path(args.db)
    db = load(dbp)

    if args.cmd == "item":
        cmd_item(args, db, dbp)
    elif args.cmd == "split":
        cmd_split(args, db, dbp)
    elif args.cmd == "account":
        cmd_account(args, db, dbp)
    elif args.cmd == "expense":
        cmd_expense(args, db, dbp)
    elif args.cmd == "moveout":
        cmd_moveout(args, db, dbp)
    elif args.cmd == "report":
        cmd_report(args, db, dbp)


if __name__ == "__main__":
    main()
