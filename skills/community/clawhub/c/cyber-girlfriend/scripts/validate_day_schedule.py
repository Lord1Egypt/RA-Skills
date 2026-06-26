#!/usr/bin/env python3
"""Validate the companion day-schedule Markdown artifact."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


EVENT_HEADING_RE = re.compile(r"^###\s+([0-2]\d:[0-5]\d)\s+-\s+(.+?)\s*$")
INTERNAL_TOKENS = ["脚本", "JSON", "cron", "系统", "模型", "工具", "payload", "contract", "debug", "Step", "步骤", "工具调用"]
PRIVATE_PATTERNS = [
    (re.compile(r"\b\d{10,}\b"), "long numeric identifier"),
    (re.compile(r"[A-Za-z0-9_-]{16,}@im\.[A-Za-z0-9_-]+\b", re.IGNORECASE), "private IM target"),
    (re.compile(r"/" r"Users/[^\\s\"'`]+"), "local user path"),
    (re.compile(r"/" r"home/[^\\s\"'`]+"), "local user path"),
    (re.compile(r"\b(?:owner_session_key|accountId|channel_id|session_key|USER\.md)\b", re.IGNORECASE), "private routing field"),
]
REQUIRED_EVENT_FIELDS = ["必定发生", "执行时间", "场景", "正在做什么", "情绪/状态", "可自然提到", "用户互动入口", "媒体信息", "不要写成"]
VAGUE_EVENT_PHRASES = [
    "处理小事",
    "处理事情",
    "学习或杂事",
    "必要安排",
    "吃点东西",
    "摸鱼",
    "轻娱乐内容",
    "看一点轻内容",
    "收拾东西",
    "准备收尾",
    "慢慢结束",
]
DRAMATIC_PHRASES = [
    "彻底崩溃",
    "崩溃到",
    "哭到停不下来",
    "绝望",
    "被抛弃",
    "严重冲突",
    "冲突到失控",
    "吵到失控",
    "病倒",
    "晕倒",
]
MEDIA_KEYWORDS = ["拍照", "照片", "相册", "修图", "自拍", "唱歌", "哼唱", "录音", "语音", "视频", "镜头"]
EXPLICIT_SELFIE_CONTEXT_TOKENS = ["镜子", "对镜", "前置", "举着手机", "手持手机", "自拍杆", "手机前置"]
EVENT_TYPE_KEYWORDS = [
    ("media_photo", ["拍照", "照片", "相册", "修图", "自拍", "镜头"]),
    ("media_audio", ["唱歌", "哼唱", "录音", "语音"]),
    ("tidying", ["清包", "小票", "整理", "收拾", "归位", "桌面", "文件夹", "擦"]),
    ("food_drink", ["便利店", "饭团", "冰美式", "冰饮", "奶茶", "冷柜", "午饭", "晚饭"]),
    ("study", ["高数", "错题", "图书馆", "课表", "展示", "课堂", "复习", "作业"]),
    ("entertainment", ["综艺", "舞台", "游戏", "版本", "前瞻", "兑换码", "追剧"]),
    ("shopping", ["商场", "买", "逛街", "小夹子"]),
    ("weather_wait", ["短雨", "阵雨", "等雨", "雨小", "地面反光"]),
]


def fail(message: str):
    raise SystemExit(f"day-schedule validation failed: {message}")


def clean_text(value) -> str:
    if value is None:
        return ""
    return str(value).strip()


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing config file: {path}")
    except json.JSONDecodeError as exc:
        fail(f"{path}: invalid JSON: {exc}")


def parse_hhmm(value: str) -> int:
    text = clean_text(value)
    if not re.match(r"^\d{1,2}:?\d{2}$", text):
        fail(f"invalid quiet hour value: {value}")
    if ":" in text:
        hour, minute = text.split(":", 1)
    else:
        hour, minute = text[:-2], text[-2:]
    hour_i = int(hour)
    minute_i = int(minute)
    if not (0 <= hour_i <= 23 and 0 <= minute_i <= 59):
        fail(f"invalid quiet hour value: {value}")
    return hour_i * 100 + minute_i


def is_in_quiet_hours(hhmm: int, quiet_start: int, quiet_end: int) -> bool:
    if quiet_start == quiet_end:
        return False
    if quiet_start < quiet_end:
        return quiet_start <= hhmm < quiet_end
    return hhmm >= quiet_start or hhmm < quiet_end


def resolve_quiet_hours(config: dict) -> tuple[int, int]:
    schedule = config.get("schedule", {}) if isinstance(config.get("schedule"), dict) else {}
    start = schedule.get("quiet_hours_start", "00:00")
    end = schedule.get("quiet_hours_end", "00:00")
    return parse_hhmm(start), parse_hhmm(end)


def parse_args():
    parser = argparse.ArgumentParser(description="Validate a cyber-girlfriend day-schedule Markdown artifact.")
    parser.add_argument("--config", required=True, help="Path to config.local.json")
    parser.add_argument("--path", default="state/day-schedule.md", help="Path to day-schedule.md")
    parser.add_argument("--min-events", type=int, default=3)
    parser.add_argument("--max-events", type=int, default=5)
    return parser.parse_args()


def parse_event_field(line: str) -> tuple[str, str] | None:
    match = re.match(r"^-\s*([^：:]+)[：:]\s*(.*)$", line)
    if not match:
        return None
    return match.group(1).strip(), match.group(2).strip()


def parse_duration_minutes(value: str) -> int:
    text = clean_text(value)
    if not text:
        return 0
    hour_match = re.search(r"(\d+)\s*(?:小时|h|hour)", text, flags=re.IGNORECASE)
    minute_match = re.search(r"(\d+)\s*(?:分钟|min|m)", text, flags=re.IGNORECASE)
    total = 0
    if hour_match:
        total += int(hour_match.group(1)) * 60
    if minute_match:
        total += int(minute_match.group(1))
    if total:
        return total
    if re.fullmatch(r"\d{1,3}", text):
        return int(text)
    return 0


def parse_events(text: str):
    events = []
    current = None
    section = ""
    for line_no, line in enumerate(text.splitlines(), 1):
        heading2 = re.match(r"^##\s+(?:(\d+)\.\s+)?(.+?)\s*$", line)
        if heading2:
            section = heading2.group(2).strip()
            current = None
            continue
        heading = EVENT_HEADING_RE.match(line)
        if heading:
            current = {
                "line": line_no,
                "time": heading.group(1),
                "title": heading.group(2).strip(),
                "fields": {},
            }
            events.append(current)
            continue
        if current is None:
            continue
        field = parse_event_field(line)
        if field:
            key, value = field
            current["fields"][key] = value
    return events


def hhmm_to_int(value: str) -> int:
    hour, minute = value.split(":", 1)
    return int(hour) * 100 + int(minute)


def hhmm_to_minutes(value: str) -> int:
    hour, minute = value.split(":", 1)
    return int(hour) * 60 + int(minute)


def hhmm_int_to_minutes(value: int) -> int:
    return (value // 100) * 60 + (value % 100)


def intervals_overlap(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return left[0] < right[1] and right[0] < left[1]


def contains_hourly_presence_tick(start: int, end: int) -> bool:
    first_tick = ((start + 59) // 60) * 60
    return start <= first_tick < end


def quiet_intervals(quiet_start: int, quiet_end: int) -> list[tuple[int, int]]:
    start = hhmm_int_to_minutes(quiet_start)
    end = hhmm_int_to_minutes(quiet_end)
    if start == end:
        return []
    if start < end:
        return [(start, end), (start + 1440, end + 1440)]
    return [(start, 1440), (0, end), (start + 1440, 2880)]


def event_text(event: dict) -> str:
    fields = event.get("fields", {})
    return " ".join(
        [
            clean_text(event.get("title")),
            clean_text(fields.get("场景")),
            clean_text(fields.get("正在做什么")),
            clean_text(fields.get("可自然提到")),
        ]
    )


def infer_event_type(event: dict) -> str:
    text = event_text(event)
    for event_type, keywords in EVENT_TYPE_KEYWORDS:
        if any(keyword in text for keyword in keywords):
            return event_type
    return ""


def validate_event_type_uniqueness(events):
    seen = {}
    for event in events:
        event_type = infer_event_type(event)
        if not event_type:
            continue
        if event_type in seen:
            fail(f"duplicate event type {event_type}: {seen[event_type]} and {event['time']}")
        seen[event_type] = event["time"]


def validate_default_life_photo_wording(time_text: str, title: str, fields: dict, media_info: str):
    if "生活照片" not in clean_text(title):
        return
    action = clean_text(fields.get("正在做什么"))
    if "自拍" not in media_info and "自拍" not in action:
        return
    context = " ".join([clean_text(fields.get("场景")), action, media_info])
    if any(token in context for token in EXPLICIT_SELFIE_CONTEXT_TOKENS):
        return
    fail(f"event {time_text} default life-photo event should not force 自拍 wording")


def validate_media_info(time_text: str, title: str, fields: dict):
    text = " ".join([fields.get("正在做什么", ""), fields.get("可自然提到", ""), fields.get("场景", "")])
    media_info = clean_text(fields.get("媒体信息"))
    if any(keyword in text for keyword in MEDIA_KEYWORDS) and not media_info:
        fail(f"event {time_text} involves media-like content but field 媒体信息 is empty")
    if media_info and len(media_info) < 10:
        fail(f"event {time_text} field 媒体信息 is too vague: {media_info}")
    if media_info:
        validate_default_life_photo_wording(time_text, title, fields, media_info)


def validate_events(events, quiet_start: int, quiet_end: int, min_events: int, max_events: int):
    daily_events = [event for event in events if event.get("fields", {}).get("必定发生") != "是"]
    if not (min_events <= len(daily_events) <= max_events):
        fail(f"daily event count must be {min_events}-{max_events}, got {len(daily_events)}")
    seen_times = set()
    event_windows = []
    for event in events:
        time_text = event["time"]
        if time_text in seen_times:
            fail(f"duplicate event time: {time_text}")
        seen_times.add(time_text)
        event_time = hhmm_to_int(time_text)
        if is_in_quiet_hours(event_time, quiet_start, quiet_end):
            fail(f"event {time_text} falls within quiet hours")
        fields = event["fields"]
        missing = [field for field in REQUIRED_EVENT_FIELDS if field not in fields]
        if missing:
            fail(f"event {time_text} missing fields: {missing}")
        if fields.get("必定发生") not in {"是", "否"}:
            fail(f"event {time_text} field 必定发生 must be 是 or 否")
        for field in REQUIRED_EVENT_FIELDS:
            if field == "必定发生":
                continue
            if field in {"用户互动入口", "媒体信息"}:
                continue
            value = fields.get(field, "").strip()
            if not value:
                fail(f"event {time_text} field {field} must not be empty")
            if field == "执行时间":
                duration = parse_duration_minutes(value)
                if not (5 <= duration <= 360):
                    fail(f"event {time_text} field 执行时间 must be 5-360 minutes: {value}")
                event_windows.append((time_text, hhmm_to_minutes(time_text), duration))
            if field in {"正在做什么", "可自然提到"}:
                validate_specific_event_text(time_text, field, value)
        validate_media_info(time_text, event["title"], fields)
    validate_event_type_uniqueness(events)
    validate_time_windows(event_windows, quiet_start, quiet_end)


def validate_specific_event_text(time_text: str, field: str, value: str):
    for phrase in VAGUE_EVENT_PHRASES:
        if phrase in value and len(value) < 24:
            fail(f"event {time_text} field {field} is too vague: {value}")
    for phrase in DRAMATIC_PHRASES:
        if phrase in value:
            fail(f"event {time_text} field {field} is too dramatic: {value}")


def validate_time_windows(event_windows: list[tuple[str, int, int]], quiet_start: int, quiet_end: int):
    quiet = quiet_intervals(quiet_start, quiet_end)
    intervals = []
    for time_text, start, duration in event_windows:
        interval = (start, start + duration)
        if not contains_hourly_presence_tick(*interval):
            fail(f"event {time_text} window must include an hourly presence tick")
        for quiet_interval in quiet:
            if intervals_overlap(interval, quiet_interval):
                fail(f"event {time_text} duration overlaps quiet hours")
        intervals.append((time_text, interval))
    for idx, (left_time, left) in enumerate(intervals):
        for right_time, right in intervals[idx + 1 :]:
            shifted_right = (right[0] + 1440, right[1] + 1440)
            if intervals_overlap(left, right) or intervals_overlap(left, shifted_right):
                fail(f"event windows overlap: {left_time} and {right_time}")


def validate_internal_tokens(text: str):
    for token in INTERNAL_TOKENS:
        if token in text:
            fail(f"contains internal token: {token}")


def validate_private_content(text: str):
    for regex, label in PRIVATE_PATTERNS:
        if regex.search(text):
            fail(f"contains private content: {label}")


def validate_markdown_leakage(text: str):
    if "```" in text:
        fail("contains code fence")
    if re.search(r"^\s*(?:Step\s*\d+|步骤\s*\d+|第[一二三四五六七八九十]+步)[：:]", text, re.MULTILINE):
        fail("contains internal step label")


def generated_content_only(text: str) -> str:
    marker = "\n## 生成约束"
    if marker not in text:
        return text
    return text.split(marker, 1)[0]


def main():
    args = parse_args()
    config_path = Path(args.config).expanduser()
    schedule_path = Path(args.path).expanduser()
    config = load_json(config_path)
    try:
        text = schedule_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"missing day-schedule file: {schedule_path}")

    generated_text = generated_content_only(text)
    validate_markdown_leakage(generated_text)
    validate_internal_tokens(generated_text)
    validate_private_content(generated_text)
    quiet_start, quiet_end = resolve_quiet_hours(config)
    events = parse_events(text)
    validate_events(events, quiet_start, quiet_end, args.min_events, args.max_events)
    print(
        json.dumps(
            {
                "status": "ok",
                "path": str(schedule_path),
                "event_count": len(events),
                "daily_event_count": len([event for event in events if event.get("fields", {}).get("必定发生") != "是"]),
                "required_event_count": len([event for event in events if event.get("fields", {}).get("必定发生") == "是"]),
                "first_event": events[0]["time"],
                "last_event": events[-1]["time"],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        fail(str(exc))
