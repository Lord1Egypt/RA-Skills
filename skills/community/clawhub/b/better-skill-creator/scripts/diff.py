#!/usr/bin/env python3
import os
import json
import argparse
import difflib
from pathlib import Path

BACKUP_ROOT = os.path.expanduser("~/.openclaw/skill-backups/")

def get_version_dir(skill_name, version_id):
    """获取版本目录路径"""
    version_dir = os.path.join(BACKUP_ROOT, skill_name, version_id)
    if not os.path.isdir(version_dir):
        print(f"❌ 版本 {version_id} 不存在")
        exit(1)
    return version_dir

def get_current_skill_path(skill_name):
    """从最新备份中获取Skill的原始路径"""
    skill_backup_dir = os.path.join(BACKUP_ROOT, skill_name)
    versions = sorted([d for d in os.listdir(skill_backup_dir) if os.path.isdir(os.path.join(skill_backup_dir, d))], reverse=True)
    if not versions:
        print(f"❌ 未找到Skill {skill_name} 的备份记录")
        exit(1)
    metadata_path = os.path.join(skill_backup_dir, versions[0], "metadata.json")
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return metadata["source_path"]

def analyze_risk(file_path, diff_lines):
    """分析变更的风险等级"""
    risk_level = "低风险"
    change_type = "文档更新"
    
    # 判断文件类型
    if file_path.endswith("SKILL.md"):
        if any("description:" in line for line in diff_lines):
            risk_level = "中风险"
            change_type = "触发逻辑变更"
        else:
            change_type = "文档更新"
    elif file_path.startswith("scripts/"):
        risk_level = "高风险"
        change_type = "核心代码修改"
    elif file_path.startswith("references/"):
        change_type = "参考文档更新"
    elif file_path.startswith("assets/"):
        change_type = "资源文件更新"
    
    return risk_level, change_type

def diff_directories(dir1, dir2, dir1_name="版本1", dir2_name="版本2"):
    """对比两个目录的内容差异，包含风险评估"""
    diff_output = []
    risk_summary = {
        "高风险": 0,
        "中风险": 0,
        "低风险": 0
    }
    change_summary = {
        "核心代码修改": 0,
        "触发逻辑变更": 0,
        "文档更新": 0,
        "参考文档更新": 0,
        "资源文件更新": 0,
        "新增文件": 0,
        "删除文件": 0
    }
    
    diff_output.append("🔍 差异概览:")
    diff_output.append("-" * 80)
    
    # 遍历第一个目录
    for root, dirs, files in os.walk(dir1):
        rel_path = os.path.relpath(root, dir1)
        for file in files:
            if file == "metadata.json":
                continue
            file1 = os.path.join(root, file)
            file2 = os.path.join(dir2, rel_path, file)
            rel_file_path = os.path.join(rel_path, file)
            
            if not os.path.exists(file2):
                diff_output.append(f"📌 [新增] {rel_file_path} (仅在 {dir1_name} 中存在)")
                change_summary["新增文件"] += 1
                continue
            
            # 对比文件内容
            with open(file1, "r", encoding="utf-8", errors="ignore") as f1, open(file2, "r", encoding="utf-8", errors="ignore") as f2:
                lines1 = f1.readlines()
                lines2 = f2.readlines()
            diff = list(difflib.unified_diff(lines1, lines2, fromfile=f"{dir1_name}/{rel_file_path}", tofile=f"{dir2_name}/{rel_file_path}", lineterm=""))
            
            if diff:
                risk_level, change_type = analyze_risk(rel_file_path, diff)
                risk_summary[risk_level] += 1
                change_summary[change_type] += 1
                
                risk_icon = "🔴" if risk_level == "高风险" else "🟡" if risk_level == "中风险" else "🟢"
                diff_output.append(f"\n{risk_icon} [{risk_level}] {change_type}: {rel_file_path}")
                diff_output.extend(diff)
    
    # 检查第二个目录中新增的文件
    for root, dirs, files in os.walk(dir2):
        rel_path = os.path.relpath(root, dir2)
        for file in files:
            if file == "metadata.json":
                continue
            file1 = os.path.join(dir1, rel_path, file)
            file2 = os.path.join(root, file)
            rel_file_path = os.path.join(rel_path, file)
            
            if not os.path.exists(file1):
                diff_output.append(f"📌 [删除] {rel_file_path} (仅在 {dir2_name} 中存在，{dir1_name}中已删除)")
                change_summary["删除文件"] += 1
    
    # 输出统计摘要
    diff_output.append("\n" + "=" * 80)
    diff_output.append("📊 变更统计:")
    for change_type, count in change_summary.items():
        if count > 0:
            diff_output.append(f"  {change_type}: {count} 处")
    diff_output.append("\n⚠️  风险评估:")
    for risk_level, count in risk_summary.items():
        if count > 0:
            diff_output.append(f"  {risk_level}: {count} 处")
    
    overall_risk = "低风险"
    if risk_summary["高风险"] > 0:
        overall_risk = "高风险"
    elif risk_summary["中风险"] > 0:
        overall_risk = "中风险"
    
    diff_output.append(f"\n🔹 整体风险等级: {overall_risk}")
    diff_output.append("=" * 80)
    
    return "\n".join(diff_output)

def main():
    parser = argparse.ArgumentParser(description="对比Skill版本差异")
    parser.add_argument("skill_name", help="Skill名称")
    parser.add_argument("version1", help="第一个版本ID")
    parser.add_argument("version2", nargs="?", help="第二个版本ID（可选，默认对比当前版本）")
    args = parser.parse_args()

    dir1 = get_version_dir(args.skill_name, args.version1)
    if args.version2:
        dir2 = get_version_dir(args.skill_name, args.version2)
        dir2_name = args.version2
    else:
        dir2 = get_current_skill_path(args.skill_name)
        dir2_name = "当前版本"

    print(f"🔍 对比 {args.skill_name} 版本差异: {args.version1} vs {dir2_name}")
    print("=" * 120)
    diff_result = diff_directories(dir1, dir2, args.version1, dir2_name)
    if not diff_result:
        print("✅ 两个版本内容完全一致")
    else:
        print(diff_result)

if __name__ == "__main__":
    main()
