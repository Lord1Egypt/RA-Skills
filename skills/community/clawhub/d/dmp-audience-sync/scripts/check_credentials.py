#!/usr/bin/env python3
"""
凭证检查模块
功能：检查鉴权技能是否已安装，以及API凭证是否已配置
"""

import os
import json
from pathlib import Path

def check_auth_skill_installed():
    """
    检查鉴权技能是否已安装
    
    Returns:
        bool: True表示已安装，False表示未安装
    """
    auth_skill_paths = [
        Path.home() / ".skills" / "mingdata-dmp-auth",
        Path.home() / ".openclaw" / "workspace" / "skills" / "mingdata-dmp-auth",
        Path.home() / ".openclaw" / "skills" / "mingdata-dmp-auth",
        Path("/tmp/.mingdata-dmp-auth")
    ]
    return any(path.exists() for path in auth_skill_paths)

def check_credentials_configured():
    """
    检查API凭证是否已配置
    
    Returns:
        bool: True表示已配置，False表示未配置
    """
    credentials_path = Path.home() / ".mingdata_dmp_credentials"
    
    if not credentials_path.exists():
        return False
    
    try:
        with open(credentials_path, 'r') as f:
            credentials = json.load(f)
            return "access_key" in credentials and "secret_key" in credentials
    except:
        return False

def print_step2_check_result():
    """
    输出第二步凭证检查的结果
    """
    auth_installed = check_auth_skill_installed()
    credentials_configured = check_credentials_configured()
    
    print("\n" + "="*70)
    print("📌 【第二步：鉴权技能检查与凭证配置】")
    print("="*70)
    
    if not auth_installed:
        print("⚠️  检测到鉴权技能未安装")
        print()
        print("该技能负责管理 API 凭证（AK/SK）、生成签名，是使用本功能的必要前提。")
        print()
        print("AI助手必须执行以下操作:")
        print("   1. 向用户询问是否需要安装鉴权技能")
        print("   2. 展示技能功能说明")
        print("   3. 等待用户明确回复(是/否)")
        print("   4. 用户确认后执行安装命令: openclaw skills install mingdata-dmp-auth")
        print()
        print("🔴 如果用户拒绝安装，必须终止流程")
        print("="*70 + "\n")
        return
    
    print("✅ 鉴权技能已安装")
    print()
    
    if not credentials_configured:
        print("⚠️  检测到API凭证未配置")
        print()
        print("AI助手必须执行以下操作:")
        print("   1. 向用户展示凭证获取指引")
        print("   2. 引导用户申请API凭证")
        print("   3. 等待用户提供凭证后保存配置")
        print()
        print("📧 凭证申请方式（二选一）：")
        print("   方式一：邮件申请 - product@mingdata.com")
        print("   方式二：在线表单 - https://doc.weixin.qq.com/forms/ANEAJwfLAAoADMAHwbhAPICNUE0vDRd8f#/fill")
        print()
        print("🔴 凭证配置完成后才能继续执行")
    else:
        print("✅ API凭证已配置")
        print()
        print("可以继续执行后续步骤")
    
    print("="*70 + "\n")

if __name__ == "__main__":
    print_step2_check_result()
