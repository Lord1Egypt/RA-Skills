#!/usr/bin/env python3
"""
DeepSeek 余额查询脚本
用法: python3 query_deepseek_balance.py
说明: 查询 DeepSeek 账户余额
⚠️ 警告: 凭证从 Base64 编码文件读取，请勿泄露
"""

import os
import base64
import requests
import json

# DeepSeek API Key 路径（Base64编码文件）
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".deepseek_key.env")

def load_credentials():
    """从 Base64 编码文件读取 DeepSeek API Key"""
    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(f"凭证文件不存在: {CREDENTIALS_FILE}")
    
    with open(CREDENTIALS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("DEEPSEEK_API_KEY_B64="):
                b64_key = line.split("=", 1)[1].strip()
                return base64.b64decode(b64_key).decode('utf-8')
    
    raise ValueError("未找到 DeepSeek API Key")

def query_balance():
    """查询 DeepSeek 账户余额"""
    api_key = load_credentials()
    
    url = "https://api.deepseek.com/user/balance"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    resp = requests.get(url, headers=headers)
    
    if resp.status_code != 200:
        raise Exception(f"API调用失败: {resp.text}")
    
    return resp.json()

def main():
    """主函数"""
    try:
        result = query_balance()
        
        print("=" * 50)
        print("🔮 DeepSeek 账户余额查询")
        print("=" * 50)
        
        for info in result.get("balance_infos", []):
            currency = info.get("currency", "CNY")
            total = info.get("total_balance", "0")
            granted = info.get("granted_balance", "0")
            topped = info.get("topped_up_balance", "0")
            
            print(f"货币: {currency}")
            print(f"总余额: {total} 元")
            print(f"赠送余额: {granted} 元")
            print(f"充值余额: {topped} 元")
        
        print("=" * 50)
        
    except FileNotFoundError as e:
        print(f"❌ 错误: {e}")
    except Exception as e:
        print(f"❌ 查询失败: {e}")

if __name__ == "__main__":
    main()
