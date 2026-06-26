#!/usr/bin/env python
"""
状态巡检引擎：每次被 /loop 触发时执行一次。

读取 itinerary.json → 更新节点状态 → 应用触发规则 → 调用生成脚本 → print 输出。

用法: python run_cron.py
  或: python run_cron.py --check-only
输出: 渲染后的 Markdown 消息到 stdout（如果触发），否则静默退出
"""

import argparse
import json
import random
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = SKILL_DIR.parent.parent
SKILL_DIR_STR = str(SKILL_DIR)
DATA_DIR = PROJECT_ROOT / "data"


def load_itinerary() -> dict | None:
    """加载行程数据。无行程时返回 None。"""
    path = DATA_DIR / "itinerary.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        itinerary = json.load(f)
    if not itinerary.get("nodes"):
        return None
    return itinerary


def save_itinerary(itinerary: dict):
    """回写行程数据。"""
    path = DATA_DIR / "itinerary.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(itinerary, f, ensure_ascii=False, indent=2)


def parse_time(time_str: str) -> datetime:
    """解析 ISO 8601 时间字符串为 UTC datetime。"""
    if time_str.endswith("Z"):
        time_str = time_str[:-1] + "+00:00"
    return datetime.fromisoformat(time_str)


def update_statuses(itinerary: dict, now: datetime) -> list[dict]:
    """更新所有节点状态，返回刚变为 ACTIVE 的节点列表。"""
    just_activated = []

    for node in itinerary["nodes"]:
        start = parse_time(node["start_time"])
        end = parse_time(node["end_time"])
        old_status = node["status"]

        if now < start:
            node["status"] = "PENDING"
        elif start <= now <= end:
            node["status"] = "ACTIVE"
        else:
            node["status"] = "COMPLETED"

        if old_status == "PENDING" and node["status"] == "ACTIVE":
            just_activated.append(node)

    return just_activated


def should_send(node: dict, itinerary: dict, now: datetime, just_activated: bool) -> bool:
    """判断是否应该对该节点发送消息。"""
    last_posted_str = itinerary.get("last_posted_at")
    if last_posted_str:
        last_posted = parse_time(last_posted_str)
        gap_minutes = (now - last_posted).total_seconds() / 60
    else:
        gap_minutes = float("inf")

    if just_activated:
        return True

    if gap_minutes < 45:
        return False

    if node["state_type"] == "attraction" and node["message_count"] == 0:
        return True

    if node["state_type"] == "attraction":
        if node["message_count"] == 1:
            return random.random() < 0.4
        elif node["message_count"] == 2:
            return random.random() < 0.1

    return False


def generate_and_render(node: dict, itinerary: dict) -> str | None:
    """调用 generate_post.py 生成内容，再调用 render_output.py 渲染模板。"""
    node_id = node["node_id"]

    result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "generate_post.py"), node_id],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
        env={**subprocess.os.environ, "SKILL_DIR": SKILL_DIR_STR},
    )

    if result.returncode != 0:
        print(f"Error generating post for {node_id}: {result.stderr}", file=sys.stderr)
        return None

    stdout_lines = result.stdout.strip().split("\n")
    try:
        post_data = json.loads(stdout_lines[-1])
    except (json.JSONDecodeError, IndexError):
        print(f"Error parsing generate_post output for {node_id}", file=sys.stderr)
        return None

    meta = node.get("meta_data", {})
    context = {
        "state_type": node["state_type"],
        "message_count": node["message_count"],
        "local_time": post_data.get("local_time", ""),
        "text_content": post_data.get("text_content", ""),
        "image_url": post_data.get("image_path", ""),
        "destination": itinerary.get("destination", ""),
        "location": meta.get("location", ""),
        "weather_desc": meta.get("weather_desc", ""),
        "weather_forecast": meta.get("weather_desc", ""),
        "temperature": meta.get("temperature", ""),
        "airport_or_station": meta.get("airport_or_station", ""),
        "transport_type": meta.get("transport_type", ""),
        "home_base": "家",
        "trip_summary": f"这次{itinerary.get('destination', '')}之旅，很开心。",
        "highlights": "\n".join(f"- {h}" for h in meta.get("highlights", [])),
        "caption": post_data.get("text_content", ""),
    }

    context_json = json.dumps(context, ensure_ascii=False)
    result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "render_output.py"), "--context", context_json],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
        env={**subprocess.os.environ, "SKILL_DIR": SKILL_DIR_STR},
    )

    if result.returncode != 0:
        print(f"Error rendering output for {node_id}: {result.stderr}", file=sys.stderr)
        return None

    return result.stdout


def check_status() -> str:
    """仅检查状态，不发送消息。"""
    itinerary = load_itinerary()
    if not itinerary:
        return "No active trip."

    active_nodes = [n for n in itinerary.get("nodes", []) if n.get("status") == "ACTIVE"]
    completed = len([n for n in itinerary.get("nodes", []) if n.get("status") == "COMPLETED"])
    total = len(itinerary.get("nodes", []))

    lines = [
        f"Destination: {itinerary.get('destination', 'N/A')}",
        f"Dates: {itinerary.get('start_date', 'N/A')} - {itinerary.get('end_date', 'N/A')}",
        f"Progress: {completed}/{total} nodes completed",
    ]

    if active_nodes:
        for n in active_nodes:
            lines.append(f"Current: {n['node_id']} ({n['meta_data'].get('location', 'N/A')}) - {n['meta_data'].get('state_type', '')}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Trip heartbeat engine")
    parser.add_argument("--check-only", action="store_true", help="Only check status, do not send messages")
    args = parser.parse_args()

    if args.check_only:
        print(check_status())
        return

    itinerary = load_itinerary()
    if not itinerary:
        sys.exit(0)

    now = datetime.now(timezone.utc)

    just_activated_nodes = update_statuses(itinerary, now)
    just_activated_ids = {n["node_id"] for n in just_activated_nodes}

    messages_sent = False
    for node in itinerary["nodes"]:
        if node["status"] != "ACTIVE":
            continue

        is_just_activated = node["node_id"] in just_activated_ids
        if not should_send(node, itinerary, now, is_just_activated):
            continue

        output = generate_and_render(node, itinerary)
        if output:
            print(output)
            node["message_count"] += 1
            itinerary["last_posted_at"] = now.isoformat()
            messages_sent = True
            break

    save_itinerary(itinerary)

    if not messages_sent:
        pass


if __name__ == "__main__":
    main()
