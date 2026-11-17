#!/usr/bin/env python3
"""founder-ledger: a one-file income ledger and milestone registry for
solo founders tracking their way to their first $1,000.

No dependencies beyond the Python 3 standard library. Copy this one file
anywhere and run it.

    python3 founder_ledger.py add 25.00 "First Gumroad sale" --source gumroad
    python3 founder_ledger.py status
    python3 founder_ledger.py list
    python3 founder_ledger.py undo

Data lives in a single JSON file next to your data (default ./ledger.json,
override with --file or the LEDGER_FILE environment variable).

Design notes:
  * Money is stored and computed with Decimal, never float, so cents never
    drift.
  * The ledger is an append-only list of entries. `undo` removes the most
    recent entry (for fixing typos), but it never rewrites history for any
    entry that isn't the last one.
  * The milestone registry is derived from the ledger, but once a milestone
    is first crossed, its record (amount, date, description, entry index)
    is frozen permanently in the registry -- an `undo` that later drops the
    running total back below a milestone does not un-ring that bell. Your
    first dollar stays your first dollar even if you later refund it.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

MILESTONES_USD = [Decimal(x) for x in ("1", "10", "50", "100", "250", "500", "1000")]


class LedgerError(RuntimeError):
    pass


@dataclass
class Entry:
    amount: Decimal
    description: str
    date: str
    source: str = ""

    def to_json(self) -> dict:
        return {
            "amount": str(self.amount),
            "description": self.description,
            "date": self.date,
            "source": self.source,
        }

    @staticmethod
    def from_json(d: dict) -> "Entry":
        return Entry(
            amount=Decimal(d["amount"]),
            description=d["description"],
            date=d["date"],
            source=d.get("source", ""),
        )


@dataclass
class Milestone:
    threshold: Decimal
    reached_date: str
    entry_index: int
    running_total: Decimal

    def to_json(self) -> dict:
        return {
            "threshold": str(self.threshold),
            "reached_date": self.reached_date,
            "entry_index": self.entry_index,
            "running_total": str(self.running_total),
        }

    @staticmethod
    def from_json(d: dict) -> "Milestone":
        return Milestone(
            threshold=Decimal(d["threshold"]),
            reached_date=d["reached_date"],
            entry_index=d["entry_index"],
            running_total=Decimal(d["running_total"]),
        )


@dataclass
class Ledger:
    entries: list[Entry] = field(default_factory=list)
    milestones: list[Milestone] = field(default_factory=list)

    def total(self) -> Decimal:
        return sum((e.amount for e in self.entries), Decimal("0"))

    def milestone_thresholds_reached(self) -> set[Decimal]:
        return {m.threshold for m in self.milestones}

    def add(self, amount: Decimal, description: str, entry_date: str, source: str = "") -> Entry:
        entry = Entry(amount=amount, description=description, date=entry_date, source=source)
        self.entries.append(entry)
        self._update_registry()
        return entry

    def undo(self) -> Entry:
        if not self.entries:
            raise LedgerError("ledger is empty; nothing to undo")
        return self.entries.pop()

    def _update_registry(self) -> None:
        already = self.milestone_thresholds_reached()
        running = Decimal("0")
        for idx, e in enumerate(self.entries):
            running += e.amount
            for threshold in MILESTONES_USD:
                if threshold in already:
                    continue
                if running >= threshold:
                    self.milestones.append(
                        Milestone(
                            threshold=threshold,
                            reached_date=e.date,
                            entry_index=idx,
                            running_total=running,
                        )
                    )
                    already.add(threshold)

    def to_json(self) -> dict:
        return {
            "version": 1,
            "entries": [e.to_json() for e in self.entries],
            "milestones": [m.to_json() for m in self.milestones],
        }

    @staticmethod
    def from_json(d: dict) -> "Ledger":
        return Ledger(
            entries=[Entry.from_json(e) for e in d.get("entries", [])],
            milestones=[Milestone.from_json(m) for m in d.get("milestones", [])],
        )


def load(path: Path) -> Ledger:
    if not path.exists():
        return Ledger()
    try:
        return Ledger.from_json(json.loads(path.read_text()))
    except (json.JSONDecodeError, KeyError, InvalidOperation) as e:
        raise LedgerError(f"could not read {path}: {e}") from e


def save(path: Path, ledger: Ledger) -> None:
    path.write_text(json.dumps(ledger.to_json(), indent=2) + "\n")


def parse_amount(raw: str) -> Decimal:
    try:
        amount = Decimal(raw)
    except InvalidOperation:
        raise LedgerError(f"'{raw}' is not a valid dollar amount") from None
    return amount.quantize(Decimal("0.01"))


def resolve_path(args_file: str | None) -> Path:
    return Path(args_file or os.environ.get("LEDGER_FILE", "ledger.json"))


def progress_bar(total: Decimal, goal: Decimal = Decimal("1000"), width: int = 30) -> str:
    fraction = min(total / goal, Decimal("1")) if goal else Decimal("1")
    filled = int(fraction * width)
    return "[" + "#" * filled + "-" * (width - filled) + f"] {fraction * 100:.1f}%"


def cmd_add(args: argparse.Namespace) -> int:
    path = resolve_path(args.file)
    ledger = load(path)
    amount = parse_amount(args.amount)
    entry_date = args.date or date.today().isoformat()
    before = ledger.total()
    ledger.add(amount, args.description, entry_date, args.source or "")
    save(path, ledger)
    after = ledger.total()
    print(f"added {amount} on {entry_date} -- {args.description}")
    print(f"total: {before} -> {after}")
    newly = [m for m in ledger.milestones if m.entry_index == len(ledger.entries) - 1]
    for m in newly:
        print(f"milestone reached: ${m.threshold} (on {m.reached_date})")
    return 0


def cmd_undo(args: argparse.Namespace) -> int:
    path = resolve_path(args.file)
    ledger = load(path)
    try:
        removed = ledger.undo()
    except LedgerError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    save(path, ledger)
    print(f"removed: {removed.amount} on {removed.date} -- {removed.description}")
    print("note: any milestone already reached stays recorded in the registry.")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    path = resolve_path(args.file)
    ledger = load(path)
    if args.json:
        print(json.dumps(ledger.to_json(), indent=2))
        return 0
    if not ledger.entries:
        print("(no entries yet)")
        return 0
    running = Decimal("0")
    for idx, e in enumerate(ledger.entries):
        running += e.amount
        source = f" [{e.source}]" if e.source else ""
        print(f"{idx:>3}  {e.date}  {e.amount:>10}  running={running:>10}  {e.description}{source}")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    path = resolve_path(args.file)
    ledger = load(path)
    total = ledger.total()
    if args.json:
        print(json.dumps({
            "total": str(total),
            "entry_count": len(ledger.entries),
            "milestones": [m.to_json() for m in ledger.milestones],
            "next_milestone": next(
                (str(t) for t in MILESTONES_USD if t not in ledger.milestone_thresholds_reached()),
                None,
            ),
        }, indent=2))
        return 0
    print(f"total revenue: ${total}")
    print(f"entries: {len(ledger.entries)}")
    print(progress_bar(total))
    reached = ledger.milestone_thresholds_reached()
    print()
    print("milestone registry:")
    for threshold in MILESTONES_USD:
        if threshold in reached:
            m = next(m for m in ledger.milestones if m.threshold == threshold)
            print(f"  [x] ${threshold:<8} reached {m.reached_date}")
        else:
            print(f"  [ ] ${threshold:<8} not yet")
    if total >= Decimal("1000"):
        print()
        print("You've tracked your first $1,000. That's the goal this tool was built for.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="founder_ledger.py",
        description="A one-file income ledger and milestone registry for your first $1,000.",
    )
    p.add_argument("--file", help="path to the ledger JSON file (default: ./ledger.json or $LEDGER_FILE)")
    sub = p.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="record a new income entry")
    add.add_argument("amount", help="dollar amount, e.g. 25.00")
    add.add_argument("description", help="what this was for")
    add.add_argument("--date", help="ISO date, default today")
    add.add_argument("--source", help="where it came from, e.g. stripe, gumroad, cash")
    add.set_defaults(func=cmd_add)

    undo = sub.add_parser("undo", help="remove the most recent entry")
    undo.set_defaults(func=cmd_undo)

    lst = sub.add_parser("list", help="list all entries with a running total")
    lst.add_argument("--json", action="store_true", help="output raw JSON")
    lst.set_defaults(func=cmd_list)

    status = sub.add_parser("status", help="show total, progress bar, and milestone registry")
    status.add_argument("--json", action="store_true", help="output raw JSON")
    status.set_defaults(func=cmd_status)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except LedgerError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
