#!/usr/bin/env python3
import argparse
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

FORMATS = [
    "%Y-%m-%d %H:%M",
    "%Y/%m/%d %H:%M",
    "%Y.%m.%d %H:%M",
    "%Y年%m月%d日 %H:%M",
    "%Y年%m月%d日%H:%M",
    "%Y-%m-%dT%H:%M",
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%Y.%m.%d",
    "%Y年%m月%d日",
]

KEYWORDS = ["复诊", "复查", "检查", "取药", "换药", "拆线", "抽血", "验血", "拍片", "输液"]


def normalize(text: str) -> str:
    text = text.strip()
    text = text.replace("上午", " ").replace("下午", " ")
    text = re.sub(r"\s+", " ", text)
    return text


def parse_dt(text: str, default_time: str = "09:00") -> datetime:
    raw = normalize(text)
    for fmt in FORMATS:
        try:
            dt = datetime.strptime(raw, fmt)
            if "%H" not in fmt:
                hh, mm = map(int, default_time.split(":"))
                dt = dt.replace(hour=hh, minute=mm)
            return dt
        except ValueError:
            continue
    raise ValueError(f"Unsupported datetime format: {text}")


def parse_cn_num(text: str) -> Optional[int]:
    mapping = {
        "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5,
        "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
    }
    if text.isdigit():
        return int(text)
    if text in mapping:
        return mapping[text]
    if len(text) == 2 and text[0] == "十" and text[1] in mapping:
        return 10 + mapping[text[1]]
    if len(text) == 2 and text[1] == "十" and text[0] in mapping:
        return mapping[text[0]] * 10
    if len(text) == 3 and text[1] == "十" and text[0] in mapping and text[2] in mapping:
        return mapping[text[0]] * 10 + mapping[text[2]]
    return None


def parse_frequency(text: str) -> Tuple[Optional[int], Optional[int], str]:
    t = text.lower().replace("每隔", "每")
    m = re.search(r"(?:一天|每日|每天)(\d+|一|二|两|三|四)次", t)
    if m:
        n = parse_cn_num(m.group(1))
        return n, None, f"每天{n}次"
    if any(k in t for k in ["一天一次", "每日一次", "每天一次", "qd"]):
        return 1, None, "每天1次"
    if any(k in t for k in ["一天两次", "每日两次", "每天两次", "bid"]):
        return 2, None, "每天2次"
    if any(k in t for k in ["一天三次", "每日三次", "每天三次", "tid"]):
        return 3, None, "每天3次"
    m = re.search(r"每(\d{1,2})小时(?:一次)?", t)
    if m:
        hours = int(m.group(1))
        return None, hours, f"每{hours}小时1次"
    return None, None, "未识别频次"


def parse_duration_days(text: str) -> int:
    t = text.lower()
    if "一周" in t or "1周" in t:
        return 7
    if "两周" in t or "2周" in t:
        return 14
    if "三周" in t or "3周" in t:
        return 21
    m = re.search(r"(?:吃|服|用|连用)?(\d+|一|二|两|三|四|五|六|七|八|九|十+)天", t)
    if m:
        return parse_cn_num(m.group(1)) or 1
    m = re.search(r"(?:吃|服|用|连用)?(\d+|一|二|两|三)周", t)
    if m:
        return (parse_cn_num(m.group(1)) or 1) * 7
    return 7


def parse_dose(text: str) -> str:
    patterns = [
        r"一次[^，。；;\s]+",
        r"每次[^，。；;\s]+",
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return m.group(0)
    return "按医嘱"


def parse_med_name(text: str) -> str:
    # 优先取首段中非频次描述的内容
    first = re.split(r"[，。,；;]", text.strip())[0].strip()
    if first and not any(x in first for x in ["一天", "每天", "每日", "每", "一次", "一周", "天"]):
        return first
    m = re.search(r"([\u4e00-\u9fa5A-Za-z0-9\-]{2,20})(?:片|粒|胶囊|口服液|注射液)?[，, ]*(?:一天|每天|每日|每\d+小时)", text)
    if m:
        return m.group(1)
    return "用药提醒"


def parse_start_dt(text: str, explicit_start: Optional[str], times_per_day: Optional[int], interval_hours: Optional[int]) -> datetime:
    if explicit_start:
        return parse_dt(explicit_start, default_time="08:00")

    patterns = [
        r"从(\d{4}[-/.]\d{1,2}[-/.]\d{1,2}(?:\s+\d{1,2}:\d{2})?)开始",
        r"从(\d{4}年\d{1,2}月\d{1,2}日(?:\s*\d{1,2}:\d{2})?)开始",
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return parse_dt(m.group(1), default_time="08:00")

    now = datetime.now()
    if interval_hours:
        return now.replace(minute=0, second=0, microsecond=0)
    if times_per_day == 1:
        return now.replace(hour=8, minute=0, second=0, microsecond=0)
    if times_per_day == 2:
        return now.replace(hour=8, minute=0, second=0, microsecond=0)
    if times_per_day == 3:
        return now.replace(hour=8, minute=0, second=0, microsecond=0)
    return now.replace(hour=9, minute=0, second=0, microsecond=0)


def daily_time_slots(times_per_day: int) -> List[Tuple[int, int]]:
    if times_per_day == 1:
        return [(8, 0)]
    if times_per_day == 2:
        return [(8, 0), (20, 0)]
    if times_per_day == 3:
        return [(8, 0), (14, 0), (20, 0)]
    if times_per_day == 4:
        return [(6, 0), (12, 0), (18, 0), (22, 0)]
    step = max(1, round(24 / times_per_day))
    slots = []
    h = 8
    for _ in range(times_per_day):
        slots.append((h % 24, 0))
        h += step
    return slots


def build_appointment_reminders(appointment: str) -> Dict:
    dt = parse_dt(appointment)
    reminders = [
        ("T-12h", dt - timedelta(hours=12)),
        ("T-6h", dt - timedelta(hours=6)),
        ("T-2h", dt - timedelta(hours=2)),
    ]
    return {
        "appointment": dt.strftime("%Y-%m-%d %H:%M"),
        "reminders": [
            {"label": label, "time": when.strftime("%Y-%m-%d %H:%M"), "title": f"就诊提醒 {label}"}
            for label, when in reminders
        ],
    }


def build_medication_reminders(text: str, explicit_start: Optional[str] = None) -> Dict:
    times_per_day, interval_hours, freq_text = parse_frequency(text)
    duration_days = parse_duration_days(text)
    dose = parse_dose(text)
    med_name = parse_med_name(text)
    start_dt = parse_start_dt(text, explicit_start, times_per_day, interval_hours)

    reminders = []
    if interval_hours:
        total_count = max(1, int((24 * duration_days) / interval_hours))
        current = start_dt
        for idx in range(total_count):
            reminders.append({
                "index": idx + 1,
                "time": current.strftime("%Y-%m-%d %H:%M"),
                "title": f"{med_name} 用药提醒",
                "content": f"{dose}，频次：{freq_text}",
            })
            current += timedelta(hours=interval_hours)
    else:
        per_day = times_per_day or 1
        slots = daily_time_slots(per_day)
        base_date = start_dt.date()
        for d in range(duration_days):
            for hh, mm in slots:
                current = datetime.combine(base_date + timedelta(days=d), datetime.min.time()).replace(hour=hh, minute=mm)
                reminders.append({
                    "index": len(reminders) + 1,
                    "time": current.strftime("%Y-%m-%d %H:%M"),
                    "title": f"{med_name} 用药提醒",
                    "content": f"{dose}，频次：{freq_text}",
                })

    return {
        "medication_name": med_name,
        "frequency": freq_text,
        "dose": dose,
        "duration_days": duration_days,
        "start_time": start_dt.strftime("%Y-%m-%d %H:%M"),
        "reminders": reminders,
    }


def parse_extra_item(raw: str) -> Dict:
    if "|" not in raw:
        raise ValueError("extra reminder format must be 标题|时间，例如 复诊|2026-03-27 10:00")
    title, when = raw.split("|", 1)
    dt = parse_dt(when.strip(), default_time="09:00")
    return {
        "title": title.strip(),
        "time": dt.strftime("%Y-%m-%d %H:%M"),
    }


def extract_extra_from_text(text: str) -> List[Dict]:
    results = []
    date_patterns = [
        r"(\d{4}[-/.]\d{1,2}[-/.]\d{1,2}(?:\s+\d{1,2}:\d{2})?)",
        r"(\d{4}年\d{1,2}月\d{1,2}日(?:\s*\d{1,2}:\d{2})?)",
        r"(\d{1,2}月\d{1,2}日(?:\s*\d{1,2}:\d{2})?)",
    ]
    seen = set()
    current_year = datetime.now().year
    segments = [seg.strip() for seg in re.split(r"[，,。；;\n]", text) if seg.strip()]
    for seg in segments:
        label = None
        for kw in KEYWORDS:
            if kw in seg:
                label = kw
                break
        if not label:
            continue
        raw_dt = None
        for ptn in date_patterns:
            m = re.search(ptn, seg)
            if m:
                raw_dt = m.group(1)
                break
        if not raw_dt:
            continue
        candidate = raw_dt
        if re.match(r"^\d{1,2}月\d{1,2}日", raw_dt):
            candidate = f"{current_year}年{raw_dt}"
        try:
            dt = parse_dt(candidate, default_time="09:00")
        except ValueError:
            continue
        key = (label, dt.strftime("%Y-%m-%d %H:%M"))
        if key in seen:
            continue
        seen.add(key)
        results.append({"title": label, "time": dt.strftime("%Y-%m-%d %H:%M")})
    return results


def build_calendar_tasks(appointment_block: Optional[Dict], medication_block: Optional[Dict], extra_items: List[Dict]) -> List[Dict]:
    tasks = []
    if appointment_block:
        for item in appointment_block["reminders"]:
            tasks.append({
                "type": "appointment",
                "title": item["title"],
                "time": item["time"],
                "content": f"本次就诊时间：{appointment_block['appointment']}",
            })
    if medication_block:
        for item in medication_block["reminders"]:
            tasks.append({
                "type": "medication",
                "title": item["title"],
                "time": item["time"],
                "content": item["content"],
            })
    for item in extra_items:
        tasks.append({
            "type": "followup",
            "title": item["title"],
            "time": item["time"],
            "content": f"{item['title']} 提醒",
        })
    tasks.sort(key=lambda x: x["time"])
    return tasks


def main() -> int:
    p = argparse.ArgumentParser(description="Generate reminders for appointments, medications and follow-up tasks")
    p.add_argument("--appointment", help="Appointment datetime, e.g. 2026-03-20 14:30")
    p.add_argument("--medication-text", help="Medication instruction text, e.g. 阿莫西林，一天两次，一次一粒，吃一周，从2026-03-20开始")
    p.add_argument("--med-start", help="Explicit medication start datetime/date, optional")
    p.add_argument("--extra-reminder", action="append", default=[], help="Extra reminder in 标题|时间 format, can repeat")
    p.add_argument("--extra-text", help="Free text containing items like 2026-03-27 10:00复诊、2026-03-21 18:00取药")
    args = p.parse_args()

    if not any([args.appointment, args.medication_text, args.extra_reminder, args.extra_text]):
        raise SystemExit("At least one of --appointment, --medication-text, --extra-reminder, --extra-text is required")

    appointment_block = build_appointment_reminders(args.appointment) if args.appointment else None
    medication_block = build_medication_reminders(args.medication_text, args.med_start) if args.medication_text else None
    extra_items = [parse_extra_item(x) for x in args.extra_reminder]
    if args.extra_text:
        extra_items.extend(extract_extra_from_text(args.extra_text))

    output = {
        "appointment_block": appointment_block,
        "medication_block": medication_block,
        "extra_reminders": extra_items,
        "calendar_tasks": build_calendar_tasks(appointment_block, medication_block, extra_items),
        "note": "若运行环境支持提醒或日历工具，可直接按 calendar_tasks 自动创建；否则把这些时间展示给用户并建议加入手机日历。",
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
