#!/usr/bin/env python3
"""
记忆系统设置脚本（简化版）

功能：
1. 创建记忆系统目录结构
2. 复制模板文件到工作区
3. 初始化核心记忆文件

注意：这是简化版脚本，完整功能请参考Claude Code进化技能文档。
"""

import os
import sys
import shutil
from pathlib import Path

def print_header():
    """打印脚本标题"""
    print("=" * 60)
    print("Claude Code记忆系统设置")
    print("=" * 60)
    print("此脚本将帮助您设置基于Claude Code架构的记忆系统。")
    print()

def get_workspace_root() -> str:
    """获取工作区根目录"""
    # 首先尝试环境变量
    workspace = os.environ.get("OPENCLAW_WORKSPACE")
    if workspace and os.path.exists(workspace):
        return workspace
    
    # 默认位置
    default = os.path.expanduser("~/.openclaw/workspace")
    if os.path.exists(default):
        return default
    
    # 使用当前目录
    return os.getcwd()

def create_directory_structure(workspace_root: str):
    """创建目录结构"""
    print("📁 创建目录结构...")
    
    directories = [
        "memory",
        "memory/audit-logs",
        "scripts",
        "references"
    ]
    
    for directory in directories:
        path = os.path.join(workspace_root, directory)
        os.makedirs(path, exist_ok=True)
        print(f"  ✅ {directory}")
    
    print()

def copy_template_files(workspace_root: str, skill_root: str):
    """复制模板文件"""
    print("📄 复制模板文件...")
    
    # 模板源目录
    templates_dir = os.path.join(skill_root, "references", "memory-templates")
    
    if not os.path.exists(templates_dir):
        print(f"  ⚠️ 模板目录不存在: {templates_dir}")
        print(f"  请确保技能包包含 references/memory-templates/ 目录")
        return False
    
    # 目标目录
    memory_dir = os.path.join(workspace_root, "memory")
    
    # 要复制的模板文件
    templates = [
        ("user-profile.md", "用户画像模板"),
        ("project-states.md", "项目状态模板"),
        ("feedback-logs.md", "反馈记录模板"),
        ("reference-pointers.md", "引用指针模板"),
        ("memory-index-template.md", "记忆索引模板")
    ]
    
    copied = 0
    for filename, description in templates:
        src = os.path.join(templates_dir, filename)
        dst = os.path.join(memory_dir, filename)
        
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  ✅ {description}: {filename}")
            copied += 1
        else:
            print(f"  ⚠️ 模板不存在: {filename}")
    
    print(f"\n  共复制 {copied}/{len(templates)} 个模板文件")
    return copied > 0

def create_initial_memory_index(workspace_root: str):
    """创建初始记忆索引"""
    print("📋 创建初始记忆索引...")
    
    memory_index_path = os.path.join(workspace_root, "MEMORY.md")
    
    # 检查是否已存在
    if os.path.exists(memory_index_path):
        print(f"  ⚠️ MEMORY.md 已存在，跳过创建")
        return False
    
    # 从模板创建
    template_path = os.path.join(workspace_root, "memory", "memory-index-template.md")
    
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换占位符
        from datetime import datetime
        now = datetime.now()
        content = content.replace("YYYY-MM-DD", now.strftime("%Y-%m-%d"))
        content = content.replace("HH:MM", now.strftime("%H:%M"))
        
        with open(memory_index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ 创建 MEMORY.md")
        return True
    else:
        print(f"  ⚠️ 索引模板不存在，创建基础版本")
        
        basic_index = """# MEMORY.md — 记忆索引

## 记忆类型
- [用户画像](memory/user-profile.md) -- 用户的基本信息和偏好
- [项目状态](memory/project-states.md) -- 项目进度和状态
- [反馈记录](memory/feedback-logs.md) -- 错误和反馈信息
- [引用指针](memory/reference-pointers.md) -- 系统配置和资源引用

## 最近记忆
- [未设置](memory/YYYY-MM-DD.md) -- 请开始记录您的日常活动

---
*初始创建时间: {}*
""".format(now.strftime("%Y-%m-%d %H:%M"))
        
        with open(memory_index_path, 'w', encoding='utf-8') as f:
            f.write(basic_index)
        
        print(f"  ✅ 创建基础版 MEMORY.md")
        return True

def validate_setup(workspace_root: str):
    """验证设置结果"""
    print("\n" + "=" * 60)
    print("验证设置结果")
    print("=" * 60)
    
    required = [
        ("memory/", "记忆目录", True),
        ("memory/user-profile.md", "用户画像模板", False),
        ("memory/project-states.md", "项目状态模板", False),
        ("memory/feedback-logs.md", "反馈记录模板", False),
        ("memory/reference-pointers.md", "引用指针模板", False),
        ("MEMORY.md", "记忆索引文件", False),
    ]
    
    all_ok = True
    for path, description, required_flag in required:
        full_path = os.path.join(workspace_root, path)
        exists = os.path.exists(full_path)
        
        if exists:
            print(f"  ✅ {description}")
        elif required_flag:
            print(f"  ❌ {description} (必需)")
            all_ok = False
        else:
            print(f"  ⚠️ {description} (可选)")
    
    print()
    if all_ok:
        print("🎉 记忆系统设置完成！")
        print("\n下一步操作：")
        print("1. 编辑 memory/user-profile.md 填写您的用户信息")
        print("2. 查看 MEMORY.md 了解记忆索引格式")
        print("3. 运行 python scripts/validate_memory.py 验证系统")
    else:
        print("⚠️ 设置完成，但缺少一些可选文件")
        print("  请检查技能包是否包含完整的模板文件")
    
    return all_ok

def main():
    """主函数"""
    print_header()
    
    # 获取技能包根目录（此脚本所在目录的父目录）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_root = os.path.dirname(script_dir)
    
    # 获取工作区根目录
    workspace_root = get_workspace_root()
    print(f"工作区根目录: {workspace_root}")
    print(f"技能包目录: {skill_root}")
    print()
    
    # 确认操作
    response = input("是否继续设置记忆系统？(y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("操作已取消")
        sys.exit(0)
    
    print()
    
    # 执行设置步骤
    create_directory_structure(workspace_root)
    
    if not copy_template_files(workspace_root, skill_root):
        print("⚠️ 模板复制可能不完整，请手动检查")
    
    create_initial_memory_index(workspace_root)
    
    validate_setup(workspace_root)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        sys.exit(1)