#!/usr/bin/env python3
"""
获取广告账户列表
功能：查询指定广告平台的可用广告账户
"""

import sys
import json
import subprocess
from pathlib import Path

# 平台映射表
PLATFORM_MAP = {
    "oceanengine": 1,    # 字节DMP
    "tencent": 2,        # 腾讯DMP
    "alipay": 3,         # 支付宝DMP
    "bilibili": 4,       # B站DMP
    "xiaohongshu": 5     # 小红书灵犀
}

def find_auth_skill_path():
    """查找鉴权技能的API脚本路径"""
    # 第一层：固定路径列表
    possible_paths = [
        Path.home() / ".openclaw" / "workspace" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        Path.home() / ".openclaw" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        Path.home() / ".skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        Path.home() / ".skills" / "9126" / "scripts" / "minri_dmp_api.py",
    ]
    for path in possible_paths:
        if path.exists():
            return path
    # 第二层：动态扫描
    scan_dirs = [
        Path.home() / ".skills",
        Path.home() / ".openclaw" / "workspace" / "skills",
        Path.home() / ".openclaw" / "skills",
    ]
    for scan_dir in scan_dirs:
        if scan_dir.exists():
            for skill_dir in scan_dir.iterdir():
                if skill_dir.is_dir():
                    candidate = skill_dir / "scripts" / "minri_dmp_api.py"
                    if candidate.exists():
                        try:
                            with open(candidate, 'r', encoding='utf-8') as f:
                                content = f.read(500)
                                if "明日DMP" in content or "mingdata" in content.lower():
                                    return candidate
                        except:
                            continue
    return None

def call_api(endpoint, request_body, method="GET"):
    """调用鉴权技能的统一API模块"""
    auth_skill_path = find_auth_skill_path()
    
    if not auth_skill_path:
        print(json.dumps({
            "error": "AUTH_SKILL_NOT_FOUND",
            "message": "未找到鉴权技能，请先安装mingdata-dmp-auth技能"
        }, ensure_ascii=False))
        sys.exit(3)
    
    try:
        result = subprocess.run(
            ["python3", str(auth_skill_path), method, endpoint, json.dumps(request_body, ensure_ascii=False)],
            capture_output=True,
            text=True,
            timeout=30
        )
        print(result.stdout)
        sys.exit(result.returncode)
    except subprocess.TimeoutExpired:
        print(json.dumps({"error": "TIMEOUT", "message": "API调用超时"}, ensure_ascii=False))
        sys.exit(6)
    except Exception as e:
        print(json.dumps({"error": "CALL_ERROR", "message": f"调用鉴权技能失败: {str(e)}"}, ensure_ascii=False))
        sys.exit(6)

def main():
    if len(sys.argv) != 2:
        print("[PARAM_ERROR] 缺少必需参数")
        print("用法: python get_ad_accounts.py <platform>")
        print("支持的平台: oceanengine, tencent, alipay, bilibili, xiaohongshu")
        sys.exit(1)
    
    platform = sys.argv[1]
    
    if platform not in PLATFORM_MAP:
        print(f"[PARAM_ERROR] 不支持的平台: {platform}")
        print(f"支持的平台: {', '.join(PLATFORM_MAP.keys())}")
        sys.exit(1)
    
    # 转换为平台编码
    platform_code = PLATFORM_MAP[platform]
    
    # 调用API（修复：移除 /api/open-api 前缀）
    call_api("/audience/sync/task/advertiser/list", {
        "mediaPlatform": platform_code
    }, method="GET")

if __name__ == "__main__":
    main()
