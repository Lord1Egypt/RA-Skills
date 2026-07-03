#!/usr/bin/env python3
"""
创建人群洞察任务
支持明略洞察和合作伙伴洞察两种类型
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path

def find_auth_skill_path():
    """
    动态查找鉴权技能的API脚本路径
    
    Returns:
        Path: 鉴权技能的minri_dmp_api.py路径，如果未找到则返回None
    """
    # 第一层：固定路径列表（按优先级排序）
    possible_paths = [
        # 标准安装路径
        Path.home() / ".skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        # OpenClaw workspace路径
        Path.home() / ".openclaw" / "workspace" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        # OpenClaw skills路径
        Path.home() / ".openclaw" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        # workspace中的路径（skill_id 8863）
        Path.cwd() / ".skills" / "8863" / "scripts" / "minri_dmp_api.py",
        # workspace中的路径（按名称）
        Path.cwd() / ".skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
    ]
    
    # 检查固定路径
    for path in possible_paths:
        if path.exists():
            return path
    
    # 第二层：动态扫描所有可能的目录
    scan_dirs = [
        Path.home() / ".skills",
        Path.home() / ".openclaw" / "workspace" / "skills",
        Path.home() / ".openclaw" / "skills",
        Path.cwd() / ".skills",
    ]
    for scan_dir in scan_dirs:
        if scan_dir.exists():
            for skill_dir in scan_dir.iterdir():
                if skill_dir.is_dir():
                    auth_path = skill_dir / "scripts" / "minri_dmp_api.py"
                    if auth_path.exists():
                        try:
                            with open(auth_path, 'r', encoding='utf-8') as f:
                                content = f.read(500)
                                if "明日DMP" in content or "mingdata" in content.lower():
                                    return auth_path
                        except:
                            continue
    
    return None

def call_api(endpoint, request_body):
    """
    调用鉴权技能的统一API模块
    
    Args:
        endpoint: API路径
        request_body: 请求体（dict）
    
    Returns:
        通过subprocess调用鉴权技能的minri_dmp_api.py
    """
    # 动态查找鉴权技能的API脚本路径
    auth_skill_path = find_auth_skill_path()
    
    if not auth_skill_path:
        print(json.dumps({
            "error": "AUTH_SKILL_NOT_FOUND",
            "message": "未找到鉴权技能，请先安装mingdata-dmp-auth技能"
        }, ensure_ascii=False))
        sys.exit(3)
    
    # 调用鉴权技能的API脚本
    try:
        result = subprocess.run(
            ["python3", str(auth_skill_path), "POST", endpoint, json.dumps(request_body)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # 输出结果
        print(result.stdout)
        
        # 传递退出码
        sys.exit(result.returncode)
        
    except subprocess.TimeoutExpired:
        print(json.dumps({
            "error": "TIMEOUT",
            "message": "API调用超时"
        }, ensure_ascii=False))
        sys.exit(6)
    except Exception as e:
        print(json.dumps({
            "error": "CALL_ERROR",
            "message": f"调用鉴权技能失败: {str(e)}"
        }, ensure_ascii=False))
        sys.exit(6)


def main():
    parser = argparse.ArgumentParser(description='创建人群洞察任务')
    parser.add_argument('--name', required=True, help='洞察任务名称')
    parser.add_argument('--audience-id', required=True, help='人群ID')
    parser.add_argument('--insight-type', required=True, type=int, choices=[0, 1], 
                       help='洞察类型：0=明略洞察，1=合作伙伴洞察')
    parser.add_argument('--dimensions', required=True, help='洞察维度，逗号分隔')
    
    args = parser.parse_args()
    
    # 构建请求体
    request_body = {
        "name": args.name,
        "audienceId": args.audience_id,
        "insightType": args.insight_type,
        "insightCondition": args.dimensions.split(',')
    }
    
    # 调用API（正确的endpoint路径，不包含/api/open-api前缀）
    call_api("/audience/insight/add", request_body)

if __name__ == "__main__":
    main()
