#!/usr/bin/env python3
import os
import json
import shutil
import argparse
from pathlib import Path

BACKUP_ROOT = os.path.expanduser("~/.openclaw/skill-backups/")

def get_version_dir(skill_name, version_id):
    """获取版本目录路径"""
    version_dir = os.path.join(BACKUP_ROOT, skill_name, version_id)
    if not os.path.isdir(version_dir):
        print(f"❌ 版本 {version_id} 不存在")
        exit(1)
    return version_dir

def get_version_metadata(skill_name, version_id):
    """获取版本元数据"""
    version_dir = get_version_dir(skill_name, version_id)
    metadata_path = os.path.join(version_dir, "metadata.json")
    with open(metadata_path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="回滚Skill到指定版本")
    parser.add_argument("skill_name", help="Skill名称")
    parser.add_argument("version_id", help="要回滚的版本ID")
    parser.add_argument("--dry-run", action="store_true", help="模拟回滚，不实际写入文件")
    args = parser.parse_args()

    metadata = get_version_metadata(args.skill_name, args.version_id)
    target_path = metadata["source_path"]

    print(f"🔄 准备回滚 {args.skill_name} 到版本: {args.version_id}")
    print(f"备份时间: {metadata['backup_time']}")
    print(f"版本备注: {metadata['note'] if metadata['note'] else '无备注'}")
    print(f"目标路径: {target_path}")

    if args.dry_run:
        print("\n📋 模拟回滚模式，以下文件将被覆盖:")
        version_dir = get_version_dir(args.skill_name, args.version_id)
        for root, dirs, files in os.walk(version_dir):
            rel_path = os.path.relpath(root, version_dir)
            for file in files:
                if file == "metadata.json":
                    continue
                print(f"  - {os.path.join(rel_path, file)}")
        print("\n✅ 模拟回滚完成，没有实际修改文件")
        return

    # 确认操作
    confirm = input("\n⚠️  确认要回滚吗？此操作会覆盖当前版本内容 (y/N): ")
    if confirm.lower() != "y":
        print("❌ 回滚已取消")
        exit(0)

    # 先备份当前版本
    import subprocess
    subprocess.run([
        "python", os.path.join(os.path.dirname(__file__), "backup.py"),
        target_path,
        "--note", f"auto-backup-before-rollback-to-{args.version_id}"
    ], check=True)

    # 执行回滚
    version_dir = get_version_dir(args.skill_name, args.version_id)
    # 清空目标目录
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    # 复制备份版本到目标路径
    shutil.copytree(version_dir, target_path)
    # 删除metadata.json
    metadata_file = os.path.join(target_path, "metadata.json")
    if os.path.exists(metadata_file):
        os.remove(metadata_file)

    print(f"\n✅ 回滚成功! {args.skill_name} 已恢复到版本 {args.version_id}")
    print(f"当前版本路径: {target_path}")

if __name__ == "__main__":
    main()
