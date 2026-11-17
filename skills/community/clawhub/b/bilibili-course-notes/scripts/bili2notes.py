#!/usr/bin/env python3
"""bili2notes — B站视频 → Markdown 笔记（大纲、要点、带时间的逐字稿）。

    python bili2notes.py "https://www.bilibili.com/video/BV1pu411o7BE"          # 没有 Key：免费看一条摘要
    export LINKDIGEST_API_KEY=ld_live_...
    python bili2notes.py "https://www.bilibili.com/video/BV1pu411o7BE" -o note.md
    python bili2notes.py "【标题】 https://b23.tv/xxxx" --depth script          # 整段分享文字也行
    python bili2notes.py "https://www.bilibili.com/video/BV1JE411g7XF?p=2" --parts 1-10 --out-dir notes/

One file, standard library only, Python 3.9+. It does not download or
transcribe anything itself: it calls the hosted LinkDigest API
(https://linkdigest.dev/docs?ref=skill-bilibili-course-notes), which reads the video and
returns the transcript, a timed outline for long videos (`outline`), key
points, and — for a multi-part video (分P) — the list of its parts (`parts`).

Exit codes: 0 ok · 2 bad arguments · 3 key refused · 4 not enough credits ·
5 the link cannot be read · 6 refused or cancelled · 7 timed out.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Callable, Dict, List, Optional, Tuple

API = os.environ.get("LINKDIGEST_BASE_URL", "https://linkdigest.dev").rstrip("/")
DOCS = "https://linkdigest.dev/docs?ref=skill-bilibili-course-notes"
PRICING = "https://linkdigest.dev/pricing"
KEYS = "https://linkdigest.dev/signin?next=/app/keys"
UA = "bilibili-course-notes-skill/1.0 (+https://github.com/jcaiagent7143-ui/linkdigest-mcp/tree/main/skills/bilibili-course-notes)"
DEPTHS = ("script", "transcript", "full")

# (status, parsed JSON body). Tests pass their own.
Transport = Callable[[str, str, Optional[dict], Optional[str]], Tuple[int, Dict[str, Any]]]


class Stop(Exception):
    """A clean exit: the message goes to stderr, the code to the shell."""

    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code


# ---- links -------------------------------------------------------------------

_BV = re.compile(r"BV[0-9A-Za-z]{10}")
_URL = re.compile(r"https?://[^\s<>\"'，。！？；：、【】（）]+", re.I)
_BARE = re.compile(r"(?<![\w/.])((?:www\.|m\.)?bilibili\.com/[^\s，。！？；：、【】（）]+|b23\.tv/[0-9A-Za-z]+)", re.I)


def find_link(text: str) -> str:
    """The Bilibili link inside whatever was pasted: a URL, a bare BV id, or a
    whole share text (「【标题】 https://b23.tv/xxxx」)."""
    text = (text or "").strip()
    for m in _URL.finditer(text):
        # Text glued straight onto a link ("…/BV1xx复制此链接") is not part of it.
        url = re.sub(r"[^\x00-\x7f].*$", "", m.group(0)).rstrip(".,;:!?)]}>'\"")
        if re.search(r"(bilibili\.com|b23\.tv)", url, re.I):
            return url
    bare = _BARE.search(text)
    if bare:
        return "https://" + bare.group(1).rstrip(".,;:!?)")
    bv = _BV.search(text)
    if bv:
        part = re.search(r"[?&]p=(\d+)", text)
        return f"https://www.bilibili.com/video/{bv.group(0)}" + (f"?p={part.group(1)}" if part else "")
    raise Stop(2, "没有在输入里找到 B站 链接（bilibili.com / b23.tv / BV 号）。No Bilibili link found in the input.")


def bvid_of(*candidates: Optional[str]) -> Optional[str]:
    for c in candidates:
        m = _BV.search(c or "")
        if m:
            return m.group(0)
    return None


def part_link(bvid: str, p: int) -> str:
    return f"https://www.bilibili.com/video/{bvid}?p={p}"


def parse_parts(spec: str, count: int) -> List[int]:
    """「1-10」「3,5,8」「2-」「all」→ part numbers within 1..count, in order, no repeats."""
    spec = (spec or "").strip().lower()
    if not spec:
        raise Stop(2, "--parts 需要一个范围，例如 1-10、3,5,8 或 all")
    if spec in ("all", "全部"):
        return list(range(1, count + 1))
    picked: List[int] = []
    for piece in spec.replace("，", ",").split(","):
        piece = piece.strip()
        m = re.fullmatch(r"(\d*)\s*-\s*(\d*)", piece)
        if m and (m.group(1) or m.group(2)):
            lo = int(m.group(1)) if m.group(1) else 1
            hi = int(m.group(2)) if m.group(2) else count
        elif piece.isdigit():
            lo = hi = int(piece)
        else:
            raise Stop(2, f"看不懂 --parts 里的「{piece}」。用 1-10、3,5,8 或 all")
        if lo < 1 or lo > hi:
            raise Stop(2, f"--parts 的范围「{piece}」不对")
        for p in range(lo, min(hi, count) + 1):
            if p not in picked:
                picked.append(p)
    if not picked:
        raise Stop(2, f"这个视频只有 {count} P，--parts {spec} 里没有一个在范围内")
    return picked


# ---- what a read costs ---------------------------------------------------------

def estimate_credits(seconds: float, depth: str) -> int:
    """An estimate from the published rule (see the pricing page): script =
    one credit per started 2 minutes; transcript = 1 + that; full = 1 + one
    per started minute. A part someone already read costs nothing, and the
    service's own count is what is charged — this is only the ceiling shown
    before a batch starts."""
    seconds = max(0.0, float(seconds or 0))
    if depth == "script":
        return max(1, math.ceil(seconds / 120))
    if depth == "transcript":
        return 1 + math.ceil(seconds / 120)
    return 1 + math.ceil(seconds / 60)


# ---- rendering -----------------------------------------------------------------

def clock(seconds: Any) -> str:
    s = int(float(seconds or 0))
    h, rest = divmod(s, 3600)
    m, sec = divmod(rest, 60)
    return f"{h}:{m:02d}:{sec:02d}" if h else f"{m:02d}:{sec:02d}"


def render_note(d: Dict[str, Any], *, on_screen: bool = False) -> str:
    """One digest → one Markdown note."""
    title = (d.get("title") or d.get("caption") or d.get("source_url") or "untitled").strip()
    lines: List[str] = [f"# {title}", ""]
    meta = []
    if d.get("source_url"):
        meta.append(f"来源：{d['source_url']}")
    if d.get("author"):
        meta.append(f"UP 主：{d['author']}")
    if d.get("posted_at"):
        meta.append(f"发布：{d['posted_at']}")
    if d.get("duration_seconds"):
        read = d.get("read_seconds")
        whole = clock(d["duration_seconds"])
        meta.append(f"时长：{whole}" + (f"（读了前 {clock(read)}）" if read and float(read) + 1 < float(d["duration_seconds"]) else ""))
    parts = d.get("parts") or {}
    if parts.get("count"):
        meta.append(f"分P：第 {parts.get('current', 1)} P / 共 {parts['count']} P")
    lines += [" · ".join(meta), ""] if meta else []

    outline = d.get("outline") or []
    if outline:
        lines += ["## 大纲", ""]
        for sec in outline:
            lines.append(f"### [{clock(sec.get('start'))}–{clock(sec.get('end'))}] {(sec.get('title') or '').strip()}")
            for b in sec.get("summary") or []:
                lines.append(f"- {b}")
            if sec.get("quote"):
                lines.append(f"> {sec['quote']}")
            lines.append("")

    points = d.get("key_points") or []
    if points:
        support = {s.get("point_index"): s for s in (d.get("key_point_support") or []) if isinstance(s, dict)}
        lines += ["## 要点", ""]
        for i, p in enumerate(points):
            text = p if isinstance(p, str) else (p.get("text") or "")
            lines.append(f"- {text}")
            s = support.get(i) or {}
            # Only a quote the service found word for word in the video is shown as one.
            if s.get("verified") and s.get("quote"):
                at = f"[{clock(s['t'])}] " if s.get("t") is not None else ""
                lines.append(f"  > {at}{s['quote']}")
        lines.append("")

    if on_screen and d.get("on_screen"):
        lines += ["## 画面上的字", ""]
        lines += [f"- [≈{clock(o.get('t'))}] {o.get('text', '')}" for o in d["on_screen"]]
        lines.append("")

    transcript = d.get("transcript") or []
    if transcript:
        lines += ["## 逐字稿", ""]
        lines += [f"[{clock(seg.get('t'))}] {seg.get('text', '')}" for seg in transcript]
        lines.append("")
    elif d.get("transcript_count") is not None:
        # The keyless look: a summary, with counts in place of the text.
        lines += [
            "## 逐字稿",
            "",
            f"（没有 API Key 时只返回摘要：这条视频读出了 {d.get('transcript_count', 0)} 段逐字稿。"
            f"带 Key 再跑一次，就有完整逐字稿和大纲：{KEYS}）",
            "",
        ]
    return "\n".join(lines).rstrip() + "\n"


def file_name(d: Dict[str, Any], p: Optional[int] = None) -> str:
    title = re.sub(r'[\\/:*?"<>|\s]+', "_", (d.get("title") or "untitled")).strip("_")[:60] or "untitled"
    return (f"P{p:03d}-" if p else "") + title + ".md"


# ---- HTTP ------------------------------------------------------------------------

def http(method: str, path: str, body: Optional[dict], key: Optional[str]) -> Tuple[int, Dict[str, Any]]:
    headers = {"User-Agent": UA, "Accept": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode()
    req = urllib.request.Request(API + path, method=method, headers=headers, data=data)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read() or b"{}")
        except ValueError:
            return e.code, {"error": f"HTTP {e.code}"}
    except (urllib.error.URLError, TimeoutError) as e:
        raise Stop(7, f"连不上 {API}：{e}")


def refuse(status: int, body: Dict[str, Any]) -> Stop:
    """A non-200 answer, said the way the service said it."""
    msg = body.get("error") or f"HTTP {status}"
    if status == 401:
        why = "今天的免费摘要用完了" if body.get("error_code") == "trial_exhausted" else "这个 API Key 无效或已撤销"
        return Stop(3, f"{msg}\n{why}。创建 Key：{KEYS}")
    if status == 402:
        offer = body.get("offer_zh") or ""
        return Stop(4, msg + (f"\n{offer}" if offer else f"\n价格和充值：{PRICING}"))
    if status == 429:
        return Stop(6, msg)
    return Stop(5, msg)


def read_one(url: str, depth: str, key: Optional[str], *, send: Transport = http, wait: float = 900, sleep: Callable[[float], None] = time.sleep) -> Dict[str, Any]:
    """One link → its digest (with a key) or its summary (without). A long
    video answers 202 with a job to collect; it is collected, never resubmitted."""
    body = {"url": url, "format": "json", **({"depth": depth} if depth != "full" else {})}
    status, out = send("POST", "/api/v1/digest", body, key)
    deadline = time.time() + wait
    while status == 202:
        poll = out.get("poll") or (f"/api/v1/digest/{out['jobId']}" if out.get("jobId") else None)
        if not poll:
            raise Stop(5, "服务端在排队，但没有给出可以取结果的任务号")
        if time.time() > deadline:
            raise Stop(7, f"等了 {int(wait)} 秒还没读完。任务还在跑，稍后重新运行同一条命令即可（读过的不会再扣费）。")
        sleep(min(float(out.get("retryAfter") or 5), 15))
        status, out = send("GET", poll + ("&" if "?" in poll else "?") + "wait=20", None, key)
    if status != 200:
        raise refuse(status, out)
    return out


def read_parts(urls: List[str], depth: str, key: str, *, send: Transport = http, wait: float = 3600, sleep: Callable[[float], None] = time.sleep, log: Callable[[str], None] = lambda s: None) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """A batch of part links → (the batch summary, digests by link)."""
    status, batch = send("POST", "/api/v1/digest/batch", {"urls": urls, "depth": depth, "label": "bili2notes"}, key)
    if status not in (200, 202):
        raise refuse(status, batch)
    bid = batch["batch_id"]
    deadline = time.time() + wait
    while batch.get("status") != "done":
        if time.time() > deadline:
            raise Stop(7, f"批量任务 {bid} 还没读完。稍后可以用同一条命令再取（读过的分 P 不会再扣费）。")
        sleep(15)
        status, batch = send("GET", f"/api/v1/digest/batch/{bid}", None, key)
        if status != 200:
            raise refuse(status, batch)
        log(f"  … {batch.get('done', 0)}/{batch.get('total', len(urls))} 读完，{batch.get('failed', 0)} 条失败")
    status, full = send("GET", f"/api/v1/digest/batch/{bid}?include=digests", None, key)
    if status != 200:
        raise refuse(status, full)
    return full, (full.get("digests") or {})


# ---- the command -----------------------------------------------------------------

def confirm(question: str, *, assume_yes: bool, stdin=None, out=None) -> bool:
    stdin = stdin or sys.stdin
    out = out or sys.stderr
    if assume_yes:
        return True
    if not stdin.isatty():
        # Never spend credits on an unattended run that did not say --yes.
        print(question + "\n不是交互终端：加 --yes 才会开始。Not a terminal: pass --yes to start.", file=out)
        return False
    print(question + " [y/N] ", end="", file=out, flush=True)
    return stdin.readline().strip().lower() in ("y", "yes", "是")


def run(argv: Optional[List[str]] = None, *, send: Transport = http, stdin=None, stdout=None, stderr=None, sleep: Callable[[float], None] = time.sleep) -> int:
    stdout, stderr = stdout or sys.stdout, stderr or sys.stderr
    ap = argparse.ArgumentParser(prog="bili2notes", description="B站视频 → Markdown 笔记（大纲、要点、带时间的逐字稿）。Bilibili video → Markdown notes.")
    ap.add_argument("link", nargs="?", help="B站链接、b23.tv 短链、BV 号，或整段分享文字")
    ap.add_argument("-o", "--output", help="写到这个文件（默认打印到标准输出）")
    ap.add_argument("--depth", choices=DEPTHS, default="transcript", help="script=只要口播；transcript=口播+少量截帧（默认）；full=逐帧读画面文字")
    ap.add_argument("--parts", help="分P视频：再读这些分 P，例如 1-10、3,5,8、all（需要 Key，会先报出要花多少积分）")
    ap.add_argument("--out-dir", default="notes", help="--parts 时每 P 一个文件，放在这个目录（默认 notes/）")
    ap.add_argument("--batch-size", type=int, default=10, help="一批几条（免费账户 10，Dev 50，Studio 200）")
    ap.add_argument("--on-screen", action="store_true", help="笔记里加上画面上的字")
    ap.add_argument("--yes", action="store_true", help="--parts 时不再确认，直接开始")
    ap.add_argument("--from-json", help="不联网：把一份已保存的读取结果（API 返回的 JSON）渲染成笔记")
    args = ap.parse_args(argv)
    say = lambda s: print(s, file=stderr)

    try:
        if args.from_json:
            with open(args.from_json, encoding="utf-8") as f:
                note = render_note(json.load(f), on_screen=args.on_screen)
            return _write(note, args.output, stdout, say)
        if not args.link:
            ap.error("需要一条 B站 链接（或 --from-json）")
        key = (os.environ.get("LINKDIGEST_API_KEY") or "").strip() or None
        url = find_link(args.link)
        if args.parts and not key:
            raise Stop(3, f"--parts 需要 API Key（批量读取按积分计费）。创建 Key：{KEYS}")
        if not key:
            say("没有 LINKDIGEST_API_KEY：用免费的一次摘要（每天有限）。有 Key 才有完整逐字稿、大纲和分 P 批量。")
        d = read_one(url, args.depth, key, send=send, sleep=sleep)
        if key:
            left = d.get("credits_left")
            say(f"读完：{d.get('credits', 0)} 积分" + ("（缓存，不扣费）" if d.get("cached") else "") + (f"，账户还剩 {left}" if left is not None else ""))
        parts = d.get("parts") or {}
        if parts.get("count") and not args.parts:
            say(f"这个视频共 {parts['count']} P，这次读的是 P{parts.get('current', 1)}。要读其余分 P：加 --parts 1-10（或 all）。")
        if not args.parts:
            return _write(render_note(d, on_screen=args.on_screen), args.output, stdout, say)

        # ---- the other parts, as batches ----
        if not parts.get("items"):
            raise Stop(5, "这条视频不是分P视频（接口没有返回分 P 列表），--parts 用不上。")
        bvid = bvid_of(d.get("source_url"), url)
        if not bvid:
            raise Stop(5, "没有从结果里认出 BV 号，没法拼出各分 P 的链接。")
        current = int(parts.get("current") or 1)
        by_p = {int(it["p"]): it for it in parts["items"]}
        wanted = parse_parts(args.parts, int(parts["count"]))
        todo = [p for p in wanted if p != current and p in by_p]
        os.makedirs(args.out_dir, exist_ok=True)
        written = []
        if current in wanted:
            path = os.path.join(args.out_dir, file_name(d, current))
            with open(path, "w", encoding="utf-8") as f:
                f.write(render_note(d, on_screen=args.on_screen))
            written.append(path)
        if todo:
            total = sum(estimate_credits(by_p[p].get("seconds") or 0, args.depth) for p in todo)
            say(f"\n要读 {len(todo)} 个分 P（{args.depth}）：")
            for p in todo[:30]:
                it = by_p[p]
                say(f"  P{p:<3} {clock(it.get('seconds')):>8}  约 {estimate_credits(it.get('seconds') or 0, args.depth):>3} 积分  {it.get('title', '')}")
            if len(todo) > 30:
                say(f"  … 另外 {len(todo) - 30} 个")
            say(f"合计最多约 {total} 积分（别人读过的分 P 不扣；以实际扣费为准）。价格：{PRICING}")
            if not confirm("开始吗？", assume_yes=args.yes, stdin=stdin, out=stderr):
                raise Stop(6, "没有开始，没有扣费。")
            size = max(1, args.batch_size)
            spent = failed = 0
            for i in range(0, len(todo), size):
                chunk = todo[i : i + size]
                links = {part_link(bvid, p): p for p in chunk}
                full, digests = read_parts(list(links), args.depth, key, send=send, sleep=sleep, log=say)
                spent += int(full.get("credits_total") or 0)
                for item in full.get("items") or []:
                    if item.get("status") == "error":
                        failed += 1
                        say(f"  没读成 {item.get('url')}: {item.get('error_code') or ''} {item.get('error') or ''}".rstrip())
                for link, dg in digests.items():
                    if not isinstance(dg, dict):
                        continue
                    p = links.get(link) or int(((dg.get("parts") or {}).get("current")) or 0) or None
                    path = os.path.join(args.out_dir, file_name(dg, p))
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(render_note(dg, on_screen=args.on_screen))
                    written.append(path)
            say(f"\n批量读完：实际扣了 {spent} 积分" + (f"，{failed} 个分 P 没读成（没扣费）" if failed else ""))
        say(f"写了 {len(written)} 个文件到 {args.out_dir}/")
        for path in written:
            print(path, file=stdout)
        return 0
    except Stop as e:
        say(str(e))
        return e.code


def _write(note: str, output: Optional[str], stdout, say) -> int:
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(note)
        say(f"写到 {output}")
    else:
        stdout.write(note)
    return 0


if __name__ == "__main__":
    sys.exit(run())
