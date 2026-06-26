#!/usr/bin/env python3
"""
任务自动续接脚本 - auto-continue
检查任务状态，判断是否需要继续执行
"""

import json
import os
import sys
import argparse
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(SCRIPT_DIR)
MEMORY_DIR = os.path.join(os.path.dirname(os.path.dirname(WORKSPACE)), "workspace", "memory")
IN_PROGRESS_FILE = os.path.join(MEMORY_DIR, "in_progress.md")

SKILLS_DIR = os.path.join(os.path.dirname(os.path.dirname(WORKSPACE)), "skills")


def read_in_progress():
    """读取任务状态文件"""
    if os.path.exists(IN_PROGRESS_FILE):
        with open(IN_PROGRESS_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def parse_tasks(content):
    """解析任务列表"""
    tasks = []
    current = {}
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("## ") or line.startswith("# "):
            continue
        if line.startswith("- **任务**"):
            current["name"] = line.replace("- **任务**", "").strip()
        elif line.startswith("- **状态**"):
            current["status"] = line.replace("- **状态**", "").strip()
        elif line.startswith("- **下一步**"):
            current["next_step"] = line.replace("- **下一步**", "").strip()
        elif line.startswith("- **开始时间**"):
            current["started"] = line.replace("- **开始时间**", "").strip()
        elif line.startswith("## 待办队列"):
            if current:
                tasks.append(current)
                current = {}
        elif line.startswith("1. [") or line.startswith("2. [") or line.startswith("3. ["):
            bracket_end = line.index("]")
            state = line[3:bracket_end]
            rest = line[bracket_end+2:].strip()
            tasks.append({"state": state, "name": rest})
    if current:
        tasks.append(current)
    return tasks


def check_skill_status():
    """检查 skills 目录下的未完成任务"""
    incomplete = []
    for skill_name in os.listdir(SKILLS_DIR):
        skill_path = os.path.join(SKILLS_DIR, skill_name)
        if not os.path.isdir(skill_path):
            continue
        skill_md = os.path.join(skill_path, "SKILL.md")
        scripts_dir = os.path.join(skill_path, "scripts")
        readme = os.path.join(skill_path, "README.md")

        issues = []
        if not os.path.exists(skill_md):
            issues.append("缺SKILL.md")
        if not os.path.exists(scripts_dir) or not os.listdir(scripts_dir):
            issues.append("scripts目录空/不存在")
        elif not [f for f in os.listdir(scripts_dir) if f.endswith(".py")]:
            issues.append("scripts无Python脚本")

        if issues:
            incomplete.append({
                "skill": skill_name,
                "issues": issues,
                "path": skill_path
            })
    return incomplete


def main():
    parser = argparse.ArgumentParser(description="▶️ 任务自动续接")
    parser.add_argument("--check", "-c", action="store_true", help="检查任务状态")
    parser.add_argument("--status", "-s", action="store_true", help="显示当前状态")
    parser.add_argument("--report", "-r", action="store_true", help="生成续接报告")
    args = parser.parse_args()

    content = read_in_progress()
    tasks = parse_tasks(content) if content else []
    incomplete = check_skill_status()

    print("▶️ 任务自动续接检查")
    print("=" * 50)

    if tasks:
        print("\n📋 进行中的任务：")
        for t in tasks:
            if "name" in t:
                status = t.get("status", "未知")
                next_step = t.get("next_step", "")
                print("  • {} — {}".format(t["name"], status))
                if next_step:
                    print("    → 下一步: {}".format(next_step))
            elif "state" in t:
                print("  • [{}] {}".format(t["state"], t["name"]))

    if incomplete:
        print("\n⚠️ 未完成的 Skills：")
        for item in incomplete:
            print("  • {}: {}".format(item["skill"], ", ".join(item["issues"])))
        print("\n▶️ 建议立即继续执行这些任务！")
    else:
        print("\n✅ 所有 Skill 开发已完成")

    if not tasks and not incomplete:
        print("\n✅ 没有进行中的任务，工作已全部完成")
    else:
        print("\n💡 使用 --report 查看详细续接建议")

    # 如果有未完成任务，返回非零退出码
    if incomplete or (tasks and any(t.get("state", "") == "进行中" for t in tasks)):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
