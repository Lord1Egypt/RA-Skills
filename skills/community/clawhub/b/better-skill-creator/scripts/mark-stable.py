#!/usr/bin/env python3
import os
import json
import argparse
from pathlib import Path

BACKUP_ROOT = os.path.expanduser("~/.openclaw/skill-backups/")

def main():
    parser = argparse.ArgumentParser(description="标记/取消标记版本为稳定版")
    parser.add_argument("skill_name", help="技能名称")
    parser.add_argument("version_id", help="版本ID")
    parser.add_argument("--unmark", action="store_true", help="取消稳定版标记")
    parser.add_argument("--note", default="", help="稳定版备注")
    args = parser.parse_args()

    version_dir = os.path.join(BACKUP_ROOT, args.skill_name, args.version_id)
    if not os.path.isdir(version_dir):
        print(f"❌ 版本 {args.version_id} 不存在")
        exit(1)

    metadata_path = os.path.join(version_dir, "metadata.json")
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    if args.unmark:
        metadata.pop("stable", None)
        metadata.pop("stable_note", None)
        print(f"✅ 已取消版本 {args.version_id} 的稳定版标记")
    else:
        metadata["stable"] = True
        metadata["stable_note"] = args.note
        metadata["stable_time"] = json.dumps({"time": metadata["backup_time"], "note": args.note}, ensure_ascii=False)
        print(f"✅ 已将版本 {args.version_id} 标记为稳定版")
        if args.note:
            print(f"备注: {args.note}")

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
