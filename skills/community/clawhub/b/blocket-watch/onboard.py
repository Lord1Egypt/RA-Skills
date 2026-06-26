#!/usr/bin/env python3
"""
Send current Blocket watch config to Telegram + delta-update instructions.
Re-runnable anytime; no LLM (uses openclaw message send only).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
CONFIG_PATH = DIR / "config.json"


def chunk_text(text: str, max_len: int = 3900) -> list[str]:
    """Split on newlines so each part stays under Telegram's ~4096 limit."""
    if len(text) <= max_len:
        return [text]
    parts: list[str] = []
    rest = text
    while rest:
        if len(rest) <= max_len:
            parts.append(rest)
            break
        cut = rest.rfind("\n", 0, max_len)
        if cut <= 0:
            cut = max_len
        parts.append(rest[:cut])
        rest = rest[cut:].lstrip("\n")
    return parts


def format_message(config: dict, config_path: Path) -> str:
    lines = [
        "Blocket watch — current configuration",
        "(re-run onboard.sh anytime to see this again)",
        "",
        f"enabled: {json.dumps(config.get('enabled'))}",
        f"telegram_target: {config.get('telegram_target', '')}",
        "",
        "Queries (argv = arguments after `blocket`):",
        "",
    ]
    queries = config.get("queries") or []
    if not queries:
        lines.append("  (none — add objects with label + argv in config.json)")
        lines.append("")
    for i, q in enumerate(queries, 1):
        label = q.get("label") if isinstance(q, dict) else None
        argv = q.get("argv") if isinstance(q, dict) else None
        label_s = str(label) if label else f"query {i}"
        argv_s = json.dumps(argv, ensure_ascii=False) if isinstance(argv, list) else repr(argv)
        lines.append(f"  {i}. {label_s}")
        lines.append(f"     argv: {argv_s}")
        if isinstance(q, dict) and q.get("max_price") is not None:
            cur = q.get("max_price_currency") or "SEK"
            lines.append(f"     max_price: {q.get('max_price')} {cur} (notify only at or below)")
        lines.append("")
    lines.extend(
        [
            "—",
            "Reply with ONLY the changes you want (add/remove/rename searches,",
            "change keywords, location, price caps, etc.). Do not repeat rows that stay the same.",
            "",
            f"Ask the assistant to edit: {config_path}",
            '(each query: {"label", "argv", optional "max_price", "max_price_currency"} — see README.md)',
            "",
            f"Dry-run poll: BLOCKET_WATCH_DRY_RUN=1 {DIR / 'poll.sh'}",
        ]
    )
    return "\n".join(lines)


def send_telegram(target: str, parts: list[str], dry_run: bool) -> None:
    for i, body in enumerate(parts):
        if len(parts) > 1 and i > 0:
            body = f"(continued — part {i + 1} of {len(parts)})\n\n{body}"
        if dry_run:
            hdr = f"[dry-run] part {i + 1}/{len(parts)}\n"
            print(hdr + body)
            continue
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
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            print(r.stderr or r.stdout, file=sys.stderr)
            raise RuntimeError("openclaw message send failed")


def main() -> int:
    ap = argparse.ArgumentParser(description="Blocket watch onboarding / settings summary")
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Print message(s) to stdout; do not send Telegram",
    )
    args = ap.parse_args()

    if not CONFIG_PATH.exists():
        print(f"Missing {CONFIG_PATH}", file=sys.stderr)
        return 1

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    target = str(config.get("telegram_target") or "").strip()
    if not target and not args.dry_run:
        print("Set telegram_target in config.json", file=sys.stderr)
        return 1

    text = format_message(config, CONFIG_PATH.resolve())
    parts = chunk_text(text)

    if args.dry_run:
        send_telegram("", parts, dry_run=True)
        return 0

    send_telegram(target, parts, dry_run=False)
    print(f"Sent {len(parts)} Telegram message(s). Reply there with delta changes only.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"blocket-watch onboard: {e}", file=sys.stderr)
        raise SystemExit(1)
