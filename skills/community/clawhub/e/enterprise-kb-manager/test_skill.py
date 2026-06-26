#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业知识库技能测试脚本
验证技能的各个功能是否正常工作
"""

import os
import sys
import subprocess
from pathlib import Path

def test_skill():
    """测试技能功能"""
    print("🧪 企业知识库技能测试")
    print("=" * 50)
    
    skill_dir = Path(__file__).parent
    main_script = skill_dir / "main.py"
    
    if not main_script.exists():
        print("❌ main.py 文件不存在")
        return False
    
    # 测试帮助命令
    print("1️⃣ 测试帮助命令...")
    try:
        result = subprocess.run([sys.executable, str(main_script), "help"], 
                              capture_output=True, text=True, cwd=skill_dir)
        if result.returncode == 0:
            print("✅ 帮助命令正常")
        else:
            print(f"❌ 帮助命令失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 帮助命令异常: {e}")
        return False
    
    # 测试统计命令
    print("2️⃣ 测试统计命令...")
    try:
        result = subprocess.run([sys.executable, str(main_script), "stats"], 
                              capture_output=True, text=True, cwd=skill_dir)
        if result.returncode == 0:
            print("✅ 统计命令正常")
        else:
            print(f"❌ 统计命令失败: {result.stderr}")
    except Exception as e:
        print(f"❌ 统计命令异常: {e}")
    
    # 测试列表命令
    print("3️⃣ 测试列表命令...")
    try:
        result = subprocess.run([sys.executable, str(main_script), "list"], 
                              capture_output=True, text=True, cwd=skill_dir)
        if result.returncode == 0:
            print("✅ 列表命令正常")
        else:
            print(f"❌ 列表命令失败: {result.stderr}")
    except Exception as e:
        print(f"❌ 列表命令异常: {e}")
    
    # 测试查询命令（如果有数据）
    print("4️⃣ 测试查询命令...")
    try:
        result = subprocess.run([sys.executable, str(main_script), "query", "测试查询"], 
                              capture_output=True, text=True, cwd=skill_dir)
        if result.returncode == 0:
            print("✅ 查询命令正常")
        else:
            print(f"⚠️ 查询命令: {result.stderr}")
    except Exception as e:
        print(f"❌ 查询命令异常: {e}")
    
    print("\n" + "=" * 50)
    print("✅ 技能测试完成")
    print("\n💡 使用方法:")
    print("  在 OpenClaw 中: @kb-manager <命令>")
    print("  直接执行: python main.py <命令>")
    
    return True

if __name__ == "__main__":
    test_skill()