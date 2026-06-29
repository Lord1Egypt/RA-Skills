#!/usr/bin/env python3
"""
创建人群同步任务
功能：将DMP人群包同步到指定广告平台的广告账户
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

def call_api(endpoint, request_body):
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
            ["python3", str(auth_skill_path), "POST", endpoint, json.dumps(request_body, ensure_ascii=False)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(result.stdout)
        
        if result.returncode == 0:
            print("\n" + "="*60)
            print("⚠️ 【第八步：任务记录检查】- 必须执行")
            print("="*60)
            print("请检查skill-logger技能是否已安装：")
            print("1. 已安装 → 自动记录任务")
            print("2. 未安装 → 询问用户是否需要安装")
            print("="*60 + "\n")
        
        sys.exit(result.returncode)
    except subprocess.TimeoutExpired:
        print(json.dumps({"error": "TIMEOUT", "message": "API调用超时"}, ensure_ascii=False))
        sys.exit(6)
    except Exception as e:
        print(json.dumps({"error": "CALL_ERROR", "message": f"调用鉴权技能失败: {str(e)}"}, ensure_ascii=False))
        sys.exit(6)

def validate_params(params):
    """参数格式校验"""
    required_fields = ["platform", "crowdId", "adAccountId"]
    
    for field in required_fields:
        if field not in params:
            return False, f"缺少必需参数: {field}"
    
    platform_code = PLATFORM_MAP.get(params["platform"])
    if not platform_code:
        return False, f"不支持的平台: {params['platform']}"
    
    # 字节DMP条件校验
    if platform_code == 1:
        if "isToBytedanceBrand" not in params:
            return False, "字节DMP必须提供isToBytedanceBrand参数"
    
    # 小红书条件校验
    if platform_code == 5:
        if "advertiserBrand" not in params:
            return False, "小红书必须提供advertiserBrand参数"
    
    return True, ""

def build_request_body(params):
    """构建符合接口文档的请求体"""
    platform_code = PLATFORM_MAP.get(params["platform"])
    
    request_body = {
        "mediaPlatform": platform_code,
        "advertiserId": params["adAccountId"],
        "audienceId": int(params["crowdId"])
    }
    
    # 字节DMP条件参数
    if platform_code == 1:
        request_body.update({
            "isToBytedanceBrand": params.get("isToBytedanceBrand", False),
            "bytedanceBrandVirtualAdvId": params.get("bytedanceBrandVirtualAdvId"),
            "bytedanceBrandName": params.get("bytedanceBrandName")
        })
    
    # 小红书条件参数
    if platform_code == 5:
        request_body["advertiserBrand"] = params.get("advertiserBrand")
    
    return request_body

def main():
    if len(sys.argv) != 2:
        print("[PARAM_ERROR] 缺少必需参数")
        print("用法: python create_sync_task.py <params_JSON>")
        sys.exit(1)
    
    try:
        params = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"[PARAM_ERROR] JSON格式错误: {str(e)}")
        sys.exit(1)
    
    is_valid, error_msg = validate_params(params)
    if not is_valid:
        print(f"[PARAM_ERROR] 参数格式错误: {error_msg}")
        sys.exit(1)
    
    request_body = build_request_body(params)
    # 调用API（修复：移除 /api/open-api 前缀）
    call_api("/audience/sync/task/create", request_body)

if __name__ == "__main__":
    main()
