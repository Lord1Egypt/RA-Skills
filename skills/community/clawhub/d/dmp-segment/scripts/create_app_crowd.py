#!/usr/bin/env python3
"""
创建APP规则人群
功能：基于APP安装/活跃数据，圈选使用特定应用的用户
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
        
        # 输出API调用结果
        print(result.stdout)
        
        # 如果API调用成功（返回码为0），执行第七步检查
        if result.returncode == 0:
            try:
                # 尝试解析API返回结果，提取任务ID
                api_result = json.loads(result.stdout)
                task_id = None
                task_name = request_body.get("name")
                
                # 从API返回中提取任务ID
                if isinstance(api_result, dict):
                    if "data" in api_result and isinstance(api_result["data"], dict):
                        task_id = api_result["data"].get("audienceId")
                
                # 调用任务记录检查模块
                check_script = Path(__file__).parent / "check_task_logger.py"
                if check_script.exists():
                    subprocess.run(
                        ["python3", str(check_script), str(task_id) if task_id else "", task_name or ""],
                        check=False
                    )
            except:
                # 如果解析失败，仍然输出基本提示
                check_script = Path(__file__).parent / "check_task_logger.py"
                if check_script.exists():
                    subprocess.run(["python3", str(check_script)], check=False)
        
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


def validate_params(name, track_type, id_types, data):
    """
    参数格式校验（严格按照API文档要求）
    
    Returns:
        tuple: (is_valid, error_message)
    """
    # 1. 人群名称格式校验
    if not name or not isinstance(name, str):
        return False, "人群名称不能为空"
    
    # 2. 平台类型格式校验（APP规则只支持MOBILE）
    if track_type != "MOBILE":
        return False, "APP规则人群的trackType只能是MOBILE"
    
    # 3. ID类型格式校验
    if not isinstance(id_types, list) or len(id_types) == 0:
        return False, "idTypes必须是非空数组"
    
    # 校验ID类型枚举值（MOBILE）
    valid_mobile_ids = ["MD5_IDFA", "MD5_IMEI", "MD5_OAID", "IDFA", "OAID", "CAID", "MD5_CAID"]
    for id_type in id_types:
        if id_type not in valid_mobile_ids:
            return False, f"idTypes只能包含: {', '.join(valid_mobile_ids)}"
    
    # 4. APP规则格式校验
    if not isinstance(data, dict):
        return False, "data必须是对象"
    
    # dimension字段校验
    if "dimension" not in data:
        return False, "data必须包含dimension字段"
    
    if data["dimension"] != "APP":
        return False, "data.dimension必须是APP"
    
    # type字段校验（0=活跃,1=安装）
    if "type" not in data:
        return False, "data必须包含type字段"
    
    if data["type"] not in [0, 1]:
        return False, "data.type必须是 0(活跃)/1(安装) 之一"
    
    # packageNames字段校验（至少4个不重复）
    if "packageNames" not in data:
        return False, "data必须包含packageNames字段"
    
    if not isinstance(data["packageNames"], list):
        return False, "data.packageNames必须是数组"
    
    if len(data["packageNames"]) < 4:
        return False, "data.packageNames至少需要4个不重复的包名"
    
    # 检查是否有重复
    if len(data["packageNames"]) != len(set(data["packageNames"])):
        return False, "data.packageNames不能包含重复的包名"
    
    return True, ""

def main():
    if len(sys.argv) != 5:
        print("[PARAM_ERROR] 缺少必需参数")
        print("用法: python create_app_crowd.py <name> <trackType> <idTypes_JSON> <data_JSON>")
        print("\n参数说明:")
        print("  name: 人群名称")
        print("  trackType: 平台类型（只能是MOBILE）")
        print("  idTypes_JSON: ID类型列表（JSON数组）")
        print("  data_JSON: APP规则（JSON对象）")
        print("\n注意:")
        print("  - data.dimension必须是APP")
        print("  - data.type: 0=活跃,1=安装")
        print("  - data.packageNames至少需要4个不重复的包名")
        print("  - 单个app覆盖不能超总量70%")
        sys.exit(1)
    
    # 解析参数
    name = sys.argv[1]
    track_type = sys.argv[2]
    
    try:
        id_types = json.loads(sys.argv[3])
        data = json.loads(sys.argv[4])
    except json.JSONDecodeError as e:
        print(f"[PARAM_ERROR] JSON格式错误: {str(e)}")
        sys.exit(1)
    
    # 格式校验
    is_valid, error_msg = validate_params(name, track_type, id_types, data)
    if not is_valid:
        print(f"[PARAM_ERROR] 参数格式错误: {error_msg}")
        sys.exit(1)
    
    # 构建请求体
    request_body = {
        "name": name,
        "trackType": track_type,
        "idTypes": id_types,
        "data": data
    }
    
    # 调用API
    call_api("/audience/rule/create/app", request_body)

if __name__ == "__main__":
    main()
