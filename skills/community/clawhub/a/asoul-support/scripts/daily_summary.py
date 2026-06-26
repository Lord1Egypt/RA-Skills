#!/usr/bin/env python3
"""
A-SOUL 每日挂机活动汇总
读取过去24小时的 asoul_activity.jsonl，生成一份总结报告。
"""

import json
import sys
import time
from pathlib import Path
from typing import List, Dict

_LOG_FILE = Path.home() / ".openclaw" / "logs" / "asoul_activity.jsonl"


def load_recent(hours: int = 24) -> List[dict]:
    if not _LOG_FILE.exists():
        return []
    cutoff = int(time.time()) - hours * 3600
    records = []
    with open(_LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
                if r.get("ts", 0) >= cutoff:
                    records.append(r)
            except Exception:
                continue
    return records


def fmt_ts(ts: int) -> str:
    return time.strftime("%H:%M", time.localtime(ts))


def fmt_date(ts: int) -> str:
    return time.strftime("%m/%d", time.localtime(ts))


def build_summary(records: List[dict]) -> str:
    checks = [r for r in records if r["type"] == "check"]
    starts = [r for r in records if r["type"] == "watch_start"]
    ends = {(r["member"], r["ts"]): r for r in records if r["type"] == "watch_end"}

    total_checks = len(checks)
    live_detections: Dict[str, List[dict]] = {}
    for c in checks:
        for m in c.get("live", []):
            name = m["name"]
            live_detections.setdefault(name, []).append({"ts": c["ts"], "title": m.get("title", "")})

    # 匹配 watch_start 和对应的 watch_end
    watch_sessions = []
    for s in starts:
        # 找最近的 watch_end (同成员，时间在 start 之后)
        best_end = None
        for (member, end_ts), end_r in ends.items():
            if member == s["member"] and end_ts > s["ts"]:
                if best_end is None or end_ts < best_end["ts"]:
                    best_end = {**end_r, "ts": end_ts}
        watch_sessions.append({"start": s, "end": best_end})

    total_watch_min = sum(
        s["end"]["minutes"] for s in watch_sessions if s["end"]
    )

    lines = [
        f"📊 **A-SOUL 过去24小时挂机日报**",
        f"",
        f"🔍 检测次数：**{total_checks}次**（每30分钟一次）",
    ]

    if not live_detections and not watch_sessions:
        lines.append("💤 过去24小时内无人开播")
    else:
        lines.append("")
        lines.append("📺 **开播检测记录：**")
        if live_detections:
            for name, detections in live_detections.items():
                first_ts = detections[0]["ts"]
                title = detections[0].get("title", "")
                title_str = f"「{title}」" if title else ""
                lines.append(f"  🔴 {name} — 首次检测到 {fmt_ts(first_ts)} {title_str}")
        else:
            lines.append("  💤 无人开播")

        if watch_sessions:
            lines.append("")
            lines.append("⏱ **挂机记录：**")
            for s in watch_sessions:
                start_r = s["start"]
                end_r = s["end"]
                start_str = fmt_ts(start_r["ts"])
                if end_r:
                    end_str = fmt_ts(end_r["ts"])
                    dur = end_r["minutes"]
                    lines.append(f"  ✅ {start_r['member']} — {start_str} 开始挂机，{end_str} 下播，共 **{dur}分钟**")
                else:
                    lines.append(f"  🔄 {start_r['member']} — {start_str} 开始挂机（仍在进行中）")

        lines.append("")
        if total_watch_min >= 60:
            h, m = divmod(total_watch_min, 60)
            dur_str = f"{h}小时{m}分钟" if m else f"{h}小时"
        else:
            dur_str = f"{total_watch_min}分钟"
        lines.append(f"🕐 **总挂机时长：{dur_str}**")

    return "\n".join(lines)


def main():
    records = load_recent(24)
    print(build_summary(records))


if __name__ == "__main__":
    main()
