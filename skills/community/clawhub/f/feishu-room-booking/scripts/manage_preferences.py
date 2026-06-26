#!/usr/bin/env python3
"""
用户会议室偏好管理

用法:
  # 设置偏好
  python3 manage_preferences.py --set --user "ou_xxx" --building "丽金" --capacity-gte 8 --preferred-rooms "F11-07,F11-15" --note "偏好靠近电梯"

  # 读取偏好
  python3 manage_preferences.py --get --user "ou_xxx"

  # 学习偏好（根据历史选择自动更新）
  python3 manage_preferences.py --learn --user "ou_xxx" --room "F11-15(8)" --building "丽金智地中心 B座"

  # 列出所有用户偏好
  python3 manage_preferences.py --list

  # 删除偏好
  python3 manage_preferences.py --delete --user "ou_xxx"
"""

import argparse
import json
import sys
from pathlib import Path
from collections import Counter

SCRIPT_DIR = Path(__file__).parent
PREFS_FILE = SCRIPT_DIR.parent / "references" / "user-preferences.json"

LEARN_THRESHOLD = 3  # 连续选择同一会议室 3 次后自动标记为偏好


def load_prefs():
    if not PREFS_FILE.exists():
        return {"preferences": {}}
    with open(PREFS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_prefs(data):
    with open(PREFS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def set_preference(user_id, args):
    """设置用户偏好"""
    data = load_prefs()
    prefs = data.setdefault("preferences", {})
    prefs[user_id] = {
        "default_building": args.building or "",
        "capacity_gte": args.capacity_gte or 0,
        "capacity_lte": args.capacity_lte or 999,
        "preferred_rooms": [r.strip() for r in args.preferred_rooms.split(",")] if args.preferred_rooms else [],
        "note": args.note or "",
        "selection_history": prefs.get(user_id, {}).get("selection_history", [])
    }
    save_prefs(data)
    print(f"✅ 已保存 {user_id} 的偏好:")
    print(json.dumps(prefs[user_id], ensure_ascii=False, indent=2))


def get_preference(user_id):
    """获取用户偏好"""
    data = load_prefs()
    prefs = data.get("preferences", {}).get(user_id)
    if not prefs:
        print(f"❌ 未找到 {user_id} 的偏好设置")
        return None
    print(json.dumps(prefs, ensure_ascii=False, indent=2))
    return prefs


def learn_preference(user_id, room_name, building_name):
    """根据用户选择学习偏好"""
    data = load_prefs()
    prefs = data.setdefault("preferences", {})

    user_prefs = prefs.get(user_id, {
        "default_building": "",
        "capacity_gte": 0,
        "capacity_lte": 999,
        "preferred_rooms": [],
        "note": "",
        "selection_history": []
    })

    # 记录选择历史
    history = user_prefs.setdefault("selection_history", [])
    history.append({
        "room": room_name,
        "building": building_name,
        "time": __import__("datetime").datetime.now().isoformat()
    })
    # 只保留最近 20 条
    user_prefs["selection_history"] = history[-20:]

    # 更新默认楼栋（最近 3 次选择的楼栋）
    recent_buildings = [h["building"] for h in history[-3:] if h["building"]]
    if len(set(recent_buildings)) == 1 and recent_buildings[0]:
        user_prefs["default_building"] = recent_buildings[0]

    # 统计会议室选择频率
    room_counts = Counter(h["room"] for h in history)
    most_common = room_counts.most_common(3)

    # 更新偏好会议室（选择次数 >= LEARN_THRESHOLD 的）
    preferred = [room for room, count in most_common if count >= LEARN_THRESHOLD]
    if preferred:
        # 去重并保持顺序
        seen = set()
        unique_preferred = []
        for r in preferred:
            if r not in seen:
                seen.add(r)
                unique_preferred.append(r)
        user_prefs["preferred_rooms"] = unique_preferred

    prefs[user_id] = user_prefs
    save_prefs(data)

    print(f"📝 已记录 {user_id} 选择了 {room_name}（{building_name}）")
    if user_prefs.get("preferred_rooms"):
        print(f"   当前偏好会议室: {', '.join(user_prefs['preferred_rooms'])}")
    if user_prefs.get("default_building"):
        print(f"   当前默认楼栋: {user_prefs['default_building']}")


def list_preferences():
    """列出所有用户偏好"""
    data = load_prefs()
    prefs = data.get("preferences", {})
    if not prefs:
        print("还没有任何用户偏好设置")
        return
    for user_id, p in prefs.items():
        building = p.get("default_building", "未设置")
        cap = p.get("capacity_gte", 0)
        rooms = ", ".join(p.get("preferred_rooms", [])) or "无"
        print(f"👤 {user_id}  楼栋:{building}  容量≥{cap}  偏好:{rooms}")


def delete_preference(user_id):
    """删除用户偏好"""
    data = load_prefs()
    prefs = data.get("preferences", {})
    if user_id in prefs:
        del prefs[user_id]
        save_prefs(data)
        print(f"✅ 已删除 {user_id} 的偏好设置")
    else:
        print(f"❌ 未找到 {user_id} 的偏好设置")


def main():
    parser = argparse.ArgumentParser(description="用户会议室偏好管理")
    parser.add_argument("--set", action="store_true", help="设置偏好")
    parser.add_argument("--get", action="store_true", help="读取偏好")
    parser.add_argument("--learn", action="store_true", help="根据选择学习偏好")
    parser.add_argument("--list", action="store_true", help="列出所有偏好")
    parser.add_argument("--delete", action="store_true", help="删除偏好")
    parser.add_argument("--user", "-u", help="用户 open_id")
    parser.add_argument("--building", "-b", help="默认楼栋")
    parser.add_argument("--capacity-gte", "-c", type=int, help="最小容量")
    parser.add_argument("--capacity-lte", type=int, help="最大容量")
    parser.add_argument("--preferred-rooms", help="偏好会议室（逗号分隔）")
    parser.add_argument("--room", "-r", help="当前选择的会议室（用于学习）")
    parser.add_argument("--note", "-n", help="备注")

    args = parser.parse_args()

    if args.list:
        list_preferences()
    elif args.set:
        if not args.user:
            print("错误: --set 需要 --user")
            sys.exit(1)
        set_preference(args.user, args)
    elif args.get:
        if not args.user:
            print("错误: --get 需要 --user")
            sys.exit(1)
        get_preference(args.user)
    elif args.learn:
        if not args.user or not args.room:
            print("错误: --learn 需要 --user 和 --room")
            sys.exit(1)
        learn_preference(args.user, args.room, args.building or "")
    elif args.delete:
        if not args.user:
            print("错误: --delete 需要 --user")
            sys.exit(1)
        delete_preference(args.user)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
