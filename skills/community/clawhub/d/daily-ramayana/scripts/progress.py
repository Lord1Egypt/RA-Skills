#!/usr/bin/env python3
"""
daily-ramayana progress tracker + segment extractor.

Serves the bundled English text of the Vālmīki Rāmāyaṇa one segment at a time
(Books 1–6: R. T. H. Griffith's verse translation; Book 7: M. N. Dutt's prose
translation) and keeps a cursor so each day continues where the last left off.

Source text:   ../data/books/book01.md .. book07.md
Progress file: ~/.daily-ramayana/progress.json   (override with DAILY_RAMAYANA_PROGRESS)

Usage:
    python3 progress.py status
    python3 progress.py next                       # next segment as JSON (does NOT move the cursor)
    python3 progress.py advance <consumed> [--title "本期标题"]
    python3 progress.py set --book N [--offset M | --canto "XII"]
    python3 progress.py reset                      # back to Book 1 start (keeps language/target)
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
BOOK_DIR = SCRIPT_DIR.parent / "data" / "books"
PROGRESS_FILE = Path(
    os.path.expanduser(os.environ.get("DAILY_RAMAYANA_PROGRESS", "~/.daily-ramayana/progress.json"))
)

TOTAL_BOOKS = 7
BOOKS = {
    1: ("Bāla Kāṇḍa", "童年篇", "Griffith"),
    2: ("Ayodhyā Kāṇḍa", "阿逾陀篇", "Griffith"),
    3: ("Araṇya Kāṇḍa", "森林篇", "Griffith"),
    4: ("Kiṣkindhā Kāṇḍa", "猴国篇", "Griffith"),
    5: ("Sundara Kāṇḍa", "美妙篇", "Griffith"),
    6: ("Yuddha Kāṇḍa", "战斗篇", "Griffith"),
    7: ("Uttara Kāṇḍa", "后篇", "Dutt"),
}

DEFAULT_PROGRESS = {
    "currentBook": 1,
    "charOffset": 0,
    "segIndex": 0,
    "segCharsMin": 1500,
    "segCharsTarget": 2000,
    "segCharsMax": 2500,
    "language": "zh",
    "history": [],
}

HEADING = re.compile(r"^## (Canto|Section) [IVXLC]+.*$", re.M)


def load():
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        for k, v in DEFAULT_PROGRESS.items():
            data.setdefault(k, v if not isinstance(v, list) else list(v))
        return data
    d = dict(DEFAULT_PROGRESS)
    d["history"] = []
    return d


def save(data):
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def book_body(book):
    """Book text with the top '# Book N' title line removed (offsets are relative to this)."""
    text = (BOOK_DIR / f"book{book:02d}.md").read_text(encoding="utf-8")
    m = re.match(r"# [^\n]*\n+", text)
    return text[m.end():] if m else text


def heading_before(body, pos):
    last = None
    for m in HEADING.finditer(body, 0, pos + 1):
        if m.start() <= pos:
            last = m.group(0)[3:]
    return last


def choose_cut(body, start, lo, target, hi):
    """Return cut position (absolute) for a segment starting at `start`."""
    n = len(body)
    if n - start <= hi:
        return n
    # 1) whole cantos: last canto heading inside (start+lo, start+hi]
    heads = [m.start() for m in HEADING.finditer(body, start + 1, start + hi + 1)]
    good = [h for h in heads if h - start >= lo]
    if good:
        return good[-1]
    # 2) stanza / paragraph boundary nearest target within [lo, hi]
    best = best_any = None
    for m in re.finditer(r"\n\s*\n", body[start + lo : start + hi]):
        p = start + lo + m.end()
        before = body[start + lo : start + lo + m.start()].rstrip()
        if best_any is None or abs(p - (start + target)) < abs(best_any - (start + target)):
            best_any = p
        if re.search(r"[\.!?\]][\"”’']?$", before):
            if best is None or abs(p - (start + target)) < abs(best - (start + target)):
                best = p
    if best is not None:
        return best
    # 3) sentence end (prose sentence or verse line ending in . ! ?) nearest target within [lo, hi]
    sent = None
    for m in re.finditer(r"[\.!?][\"”’']?(?=\s)", body[start + lo : start + hi]):
        p = start + lo + m.end()
        if sent is None or abs(p - (start + target)) < abs(sent - (start + target)):
            sent = p
    if sent is not None:
        return sent
    # 4) any stanza break, else hard cut at target
    return best_any if best_any is not None else start + target


def next_segment():
    p = load()
    book = p["currentBook"]
    if book > TOTAL_BOOKS:
        return {"done_all": True, "book": book, "episode": len(p["history"]) + 1}
    body = book_body(book)
    start = p["charOffset"]
    if start >= len(body.rstrip()):
        return {"done_book": True, "done_all": book >= TOTAL_BOOKS, "book": book,
                "hint": "run advance 0 to roll to the next book"}
    cut = choose_cut(body, start, p["segCharsMin"], p["segCharsTarget"], p["segCharsMax"])
    raw = body[start:cut]
    cantos = []
    first = heading_before(body, start)
    if first and not raw.lstrip().startswith("## "):
        cantos.append(first + " (cont.)")
    cantos += [m.group(0)[3:] for m in HEADING.finditer(raw)]
    name, zh, tr = BOOKS[book]
    remaining = max(0, len(body.rstrip()) - cut)
    return {
        "done_book": False,
        "done_all": False,
        "episode": len(p["history"]) + 1,
        "book": book,
        "total_books": TOTAL_BOOKS,
        "book_name": name,
        "book_name_zh": zh,
        "translator": "R. T. H. Griffith (verse)" if tr == "Griffith" else "M. N. Dutt (prose, OCR)",
        "seg_index": p["segIndex"],
        "char_offset": start,
        "consumed": cut - start,
        "cantos": cantos,
        "text": raw.strip(),
        "book_len": len(body),
        "remaining_after": remaining,
        "last_in_book": remaining == 0,
        "language": p.get("language", "zh"),
    }


def advance(consumed, title=None):
    p = load()
    book = p["currentBook"]
    if book > TOTAL_BOOKS:
        return {"done_all": True}
    consumed = int(consumed)
    body = book_body(book)
    new_off = p["charOffset"] + consumed
    if consumed > 0:
        p["history"].append({
            "episode": len(p["history"]) + 1,
            "book": book,
            "segIndex": p["segIndex"],
            "charOffset": p["charOffset"],
            "consumed": consumed,
            "title": title or "",
            "completedAt": datetime.now(timezone.utc).isoformat(),
        })
    if new_off >= len(body.rstrip()):
        p["currentBook"] = book + 1
        p["segIndex"] = 0
        p["charOffset"] = 0
        rolled = True
    else:
        p["segIndex"] += 1
        p["charOffset"] = new_off
        rolled = False
    save(p)
    return {"currentBook": p["currentBook"], "charOffset": p["charOffset"],
            "segIndex": p["segIndex"], "rolledBook": rolled,
            "episodesDone": len(p["history"]), "doneAll": p["currentBook"] > TOTAL_BOOKS}


def cmd_status(a):
    p = load()
    out = {k: v for k, v in p.items() if k != "history"}
    out["episodesDone"] = len(p["history"])
    out["lastEpisode"] = p["history"][-1] if p["history"] else None
    b = p["currentBook"]
    if b <= TOTAL_BOOKS:
        body = book_body(b)
        out["bookName"] = f"{BOOKS[b][0]}（{BOOKS[b][1]}）"
        out["bookPercent"] = round(100 * p["charOffset"] / max(1, len(body)), 1)
        out["currentCanto"] = heading_before(body, p["charOffset"])
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_next(a):
    print(json.dumps(next_segment(), ensure_ascii=False))


def cmd_advance(a):
    print(json.dumps(advance(a.consumed, title=a.title), ensure_ascii=False))


def cmd_set(a):
    p = load()
    if a.book is not None:
        if not 1 <= a.book <= TOTAL_BOOKS:
            sys.exit("❌ book must be 1-7")
        p["currentBook"] = a.book
        p["charOffset"] = 0
        p["segIndex"] = 0
    if a.canto:
        body = book_body(p["currentBook"])
        m = re.search(rf"^## (Canto|Section) {re.escape(a.canto.upper())}\b", body, re.M)
        if not m:
            sys.exit(f"❌ canto/section {a.canto} not found in book {p['currentBook']}")
        p["charOffset"] = m.start()
        p["segIndex"] = 0
    elif a.offset is not None:
        p["charOffset"] = a.offset
        p["segIndex"] = 0
    save(p)
    print(f"📍 Set to book {p['currentBook']}, charOffset {p['charOffset']}")


def cmd_reset(a):
    old = load()
    p = dict(DEFAULT_PROGRESS)
    p["history"] = []
    for k in ("language", "segCharsMin", "segCharsTarget", "segCharsMax"):
        p[k] = old.get(k, p[k])
    save(p)
    print("🔄 Progress reset to the beginning (Book 1, Canto I).")


def cmd_set_lang(a):
    p = load()
    p["language"] = a.lang
    save(p)
    print(f"🌐 Language set to: {'中文' if a.lang == 'zh' else 'English'}")


def main():
    ap = argparse.ArgumentParser(description="daily-ramayana progress tracker")
    sub = ap.add_subparsers(dest="command")
    sub.add_parser("status")
    sub.add_parser("next")
    adv = sub.add_parser("advance")
    adv.add_argument("consumed")
    adv.add_argument("--title")
    sp = sub.add_parser("set")
    sp.add_argument("--book", type=int)
    sp.add_argument("--offset", type=int)
    sp.add_argument("--canto", help="Roman numeral, e.g. XII")
    sub.add_parser("reset")
    sl = sub.add_parser("set-lang")
    sl.add_argument("--lang", required=True, choices=["zh", "en"])
    a = ap.parse_args()
    if not a.command:
        ap.print_help()
        sys.exit(1)
    {"status": cmd_status, "next": cmd_next, "advance": cmd_advance, "set": cmd_set,
     "reset": cmd_reset, "set-lang": cmd_set_lang}[a.command](a)


if __name__ == "__main__":
    main()
