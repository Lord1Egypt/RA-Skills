#!/usr/bin/env python3
"""
Agent Reach Cookie 加密工具
使用 AES-256-GCM 加密存储敏感的 Cookie 数据
"""

import os
import json
import base64
import getpass
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any
import hashlib

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.backends import default_backend
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("警告: cryptography 未安装，将使用基础加密")
    import secrets

class CookieEncryptor:
    """Cookie 加密器"""

    def __init__(self, config_dir: str = None):
        self.config_dir = Path(config_dir or os.path.expanduser("~/.config/agent-reach-secure"))
        self.config_dir.mkdir(parents=True, exist_ok=True, mode=0o700)

        self.cookies_file = self.config_dir / "cookies.json"
        self.encrypted_file = self.config_dir / "cookies.enc"
        self.key_file = self.config_dir / ".key"

    def _generate_key(self) -> bytes:
        """生成加密密钥"""
        if CRYPTO_AVAILABLE:
            return AESGCM.generate_key(bit_length=256)
        else:
            return secrets.token_bytes(32)

    def _get_or_create_key(self, password: str = None) -> bytes:
        """获取或创建加密密钥"""
        if self.key_file.exists():
            # 从密码派生密钥
            if password:
                kdf = hashlib.pbkdf2_hmac('sha256', password.encode(), b'agent-reach-salt', 100000)
                return kdf
            else:
                with open(self.key_file, 'rb') as f:
                    return f.read()
        else:
            # 创建新密钥
            key = self._generate_key()
            if password:
                # 如果提供密码，派生密钥
                key = hashlib.pbkdf2_hmac('sha256', password.encode(), b'agent-reach-salt', 100000)
            else:
                # 保存密钥文件
                with open(self.key_file, 'wb') as f:
                    f.write(key)
                os.chmod(self.key_file, 0o600)
            return key

    def encrypt_cookies(self, cookies: Dict[str, Any], password: str = None) -> bool:
        """加密 Cookie 数据"""
        try:
            key = self._get_or_create_key(password)
            plaintext = json.dumps(cookies).encode()

            if CRYPTO_AVAILABLE:
                # 使用 AES-256-GCM
                aesgcm = AESGCM(key)
                nonce = os.urandom(12)
                ciphertext = aesgcm.encrypt(nonce, plaintext, None)

                # 保存：nonce + ciphertext
                data = {
                    'nonce': base64.b64encode(nonce).decode(),
                    'ciphertext': base64.b64encode(ciphertext).decode(),
                    'timestamp': datetime.now().isoformat(),
                    'version': '1.0'
                }

                with open(self.encrypted_file, 'w') as f:
                    json.dump(data, f, indent=2)

                os.chmod(self.encrypted_file, 0o600)

                print("✅ Cookie 已加密保存")
                return True
            else:
                # 降级方案：Base64 + 简单混淆
                import secrets
                salt = secrets.token_bytes(16)
                obfuscated = bytes([b ^ key[i % len(key)] ^ salt[i % len(salt)]
                                   for i, b in enumerate(plaintext)])

                data = {
                    'salt': base64.b64encode(salt).decode(),
                    'data': base64.b64encode(obfuscated).decode(),
                    'timestamp': datetime.now().isoformat()
                }

                with open(self.encrypted_file, 'w') as f:
                    json.dump(data, f, indent=2)

                os.chmod(self.encrypted_file, 0o600)
                print("✅ Cookie 已加密保存（降级模式）")
                return True

        except Exception as e:
            print(f"❌ 加密失败: {e}")
            return False

    def decrypt_cookies(self, password: str = None) -> Dict[str, Any]:
        """解密 Cookie 数据"""
        try:
            if not self.encrypted_file.exists():
                print("❌ 未找到加密的 Cookie 文件")
                return None

            with open(self.encrypted_file, 'r') as f:
                data = json.load(f)

            key = self._get_or_create_key(password)

            if CRYPTO_AVAILABLE:
                # AES-256-GCM 解密
                nonce = base64.b64decode(data['nonce'])
                ciphertext = base64.b64decode(data['ciphertext'])

                aesgcm = AESGCM(key)
                plaintext = aesgcm.decrypt(nonce, ciphertext, None)

                cookies = json.loads(plaintext.decode())

                print(f"✅ Cookie 解密成功（创建于 {data['timestamp']}）")
                return cookies
            else:
                # 降级方案
                salt = base64.b64decode(data['salt'])
                obfuscated = base64.b64decode(data['data'])

                plaintext = bytes([b ^ key[i % len(key)] ^ salt[i % len(salt)]
                                  for i, b in enumerate(obfuscated)])

                cookies = json.loads(plaintext.decode())
                print(f"✅ Cookie 解密成功（降级模式）")
                return cookies

        except Exception as e:
            print(f"❌ 解密失败: {e}")
            return None

    def import_from_json(self, json_file: str = None, password: str = None):
        """从 JSON 文件导入并加密 Cookie"""
        if json_file is None:
            json_file = self.cookies_file

        if not Path(json_file).exists():
            print(f"❌ Cookie 文件不存在: {json_file}")
            return False

        with open(json_file, 'r') as f:
            cookies = json.load(f)

        print(f"📦 导入 {len(cookies)} 个平台的 Cookie")

        # 加密
        if self.encrypt_cookies(cookies, password):
            # 删除原始文件
            os.remove(json_file)
            print("✅ 原始 Cookie 文件已删除")
            return True
        return False

    def export_to_json(self, output_file: str = None, password: str = None):
        """解密并导出 Cookie 到 JSON 文件"""
        cookies = self.decrypt_cookies(password)

        if cookies:
            if output_file is None:
                output_file = self.cookies_file

            with open(output_file, 'w') as f:
                json.dump(cookies, f, indent=2)

            os.chmod(output_file, 0o600)
            print(f"✅ Cookie 已导出到: {output_file}")
            return True
        return False

    def rotate_key(self, old_password: str = None, new_password: str = None):
        """轮换加密密钥"""
        print("🔄 开始轮换密钥...")

        # 解密旧数据
        cookies = self.decrypt_cookies(old_password)
        if not cookies:
            return False

        # 删除旧密钥
        if self.key_file.exists():
            os.remove(self.key_file)

        # 使用新密钥加密
        if self.encrypt_cookies(cookies, new_password):
            print("✅ 密钥轮换完成")
            return True
        return False

    def check_age(self) -> bool:
        """检查 Cookie 是否需要轮换"""
        if not self.encrypted_file.exists():
            return False

        with open(self.encrypted_file, 'r') as f:
            data = json.load(f)

        created = datetime.fromisoformat(data['timestamp'])
        age_days = (datetime.now() - created).days

        if age_days > 30:
            print(f"⚠️  Cookie 已使用 {age_days} 天，建议轮换")
            return True
        else:
            print(f"✅ Cookie 使用时间: {age_days} 天")
            return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Agent Reach Cookie 加密工具")
    parser.add_argument('action', choices=['encrypt', 'decrypt', 'import', 'export', 'rotate', 'check'],
                       help='操作类型')
    parser.add_argument('--file', help='Cookie 文件路径')
    parser.add_argument('--output', help='输出文件路径')
    parser.add_argument('--password', help='加密密码（可选，不提供则使用密钥文件）')

    args = parser.parse_args()

    encryptor = CookieEncryptor()

    if args.action == 'encrypt':
        # 从文件读取并加密
        if args.file:
            with open(args.file, 'r') as f:
                cookies = json.load(f)
            encryptor.encrypt_cookies(cookies, args.password)
        else:
            print("❌ 请提供 --file 参数")

    elif args.action == 'decrypt':
        cookies = encryptor.decrypt_cookies(args.password)
        if cookies:
            print(json.dumps(cookies, indent=2))

    elif args.action == 'import':
        encryptor.import_from_json(args.file, args.password)

    elif args.action == 'export':
        encryptor.export_to_json(args.output, args.password)

    elif args.action == 'rotate':
        old_pwd = args.password or getpass.getpass("旧密码（留空使用密钥文件）: ")
        new_pwd = getpass.getpass("新密码（留空使用新密钥文件）: ")
        encryptor.rotate_key(old_pwd or None, new_pwd or None)

    elif args.action == 'check':
        encryptor.check_age()


if __name__ == "__main__":
    if not CRYPTO_AVAILABLE:
        print("⚠️  警告: cryptography 库未安装，使用降级加密")
        print("   安装: pip install cryptography")
        print()

    main()
