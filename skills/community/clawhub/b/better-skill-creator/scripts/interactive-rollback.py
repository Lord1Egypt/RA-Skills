#!/usr/bin/env python3
import os
import json
import subprocess
import argparse
from pathlib import Path

BACKUP_ROOT = os.path.expanduser("~/.openclaw/skill-backups/")

def get_version_list(skill_name):
    """获取Skill的所有版本列表"""
    skill_backup_dir = os.path.join(BACKUP_ROOT, skill_name)
    if not os.path.isdir(skill_backup_dir):
        print(f"❌ 未找到Skill {skill_name} 的备份记录")
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
    return versions

def main():
    parser = argparse.ArgumentParser(description="交互式Skill版本回滚")
    parser.add_argument("skill_name", help="Skill名称")
    args = parser.parse_args()

    versions = get_version_list(args.skill_name)
    if not versions:
        print(f"❌ 未找到Skill {args.skill_name} 的任何备份版本")
        exit(1)

    print(f"📋 Skill {args.skill_name} 历史版本列表:")
    print("-" * 120)
    print(f"{'序号':<4} {'版本ID':<22} {'备份时间':<20} {'版本号':<8} {'备注'}")
    print("-" * 120)
    for i, v in enumerate(versions, 1):
        version = v.get("version", "")
        note = v["note"] if v["note"] else "无备注"
        print(f"{i:<4} {v['version_id']:<22} {v['backup_time']:<20} {version:<8} {note}")

    # 让用户选择版本
    while True:
        try:
            choice = input("\n请选择要回滚的版本序号 (输入q退出): ")
            if choice.lower() == 'q':
                print("✅ 已取消回滚")
                exit(0)
            idx = int(choice) - 1
            if 0 <= idx < len(versions):
                selected_version = versions[idx]
                break
            else:
                print(f"❌ 序号超出范围，请输入1-{len(versions)}之间的数字")
        except ValueError:
            print("❌ 请输入有效的数字序号")

    # 显示版本详情
    print(f"\n🔍 你选择的版本详情:")
    print(f"版本ID: {selected_version['version_id']}")
    print(f"备份时间: {selected_version['backup_time']}")
    print(f"版本号: {selected_version.get('version', '未设置')}")
    print(f"版本备注: {selected_version['note'] if selected_version['note'] else '无备注'}")
    print(f"原路径: {selected_version['source_path']}")

    # 询问是否查看差异
    show_diff = input("\n是否查看该版本与当前版本的差异? (y/N): ")
    if show_diff.lower() == 'y':
        diff_script = os.path.join(os.path.dirname(__file__), "diff.py")
        subprocess.run([
            "python", diff_script,
            args.skill_name,
            selected_version["version_id"]
        ], check=True)

    # 确认回滚
    confirm = input("\n⚠️  确认要回滚到该版本吗？此操作会覆盖当前版本内容 (y/N): ")
    if confirm.lower() != "y":
        print("✅ 回滚已取消")
        exit(0)

    # 执行回滚
    rollback_script = os.path.join(os.path.dirname(__file__), "rollback.py")
    subprocess.run([
        "python", rollback_script,
        args.skill_name,
        selected_version["version_id"]
    ], check=True)

if __name__ == "__main__":
    main()
