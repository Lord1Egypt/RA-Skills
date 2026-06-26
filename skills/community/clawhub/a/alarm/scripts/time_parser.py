
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

TASK_KEYWORDS = [
    '提醒', '记得', '别忘', '截止', '前给我', '前发我', '前提交', '前完成',
    '开会', '评审', '确认', '安排', '提交', '发我', '做完', '完成', '处理', '给我',
]

IMPORTANT_KEYWORDS = ['重要', '务必', '一定', '千万', '别迟到', '开会', '评审', '面试', '汇报', '提交', '截止']
WEEKDAY_MAP = {'一': 0, '二': 1, '三': 2, '四': 3, '五': 4, '六': 5, '日': 6, '天': 6}
CH_NUM = {'零': 0, '〇': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}


@dataclass
class ParsedReminder:
    need_reminder: bool
    reason: str
    deadline_dt: datetime | None
    reminder_dt: datetime | None
    lead_minutes: int | None
    deadline_text: str | None
    summary: str | None
    confirm_text: str | None
    reminder_text: str | None


_DATE_TIME_PATTERNS = [
    re.compile(r'(?P<year>20\d{2})[-/年](?P<month>\d{1,2})[-/月](?P<day>\d{1,2})[日号]?\s*(?P<hour>\d{1,2})(?:[:点时](?P<minute>\d{1,2}))?'),
    re.compile(r'(?P<month>\d{1,2})月(?P<day>\d{1,2})[日号]?\s*(?P<part>上午|中午|下午|晚上|今晚|凌晨)?\s*(?P<hour>[零〇一二两三四五六七八九十百\d]{1,4})(?:[:点时](?P<minute>[零〇一二两三四五六七八九十百\d]{1,4}))?'),
    re.compile(r'(?P<relative>今天|今晚|明天|后天)\s*(?P<part>上午|中午|下午|晚上|今晚|凌晨)?\s*(?P<hour>[零〇一二两三四五六七八九十百\d]{1,4})?(?:[:点时](?P<minute>[零〇一二两三四五六七八九十百\d]{1,4}))?'),
    re.compile(r'(?P<week_prefix>下周|这周|本周)?周(?P<weekday>[一二三四五六日天])\s*(?P<part>上午|中午|下午|晚上|今晚|凌晨)?\s*(?P<hour>[零〇一二两三四五六七八九十百\d]{1,4})?(?:[:点时](?P<minute>[零〇一二两三四五六七八九十百\d]{1,4}))?'),
    re.compile(r'(?P<part>上午|中午|下午|晚上|今晚|凌晨)\s*(?P<hour>[零〇一二两三四五六七八九十百\d]{1,4})?(?:[:点时](?P<minute>[零〇一二两三四五六七八九十百\d]{1,4}))?'),
    re.compile(r'(?P<hour>\d{1,2})(?:[:点时](?P<minute>\d{1,2}))'),
]


def chinese_to_int(text: str | None) -> int | None:
    if text is None or text == '':
        return None
    text = str(text).strip()
    if text.isdigit():
        return int(text)
    if text == '十':
        return 10
    if '十' in text:
        left, _, right = text.partition('十')
        tens = CH_NUM.get(left, 1 if left == '' else 0)
        units = CH_NUM.get(right, 0) if right else 0
        return tens * 10 + units
    total = 0
    for ch in text:
        if ch not in CH_NUM:
            return None
        total = total * 10 + CH_NUM[ch]
    return total


def _apply_part(part: str | None, hour: int | None) -> tuple[int, int]:
    if hour is None:
        if part in ('上午',):
            return 10, 0
        if part in ('中午',):
            return 12, 0
        if part in ('下午',):
            return 15, 0
        if part in ('晚上', '今晚'):
            return 20, 0
        if part in ('凌晨',):
            return 1, 0
        return 18, 0
    h = hour
    if part in ('下午',) and 1 <= h <= 11:
        h += 12
    elif part in ('晚上', '今晚') and 1 <= h <= 11:
        h += 12
    elif part in ('中午',) and 1 <= h <= 10:
        h += 12
    return h, 0


def _normalize_hour_without_part(hour: int | None) -> int | None:
    if hour is None:
        return None
    if 1 <= hour <= 7:
        return hour + 12
    return hour


def _safe_datetime(year: int, month: int, day: int, hour: int, minute: int, tz: ZoneInfo) -> datetime | None:
    try:
        return datetime(year, month, day, hour, minute, tzinfo=tz)
    except ValueError:
        return None


def parse_deadline(text: str, now: datetime, tz_name: str = 'Asia/Shanghai') -> tuple[datetime | None, str | None]:
    tz = ZoneInfo(tz_name)
    if now.tzinfo is None:
        now = now.replace(tzinfo=tz)
    else:
        now = now.astimezone(tz)
    content = text.strip()

    for pattern in _DATE_TIME_PATTERNS:
        match = pattern.search(content)
        if not match:
            continue
        gd = match.groupdict()
        deadline = None
        if gd.get('year'):
            year = int(gd['year'])
            month = int(gd['month'])
            day = int(gd['day'])
            hour = chinese_to_int(gd.get('hour')) or 18
            minute = chinese_to_int(gd.get('minute')) or 0
            deadline = _safe_datetime(year, month, day, hour, minute, tz)
        elif gd.get('month') and gd.get('day'):
            year = now.year
            month = int(gd['month'])
            day = int(gd['day'])
            hour = chinese_to_int(gd.get('hour'))
            if not gd.get('part'):
                hour = _normalize_hour_without_part(hour)
            minute = chinese_to_int(gd.get('minute')) or 0
            hour, default_minute = _apply_part(gd.get('part'), hour)
            minute = minute or default_minute
            deadline = _safe_datetime(year, month, day, hour, minute, tz)
            if deadline and deadline < now:
                deadline = _safe_datetime(year + 1, month, day, hour, minute, tz)
        elif gd.get('relative'):
            delta_days = {'今天': 0, '今晚': 0, '明天': 1, '后天': 2}[gd['relative']]
            target_date = (now + timedelta(days=delta_days)).date()
            hour = chinese_to_int(gd.get('hour'))
            if not gd.get('part') and gd['relative'] != '今晚':
                hour = _normalize_hour_without_part(hour)
            minute = chinese_to_int(gd.get('minute')) or 0
            hour, default_minute = _apply_part(gd.get('part') or ('今晚' if gd['relative'] == '今晚' else None), hour)
            minute = minute or default_minute
            deadline = datetime(target_date.year, target_date.month, target_date.day, hour, minute, tzinfo=tz)
            if deadline < now and gd['relative'] in ('今天', '今晚'):
                deadline = deadline + timedelta(days=1)
        elif gd.get('weekday'):
            wd = WEEKDAY_MAP[gd['weekday']]
            prefix = gd.get('week_prefix') or ''
            current_wd = now.weekday()
            delta = (wd - current_wd) % 7
            if prefix == '下周':
                delta += 7 if delta == 0 else 7
            elif prefix in ('这周', '本周') and delta == 0:
                delta = 0
            elif prefix == '' and delta == 0:
                delta = 7
            target_date = (now + timedelta(days=delta)).date()
            hour = chinese_to_int(gd.get('hour'))
            if not gd.get('part'):
                hour = _normalize_hour_without_part(hour)
            minute = chinese_to_int(gd.get('minute')) or 0
            hour, default_minute = _apply_part(gd.get('part'), hour)
            minute = minute or default_minute
            deadline = datetime(target_date.year, target_date.month, target_date.day, hour, minute, tzinfo=tz)
        elif gd.get('part'):
            target_date = now.date()
            hour = chinese_to_int(gd.get('hour'))
            minute = chinese_to_int(gd.get('minute')) or 0
            hour, default_minute = _apply_part(gd.get('part'), hour)
            minute = minute or default_minute
            deadline = datetime(target_date.year, target_date.month, target_date.day, hour, minute, tzinfo=tz)
            if deadline < now:
                deadline = deadline + timedelta(days=1)
        else:
            hour = _normalize_hour_without_part(chinese_to_int(gd.get('hour')))
            minute = chinese_to_int(gd.get('minute')) or 0
            if hour is None:
                continue
            target_date = now.date()
            deadline = datetime(target_date.year, target_date.month, target_date.day, hour, minute, tzinfo=tz)
            if deadline < now:
                deadline = deadline + timedelta(days=1)

        if deadline:
            return deadline, match.group(0)
    return None, None


def looks_like_task(text: str) -> bool:
    return any(keyword in text for keyword in TASK_KEYWORDS)


def extract_summary(text: str) -> str:
    content = re.sub(r'\s+', ' ', text).strip()
    content = re.sub(r'^(提醒我|记得|别忘了?|请|帮我|麻烦)[:：,，\s]*', '', content)
    content = content[:60].strip('，。,. ')
    return content or '这件事'


def format_human_time(dt: datetime, now: datetime) -> str:
    if dt.date() == now.date():
        day = '今天'
    elif dt.date() == (now + timedelta(days=1)).date():
        day = '明天'
    else:
        day = f'{dt.month}月{dt.day}日'
    return f'{day} {dt:%H:%M}'


def parse_explicit_lead_minutes(text: str) -> int | None:
    explicit_patterns = [
        (re.compile(r'提前\s*(\d{1,3})\s*分钟'), lambda m: int(m.group(1))),
        (re.compile(r'提前\s*(\d{1,2})\s*小时'), lambda m: int(m.group(1)) * 60),
        (re.compile(r'提前\s*半小时'), lambda m: 30),
        (re.compile(r'提前\s*一刻钟'), lambda m: 15),
        (re.compile(r'提前\s*一天'), lambda m: 1440),
    ]
    for pattern, fn in explicit_patterns:
        match = pattern.search(text)
        if match:
            return max(5, fn(match))
    return None


def choose_lead_minutes(text: str, now: datetime, deadline_dt: datetime) -> int:
    explicit = parse_explicit_lead_minutes(text)
    if explicit is not None:
        return explicit

    delta = deadline_dt - now
    total_minutes = max(1, int(delta.total_seconds() // 60))

    # 默认策略：时间预留更宽松，越远的事越早提醒。
    if total_minutes <= 45:
        lead = 10
    elif total_minutes <= 120:
        lead = 20
    elif total_minutes <= 360:
        lead = 40
    elif total_minutes <= 24 * 60:
        lead = 90
    elif total_minutes <= 3 * 24 * 60:
        lead = 240
    else:
        lead = 24 * 60

    if any(k in text for k in IMPORTANT_KEYWORDS):
        lead = int(lead * 1.5)

    # 不要超过截止时间的 80%，避免提醒落在过早位置
    lead = min(lead, max(5, int(total_minutes * 0.8)))
    return max(5, lead)


def analyze_message(text: str, now: datetime, tz_name: str = 'Asia/Shanghai', sender_name: str | None = None) -> ParsedReminder:
    deadline_dt, deadline_text = parse_deadline(text, now, tz_name)
    if deadline_dt is None:
        return ParsedReminder(False, '未识别到可用时间', None, None, None, None, None, None, None)
    if not looks_like_task(text):
        return ParsedReminder(False, '没有明显提醒/待办语义', None, None, None, None, None, None, None)
    tz = ZoneInfo(tz_name)
    if now.tzinfo is None:
        now = now.replace(tzinfo=tz)
    else:
        now = now.astimezone(tz)

    lead_minutes = choose_lead_minutes(text, now, deadline_dt)
    reminder_dt = deadline_dt - timedelta(minutes=lead_minutes)

    # 如果用户提得太晚，仍然给一个近端提醒机会，而不是直接放弃
    if reminder_dt <= now:
        if deadline_dt <= now + timedelta(minutes=3):
            return ParsedReminder(False, '截止时间过近，无法安排有效提醒', None, None, None, None, None, None, None)
        reminder_dt = now + timedelta(minutes=2)
        lead_minutes = max(1, int((deadline_dt - reminder_dt).total_seconds() // 60))

    summary = extract_summary(text)
    human_reminder = format_human_time(reminder_dt, now)
    human_deadline = format_human_time(deadline_dt, now)
    confirm_text = f'我已经记住并在{human_reminder}提醒'
    if sender_name:
        reminder_text = f'提醒{sender_name}：{summary}（截止时间 {human_deadline}）'
    else:
        reminder_text = f'提醒你：{summary}（截止时间 {human_deadline}）'
    return ParsedReminder(True, 'ok', deadline_dt, reminder_dt, lead_minutes, human_deadline, summary, confirm_text, reminder_text)
