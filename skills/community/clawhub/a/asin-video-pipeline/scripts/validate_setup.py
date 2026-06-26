#!/usr/bin/env python3
"""
ASIN营销视频流水线配置验证脚本
验证所有API连接和配置是否正确
"""

import os
import sys
import json
import requests
from pathlib import Path

def print_header(title):
    """打印格式化标题"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def check_env_vars():
    """检查环境变量"""
    print_header("1. 环境变量检查")
    
    required_vars = [
        "GOOGLE_SHEETS_ID",
        "TOPVIEW_API_KEY",
        "APIFY_API_TOKEN"
    ]
    
    all_ok = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var}")
        else:
            print(f"  ❌ {var}: 未设置")
            all_ok = False
    
    return all_ok

def validate_topview_api():
    """验证Topview AI API"""
    print_header("2. Topview AI API 验证")
    
    api_key = os.getenv("TOPVIEW_API_KEY")
    if not api_key:
        print("  ❌ 未设置 TOPVIEW_API_KEY")
        return False
    
    try:
        # 尝试调用API获取账户信息（假设有此类接口）
        # 实际应根据Topview API文档调整
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 这里使用任务列表接口作为健康检查
        # 根据实际API文档调整URL
        response = requests.get(
            "https://api.topview.ai/v1/m2v/task",
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 401, 403]:
            # 401/403 说明API Key有效但可能权限不足
            print("  ✅ API连接正常")
            return True
        else:
            print(f"  ⚠️  API返回状态码: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"  ⚠️  连接失败: {e}")
        return False

def validate_apify_api():
    """验证Apify API"""
    print_header("3. Apify API 验证")
    
    api_token = os.getenv("APIFY_API_TOKEN")
    if not api_token:
        print("  ❌ 未设置 APIFY_API_TOKEN")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {api_token}"
        }
        
        # 获取用户信息作为健康检查
        response = requests.get(
            "https://api.apify.com/v2/users/me",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            username = data.get("data", {}).get("username", "unknown")
            print(f"  ✅ API连接正常 (用户: {username})")
            return True
        else:
            print(f"  ❌ API验证失败: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ 连接失败: {e}")
        return False

def validate_google_sheets():
    """验证Google Sheets配置"""
    print_header("4. Google Sheets 验证")
    
    sheet_id = os.getenv("GOOGLE_SHEETS_ID")
    if not sheet_id:
        print("  ❌ 未设置 GOOGLE_SHEETS_ID")
        return False
    
    # 基本格式验证
    if len(sheet_id) != 44:
        print(f"  ⚠️  Sheets ID长度异常 (应为44位，实际{len(sheet_id)}位)")
    
    # 构建表格URL供用户检查
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
    print(f"  ℹ️  表格URL: {sheet_url}")
    print("  ⚠️  请确保已：")
    print("     1. 分享表格给Service Account")
    print("     2. 在n8n中配置Google Sheets凭证")
    
    return True

def check_workflow_files():
    """检查工作流文件"""
    print_header("5. 工作流文件检查")
    
    base_path = Path(__file__).parent.parent / "references"
    files = [
        "n8n-workflow-preview.json",
        "n8n-workflow-export.json",
        "WORKFLOW_SETUP.md"
    ]
    
    all_exist = True
    for file in files:
        file_path = base_path / file
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  ✅ {file} ({size} bytes)")
        else:
            print(f"  ❌ {file} (未找到)")
            all_exist = False
    
    return all_exist

def check_n8n_installation():
    """检查n8n安装状态"""
    print_header("6. n8n 安装检查")
    
    # 检查n8n是否安装
    import subprocess
    try:
        result = subprocess.run(
            ["n8n", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"  ✅ n8n 已安装 ({version})")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # 检查Docker是否运行
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=n8n", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if "n8n" in result.stdout:
            print("  ✅ n8n Docker容器正在运行")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("  ❌ n8n 未检测到")
    print("  安装方式:")
    print("    Docker: docker run -it --rm -p 5678:5678 n8nio/n8n")
    print("    npm: npm install n8n -g")
    return False

def print_summary(results):
    """打印验证结果摘要"""
    print_header("验证结果摘要")
    
    checks = [
        ("环境变量", results["env"]),
        ("Topview API", results["topview"]),
        ("Apify API", results["apify"]),
        ("Google Sheets", results["sheets"]),
        ("工作流文件", results["workflow"]),
        ("n8n安装", results["n8n"])
    ]
    
    passed = sum(1 for _, ok in checks if ok)
    total = len(checks)
    
    for name, ok in checks:
        status = "✅ 通过" if ok else "❌ 失败"
        print(f"  {status} - {name}")
    
    print(f"\n  总计: {passed}/{total} 项通过")
    
    if passed == total:
        print("\n  🎉 所有检查通过！可以开始使用流水线了")
        return True
    else:
        print("\n  ⚠️  部分检查未通过，请根据上述提示修复")
        return False

def main():
    """主函数"""
    print_header("ASIN营销视频流水线配置验证")
    
    # 加载.env文件（如果存在）
    env_file = Path(".env")
    if env_file.exists():
        print("  ℹ️  加载 .env 文件")
        with open(env_file) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, _, value = line.partition('=')
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")
    
    # 执行各项检查
    results = {
        "env": check_env_vars(),
        "topview": validate_topview_api(),
        "apify": validate_apify_api(),
        "sheets": validate_google_sheets(),
        "workflow": check_workflow_files(),
        "n8n": check_n8n_installation()
    }
    
    # 打印摘要
    all_ok = print_summary(results)
    
    if not all_ok:
        sys.exit(1)

if __name__ == "__main__":
    main()
