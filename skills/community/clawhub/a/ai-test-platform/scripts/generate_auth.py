#!/usr/bin/env python3
"""
AI 自动化测试平台 - 授权码生成器

使用AES加密生成授权码，密钥基于"yanghua"+时间戳+"360"组合
"""

import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import secrets
import string

def generate_encryption_key():
    """
    生成AES加密密钥
    格式: "yanghua" + 当前时间戳 + "360sb"
    """
    encryption_key = f"yanghua{int(time.time())}360"
    # 确保密钥长度为16, 24, 或32字节（AES标准）
    encryption_key = encryption_key[:32].ljust(32, '0')[:32]
    return encryption_key.encode('utf-8')

def encrypt_auth_code(code, key):
    """
    使用AES加密授权码

    Args:
        code: 原始授权码字符串
        key: AES加密密钥

    Returns:
        加密后的授权码（base64编码）
    """
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(code.encode('utf-8'), AES.block_size))
    return base64.b64encode(encrypted).decode('utf-8')

def generate_random_code(length=16):
    """
    生成随机授权码

    Args:
        length: 授权码长度

    Returns:
        随机生成的原始授权码
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_authorization_code(permission='all', max_days=365, max_count=100):
    """
    生成完整的授权码信息

    Args:
        permission: 权限类型 (all/generate/execute)
        max_days: 有效期（天）
        max_count: 最大使用次数

    Returns:
        包含授权码信息的字典
    """
    # 生成加密密钥
    key = generate_encryption_key()

    # 生成原始授权码
    original_code = generate_random_code(16)

    # 加密授权码
    encrypted_code = encrypt_auth_code(original_code, key)

    from datetime import datetime, timedelta
    import json

    # 计算过期时间
    expire_time = datetime.now() + timedelta(days=max_days)

    auth_info = {
        'original_code': original_code,
        'encrypted_code': encrypted_code,
        'permission': permission,
        'expire_time': expire_time.strftime('%Y-%m-%d %H:%M:%S'),
        'max_count': max_count,
        'encrypt_key': key.decode('utf-8')  # 只用于显示，实际使用时应该安全存储
    }

    return auth_info

def main():
    """
    主函数：交互式生成授权码
    """
    print("=" * 80)
    print("AI 自动化测试平台 - 授权码生成器")
    print("=" * 80)
    print()

    while True:
        print("请选择权限类型：")
        print("1. 全功能权限 (all)")
        print("2. 仅生成权限 (generate)")
        print("3. 仅执行权限 (execute)")
        print("4. 退出")

        choice = input("\n请输入选项 (1-4): ").strip()

        if choice == '4':
            print("退出授权码生成器。")
            break

        if choice not in ['1', '2', '3']:
            print("无效选项，请重新选择。\n")
            continue

        # 权限映射
        permission_map = {
            '1': 'all',
            '2': 'generate',
            '3': 'execute'
        }
        permission = permission_map[choice]

        # 获取有效期
        try:
            max_days = int(input("请输入有效期（天，默认365）: ").strip() or "365")
        except ValueError:
            print("无效的数字，使用默认值365天。\n")
            max_days = 365

        # 获取使用次数
        try:
            max_count = int(input("请输入最大使用次数（默认100）: ").strip() or "100")
        except ValueError:
            print("无效的数字，使用默认值100次。\n")
            max_count = 100

        # 生成授权码
        print("\n正在生成授权码...")
        auth_info = generate_authorization_code(permission, max_days, max_count)

        # 显示结果
        print("\n" + "=" * 80)
        print("授权码生成成功！")
        print("=" * 80)
        print(f"权限类型: {auth_info['permission']}")
        print(f"过期时间: {auth_info['expire_time']}")
        print(f"最大使用次数: {auth_info['max_count']}")
        print(f"原始授权码: {auth_info['original_code']}")
        print(f"加密授权码: {auth_info['encrypted_code']}")
        print(f"加密密钥: {auth_info['encrypt_key']}")
        print("=" * 80)
        print()
        print("注意：")
        print("- 请妥善保存加密授权码和加密密钥")
        print("- 加密密钥用于解密和验证，必须安全存储")
        print("- 原始授权码仅用于记录，实际使用加密授权码")
        print()
        print("-" * 80)
        print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序已中断。")
    except Exception as e:
        print(f"\n发生错误: {str(e)}")
