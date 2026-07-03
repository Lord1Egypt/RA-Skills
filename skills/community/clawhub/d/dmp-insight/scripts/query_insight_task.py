#!/usr/bin/env python3
"""
查询人群洞察任务状态（改进版）
增加状态码映射和结构化输出，避免状态误判
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path

# 状态码映射表（根据明日DMP官方文档）
STATUS_MAP = {
    0: {
        "name": "失败",
        "display": "❌ 失败",
        "can_get_result": False,
        "description": "任务计算失败"
    },
    1: {
        "name": "成功",
        "display": "✅ 已完成",
        "can_get_result": True,
        "description": "任务计算成功完成"
    },
    2: {
        "name": "等待中",
        "display": "🟡 等待中",
        "can_get_result": False,
        "description": "任务等待处理"
    },
    3: {
        "name": "计算中",
        "display": "🔵 计算中",
        "can_get_result": False,
        "description": "任务正在计算处理"
    }
}

def get_next_action(status_code):
    """根据状态码提供下一步操作建议"""
    if status_code == 1:
        return "✅ 可以获取洞察结果了！使用命令：获取洞察任务 {task_id} 的结果"
    elif status_code == 2:
        return "⏳ 任务正在等待处理，请继续等待（通常 < 1分钟）"
    elif status_code == 3:
        return "⏳ 任务正在计算中，建议5-10分钟后重新查询（通常需要5-30分钟）"
    elif status_code == 0:
        return "❌ 任务失败，请检查错误信息或重新创建任务"
    else:
        return "❓ 未知状态，请联系技术支持"

def format_task_status(task_data):
    """格式化任务状态为结构化输出"""
    status_code = task_data.get("status")
    status_info = STATUS_MAP.get(status_code, {
        "name": "未知",
        "display": "❓ 未知状态",
        "can_get_result": False,
        "description": "未知的状态码"
    })
    
    # 构建结构化输出
    output = {
        "success": True,
        "task_info": {
            "任务ID": task_data.get("id"),
            "任务名称": task_data.get("name"),
            "人群ID": task_data.get("audienceId"),
            "人群名称": task_data.get("audienceName"),
            "洞察类型": "明略洞察" if task_data.get("type") == 0 else "合作伙伴洞察",
            "创建时间": task_data.get("createdAt"),
            "创建者": task_data.get("createdBy")
        },
        "status_info": {
            "状态码": status_code,
            "状态名称": status_info["name"],
            "状态显示": status_info["display"],
            "状态说明": status_info["description"],
            "可获取结果": "是" if status_info["can_get_result"] else "否"
        },
        "next_action": get_next_action(status_code).format(task_id=task_data.get("id"))
    }
    
    return output

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

def call_api(task_id):
    """
    调用鉴权技能查询洞察任务状态
    
    Args:
        task_id: 任务ID
    """
    # 动态查找鉴权技能的API脚本路径
    auth_skill_path = find_auth_skill_path()
    
    if not auth_skill_path:
        print(json.dumps({
            "success": False,
            "error": "AUTH_SKILL_NOT_FOUND",
            "message": "未找到鉴权技能，请先安装mingdata-dmp-auth技能"
        }, ensure_ascii=False, indent=2))
        sys.exit(3)
    
    # 调用鉴权技能的API脚本
    try:
        result = subprocess.run(
            [
                "python3", 
                str(auth_skill_path), 
                "POST", 
                "/audience/insight/list",
                json.dumps({"taskIds": [int(task_id)]})
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # 解析API返回结果
        try:
            api_response = json.loads(result.stdout)
            
            # 检查API调用是否成功
            if api_response.get("code") == "0" and api_response.get("data"):
                task_list = api_response.get("data", [])
                if task_list and len(task_list) > 0:
                    task_data = task_list[0]
                    # 格式化并输出结构化状态信息
                    formatted_output = format_task_status(task_data)
                    print(json.dumps(formatted_output, ensure_ascii=False, indent=2))
                    sys.exit(0)
                else:
                    print(json.dumps({
                        "success": False,
                        "error": "TASK_NOT_FOUND",
                        "message": f"未找到任务ID {task_id} 的信息"
                    }, ensure_ascii=False, indent=2))
                    sys.exit(1)
            else:
                # API返回错误
                print(json.dumps({
                    "success": False,
                    "error": "API_ERROR",
                    "message": api_response.get("msg", "API调用失败"),
                    "raw_response": api_response
                }, ensure_ascii=False, indent=2))
                sys.exit(1)
                
        except json.JSONDecodeError:
            # 无法解析API返回
            print(json.dumps({
                "success": False,
                "error": "PARSE_ERROR",
                "message": "无法解析API返回结果",
                "raw_output": result.stdout
            }, ensure_ascii=False, indent=2))
            sys.exit(1)
        
    except subprocess.TimeoutExpired:
        print(json.dumps({
            "success": False,
            "error": "TIMEOUT",
            "message": "API调用超时"
        }, ensure_ascii=False, indent=2))
        sys.exit(6)
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": "CALL_ERROR",
            "message": f"调用鉴权技能失败: {str(e)}"
        }, ensure_ascii=False, indent=2))
        sys.exit(6)

def main():
    parser = argparse.ArgumentParser(description='查询人群洞察任务状态（改进版）')
    parser.add_argument('task_id', help='洞察任务ID')
    
    args = parser.parse_args()
    
    # 调用API
    call_api(args.task_id)

if __name__ == "__main__":
    main()
