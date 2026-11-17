#!/usr/bin/env python3
"""
ledger.py -- FairSplit group expense ledger and debt-settlement engine.

Stdlib only (json, argparse, decimal, heapq, csv, urllib). No accounts,
no API keys, no network required for the core workflow. One JSON file
per group on disk; every command is a single deterministic operation
so an agent (or a human) can call it directly from a shell.

All money is stored internally as integer *minor units* (cents / paise /
etc. -- i.e. amount * 10**2) to avoid floating point drift. Decimal is
used only to parse user-supplied strings safely.

Run `ledger.py <command> --help` for per-command options.
"""

import argparse
import csv
import heapq
import json
import os
import sys
import time
import urllib.request
import urllib.error
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

SCALE = Decimal("0.01")  # 2 decimal places for internal storage


# --------------------------------------------------------------------------
# Storage helpers
# --------------------------------------------------------------------------

def default_data_dir():
    return os.environ.get(
        "FAIRSPLIT_DATA_DIR",
        os.path.expanduser("~/.hermes/data/fairsplit"),
    )


def slugify(name):
    slug = "".join(c.lower() if c.isalnum() else "-" for c in name.strip())
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-") or "group"


def group_path(data_dir, group):
    return os.path.join(data_dir, f"{slugify(group)}.json")


def load_group(data_dir, group, required=True):
    path = group_path(data_dir, group)
    if not os.path.exists(path):
        if required:
            die(f"No group called '{group}' at {path}. "
                f"Run 'init' first, e.g.:\n"
                f"  ledger.py init --group \"{group}\" --currency USD --members \"Alice,Bob\"")
        return None
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def save_group(data_dir, group, state):
    os.makedirs(data_dir, exist_ok=True)
    path = group_path(data_dir, group)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2, sort_keys=False)
    os.replace(tmp, path)
    return path


def die(msg, code=1):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


# --------------------------------------------------------------------------
# Money helpers (integer minor units throughout)
# --------------------------------------------------------------------------

def parse_decimal(value, what="amount"):
    """Parse a user-supplied string into a finite Decimal, or exit cleanly."""
    try:
        d = Decimal(str(value).strip())
    except InvalidOperation:
        die(f"'{value}' is not a valid {what}")
    if not d.is_finite():
        die(f"'{value}' is not a valid {what}")
    return d


def to_minor(amount_str):
    """Parse a decimal amount string into integer minor units (cents)."""
    d = parse_decimal(amount_str)
    minor = (d * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return int(minor)


def from_minor(minor):
    return str((Decimal(minor) / 100).quantize(SCALE))


def distribute_remainder(base_shares, remainder, order):
    """Hand out `remainder` extra minor units (can be negative), one at a
    time, to participants in `order` (deterministic, e.g. sorted by name),
    wrapping around if remainder's absolute value exceeds len(order)."""
    if remainder == 0 or not order:
        return base_shares
    step = 1 if remainder > 0 else -1
    n = abs(remainder)
    i = 0
    while n > 0:
        who = order[i % len(order)]
        base_shares[who] += step
        i += 1
        n -= 1
    return base_shares


def compute_shares(total_minor, participants, split_type, split_detail):
    """Return {participant: minor_units_owed}, summing exactly to total_minor."""
    participants = list(dict.fromkeys(participants))  # de-dupe, keep order
    if not participants:
        die("an expense needs at least one participant")
    order = sorted(participants)  # deterministic remainder order

    if split_type == "equal":
        base = total_minor // len(participants)
        shares = {p: base for p in participants}
        remainder = total_minor - base * len(participants)
        return distribute_remainder(shares, remainder, order)

    if split_type == "exact":
        shares = {}
        for p in participants:
            if p not in split_detail:
                die(f"exact split is missing an amount for '{p}'")
            shares[p] = to_minor(split_detail[p])
        total_given = sum(shares.values())
        if total_given != total_minor:
            die(f"exact amounts sum to {from_minor(total_given)} but the "
                f"expense total is {from_minor(total_minor)}")
        return shares

    if split_type in ("shares", "percent"):
        weights = {}
        for p in participants:
            if p not in split_detail:
                die(f"{split_type} split is missing a weight for '{p}'")
            weights[p] = parse_decimal(split_detail[p], what="weight")
            if weights[p] < 0:
                die(f"{split_type} weight for '{p}' cannot be negative")
        weight_sum = sum(weights.values())
        if weight_sum <= 0:
            die("weights must sum to more than zero")
        shares = {}
        running = 0
        for idx, p in enumerate(participants):
            if idx < len(participants) - 1:
                amt = int((Decimal(total_minor) * weights[p] / weight_sum)
                          .quantize(Decimal("1"), rounding=ROUND_HALF_UP))
                shares[p] = amt
                running += amt
            else:
                # last participant absorbs the rounding remainder directly
                shares[p] = total_minor - running
        return shares

    die(f"unknown split type '{split_type}' (use equal, exact, shares, or percent)")


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------

def cmd_init(args):
    data_dir = args.data_dir
    path = group_path(data_dir, args.group)
    if os.path.exists(path) and not args.force:
        die(f"group '{args.group}' already exists at {path} (use --force to reset)")
    members = [m.strip() for m in args.members.split(",") if m.strip()] if args.members else []
    state = {
        "group": args.group,
        "currency": args.currency.upper(),
        "members": members,
        "expenses": [],
        "next_id": 1,
        "created_at": now_iso(),
    }
    save_group(data_dir, args.group, state)
    print(f"Created group '{args.group}' ({state['currency']}) with members: "
          f"{', '.join(members) if members else '(none yet -- add with add-member)'}")
    print(f"Ledger file: {group_path(data_dir, args.group)}")


def cmd_add_member(args):
    state = load_group(args.data_dir, args.group)
    if args.member not in state["members"]:
        state["members"].append(args.member)
        save_group(args.data_dir, args.group, state)
    print(f"Members of '{args.group}': {', '.join(state['members'])}")


def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def cmd_add(args):
    state = load_group(args.data_dir, args.group)
    home_currency = state["currency"]
    expense_currency = (args.currency or home_currency).upper()

    original_minor = to_minor(args.amount)
    if original_minor <= 0:
        die(f"amount must be greater than zero (got '{args.amount}'); "
            f"to reverse an expense use 'undo'")
    fx_rate = None
    amount_minor = original_minor

    if expense_currency != home_currency:
        if args.fx_rate is None:
            die(f"expense is in {expense_currency} but group currency is "
                f"{home_currency}; pass --fx-rate (units of {home_currency} "
                f"per 1 {expense_currency}), or fetch one with the 'fx' command")
        fx_rate = parse_decimal(args.fx_rate, what="fx rate")
        if fx_rate <= 0:
            die("--fx-rate must be greater than zero")
        amount_minor = int((Decimal(original_minor) * fx_rate)
                            .quantize(Decimal("1"), rounding=ROUND_HALF_UP))

    participants = [p.strip() for p in args.participants.split(",") if p.strip()] \
        if args.participants else list(state["members"])
    if not participants:
        die("no participants given and the group has no members yet")

    for p in [args.payer] + participants:
        if p not in state["members"]:
            state["members"].append(p)

    split_detail = {}
    if args.split in ("exact", "shares", "percent"):
        if not args.detail:
            die(f"--detail is required for split type '{args.split}', e.g. "
                f"--detail \"Alice:2,Bob:1\"")
        for pair in args.detail.split(","):
            k, _, v = pair.partition(":")
            split_detail[k.strip()] = v.strip()

    shares_minor = compute_shares(amount_minor, participants, args.split, split_detail)

    expense = {
        "id": f"e{state['next_id']}",
        "date": args.date or time.strftime("%Y-%m-%d"),
        "payer": args.payer,
        "description": args.description or "(no description)",
        "category": args.category or "general",
        "amount_minor": amount_minor,
        "currency": home_currency,
        "original_amount_minor": original_minor,
        "original_currency": expense_currency,
        "fx_rate": str(fx_rate) if fx_rate else None,
        "participants": participants,
        "split_type": args.split,
        "split_detail": split_detail or None,
        "shares_minor": shares_minor,
        "created_at": now_iso(),
    }
    state["next_id"] += 1
    state["expenses"].append(expense)
    save_group(args.data_dir, args.group, state)

    print(f"Added {expense['id']}: {args.payer} paid {from_minor(amount_minor)} "
          f"{home_currency} for \"{expense['description']}\", "
          f"split {args.split} across {', '.join(participants)}")
    if fx_rate:
        print(f"  (converted from {from_minor(original_minor)} {expense_currency} "
              f"at rate {fx_rate})")
    for p, m in sorted(shares_minor.items()):
        print(f"  {p}: owes {from_minor(m)} {home_currency}")


def cmd_undo(args):
    state = load_group(args.data_dir, args.group)
    before = len(state["expenses"])
    state["expenses"] = [e for e in state["expenses"] if e["id"] != args.id]
    if len(state["expenses"]) == before:
        die(f"no expense with id '{args.id}' in group '{args.group}'")
    save_group(args.data_dir, args.group, state)
    print(f"Removed {args.id} from '{args.group}'")


def compute_balances(state):
    """Return {person: net_minor}. Positive = owed money. Negative = owes money."""
    net = {m: 0 for m in state["members"]}
    for e in state["expenses"]:
        net[e["payer"]] = net.get(e["payer"], 0) + e["amount_minor"]
        for p, m in e["shares_minor"].items():
            net[p] = net.get(p, 0) - m
    return net


def cmd_balances(args):
    state = load_group(args.data_dir, args.group)
    net = compute_balances(state)
    currency = state["currency"]
    print(f"Balances for '{args.group}' ({currency}):")
    for p in sorted(net):
        amt = net[p]
        if amt > 0:
            print(f"  {p}: is owed {from_minor(amt)}")
        elif amt < 0:
            print(f"  {p}: owes {from_minor(-amt)}")
        else:
            print(f"  {p}: settled up")
    total_drift = sum(net.values())
    if total_drift != 0:
        # Should only ever be nonzero from a corrupted/hand-edited file.
        print(f"  warning: balances do not sum to zero (drift = "
              f"{from_minor(total_drift)}) -- check for a hand-edited ledger file",
              file=sys.stderr)


def cmd_settle(args):
    state = load_group(args.data_dir, args.group)
    net = compute_balances(state)
    currency = state["currency"]

    # Min-heap of negated amounts == max-heap by amount. Creditors are
    # popped largest-owed-to first; debtors popped largest-owed first
    # (their net is already negative, so a plain min-heap does that).
    creditors = [(-amt, p) for p, amt in net.items() if amt > 0]
    debtor_heap = [(amt, p) for p, amt in net.items() if amt < 0]
    heapq.heapify(creditors)
    heapq.heapify(debtor_heap)

    transactions = []
    while creditors and debtor_heap:
        neg_credit, creditor = heapq.heappop(creditors)
        credit_amt = -neg_credit
        debt_amt_neg, debtor = heapq.heappop(debtor_heap)
        debt_amt = -debt_amt_neg  # positive amount this person owes

        pay = min(credit_amt, debt_amt)
        if pay > 0:
            transactions.append((debtor, creditor, pay))

        credit_amt -= pay
        debt_amt -= pay
        if credit_amt > 0:
            heapq.heappush(creditors, (-credit_amt, creditor))
        if debt_amt > 0:
            heapq.heappush(debtor_heap, (-debt_amt, debtor))

    if not transactions:
        print(f"'{args.group}' is fully settled -- nobody owes anybody anything.")
        return

    print(f"Settlement plan for '{args.group}' ({len(transactions)} payment"
          f"{'s' if len(transactions) != 1 else ''}):")
    for debtor, creditor, amt in transactions:
        print(f"  {debtor} pays {creditor}: {from_minor(amt)} {currency}")


def cmd_history(args):
    state = load_group(args.data_dir, args.group)
    rows = state["expenses"]
    if args.person:
        rows = [e for e in rows if args.person in e["participants"] or e["payer"] == args.person]
    if args.category:
        rows = [e for e in rows if e["category"] == args.category]
    rows = sorted(rows, key=lambda e: (e["date"], e["id"]))
    if args.limit:
        rows = rows[-args.limit:]
    if not rows:
        print("No matching expenses.")
        return
    for e in rows:
        tag = f" [{e['original_currency']}]" if e["original_currency"] != state["currency"] else ""
        print(f"{e['id']}  {e['date']}  {e['payer']:<12} paid "
              f"{from_minor(e['amount_minor']):>10} {state['currency']}{tag}  "
              f"{e['description']}  ({e['split_type']}: {', '.join(e['participants'])})")


def cmd_export(args):
    state = load_group(args.data_dir, args.group)
    if args.format == "csv":
        out_path = args.out or f"{slugify(args.group)}-expenses.csv"
        with open(out_path, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["id", "date", "payer", "amount", "currency", "description",
                        "category", "participants", "split_type"])
            for e in sorted(state["expenses"], key=lambda e: e["date"]):
                w.writerow([e["id"], e["date"], e["payer"], from_minor(e["amount_minor"]),
                            state["currency"], e["description"], e["category"],
                            "|".join(e["participants"]), e["split_type"]])
        print(f"Wrote {out_path}")
    elif args.format == "md":
        out_path = args.out or f"{slugify(args.group)}-summary.md"
        net = compute_balances(state)
        lines = [f"# {args.group} -- expense summary ({state['currency']})", ""]
        lines.append("## Expenses")
        lines.append("")
        lines.append("| Date | Payer | Amount | Description | Split |")
        lines.append("|---|---|---|---|---|")
        for e in sorted(state["expenses"], key=lambda e: e["date"]):
            lines.append(f"| {e['date']} | {e['payer']} | {from_minor(e['amount_minor'])} "
                         f"| {e['description']} | {e['split_type']} ({', '.join(e['participants'])}) |")
        lines.append("")
        lines.append("## Balances")
        lines.append("")
        for p in sorted(net):
            amt = net[p]
            state_str = "settled up" if amt == 0 else (
                f"is owed {from_minor(amt)}" if amt > 0 else f"owes {from_minor(-amt)}")
            lines.append(f"- **{p}**: {state_str}")
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        print(f"Wrote {out_path}")
    else:
        die("format must be 'csv' or 'md'")


def cmd_list_groups(args):
    data_dir = args.data_dir
    if not os.path.isdir(data_dir):
        print("No groups yet.")
        return
    found = False
    for fname in sorted(os.listdir(data_dir)):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(data_dir, fname), encoding="utf-8") as fh:
            state = json.load(fh)
        net = compute_balances(state)
        unsettled = sum(1 for v in net.values() if v != 0)
        print(f"- {state['group']} ({state['currency']}, "
              f"{len(state['expenses'])} expenses, "
              f"{unsettled} member{'s' if unsettled != 1 else ''} unsettled)")
        found = True
    if not found:
        print("No groups yet.")


def cmd_fx(args):
    """Best-effort keyless FX lookup via Frankfurter (ECB rates). Optional --
    the rest of the skill works fine with a manually supplied --fx-rate."""
    base, quote = args.base.strip().upper(), args.quote.strip().upper()
    for code in (base, quote):
        if len(code) != 3 or not code.isalpha():
            die(f"'{code}' is not an ISO 4217 currency code (e.g. USD, EUR, INR)")
    urls = [
        f"https://api.frankfurter.dev/v1/latest?base={base}&symbols={quote}",
        f"https://api.frankfurter.app/latest?from={base}&to={quote}",
    ]
    last_err = None
    for url in urls:
        try:
            with urllib.request.urlopen(url, timeout=6) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            rate = data["rates"][quote]
            print(f"1 {base} = {rate} {quote}  (source: {url})")
            return
        except Exception as exc:  # noqa: BLE001 -- best-effort, fall through
            last_err = exc
            continue
    die(f"could not fetch a live rate ({last_err}); supply --fx-rate manually to 'add' instead")


# --------------------------------------------------------------------------
# CLI wiring
# --------------------------------------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(prog="ledger.py", description=__doc__.strip().splitlines()[0])
    p.add_argument("--data-dir", default=default_data_dir(),
                    help="directory holding group ledger files (default: %(default)s)")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("init", help="create a new group ledger")
    s.add_argument("--group", required=True)
    s.add_argument("--currency", default="USD")
    s.add_argument("--members", help="comma-separated names, e.g. \"Alice,Bob,Priya\"")
    s.add_argument("--force", action="store_true", help="overwrite an existing group")
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("add-member", help="add a member to an existing group")
    s.add_argument("--group", required=True)
    s.add_argument("--member", required=True)
    s.set_defaults(func=cmd_add_member)

    s = sub.add_parser("add", help="record an expense")
    s.add_argument("--group", required=True)
    s.add_argument("--payer", required=True)
    s.add_argument("--amount", required=True, help="e.g. 1200.50")
    s.add_argument("--currency", help="defaults to the group's home currency")
    s.add_argument("--fx-rate",
                    help="home-currency units per 1 expense-currency unit, required if --currency differs")
    s.add_argument("--description", default="")
    s.add_argument("--category", default="general")
    s.add_argument("--date", help="YYYY-MM-DD, defaults to today")
    s.add_argument("--participants", help="comma-separated names; defaults to all group members")
    s.add_argument("--split", choices=["equal", "exact", "shares", "percent"], default="equal")
    s.add_argument("--detail", help="required for exact/shares/percent, e.g. \"Alice:2,Bob:1\"")
    s.set_defaults(func=cmd_add)

    s = sub.add_parser("undo", help="delete an expense by id")
    s.add_argument("--group", required=True)
    s.add_argument("--id", required=True)
    s.set_defaults(func=cmd_undo)

    s = sub.add_parser("balances", help="show each member's net balance")
    s.add_argument("--group", required=True)
    s.set_defaults(func=cmd_balances)

    s = sub.add_parser("settle", help="compute the minimum-payment settlement plan")
    s.add_argument("--group", required=True)
    s.set_defaults(func=cmd_settle)

    s = sub.add_parser("history", help="list recorded expenses")
    s.add_argument("--group", required=True)
    s.add_argument("--person")
    s.add_argument("--category")
    s.add_argument("--limit", type=int)
    s.set_defaults(func=cmd_history)

    s = sub.add_parser("export", help="write a CSV or Markdown summary to disk")
    s.add_argument("--group", required=True)
    s.add_argument("--format", choices=["csv", "md"], default="md")
    s.add_argument("--out")
    s.set_defaults(func=cmd_export)

    s = sub.add_parser("list-groups", help="list all groups in the data directory")
    s.set_defaults(func=cmd_list_groups)

    s = sub.add_parser("fx", help="best-effort keyless FX rate lookup (Frankfurter/ECB)")
    s.add_argument("--base", required=True)
    s.add_argument("--quote", required=True)
    s.set_defaults(func=cmd_fx)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    # The configured fairsplit.data_dir defaults to "~/..."; expand it here so
    # a quoted path from the agent doesn't create a literal "~" directory.
    args.data_dir = os.path.expandvars(os.path.expanduser(args.data_dir))
    args.func(args)


if __name__ == "__main__":
    main()
