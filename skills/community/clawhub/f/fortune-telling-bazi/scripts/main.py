#!/usr/bin/env python3
"""
八字算命 CLI 入口
使用方式:
  python3 scripts/main.py add    <name> <year> <month> <day> <time> <gender>
  python3 scripts/main.py update <name> <year> <month> <day> <time> <gender>
  python3 scripts/main.py list
  python3 scripts/main.py view   [name]
  python3 scripts/main.py remove <name>
  python3 scripts/main.py active [name1,name2,...|none]
  python3 scripts/main.py status
  python3 scripts/main.py joint  [name1,name2,...]
"""
import sys, re
from calc import calculate_fate, dict_to_fate
from report import view_single, view_joint
from store import (load_users, save_users, load_active, save_active, now_iso,
                   ensure_dir)


# ── 时间解析 ─────────────────────────────────────────────────────────────────

def parse_time(time_str):
    """解析自然时间字符串，返回 (hour, minute)"""
    t = time_str.strip()
    t = re.sub(r'[点时]', '', t)

    is_pm = False
    if '下午' in t or '晚' in t or 'PM' in t.upper():
        is_pm = True
        t = re.sub(r'下午|晚|PM', '', t, flags=re.IGNORECASE).strip()
    if '上午' in t or '早' in t or 'AM' in t.upper():
        t = re.sub(r'上午|早|AM', '', t, flags=re.IGNORECASE).strip()

    if ':' in t:
        parts = t.split(':')
        h = int(parts[0])
        m = int(parts[1]) if len(parts) > 1 else 0
    else:
        h = int(t) if t else 0
        m = 0

    if is_pm and h < 12:
        h += 12

    return h, m


# ── 命令实现 ─────────────────────────────────────────────────────────────────

def cmd_add():
    args = sys.argv[2:]
    if len(args) < 5:
        print("用法: python3 scripts/main.py add <name> <year> <month> <day> <time> <gender>")
        sys.exit(1)

    name = args[0]
    year, month, day = args[1], args[2], args[3]
    time_str = args[4]
    gender = args[-1]
    hour, minute = parse_time(time_str)

    users = load_users()
    if name in users:
        print(f"'{name}' 已存在，用 update 命令更新。")
        sys.exit(1)

    fate_dict = calculate_fate(name, year, month, day, hour, minute, gender)
    users[name] = {
        "birth": {"year": int(year), "month": int(month), "day": int(day),
                  "hour": int(hour), "minute": int(minute), "gender": gender},
        "bazi": fate_dict,
        "fetched_at": now_iso(),
    }
    save_users(users)
    bazi_s = " ".join(fate_dict['bazi'].values()) if isinstance(fate_dict.get('bazi'), dict) else str(fate_dict.get('bazi', ''))
    print(f"✅ 已添加：{name}")
    print(f"   八字：{bazi_s}")
    print(f"   命格：{fate_dict['mingge']} | {fate_dict['wangshuai']} | 喜用：{fate_dict['xiyong']}")


def cmd_update():
    args = sys.argv[2:]
    if len(args) < 5:
        print("用法: python3 scripts/main.py update <name> <year> <month> <day> <time> <gender>")
        sys.exit(1)

    name = args[0]
    year, month, day = args[1], args[2], args[3]
    time_str = args[4]
    gender = args[-1]
    hour, minute = parse_time(time_str)

    users = load_users()
    fate_dict = calculate_fate(name, year, month, day, hour, minute, gender)
    users[name] = {
        "birth": {"year": int(year), "month": int(month), "day": int(day),
                  "hour": int(hour), "minute": int(minute), "gender": gender},
        "bazi": fate_dict,
        "fetched_at": now_iso(),
    }
    save_users(users)
    bazi_s = " ".join(fate_dict['bazi'].values()) if isinstance(fate_dict.get('bazi'), dict) else str(fate_dict.get('bazi', ''))
    print(f"✅ 已更新：{name}")
    print(f"   八字：{bazi_s}")


def cmd_list():
    users = load_users()
    if not users:
        print("还没有保存任何八字。")
        return
    for name, data in users.items():
        bazi = data.get("bazi", {})
        if isinstance(bazi, dict):
            raw = bazi.get("bazi", {})
            bazi_str = " ".join(raw.values()) if isinstance(raw, dict) else str(raw)
        else:
            bazi_str = "?"
        birth = data["birth"]
        print(f"• {name}：{birth['year']}年{birth['month']}月{birth['day']}日 {bazi_str} ({birth['gender']})")


def cmd_view():
    users = load_users()
    args = sys.argv[2:]

    if args:
        name = args[0]
    else:
        active = load_active()
        if not active.get("names"):
            print("未指定姓名，且无激活用户。")
            sys.exit(1)
        name = active["names"][0]

    if name not in users:
        print(f"未找到：{name}")
        sys.exit(1)

    # dict → Fate dataclass（供 report.py 使用）
    user_data = users[name]
    fate_obj  = dict_to_fate(user_data, user_data["birth"], user_data.get("gender", "男"))
    print(view_single(name, {"birth": user_data["birth"], "bazi": fate_obj}))


def cmd_remove():
    users = load_users()
    args = sys.argv[2:]
    if not args:
        print("用法: python3 scripts/main.py remove <name>")
        sys.exit(1)

    name = args[0]
    if name not in users:
        print(f"未找到：{name}")
        sys.exit(1)

    del users[name]
    save_users(users)

    active = load_active()
    if name in active.get("names", []):
        active["names"] = [n for n in active["names"] if n != name]
        save_active(active)

    print(f"✅ 已删除：{name}")


def cmd_active():
    users = load_users()
    args = sys.argv[2:]

    if not args:
        active = load_active()
        if active.get("names"):
            print("当前激活：" + ", ".join(active["names"]))
        else:
            print("当前无激活用户")
        return

    names_input = args[0]
    if names_input.lower() == "none":
        names = []
    else:
        names = [n.strip() for n in names_input.split(",")]
        for n in names:
            if n not in users:
                print(f"错误：'{n}' 未找到，请先用 add 添加。")
                sys.exit(1)

    save_active({"active": True, "names": names})
    if names:
        print(f"✅ 已激活：{', '.join(names)}")
    else:
        print("✅ 已取消激活")


def cmd_status():
    active = load_active()
    users = load_users()
    if not users:
        print("NOT_FOUND:无任何用户")
        return
    if not active.get("active") or not active.get("names"):
        print("NOT_ACTIVE")
        return
    for n in active["names"]:
        if n not in users:
            print(f"NOT_ACTIVE:{n}已删除")
            return
    print(f"ACTIVE:{','.join(active['names'])}")


def cmd_joint():
    users = load_users()
    args = sys.argv[2:]

    if args:
        names = [n.strip() for n in args[0].split(",")]
    else:
        active = load_active()
        names = active.get("names", [])
        if not names:
            print("未指定用户，且无激活用户。请用 active 或 joint name1,name2")
            sys.exit(1)

    if len(names) < 2:
        print("联合分析至少需要2个人。")
        sys.exit(1)

    data_list = []
    for name in names:
        if name not in users:
            print(f"未找到：{name}")
            sys.exit(1)
        ud = users[name]
        fate_obj  = dict_to_fate(ud, ud["birth"], ud.get("gender", "男"))
        data_list.append({"name": name, "birth": ud["birth"], "bazi": fate_obj})

    print(view_joint(data_list))


# ── 入口 ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 scripts/main.py <add|update|list|view|remove|active|status|joint>")
        sys.exit(1)

    cmd_map = {
        "add":    cmd_add,
        "update": cmd_update,
        "list":   cmd_list,
        "view":   cmd_view,
        "remove": cmd_remove,
        "active": cmd_active,
        "status": cmd_status,
        "joint":  cmd_joint,
    }

    cmd = sys.argv[1]
    if cmd in cmd_map:
        cmd_map[cmd]()
    else:
        print(f"未知命令：{cmd}")
        sys.exit(1)
