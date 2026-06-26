#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大华云设备密码加密工具

该脚本提供了设备密码的加密方法，支持两种加密方式：
1. Base64加密方式
2. AES256加密方式
"""

import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from typing import Optional


class DeviceCodeEncryptor:
    """设备密码加密工具类"""
    
    # AES加密的固定IV值
    IV = b'86E2DB6D77B5E9CD'
    
    # 默认密钥（当设备序列号为空时使用）
    DEFAULT_KEY = "DEFAULT_KEY"
    
    def __init__(self, secret_access_key: str, device_id: Optional[str] = None):
        """
        初始化加密工具
        
        Args:
            secret_access_key: 产品的SecretAccessKey
            device_id: 设备序列号（可选）
        """
        self.secret_access_key = secret_access_key
        self.device_id = device_id
    
    @staticmethod
    def base64_encode(text: str) -> str:
        """
        Base64编码
        
        Args:
            text: 待编码的文本
            
        Returns:
            Base64编码后的字符串
        """
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')
    
    def _generate_aes_key(self) -> bytes:
        """
        生成AES密钥
        
        算法：Cut32(UpperCase(MD5-32位(UpperCase(sk))))
        
        Returns:
            32字节的AES密钥
        """
        # 如果设备序列号为空，使用默认密钥
        key_source = self.secret_access_key if self.device_id else self.DEFAULT_KEY
        
        # 计算MD5-32位
        md5_hash = hashlib.md5(key_source.upper().encode('utf-8')).hexdigest().upper()
        
        # 截取前32位
        aes_key = md5_hash[:32]
        
        return aes_key.encode('utf-8')
    
    def encrypt_base64(self, device_password: str) -> str:
        """
        方式一：Base64加密设备密码
        
        格式："Dolynk_" + Base64(设备密码)
        
        Args:
            device_password: 设备密码（明文）
            
        Returns:
            加密后的设备密码
        """
        encoded = self.base64_encode(device_password)
        return f"Dolynk_{encoded}"
    
    def encrypt_aes256(self, device_password: str) -> str:
        """
        方式二：AES256加密设备密码
        
        格式：Base64(Aes256(待加密内容, AesKey, IV初始向量))
        加密算法：Aes256/CBC/PKCS7
        
        Args:
            device_password: 设备密码（明文）
            
        Returns:
            加密后的设备密码（Base64编码）
        """
        # 生成AES密钥
        aes_key = self._generate_aes_key()
        
        # 创建AES加密器（CBC模式）
        cipher = AES.new(aes_key, AES.MODE_CBC, self.IV)
        
        # PKCS7填充并加密
        encrypted = cipher.encrypt(pad(device_password.encode('utf-8'), AES.block_size))
        
        # Base64编码
        encoded = base64.b64encode(encrypted).decode('utf-8')
        
        return encoded
    
    def encrypt_device_code(self, device_password: str, method: str = 'aes256') -> str:
        """
        加密设备密码
        
        Args:
            device_password: 设备密码（明文）
            method: 加密方式，'base64' 或 'aes256'，默认 'aes256'
            
        Returns:
            加密后的设备密码
            
        Raises:
            ValueError: 如果加密方式不支持
        """
        if method == 'base64':
            return self.encrypt_base64(device_password)
        elif method == 'aes256':
            return self.encrypt_aes256(device_password)
        else:
            raise ValueError(f"不支持的加密方式: {method}. 请使用 'base64' 或 'aes256'")


def main():
    """示例用法"""
    # 示例配置
    SECRET_ACCESS_KEY = "your_secret_access_key"
    DEVICE_ID = "your_device_id"
    DEVICE_PASSWORD = "admin123"
    
    # 创建加密工具实例
    encryptor = DeviceCodeEncryptor(SECRET_ACCESS_KEY, DEVICE_ID)
    
    print("=" * 60)
    print("设备密码加密示例")
    print("=" * 60)
    print(f"原始密码: {DEVICE_PASSWORD}")
    
    # 方式一：Base64加密
    print("\n方式一：Base64加密")
    encrypted_base64 = encryptor.encrypt_base64(DEVICE_PASSWORD)
    print(f"加密结果: {encrypted_base64}")
    
    # 方式二：AES256加密
    print("\n方式二：AES256加密")
    encrypted_aes256 = encryptor.encrypt_aes256(DEVICE_PASSWORD)
    print(f"加密结果: {encrypted_aes256}")
    
    # 使用encrypt_device_code方法（推荐）
    print("\n使用encrypt_device_code方法（推荐）")
    encrypted = encryptor.encrypt_device_code(DEVICE_PASSWORD, method='aes256')
    print(f"加密结果: {encrypted}")


if __name__ == "__main__":
    main()
