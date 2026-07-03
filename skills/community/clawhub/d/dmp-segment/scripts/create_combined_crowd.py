#!/usr/bin/env python3
"""
创建组合人群
功能：基于DMP标签体系，通过交并差逻辑组合多个标签条件圈选人群
"""

import sys
import json
import subprocess
from pathlib import Path

def find_auth_skill_path():
    """查找鉴权技能的API脚本路径"""
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
        
        sys.exit(result.returncode)
    except subprocess.TimeoutExpired:
        print(json.dumps({"error": "TIMEOUT", "message": "API调用超时"}, ensure_ascii=False))
        sys.exit(6)
    except Exception as e:
        print(json.dumps({"error": "CALL_ERROR", "message": f"调用鉴权技能失败: {str(e)}"}, ensure_ascii=False))
        sys.exit(6)

def validate_params(name, track_type, id_types, data):
    """参数格式校验（严格按照API实际要求）"""
    if not name or not isinstance(name, str):
        return False, "人群名称不能为空"
    
    valid_track_types = ["MOBILE", "PC", "OTT"]
    if track_type not in valid_track_types:
        return False, f"trackType必须是 {'/'.join(valid_track_types)} 之一"
    
    if not isinstance(id_types, list) or len(id_types) == 0:
        return False, "idTypes必须是非空数组"
    
    valid_mobile_ids = ["MD5_IDFA", "MD5_IMEI", "MD5_OAID", "IDFA", "OAID", "CAID", "MD5_CAID"]
    valid_ott_ids = ["MD5_MAC"]
    valid_pc_ids = ["MZID"]
    
    valid_ids = valid_mobile_ids if track_type == "MOBILE" else (valid_ott_ids if track_type == "OTT" else valid_pc_ids)
    
    for id_type in id_types:
        if id_type not in valid_ids:
            return False, f"trackType={track_type}时，idTypes只能包含: {', '.join(valid_ids)}"
    
    if not isinstance(data, list) or len(data) == 0:
        return False, "data必须是非空数组"
    
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            return False, f"data[{idx}]必须是对象"
        
        if "op" not in item:
            return False, f"data[{idx}]必须包含op字段（and/not/noop）"
        
        valid_ops = ["and", "not", "noop"]
        if item["op"] not in valid_ops:
            return False, f"data[{idx}].op必须是 {'/'.join(valid_ops)} 之一"
        
        if "rule" not in item:
            return False, f"data[{idx}]必须包含rule字段"
        
        if not isinstance(item["rule"], dict):
            return False, f"data[{idx}].rule必须是对象(不是数组)"
        
        if "tag" not in item["rule"] and "audience" not in item["rule"]:
            return False, f"data[{idx}].rule必须包含tag或audience字段"
        
        if "tag" in item["rule"]:
            if not isinstance(item["rule"]["tag"], list):
                return False, f"data[{idx}].rule.tag必须是数组"
            for tag_idx, tag_id in enumerate(item["rule"]["tag"]):
                if not isinstance(tag_id, int):
                    return False, f"data[{idx}].rule.tag[{tag_idx}]必须是整数"
        
        if "audience" in item["rule"]:
            if not isinstance(item["rule"]["audience"], list):
                return False, f"data[{idx}].rule.audience必须是数组"
            for aud_idx, aud_id in enumerate(item["rule"]["audience"]):
                if not isinstance(aud_id, int):
                    return False, f"data[{idx}].rule.audience[{aud_idx}]必须是整数"
    
    if data[-1]["op"] != "noop":
        return False, "data数组的最后一个元素的op字段必须是'noop'"
    
    for idx in range(len(data) - 1):
        if data[idx]["op"] not in ["and", "not"]:
            return False, f"data[{idx}].op必须是'and'或'not'（只有最后一个元素可以是'noop'）"
    
    return True, ""

def main():
    if len(sys.argv) != 5:
        print("[PARAM_ERROR] 缺少必需参数")
        print("用法: python create_combined_crowd.py <name> <trackType> <idTypes_JSON> <data_JSON>")
        sys.exit(1)
    
    name = sys.argv[1]
    track_type = sys.argv[2]
    
    try:
        id_types = json.loads(sys.argv[3])
        data = json.loads(sys.argv[4])
    except json.JSONDecodeError as e:
        print(f"[PARAM_ERROR] JSON格式错误: {str(e)}")
        sys.exit(1)
    
    is_valid, error_msg = validate_params(name, track_type, id_types, data)
    if not is_valid:
        print(f"[PARAM_ERROR] 参数格式错误: {error_msg}")
        sys.exit(1)
    
    request_body = {
        "name": name,
        "trackType": track_type,
        "idTypes": id_types,
        "data": data
    }
    
    call_api("/audience/manage/combine/create", request_body)

if __name__ == "__main__":
    main()
