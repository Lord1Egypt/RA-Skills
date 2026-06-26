#!/usr/bin/env python3
"""
金甲龙虾安装脚本
"""

import os
import sys
import subprocess


def run_command(cmd, description):
    """运行命令"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败: {e}")
        print(f"   {e.stderr}")
        return False


def main():
    print("🦞 金甲龙虾 - 安装向导")
    print("=" * 40)

    # 检查 Python 版本
    if sys.version_info < (3, 8):
        print("❌ 需要 Python 3.8 或更高版本")
        return

    print(f"✅ Python 版本: {sys.version_info.major}.{sys.version_info.minor}")

    # 安装依赖
    print("\n正在安装依赖...")
    success = run_command(
        sys.executable + " -m pip install -r requirements.txt",
        "安装 Python 依赖"
    )

    if not success:
        print("\n⚠️ 部分依赖安装失败，可能需要手动安装")

    # 创建 .env 文件（如果不存在）
    env_file = ".env"
    if not os.path.exists(env_file):
        print(f"\n📝 创建 {env_file} 模板...")
        try:
            import shutil
            shutil.copy(".env.example", env_file)
            print(f"✅ 已创建 {env_file}")
            print(f"⚠️ 请编辑 {env_file} 填入你的币安 API Key")
        except Exception as e:
            print(f"❌ 创建 {env_file} 失败: {e}")

    print("\n🎉 安装完成！")
    print("\n下一步:")
    print("1. 编辑 .env 文件，填入你的币安 API Key 和 Secret")
    print("2. 运行: python main.py --check  (进行安全检查)")
    print("   或运行: python main.py --all    (运行所有检查)")
    print("\n💡 提示: 建议使用子账户，并绑定 IP 白名单")


if __name__ == "__main__":
    main()
