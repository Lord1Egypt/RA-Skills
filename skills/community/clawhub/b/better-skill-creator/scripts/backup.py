#!/usr/bin/env python3
import os
import shutil
import json
import time
import hashlib
import argparse
from pathlib import Path

BACKUP_ROOT = os.path.expanduser("~/.openclaw/skill-backups/")
KEEP_VERSIONS = 20  # 每个Skill最多保留20个版本

def get_skill_name(skill_path):
    """从路径中获取Skill名称"""
    return os.path.basename(os.path.normpath(skill_path))

def generate_version_hash(skill_path):
    """生成当前Skill内容的哈希值"""
    hash_md5 = hashlib.md5()
    for root, dirs, files in os.walk(skill_path):
        for file in sorted(files):
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                with open(file_path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
    return hash_md5.hexdigest()[:8]

def cleanup_old_versions(skill_backup_dir):
    """清理超过保留数量的旧版本，跳过稳定版"""
    all_versions = []
    for d in os.listdir(skill_backup_dir):
        version_path = os.path.join(skill_backup_dir, d)
        if not os.path.isdir(version_path):
            continue
        metadata_path = os.path.join(version_path, "metadata.json")
        if not os.path.exists(metadata_path):
            continue
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        all_versions.append({
            "id": d,
            "timestamp": metadata["timestamp"],
            "is_stable": metadata.get("stable", False)
        })
    
    # 稳定版不参与清理
    non_stable_versions = [v for v in all_versions if not v["is_stable"]]
    # 按时间倒序排序
    non_stable_versions.sort(key=lambda x: x["timestamp"], reverse=True)
    
    if len(non_stable_versions) > KEEP_VERSIONS:
        for old_version in non_stable_versions[KEEP_VERSIONS:]:
            shutil.rmtree(os.path.join(skill_backup_dir, old_version["id"]))
            print(f"清理旧版本: {old_version['id']}")

def main():
    parser = argparse.ArgumentParser(description="备份Skill版本")
    parser.add_argument("skill_path", help="Skill目录路径")
    parser.add_argument("--note", default="", help="版本备注")
    args = parser.parse_args()

    skill_path = os.path.abspath(args.skill_path)
    if not os.path.isdir(skill_path):
        print(f"错误: {skill_path} 不是有效的目录")
        exit(1)

    skill_name = get_skill_name(skill_path)
    version_hash = generate_version_hash(skill_path)
    timestamp = str(int(time.time()))
    version_id = f"{timestamp}_{version_hash}"

    # 创建备份目录
    skill_backup_dir = os.path.join(BACKUP_ROOT, skill_name)
    os.makedirs(skill_backup_dir, exist_ok=True)
    backup_dir = os.path.join(skill_backup_dir, version_id)

    # 复制Skill内容
    shutil.copytree(skill_path, backup_dir)

    # 写入元数据
    metadata = {
        "version_id": version_id,
        "skill_name": skill_name,
        "source_path": skill_path,
        "backup_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp))),
        "timestamp": int(timestamp),
        "note": args.note,
        "version_hash": version_hash
    }
    with open(os.path.join(backup_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    # 清理旧版本
    cleanup_old_versions(skill_backup_dir)

    print(f"✅ 备份成功! 版本ID: {version_id}")
    print(f"备份路径: {backup_dir}")
    if args.note:
        print(f"版本备注: {args.note}")

if __name__ == "__main__":
    main()
