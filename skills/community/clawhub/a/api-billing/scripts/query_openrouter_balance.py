#!/usr/bin/env python3
"""
OpenRouter 余额查询脚本
用法: python3 query_openrouter_balance.py
说明: 查询 OpenRouter 账户余额
⚠️ 警告: 凭证从 Base64 编码文件读取，请勿泄露
"""

import os
import base64
import requests

# OpenRouter API Key 路径（Base64编码文件）
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".openrouter_key.env")

def load_credentials():
    """从 Base64 编码文件读取 OpenRouter API Key"""
    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(f"凭证文件不存在: {CREDENTIALS_FILE}")
    
    with open(CREDENTIALS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("OPENROUTER_API_KEY_B64="):
                b64_key = line.split("=", 1)[1].strip()
                return base64.b64decode(b64_key).decode('utf-8')
    
    raise ValueError("未找到 OpenRouter API Key")

def query_balance():
    """查询 OpenRouter 账户余额"""
    api_key = load_credentials()
    
    url = "https://openrouter.ai/api/v1/credits"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    resp = requests.get(url, headers=headers)
    
    if resp.status_code != 200:
        raise Exception(f"API调用失败: {resp.text}")
    
    return resp.json()["data"]

def main():
    """主函数"""
    try:
        result = query_balance()
        
        total = float(result.get("total_credits", 0))
        usage = float(result.get("total_usage", 0))
        remaining = total - usage
        
        print("=" * 50)
        print("🌐 OpenRouter 账户余额查询")
        print("=" * 50)
        print(f"总额度: ${total:.2f}")
        print(f"已使用: ${usage:.2f}")
        print(f"剩余: ${remaining:.2f}")
        print("=" * 50)
        
    except FileNotFoundError as e:
        print(f"❌ 错误: {e}")
    except Exception as e:
        print(f"❌ 查询失败: {e}")

if __name__ == "__main__":
    main()
