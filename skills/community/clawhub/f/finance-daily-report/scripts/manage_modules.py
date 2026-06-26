#!/usr/bin/env python3
"""
Manage finance report modules via CLI commands.
Called by the agent when user sends natural language module management requests.

Usage:
    python3 manage_modules.py add --name "AI Agent资管应用动态" \
        --keywords "AI agent asset management,AI agent 资管" \
        --prompt "搜索AI Agent在资管行业的最新动态..."

    python3 manage_modules.py remove --name "AI Agent资管应用动态"
    python3 manage_modules.py enable --name "AI Agent资管应用动态"
    python3 manage_modules.py disable --name "AI Agent资管应用动态"
    python3 manage_modules.py list
    python3 manage_modules.py reorder --name "AI Agent资管应用动态" --priority 5
"""

import argparse
import json
import os
import re
import sys
import copy

# Config file location (workspace)
CONFIG_DIR = os.environ.get("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace")
CONFIG_FILE = os.path.join(CONFIG_DIR, "finance-report-config.yaml")
DEFAULT_CONFIG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              "assets", "default-config.yaml")


def load_config():
    """Load config as raw text + parsed modules list."""
    config_path = CONFIG_FILE if os.path.exists(CONFIG_FILE) else DEFAULT_CONFIG
    with open(config_path, "r", encoding="utf-8") as f:
        raw = f.read()
    # Simple YAML-like parser for our specific format
    modules = parse_modules(raw)
    return config_path, raw, modules


def parse_modules(raw):
    """Parse modules from our YAML config format."""
    modules = []
    # Split by module markers
    parts = re.split(r'\n  - id: ', raw)
    header = parts[0]
    for part in parts[1:]:
        mod = {"raw": "  - id: " + part}
        # Extract fields
        for field, pattern in [
            ("id", r'id: (\S+)'),
            ("name", r'name: (.+)'),
            ("enabled", r'enabled: (true|false)'),
            ("priority", r'priority: (\d+)'),
            ("data_strategy", r'data_strategy: (\S+)'),
        ]:
            m = re.search(pattern, part)
            if m:
                val = m.group(1).strip()
                if field == "enabled":
                    val = val == "true"
                elif field == "priority":
                    val = int(val)
                mod[field] = val
        modules.append(mod)
    return modules


def name_to_id(name):
    """Convert Chinese/English name to a valid ID."""
    # Simple transliteration: keep alphanumeric, replace rest with underscore
    ascii_name = re.sub(r'[^a-zA-Z0-9]', '_', name.lower())
    ascii_name = re.sub(r'_+', '_', ascii_name).strip('_')
    if not ascii_name or len(ascii_name) < 2:
        ascii_name = "custom_module_" + str(hash(name) % 10000)
    return ascii_name


def generate_module_yaml(name, module_id, keywords, prompt, priority=None, data_strategy="search"):
    """Generate YAML block for a new module."""
    if priority is None:
        priority = 50  # default mid-range

    kw_lines = "\n".join(f'      - "{kw} {{date}}"' for kw in keywords)

    yaml_block = f"""
  # ── 自定义模块：{name} ──
  - id: {module_id}
    name: {name}
    enabled: true
    priority: {priority}
    data_strategy: {data_strategy}
    fetch_urls: []
    search_keywords:
{kw_lines}
    collector_prompt: |
      {prompt}
"""
    return yaml_block


def cmd_add(args):
    """Add a new module."""
    config_path, raw, modules = load_config()

    # Check if module already exists
    module_id = name_to_id(args.name)
    for mod in modules:
        if mod.get("id") == module_id or mod.get("name") == args.name:
            # Enable it if it exists but is disabled
            if mod.get("enabled") == False:
                return cmd_enable(argparse.Namespace(name=args.name))
            print(f"模块已存在：{args.name} (id={mod.get('id')})")
            print("如需修改，请使用 remove 后重新 add")
            return 0

    # Parse keywords
    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    if not keywords:
        keywords = [args.name]

    # Generate prompt if not provided
    prompt = args.prompt or f"搜索 {{date}} 关于「{args.name}」的最新动态、新闻、数据和事件。每条必须有具体来源链接。"

    # Determine priority
    max_priority = max((m.get("priority", 0) for m in modules), default=9)
    priority = args.priority or (max_priority + 1)

    # Generate YAML
    new_block = generate_module_yaml(args.name, module_id, keywords, prompt, priority)

    # If using default config, copy it first
    if config_path == DEFAULT_CONFIG:
        with open(DEFAULT_CONFIG, "r", encoding="utf-8") as f:
            raw = f.read()
        config_path = CONFIG_FILE

    # Append to config
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(raw.rstrip() + "\n" + new_block)

    print(f"✅ 模块已添加：{args.name}")
    print(f"   ID: {module_id}")
    print(f"   优先级: {priority}")
    print(f"   关键词: {', '.join(keywords)}")
    print(f"   配置文件: {config_path}")
    return 0


def cmd_remove(args):
    """Remove a module."""
    config_path, raw, modules = load_config()

    found = False
    for mod in modules:
        if mod.get("name") == args.name or mod.get("id") == args.name:
            found = True
            # Remove the raw block from config
            raw = raw.replace(mod["raw"], "")
            break

    if not found:
        print(f"❌ 未找到模块：{args.name}")
        return 1

    if config_path == DEFAULT_CONFIG:
        config_path = CONFIG_FILE

    with open(config_path, "w", encoding="utf-8") as f:
        f.write(raw)

    print(f"✅ 模块已删除：{args.name}")
    return 0


def cmd_enable(args):
    """Enable a module."""
    config_path, raw, modules = load_config()

    for mod in modules:
        if mod.get("name") == args.name or mod.get("id") == args.name:
            raw = raw.replace(mod["raw"], mod["raw"].replace("enabled: false", "enabled: true"))
            if config_path == DEFAULT_CONFIG:
                config_path = CONFIG_FILE
            with open(config_path, "w", encoding="utf-8") as f:
                f.write(raw)
            print(f"✅ 模块已启用：{args.name}")
            return 0

    print(f"❌ 未找到模块：{args.name}")
    return 1


def cmd_disable(args):
    """Disable a module."""
    config_path, raw, modules = load_config()

    for mod in modules:
        if mod.get("name") == args.name or mod.get("id") == args.name:
            raw = raw.replace(mod["raw"], mod["raw"].replace("enabled: true", "enabled: false"))
            if config_path == DEFAULT_CONFIG:
                config_path = CONFIG_FILE
            with open(config_path, "w", encoding="utf-8") as f:
                f.write(raw)
            print(f"✅ 模块已禁用：{args.name}")
            return 0

    print(f"❌ 未找到模块：{args.name}")
    return 1


def cmd_list(args):
    """List all modules."""
    _, _, modules = load_config()

    print(f"{'状态':<4} {'优先级':<6} {'ID':<30} {'名称'}")
    print("-" * 70)
    for mod in sorted(modules, key=lambda m: m.get("priority", 99)):
        status = "✅" if mod.get("enabled", True) else "⬚"
        print(f"{status:<4} {mod.get('priority', '?'):<6} {mod.get('id', '?'):<30} {mod.get('name', '?')}")

    return 0


def main():
    parser = argparse.ArgumentParser(description="Manage finance report modules")
    sub = parser.add_subparsers(dest="command")

    # Add
    p_add = sub.add_parser("add", help="Add a new module")
    p_add.add_argument("--name", required=True, help="Module display name")
    p_add.add_argument("--keywords", default="", help="Comma-separated search keywords")
    p_add.add_argument("--prompt", default="", help="Collector prompt")
    p_add.add_argument("--priority", type=int, default=None, help="Sort priority")

    # Remove
    p_rm = sub.add_parser("remove", help="Remove a module")
    p_rm.add_argument("--name", required=True)

    # Enable/Disable
    p_en = sub.add_parser("enable", help="Enable a module")
    p_en.add_argument("--name", required=True)
    p_dis = sub.add_parser("disable", help="Disable a module")
    p_dis.add_argument("--name", required=True)

    # List
    sub.add_parser("list", help="List all modules")

    # Reorder
    p_re = sub.add_parser("reorder", help="Change module priority")
    p_re.add_argument("--name", required=True)
    p_re.add_argument("--priority", type=int, required=True)

    args = parser.parse_args()

    if args.command == "add":
        return cmd_add(args)
    elif args.command == "remove":
        return cmd_remove(args)
    elif args.command == "enable":
        return cmd_enable(args)
    elif args.command == "disable":
        return cmd_disable(args)
    elif args.command == "list":
        return cmd_list(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
