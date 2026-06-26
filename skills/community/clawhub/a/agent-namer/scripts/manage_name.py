#!/usr/bin/env python3
"""
Agent Name Manager - Internal naming tool for "货xx" format names.
Manages used names dictionary to avoid duplicates.
"""

import sys
import re
import json

SCRIPT_PATH = __file__

# 已使用的名字字典（内部记录）
USED_NAMES = json.load(open("scripts/used_names.json", "r", encoding="utf-8"))


def update_used_names():
    """将USED_NAMES字典更新到JSON文件"""
    try:
        with open("scripts/used_names.json", "w", encoding="utf-8") as f:
            json.dump(USED_NAMES, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"更新失败: {e}")
        return False


def check_name(name):
    """检查名字是否可用

    返回值: (is_available, message)
    - 不在字典中: 可用
    - 在字典中且状态为"活跃": 不可用
    - 在字典中且状态为"阵亡": 可用
    """
    if name not in USED_NAMES:
        return True, f"✅ '{name}' 可用（全新）"

    info = USED_NAMES[name]
    if info["status"] == "活跃":
        role_info = f" ({info['role']})" if info["role"] else ""
        return False, f"❌ '{name}' 已被使用{role_info}"
    else:  # 阵亡
        return True, f"✅ '{name}' 可用（阵亡，可复活）"


def add_used_name(name, role=""):
    """添加或复活名字

    - 不在字典中: 添加新元素，状态为活跃
    - 在字典中且状态为阵亡: 改为活跃，role为空则不修改，不为空则修改
    - 在字典中且状态为活跃: 返回错误
    """
    if name not in USED_NAMES:
        # 全新添加
        USED_NAMES[name] = {"status": "活跃", "role": role}
        if save_used_names():
            return True, f"✅ '{name}' 已添加为新名字并保存"
        return True, f"✅ '{name}' 已添加为新名字（⚠️ 保存失败，请手动更新）"

    info = USED_NAMES[name]
    if info["status"] == "活跃":
        return False, f"⚠️ '{name}' 已经在活跃使用中"

    # 复活阵亡的名字
    if role:  # role不为空则修改
        info["role"] = role
    info["status"] = "活跃"
    USED_NAMES[name] = info
    return True, f"✅ '{name}' 已复活并保存"


def kill_name(name):
    """将名字状态从活跃改为阵亡"""
    if name not in USED_NAMES:
        return False, f"⚠️ '{name}' 不在列表中"

    info = USED_NAMES[name]
    if info["status"] == "阵亡":
        return False, f"⚠️ '{name}' 已经是阵亡状态"

    info["status"] = "阵亡"
    USED_NAMES[name] = info
    return True, f"💀 '{name}' 阵亡并保存"


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print(f"  python3 {sys.argv[0]} check <名字>              - 检查名字是否可用")
        print(f"  python3 {sys.argv[0]} add <名字> [角色]         - 添加/复活名字")
        print(f"  python3 {sys.argv[0]} kill <名字>               - 将名字设为阵亡")
        print(f"  python3 {sys.argv[0]} list                      - 列出活跃的名字")
        sys.exit(1)

    command = sys.argv[1]

    if command == "check":
        if len(sys.argv) < 3:
            print("错误：请提供要检查的名字")
            sys.exit(1)
        name = sys.argv[2]
        available, msg = check_name(name)
        print(msg)
        sys.exit(0 if available else 1)

    elif command == "add":
        if len(sys.argv) < 3:
            print("错误：请提供要添加的名字")
            sys.exit(1)
        name = sys.argv[2]
        role = sys.argv[3] if len(sys.argv) > 3 else ""
        success, msg = add_used_name(name, role)
        print(msg)
        if success:
            update_used_names()
        sys.exit(0 if success else 1)

    elif command == "kill":
        if len(sys.argv) < 3:
            print("错误：请提供要设为阵亡的名字")
            sys.exit(1)
        name = sys.argv[2]
        success, msg = kill_name(name)
        print(msg)
        if success:
            update_used_names()
        sys.exit(0 if success else 1)

    elif command == "list":
        active_names = {k: v for k, v in USED_NAMES.items() if v["status"] == "活跃"}
        print(f"📋 活跃中的名字（共{len(active_names)}个）：")
        for name, info in active_names.items():
            role_info = f" - {info['role']}" if info["role"] else ""
            print(f"  • {name}{role_info}")

    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
