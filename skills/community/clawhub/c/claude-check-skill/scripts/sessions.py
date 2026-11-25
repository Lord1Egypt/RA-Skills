#!/usr/bin/env python3
"""找回本地 Claude Code 对话：扫描 .jsonl 记录，按关键词 / 项目 / 日期筛选，导出 Markdown。

只读。跳过符号链接，限制文件数量与大小，不扫描整个家目录。不上传、不修改原记录。
  python3 sessions.py --root ~/.claude/projects --q 关键词
  python3 sessions.py --root ~/.claude/projects --key <session_key> --export out.md
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path

MAX_FILE = 50 << 20
MAX_TOTAL = 128 << 20
MAX_FILES = 5000
HOME = Path.home()


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        out = []
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text" and isinstance(part.get("text"), str):
                out.append(part["text"])
        return "\n".join(out)
    return ""


def parse(path, rel):
    """解析一个 .jsonl，返回会话 dict。只取 user / assistant 的文本，忽略工具调用内容。"""
    key = hashlib.sha256(str(path).encode()).hexdigest()[:16]
    msgs, times, bad = [], [], 0
    try:
        with path.open(encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except ValueError:
                    bad += 1
                    continue
                if not isinstance(rec, dict) or rec.get("type") not in ("user", "assistant"):
                    continue
                m = rec.get("message")
                if not isinstance(m, dict):
                    continue
                body = text_of(m.get("content")).strip()
                if not body:
                    continue
                msgs.append({"role": m.get("role") or rec["type"], "text": body, "ts": rec.get("timestamp") or ""})
                if rec.get("timestamp"):
                    times.append(rec["timestamp"])
    except OSError:
        return {"key": key, "source": rel, "status": "error", "title": "", "messages": [], "started": "", "ended": "", "turns": 0, "bad": 0}
    times.sort()
    title = next((m["text"] for m in msgs if m["role"] == "user"), "") or (msgs[0]["text"] if msgs else "")
    return {"key": key, "source": rel, "status": "ok" if msgs else "empty",
            "title": re.sub(r"\s+", " ", title)[:80], "messages": msgs,
            "started": times[0][:19] if times else "", "ended": times[-1][:19] if times else "",
            "turns": len(msgs), "bad": bad}


def scan(root):
    root = Path(root).expanduser()
    resolved = root.resolve()
    if resolved == HOME.resolve() or resolved == resolved.parent:
        raise SystemExit("请指定具体的记录目录，不要用家目录或磁盘根目录")
    if not resolved.is_dir():
        raise SystemExit("目录不存在：%s" % root)
    sessions, total, files, partial = [], 0, 0, False
    for dirpath, dirnames, filenames in os.walk(resolved, followlinks=False):
        dirnames[:] = [d for d in dirnames if not (Path(dirpath) / d).is_symlink()]
        for name in sorted(filenames):
            if not name.lower().endswith(".jsonl"):
                continue
            p = Path(dirpath) / name
            if p.is_symlink() or not p.is_file():
                continue
            files += 1
            if files > MAX_FILES or total >= MAX_TOTAL:
                partial = True
                break
            size = p.stat().st_size
            if size > MAX_FILE:
                partial = True
                continue
            total += size
            rel = str(p.relative_to(resolved))
            s = parse(p, rel)
            s["project"] = rel.split(os.sep)[0] if os.sep in rel else "."
            sessions.append(s)
        if partial:
            break
    sessions.sort(key=lambda s: s["ended"] or s["started"], reverse=True)
    return sessions, partial


def match(s, q, project, since, until):
    if project and s.get("project") != project:
        return False
    stamp = (s["ended"] or s["started"])[:10]
    if since and stamp and stamp < since:
        return False
    if until and stamp and stamp > until:
        return False
    if q:
        ql = q.lower()
        if ql not in s["title"].lower() and not any(ql in m["text"].lower() for m in s["messages"]):
            return False
    return True


def markdown(s):
    lines = ["# %s" % (s["title"] or "（无标题）"), "",
             "- 记录：%s" % s["source"], "- 项目：%s" % s.get("project", ""),
             "- 时间：%s → %s" % (s["started"] or "未知", s["ended"] or "未知"),
             "- 轮次：%d" % s["turns"], ""]
    for m in s["messages"]:
        who = "用户" if m["role"] == "user" else "Claude"
        lines.append("## %s%s" % (who, ("　" + m["ts"][:19]) if m["ts"] else ""))
        lines.append(m["text"])
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", required=True, help="记录目录，如 ~/.claude/projects")
    ap.add_argument("--q", default="", help="关键词")
    ap.add_argument("--project", default="", help="只看某个项目目录")
    ap.add_argument("--since", default="", help="起始日期 YYYY-MM-DD")
    ap.add_argument("--until", default="", help="截止日期 YYYY-MM-DD")
    ap.add_argument("--key", help="导出指定会话（配合 --export）")
    ap.add_argument("--export", help="把 --key 对应会话写入该 Markdown 文件")
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    sessions, partial = scan(a.root)
    if a.key:
        s = next((x for x in sessions if x["key"] == a.key), None)
        if not s:
            raise SystemExit("未找到该会话，请重新扫描")
        md = markdown(s)
        if a.export:
            Path(a.export).expanduser().write_text(md, encoding="utf-8")
            print("已导出：%s（%d 轮）" % (a.export, s["turns"]))
        else:
            print(md)
        return
    hits = [s for s in sessions if match(s, a.q, a.project, a.since, a.until)]
    shown = hits[:a.limit]
    if a.json:
        print(json.dumps({"total": len(hits), "partial": partial,
                          "items": [{k: s[k] for k in ("key", "title", "project", "started", "ended", "turns", "status")} for s in shown]},
                         ensure_ascii=False, indent=2))
        return
    if partial:
        print("（达到扫描上限，结果可能不完整）")
    print("命中 %d 条%s：" % (len(hits), "，显示前 %d" % a.limit if len(hits) > a.limit else ""))
    for s in shown:
        print("- [%s] %s｜%s｜%s" % (s["key"], s["ended"][:10] or "日期未知", s["project"], s["title"] or "（无标题）"))
    if shown:
        print("\n导出：python3 sessions.py --root %s --key <上面的 key> --export 对话.md" % a.root)


if __name__ == "__main__":
    main()
