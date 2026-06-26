#!/usr/bin/env python3
"""
设置天眼查/企查查登录凭证

使用方法:
    python scripts/setup_credentials.py
"""

import os
import json
import getpass
from pathlib import Path
from cryptography.fernet import Fernet
import base64
import hashlib

CONFIG_DIR = Path.home() / ".due_diligence"
CREDENTIALS_FILE = CONFIG_DIR / "credentials.enc"
KEY_FILE = CONFIG_DIR / ".key"


def get_or_create_key():
    """获取或创建加密密钥"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if KEY_FILE.exists():
        with open(KEY_FILE, "rb") as f:
            return f.read()

    # 生成新密钥
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

    # 设置文件权限
    os.chmod(KEY_FILE, 0o600)

    return key


def encrypt_password(password: str, key: bytes) -> str:
    """加密密码"""
    f = Fernet(key)
    encrypted = f.encrypt(password.encode())
    return base64.b64encode(encrypted).decode()


def decrypt_password(encrypted: str, key: bytes) -> str:
    """解密密码"""
    f = Fernet(key)
    decoded = base64.b64decode(encrypted.encode())
    return f.decrypt(decoded).decode()


def setup_credentials():
    """设置登录凭证"""
    print("=" * 50)
    print("尽职调查工具 - 登录凭证设置")
    print("=" * 50)
    print()

    credentials = {}

    # 天眼查
    print("【天眼查】")
    use_tianyancha = input("是否配置天眼查账号？(y/n): ").lower() == 'y'
    if use_tianyancha:
        username = input("手机号: ").strip()
        password = getpass.getpass("密码: ")
        print()

        credentials["tianyancha"] = {
            "username": username,
            "password": password
        }
        print("✓ 天眼查凭证已配置")
    else:
        print("- 跳过天眼查")
    print()

    # 企查查
    print("【企查查】")
    use_qichacha = input("是否配置企查查账号？(y/n): ").lower() == 'y'
    if use_qichacha:
        username = input("手机号: ").strip()
        password = getpass.getpass("密码: ")
        print()

        credentials["qichacha"] = {
            "username": username,
            "password": password
        }
        print("✓ 企查查凭证已配置")
    else:
        print("- 跳过企查查")
    print()

    if not credentials:
        print("⚠ 未配置任何凭证")
        return

    # 加密保存
    key = get_or_create_key()

    encrypted_credentials = {}
    for source, creds in credentials.items():
        encrypted_credentials[source] = {
            "username": creds["username"],
            "password": encrypt_password(creds["password"], key)
        }

    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(encrypted_credentials, f, indent=2)

    os.chmod(CREDENTIALS_FILE, 0o600)

    print("=" * 50)
    print("✓ 凭证已加密保存到:", CREDENTIALS_FILE)
    print("=" * 50)


def load_credentials():
    """加载登录凭证"""
    if not CREDENTIALS_FILE.exists():
        return None

    key = get_or_create_key()

    with open(CREDENTIALS_FILE, "r") as f:
        encrypted = json.load(f)

    credentials = {}
    for source, creds in encrypted.items():
        credentials[source] = {
            "username": creds["username"],
            "password": decrypt_password(creds["password"], key)
        }

    return credentials


if __name__ == "__main__":
    setup_credentials()
