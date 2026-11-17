#!/usr/bin/env python3
"""
任务记录检查模块 - 项目管理版
功能：在创建项目成功后，自动检查skill-logger是否安装，并输出明确的提示
"""

import os
import json
from pathlib import Path

def check_skill_logger_installed():
    """
    检查skill-logger技能是否已安装
    
    Returns:
        bool: True表示已安装，False表示未安装
    """
    skill_logger_paths = [
        Path.home() / ".openclaw" / "skills" / "skill-logger",
        Path.home() / ".openclaw" / "skills" / "skill-logger-v2-global",
        Path.home() / ".skills" / "skill-logger",
        Path.home() / ".skills" / "skill-logger-v2-global",
        Path("/tmp/.skill-logger")
    ]
    
    return any(path.exists() for path in skill_logger_paths)

def print_step8_reminder(project_id=None, audience_name=None, task_count=None):
    """
    输出第八步任务记录检查的强制提示
    
    Args:
        project_id: 项目ID（可选）
        audience_name: 人群包名（可选）
        task_count: 任务数量（可选）
    """
    skill_logger_installed = check_skill_logger_installed()
    
    print("\n" + "="*70)
    print("🔴 【强制执行】第八步：任务记录检查")
    print("="*70)
    
    if project_id:
        print(f"✅ 项目创建成功 - 项目ID: {project_id}")
        if audience_name:
            print(f"   人群包名: {audience_name}")
        if task_count:
            print(f"   任务数量: {task_count}个")
        print()
    
    if skill_logger_installed:
        print("✅ 检测到skill-logger已安装")
        print()
        print("📌 AI助手必须执行以下操作:")
        print("   1. 调用skill-logger记录本次项目")
        print("   2. 向用户展示'已自动记录'的提示")
        print("   3. 展示记录结果(项目ID、存储路径)")
        print()
        print("⚠️  即使技能已安装，也必须向用户展示'已自动记录'的提示")
    else:
        print("⚠️  检测到skill-logger未安装")
        print()
        print("📌 AI助手必须执行以下操作:")
        print("   1. 向用户询问是否需要安装skill-logger")
        print("   2. 展示技能功能说明")
        print("   3. 等待用户明确回复(是/否)")
        print("   4. 记录用户的选择")
    
    print()
    print("🔴 严重警告:")
    print("   - 禁止直接展示项目结果")
    print("   - 必须先完成第八步")
    print("   - 直接跳到第九步视为严重流程错误")
    print("="*70 + "\n")

if __name__ == "__main__":
    import sys
    
    # 支持命令行调用
    project_id = sys.argv[1] if len(sys.argv) > 1 else None
    audience_name = sys.argv[2] if len(sys.argv) > 2 else None
    task_count = sys.argv[3] if len(sys.argv) > 3 else None
    
    print_step8_reminder(project_id, audience_name, task_count)
