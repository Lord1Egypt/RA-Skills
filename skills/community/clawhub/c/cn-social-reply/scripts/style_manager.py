#!/usr/bin/env python3
"""cn-social-reply 风格模板管理器"""
import argparse
import json
import os
import sys

STYLES_DIR = os.path.expanduser("~/.qclaw/workspace/cn-social-reply")
STYLES_FILE = os.path.join(STYLES_DIR, "styles.json")


def _ensure_dir():
    os.makedirs(STYLES_DIR, exist_ok=True)


def _load() -> dict:
    _ensure_dir()
    if os.path.exists(STYLES_FILE):
        with open(STYLES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"styles": {}}


def _save(data: dict):
    _ensure_dir()
    with open(STYLES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def cmd_save(args):
    data = _load()
    name = args.name
    data["styles"][name] = {
        "style": args.style,
        "extra": args.extra or "",
        "platform": args.platform or "通用",
        "created": args.created,
    }
    _save(data)
    print(f"✅ 风格模板「{name}」已保存")
    print(f"   策略: {args.style} | 平台: {args.platform or '通用'}")
    if args.extra:
        print(f"   备注: {args.extra}")


def cmd_list(args):
    data = _load()
    styles = data.get("styles", {})
    if not styles:
        print("📭 还没有保存任何风格模板")
        print("   用 save 命令创建：python3 style_manager.py save --name \"我的风格\" --style 温暖")
        return
    print(f"📋 已保存 {len(styles)} 个风格模板：\n")
    for i, (name, info) in enumerate(styles.items(), 1):
        print(f"  {i}. {name}")
        print(f"     策略: {info.get('style', '未设置')} | 平台: {info.get('platform', '通用')}")
        if info.get("extra"):
            print(f"     备注: {info['extra']}")
        print(f"     创建: {info.get('created', '未知')}")
        print()


def cmd_load(args):
    data = _load()
    styles = data.get("styles", {})
    name = args.name
    if name not in styles:
        available = ", ".join(styles.keys()) if styles else "无"
        print(f"❌ 未找到风格模板「{name}」")
        print(f"   已有模板: {available}")
        sys.exit(1)
    info = styles[name]
    print(f"✅ 已加载风格模板「{name}」")
    print(json.dumps(info, ensure_ascii=False, indent=2))


def cmd_delete(args):
    data = _load()
    styles = data.get("styles", {})
    name = args.name
    if name not in styles:
        print(f"❌ 未找到风格模板「{name}」")
        sys.exit(1)
    del styles[name]
    _save(data)
    print(f"🗑️ 风格模板「{name}」已删除")


def main():
    from datetime import datetime

    parser = argparse.ArgumentParser(description="cn-social-reply 风格模板管理")
    sub = parser.add_subparsers(dest="command")

    # save
    p_save = sub.add_parser("save", help="保存风格模板")
    p_save.add_argument("--name", required=True, help="模板名称")
    p_save.add_argument("--style", required=True, help="回复策略（幽默/专业/温暖/高情商/互动引导/毒舌俏皮）")
    p_save.add_argument("--extra", default="", help="额外备注（字数限制、口头禅等）")
    p_save.add_argument("--platform", default="", help="目标平台（小红书/抖音/微博/B站/知乎）")
    p_save.add_argument("--created", default=datetime.now().strftime("%Y-%m-%d %H:%M"))

    # list
    sub.add_parser("list", help="列出所有风格模板")

    # load
    p_load = sub.add_parser("load", help="加载风格模板详情")
    p_load.add_argument("--name", required=True, help="模板名称")

    # delete
    p_del = sub.add_parser("delete", help="删除风格模板")
    p_del.add_argument("--name", required=True, help="模板名称")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    cmds = {"save": cmd_save, "list": cmd_list, "load": cmd_load, "delete": cmd_delete}
    cmds[args.command](args)


if __name__ == "__main__":
    main()
