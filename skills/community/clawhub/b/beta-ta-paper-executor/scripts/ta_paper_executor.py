#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
from typing import Dict, List


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def default_ledger() -> str:
    return os.path.expanduser("~/.openclaw/workspace-papertrader/journal/paper-orders.jsonl")


def ensure_dir(path: str):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)


def read_ledger(path: str) -> List[Dict]:
    if not os.path.exists(path):
        return []
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def append_line(path: str, payload: Dict):
    ensure_dir(path)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=True) + "\n")


def order_id(existing_events: int) -> str:
    stamp = dt.datetime.now().strftime("%Y%m%d")
    seq = str(existing_events + 1).zfill(3)
    return f"ORD-{stamp}-{seq}"


def current_open_positions(events: List[Dict]) -> Dict[str, Dict]:
    open_pos = {}
    for e in events:
        oid = e["id"]
        if e["event"] == "OPEN":
            open_pos[oid] = e
        elif e["event"] == "CLOSE" and oid in open_pos:
            del open_pos[oid]
    return open_pos


def place(args):
    events = read_ledger(args.ledger)
    oid = order_id(len(events))
    ev = {
        "ts": now_iso(),
        "event": "OPEN",
        "id": oid,
        "symbol": args.symbol,
        "side": args.side,
        "entry": args.entry,
        "stop": args.stop,
        "target": args.target,
        "qty": args.qty,
        "strategy": args.strategy,
        "reason": args.reason,
        "status": "OPEN",
    }
    append_line(args.ledger, ev)
    print(json.dumps(ev, ensure_ascii=True, indent=2) if args.json else f"Placed {oid}")


def close(args):
    events = read_ledger(args.ledger)
    open_pos = current_open_positions(events)
    if args.id not in open_pos:
        raise SystemExit(f"Open order not found: {args.id}")

    p = open_pos[args.id]
    side = p["side"]
    qty = float(p["qty"])
    entry = float(p["entry"])
    exit_px = float(args.exit)
    pnl = (exit_px - entry) * qty if side == "long" else (entry - exit_px) * qty

    ev = {
        "ts": now_iso(),
        "event": "CLOSE",
        "id": args.id,
        "symbol": p["symbol"],
        "side": side,
        "entry": entry,
        "exit": exit_px,
        "qty": qty,
        "pnl": round(pnl, 6),
        "close_reason": args.close_reason,
        "status": "CLOSED",
    }
    append_line(args.ledger, ev)
    print(json.dumps(ev, ensure_ascii=True, indent=2) if args.json else f"Closed {args.id} pnl={ev['pnl']}")


def status(args):
    events = read_ledger(args.ledger)
    open_pos = current_open_positions(events)

    lines = []
    total_unreal = 0.0
    for oid, p in open_pos.items():
        if args.symbol and p["symbol"] != args.symbol:
            continue
        mark = args.mark
        unreal = None
        if mark is not None:
            unreal = (mark - p["entry"]) * p["qty"] if p["side"] == "long" else (p["entry"] - mark) * p["qty"]
            total_unreal += unreal
        lines.append(
            {
                "id": oid,
                "symbol": p["symbol"],
                "side": p["side"],
                "entry": p["entry"],
                "stop": p["stop"],
                "target": p["target"],
                "qty": p["qty"],
                "strategy": p["strategy"],
                "unrealized": None if unreal is None else round(unreal, 6),
            }
        )

    out = {
        "ledger": args.ledger,
        "open_count": len(lines),
        "positions": lines,
        "total_unrealized": None if args.mark is None else round(total_unreal, 6),
    }

    if args.json:
        print(json.dumps(out, ensure_ascii=True, indent=2))
    else:
        print(f"open_count={out['open_count']}")
        for p in lines:
            print(p)
        if args.mark is not None:
            print(f"total_unrealized={out['total_unrealized']}")


def main():
    ap = argparse.ArgumentParser(description="Paper execution ledger for TA strategies")
    ap.add_argument("--ledger", default=default_ledger())
    ap.add_argument("--json", action="store_true")

    sp = ap.add_subparsers(dest="cmd", required=True)

    p1 = sp.add_parser("place")
    p1.add_argument("--symbol", required=True)
    p1.add_argument("--side", choices=["long", "short"], required=True)
    p1.add_argument("--entry", type=float, required=True)
    p1.add_argument("--stop", type=float, required=True)
    p1.add_argument("--target", type=float, required=True)
    p1.add_argument("--qty", type=float, required=True)
    p1.add_argument("--strategy", default="ta")
    p1.add_argument("--reason", default="")

    p2 = sp.add_parser("close")
    p2.add_argument("--id", required=True)
    p2.add_argument("--exit", type=float, required=True)
    p2.add_argument("--close-reason", default="manual")

    p3 = sp.add_parser("status")
    p3.add_argument("--symbol")
    p3.add_argument("--mark", type=float)

    args = ap.parse_args()

    if args.cmd == "place":
        place(args)
    elif args.cmd == "close":
        close(args)
    elif args.cmd == "status":
        status(args)


if __name__ == "__main__":
    main()
