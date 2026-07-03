#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
明日DMP人群投放技能 - 凭证配置脚本
用于配置API访问凭证和RTQ投放凭证
"""

import json
import os
import sys

def setup_credentials():
    """配置明日DMP API凭证和RTQ投放凭证"""
    
    print("=" * 60)
    print("明日DMP人群投放 - 凭证配置")
    print("=" * 60)
    print()
    
    # 获取凭证保存路径
    workspace_dir = os.path.expanduser("~/workspace")
    credentials_file = os.path.join(workspace_dir, ".mingdata_credentials")
    
    # 检查是否已有凭证
    if os.path.exists(credentials_file):
        print("⚠️  检测到已有凭证配置")
        choice = input("是否覆盖现有配置？(y/n): ").strip().lower()
        if choice != 'y':
            print("已取消配置")
            return
    
    print("\n请输入以下凭证信息：")
    print("-" * 60)
    
    # 收集API凭证
    print("\n📌 API访问凭证（通过商务获取）：")
    access_key = input("Access Key: ").strip()
    secret_key = input("Secret Key: ").strip()
    
    # 收集RTQ凭证
    print("\n📌 RTQ投放凭证（通过商务获取）：")
    rtq_cluster = input("RTQ机房名称（如：明日RTQ机房）: ").strip()
    rtq_access_key = input("RTQ Access Key: ").strip()
    
    # 验证必填项
    if not all([access_key, secret_key, rtq_cluster, rtq_access_key]):
        print("\n❌ 错误：所有凭证信息都是必填项！")
        sys.exit(1)
    
    # 保存凭证
    credentials = {
        "access_key": access_key,
        "secret_key": secret_key,
        "rtq_cluster": rtq_cluster,
        "rtq_access_key": rtq_access_key
    }
    
    try:
        os.makedirs(workspace_dir, exist_ok=True)
        with open(credentials_file, 'w', encoding='utf-8') as f:
            json.dump(credentials, f, ensure_ascii=False, indent=2)
        
        # 设置文件权限
        os.chmod(credentials_file, 0o600)
        
        print("\n" + "=" * 60)
        print("✅ 凭证配置成功！")
        print("=" * 60)
        print(f"凭证已保存到: {credentials_file}")
        print("\n配置内容：")
        print(f"  - API Access Key: {access_key[:8]}...")
        print(f"  - RTQ机房: {rtq_cluster}")
        print(f"  - RTQ Access Key: {rtq_access_key[:8]}...")
        print("\n现在可以开始创建投放订单了！")
        
    except Exception as e:
        print(f"\n❌ 保存凭证失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_credentials()
