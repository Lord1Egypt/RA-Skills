#!/usr/bin/env python3
"""
AI Coding Tools Full Suite - Skill Packaging Script
打包AI编程工具全能套件技能包
"""

import os
import json
import shutil
import zipfile
from datetime import datetime

# 配置
SKILL_DIR = "/workspace/temp-skills/ai-coding-tools-full-suite"
OUTPUT_DIR = "/workspace/temp-skills/packages"
PACKAGE_NAME = "ai-coding-tools-full-suite"
VERSION = "1.0.0"

def read_meta():
    """读取技能元数据"""
    meta_path = os.path.join(SKILL_DIR, "_meta.json")
    with open(meta_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_skill_md():
    """读取技能主文件"""
    skill_path = os.path.join(SKILL_DIR, "SKILL.md")
    with open(skill_path, 'r', encoding='utf-8') as f:
        return f.read()

def list_references():
    """列出参考文档"""
    refs_dir = os.path.join(SKILL_DIR, "references")
    if not os.path.exists(refs_dir):
        return []
    return [f for f in os.listdir(refs_dir) if f.endswith('.md')]

def create_package_info():
    """创建包信息"""
    meta = read_meta()

    package_info = {
        "name": PACKAGE_NAME,
        "version": VERSION,
        "created": datetime.now().isoformat(),
        "skill_id": meta.get("skill-id", ""),
        "description": meta.get("description", ""),
        "tags": meta.get("tags", []),
        "sub_skills": meta.get("sub-skills", []),
        "commands": meta.get("commands", []),
        "files": {
            "main": "SKILL.md",
            "meta": "_meta.json",
            "references": list_references()
        },
        "stats": {
            "main_file_lines": len(read_skill_md().splitlines()),
            "references_count": len(list_references()),
            "sub_skills_count": len(meta.get("sub-skills", []))
        }
    }

    return package_info

def package_skill():
    """打包技能"""
    print(f"📦 开始打包技能: {PACKAGE_NAME} v{VERSION}")

    # 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 创建包信息
    package_info = create_package_info()

    # 打包文件列表
    files_to_package = [
        ("SKILL.md", "SKILL.md"),
        ("_meta.json", "_meta.json"),
    ]

    # 添加参考文档
    for ref in list_references():
        files_to_package.append(
            (os.path.join("references", ref), os.path.join("references", ref))
        )

    # 创建ZIP包
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"{PACKAGE_NAME}_v{VERSION}_{timestamp}.zip"
    zip_path = os.path.join(OUTPUT_DIR, zip_filename)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for source_path, archive_path in files_to_package:
            full_path = os.path.join(SKILL_DIR, source_path)
            if os.path.exists(full_path):
                zipf.write(full_path, archive_path)
                print(f"  ✓ 添加: {archive_path}")

    # 保存包信息JSON
    info_path = os.path.join(OUTPUT_DIR, f"{PACKAGE_NAME}_info.json")
    with open(info_path, 'w', encoding='utf-8') as f:
        json.dump(package_info, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 打包完成!")
    print(f"   包路径: {zip_path}")
    print(f"   包信息: {info_path}")
    print(f"\n📊 包统计:")
    print(f"   - 主文件: {package_info['stats']['main_file_lines']} 行")
    print(f"   - 参考文档: {package_info['stats']['references_count']} 个")
    print(f"   - 子技能: {package_info['stats']['sub_skills_count']} 个")

    return zip_path, package_info

if __name__ == "__main__":
    package_skill()
