#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
- 使用 Fernet 对称加密保护所有 COS 敏感配置
- 包括 SecretId、SecretKey、桶名、Region 等
- 加密密钥存储在独立文件中，配置文件与密钥文件分离
"""

import os
import json
from cryptography.fernet import Fernet

# ==================== 基础配置 ====================

# 脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 配置文件路径
CONFIG_DIR = os.path.join(SCRIPT_DIR, "conf")
ENCRYPTED_CONFIG_FILE = os.path.join(CONFIG_DIR, "cos_secret.enc")
ENCRYPTION_KEY_FILE = os.path.join(CONFIG_DIR, ".encryption_key")

# ==================== OpenClaw 配置 ====================

# OpenClaw 图片缓存目录
OPENCLAW_MEDIA_DIR = "/root/.openclaw/media/inbound"

# ==================== 存储类型选项 ====================

# 支持的 COS 存储类型
STORAGE_CLASS_OPTIONS = {
    "1": ("STANDARD", "标准存储（访问频繁，成本较高）"),
    "2": ("STANDARD_IA", "低频存储（访问较少，成本较低，推荐）"),
    "3": ("ARCHIVE", "归档存储（极少访问，成本最低，取回需等待）"),
}

# 默认存储类型
DEFAULT_STORAGE_CLASS = "STANDARD_IA"

# ==================== 加密配置管理 ====================


def _ensure_config_dir():
    """确保配置目录存在"""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, mode=0o700, exist_ok=True)


def _generate_encryption_key():
    """生成加密密钥并保存到文件"""
    _ensure_config_dir()
    key = Fernet.generate_key()
    with open(ENCRYPTION_KEY_FILE, 'wb') as f:
        f.write(key)
    # 设置文件权限为仅所有者可读写
    os.chmod(ENCRYPTION_KEY_FILE, 0o600)
    return key


def _load_encryption_key():
    """加载加密密钥（密钥文件不存在时抛出异常，不自动生成）"""
    if not os.path.exists(ENCRYPTION_KEY_FILE):
        raise FileNotFoundError(
            f"加密密钥文件不存在: {ENCRYPTION_KEY_FILE}\n"
            f"请先运行 setup_config.py 初始化配置"
        )
    with open(ENCRYPTION_KEY_FILE, 'rb') as f:
        return f.read()


def save_cos_config(config_data):
    """
    加密并保存完整的 COS 配置到文件

    Args:
        config_data: dict，包含以下字段：
            - secret_id (str): 腾讯云 SecretId
            - secret_key (str): 腾讯云 SecretKey
            - bucket (str): COS 桶名称（如 baby-gallery-1301557826）
            - region (str): COS 区域（如 ap-guangzhou）
            - storage_class (str): 存储类型（如 STANDARD_IA）
            - use_internal (bool): 是否使用内网域名
    """
    _ensure_config_dir()
    # 保存时如果密钥文件不存在，则生成新密钥
    if not os.path.exists(ENCRYPTION_KEY_FILE):
        key = _generate_encryption_key()
    else:
        key = _load_encryption_key()
    fernet = Fernet(key)

    # 将配置信息序列化为 JSON
    config_json = json.dumps(config_data).encode('utf-8')

    # 加密
    encrypted_data = fernet.encrypt(config_json)

    # 写入加密配置文件
    with open(ENCRYPTED_CONFIG_FILE, 'wb') as f:
        f.write(encrypted_data)
    os.chmod(ENCRYPTED_CONFIG_FILE, 0o600)

    print("✅ COS 配置已加密保存")


def load_cos_config():
    """
    从加密配置文件中读取完整的 COS 配置

    Returns:
        dict: 包含所有 COS 配置信息的字典，字段包括：
            - secret_id (str): 腾讯云 SecretId
            - secret_key (str): 腾讯云 SecretKey
            - bucket (str): COS 桶名称
            - region (str): COS 区域
            - storage_class (str): 存储类型
            - use_internal (bool): 是否使用内网域名

    Raises:
        FileNotFoundError: 配置文件不存在
        Exception: 解密失败
    """
    if not os.path.exists(ENCRYPTED_CONFIG_FILE):
        raise FileNotFoundError(
            f"加密配置文件不存在: {ENCRYPTED_CONFIG_FILE}\n"
            f"请先运行 setup_config.py 初始化配置"
        )

    if not os.path.exists(ENCRYPTION_KEY_FILE):
        raise FileNotFoundError(
            f"加密密钥文件不存在: {ENCRYPTION_KEY_FILE}\n"
            f"请先运行 setup_config.py 初始化配置"
        )

    key = _load_encryption_key()
    fernet = Fernet(key)

    with open(ENCRYPTED_CONFIG_FILE, 'rb') as f:
        encrypted_data = f.read()

    # 解密
    decrypted_data = fernet.decrypt(encrypted_data)
    config_data = json.loads(decrypted_data.decode('utf-8'))

    # 兼容旧版配置（仅包含 secret_id 和 secret_key）
    if "bucket" not in config_data:
        raise ValueError(
            "配置文件格式过旧，缺少桶信息。\n"
            "请重新运行 setup_config.py 初始化配置"
        )

    return config_data


# ==================== 兼容旧接口（向后兼容） ====================


def load_cos_secret():
    """
    兼容旧接口：从加密配置中读取 SecretId 和 SecretKey

    Returns:
        tuple: (secret_id, secret_key)
    """
    config = load_cos_config()
    return config["secret_id"], config["secret_key"]
