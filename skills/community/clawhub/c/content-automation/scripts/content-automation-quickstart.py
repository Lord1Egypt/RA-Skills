#!/usr/bin/env python3
"""
content-automation-quickstart.py - 内容自动化工具快速启动脚本
"""

import subprocess
import sys
import os

def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 12:
        return True
    return False

def check_repo():
    """检查是否已克隆仓库"""
    return os.path.exists("./MoneyPrinterV2/src")

def main():
    print("🎬 内容自动化工具快速启动器\n")
    
    # 检查 Python 版本
    if not check_python_version():
        print(f"⚠️  Python 版本 {sys.version.split()[0]}")
        print("❌ 需要 Python 3.12+")
        return
    
    print(f"✅ Python {sys.version.split()[0]}")
    
    # 检查仓库
    if not check_repo():
        print("\n⚠️  未找到 MoneyPrinterV2 仓库")
        print("📥 克隆并安装:")
        print("   git clone https://github.com/FujiwaraChoki/MoneyPrinterV2.git")
        print("   cd MoneyPrinterV2")
        print("   python -m venv venv")
        print("   source venv/bin/activate")
        print("   pip install -r requirements.txt")
        print("   cp config.example.json config.json")
        return
    
    print("✅ 仓库已就绪\n")
    
    # 检查配置
    if not os.path.exists("./MoneyPrinterV2/config.json"):
        print("⚠️  配置文件未创建")
        print("   cp config.example.json config.json")
        print("   # 然后编辑 config.json 填入 API 密钥")
        return
    
    print("✅ 配置文件已存在\n")
    
    # 显示使用指南
    print("📚 快速开始:\n")
    print("1. 编辑配置:")
    print("   vim config.json")
    print("")
    print("2. 运行示例:")
    print("   python src/main.py")
    print("")
    print("3. 查看 SKILL.md 获取:")
    print("   - 批量生成内容示例")
    print("   - 视频脚本创作")
    print("   - 内容日历管理")
    print("")
    print("⚠️  重要提示:")
    print("   本工具仅供内容创作辅助")
    print("   请遵守各平台使用条款")

if __name__ == "__main__":
    main()
