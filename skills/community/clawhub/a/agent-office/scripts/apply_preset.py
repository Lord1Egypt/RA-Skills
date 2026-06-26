#!/usr/bin/env python3
"""
apply_preset.py —— 应用团队预设

用法:
  python3 apply_preset.py --list
  python3 apply_preset.py 出版公司
  python3 apply_preset.py coding-company --dry-run
"""
import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import add_worker


PRESET_DIR = Path(__file__).resolve().parent.parent / "presets"
PRESET_ALIASES = {
    "出版公司": "publishing-company",
    "出版": "publishing-company",
    "publishing": "publishing-company",
    "publishing-company": "publishing-company",
    "编程公司": "coding-company",
    "程序公司": "coding-company",
    "coding": "coding-company",
    "coding-company": "coding-company",
}


def list_presets() -> list[dict]:
    presets = []
    for path in sorted(PRESET_DIR.glob("*.json")):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        presets.append(data)
    return presets


def resolve_preset_name(name: str) -> str:
    key = (name or "").strip()
    return PRESET_ALIASES.get(key, key)


def load_preset(name: str) -> dict:
    slug = resolve_preset_name(name)
    path = PRESET_DIR / f"{slug}.json"
    if not path.exists():
        raise FileNotFoundError(f"找不到预设：{name}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def print_presets() -> None:
    print("可用预设：")
    for preset in list_presets():
        print(f"- {preset['name']} ({preset['slug']})")
        print(f"  {preset['description']}")
        print(f"  员工数量: {len(preset.get('workers', []))}")


def apply_preset(name: str, dry_run: bool = False) -> list[dict]:
    preset = load_preset(name)
    results = []

    print(f"🏢 应用预设：{preset['name']}")
    print(f"   {preset['description']}")
    print(f"   计划添加 {len(preset.get('workers', []))} 位员工")
    print()

    for item in preset.get("workers", []):
        worker_name = item["name"]
        worker_id = item.get("worker_id")
        engine = item["engine"]
        role = item["role"]
        duty = item.get("duty", "")

        print(f"→ {worker_name} | {engine} | {role}")
        if duty:
            print(f"   职责: {duty}")

        if dry_run:
            results.append(
                {
                    "name": worker_name,
                    "worker_id": worker_id,
                    "engine": engine,
                    "role": role,
                    "status": "planned",
                }
            )
            continue

        result = add_worker.create_worker(
            name=worker_name,
            engine=engine,
            role=role,
            worker_id_override=worker_id,
        )
        results.append(result)
        print(f"   ✅ 已添加：{result['worker_id']} @ {result['port']}")
        print()

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply Agent Office presets")
    parser.add_argument("preset", nargs="?", help="预设名称，如 出版公司 / 编程公司")
    parser.add_argument("--list", action="store_true", help="列出可用预设")
    parser.add_argument("--dry-run", action="store_true", help="只预览，不真正创建员工")
    args = parser.parse_args()

    if args.list:
        print_presets()
        return

    if not args.preset:
        print("❌ 用法: python3 apply_preset.py <预设名> [--dry-run]")
        print("   先看列表: python3 apply_preset.py --list")
        sys.exit(1)

    try:
        results = apply_preset(args.preset, dry_run=args.dry_run)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 应用预设失败: {e}")
        sys.exit(1)

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"✅ 预设处理完成，共 {len(results)} 项")
    if args.dry_run:
        print("   当前为预演模式，未真正创建员工")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


if __name__ == "__main__":
    main()
