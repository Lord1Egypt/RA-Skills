#!/usr/bin/env python3
"""
查询人群同步任务
功能：查询人群同步任务的执行状态和详细信息
"""

import sys
import json
import subprocess
from pathlib import Path

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
        sys.exit(result.returncode)
    except subprocess.TimeoutExpired:
        print(json.dumps({"error": "TIMEOUT", "message": "API调用超时"}, ensure_ascii=False))
        sys.exit(6)
    except Exception as e:
        print(json.dumps({"error": "CALL_ERROR", "message": f"调用鉴权技能失败: {str(e)}"}, ensure_ascii=False))
        sys.exit(6)

def parse_args(args):
    """解析命令行参数"""
    params = {
        "current": 1,
        "pageSize": 20
    }
    
    i = 0
    while i < len(args):
        arg = args[i]
        
        if arg.startswith("--"):
            # 长选项参数
            if arg == "--status" and i + 1 < len(args):
                params["status"] = int(args[i + 1])
                i += 2
            elif arg == "--start-date" and i + 1 < len(args):
                params["startDate"] = args[i + 1]
                i += 2
            elif arg == "--end-date" and i + 1 < len(args):
                params["endDate"] = args[i + 1]
                i += 2
            elif arg == "--current" and i + 1 < len(args):
                params["current"] = int(args[i + 1])
                i += 2
            elif arg == "--page-size" and i + 1 < len(args):
                params["pageSize"] = int(args[i + 1])
                i += 2
            else:
                i += 1
        else:
            # 任务ID参数（支持逗号分隔的多个ID）
            task_ids = arg.split(",")
            params["ids"] = [int(id.strip()) for id in task_ids]
            i += 1
    
    return params

def main():
    if len(sys.argv) < 2:
        print("[PARAM_ERROR] 缺少必需参数")
        print("用法示例：")
        print("  查询单个任务: python query_sync_task.py 100260")
        print("  查询多个任务: python query_sync_task.py 100260,100261,100262")
        print("  查询指定状态: python query_sync_task.py --status 1")
        print("  查询时间范围: python query_sync_task.py --start-date 2025-01-01 --end-date 2025-12-31")
        print("  分页查询: python query_sync_task.py --current 2 --page-size 10")
        print("")
        print("状态说明：0=失败，1=成功，2=等待中，3=计算中")
        sys.exit(1)
    
    # 解析参数
    params = parse_args(sys.argv[1:])
    
    # 调用API（修复：移除 /api/open-api 前缀）
    call_api("/audience/sync/task/list", params)

if __name__ == "__main__":
    main()
