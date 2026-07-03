#!/usr/bin/env python3
"""
创建广告行为规则人群
功能：基于广告监测数据，圈选在特定时间段内有曝光/点击行为的用户
"""

import sys
import json
from datetime import datetime
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

def validate_dimension_params(label, category_en, selected_keys):
    """
    校验维度参数的配对关系
    
    根据API文档的实际要求：
    - 活动维度（活动ID）：label="活动维度", category_en="CAMPAIGN_ID", selectedKeys=普通数字字符串
    - 活动维度（点位ID）：label="活动维度", category_en="SPOT_ID", selectedKeys=普通字符串
    - 地域维度：label="地域维度", 不需要category_en, selectedKeys=普通数字字符串
    - 行业维度：label="行业维度", category_en="INDUSTRY_L1", selectedKeys=24位格式
    - 媒体维度：label="媒体维度", category_en="MEDIA_STID", selectedKeys=24位格式
    """
    # 地域维度不需要category_en
    if label == "地域维度":
        if category_en is not None:
            return False, "地域维度不需要category_en字段"
        return True, ""
    
    # 其他维度必须有category_en
    if label in ["活动维度", "行业维度", "媒体维度"]:
        if category_en is None:
            return False, f"{label}必须提供category_en字段"
        
        # 校验category_en的值
        valid_category_map = {
            "活动维度": ["CAMPAIGN_ID", "SPOT_ID"],
            "行业维度": ["INDUSTRY_L1"],
            "媒体维度": ["MEDIA_STID"]
        }
        
        if category_en not in valid_category_map.get(label, []):
            return False, f"{label}的category_en必须是 {'/'.join(valid_category_map[label])} 之一"
        
        # 行业维度和媒体维度需要24位格式ID
        if label in ["行业维度", "媒体维度"]:
            for key in selected_keys:
                if not isinstance(key, str) or len(key) != 24:
                    return False, f"{label}的selectedKeys必须是24位格式的字符串（如'000000130000000000001950'）"
        
        return True, ""
    
    return False, f"不支持的label值: {label}"

def validate_params(name, track_type, start_date, end_date, id_types, data):
    """参数格式校验（严格按照API文档要求）"""
    if not name or not isinstance(name, str):
        return False, "人群名称不能为空"
    
    valid_track_types = ["MOBILE", "PC", "OTT"]
    if track_type not in valid_track_types:
        return False, f"trackType必须是 {'/'.join(valid_track_types)} 之一"
    
    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return False, "startDate和endDate格式必须是 YYYY-MM-DD"
    
    if (end_dt - start_dt).days > 62:
        return False, "时间跨度不能超过62天"
    
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
    
    # ⚠️ 重要限制：data只支持1组op+rule
    if len(data) > 1:
        return False, "data数组只支持1组op+rule（API实际限制）"
    
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            return False, f"data[{idx}]必须是对象"
        
        if "op" not in item or "rule" not in item:
            return False, f"data[{idx}]必须包含op和rule字段"
        
        if not isinstance(item["op"], list):
            return False, f"data[{idx}].op必须是数组"
        
        for op in item["op"]:
            if op not in ["and", "or"]:
                return False, f"data[{idx}].op只能包含 and/or"
        
        if not isinstance(item["rule"], list) or len(item["rule"]) == 0:
            return False, f"data[{idx}].rule必须是非空数组"
        
        # 只有1个rule时，op必须是空数组
        if len(item["rule"]) == 1 and len(item["op"]) != 0:
            return False, f"data[{idx}]只有1个rule时，op必须是空数组[]"
        
        # 多个rule时，op数量 = rule数量 - 1
        if len(item["rule"]) > 1 and len(item["op"]) != len(item["rule"]) - 1:
            return False, f"data[{idx}].op数量必须等于rule数量减1"
        
        for r_idx, rule in enumerate(item["rule"]):
            if not isinstance(rule, dict):
                return False, f"data[{idx}].rule[{r_idx}]必须是对象"
            
            if "label" in rule:
                valid_labels = ["活动维度", "行业维度", "地域维度", "媒体维度"]
                if rule["label"] not in valid_labels:
                    return False, f"data[{idx}].rule[{r_idx}].label必须是 {'/'.join(valid_labels)} 之一"
                
                # 校验维度参数配对
                is_valid, error_msg = validate_dimension_params(
                    rule["label"],
                    rule.get("category_en"),
                    rule.get("selectedKeys", [])
                )
                if not is_valid:
                    return False, f"data[{idx}].rule[{r_idx}]: {error_msg}"
            
            if "event_type" in rule:
                if rule["event_type"] not in ["imp", "clk"]:
                    return False, f"data[{idx}].rule[{r_idx}].event_type必须是 imp(曝光)/clk(点击) 之一"
            
            if "selectedKeys" in rule:
                if not isinstance(rule["selectedKeys"], list) or len(rule["selectedKeys"]) == 0:
                    return False, f"data[{idx}].rule[{r_idx}].selectedKeys必须是非空数组"
            
            if "frequency_min" in rule:
                if not isinstance(rule["frequency_min"], int) or rule["frequency_min"] < 1 or rule["frequency_min"] > 999:
                    return False, f"data[{idx}].rule[{r_idx}].frequency_min必须是1-999的整数"
            
            if "frequency_max" in rule:
                if not isinstance(rule["frequency_max"], int) or rule["frequency_max"] < 1 or rule["frequency_max"] > 999:
                    return False, f"data[{idx}].rule[{r_idx}].frequency_max必须是1-999的整数"
    
    return True, ""

def main():
    if len(sys.argv) != 7:
        print("[PARAM_ERROR] 缺少必需参数")
        print("用法: python create_ad_behavior_crowd.py <name> <trackType> <startDate> <endDate> <idTypes_JSON> <data_JSON>")
        sys.exit(1)
    
    name = sys.argv[1]
    track_type = sys.argv[2]
    start_date = sys.argv[3]
    end_date = sys.argv[4]
    
    try:
        id_types = json.loads(sys.argv[5])
        data = json.loads(sys.argv[6])
    except json.JSONDecodeError as e:
        print(f"[PARAM_ERROR] JSON格式错误: {str(e)}")
        sys.exit(1)
    
    is_valid, error_msg = validate_params(name, track_type, start_date, end_date, id_types, data)
    if not is_valid:
        print(f"[PARAM_ERROR] 参数格式错误: {error_msg}")
        sys.exit(1)
    
    request_body = {
        "name": name,
        "trackType": track_type,
        "startDate": start_date,
        "endDate": end_date,
        "idTypes": id_types,
        "data": data
    }
    
    call_api("/audience/rule/create/advertisement", request_body)

if __name__ == "__main__":
    main()
