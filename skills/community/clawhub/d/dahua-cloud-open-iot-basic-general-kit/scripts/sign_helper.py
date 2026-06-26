#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大华云开发者平台API签名工具

该脚本提供了生成大华云API签名的方法，支持授权API和业务API的签名生成。
"""

import hmac
import hashlib
import time
import uuid
import json
from typing import Dict, Optional


class DahuaAPISigner:
    """大华云API签名工具类"""
    
    def __init__(self, access_key: str, secret_access_key: str, product_id: str):
        """
        初始化签名工具
        
        Args:
            access_key: 产品的AccessKey
            secret_access_key: 产品的SecretAccessKey
            product_id: 产品ID
        """
        self.access_key = access_key
        self.secret_access_key = secret_access_key
        self.product_id = product_id
    
    def generate_nonce(self) -> str:
        """生成随机数（Nonce）"""
        return str(uuid.uuid4()).replace('-', '')
    
    def generate_trace_id(self) -> str:
        """生成链路跟踪ID"""
        return f"tid-{int(time.time() * 1000)}"
    
    def generate_timestamp(self) -> str:
        """生成13位标准时间戳"""
        return str(int(time.time() * 1000))
    
    def sign_for_auth_api(self) -> Dict[str, str]:
        """
        生成授权API（获取AppAccessToken）的请求头
        
        签名算法：
        strAuthFactor = AccessKey + Timestamp + Nonce
        sign = HMAC-SHA512(strAuthFactor, secretAccessKey).toUpperCase()
        
        Returns:
            包含所有必需请求头的字典
        """
        timestamp = self.generate_timestamp()
        nonce = self.generate_nonce()
        
        # 拼接签名字符串
        str_auth_factor = self.access_key + timestamp + nonce
        
        # 生成签名
        sign = hmac.new(
            self.secret_access_key.encode('utf-8'),
            str_auth_factor.encode('utf-8'),
            hashlib.sha512
        ).hexdigest().upper()
        
        return {
            'Content-Type': 'application/json',
            'Accept-Language': 'zh-CN',
            'Version': 'v1',
            'AccessKey': self.access_key,
            'Timestamp': timestamp,
            'Nonce': nonce,
            'Sign': sign,
            'X-TraceId-Header': self.generate_trace_id(),
            'ProductID': self.product_id
        }
    
    def sign_for_business_api(self, app_access_token: str, sign_type: str = 'simple') -> Dict[str, str]:
        """
        生成业务API的请求头
        
        签名算法：
        strAuthFactor = AccessKey + AppAccessToken + Timestamp + Nonce
        sign = HMAC-SHA512(strAuthFactor, secretAccessKey).toUpperCase()
        
        Args:
            app_access_token: 应用访问令牌
            sign_type: 签名类型，'simple'表示简化签名模式
            
        Returns:
            包含所有必需请求头的字典
        """
        timestamp = self.generate_timestamp()
        nonce = self.generate_nonce()
        
        # 拼接签名字符串
        str_auth_factor = self.access_key + app_access_token + timestamp + nonce
        
        # 生成签名
        sign = hmac.new(
            self.secret_access_key.encode('utf-8'),
            str_auth_factor.encode('utf-8'),
            hashlib.sha512
        ).hexdigest().upper()
        
        headers = {
            'Content-Type': 'application/json',
            'Accept-Language': 'zh-CN',
            'Version': 'v1',
            'AccessKey': self.access_key,
            'AppAccessToken': app_access_token,
            'Timestamp': timestamp,
            'Nonce': nonce,
            'Sign': sign,
            'X-TraceId-Header': self.generate_trace_id(),
            'ProductID': self.product_id
        }
        
        # 如果使用简化签名模式，添加Sign-Type头
        if sign_type == 'simple':
            headers['Sign-Type'] = 'simple'
        
        return headers
    
    def print_auth_headers(self):
        """打印授权API请求头（用于调试）"""
        headers = self.sign_for_auth_api()
        print("授权API请求头：")
        print(json.dumps(headers, indent=2, ensure_ascii=False))
    
    def print_business_headers(self, app_access_token: str):
        """打印业务API请求头（用于调试）"""
        headers = self.sign_for_business_api(app_access_token)
        print("业务API请求头：")
        print(json.dumps(headers, indent=2, ensure_ascii=False))


def main():
    """示例用法"""
    # 示例配置（请替换为实际的AccessKey、SecretAccessKey和ProductID）
    ACCESS_KEY = "your_access_key"
    SECRET_ACCESS_KEY = "your_secret_access_key"
    PRODUCT_ID = "your_product_id"
    
    # 创建签名工具实例
    signer = DahuaAPISigner(ACCESS_KEY, SECRET_ACCESS_KEY, PRODUCT_ID)
    
    # 示例1：生成授权API请求头
    print("=" * 60)
    print("示例1：授权API请求头")
    print("=" * 60)
    auth_headers = signer.sign_for_auth_api()
    print(json.dumps(auth_headers, indent=2, ensure_ascii=False))
    
    # 示例2：生成业务API请求头
    print("\n" + "=" * 60)
    print("示例2：业务API请求头")
    print("=" * 60)
    # 假设已经获取到了AppAccessToken
    APP_ACCESS_TOKEN = "your_app_access_token"
    business_headers = signer.sign_for_business_api(APP_ACCESS_TOKEN)
    print(json.dumps(business_headers, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
