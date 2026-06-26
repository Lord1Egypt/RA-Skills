#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化配置向导
首次运行时引导用户配置 APPKEY 和 SECRET

支持两种使用方式：
1. 交互模式：python init_config.py
2. 非交互模式（推荐大模型使用）：python init_config.py --appkey <APPKEY> --secret <SECRET>
"""

import os
import json
import getpass
import re
import sys
import argparse

from duwi_client import DuwiClient

script_dir = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(script_dir, 'app_config.json')

def print_banner():
    """打印欢迎横幅"""
    print("\n")
    print("=" * 50)
    print("            迪惟智能家居技能 - 配置向导")
    print("=" * 50)

def check_is_require_config(force: bool = False):
    """检查是否需要进行配置"""
    if os.path.exists(CONFIG_FILE):
        if force:
            print("ℹ️  将覆盖现有配置：app_config.json")
            return True
        print("⚠️  检测到已有配置文件：app_config.json")
        print()
        print("💡 提示：如需重新配置，请添加 --force 参数")
        print()
        print("示例：python init_config.py --force")
        print("      python init_config.py --appkey <APPKEY> --secret <SECRET> --force")
        print()
        return False
    return True

def validate_credentials(appkey: str, secret: str) -> tuple[bool, str]:
    """
    验证凭证格式
    
    Returns:
        (是否有效，错误信息)
    """
    if not appkey or not secret:
        return False, "APPKEY 和 SECRET 不能为空"
    
    # 验证 UUID 格式（带横线的 36 位标准 UUID）
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE
    )

    if len(appkey) < 30 or not uuid_pattern.match(appkey):
        return False, "APPKEY 格式不正确（应该是 UUID 格式，36 位，如：xxxxx-xxxx-...）"

    # 验证 SECRET 格式（32 位十六进制字符串，无横线）
    secret_pattern = re.compile(r'^[0-9a-f]{32}$', re.IGNORECASE)

    if len(secret) < 30 or not secret_pattern.match(secret):
        return False, "SECRET 格式不正确（应该是 32 位十六进制字符串，无横线）"
    
    return True, ""

def get_app_credentials():
    """获取应用凭证（交互模式）"""
    print("\n📋 需要配置迪惟开放平台应用凭证")
    print()
    print("💡 如何获取：")
    print("1. 邮箱联系迪惟研发中心")
    print("2. 审核通过，获取授权，分配 APPKEY 和 SECRET")
    print("3. 复制 APPKEY 和 SECRET")
    print()
    print("⚠️  注意：")
    print("- 这是应用级凭证，不是个人账户信息")
    print("- 请妥善保管，不要分享给他人")
    print("- 配置文件仅保存在本地，不会上传")
    print("- 输入时密码将隐藏显示")
    print()
    print("💡 提示：也可以使用非交互模式一次性传入凭证：")
    print("   python init_config.py --appkey <APPKEY> --secret <SECRET>")
    print()
    appkey = input("请输入 APPKEY: ").strip()
    secret = getpass.getpass("请输入 SECRET: ").strip()

    valid, error_msg = validate_credentials(appkey, secret)
    if not valid:
        print(f"\n❌ {error_msg}")
        print("💡 请检查凭证格式后重新运行")
        return None, None

    return appkey, secret

def save_config(appkey, secret):
    """保存配置"""
    config = {
        "appkey": appkey,
        "secret": secret,
        "note": "这是迪惟开放平台应用凭证，请妥善保管"
    }

    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    try:
        os.chmod(CONFIG_FILE, 0o600)
    except Exception:
        pass

    print(f"\n✅ 配置已保存至：{CONFIG_FILE}")
    print("🔒 文件权限已设置为仅所有者可读写")

def load_config():
    """加载配置"""
    if not os.path.exists(CONFIG_FILE):
        return None, None

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)

    return config.get('appkey'), config.get('secret')

def print_next_steps():
    """打印下一步操作提示"""
    print("\n" + "=" * 50)
    print("✅ 配置完成！")
    print()
    print("下一步:")
    print("1. 登录账户:")
    print("   python duwi_cli.py login <手机号> <密码>")
    print()
    print("2. 选择房屋:")
    print("   python duwi_cli.py choose-house")
    print("   或：python duwi_cli.py choose-house --house_no <房屋编号>")
    print()
    print("3. 开始使用智能家居控制功能")
    print("=" * 50)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='迪惟智能家居技能 - 配置向导',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  交互模式：python init_config.py
  非交互模式：python init_config.py --appkey <APPKEY> --secret <SECRET>
  强制重新配置：python init_config.py --force
  强制重新配置（非交互）：python init_config.py --appkey <APPKEY> --secret <SECRET> --force

获取凭证:
  邮箱联系迪惟研发中心
'''
    )
    parser.add_argument('--appkey', help='应用 KEY（UUID 格式）')
    parser.add_argument('--secret', help='应用密钥（32 位十六进制）')
    parser.add_argument('--force', action='store_true', help='强制重新配置，覆盖现有配置')
    
    args = parser.parse_args()

    print_banner()

    # 检查是否需要配置
    if not check_is_require_config(args.force):
        print("\n👌 使用现有配置")
        appkey, secret = load_config()
        if appkey:
            print(f"APPKEY: {appkey[:8]}...{appkey[-8:]}")
        print()
        print("💡 如需重新配置，请添加 --force 参数")
        return

    # 非交互模式：从命令行参数获取凭证
    if args.appkey and args.secret:
        print("\nℹ️  使用命令行参数提供的凭证")
        valid, error_msg = validate_credentials(args.appkey, args.secret)
        if not valid:
            print(f"\n❌ {error_msg}")
            print("💡 请检查凭证格式后重新运行")
            sys.exit(1)
        appkey, secret = args.appkey, args.secret
    else:
        # 交互模式
        if args.appkey or args.secret:
            print("\n⚠️  警告：--appkey 和 --secret 必须同时提供")
            print("💡 请同时提供两个参数，或不提供以使用交互模式")
            sys.exit(1)
        appkey, secret = get_app_credentials()
        if not appkey or not secret:
            print("\n❌ 配置取消")
            sys.exit(1)

    print("\n🔄 正在验证凭证...")
    client = DuwiClient(appkey, secret)

    if client.verify_credentials():
        print("✅ 凭证验证成功")
    else:
        print("\n⚠️  凭证验证失败，可能原因：")
        print("   - APPKEY 或 SECRET 不正确")
        print("   - 应用未授权或已过期")
        print("   - 网络连接问题")
        print()
        print("💡 建议：")
        print("   - 检查凭证是否正确复制（注意不要有多余空格）")
        print("   - 联系迪惟研发中心确认应用状态")
        print()
        # 判断是否是交互模式：没有提供 --appkey 和 --secret 参数
        is_interactive = not (args.appkey and args.secret)
        
        if is_interactive:
            print("⚠️  仍要保存吗？保存后可能导致后续 API 调用失败")
            confirm = input("是否仍要保存？(y/n): ").strip().lower()
            if confirm != 'y':
                print("\n❌ 配置取消")
                sys.exit(1)
        else:
            print("⚠️  非交互模式：将保存凭证，请在后续使用中注意验证")
        # 非交互模式下继续保存

    save_config(appkey, secret)
    print_next_steps()


if __name__ == "__main__":
    main()
