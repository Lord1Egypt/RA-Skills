#!/usr/bin/env python3
"""
calendar.py - Bid calendar & opening-countdown reminder (BidHunter v1.5, A2).

Reads qualification output (qual_*.jsonl) and:
  - extracts opening/deadline dates from titles when present
  - prints a calendar view grouped by deadline (next N days)
  - prints countdown to the nearest deadline
  - with --remind: pushes a DingTalk/WeCom/email reminder for items
    whose deadline is within --urgent-window hours (default 48h)

Note: most platforms' list API lacks a deadline field (see SKILL.md 已知坑点),
so deadlines are best-effort extracted from title text. Items without a
detectable deadline are listed under "待核实截止日".

Usage:
  python3 calendar.py <qual_file.jsonl> [--days 7] [--remind] [--urgent-window 48]
  python3 calendar.py <qual_file.jsonl> --today        # only items due today/overdue
"""
import json
import sys
import os
import re
import argparse
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", file=sys.stderr)


def _extract_deadline(title):
    """Extract an opening/deadline date from title text. Returns 'YYYY-MM-DD' or None."""
    if not title:
        return None
    # explicit ISO date near 开标/截止/投标截止
    for kw in ("开标", "截止", "投标截止", "递交截止", "响应截止"):
        m = re.search(kw + r"\D*?(\d{4})[-/年.](\d{1,2})[-/月.](\d{1,2})", title)
        if m:
            try:
                return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"
            except Exception:
                pass
    # X月X日 (current/next year implied)
    m = re.search(r"(开标|截止|投标截止)\D*?(\d{1,2})月(\d{1,2})日", title)
    if m:
        try:
            month, day = int(m.group(2)), int(m.group(3))
            now = datetime.now()
            year = now.year
            if (month, day) < (now.month, now.day):
                year += 1
            return f"{year:04d}-{month:02d}-{day:02d}"
        except Exception:
            pass
    return None


def load_qual(path):
    items = []
    if not os.path.exists(path):
        return items
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return items


def build_calendar(items, days=7):
    """Return dict: date_str -> list of items (investable/needs_review with deadline)."""
    today = datetime.now().date()
    horizon = today + timedelta(days=days)
    cal = {}
    no_deadline = []
    for it in items:
        v = it.get("verdict", "")
        if v not in ("investable", "needs_review"):
            continue
        dl = _extract_deadline(it.get("title", ""))
        if not dl:
            no_deadline.append(it)
            continue
        try:
            d = datetime.strptime(dl, "%Y-%m-%d").date()
        except Exception:
            no_deadline.append(it)
            continue
        if today <= d <= horizon:
            cal.setdefault(dl, []).append(it)
    return cal, no_deadline


def render(cal, no_deadline, days):
    today = datetime.now().date()
    lines = []
    lines.append(f"【投标日历 · 未来 {days} 天】生成于 {datetime.now():%Y-%m-%d %H:%M}")
    lines.append("=" * 48)
    if not cal:
        lines.append("（未来窗口内未解析到明确开标/截止日）")
    for dl in sorted(cal.keys()):
        d = datetime.strptime(dl, "%Y-%m-%d").date()
        delta = (d - today).days
        tag = "今天" if delta == 0 else (f"{delta}天后" if delta > 0 else f"已过期{-delta}天")
        lines.append(f"\n📅 {dl}（{tag}）")
        for it in cal[dl]:
            score = it.get("score", 0)
            lvl = it.get("score_level", "")
            lines.append(f"  · [{lvl} {score}] {it.get('title','')[:40]}")
            if it.get("url"):
                lines.append(f"    {it['url']}")
    if no_deadline:
        lines.append(f"\n⏳ 待核实截止日（{len(no_deadline)} 条，标题未含明确日期）：")
        for it in no_deadline[:15]:
            lines.append(f"  · {it.get('title','')[:42]}")
        if len(no_deadline) > 15:
            lines.append(f"  · …（其余 {len(no_deadline)-15} 条）")
    lines.append("\n" + "=" * 48)
    return "\n".join(lines)


def urgent_items(items, window_hours=48):
    now = datetime.now()
    out = []
    for it in items:
        v = it.get("verdict", "")
        if v not in ("investable", "needs_review"):
            continue
        dl = _extract_deadline(it.get("title", ""))
        if not dl:
            continue
        try:
            d = datetime.strptime(dl + " 18:00", "%Y-%m-%d %H:%M")
        except Exception:
            continue
        hours = (d - now).total_seconds() / 3600.0
        if 0 <= hours <= window_hours:
            out.append((hours, it))
    out.sort(key=lambda x: x[0])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("qual_file")
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--today", action="store_true", help="仅显示今天/过期")
    ap.add_argument("--remind", action="store_true", help="对临近截止项推送提醒")
    ap.add_argument("--urgent-window", type=int, default=48, help="提醒窗口(小时)")
    args = ap.parse_args()

    items = load_qual(args.qual_file)
    log(f"Loaded {len(items)} items from {args.qual_file}")

    if args.today:
        now = datetime.now().date()
        today_items = [it for it in items
                       if it.get("verdict") in ("investable", "needs_review")
                       and _extract_deadline(it.get("title", "")) == now.strftime("%Y-%m-%d")]
        print(render({now.strftime("%Y-%m-%d"): today_items}, [], 0))
        return

    cal, no_deadline = build_calendar(items, args.days)
    print(render(cal, no_deadline, args.days))

    if args.remind:
        urg = urgent_items(items, args.urgent_window)
        if not urg:
            log("No items within urgent window; nothing to push.")
            return
        cfg = os.path.expanduser("~/.config/bidhunter/push.json")
        if not os.path.exists(cfg):
            log("Push not configured; skipping reminder (run config_wizard.py).")
            return
        sys.path.insert(0, SCRIPT_DIR)
        try:
            from push_manager import PushManager
        except Exception as e:
            log(f"Cannot import push_manager: {e}")
            return
        pm = PushManager(cfg)
        body = ["【开标倒计时提醒】以下标讯临近截止，请尽快决策："]
        for hours, it in urg:
            body.append(f"  · 剩{hours:.0f}h | {it.get('title','')[:40]} | {it.get('url','')}")
        text = "\n".join(body)
        ok, msg = pm.send_one(text, title="开标倒计时提醒")
        log(f"Reminder push: ok={ok} msg={msg}")


if __name__ == "__main__":
    main()
