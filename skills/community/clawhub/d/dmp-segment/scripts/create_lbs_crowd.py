#!/usr/bin/env python3
"""
创建LBS规则人群
功能：基于地理位置数据，圈选到访过特定区域的用户
"""

import sys
import json
from datetime import datetime
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
    
    # 2. 平台类型格式校验（LBS只支持MOBILE）
    if track_type != "MOBILE":
        return False, "LBS人群的trackType只能是MOBILE"
    
    # 3. ID类型格式校验
    if not isinstance(id_types, list) or len(id_types) == 0:
        return False, "idTypes必须是非空数组"
    
    # 校验ID类型枚举值（MOBILE）
    valid_mobile_ids = ["MD5_IDFA", "MD5_IMEI", "MD5_OAID", "IDFA", "OAID", "CAID", "MD5_CAID"]
    for id_type in id_types:
        if id_type not in valid_mobile_ids:
            return False, f"idTypes只能包含: {', '.join(valid_mobile_ids)}"
    
    # 4. LBS规则格式校验（必须是数组）
    if not isinstance(data, list) or len(data) == 0:
        return False, "data必须是非空数组"
    
    # 校验每个LBS规则的结构
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            return False, f"data[{idx}]必须是对象"
        
        # drawMode枚举校验
        if "drawMode" not in item:
            return False, f"data[{idx}]必须包含drawMode字段"
        
        if item["drawMode"] not in ["batch", "manual"]:
            return False, f"data[{idx}].drawMode必须是 batch(圆形)/manual(多边形) 之一"
        
        # dataOrigin校验
        if "dataOrigin" not in item:
            return False, f"data[{idx}]必须包含dataOrigin字段"
        
        valid_origins = ["recentArrive", "homeAddress", "workAddress"]
        origins = item["dataOrigin"].split(",")
        for origin in origins:
            if origin not in valid_origins:
                return False, f"data[{idx}].dataOrigin只能包含: {', '.join(valid_origins)}（逗号分隔）"
        
        # 如果选择recentArrive，必须有时间范围
        if "recentArrive" in item["dataOrigin"]:
            if "startTime" not in item or "endTime" not in item:
                return False, f"data[{idx}]选择recentArrive时必须包含startTime和endTime"
            
            # 时间格式校验 YYYY-MM-DD HH
            try:
                datetime.strptime(item["startTime"], "%Y-%m-%d %H")
                datetime.strptime(item["endTime"], "%Y-%m-%d %H")
            except ValueError:
                return False, f"data[{idx}]的startTime/endTime格式必须是 YYYY-MM-DD HH"
        
        # 圆形模式校验
        if item["drawMode"] == "batch":
            if "center" not in item:
                return False, f"data[{idx}]圆形模式必须包含center字段"
            
            center = item["center"]
            if not isinstance(center, dict):
                return False, f"data[{idx}].center必须是对象"
            
            if "lng" not in center or "lat" not in center or "radius" not in center:
                return False, f"data[{idx}].center必须包含lng、lat、radius字段"
            
            # radius范围校验（150-6000米）
            try:
                radius = int(center["radius"])
                if radius < 150 or radius > 6000:
                    return False, f"data[{idx}].center.radius必须在150-6000米之间"
            except (ValueError, TypeError):
                return False, f"data[{idx}].center.radius必须是整数"
        
        # 多边形模式校验
        elif item["drawMode"] == "manual":
            if "points" not in item:
                return False, f"data[{idx}]多边形模式必须包含points字段"
            
            points = item["points"]
            if not isinstance(points, list) or len(points) < 3:
                return False, f"data[{idx}].points必须是至少3个点的数组"
            
            for p_idx, point in enumerate(points):
                if not isinstance(point, dict):
                    return False, f"data[{idx}].points[{p_idx}]必须是对象"
                
                if "lng" not in point or "lat" not in point:
                    return False, f"data[{idx}].points[{p_idx}]必须包含lng和lat字段"
    
    return True, ""

def main():
    if len(sys.argv) != 5:
        print("[PARAM_ERROR] 缺少必需参数")
        print("用法: python create_lbs_crowd.py <name> <trackType> <idTypes_JSON> <data_JSON>")
        print("\n参数说明:")
        print("  name: 人群名称")
        print("  trackType: 平台类型（只能是MOBILE）")
        print("  idTypes_JSON: ID类型列表（JSON数组）")
        print("  data_JSON: LBS规则（JSON数组，包含坐标/时间）")
        print("\n注意:")
        print("  - 坐标系统必须使用百度坐标系（BD09）")
        print("  - 圆形模式radius范围: 150-6000米")
        print("  - 选择recentArrive时时间跨度需<90天")
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
    call_api("/audience/rule/create/lbs", request_body)

if __name__ == "__main__":
    main()
