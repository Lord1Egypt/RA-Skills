#!/usr/bin/env python3
"""
ASIN营销视频流水线初始化脚本
用于快速配置和验证n8n + Topview AI + Apify + Google Sheets集成
"""

import os
import sys
import json
import re
from pathlib import Path

def print_header(title):
    """打印格式化标题"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def check_env_vars():
    """检查必要的环境变量"""
    print_header("检查环境变量")
    
    required_vars = [
        "GOOGLE_SHEETS_ID",
        "TOPVIEW_API_KEY",
        "APIFY_API_TOKEN"
    ]
    
    missing = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            masked = value[:4] + "..." + value[-4:] if len(value) > 8 else "***"
            print(f"  ✅ {var}: {masked}")
        else:
            print(f"  ❌ {var}: 未设置")
            missing.append(var)
    
    if missing:
        print(f"\n  ⚠️  缺少 {len(missing)} 个环境变量")
        print("  请设置以下环境变量后重试：")
        for var in missing:
            print(f"    - {var}")
        return False
    
    print("\n  ✅ 所有环境变量已设置")
    return True

def validate_sheet_id(sheet_id):
    """验证Google Sheets ID格式"""
    # Sheets ID 通常是44个字符的字符串
    pattern = r'^[a-zA-Z0-9_-]{44}$'
    return bool(re.match(pattern, sheet_id))

def validate_api_key(key, name):
    """验证API Key基本格式"""
    if not key or len(key) < 10:
        return False, f"{name} 太短或为空"
    return True, "OK"

def create_env_template():
    """创建.env模板文件"""
    print_header("创建环境变量模板")
    
    env_content = """# ASIN营销视频流水线配置
# 复制此文件为 .env 并填入实际值

# Google Sheets
GOOGLE_SHEETS_ID=your_spreadsheet_id_here

# Topview AI
TOPVIEW_API_KEY=your_topview_api_key_here

# Apify
APIFY_API_TOKEN=your_apify_token_here

# n8n (可选)
N8N_PORT=5678
N8N_PROTOCOL=http
N8N_HOST=localhost
"""
    
    env_file = Path(".env.template")
    if not env_file.exists():
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(env_content)
        print("  ✅ 已创建 .env.template")
        print("  请复制为 .env 并填入实际值")
    else:
        print("  ℹ️  .env.template 已存在")

def print_setup_guide():
    """打印设置指南"""
    print_header("快速开始指南")
    print("""
1. 环境准备:
   - 确保已安装 n8n (docker/npm)
   - 确保已安装 Python 3.8+

2. 服务注册:
   - Topview AI: https://www.topview.ai
   - Apify: https://apify.com
   - Google Cloud: https://console.cloud.google.com

3. 配置步骤:
   a) 复制 .env.template 为 .env
   b) 填入所有API密钥和ID
   c) 运行: python scripts/validate_setup.py
   d) 导入n8n工作流文件
   e) 配置n8n凭证

4. 工作流文件位置:
   - references/n8n-workflow-preview.json (预览版)
   - references/n8n-workflow-export.json (正式版)

详细文档: references/WORKFLOW_SETUP.md
""")

def main():
    """主函数"""
    print_header("ASIN营销视频流水线初始化")
    
    # 检查环境变量
    env_ok = check_env_vars()
    
    # 创建模板
    create_env_template()
    
    # 打印指南
    print_setup_guide()
    
    if not env_ok:
        print("\n  ⚠️  请先配置环境变量再运行工作流")
        sys.exit(1)
    else:
        print("\n  ✅ 初始化完成！可以导入n8n工作流了")
        print("  详细配置请参考: references/WORKFLOW_SETUP.md")

if __name__ == "__main__":
    main()
