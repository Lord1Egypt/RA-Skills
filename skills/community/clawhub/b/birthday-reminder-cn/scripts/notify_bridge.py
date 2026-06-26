#!/usr/bin/env python3
"""生日提醒通知桥接器。

把 birthday_reminder.py 的到期提醒分发到多个通知通道。
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import urllib.request
from pathlib import Path

from birthday_reminder import DEFAULT_TZ, check_due, load_config, parse_now


def post_json(url: str, payload: dict, timeout: int = 10) -> None:
    req = urllib.request.Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout):
        pass


def _format_datetime(iso_str: str) -> str:
    try:
        ts = dt.datetime.fromisoformat(iso_str)
        return ts.strftime("%m-%d %H:%M")
    except Exception:
        return iso_str


def format_text(rows: list[dict], style: str = "warm") -> str:
    normalized = (style or "warm").strip().lower()
    if normalized not in {"warm", "simple"}:
        normalized = "warm"

    if normalized == "simple":
        lines = [f"生日提醒（共 {len(rows)} 条）"]
        for row in rows:
            phase = "今天生日" if row["offset_days"] == 0 else f"还有 {row['offset_days']} 天"
            cal = "阳历" if row["calendar"] == "solar" else "农历"
            remind_time = _format_datetime(row["remind_at"])
            lines.append(
                f"- {row['name']}：{phase}｜{cal}生日 {row['birthday_date']}｜提醒 {remind_time}"
            )
        return "\n".join(lines)

    lines = [f"🎂 生日小提醒（共 {len(rows)} 条）"]
    for row in rows:
        phase = "就是今天" if row["offset_days"] == 0 else f"还有 {row['offset_days']} 天"
        cal = "阳历" if row["calendar"] == "solar" else "农历"
        remind_time = _format_datetime(row["remind_at"])
        lines.append(
            f"🎉 {row['name']}：{phase}过生日（{cal} {row['birthday_date']}），提醒时间 {remind_time}"
        )
    return "\n".join(lines)


def send_console(text: str, _channel: dict) -> None:
    print(text)


def send_file(text: str, channel: dict) -> None:
    path = Path(channel["path"])
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(text + "\n")


def send_webhook(text: str, rows: list[dict], channel: dict) -> None:
    payload = channel.get("payload_template", {"text": "{text}"})

    def replace(value):
        if isinstance(value, str):
            return value.replace("{text}", text)
        if isinstance(value, dict):
            return {k: replace(v) for k, v in value.items()}
        if isinstance(value, list):
            return [replace(v) for v in value]
        return value

    body = replace(payload)
    if "{rows}" in json.dumps(payload, ensure_ascii=False):
        body = json.loads(json.dumps(body, ensure_ascii=False).replace("{rows}", json.dumps(rows, ensure_ascii=False)))
    post_json(channel["url"], body)


def send_feishu(text: str, channel: dict) -> None:
    post_json(
        channel["webhook"],
        {"msg_type": "text", "content": {"text": text}},
    )


def send_dingtalk(text: str, channel: dict) -> None:
    post_json(
        channel["webhook"],
        {"msgtype": "text", "text": {"content": text}},
    )


def send_slack(text: str, channel: dict) -> None:
    post_json(
        channel["webhook"],
        {"text": text},
    )


def send_telegram(text: str, channel: dict) -> None:
    token = channel["bot_token"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    post_json(url, {"chat_id": channel["chat_id"], "text": text})


SENDERS = {
    "console": lambda text, rows, c: send_console(text, c),
    "file": lambda text, rows, c: send_file(text, c),
    "webhook": lambda text, rows, c: send_webhook(text, rows, c),
    "feishu": lambda text, rows, c: send_feishu(text, c),
    "dingtalk": lambda text, rows, c: send_dingtalk(text, c),
    "slack": lambda text, rows, c: send_slack(text, c),
    "telegram": lambda text, rows, c: send_telegram(text, c),
}


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    parser = argparse.ArgumentParser(description="生日提醒通知桥接器")
    parser.add_argument("--birthday-config", required=True, help="生日配置 JSON 路径")
    parser.add_argument("--notify-config", required=True, help="通知配置 JSON 路径")
    parser.add_argument("--window-minutes", type=int, default=70, help="检查窗口（分钟）")
    parser.add_argument("--now", default=None, help="测试时间，例如 2026-03-25 09:00:00")
    parser.add_argument("--dry-run", action="store_true", help="只打印，不实际发送")
    args = parser.parse_args()

    birthday_config = load_config(args.birthday_config)
    notify_config = load_json(args.notify_config)

    tz_name = birthday_config.get("defaults", {}).get("timezone", DEFAULT_TZ)
    now = parse_now(args.now, tz_name)
    rows = check_due(birthday_config, now, args.window_minutes)
    if not rows:
        return 0

    style = notify_config.get("message_style", "warm")
    text = format_text(rows, style=style)
    channels = notify_config.get("channels", [])
    if not isinstance(channels, list):
        raise ValueError("notify config: channels 必须是数组")

    for channel in channels:
        if not channel.get("enabled", True):
            continue
        channel_type = channel.get("type")
        sender = SENDERS.get(channel_type)
        if not sender:
            raise ValueError(f"不支持的通知类型: {channel_type}")
        if args.dry_run:
            print(f"[dry-run] {channel_type}: {text}")
            continue
        sender(text, rows, channel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
