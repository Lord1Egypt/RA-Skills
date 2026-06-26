#!/usr/bin/env python3
"""
中文生日提醒管理脚本。

功能：
- 从中国身份证提取公历生日
- 默认按农历保存，也支持按公历保存
- 为每条记录单独设置提前提醒天数
- 列出记录、查询下一个生日、检查当天是否需要提醒
"""

from __future__ import annotations

import argparse
import json
import os
import re
import smtplib
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from email.message import EmailMessage
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib import error, request


LUNAR_INFO = [
    0x04BD8, 0x04AE0, 0x0A570, 0x054D5, 0x0D260, 0x0D950, 0x16554, 0x056A0,
    0x09AD0, 0x055D2, 0x04AE0, 0x0A5B6, 0x0A4D0, 0x0D250, 0x1D255, 0x0B540,
    0x0D6A0, 0x0ADA2, 0x095B0, 0x14977, 0x04970, 0x0A4B0, 0x0B4B5, 0x06A50,
    0x06D40, 0x1AB54, 0x02B60, 0x09570, 0x052F2, 0x04970, 0x06566, 0x0D4A0,
    0x0EA50, 0x06E95, 0x05AD0, 0x02B60, 0x186E3, 0x092E0, 0x1C8D7, 0x0C950,
    0x0D4A0, 0x1D8A6, 0x0B550, 0x056A0, 0x1A5B4, 0x025D0, 0x092D0, 0x0D2B2,
    0x0A950, 0x0B557, 0x06CA0, 0x0B550, 0x15355, 0x04DA0, 0x0A5D0, 0x14573,
    0x052D0, 0x0A9A8, 0x0E950, 0x06AA0, 0x0AEA6, 0x0AB50, 0x04B60, 0x0AAE4,
    0x0A570, 0x05260, 0x0F263, 0x0D950, 0x05B57, 0x056A0, 0x096D0, 0x04DD5,
    0x04AD0, 0x0A4D0, 0x0D4D4, 0x0D250, 0x0D558, 0x0B540, 0x0B5A0, 0x195A6,
    0x095B0, 0x049B0, 0x0A974, 0x0A4B0, 0x0B27A, 0x06A50, 0x06D40, 0x0AF46,
    0x0AB60, 0x09570, 0x04AF5, 0x04970, 0x064B0, 0x074A3, 0x0EA50, 0x06B58,
    0x05AC0, 0x0AB60, 0x096D5, 0x092E0, 0x0C960, 0x0D954, 0x0D4A0, 0x0DA50,
    0x07552, 0x056A0, 0x0ABB7, 0x025D0, 0x092D0, 0x0CAB5, 0x0A950, 0x0B4A0,
    0x0BAA4, 0x0AD50, 0x055D9, 0x04BA0, 0x0A5B0, 0x15176, 0x052B0, 0x0A930,
    0x07954, 0x06AA0, 0x0AD50, 0x05B52, 0x04B60, 0x0A6E6, 0x0A4E0, 0x0D260,
    0x0EA65, 0x0D530, 0x05AA0, 0x076A3, 0x096D0, 0x04BD7, 0x04AD0, 0x0A4D0,
    0x1D0B6, 0x0D250, 0x0D520, 0x0DD45, 0x0B5A0, 0x056D0, 0x055B2, 0x049B0,
    0x0A577, 0x0A4B0, 0x0AA50, 0x1B255, 0x06D20, 0x0ADA0,
]

MIN_YEAR = 1900
MAX_YEAR = 2099
BASE_SOLAR_DATE = date(1900, 1, 31)
DEFAULT_DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "birthdays.json"
DEFAULT_NOTIFICATION_CONFIG = Path(__file__).resolve().parents[1] / "data" / "notification.json"
DEFAULT_NOTIFICATION_TEMPLATE = {
    "channels": [
        {"type": "agent", "enabled": True},
        {
            "type": "email",
            "enabled": False,
            "host": "${BIRTHDAY_SMTP_HOST}",
            "port": "${BIRTHDAY_SMTP_PORT}",
            "username": "${BIRTHDAY_SMTP_USERNAME}",
            "password": "${BIRTHDAY_SMTP_PASSWORD}",
            "from": "${BIRTHDAY_EMAIL_FROM}",
            "to": ["${BIRTHDAY_EMAIL_TO}"],
            "use_tls": True,
            "subject": "生日提醒",
        },
    ]
}


@dataclass
class LunarDate:
    year: int
    month: int
    day: int
    is_leap: bool = False


def leap_month(year: int) -> int:
    return LUNAR_INFO[year - MIN_YEAR] & 0xF


def leap_days(year: int) -> int:
    if leap_month(year):
        return 30 if (LUNAR_INFO[year - MIN_YEAR] & 0x10000) else 29
    return 0


def month_days(year: int, month: int) -> int:
    return 30 if (LUNAR_INFO[year - MIN_YEAR] & (0x10000 >> month)) else 29


def lunar_year_days(year: int) -> int:
    total = 348
    bit = 0x8000
    info = LUNAR_INFO[year - MIN_YEAR]
    while bit > 0x8:
        if info & bit:
            total += 1
        bit >>= 1
    return total + leap_days(year)


def ensure_supported_year(year: int) -> None:
    if year < MIN_YEAR or year > MAX_YEAR:
        raise ValueError(f"年份 {year} 超出支持范围，当前仅支持 {MIN_YEAR}-{MAX_YEAR}。")


def solar_to_lunar(value: date) -> LunarDate:
    ensure_supported_year(value.year)
    offset = (value - BASE_SOLAR_DATE).days
    lunar_year = MIN_YEAR

    while lunar_year <= MAX_YEAR and offset >= lunar_year_days(lunar_year):
        offset -= lunar_year_days(lunar_year)
        lunar_year += 1

    if lunar_year > MAX_YEAR:
        raise ValueError("公历日期超出农历换算范围。")

    leap = leap_month(lunar_year)
    lunar_month = 1
    is_leap = False

    while lunar_month <= 12:
        if leap and lunar_month == leap + 1 and not is_leap:
            lunar_month -= 1
            is_leap = True
            days = leap_days(lunar_year)
        else:
            days = month_days(lunar_year, lunar_month)

        if offset < days:
            break

        offset -= days
        if is_leap and lunar_month == leap:
            is_leap = False
        lunar_month += 1

    lunar_day = offset + 1
    return LunarDate(lunar_year, lunar_month, lunar_day, is_leap)


def lunar_to_solar(lunar: LunarDate) -> date:
    ensure_supported_year(lunar.year)
    offset = 0

    for year in range(MIN_YEAR, lunar.year):
        offset += lunar_year_days(year)

    leap = leap_month(lunar.year)
    for month in range(1, lunar.month):
        offset += month_days(lunar.year, month)
        if leap == month:
            offset += leap_days(lunar.year)

    if lunar.is_leap:
        if leap != lunar.month:
            raise ValueError(f"{lunar.year} 年农历 {lunar.month} 月不是闰月。")
        offset += month_days(lunar.year, lunar.month)

    max_days = leap_days(lunar.year) if lunar.is_leap else month_days(lunar.year, lunar.month)
    if lunar.day < 1 or lunar.day > max_days:
        raise ValueError("农历日期不合法。")

    offset += lunar.day - 1
    return BASE_SOLAR_DATE + timedelta(days=offset)


def mask_idcard(idcard: str) -> str:
    if len(idcard) < 8:
        return "*" * len(idcard)
    return f"{idcard[:6]}{'*' * (len(idcard) - 10)}{idcard[-4:]}"


def parse_idcard_birthday(idcard: str) -> date:
    raw = idcard.strip().upper()
    if len(raw) == 18:
        digits = raw[:17]
        if not digits.isdigit() or (not raw[-1].isdigit() and raw[-1] != "X"):
            raise ValueError("18 位身份证号码格式不合法。")
        birthday = raw[6:14]
        year = int(birthday[:4])
        month = int(birthday[4:6])
        day = int(birthday[6:8])
        return date(year, month, day)
    if len(raw) == 15:
        if not raw.isdigit():
            raise ValueError("15 位身份证号码格式不合法。")
        birthday = raw[6:12]
        year = int("19" + birthday[:2])
        month = int(birthday[2:4])
        day = int(birthday[4:6])
        return date(year, month, day)
    raise ValueError("仅支持 15 位或 18 位中国身份证号码。")


def is_idcard_value(value: str) -> bool:
    raw = value.strip().upper()
    return bool(re.fullmatch(r"\d{15}", raw) or re.fullmatch(r"\d{17}[\dX]", raw))


def parse_birthday_value(value: str, calendar_hint: Optional[str], leap_month: bool) -> Dict[str, Any]:
    raw = value.strip()
    calendar = calendar_hint

    for prefix, detected in (
        ("公历:", "solar"),
        ("solar:", "solar"),
        ("阳历:", "solar"),
        ("农历:", "lunar"),
        ("lunar:", "lunar"),
    ):
        if raw.lower().startswith(prefix.lower()):
            raw = raw[len(prefix):].strip()
            calendar = detected
            break

    calendar = calendar or "lunar"
    normalized = raw.replace("/", "-").replace(".", "-")
    local_leap = leap_month
    if normalized.startswith("闰"):
        local_leap = True
        normalized = normalized[1:]

    parts = [part for part in normalized.split("-") if part]
    if len(parts) not in (2, 3):
        raise ValueError("生日格式不正确。请使用 YYYY-MM-DD、MM-DD、农历:8-15 或 公历:1990-03-14。")

    numbers = [int(part) for part in parts]
    year = None
    if len(numbers) == 3:
        year, month, day = numbers
    else:
        month, day = numbers

    if calendar == "solar":
        _ = date(year or 2000, month, day)
        return {
            "source": "manual",
            "calendar": "solar",
            "month": month,
            "day": day,
            "year": year,
            "leap_month": False,
        }

    target_year = year or date.today().year
    ensure_supported_year(target_year)
    _ = lunar_to_solar(LunarDate(target_year, month, day, local_leap))
    return {
        "source": "manual",
        "calendar": "lunar",
        "month": month,
        "day": day,
        "year": year,
        "leap_month": local_leap,
    }


def ensure_data_file(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(json.dumps({"records": []}, ensure_ascii=False, indent=2), encoding="utf-8")


def load_data(path: Path) -> Dict[str, Any]:
    ensure_data_file(path)
    return json.loads(path.read_text(encoding="utf-8"))


def save_data(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def ensure_notification_config(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(
            json.dumps(DEFAULT_NOTIFICATION_TEMPLATE, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def resolve_config_value(value: Any) -> Any:
    if isinstance(value, str):
        match = re.fullmatch(r"\$\{([A-Z0-9_]+)\}", value)
        if match:
            return os.environ.get(match.group(1), "")
        return value
    if isinstance(value, list):
        return [resolve_config_value(item) for item in value]
    if isinstance(value, dict):
        return {key: resolve_config_value(item) for key, item in value.items()}
    return value


def find_record(records: List[Dict[str, Any]], name: str) -> Optional[Dict[str, Any]]:
    for record in records:
        if record["name"] == name:
            return record
    return None


def birthday_storage_text(record: Dict[str, Any]) -> str:
    prefix = "农历" if record["calendar"] == "lunar" else "公历"
    leap = "闰" if record.get("leap_month") else ""
    year = f"{record['year']}年" if record.get("year") else ""
    return f"{prefix} {year}{leap}{record['month']}月{record['day']}日"


def resolve_next_solar_birthday(record: Dict[str, Any], today: date) -> date:
    if record["calendar"] == "solar":
        current = date(today.year, record["month"], record["day"])
        if current < today:
            current = date(today.year + 1, record["month"], record["day"])
        return current

    for target_year in (today.year, today.year + 1):
        leap_requested = record.get("leap_month", False)
        candidates = [leap_requested]
        if leap_requested:
            # 闰月生日在目标年份没有同名闰月时，回退到同月的非闰月日期。
            candidates.append(False)

        converted = None
        for is_leap in candidates:
            try:
                converted = lunar_to_solar(
                    LunarDate(
                        year=target_year,
                        month=record["month"],
                        day=record["day"],
                        is_leap=is_leap,
                    )
                )
                break
            except ValueError:
                continue
        if converted is None:
            continue
        if converted >= today:
            return converted

    raise ValueError(f"无法为 {record['name']} 计算下一次生日。")


def compute_turning_age(record: Dict[str, Any], solar_birthday: date) -> Optional[int]:
    if not record.get("year"):
        return None
    return solar_birthday.year - int(record["year"])


def build_summary(record: Dict[str, Any], today: date) -> Dict[str, Any]:
    next_birthday = resolve_next_solar_birthday(record, today)
    remind_before = int(record.get("remind_before_days", 1))
    remind_date = next_birthday - timedelta(days=remind_before)
    return {
        "name": record["name"],
        "storage": birthday_storage_text(record),
        "next_birthday": next_birthday.isoformat(),
        "days_until_birthday": (next_birthday - today).days,
        "remind_before_days": remind_before,
        "next_remind_date": remind_date.isoformat(),
        "days_until_remind": (remind_date - today).days,
        "turning_age": compute_turning_age(record, next_birthday),
    }


def load_notification_channels(path: Path) -> List[Dict[str, Any]]:
    ensure_notification_config(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    data = resolve_config_value(data)
    channels = data.get("channels", [])
    enabled_channels = [channel for channel in channels if channel.get("enabled", True)]
    return enabled_channels or [{"type": "agent"}]


def emit_openclaw_scheduler_hint(data_file: Path, notification_config: Path) -> None:
    current = str(Path.cwd()).lower()
    if "openclaw" not in current and "CODEX_HOME" not in os.environ:
        return
    hint = {
        "name": "生日提醒检查",
        "prompt": (
            f"运行 python3 {Path(__file__).resolve()} --data-file {data_file} "
            f"--notification-config {notification_config} check，并处理输出中的提醒结果。"
        ),
        "rrule": "FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR,SA,SU;BYHOUR=9;BYMINUTE=0",
        "cwds": str(Path(__file__).resolve().parents[1]),
        "status": "ACTIVE",
    }
    print(f"OPENCLAW_AUTOMATION_SUGGESTION {json.dumps(hint, ensure_ascii=False)}")


def dispatch_notifications(matches: List[Dict[str, Any]], config_path: Path) -> None:
    if not matches:
        return
    channels = load_notification_channels(config_path)
    lines = []
    for item in matches:
        age_text = f"，这次过 {item['turning_age']} 岁" if item["turning_age"] is not None else ""
        lines.append(
            f"生日提醒：{item['name']}（{item['storage']}）将在 {item['next_birthday']} 过生日，"
            f"今天需要提醒，已提前 {item['remind_before_days']} 天设置{age_text}。"
        )
    message = "\n".join(lines)

    for channel in channels:
        channel_type = channel.get("type", "agent")
        if channel_type == "agent":
            print(f"AGENT_NOTIFICATION\n{message}")
            continue
        if channel_type == "stdout":
            print(message)
            continue
        if channel_type == "email":
            recipients = [item for item in channel.get("to", []) if item]
            host = channel.get("host")
            if not recipients or not host:
                print("通知失败：email 渠道缺少 host 或 to 配置。")
                continue
            email_message = EmailMessage()
            email_message["Subject"] = channel.get("subject", "生日提醒")
            email_message["From"] = channel.get("from") or channel.get("username") or "birthday-reminder@localhost"
            email_message["To"] = ", ".join(recipients)
            email_message.set_content(message)
            try:
                port = int(channel.get("port") or 587)
                with smtplib.SMTP(host, port, timeout=10) as smtp:
                    if channel.get("use_tls", True):
                        smtp.starttls()
                    username = channel.get("username")
                    password = channel.get("password")
                    if username:
                        smtp.login(username, password or "")
                    smtp.send_message(email_message)
            except Exception as exc:
                print(f"通知失败：email 渠道发送异常，原因：{exc}")
            continue
        if channel_type == "webhook":
            payload = json.dumps({"text": message}, ensure_ascii=False).encode("utf-8")
            headers = {"Content-Type": "application/json"}
            headers.update(channel.get("headers", {}))
            req = request.Request(channel["url"], data=payload, headers=headers, method="POST")
            try:
                with request.urlopen(req, timeout=10):
                    pass
            except error.URLError as exc:
                print(f"通知失败：webhook {channel['url']}，原因：{exc}")


def build_record_from_input(
    name: str,
    value: str,
    calendar: Optional[str],
    remind_before: int,
    leap_month: bool,
) -> Dict[str, Any]:
    if is_idcard_value(value):
        solar_birthday = parse_idcard_birthday(value)
        target_calendar = calendar or "lunar"
        if target_calendar == "lunar":
            lunar = solar_to_lunar(solar_birthday)
            return {
                "name": name,
                "calendar": "lunar",
                "month": lunar.month,
                "day": lunar.day,
                "year": lunar.year,
                "leap_month": lunar.is_leap,
                "remind_before_days": remind_before,
                "source": "idcard",
                "idcard_masked": mask_idcard(value),
                "solar_birthday": solar_birthday.isoformat(),
                "created_at": datetime.now().isoformat(timespec="seconds"),
            }
        return {
            "name": name,
            "calendar": "solar",
            "month": solar_birthday.month,
            "day": solar_birthday.day,
            "year": solar_birthday.year,
            "leap_month": False,
            "remind_before_days": remind_before,
            "source": "idcard",
            "idcard_masked": mask_idcard(value),
            "solar_birthday": solar_birthday.isoformat(),
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

    parsed = parse_birthday_value(value, calendar, leap_month)
    parsed.update(
        {
            "name": name,
            "remind_before_days": remind_before,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
    )
    return parsed


def upsert_record(path: Path, record: Dict[str, Any]) -> Dict[str, bool]:
    data = load_data(path)
    records = data.setdefault("records", [])
    first_add = len(records) == 0
    existing = find_record(records, record["name"])
    if existing:
        existing.update(record)
        created = False
    else:
        records.append(record)
        created = True
    save_data(path, data)
    return {"created": created, "first_add": first_add and created}


def add_auto(args: argparse.Namespace) -> None:
    record = build_record_from_input(
        args.name,
        args.value,
        args.calendar,
        args.remind_before,
        args.leap_month,
    )
    result = upsert_record(args.data_file, record)
    print(f"已保存：{args.name}，{birthday_storage_text(record)}，提前 {args.remind_before} 天提醒。")
    if result["first_add"]:
        emit_openclaw_scheduler_hint(args.data_file, args.notification_config)


def add_idcard(args: argparse.Namespace) -> None:
    args.value = args.idcard
    args.leap_month = False
    add_auto(args)


def add_manual(args: argparse.Namespace) -> None:
    prefix = "公历:" if args.calendar == "solar" else "农历:"
    leap = "闰" if args.leap_month and args.calendar == "lunar" else ""
    value = f"{prefix}{leap}"
    if args.year:
        value += f"{args.year}-"
    value += f"{args.month}-{args.day}"
    args.value = value
    add_auto(args)


def remove_record(args: argparse.Namespace) -> None:
    data = load_data(args.data_file)
    records = data.setdefault("records", [])
    before = len(records)
    data["records"] = [record for record in records if record["name"] != args.name]
    if len(data["records"]) == before:
        print(f"未找到记录：{args.name}")
        return
    save_data(args.data_file, data)
    print(f"已删除：{args.name}")


def list_records(args: argparse.Namespace) -> None:
    data = load_data(args.data_file)
    today = parse_today(args.today)
    records = data.get("records", [])
    if not records:
        print("暂无生日记录。")
        return

    items = [build_summary(record, today) for record in records]
    items.sort(key=lambda item: item["days_until_birthday"])
    for item in items:
        if args.upcoming and item["days_until_birthday"] > args.days:
            continue
        age_text = f"，即将 {item['turning_age']} 岁" if item["turning_age"] is not None else ""
        print(
            f"{item['name']} | {item['storage']} | 下次公历生日 {item['next_birthday']} | "
            f"还有 {item['days_until_birthday']} 天{age_text} | 提醒日 {item['next_remind_date']}"
        )


def show_next(args: argparse.Namespace) -> None:
    data = load_data(args.data_file)
    today = parse_today(args.today)
    records = data.get("records", [])
    if not records:
        print("暂无生日记录。")
        return
    items = [build_summary(record, today) for record in records]
    items.sort(key=lambda item: item["days_until_birthday"])
    item = items[0]
    print(
        f"最近生日：{item['name']}，{item['storage']}，"
        f"下次公历生日 {item['next_birthday']}，还有 {item['days_until_birthday']} 天。"
    )


def check_reminders(args: argparse.Namespace) -> None:
    data = load_data(args.data_file)
    today = parse_today(args.today)
    records = data.get("records", [])
    if not records:
        return

    results = []
    for record in records:
        item = build_summary(record, today)
        if item["days_until_remind"] == 0:
            results.append(item)

    results.sort(key=lambda item: item["next_birthday"])
    dispatch_notifications(results, args.notification_config)


def parse_today(raw: Optional[str]) -> date:
    if raw:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    return date.today()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="农历/公历生日提醒管理")
    parser.add_argument("--data-file", type=Path, default=DEFAULT_DATA_FILE, help="生日数据文件路径")
    parser.add_argument(
        "--notification-config",
        type=Path,
        default=DEFAULT_NOTIFICATION_CONFIG,
        help="通知渠道配置文件路径",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="自动识别身份证或生日文本并添加记录")
    add_parser.add_argument("name", help="姓名")
    add_parser.add_argument("value", help="身份证号或生日文本")
    add_parser.add_argument("--calendar", choices=["lunar", "solar"], help="保存口径，默认农历")
    add_parser.add_argument("--leap-month", action="store_true", help="仅对农历生日生效")
    add_parser.add_argument("--remind-before", type=int, default=1, help="提前几天提醒，默认 1")
    add_parser.set_defaults(func=add_auto)

    add_idcard_parser = subparsers.add_parser("add-idcard", help="从身份证添加生日")
    add_idcard_parser.add_argument("name", help="姓名")
    add_idcard_parser.add_argument("idcard", help="15 位或 18 位中国身份证号码")
    add_idcard_parser.add_argument(
        "--calendar",
        choices=["lunar", "solar"],
        default="lunar",
        help="保存口径，默认保存为农历",
    )
    add_idcard_parser.add_argument("--remind-before", type=int, default=1, help="提前几天提醒，默认 1")
    add_idcard_parser.set_defaults(func=add_idcard)

    add_manual_parser = subparsers.add_parser("add-manual", help="手动添加生日")
    add_manual_parser.add_argument("name", help="姓名")
    add_manual_parser.add_argument("--calendar", choices=["lunar", "solar"], default="lunar")
    add_manual_parser.add_argument("--month", type=int, required=True, help="月份")
    add_manual_parser.add_argument("--day", type=int, required=True, help="日期")
    add_manual_parser.add_argument("--year", type=int, help="出生年份，可选")
    add_manual_parser.add_argument("--leap-month", action="store_true", help="农历闰月生日")
    add_manual_parser.add_argument("--remind-before", type=int, default=1, help="提前几天提醒，默认 1")
    add_manual_parser.set_defaults(func=add_manual)

    list_parser = subparsers.add_parser("list", help="列出生日记录")
    list_parser.add_argument("--upcoming", action="store_true", help="仅显示近期生日")
    list_parser.add_argument("--days", type=int, default=30, help="近期范围，默认 30 天")
    list_parser.add_argument("--today", help="指定今天日期，格式 YYYY-MM-DD")
    list_parser.set_defaults(func=list_records)

    next_parser = subparsers.add_parser("next", help="查看最近一个生日")
    next_parser.add_argument("--today", help="指定今天日期，格式 YYYY-MM-DD")
    next_parser.set_defaults(func=show_next)

    check_parser = subparsers.add_parser("check", help="检查今天需要发送的提醒")
    check_parser.add_argument("--today", help="指定今天日期，格式 YYYY-MM-DD")
    check_parser.set_defaults(func=check_reminders)

    remove_parser = subparsers.add_parser("remove", help="删除记录")
    remove_parser.add_argument("name", help="姓名")
    remove_parser.set_defaults(func=remove_record)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if hasattr(args, "remind_before") and args.remind_before < 0:
        raise SystemExit("提前提醒天数不能小于 0。")
    args.func(args)


if __name__ == "__main__":
    main()
