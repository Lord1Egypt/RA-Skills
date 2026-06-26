#!/usr/bin/env python3
import os
import shutil
import sys
from pathlib import Path

# 可能存在的旧技能路径
OLD_PATHS = [
    "/usr/lib/node_modules/openclaw/skills/skill-creator",
    os.path.expanduser("~/.openclaw/skills/skill-creator"),
    "/workspace/projects/workspace/skills/skill-creator",
    "/workspace/projects/workspace/skills/skill-version-control"
]

BACKUP_ROOT = os.path.expanduser("~/.openclaw/skill-backups/")
PROPOSAL_DIR = os.path.expanduser("~/.openclaw/skill-proposals/")

def detect_old_skills():
    """检测已存在的旧技能"""
    existing = []
    for path in OLD_PATHS:
        if os.path.exists(path):
            skill_name = os.path.basename(path)
            # 统计数据量
            if skill_name == "skill-version-control":
                # 统计备份数量
                backup_count = 0
                if os.path.exists(BACKUP_ROOT):
                    for skill_dir in os.listdir(BACKUP_ROOT):
                        if os.path.isdir(os.path.join(BACKUP_ROOT, skill_dir)):
                            backup_count += len([d for d in os.listdir(os.path.join(BACKUP_ROOT, skill_dir)) if os.path.isdir(os.path.join(BACKUP_ROOT, skill_dir, d))])
                # 统计方案数量
                proposal_count = 0
                if os.path.exists(PROPOSAL_DIR):
                    proposal_count = len([f for f in os.listdir(PROPOSAL_DIR) if f.endswith(".json")])
                existing.append({
                    "path": path,
                    "name": skill_name,
                    "backup_count": backup_count,
                    "proposal_count": proposal_count
                })
            else:
                existing.append({
                    "path": path,
                    "name": skill_name,
                    "backup_count": 0,
                    "proposal_count": 0
                })
    return existing

def migrate_data():
    """迁移历史数据"""
    print("\n📦 正在迁移历史数据...")
    # 备份数据已经在全局目录，不需要迁移，直接继承
    print(f"✅ 已继承历史备份数据: {BACKUP_ROOT}")
    print(f"✅ 已继承历史方案数据: {PROPOSAL_DIR}")
    return True

def uninstall_old_skills(old_skills):
    """卸载旧技能"""
    for skill in old_skills:
        try:
            if os.path.exists(skill["path"]):
                shutil.rmtree(skill["path"])
                print(f"✅ 已卸载旧技能: {skill['name']} ({skill['path']})")
        except Exception as e:
            print(f"⚠️  卸载旧技能 {skill['name']} 失败: {str(e)}")
            print("请手动删除该目录")

def main():
    print("🚀 开始安装 better-skill-creator 增强版技能创建工具")
    print("=" * 80)

    # 检测旧技能
    old_skills = detect_old_skills()
    if old_skills:
        print("⚠️  检测到已存在以下旧版本技能:")
        for s in old_skills:
            extra = ""
            if s["backup_count"] > 0:
                extra += f", 包含{s['backup_count']}个历史备份"
            if s["proposal_count"] > 0:
                extra += f", {s['proposal_count']}个优化方案"
            print(f"  - {s['name']}: {s['path']}{extra}")
        
        print("\n请选择操作:")
        print("1. 迁移所有历史数据并卸载旧版本（推荐）")
        print("2. 仅迁移数据，保留旧版本")
        print("3. 不迁移数据，直接安装新版本")
        print("4. 取消安装")

        while True:
            choice = input("\n请输入选项 (1-4): ")
            if choice == "4":
                print("❌ 安装已取消")
                exit(0)
            elif choice in ["1", "2", "3"]:
                break
            else:
                print("❌ 无效选项，请输入1-4")

        if choice in ["1", "2"]:
            migrate_data()
        
        if choice == "1":
            uninstall_old_skills(old_skills)

    print("\n✅ 安装完成!")
    print("=" * 80)
    print("📖 快速开始:")
    print("  创建新技能: python scripts/init_skill.py <skill-name> --path <输出目录>")
    print("  查看版本列表: python scripts/list.py <skill-name>")
    print("  交互式回滚: python scripts/interactive-rollback.py <skill-name>")
    print("  生成优化方案: python scripts/proposal.py generate <skill-name> \"需求描述\"")
    print("\n💡 所有旧版本的历史备份和方案数据已自动继承，可直接使用!")

if __name__ == "__main__":
    main()
