#!/usr/bin/env python3
"""
查询标签列表
功能：查询DMP标签列表，支持按标签类型筛选
"""

import sys
import json
import subprocess
from pathlib import Path

def find_auth_skill_path():
    """
    查找鉴权技能的API脚本路径
    
    设计原则：
    1. 只查找标准安装路径 ~/.skills/mingdata-dmp-auth/
    2. 不依赖任何平台特定的路径（如workspace）
    3. 确保技能在任何环境中都能正常工作
    
    Returns:
        Path: 鉴权技能的minri_dmp_api.py路径，如果未找到则返回None
    """
    # 标准安装路径（唯一正确的查找位置）
    possible_paths = [
        Path.home() / ".skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        Path.home() / ".openclaw" / "workspace" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        Path.home() / ".openclaw" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        Path.cwd() / ".skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
    ]
    for path in possible_paths:
        if path.exists():
            return path
    # 动态扫描
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

def call_api(endpoint, request_body, method="POST"):
    """
    调用鉴权技能的统一API模块
    
    Args:
        endpoint: API路径
        request_body: 请求体（dict）
        method: HTTP方法（GET或POST）
    
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
    
    # 调用鉴权技能的API脚本（新格式：包含method参数）
    try:
        result = subprocess.run(
            ["python3", str(auth_skill_path), method, endpoint, json.dumps(request_body)],
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
    # 解析可选参数
    tag_type = None
    
    # 简单的参数解析
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--type" and i + 1 < len(sys.argv):
            tag_type = int(sys.argv[i + 1])
            i += 2
        elif arg == "--help":
            print("用法: python query_tag_list.py [选项]")
            print("\n选项:")
            print("  --type <类型>  标签类型: 1=明略标签, 3=合作伙伴标签")
            print("\n示例:")
            print("  python query_tag_list.py")
            print("  python query_tag_list.py --type 1")
            sys.exit(0)
        else:
            i += 1
    
    # 构建请求体
    request_body = {}
    
    if tag_type is not None:
        request_body["tagType"] = tag_type
    
    # 调用API（使用GET方法）
    call_api("/tag/list", request_body, method="GET")

if __name__ == "__main__":
    main()
