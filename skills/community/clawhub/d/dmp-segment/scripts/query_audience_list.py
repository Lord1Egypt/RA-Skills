#!/usr/bin/env python3
"""
查询人群列表
功能：查询人群列表，支持按类型、状态、ID等条件筛选
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
    # 解析可选参数
    audience_type = None
    audience_status = None
    audience_ids = None
    current = 1
    page_size = 20
    
    # 简单的参数解析
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--type" and i + 1 < len(sys.argv):
            audience_type = int(sys.argv[i + 1])
            i += 2
        elif arg == "--status" and i + 1 < len(sys.argv):
            audience_status = int(sys.argv[i + 1])
            i += 2
        elif arg == "--ids" and i + 1 < len(sys.argv):
            audience_ids = json.loads(sys.argv[i + 1])
            i += 2
        elif arg == "--page" and i + 1 < len(sys.argv):
            current = int(sys.argv[i + 1])
            i += 2
        elif arg == "--size" and i + 1 < len(sys.argv):
            page_size = int(sys.argv[i + 1])
            i += 2
        elif arg == "--help":
            print("用法: python query_audience_list.py [选项]")
            print("\n选项:")
            print("  --type <类型>     人群类型: 1=上传, 2=组合, 3=规则, 4=拓展, 5=打通")
            print("  --status <状态>   人群状态: 0=失败, 1=成功, 2=等待中, 3=计算中")
            print("  --ids <JSON数组>  人群ID列表，如 '[100001,100002]'")
            print("  --page <页码>     页码，默认1")
            print("  --size <条数>     每页条数，默认20")
            print("\n示例:")
            print("  python query_audience_list.py")
            print("  python query_audience_list.py --type 2 --status 1")
            print("  python query_audience_list.py --ids '[100001,100002]'")
            sys.exit(0)
        else:
            i += 1
    
    # 构建请求体
    request_body = {
        "current": current,
        "pageSize": page_size
    }
    
    if audience_type is not None:
        request_body["audienceType"] = audience_type
    
    if audience_status is not None:
        request_body["audienceStatus"] = audience_status
    
    if audience_ids is not None:
        request_body["audienceIds"] = audience_ids
    
    # 调用API
    call_api("/audience/manage/list", request_body)

if __name__ == "__main__":
    main()
