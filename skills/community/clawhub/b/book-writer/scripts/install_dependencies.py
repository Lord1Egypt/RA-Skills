#!/usr/bin/env python3
"""
依赖安装脚本 - 自动安装智能写书技能所需的所有依赖
"""

import subprocess
import sys
import os
import platform

def run_command(cmd, description=""):
    """运行命令并显示进度"""
    if description:
        print(f"🔧 {description}...")

    print(f"   💻 执行: {cmd}")

    try:
        result = subprocess.run(cmd, shell=True, check=True,
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ 成功")
            if result.stdout.strip():
                print(f"   输出: {result.stdout.strip()}")
            return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ 失败")
        print(f"   错误: {e.stderr}")
        if e.stdout.strip():
            print(f"   输出: {e.stdout}")
        return False
    return True

def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    version = sys.version_info
    print(f"   当前Python版本: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("   ❌ 需要Python 3.8或更高版本")
        return False
    print("   ✅ Python版本满足要求")
    return True

def install_pip_packages():
    """安装必要的Python包"""
    packages = [
        "openai>=1.0.0",
        "requests>=2.28.0",
        "pyyaml>=6.0",
        "python-dotenv>=0.19.0",
        "tiktoken>=0.3.0",
        "beautifulsoup4>=4.11.0",
        "lxml>=4.9.0"
    ]

    print("📦 安装Python依赖包...")

    for package in packages:
        package_name = package.split(">=")[0].split("<=")[0]
        cmd = f"{sys.executable} -m pip install --upgrade {package}"
        run_command(cmd, f"安装 {package_name}")

    return True

def setup_environment():
    """设置环境变量和配置"""
    print("⚙️ 设置环境...")

    # 创建必要的目录
    directories = [
        "generated_books",
        "temp_files",
        "logs"
    ]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   📁 创建目录: {directory}")

    # 检查API密钥环境变量
    print("🔑 检查API密钥环境变量...")
    api_keys = {
        "OPENAI_API_KEY": "OpenAI API密钥",
        "GOOGLE_CSE_ID": "Google自定义搜索引擎ID",
        "GOOGLE_API_KEY": "Google API密钥"
    }

    missing_keys = []
    for key, description in api_keys.items():
        if os.environ.get(key):
            print(f"   ✅ {description}: 已设置")
        else:
            print(f"   ⚠️  {description}: 未设置")
            missing_keys.append(key)

    if missing_keys:
        print(f"\n🔔 需要设置以下环境变量:")
        for key in missing_keys:
            print(f"   export {key}=your_api_key_here")
        print("\n💡 提示: 可以将这些设置添加到 ~/.bashrc 或 ~/.zshrc")

    return True

def main():
    """主安装函数"""
    print("🚀 开始安装智能写书技能依赖...")
    print("=" * 60)

    # 检查Python版本
    if not check_python_version():
        sys.exit(1)

    # 安装pip包
    if not install_pip_packages():
        print("❌ Python包安装失败")
        sys.exit(1)

    # 设置环境
    setup_environment()

    print("\n" + "=" * 60)
    print("🎉 安装完成！")
    print("\n📋 后续步骤:")
    print("1. 设置API密钥环境变量")
    print("2. 开始使用写书技能!")

    return 0

if __name__ == "__main__":
    main()