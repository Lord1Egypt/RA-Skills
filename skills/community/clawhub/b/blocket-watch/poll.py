#!/usr/bin/env python3
"""
Blocket poll: runs blocket CLI, dedupes by ad id, notifies via openclaw message send only.
Does not call an LLM.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
CONFIG_PATH = DIR / "config.json"
SEEN_PATH = DIR / "seen.json"


def load(p: Path) -> dict:
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def save(p: Path, data: dict) -> None:
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(p)


def row_passes_max_price(q: dict, row: dict) -> bool:
    """
    If the query sets max_price, only accept rows at or below that price in max_price_currency.
    Omit max_price to allow any price (previous behaviour).
    """
    raw_max = q.get("max_price")
    if raw_max is None:
        return True
    try:
        cap = float(raw_max)
    except (TypeError, ValueError):
        return True
    want_cur = (q.get("max_price_currency") or "SEK").strip().upper()
    rp = row.get("price")
    if rp is None:
        return False
    try:
        price = float(rp)
    except (TypeError, ValueError):
        return False
    cur = row.get("currency") or "SEK"
    if isinstance(cur, str):
        cur = cur.strip().upper()
    else:
        cur = "SEK"
    if cur != want_cur:
        return False
    return price <= cap


def run_blocket(argv: list[str]) -> dict:
    cmd = ["blocket", *argv]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"blocket failed: {' '.join(cmd)}\n{r.stderr or r.stdout}")
    if not r.stdout.strip():
        return {"total": 0, "results": []}
    return json.loads(r.stdout)


def notify_telegram(target: str, body: str, dry_run: bool) -> None:
    if dry_run:
        print("[dry-run] message send skipped:\n", body[:500], "...", sep="")
        return
    cmd = [
        "openclaw",
        "message",
        "send",
        "--channel",
        "telegram",
        "--target",
        target,
        "--message",
        body,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        print(r.stderr or r.stdout, file=sys.stderr)
        raise RuntimeError("openclaw message send failed")


def main() -> int:
    dry = os.environ.get("BLOCKET_WATCH_DRY_RUN", "").lower() in ("1", "true", "yes")
    config = load(CONFIG_PATH)
    seen_data = load(SEEN_PATH)
    seen: set[str] = set(seen_data.get("ids") or [])

    if not config.get("enabled", False):
        print(
            "blocket-watch: disabled in config.json (set enabled true after setup).",
            file=sys.stderr,
        )
        return 0

    queries = config.get("queries") or []
    if not queries:
        print(
            "blocket-watch: no queries configured; add queries in config.json.",
            file=sys.stderr,
        )
        return 0

    target = str(config.get("telegram_target") or "").strip()
    if not target:
        print("blocket-watch: missing telegram_target in config.json.", file=sys.stderr)
        return 1

    new_items: list[dict] = []
    skipped_price = 0
    for q in queries:
        argv = q.get("argv")
        if not isinstance(argv, list) or not all(isinstance(x, str) for x in argv):
            print(f"blocket-watch: bad query entry (need argv list of strings): {q!r}", file=sys.stderr)
            continue
        label = q.get("label") or " ".join(argv[:3])
        data = run_blocket(argv)
        for row in data.get("results") or []:
            rid = str(row.get("id") or "")
            if not rid or rid in seen:
                continue
            seen.add(rid)
            if not row_passes_max_price(q, row):
                skipped_price += 1
                continue
            row["_query_label"] = label
            new_items.append(row)

    if skipped_price:
        print(f"blocket-watch: skipped {skipped_price} listing(s) above max_price (still marked seen).")

    if not new_items:
        print("blocket-watch: no new listings.")
        return 0

    lines = ["Blocket — new listings (automated)", ""]
    for row in new_items[:30]:
        h = row.get("heading") or "?"
        price = row.get("price")
        loc = row.get("location") or ""
        url = row.get("url") or ""
        lbl = row.get("_query_label", "")
        price_s = f"{price} {row.get('currency') or 'SEK'}" if price is not None else "—"
        lines.append(f"• {h}")
        lines.append(f"  {price_s} · {loc} · {lbl}")
        if url:
            lines.append(f"  {url}")
        lines.append("")

    if len(new_items) > 30:
        lines.append(f"(+{len(new_items) - 30} more new ids tracked; increase limit in script if needed)")

    body = "\n".join(lines).strip()
    if not dry:
        save(SEEN_PATH, {"ids": sorted(seen, key=lambda x: int(x) if x.isdigit() else 0)})
    notify_telegram(target, body, dry)
    print(f"blocket-watch: notified {len(new_items)} new listing(s).")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"blocket-watch: error: {e}", file=sys.stderr)
        sys.exit(1)
