#!/usr/bin/env python3
"""
daily-xuanzang progress tracker + segment extractor.

Reads the bundled 12-volume source text of 《大唐西域记》 (Great Tang Records on the
Western Regions, CBETA T51n2087) and serves one segment at a time, tracking a cursor
so each day continues where the last left off.

Source text lives next to this script at:  ../data/volumes/vol01.txt .. vol12.txt
Progress is stored at:                      ~/.openclaw/workspace/daily-xuanzang/progress.json

Usage:
    python3 progress.py status                 # Show cursor + language
    python3 progress.py next                   # Print next segment (JSON)
    python3 progress.py advance <consumed>     # Advance cursor by N chars (after writing the lecture)
    python3 progress.py set --volume N --offset M
    python3 progress.py reset
    python3 progress.py set-lang --lang zh|en
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VOL_DIR = SCRIPT_DIR.parent / "data" / "volumes"
PROGRESS_FILE = Path(
    os.path.expanduser("~/.openclaw/workspace/daily-xuanzang/progress.json")
)

TOTAL_VOLUMES = 12

DEFAULT_PROGRESS = {
    "currentVolume": 1,
    "charOffset": 0,
    "segIndex": 0,
    "segCharsTarget": 900,
    "language": "",
    "history": [],
}

# 正文真正开始的锚点（卷一序末；其余卷用国名清单结束后的首段正文）
NARRATIVE_START_HINTS = [
    r"印\s*度風俗，語在後記。",
    r"曰阿耆尼國",
]


def ensure_dir():
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)


def load():
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        for k, v in DEFAULT_PROGRESS.items():
            data.setdefault(k, v)
        return data
    return dict(DEFAULT_PROGRESS)


def save(data):
    ensure_dir()
    PROGRESS_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def vol_body(vol):
    return (VOL_DIR / f"vol{vol:02d}.txt").read_text(encoding="utf-8")


def strip_volume_header(body):
    """返回正文起点 base：跳过译者署名 + 国名目次清单，定位到正文/序起点。"""
    m = re.search(r"撰\s*", body)
    start = m.end() if m else 0
    anchor = None
    for hint in NARRATIVE_START_HINTS:
        a = re.search(hint, body)
        if a:
            anchor = a.start()
            break
    if anchor is not None and anchor > start:
        start = anchor
    return start


def clean_segment_text(s):
    out = []
    for ln in s.splitlines():
        t = ln.strip()
        if not t:
            continue
        if re.fullmatch(r"\d{1,4}", t):
            continue
        if "cbeta" in t.lower():
            continue
        out.append(t)
    return "".join(out)


def next_segment():
    p = load()
    vol = p["currentVolume"]
    if vol > TOTAL_VOLUMES:
        return {"done_all": True, "vol": vol}
    off = p["charOffset"]
    target = p.get("segCharsTarget", 900)
    body = vol_body(vol)
    base = strip_volume_header(body)
    start = base + off
    if start >= len(body):
        return {"done_volume": True, "vol": vol}

    window = body[start : start + target + 500]
    cut = min(target, len(window))
    if len(window) > target:
        m = re.search(r"[。！？」]", window[target:])
        cut = target + m.end() if m else len(window)
    raw = window[:cut]
    seg_text = clean_segment_text(raw)
    consumed = cut

    return {
        "done_volume": False,
        "done_all": False,
        "vol": vol,
        "total_volumes": TOTAL_VOLUMES,
        "seg_index": p["segIndex"],
        "char_offset": off,
        "consumed": consumed,
        "text": seg_text,
        "vol_body_len": len(body),
        "remaining_after": max(0, len(body) - (start + consumed)),
    }


def advance(consumed, title=None, next_preview=None):
    p = load()
    vol = p["currentVolume"]
    consumed = int(consumed)
    body = vol_body(vol)
    base = strip_volume_header(body)
    new_off = p["charOffset"] + consumed
    p["history"].append(
        {
            "volume": vol,
            "segIndex": p["segIndex"],
            "consumed": consumed,
            "title": title or "",
            "completedAt": datetime.now(timezone.utc).isoformat(),
        }
    )
    if base + new_off >= len(body):
        p["currentVolume"] = vol + 1
        p["segIndex"] = 0
        p["charOffset"] = 0
        rolled = True
    else:
        p["segIndex"] += 1
        p["charOffset"] = new_off
        rolled = False
    save(p)
    return {
        "currentVolume": p["currentVolume"],
        "charOffset": p["charOffset"],
        "segIndex": p["segIndex"],
        "rolledVolume": rolled,
    }


def cmd_status(args):
    p = load()
    if not p["language"]:
        print("⚠️  Language not set. Run: python3 progress.py set-lang --lang zh|en")
    print(json.dumps(p, ensure_ascii=False, indent=2))


def cmd_next(args):
    print(json.dumps(next_segment(), ensure_ascii=False))


def cmd_advance(args):
    print(
        json.dumps(
            advance(args.consumed, title=args.title, next_preview=args.next),
            ensure_ascii=False,
        )
    )


def cmd_set(args):
    p = load()
    if args.volume is not None:
        p["currentVolume"] = args.volume
    if args.offset is not None:
        p["charOffset"] = args.offset
        p["segIndex"] = 0
    save(p)
    print(f"📍 Set to volume {p['currentVolume']}, charOffset {p['charOffset']}")


def cmd_reset(args):
    p = dict(DEFAULT_PROGRESS)
    # 保留语言偏好
    old = load()
    p["language"] = old.get("language", "")
    save(p)
    print("🔄 Progress reset to beginning (卷一 起点).")


def cmd_set_lang(args):
    if args.lang not in ("zh", "en"):
        print("❌ Language must be 'zh' or 'en'", file=sys.stderr)
        sys.exit(1)
    p = load()
    p["language"] = args.lang
    save(p)
    label = "中文" if args.lang == "zh" else "English"
    print(f"🌐 Language set to: {label}")


def main():
    parser = argparse.ArgumentParser(description="daily-xuanzang progress tracker")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="Show current cursor + language")
    sub.add_parser("next", help="Print next source segment as JSON")

    adv = sub.add_parser("advance", help="Advance cursor by consumed chars")
    adv.add_argument("consumed", help="Number of chars consumed (from 'next')")
    adv.add_argument("--title", help="Title of completed lecture")
    adv.add_argument("--next", help="Preview/title of next lecture")

    sp = sub.add_parser("set", help="Jump to a specific position")
    sp.add_argument("--volume", type=int, help="Volume number (1-12)")
    sp.add_argument("--offset", type=int, help="Char offset within volume body")

    sub.add_parser("reset", help="Reset to beginning")

    sl = sub.add_parser("set-lang", help="Set language preference")
    sl.add_argument("--lang", required=True, choices=["zh", "en"], help="zh or en")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    {
        "status": cmd_status,
        "next": cmd_next,
        "advance": cmd_advance,
        "set": cmd_set,
        "reset": cmd_reset,
        "set-lang": cmd_set_lang,
    }[args.command](args)


if __name__ == "__main__":
    main()
