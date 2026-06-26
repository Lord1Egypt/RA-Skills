from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

ROOT = Path(__file__).resolve().parent.parent
STATE_PATH = ROOT / "data" / "subscriptions.json"
TIMEZONE_STATE_PATH = ROOT / "data" / "user_timezones.json"

DEFAULT_TOPICS = ["国际科技", "国际军事"]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["add", "list", "remove", "update", "test", "set-timezone", "get-timezone"])
    p.add_argument("--to")
    p.add_argument("--time")
    p.add_argument("--topics")
    p.add_argument("--id")
    p.add_argument("--timezone")
    return p.parse_args()


def load_json_list(path: Path) -> list:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save_json_list(path: Path, items: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


def load_timezones() -> dict:
    if not TIMEZONE_STATE_PATH.exists():
        return {}
    return json.loads(TIMEZONE_STATE_PATH.read_text(encoding="utf-8"))


def save_timezones(state: dict) -> None:
    TIMEZONE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    TIMEZONE_STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def load_state() -> list[dict]:
    return load_json_list(STATE_PATH)


def save_state(items: list[dict]) -> None:
    save_json_list(STATE_PATH, items)


def print_json(data: object) -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print(json.dumps(data, ensure_ascii=False, indent=2))


def run_cmd(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def find_openclaw_cmd() -> str:
    candidates = [
        "openclaw.cmd",
        str(Path.home() / "AppData" / "Roaming" / "npm" / "openclaw.cmd"),
    ]
    for candidate in candidates:
        try:
            result = subprocess.run([candidate, "--version"], capture_output=True, text=True, encoding="utf-8", errors="replace")
            if result.returncode == 0 or result.stdout or result.stderr:
                return candidate
        except FileNotFoundError:
            continue
    raise SystemExit("openclaw.cmd not found in PATH.")


def normalize_topics(raw: str | None) -> list[str]:
    if not raw or not raw.strip():
        return DEFAULT_TOPICS.copy()
    parts = [x.strip() for x in raw.replace("，", ",").split(",")]
    return [x for x in parts if x] or DEFAULT_TOPICS.copy()


def get_timezone_for_target(target: str) -> str | None:
    return load_timezones().get(target)


def set_timezone_for_target(target: str, timezone: str) -> None:
    ZoneInfo(timezone)
    state = load_timezones()
    state[target] = timezone
    save_timezones(state)


def get_timezone(to: str) -> dict:
    return {"to": to, "timezone": get_timezone_for_target(to)}


def set_timezone(to: str, timezone: str) -> dict:
    try:
        ZoneInfo(timezone)
    except ZoneInfoNotFoundError:
        raise SystemExit("无效时区，请使用 IANA 时区名，例如 Asia/Shanghai")
    set_timezone_for_target(to, timezone)
    return {"ok": True, "to": to, "timezone": timezone}


def ensure_timezone(to: str) -> str:
    timezone = get_timezone_for_target(to)
    if not timezone:
        raise SystemExit("missing timezone for target, set timezone first")
    return timezone


def build_content(topics: list[str]) -> str:
    topic_text = "、".join(topics)
    return f"每日新闻推送: {topic_text}"


def build_prompt(topics: list[str]) -> str:
    topic_text = "、".join(topics)
    topic_lines = "\n".join(f"## {t}" for t in topics)
    return (
        f"请整理今天的新闻简报，主题为：{topic_text}。"
        "要求：1. 通过 web_fetch 等方式抓取当天相关新闻 2. 优先权威来源，过滤重复和明显旧闻 "
        "3. 每个主题整理 2 到 4 条 4. 每条格式为“标题 | 来源 | 要点” "
        "5. 总体保持简洁，适合即时消息阅读 6. 直接输出最终简报，不要解释过程。\n\n"
        "输出结构示例：\n"
        "今日热点简报\n\n"
        f"{topic_lines}\n"
        "1. 标题 | 来源：xxx | 要点：xxx"
    )


def build_agent_message(to: str, topics: list[str], *, test_mode: bool = False) -> str:
    topic_text = "、".join(topics)
    prefix = "[TEST] " if test_mode else ""
    return (
        f"{prefix}请为 QQ 用户 {to} 生成并投递一份今日新闻简报，主题：{topic_text}。"
        "先抓取当天相关新闻，再筛选、去重、整理为简洁中文简报。"
        "输出时直接给用户最终内容，不要解释过程，不要输出系统说明。"
        "每个主题 2 到 4 条，每条包含标题、来源、要点。"
        "如果是测试，只需要立即发出一份简洁可读的真实新闻简报即可。"
    )


def parse_relative_time(text: str, tz_name: str) -> str | None:
    tz = ZoneInfo(tz_name)
    now = datetime.now(tz)
    raw = text.strip().replace("个", "")
    chinese_digits = {
        "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5,
        "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
    }

    def parse_num(s: str) -> int | None:
        s = s.strip()
        if not s:
            return None
        if s.isdigit():
            return int(s)
        if s == "十":
            return 10
        if s.startswith("十") and len(s) == 2 and s[1] in chinese_digits:
            return 10 + chinese_digits[s[1]]
        if s.endswith("十") and len(s) == 2 and s[0] in chinese_digits:
            return chinese_digits[s[0]] * 10
        if len(s) == 2 and s[0] in chinese_digits and s[1] in chinese_digits and s[0] == "十":
            return 10 + chinese_digits[s[1]]
        if len(s) == 1 and s in chinese_digits:
            return chinese_digits[s]
        return None

    for suffixes, unit in [(("分钟后", "分后", "分钟", "分"), "minutes"), (("小时后", "钟头后", "小时", "钟头"), "hours")]:
        for suffix in suffixes:
            if raw.endswith(suffix):
                value = parse_num(raw[:-len(suffix)])
                if value is None:
                    return None
                delta = timedelta(minutes=value) if unit == "minutes" else timedelta(hours=value)
                return (now + delta).isoformat(timespec="minutes")
    return None


def parse_time_text(text: str, tz_name: str) -> tuple[str | None, str | None]:
    tz = ZoneInfo(tz_name)
    now = datetime.now(tz)
    raw = text.strip().replace("：", ":").replace(".", ":")

    relative_dt = parse_relative_time(raw, tz_name)
    if relative_dt:
        return relative_dt, None

    recurring_prefix = {
        "每天": "*",
        "每日": "*",
        "工作日": "1-5",
        "周一": "1",
        "周二": "2",
        "周三": "3",
        "周四": "4",
        "周五": "5",
        "周六": "6",
        "周日": "0",
        "周天": "0",
        "星期一": "1",
        "星期二": "2",
        "星期三": "3",
        "星期四": "4",
        "星期五": "5",
        "星期六": "6",
        "星期日": "0",
        "星期天": "0",
    }
    period_map = {
        "凌晨": 0,
        "早上": 8,
        "上午": 9,
        "中午": 12,
        "下午": 15,
        "晚上": 20,
        "今晚": 20,
    }

    prefix = None
    for key in sorted(recurring_prefix.keys(), key=len, reverse=True):
        if raw.startswith(key):
            prefix = key
            raw = raw[len(key):].strip()
            break

    tomorrow = False
    if raw.startswith("明天"):
        tomorrow = True
        raw = raw[2:].strip()
    elif raw.startswith("今天"):
        raw = raw[2:].strip()

    period = None
    for key in period_map:
        if raw.startswith(key):
            period = key
            raw = raw[len(key):].strip()
            break

    normalized = raw.replace("点半", ":30").replace("点", ":").replace("分", "")
    if normalized.endswith(":"):
        normalized += "00"
    if ":" not in normalized and normalized.isdigit():
        normalized = f"{normalized}:00"

    try:
        hour_str, minute_str = normalized.split(":", 1)
        hour = int(hour_str)
        minute = int(minute_str or "0")
    except ValueError:
        raise SystemExit("无法解析时间，请改用更明确的格式。")

    if period in {"下午", "晚上", "今晚"} and 1 <= hour <= 11:
        hour += 12
    if period == "中午" and hour < 11:
        hour += 12
    if period == "凌晨" and hour == 12:
        hour = 0

    if prefix:
        return None, f"{minute} {hour} * * {recurring_prefix[prefix]}"

    for fmt in ("%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M", "%H:%M"):
        try:
            parsed = datetime.strptime(text.strip().replace(".", ":"), fmt)
            if fmt == "%H:%M":
                dt = now.replace(hour=parsed.hour, minute=parsed.minute, second=0, microsecond=0)
                if dt <= now:
                    dt += timedelta(days=1)
                return dt.isoformat(timespec="minutes"), None
            dt = parsed.replace(tzinfo=tz)
            return dt.isoformat(timespec="minutes"), None
        except ValueError:
            continue

    dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if tomorrow:
        dt += timedelta(days=1)
    elif dt <= now:
        dt += timedelta(days=1)
    return dt.isoformat(timespec="minutes"), None


def resolve_schedule(time_text: str, timezone: str) -> tuple[str | None, str | None]:
    return parse_time_text(time_text, timezone)


def create_cron_job(openclaw_cmd: str, *, to: str, topics: list[str], time_text: str, test_mode: bool = False) -> dict:
    timezone = ensure_timezone(to)
    at_value, cron_expr = resolve_schedule(time_text, timezone)
    name = build_content(topics)
    message = build_agent_message(to, topics, test_mode=test_mode)
    cmd = [
        openclaw_cmd,
        "cron",
        "add",
        "--name",
        name,
        "--session",
        "isolated",
        "--message",
        message,
        "--channel",
        "qqbot",
        "--to",
        to,
        "--announce",
        "--json",
    ]
    delete_after_run = False
    if cron_expr:
        cmd.extend(["--cron", cron_expr, "--tz", timezone])
    else:
        cmd.extend(["--at", at_value, "--delete-after-run"])
        delete_after_run = True
    result = run_cmd(cmd)
    if result.returncode != 0:
        raise SystemExit(result.stderr or result.stdout)
    payload = json.loads(result.stdout.strip())
    return {
        "id": payload.get("id"),
        "name": name,
        "timezone": timezone,
        "schedule": payload.get("schedule"),
        "delivery": payload.get("delivery"),
        "deleteAfterRun": delete_after_run,
    }


def build_entry(payload: dict, *, to: str, time_text: str, topics: list[str]) -> dict:
    return {
        "id": payload.get("id"),
        "to": to,
        "time": time_text,
        "topics": topics,
        "name": payload.get("name"),
        "schedule": payload.get("schedule"),
        "timezone": payload.get("timezone"),
        "prompt": build_prompt(topics),
        "delivery": payload.get("delivery"),
        "deleteAfterRun": payload.get("deleteAfterRun"),
    }


def create_subscription(to: str, time_text: str, topics: list[str]) -> dict:
    openclaw_cmd = find_openclaw_cmd()
    payload = create_cron_job(openclaw_cmd, to=to, topics=topics, time_text=time_text)
    items = load_state()
    entry = build_entry(payload, to=to, time_text=time_text, topics=topics)
    items = [x for x in items if x.get("id") != entry["id"]]
    items.append(entry)
    save_state(items)
    return entry


def create_test_push(to: str, topics: list[str], time_text: str = "5分钟后") -> dict:
    openclaw_cmd = find_openclaw_cmd()
    payload = create_cron_job(openclaw_cmd, to=to, topics=topics, time_text=time_text, test_mode=True)
    return build_entry(payload, to=to, time_text=time_text, topics=topics)


def list_subscriptions(to: str) -> list[dict]:
    items = load_state()
    return [x for x in items if x.get("to") == to]


def remove_subscription(job_id: str) -> dict:
    openclaw_cmd = find_openclaw_cmd()
    result = run_cmd([openclaw_cmd, "cron", "rm", job_id, "--json"])
    if result.returncode != 0:
        raise SystemExit(result.stderr or result.stdout)
    items = [x for x in load_state() if x.get("id") != job_id]
    save_state(items)
    try:
        return json.loads(result.stdout or "{}")
    except Exception:
        return {"ok": True, "id": job_id}


def update_subscription(job_id: str, *, time_text: str | None, topics_raw: str | None) -> dict:
    items = load_state()
    existing = next((x for x in items if x.get("id") == job_id), None)
    if not existing:
        raise SystemExit("subscription not found")

    to = existing.get("to")
    if not to:
        raise SystemExit("subscription missing target")

    time_value = time_text or existing.get("time")
    topics = normalize_topics(topics_raw) if topics_raw is not None else existing.get("topics") or DEFAULT_TOPICS.copy()

    remove_subscription(job_id)
    try:
        return create_subscription(to, time_value, topics)
    except Exception:
        recreated = create_subscription(to, existing.get("time"), existing.get("topics") or DEFAULT_TOPICS.copy())
        raise SystemExit(f"update failed and original subscription was restored: {recreated.get('id')}")


def main() -> int:
    args = parse_args()

    if args.action == "get-timezone":
        if not args.to:
            raise SystemExit("get-timezone needs --to")
        print_json(get_timezone(args.to))
        return 0

    if args.action == "set-timezone":
        if not args.to or not args.timezone:
            raise SystemExit("set-timezone needs --to and --timezone")
        print_json(set_timezone(args.to, args.timezone))
        return 0

    if args.action == "list":
        if not args.to:
            raise SystemExit("list needs --to")
        print_json(list_subscriptions(args.to))
        return 0

    if args.action == "remove":
        if not args.id:
            raise SystemExit("remove needs --id")
        print_json(remove_subscription(args.id))
        return 0

    if args.action == "update":
        if not args.id:
            raise SystemExit("update needs --id")
        if args.time is None and args.topics is None:
            raise SystemExit("update needs at least one of --time or --topics")
        print_json(update_subscription(args.id, time_text=args.time, topics_raw=args.topics))
        return 0

    if args.action == "test":
        if not args.to:
            raise SystemExit("test needs --to")
        topics = normalize_topics(args.topics)
        ensure_timezone(args.to)
        print_json(create_test_push(args.to, topics, time_text=args.time or "5分钟后"))
        return 0

    if args.action == "add":
        if not args.to or not args.time:
            raise SystemExit("add needs --to and --time")
        topics = normalize_topics(args.topics)
        ensure_timezone(args.to)
        print_json(create_subscription(args.to, args.time, topics))
        return 0

    raise SystemExit("unsupported action")


if __name__ == "__main__":
    raise SystemExit(main())
