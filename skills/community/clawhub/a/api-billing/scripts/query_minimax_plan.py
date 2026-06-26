#!/usr/bin/env python3
"""
MiniMax Coding Plan 用量查询脚本
用法: python3 query_minimax_plan.py
说明: 查询 MiniMax 订阅的剩余用量
⚠️ 警告: 凭证从 Base64 编码文件读取，请勿泄露
"""

import os
import base64
import requests

# MiniMax API Key 路径（Base64编码文件）
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "..", ".minimax_cp_key.env")

def load_credentials():
    """从 Base64 编码文件读取 MiniMax API Key"""
    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(f"凭证文件不存在: {CREDENTIALS_FILE}")
    
    with open(CREDENTIALS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("MINIMAX_CODING_PLAN_KEY_B64="):
                b64_key = line.split("=", 1)[1].strip()
                return base64.b64decode(b64_key).decode('utf-8')
    
    raise ValueError("未找到 MiniMax API Key")

def query_plan():
    """查询 Coding Plan 剩余用量"""
    api_key = load_credentials()
    
    url = "https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains?GroupId="
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    resp = requests.get(url, headers=headers)
    
    if resp.status_code != 200:
        raise Exception(f"API调用失败: {resp.text}")
    
    data = resp.json()
    return data.get("model_remains", [])

def main():
    """主函数"""
    try:
        models = query_plan()
        
        print("=" * 60)
        print("🎯 MiniMax Coding Plan 剩余用量查询")
        print("=" * 60)
        
        for model in models:
            name = model.get("model_name", "N/A")
            total = model.get("current_interval_total_count", 0)
            used = model.get("current_interval_usage_count", 0)
            remains = model.get("remains_time", 0)
            
            # 转换时间
            if "M*" in name:
                remains_min = remains / 60
                print(f"\n📦 {name}")
                print(f"   本周期总额度: {total} 分钟")
                print(f"   本周期已用: {used} 分钟")
                print(f"   剩余: {remains_min:.1f} 分钟")
            elif total > 0:
                print(f"\n📦 {name}")
                print(f"   本周期总额度: {total}")
                print(f"   本周期已用: {used}")
                print(f"   剩余: {remains}")
        
        print("\n" + "=" * 60)
        
    except FileNotFoundError as e:
        print(f"❌ 错误: {e}")
    except Exception as e:
        print(f"❌ 查询失败: {e}")

if __name__ == "__main__":
    main()
