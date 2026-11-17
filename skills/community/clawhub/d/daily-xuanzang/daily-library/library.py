#!/usr/bin/env python3
"""Per-book library for the daily-reading skills (tongjian / xuanzang / ramayana / zen-koan).

Layout (one self-contained folder per book):
  /workspace/library/<book>/
    book.json        manifest, episodes in reading order (export scripts read this)
    index.md         table of contents (regenerated from book.json)
    <chapter-dir>/epNNN/   lecture.md  image.png|map.png  voice.mp3  read.txt
  zen-koan has no chapters:  zen-koan/epNNN-<slug>/...

Commands:
  add     file one episode (copies files in, rewrites media links, updates book.json + index.md)
  index   regenerate index.md for a book
  status  list episodes and which files each one is missing (JSON)
"""
import argparse, datetime, json, os, re, shutil, sys
from zoneinfo import ZoneInfo

LIB = os.environ.get("DAILY_LIBRARY", "/workspace/library")
TZ = ZoneInfo("America/Los_Angeles")

BOOKS = {
    "tongjian": {"title": "资治通鉴", "series": "每日通鉴", "unit": "卷", "chapter_fmt": "vol{:03d}",
                  "chapter_label": "卷 {}", "image_name": "image", "total_chapters": 294},
    "xuanzang": {"title": "大唐西域记", "series": "每日西域记", "unit": "卷", "chapter_fmt": "vol{:02d}",
                  "chapter_label": "卷 {}", "image_name": "map", "total_chapters": 12},
    "ramayana": {"title": "罗摩衍那", "series": "每日罗摩衍那", "unit": "篇", "chapter_fmt": "book{:02d}",
                  "chapter_label": "第 {} 篇", "image_name": "image", "total_chapters": 7},
    "zen-koan": {"title": "禅宗公案", "series": "每日禅宗公案", "unit": None, "chapter_fmt": None,
                  "chapter_label": None, "image_name": "image", "total_chapters": None},
}
RAMAYANA_BOOKS = {1: "Bāla Kāṇḍa 童年篇", 2: "Ayodhyā Kāṇḍa 阿逾陀篇", 3: "Araṇya Kāṇḍa 森林篇",
                  4: "Kiṣkindhā Kāṇḍa 猴国篇", 5: "Sundara Kāṇḍa 美妙篇", 6: "Yuddha Kāṇḍa 战斗篇",
                  7: "Uttara Kāṇḍa 后篇"}


def book_dir(book):
    return os.path.join(LIB, book)


def load_manifest(book):
    p = os.path.join(book_dir(book), "book.json")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    meta = BOOKS[book]
    return {"book": book, "title": meta["title"], "series": meta["series"],
            "chapter_unit": meta["unit"], "total_chapters": meta["total_chapters"],
            "layout_version": 1, "episodes": []}


def save_manifest(book, m):
    m["episodes"].sort(key=lambda e: (e["episode"]))
    m["updated"] = datetime.datetime.now(TZ).isoformat(timespec="seconds")
    os.makedirs(book_dir(book), exist_ok=True)
    p = os.path.join(book_dir(book), "book.json")
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
    os.replace(tmp, p)


def slugify(s):
    s = re.sub(r"[^\w\-]+", "-", s.strip().lower(), flags=re.UNICODE).strip("-")
    return s or "koan"


def episode_rel_dir(book, episode, chapter, slug):
    meta = BOOKS[book]
    ep = f"ep{episode:03d}"
    if meta["chapter_fmt"] is None:
        return f"{ep}-{slugify(slug)}" if slug else ep
    if chapter is None:
        sys.exit("--chapter is required for book " + book)
    return os.path.join(meta["chapter_fmt"].format(chapter), ep)


MEDIA_LINE = re.compile(r"^\s*[（(]?(路线地图|配图|语音|地图|图片)[:：].*(/workspace/|\.png|\.jpg|\.mp3).*$")
BEGIN, END = "<!-- media:begin -->", "<!-- media:end -->"


def media_block(image_rel, audio_rel, image_alt):
    parts = [BEGIN]
    if image_rel:
        parts.append(f"![{image_alt}]({image_rel})")
        parts.append("")
    if audio_rel:
        parts.append(f'<audio controls src="{audio_rel}"></audio>')
        parts.append("")
        parts.append(f"🔊 语音朗读：[{audio_rel}]({audio_rel})")
    parts.append(END)
    return "\n".join(parts)


def build_lecture(text, image_rel, audio_rel, image_alt):
    # drop old absolute-path media notes and any previous media block
    text = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n*", "", text, flags=re.S)
    lines = [l for l in text.splitlines() if not MEDIA_LINE.match(l)]
    block = media_block(image_rel, audio_rel, image_alt)
    if not image_rel and not audio_rel:
        return "\n".join(lines).rstrip() + "\n"
    # insert after the first horizontal rule (end of header block); else after the H2 title
    idx = next((i for i, l in enumerate(lines) if l.strip() == "---"), None)
    if idx is None:
        idx = next((i for i, l in enumerate(lines) if l.startswith("#")), -1)
    out = lines[:idx + 1] + ["", block, ""] + lines[idx + 1:]
    return "\n".join(out).rstrip() + "\n"


def chapter_label(book, chapter):
    meta = BOOKS[book]
    if chapter is None or meta["chapter_label"] is None:
        return None
    lab = meta["chapter_label"].format(chapter)
    if book == "ramayana" and chapter in RAMAYANA_BOOKS:
        lab += " · " + RAMAYANA_BOOKS[chapter]
    return lab


def write_index(book, m):
    meta = BOOKS[book]
    L = [f"# {m['title']} · {m['series']}", "",
         f"共 {len(m['episodes'])} 期 · 更新于 {m.get('updated', '')}", "",
         "按阅读顺序排列。每期文件夹内：`lecture.md` 讲稿、图片、`voice.mp3` 语音、`read.txt` 朗读稿。", ""]
    cur = object()
    if not meta["chapter_fmt"]:
        L += ["| 期 | 标题 | 出处 | 日期 | 讲稿 | 图 | 语音 |", "|---|---|---|---|---|---|---|"]
    for e in m["episodes"]:
        ch = e.get("chapter")
        if meta["chapter_fmt"] and ch != cur:
            cur = ch
            L += ["", f"## {e.get('chapter_label') or ch}", "",
                  "| 期 | 标题 | 日期 | 讲稿 | 图 | 语音 |", "|---|---|---|---|---|---|"]
        d, f = e["dir"], e["files"]
        lk = lambda k, label: f"[{label}]({d}/{f[k]})" if f.get(k) else "—"
        row = [str(e["episode"]), e.get("title", "")]
        if not meta["chapter_fmt"]:
            row.append(e.get("source", ""))
        row += [e.get("date", ""), lk("lecture", "讲稿"), lk("image", "图"), lk("audio", "语音")]
        L.append("| " + " | ".join(r.replace("|", "／") for r in row) + " |")
    with open(os.path.join(book_dir(book), "index.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L).rstrip() + "\n")


def cmd_add(a):
    book = a.book
    m = load_manifest(book)
    meta = BOOKS[book]
    prev = next((e for e in m["episodes"] if e["episode"] == a.episode), None)
    if prev and a.chapter is None and not a.slug:
        # filling in pieces of an existing episode: reuse its folder
        rel, a.chapter = prev["dir"], prev.get("chapter")
    else:
        rel = episode_rel_dir(book, a.episode, a.chapter, a.slug)
    if prev and prev["dir"] != rel:
        old_dir = os.path.join(book_dir(book), prev["dir"])
        if os.path.isdir(old_dir) and not os.path.exists(os.path.join(book_dir(book), rel)):
            os.makedirs(os.path.dirname(os.path.join(book_dir(book), rel)) or ".", exist_ok=True)
            shutil.move(old_dir, os.path.join(book_dir(book), rel))
    dest = os.path.join(book_dir(book), rel)
    os.makedirs(dest, exist_ok=True)
    files = dict(prev["files"]) if prev else {}

    image_rel = files.get("image")
    if a.image:
        ext = os.path.splitext(a.image)[1].lower() or ".png"
        image_rel = meta["image_name"] + ext
        if os.path.abspath(a.image) != os.path.abspath(os.path.join(dest, image_rel)):
            shutil.copy2(a.image, os.path.join(dest, image_rel))
        files["image"] = image_rel
    audio_rel = files.get("audio")
    if a.audio:
        audio_rel = "voice.mp3"
        if os.path.abspath(a.audio) != os.path.abspath(os.path.join(dest, audio_rel)):
            shutil.copy2(a.audio, os.path.join(dest, audio_rel))
        files["audio"] = audio_rel
    if a.read:
        if os.path.abspath(a.read) != os.path.abspath(os.path.join(dest, "read.txt")):
            shutil.copy2(a.read, os.path.join(dest, "read.txt"))
        files["read"] = "read.txt"
    lec_src = a.lecture or (os.path.join(dest, "lecture.md") if files.get("lecture") else None)
    if lec_src:
        with open(lec_src, encoding="utf-8") as f:
            text = f.read()
        alt = "路线图" if meta["image_name"] == "map" else "配图"
        with open(os.path.join(dest, "lecture.md"), "w", encoding="utf-8") as f:
            f.write(build_lecture(text, image_rel, audio_rel, alt))
        files["lecture"] = "lecture.md"

    e = prev or {"episode": a.episode}
    e.update({"chapter": a.chapter, "chapter_label": a.chapter_label or chapter_label(book, a.chapter),
              "dir": rel, "files": files})
    for k in ("title", "date", "source", "range"):
        v = getattr(a, k)
        if v:
            e[k] = v
    if not e.get("date"):
        e["date"] = datetime.datetime.now(TZ).date().isoformat()
    if a.meta:
        e.setdefault("meta", {})
        for kv in a.meta:
            k, _, v = kv.partition("=")
            e["meta"][k] = v
    if not prev:
        m["episodes"].append(e)
    save_manifest(book, m)
    write_index(book, m)
    print(json.dumps({"ok": True, "book": book, "episode": a.episode, "dir": dest, "files": files},
                     ensure_ascii=False))


def cmd_index(a):
    m = load_manifest(a.book)
    save_manifest(a.book, m)
    write_index(a.book, m)
    print("ok")


def cmd_status(a):
    m = load_manifest(a.book)
    out = []
    for e in m["episodes"]:
        missing = [k for k in ("lecture", "image", "audio", "read") if not e["files"].get(k)
                   or not os.path.exists(os.path.join(book_dir(a.book), e["dir"], e["files"][k]))]
        out.append({"episode": e["episode"], "title": e.get("title"), "date": e.get("date"),
                    "dir": e["dir"], "missing": missing})
    print(json.dumps({"book": a.book, "count": len(out), "next_episode": (max([o["episode"] for o in out]) + 1) if out else 1,
                      "episodes": out}, ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    ad = sub.add_parser("add", help="file one episode into the library (re-run to fill in missing pieces)")
    ad.add_argument("--book", required=True, choices=BOOKS)
    ad.add_argument("--episode", required=True, type=int)
    ad.add_argument("--chapter", type=int, help="卷/篇 number (not for zen-koan)")
    ad.add_argument("--chapter-label")
    ad.add_argument("--slug", help="zen-koan folder slug, e.g. ririshihaori")
    ad.add_argument("--title")
    ad.add_argument("--date", help="YYYY-MM-DD (default today, America/Los_Angeles)")
    ad.add_argument("--source", help="e.g. 碧岩录 第6则")
    ad.add_argument("--range", help="e.g. Canto I (cont.) / 屈支国→素叶水城")
    ad.add_argument("--lecture"); ad.add_argument("--image"); ad.add_argument("--audio"); ad.add_argument("--read")
    ad.add_argument("--meta", action="append", help="extra key=value")
    ad.set_defaults(fn=cmd_add)
    for name, fn in (("index", cmd_index), ("status", cmd_status)):
        sp = sub.add_parser(name)
        sp.add_argument("--book", required=True, choices=BOOKS)
        sp.set_defaults(fn=fn)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
