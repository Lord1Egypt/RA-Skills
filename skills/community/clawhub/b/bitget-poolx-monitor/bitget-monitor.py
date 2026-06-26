#!/usr/bin/env python3
"""
Bitget PoolX Monitor - 使用 r.jina.ai 绕过 Cloudflare
"""
import requests
import time

def check_poolx():
    """检查 Bitget PoolX 状态"""
    url = "https://r.jina.ai/https://www.bitget.com/events/poolx"
    
    try:
        resp = requests.get(url, timeout=30)
        content = resp.text
        
        print("=== Bitget PoolX 状态 ===")
        
        if "Ongoing" in content:
            print("✅ 有进行中的项目!")
            
            # 提取池子信息
            lines = content.split('\n')
            for line in lines:
                if "ETH" in line and "Pool" in line:
                    print(f"  - ETH Pool: {line.strip()[:100]}")
                if "BTC" in line and "Pool" in line:
                    print(f"  - BTC Pool: {line.strip()[:100]}")
                    
            return "HAS_POOLS"
        elif "Upcoming" in content and "0" in content:
            print("❌ 当前没有项目")
            return "NO_POOLS"
        else:
            print("⚠️ 状态未知")
            return "UNKNOWN"
            
    except Exception as e:
        print(f"错误: {e}")
        return "ERROR"

if __name__ == "__main__":
    result = check_poolx()
    print(f"\n结果: {result}")
