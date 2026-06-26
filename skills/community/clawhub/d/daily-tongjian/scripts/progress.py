#!/usr/bin/env python3
"""
daily-tongjian progress tracker.

Stores reading progress in ~/.openclaw/workspace/daily-tongjian/progress.json

Usage:
    python3 progress.py status                          # Show current position
    python3 progress.py advance --title "..." --next "..." # Mark done, advance
    python3 progress.py set --volume N --lecture N --title "..."  # Jump to position
    python3 progress.py reset                           # Start over
    python3 progress.py set-lang --lang zh|en           # Change language
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

PROGRESS_FILE = os.path.expanduser("~/.openclaw/workspace/daily-tongjian/progress.json")

DEFAULT_PROGRESS = {
    "currentVolume": 1,
    "currentLecture": 1,
    "lectureTitle": "",
    "nextPreview": "",
    "language": "",
    "history": []
}


def ensure_dir():
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)


def load():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for k, v in DEFAULT_PROGRESS.items():
            if k not in data:
                data[k] = v
        return data
    return dict(DEFAULT_PROGRESS)


def save(data):
    ensure_dir()
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def cmd_status(args):
    data = load()
    if not data["language"]:
        print("⚠️  Language not set. Run: python3 progress.py set-lang --lang zh|en")
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_advance(args):
    data = load()
    data["history"].append({
        "volume": data["currentVolume"],
        "lecture": data["currentLecture"],
        "title": data["lectureTitle"],
        "completedAt": datetime.now(timezone.utc).isoformat()
    })
    data["currentLecture"] += 1
    data["lectureTitle"] = args.next or ""
    data["nextPreview"] = ""
    if args.title:
        data["history"][-1]["title"] = args.title
    save(data)
    print(f"✅ Advanced to lecture {data['currentLecture']} (volume {data['currentVolume']})")
    if args.next:
        print(f"📖 Next: {args.next}")


def cmd_set(args):
    data = load()
    if args.volume is not None:
        data["currentVolume"] = args.volume
    if args.lecture is not None:
        data["currentLecture"] = args.lecture
    if args.title is not None:
        data["lectureTitle"] = args.title
    save(data)
    print(f"📍 Set to volume {data['currentVolume']}, lecture {data['currentLecture']}: {data['lectureTitle']}")


def cmd_reset(args):
    save(dict(DEFAULT_PROGRESS))
    print("🔄 Progress reset to beginning.")


def cmd_set_lang(args):
    if args.lang not in ("zh", "en"):
        print("❌ Language must be 'zh' or 'en'", file=sys.stderr)
        sys.exit(1)
    data = load()
    data["language"] = args.lang
    save(data)
    label = "中文" if args.lang == "zh" else "English"
    print(f"🌐 Language set to: {label}")


def main():
    parser = argparse.ArgumentParser(description="daily-tongjian progress tracker")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="Show current progress")

    adv = sub.add_parser("advance", help="Complete current lecture, advance")
    adv.add_argument("--title", help="Title of completed lecture")
    adv.add_argument("--next", help="Preview/title of next lecture")

    sp = sub.add_parser("set", help="Jump to a specific position")
    sp.add_argument("--volume", type=int, help="Volume number (1-294)")
    sp.add_argument("--lecture", type=int, help="Lecture number within volume")
    sp.add_argument("--title", help="Lecture title")

    sub.add_parser("reset", help="Reset to beginning")

    sl = sub.add_parser("set-lang", help="Set language preference")
    sl.add_argument("--lang", required=True, choices=["zh", "en"], help="zh or en")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    {
        "status": cmd_status,
        "advance": cmd_advance,
        "set": cmd_set,
        "reset": cmd_reset,
        "set-lang": cmd_set_lang,
    }[args.command](args)


if __name__ == "__main__":
    main()
