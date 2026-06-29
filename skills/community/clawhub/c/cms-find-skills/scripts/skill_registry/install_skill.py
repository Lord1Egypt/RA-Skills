#!/usr/bin/env python3
"""
Skill 安装：中心化 API 代理版本
不再进行任何沙盒逃逸或者本地 API 调用，而是作为纯粹的客户端，向用户的中心服务发起指令。
"""

import argparse
import json
import os
import sys
import requests
import warnings

# 禁用 InsecureRequestWarning (防止环境没有正确证书)
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

# 您未来部署的真实的中心服务域名/接口
API_BASE = "https://aishuo.co"
CENTRAL_SERVICE_URL = f"{API_BASE}/api/skill/proxy/install"

def install_skill(user_id: str, code: str = None, url: str = None, force: bool = False, quiet: bool = False):
    if not user_id:
        return {
            "success": False, 
            "message": "未能从上下文中获取到 User ID，无法向中心服务发起请求"
        }

    payload = {
        "userId": user_id,
        "code": code,
        "force": force
    }
    
    try:
        # 发起跨外网的调用到中控中心
        resp = requests.post(CENTRAL_SERVICE_URL, json=payload, timeout=30)
        
        # 假设中心服务端会中转网关插件执行完毕后的结果
        result = resp.json()
        if result.get("success"):
            # 追加提示给 AI，使其能够知道需要重新加载技能
            result["ai_instruction"] = "技能已成功安装或更新。为了使最新技能立刻生效，请 AI 立即读取此技能的最新配置并加载（例如重新查看该技能的 SKILL.md）。"
        return result
    except Exception as e:
        return {"success": False, "message": f"呼叫中控服务 API 失败: {str(e)}"}

def main():
    parser = argparse.ArgumentParser(description="Skill 安装（星型架构中心化 API 版）")
    parser.add_argument("--code", "-c", required=True, help="Skill code")
    parser.add_argument("--target", "-t", help="安装目标目录(已废弃，由服务端接管)")
    parser.add_argument("--force", "-f", action="store_true", help="强制覆盖")
    parser.add_argument("--quiet", "-q", action="store_true", help="静默模式")
    parser.add_argument("--user-id", required=True, help="用户的 User ID（必填，用于向中心服务发指令）")
    args = parser.parse_args()

    result = install_skill(args.user_id, args.code, None, args.force, args.quiet)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result.get("success"):
        sys.exit(1)

if __name__ == "__main__":
    main()
