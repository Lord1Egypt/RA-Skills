#!/usr/bin/env python3
"""
amemo 时间解析脚本 — 将自然语言时间词转换为标准 datetime 字符串。

用法:
    python parse_time.py "明天下午3点开会"
    python parse_time.py "后天" --extract-only
    echo "今天和明天都要开会" | python parse_time.py --stdin

输出格式: JSON 数组，每个元素包含 {time, content, raw}
"""

import re
import json
import sys
from datetime import datetime, timedelta

# ── 相对日期词 ──────────────────────────────────────────────
RELATIVE_DAYS = {
    "今天": 0, "今日": 0, "当天": 0,
    "明天": 1, "明日": 1,
    "昨天": -1, "昨日": -1,
    "后天": 2,
    "大后天": 3,
}

RELATIVE_SPECIAL = {
    "将来": 365, "未来": 365,
    "最近": 15, "最新": 15, "近期": 15,
}

# ── 时段词 → 默认小时 ─────────────────────────────────────
TIME_OF_DAY = {
    "早上": 7, "早晨": 7, "清早": 7,
    "上午": 9,
    "中午": 12,
    "下午": 14,
    "晚上": 19, "傍晚": 19,
    "深夜": 23, "半夜": 23,
}

# ── 祈使动词列表（用于判断任务 vs 笔记） ─────────────────────
IMPERATIVE_VERBS = [
    "开会", "吃饭", "去", "买", "交", "看", "做", "提醒", "记得",
    "提交", "参加", "拜访", "取", "拿", "送", "接", "打", "回",
    "复习", "考试", "面试", "体检", "复查", "出发", "开始",
]

STATEMENT_MARKERS = ["的时候", "的情况", "的情景", "的经历"]


def get_weekday_offset(target_weekday: int, now: datetime) -> int:
    """计算到下一个目标星期几的天数偏移。"""
    today_weekday = now.weekday()  # Monday=0
    days_ahead = target_weekday - today_weekday
    if days_ahead <= 0:
        days_ahead += 7
    return days_ahead


def parse_specific_time(text: str) -> int | None:
    """从文本中提取具体时间（小时:分钟），返回分钟数或 None。"""
    # "3点" / "3点半" / "10点30" / "15:30"
    m = re.search(r"(\d{1,2})点(\d{1,2}分?)?", text)
    if m:
        hour = int(m.group(1))
        minute = int(m.group(2).replace("分", "")) if m.group(2) else 0
        # 如果文本包含下午/晚上等时段词且小时≤12，转换为24小时制
        if hour <= 12:
            for tod_word in ["下午", "晚上", "傍晚", "深夜", "半夜"]:
                if tod_word in text:
                    hour += 12
                    break
        return hour * 60 + minute
    m = re.search(r"(\d{1,2}):(\d{1,2})", text)
    if m:
        return int(m.group(1)) * 60 + int(m.group(2))
    return None


def parse_date_phrase(phrase: str, now: datetime) -> datetime | None:
    """解析单个日期短语，返回 datetime（时间为 00:00:00）。"""
    # 相对词
    for word, offset in RELATIVE_DAYS.items():
        if word in phrase:
            return (now + timedelta(days=offset)).replace(hour=0, minute=0, second=0, microsecond=0)

    # 特殊偏移
    for word, offset in RELATIVE_SPECIAL.items():
        if word in phrase:
            return (now + timedelta(days=offset)).replace(hour=0, minute=0, second=0, microsecond=0)

    # 下周X
    weekday_map = {"一": 0, "二": 1, "三": 2, "四": 3, "五": 4, "六": 5, "日": 6, "天": 6}
    m = re.search(r"下[周星期]([一二三四五六日天])", phrase)
    if m:
        target = weekday_map[m.group(1)]
        offset = get_weekday_offset(target, now) + 7
        return (now + timedelta(days=offset)).replace(hour=0, minute=0, second=0, microsecond=0)

    # 本周末 / 这周末 → 本周六
    if "本周末" in phrase or "这周末" in phrase:
        offset = get_weekday_offset(5, now)
        return (now + timedelta(days=offset)).replace(hour=0, minute=0, second=0, microsecond=0)

    # 下周末 → 下周六
    if "下周末" in phrase:
        offset = get_weekday_offset(5, now) + 7
        return (now + timedelta(days=offset)).replace(hour=0, minute=0, second=0, microsecond=0)

    # 具体日期: "12月25日" / "3月1号" / "2025-12-25"
    m = re.search(r"(\d{1,2})月(\d{1,2})[日号]", phrase)
    if m:
        month, day = int(m.group(1)), int(m.group(2))
        year = now.year
        try:
            return datetime(year, month, day, 0, 0, 0)
        except ValueError:
            return None

    m = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", phrase)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), 0, 0, 0)
        except ValueError:
            return None

    return None


def apply_time_of_day(dt: datetime, text: str) -> datetime:
    """在日期基础上叠加时段词或具体时间。"""
    # 具体时间优先
    minutes = parse_specific_time(text)
    if minutes is not None:
        return dt.replace(hour=minutes // 60, minute=minutes % 60)

    # 时段词
    for word, hour in TIME_OF_DAY.items():
        if word in text:
            return dt.replace(hour=hour)

    return dt


def is_imperative(text: str) -> bool:
    """判断文本是否为祈使句（任务）vs 陈述句（笔记）。"""
    # 陈述性标记优先
    for marker in STATEMENT_MARKERS:
        if marker in text:
            return False
    # 检查祈使动词
    for verb in IMPERATIVE_VERBS:
        if verb in text:
            return True
    return False


def extract_time_content_pairs(user_input: str) -> list[dict]:
    """
    从用户输入中提取所有 (时间, 内容) 对。
    返回 [{"time": "YYYY-MM-DD HH:MM:SS", "content": "...", "raw": "..."}]
    """
    now = datetime.now()
    results = []

    # 提取所有日期短语
    date_patterns = list(RELATIVE_DAYS.keys()) + list(RELATIVE_SPECIAL.keys())
    date_patterns += ["下周[一二三四五六日天]", "本周末", "这周末", "下周末",
                      r"\d{1,2}月\d{1,2}[日号]", r"\d{4}-\d{1,2}-\d{1,2}"]

    found_dates = []
    for pattern in date_patterns:
        for m in re.finditer(pattern, user_input):
            found_dates.append((m.start(), m.end(), m.group()))

    found_dates.sort(key=lambda x: x[0])

    if not found_dates:
        # 无时间词，不处理
        return []

    # 多时间词拆分
    for i, (start, end, phrase) in enumerate(found_dates):
        dt = parse_date_phrase(phrase, now)
        if dt is None:
            continue

        dt = apply_time_of_day(dt, user_input)

        # 提取对应内容：取该时间词附近的动词性内容
        # 简单策略：取整句去除时间词后的剩余部分
        content = user_input.strip()

        results.append({
            "time": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "content": content,
            "raw": phrase,
        })

    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(description="amemo 时间解析器")
    parser.add_argument("text", nargs="?", help="要解析的文本")
    parser.add_argument("--stdin", action="store_true", help="从 stdin 读取")
    parser.add_argument("--now", help="指定基准时间 (YYYY-MM-DD HH:MM:SS)，默认当前系统时间")
    parser.add_argument("--extract-only", action="store_true", help="仅提取时间词，不关联内容")
    args = parser.parse_args()

    if args.stdin:
        text = sys.stdin.read().strip()
    elif args.text:
        text = args.text
    else:
        parser.print_help()
        sys.exit(1)

    now = datetime.now()
    if args.now:
        now = datetime.strptime(args.now, "%Y-%m-%d %H:%M:%S")

    # 提取时间-内容对
    pairs = extract_time_content_pairs(text)

    if not pairs:
        print(json.dumps({"error": "未识别到时间词", "input": text}, ensure_ascii=False))
        sys.exit(1)

    # 判断意图
    imperative = is_imperative(text)
    intent = "task" if imperative else "memo"

    output = {
        "intent": intent,
        "pairs": pairs,
        "base_time": now.strftime("%Y-%m-%d %H:%M:%S"),
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
