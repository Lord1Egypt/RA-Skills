#!/usr/bin/env python3
"""
auto-create-skill 注册表管理工具

管理由 auto-create-skill 创建的所有工作流 Skill 的注册信息。
注册表存储在 /mnt/skills/user/.auto-skill-registry.json
如果该路径不可写，回退到 /home/claude/.auto-skill-registry.json
"""

import json
import sys
import os
from datetime import datetime, timezone

# 尝试多个注册表路径（按优先级排列）
REGISTRY_PATHS = [
    os.path.expanduser("~/.claude/skills/.auto-skill-registry.json"),  # Claude Code
    "/mnt/skills/user/.auto-skill-registry.json",                       # Claude.ai
    "/home/claude/.auto-skill-registry.json",                           # 回退
]


def get_registry_path():
    """找到第一个可写的注册表路径"""
    for path in REGISTRY_PATHS:
        dir_path = os.path.dirname(path)
        if os.path.exists(path):
            if os.access(path, os.W_OK):
                return path
            continue
        if os.path.isdir(dir_path) and os.access(dir_path, os.W_OK):
            return path
    # 最终回退
    fallback = "/home/claude/.auto-skill-registry.json"
    os.makedirs(os.path.dirname(fallback), exist_ok=True)
    return fallback


def load_registry(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"version": 1, "skills": []}


def save_registry(path, registry):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)
    print(f"注册表已保存到: {path}")


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def cmd_add(args):
    path = get_registry_path()
    registry = load_registry(path)

    name = args["name"]
    # 检查是否已存在
    for skill in registry["skills"]:
        if skill["name"] == name:
            print(f"错误: Skill '{name}' 已存在。如需更新请使用 update 命令。")
            sys.exit(1)

    params = []
    if args.get("params"):
        try:
            params = json.loads(args["params"])
        except json.JSONDecodeError:
            params = [p.strip() for p in args["params"].split(",")]

    skill_entry = {
        "name": name,
        "description": args.get("description", ""),
        "path": args.get("path", f"/mnt/skills/user/{name}/SKILL.md"),
        "params": params,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "version": 1,
    }

    registry["skills"].append(skill_entry)
    save_registry(path, registry)
    print(f"✅ Skill '{name}' 已注册成功。")
    print(f"   路径: {skill_entry['path']}")
    print(f"   参数: {', '.join(params) if params else '无'}")


def cmd_update(args):
    path = get_registry_path()
    registry = load_registry(path)

    name = args["name"]
    found = False
    for skill in registry["skills"]:
        if skill["name"] == name:
            if args.get("description"):
                skill["description"] = args["description"]
            if args.get("path"):
                skill["path"] = args["path"]
            if args.get("params"):
                try:
                    skill["params"] = json.loads(args["params"])
                except json.JSONDecodeError:
                    skill["params"] = [p.strip() for p in args["params"].split(",")]
            skill["updated_at"] = now_iso()
            skill["version"] = skill.get("version", 1) + 1
            found = True
            break

    if not found:
        print(f"错误: Skill '{name}' 不存在。")
        sys.exit(1)

    save_registry(path, registry)
    print(f"✅ Skill '{name}' 已更新 (v{skill['version']})。")


def cmd_remove(args):
    path = get_registry_path()
    registry = load_registry(path)

    name = args["name"]
    original_len = len(registry["skills"])
    registry["skills"] = [s for s in registry["skills"] if s["name"] != name]

    if len(registry["skills"]) == original_len:
        print(f"错误: Skill '{name}' 不存在。")
        sys.exit(1)

    save_registry(path, registry)
    print(f"✅ Skill '{name}' 已从注册表中移除。")


def cmd_list(args):
    path = get_registry_path()
    registry = load_registry(path)

    if not registry["skills"]:
        print("📋 暂无已注册的工作流 Skill。")
        return

    print(f"📋 已注册的工作流 Skill ({len(registry['skills'])} 个)：\n")
    for i, skill in enumerate(registry["skills"], 1):
        params_str = ", ".join(skill.get("params", [])) or "无"
        print(f"  {i}. {skill['name']} (v{skill.get('version', 1)})")
        print(f"     描述: {skill.get('description', 'N/A')}")
        print(f"     路径: {skill.get('path', 'N/A')}")
        print(f"     参数: {params_str}")
        print(f"     创建: {skill.get('created_at', 'N/A')}")
        print(f"     更新: {skill.get('updated_at', 'N/A')}")
        print()


def cmd_get(args):
    path = get_registry_path()
    registry = load_registry(path)

    name = args["name"]
    for skill in registry["skills"]:
        if skill["name"] == name:
            print(json.dumps(skill, ensure_ascii=False, indent=2))
            return

    print(f"错误: Skill '{name}' 不存在。")
    sys.exit(1)


def parse_args(argv):
    """简单的参数解析器，避免依赖 argparse 以外的库"""
    if len(argv) < 2:
        print("用法: manage_registry.py <command> [--key value ...]")
        print("命令: add, update, remove, list, get")
        sys.exit(1)

    command = argv[1]
    args = {}
    i = 2
    while i < len(argv):
        if argv[i].startswith("--"):
            key = argv[i][2:]
            if i + 1 < len(argv) and not argv[i + 1].startswith("--"):
                args[key] = argv[i + 1]
                i += 2
            else:
                args[key] = True
                i += 1
        else:
            i += 1

    return command, args


if __name__ == "__main__":
    command, args = parse_args(sys.argv)

    commands = {
        "add": cmd_add,
        "update": cmd_update,
        "remove": cmd_remove,
        "list": cmd_list,
        "get": cmd_get,
    }

    if command not in commands:
        print(f"未知命令: {command}")
        print(f"可用命令: {', '.join(commands.keys())}")
        sys.exit(1)

    commands[command](args)
