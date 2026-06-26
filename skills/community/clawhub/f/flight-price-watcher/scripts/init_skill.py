#!/usr/bin/env python3
"""
Flight Price Watcher - 技能初始化脚本

用法:
    python scripts/init_skill.py

功能:
    1. 检查 FlyAI CLI 是否已安装
    2. 创建初始任务数据文件
    3. 验证技能配置
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# 技能根目录
SKILL_ROOT = Path(__file__).parent.parent

def check_flyai_cli():
    """检查 FlyAI CLI 是否已安装"""
    print("🔍 检查 FlyAI CLI 安装状态...")
    
    try:
        result = subprocess.run(
            ["flyai", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✅ FlyAI CLI 已安装：{result.stdout.strip()}")
            return True
        else:
            print("❌ FlyAI CLI 未正确安装")
            return False
    except FileNotFoundError:
        print("❌ FlyAI CLI 未安装")
        print("\n📦 请运行以下命令安装:")
        print("   npm i @fly-ai/flyai-cli")
        return False
    except subprocess.TimeoutExpired:
        print("⚠️  检查超时，可能未正确安装")
        return False

def init_data_file():
    """初始化任务数据文件"""
    data_file = SKILL_ROOT / "data" / "tasks.json"
    
    if data_file.exists():
        print(f"✅ 数据文件已存在：{data_file}")
        return True
    
    try:
        # 确保目录存在
        data_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 创建初始数据
        initial_data = {
            "tasks": [],
            "nextTaskId": 1
        }
        
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 数据文件已创建：{data_file}")
        return True
    except Exception as e:
        print(f"❌ 创建数据文件失败：{e}")
        return False

def verify_structure():
    """验证技能目录结构"""
    print("\n📁 验证技能目录结构...")
    
    required_files = [
        "SKILL.md",
        "package.json",
        "scripts/monitor.js",
        "scripts/task_manager.js",
        "references/flyai-cli-docs.md",
        "references/pricing-strategy.md",
        "data/tasks.json",
    ]
    
    all_ok = True
    for file_path in required_files:
        full_path = SKILL_ROOT / file_path
        if full_path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} (缺失)")
            all_ok = False
    
    return all_ok

def main():
    """主函数"""
    print("=" * 50)
    print("🛫 Flight Price Watcher - 技能初始化")
    print("=" * 50)
    
    # 1. 检查 FlyAI CLI
    cli_ok = check_flyai_cli()
    
    # 2. 初始化数据文件
    data_ok = init_data_file()
    
    # 3. 验证目录结构
    structure_ok = verify_structure()
    
    # 总结
    print("\n" + "=" * 50)
    if cli_ok and data_ok and structure_ok:
        print("✅ 技能初始化完成！可以开始使用了")
        print("\n📝 使用方式:")
        print("   对助手说：'帮我监控北京到上海 4 月 15 日的机票'")
        return 0
    else:
        print("⚠️  技能初始化未完成，请检查上述错误")
        if not cli_ok:
            print("\n💡 提示：需要先安装 FlyAI CLI")
            print("   命令：npm i @fly-ai/flyai-cli")
        return 1

if __name__ == "__main__":
    sys.exit(main())
