#!/usr/bin/env python3
"""《AI四库全典》离线全文检索 —— 仅用 Python 标准库，零依赖、无网络。

用法:
  python3 scripts/search.py "世界模型 压缩 预测"      # 多词 AND 检索
  python3 scripts/search.py "RAG" --vol 子 --limit 8  # 限定部类
  python3 scripts/search.py --read vol-031 --lines 120
  python3 scripts/search.py --list
  python3 scripts/search.py "智能体" --json
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CORPUS = os.path.join(ROOT, "assets", "corpus")
MANIFEST = os.path.join(CORPUS, "manifest.json")


def load_manifest():
    with open(MANIFEST, encoding="utf-8") as f:
        return json.load(f)["volumes"]


def read_volume(v):
    with open(os.path.join(CORPUS, v["file"]), encoding="utf-8") as f:
        return f.read()


def blocks_of(text):
    """按 Markdown 标题切块，保留标题上下文；每块作为一条可引用片段。"""
    lines = text.splitlines()
    out, head, buf = [], "", []

    def flush():
        body = "\n".join(buf).strip()
        if body:
            out.append((head, body))

    for line in lines:
        if re.match(r"^#{1,6}\s+", line):
            flush()
            head = line.lstrip("#").strip()
            buf = []
        else:
            buf.append(line)
    flush()
    if not out:
        out = [("", text.strip())]
    return out


def search(query, vols, limit, snippet):
    tokens = [t for t in re.split(r"\s+", query.strip()) if t]
    if not tokens:
        return []
    low = [t.lower() for t in tokens]
    phrase = query.strip().lower()
    results = []
    for v in vols:
        text = read_volume(v)
        lowtext = text.lower()
        if not all(t in lowtext for t in low):
            continue
        for head, body in blocks_of(text):
            b = body.lower()
            if not all(t in b for t in low):
                continue
            score = sum(min(b.count(t), 20) for t in low)
            if phrase in b:
                score += 25
            if head and any(t in head.lower() for t in low):
                score += 12
            flat = re.sub(r"\s+", " ", body).strip()
            pos = min([flat.lower().find(t) for t in low if flat.lower().find(t) >= 0] or [0])
            start = max(0, pos - 60)
            results.append({
                "score": score,
                "id": v["id"],
                "part": v["partName"],
                "no": v["no"],
                "title": v["title"],
                "heading": head,
                "snippet": flat[start:start + snippet],
            })
    results.sort(key=lambda x: -x["score"])
    return results[:limit]


def fmt_hit(h, i):
    src = "%s·第%d卷《%s》" % (h["part"], h["no"], h["title"])
    if h["heading"]:
        src += " · " + h["heading"]
    return "[%d] 得分 %d ｜ %s ｜ %s\n    %s" % (i + 1, h["score"], h["id"], src, h["snippet"])


def main():
    ap = argparse.ArgumentParser(description="《AI四库全典》离线全文检索")
    ap.add_argument("query", nargs="*", help="检索词，空格分隔表示同时命中")
    ap.add_argument("--limit", type=int, default=6, help="返回条数，默认 6")
    ap.add_argument("--snippet", type=int, default=320, help="摘要长度，默认 320 字")
    ap.add_argument("--vol", choices=["经", "史", "子", "集"], help="限定部类")
    ap.add_argument("--id", help="限定卷 ID，如 vol-031")
    ap.add_argument("--read", help="读取整卷，如 vol-031")
    ap.add_argument("--lines", type=int, default=100, help="--read 时输出前 N 行")
    ap.add_argument("--all", action="store_true", help="--read 时输出全文")
    ap.add_argument("--list", action="store_true", help="列出全书 48 卷")
    ap.add_argument("--json", action="store_true", help="结构化输出")
    a = ap.parse_args()

    vols = load_manifest()

    if a.list:
        if a.json:
            print(json.dumps(vols, ensure_ascii=False, indent=1))
        else:
            cur = None
            for v in vols:
                if v["partName"] != cur:
                    cur = v["partName"]
                    print("\n== " + cur + " ==")
                print("%s  第%d卷  %s  (%s字)" % (v["id"], v["no"], v["title"], v["words"]))
        return

    if a.read:
        hit = [v for v in vols if v["id"] == a.read]
        if not hit:
            sys.exit("没有这一卷：%s（可用 --list 查看卷 ID）" % a.read)
        text = read_volume(hit[0])
        out = text if a.all else "\n".join(text.splitlines()[:a.lines])
        print(out)
        if not a.all and len(text.splitlines()) > a.lines:
            print("\n… 还有 %d 行，追加 --all 读取全文" % (len(text.splitlines()) - a.lines))
        return

    query = " ".join(a.query).strip()
    if not query:
        ap.print_help()
        return

    sel = vols
    if a.vol:
        sel = [v for v in sel if v["part"] == a.vol]
    if a.id:
        sel = [v for v in sel if v["id"] == a.id]

    hits = search(query, sel, a.limit, a.snippet)
    if a.json:
        print(json.dumps(hits, ensure_ascii=False, indent=1))
        return
    if not hits:
        print("全书中没有检索到同时包含「%s」的段落。" % query)
        print("提示：减少关键词，或改用 --list / --read 浏览目录。")
        return
    print("《AI四库全典》命中 %d 处（按相关度排序）：\n" % len(hits))
    for i, h in enumerate(hits):
        print(fmt_hit(h, i))
        print()


if __name__ == "__main__":
    main()
