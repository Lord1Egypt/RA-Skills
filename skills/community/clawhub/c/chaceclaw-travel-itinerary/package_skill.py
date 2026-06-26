#!/usr/bin/env python3
"""
打包旅行规划技能为分享格式
修复版：文件名和路径修正
"""
import os
import zipfile
from datetime import datetime

def create_skill_package():
    """创建技能包"""
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    skill_name = os.path.basename(skill_dir)

    # 输出到 skill 目录
    output_zip = os.path.join(skill_dir, f"{skill_name}-v1.0.0.zip")

    # 需要包含的文件（SKILL.md 大写）
    files_to_include = [
        "SKILL.md",
        "README.md",
        "_meta.json",
        "requirements.txt",
        "travel_planner.py",
        "travel_planner_extensions.py",
        "user_trip_planner.py",
        "complete_demo.py",
    ]

    # 检查文件
    missing_files = []
    for file in files_to_include:
        file_path = os.path.join(skill_dir, file)
        if not os.path.exists(file_path):
            missing_files.append(file)

    if missing_files:
        print(f"❌ 缺少文件: {', '.join(missing_files)}")
        return None

    print("📦 开始打包技能包...")

    # 创建 ZIP（覆盖旧文件）
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_include:
            file_path = os.path.join(skill_dir, file)
            zipf.write(file_path, file)
            print(f"  ✅ 已添加: {file}")

    file_size = os.path.getsize(output_zip)
    print(f"\n✅ 技能包已创建: {output_zip}")
    print(f"📦 文件大小: {file_size / 1024:.1f} KB")

    print("\n📋 包含的文件:")
    with zipfile.ZipFile(output_zip, 'r') as zipf:
        for info in zipf.infolist():
            print(f"  - {info.filename} ({info.file_size / 1024:.1f} KB)")

    return output_zip

if __name__ == "__main__":
    print("🚀 旅行规划技能打包工具 v1.0.1")
    print("=" * 60)
    result = create_skill_package()
    if result:
        print("\n✅ 打包成功！")
    else:
        print("\n❌ 打包失败")