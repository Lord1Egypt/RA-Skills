#!/usr/bin/env python3
import os
import json
import argparse
from pathlib import Path

BACKUP_ROOT = os.path.expanduser("~/.openclaw/skill-backups/")

def main():
    parser = argparse.ArgumentParser(description="查看Skill历史版本列表")
    parser.add_argument("skill_name", help="Skill名称")
    args = parser.parse_args()

    skill_backup_dir = os.path.join(BACKUP_ROOT, args.skill_name)
    if not os.path.isdir(skill_backup_dir):
        print(f"❌ 未找到Skill {args.skill_name} 的备份记录")
        exit(1)

    versions = []
    for version_dir in os.listdir(skill_backup_dir):
        version_path = os.path.join(skill_backup_dir, version_dir)
        if not os.path.isdir(version_path):
            continue
        metadata_path = os.path.join(version_path, "metadata.json")
        if not os.path.exists(metadata_path):
            continue
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        versions.append(metadata)

    # 按时间倒序排序
    versions.sort(key=lambda x: x["timestamp"], reverse=True)

    print(f"📋 Skill {args.skill_name} 历史版本列表 (共{len(versions)}个版本):")
    print("-" * 130)
    print(f"{'标记':<4} {'版本ID':<22} {'备份时间':<20} {'版本号':<8} {'备注'}")
    print("-" * 130)
    for v in versions:
        stable_tag = "🏆" if v.get("stable", False) else ""
        version = v.get("version", "")
        note = v["note"] if v["note"] else "无备注"
        print(f"{stable_tag:<4} {v['version_id']:<22} {v['backup_time']:<20} {version:<8} {note}")

if __name__ == "__main__":
    main()
