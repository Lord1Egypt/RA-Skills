#!/usr/bin/env python3
"""
候补会议室轮询 - 定期检查候补队列中的日程是否有空闲会议室

用法:
  # 检查候补队列状态
  python3 watch_waitlist.py --status

  # 执行一轮轮询（尝试为候补日程预订会议室）
  python3 watch_waitlist.py --poll

  # 添加到候补队列
  python3 watch_waitlist.py --add --event-id "xxx" --summary "周会" \
    --start "2026-04-20T14:00:00+08:00" --end "2026-04-20T15:00:00+08:00" \
    --building "丽金" --capacity-gte 8

  # 移除候补
  python3 watch_waitlist.py --remove --event-id "xxx"

  # 清理已过期的候补
  python3 watch_waitlist.py --clean
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional

SCRIPT_DIR = Path(__file__).parent
WAITLIST_FILE = SCRIPT_DIR.parent / "references" / "room-waitlist.json"
QUERY_SCRIPT = SCRIPT_DIR / "query_rooms.py"
WaitlistItem = dict[str, Any]
WaitlistData = dict[str, list[WaitlistItem]]


def load_waitlist() -> WaitlistData:
    if not WAITLIST_FILE.exists():
        return {"pending": []}
    with open(WAITLIST_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("候补队列文件格式错误: 顶层必须是对象")
    pending = data.get("pending", [])
    if not isinstance(pending, list):
        raise ValueError("候补队列文件格式错误: pending 必须是数组")

    normalized_pending = [item for item in pending if isinstance(item, dict)]
    if len(normalized_pending) != len(pending):
        raise ValueError("候补队列文件格式错误: pending 项必须是对象")
    return {"pending": normalized_pending}


def save_waitlist(data: WaitlistData) -> None:
    with open(WAITLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def show_status() -> None:
    """查看候补队列状态"""
    data = load_waitlist()
    pending = data.get("pending", [])
    if not pending:
        print("📭 候补队列为空")
        return
    print(f"📋 候补队列 ({len(pending)} 条):")
    for i, item in enumerate(pending, 1):
        event_id = item.get("event_id", "unknown")
        summary = item.get("summary", "")
        start = item.get("time", "")
        building = item.get("building", "")
        attempts = item.get("attempts", 0)
        print(f"  {i}. {summary}")
        print(f"     时间: {start}")
        print(f"     楼栋: {building}")
        print(f"     尝试次数: {attempts}")


def add_waitlist(args: argparse.Namespace) -> None:
    """添加到候补队列"""
    data = load_waitlist()
    pending = data.setdefault("pending", [])

    # 检查是否已存在
    event_id = args.event_id
    for item in pending:
        if item.get("event_id") == event_id:
            print(f"⚠️ {event_id} 已在候补队列中")
            return

    pending.append({
        "event_id": event_id,
        "summary": args.summary or "",
        "start": args.start,
        "end": args.end,
        "building": args.building or "",
        "capacity_gte": args.capacity_gte or 0,
        "attempted_rooms": [],
        "attempts": 0,
        "added_at": datetime.now().isoformat(),
        "status": "waiting"
    })
    save_waitlist(data)
    print(f"✅ 已加入候补: {args.summary} ({args.start})")


def remove_waitlist(event_id: str) -> None:
    """从候补队列移除"""
    data = load_waitlist()
    pending = data.get("pending", [])
    new_pending = [item for item in pending if item.get("event_id") != event_id]
    if len(new_pending) == len(pending):
        print(f"⚠️ {event_id} 不在候补队列中")
        return
    data["pending"] = new_pending
    save_waitlist(data)
    print(f"✅ 已从候补移除: {event_id}")


def clean_expired() -> None:
    """清理已过期的候补"""
    data = load_waitlist()
    pending = data.get("pending", [])
    now = datetime.now(timezone.utc)

    # 简单判断：如果 start 时间已过去 1 小时，认为过期
    active = []
    removed = 0
    for item in pending:
        start_str = item.get("start", "")
        if start_str:
            try:
                start_dt = datetime.fromisoformat(start_str)
                if start_dt.tzinfo is None:
                    start_dt = start_dt.replace(tzinfo=timezone.utc)
                if start_dt < now - timedelta(hours=1):
                    removed += 1
                    continue
            except ValueError:
                pass
        active.append(item)

    if removed > 0:
        data["pending"] = active
        save_waitlist(data)
        print(f"🧹 清理了 {removed} 条过期候补")
    else:
        print("✅ 没有过期候补")


def apply_verification_result(
    item: dict[str, Any],
    verification_status: str,
    verification_reason: str,
    *,
    verified_at: Optional[str] = None,
) -> tuple[Optional[dict[str, Any]], bool]:
    updated_item = dict(item)
    timestamp = verified_at or datetime.now().isoformat()
    updated_item["last_verification_status"] = verification_status
    updated_item["last_verification_reason"] = verification_reason
    updated_item["last_verified_at"] = timestamp

    if verification_status == "confirmed":
        return None, True

    if verification_status == "pending":
        updated_item["status"] = "verification_pending"
        return updated_item, False

    attempted_rooms = [room_id for room_id in updated_item.get("attempted_rooms", []) if room_id]
    suggested_room_id = updated_item.get("suggested_room_id")
    if suggested_room_id and suggested_room_id not in attempted_rooms:
        attempted_rooms.append(suggested_room_id)
    updated_item["attempted_rooms"] = attempted_rooms
    updated_item["status"] = "waiting"
    updated_item.pop("suggested_room", None)
    updated_item.pop("suggested_room_id", None)
    return updated_item, False


def poll_waitlist() -> None:
    """执行一轮候补轮询"""
    data = load_waitlist()
    pending = data.get("pending", [])
    if not pending:
        print("📭 候补队列为空，无需轮询")
        return

    updated = False
    results = []

    for item in pending:
        if item.get("status") not in {"waiting", "verification_pending"}:
            continue

        event_id = item["event_id"]
        start = item.get("start", "")
        end = item.get("end", "")
        building = item.get("building", "")
        cap_gte = item.get("capacity_gte", 0)
        attempted = set(item.get("attempted_rooms", []))

        print(f"\n🔍 检查: {item.get('summary', event_id)}")
        print(f"   时间: {start} ~ {end}")

        # 用查询脚本查空闲会议室
        cmd = [
            sys.executable, str(QUERY_SCRIPT),
            "-b", building,
            "-s", start,
            "-e", end,
            "-o", "json"
        ]
        if cap_gte:
            cmd.extend(["--capacity-gte", str(cap_gte)])

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode != 0:
                print(f"   ❌ 查询失败: {result.stderr}")
                item["attempts"] = item.get("attempts", 0) + 1
                updated = True
                continue

            rooms = json.loads(result.stdout)
            # 找到空闲且未尝试过的会议室
            free_room = None
            for room in rooms:
                if room.get("status") == "free" and room.get("room_id") not in attempted:
                    free_room = room
                    break

            if free_room:
                room_name = free_room["name"]
                room_id = free_room["room_id"]
                print(f"   🟢 找到空闲: {room_name}")
                print(f"   ⏳ 等待 agent 执行预订...")
                item["status"] = "ready"
                item["suggested_room"] = room_name
                item["suggested_room_id"] = room_id
                results.append({
                    "event_id": event_id,
                    "action": "book",
                    "room_name": room_name,
                    "room_id": room_id,
                    "summary": item.get("summary", "")
                })
            else:
                # 没有空闲，更新已尝试列表
                new_attempted = set(attempted)
                for room in rooms:
                    new_attempted.add(room.get("room_id", ""))
                item["attempted_rooms"] = list(new_attempted)
                item["attempts"] = item.get("attempts", 0) + 1
                print(f"   🔴 仍然没有空闲会议室 (已尝试 {item['attempts']} 次)")

            updated = True

        except subprocess.TimeoutExpired:
            print(f"   ⏱️ 查询超时")
            item["attempts"] = item.get("attempts", 0) + 1
            updated = True

    if updated:
        save_waitlist(data)

    if results:
        print(f"\n🎉 有 {len(results)} 个候补可以预订:")
        for r in results:
            print(f"  📌 {r['summary']} → {r['room_name']} ({r['room_id']})")
        print("\n请 agent 执行以下操作:")
        print("  1. 对每个 result，调用 feishu_calendar_event_attendee create 添加会议室")
        print("  2. 等待 5 秒验证 RSVP")
        print("  3. accept → 从候补移除；decline → 保持 waiting")
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print("\n📭 本轮轮询没有可用会议室")


def main() -> None:
    parser = argparse.ArgumentParser(description="候补会议室轮询")
    parser.add_argument("--status", action="store_true", help="查看候补状态")
    parser.add_argument("--poll", action="store_true", help="执行一轮轮询")
    parser.add_argument("--add", action="store_true", help="添加候补")
    parser.add_argument("--remove", action="store_true", help="移除候补")
    parser.add_argument("--clean", action="store_true", help="清理过期候补")
    parser.add_argument("--event-id", help="日程 ID")
    parser.add_argument("--summary", help="会议标题")
    parser.add_argument("--start", "-s", help="开始时间")
    parser.add_argument("--end", "-e", help="结束时间")
    parser.add_argument("--building", "-b", help="楼栋")
    parser.add_argument("--capacity-gte", "-c", type=int, help="最小容量")

    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.poll:
        poll_waitlist()
    elif args.add:
        if not args.event_id or not args.start or not args.end:
            print("错误: --add 需要 --event-id, --start, --end")
            sys.exit(1)
        add_waitlist(args)
    elif args.remove:
        if not args.event_id:
            print("错误: --remove 需要 --event-id")
            sys.exit(1)
        remove_waitlist(args.event_id)
    elif args.clean:
        clean_expired()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
