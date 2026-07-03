#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
明日DMP人群投放技能 - 查询RTQ投放订单
"""

import json
import os
import sys
import subprocess

# query_rtq_deal.py 不需要读取凭证，所有API调用通过鉴权技能完成

def query_rtq_deal(deal_id):
    """
    查询RTQ投放订单详情
    
    参数:
        deal_id: 订单ID
    """
    
    print("=" * 60)
    print("查询RTQ投放订单")
    print("=" * 60)
    
    # 构建请求参数
    params = {
        "dealId": deal_id
    }
    
    print(f"\n查询订单ID: {deal_id}\n")
    
    # 查找鉴权技能路径
    auth_skill_path = None
    possible_paths = [
        os.path.expanduser("~/.skills/9126/scripts/minri_dmp_api.py"),
        "/data/dm-agent-outputs/workspace/.skills/9126/scripts/minri_dmp_api.py"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            auth_skill_path = path
            break
    
    if not auth_skill_path:
        print("❌ 错误：未找到鉴权技能")
        print("请确保已安装 mingdata-dmp-auth 技能 (skill_id: 9126)")
        sys.exit(1)
    
    # 调用鉴权技能的API模块
    try:
        result = subprocess.run(
            ["python3", auth_skill_path, "POST", "/rtq/deal/query", 
             json.dumps(params, ensure_ascii=False)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        response = json.loads(result.stdout)
        
        if response.get('code') == '0' or response.get('code') == 0:
            print("=" * 60)
            print("✅ 查询成功")
            print("=" * 60)
            
            data = response.get('data', {})
            print(f"\n订单详情:")
            print(json.dumps(data, ensure_ascii=False, indent=2))
            
            return data
        else:
            print("=" * 60)
            print("❌ 查询失败")
            print("=" * 60)
            print(f"错误代码: {response.get('code')}")
            print(f"错误信息: {response.get('msg')}")
            sys.exit(1)
            
    except subprocess.TimeoutExpired:
        print("❌ 请求超时")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='查询RTQ投放订单')
    parser.add_argument('--deal-id', required=True, help='订单ID')
    
    args = parser.parse_args()
    
    query_rtq_deal(deal_id=args.deal_id)
