#!/usr/bin/env python3
"""
明日DMP API凭证配置脚本
功能：保存Access Key和Secret Key到本地配置文件
"""

import sys
import json
import os
from pathlib import Path

def main():
    if len(sys.argv) != 3:
        print("[ERROR] 缺少必需参数")
        print("用法: python setup_credentials.py <ACCESS_KEY> <SECRET_KEY>")
        sys.exit(1)
    
    access_key = sys.argv[1]
    secret_key = sys.argv[2]
    
    # 验证凭证格式
    if not access_key or not secret_key:
        print("[ERROR] 凭证不能为空")
        sys.exit(1)
    
    # 保存凭证到文件
    credentials_file = Path.home() / ".MINGRI_DMP_CREDENTIALS"
    credentials = {
        "access_key": access_key,
        "secret_key": secret_key
    }
    
    try:
        with open(credentials_file, 'w', encoding='utf-8') as f:
            json.dump(credentials, f, indent=2)
        
        # 设置文件权限为600（仅当前用户可读写）
        os.chmod(credentials_file, 0o600)
        
        print(f"[SUCCESS] 凭证已保存到 {credentials_file}")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] 保存凭证失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
