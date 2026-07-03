#!/usr/bin/env python3
"""
创建打通人群（跨屏ID打通）
功能：将一个平台的人群ID打通到另一个平台（TV-Mobile跨屏）
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


def validate_params(name, link_type, input_track_type, input_id_types, input_audience_id, output_track_type, output_id_types):
    """
    参数格式校验（严格按照API文档要求）
    
    Returns:
        tuple: (is_valid, error_message)
    """
    # 1. 人群名称格式校验
    if not name or not isinstance(name, str):
        return False, "人群名称不能为空"
    
    # 2. 打通类型格式校验（目前只支持1=TV-Mobile跨屏打通）
    if link_type != 1:
        return False, "linkType只能是1（TV-Mobile跨屏打通）"
    
    # 3. 输入平台类型格式校验
    valid_track_types = ["MOBILE", "OTT"]
    if input_track_type not in valid_track_types:
        return False, f"inputTrackType必须是 {'/'.join(valid_track_types)} 之一"
    
    # 4. 输出平台类型格式校验
    if output_track_type not in valid_track_types:
        return False, f"outputTrackType必须是 {'/'.join(valid_track_types)} 之一"
    
    # 5. 输入输出平台类型互斥校验（输入MOBILE时输出必须OTT，反之亦然）
    if input_track_type == output_track_type:
        return False, "inputTrackType和outputTrackType不能相同（输入MOBILE时输出必须OTT，反之亦然）"
    
    # 6. 输入ID类型格式校验
    if not isinstance(input_id_types, list) or len(input_id_types) == 0:
        return False, "inputIdTypes必须是非空数组"
    
    # 校验输入ID类型枚举值
    valid_mobile_ids = ["MD5_IDFA", "MD5_IMEI", "MD5_OAID", "IDFA", "OAID", "CAID", "MD5_CAID"]
    valid_ott_ids = ["MD5_MAC"]
    
    input_valid_ids = valid_mobile_ids if input_track_type == "MOBILE" else valid_ott_ids
    for id_type in input_id_types:
        if id_type not in input_valid_ids:
            return False, f"inputTrackType={input_track_type}时，inputIdTypes只能包含: {', '.join(input_valid_ids)}"
    
    # 7. 输出ID类型格式校验
    if not isinstance(output_id_types, list) or len(output_id_types) == 0:
        return False, "outputIdTypes必须是非空数组"
    
    # 校验输出ID类型枚举值
    output_valid_ids = valid_mobile_ids if output_track_type == "MOBILE" else valid_ott_ids
    for id_type in output_id_types:
        if id_type not in output_valid_ids:
            return False, f"outputTrackType={output_track_type}时，outputIdTypes只能包含: {', '.join(output_valid_ids)}"
    
    # 8. 输入人群ID格式校验
    if not isinstance(input_audience_id, int) or input_audience_id <= 0:
        return False, "inputAudienceId必须是正整数"
    
    return True, ""

def main():
    if len(sys.argv) != 8:
        print("[PARAM_ERROR] 缺少必需参数")
        print("用法: python create_crossscreen_crowd.py <name> <linkType> <inputTrackType> <inputIdTypes_JSON> <inputAudienceId> <outputTrackType> <outputIdTypes_JSON>")
        print("\n参数说明:")
        print("  name: 人群名称")
        print("  linkType: 打通类型（只能是1=TV-Mobile跨屏打通）")
        print("  inputTrackType: 输入平台类型（MOBILE/OTT）")
        print("  inputIdTypes_JSON: 输入ID类型列表（JSON数组）")
        print("  inputAudienceId: 输入人群ID")
        print("  outputTrackType: 输出平台类型（MOBILE/OTT）")
        print("  outputIdTypes_JSON: 输出ID类型列表（JSON数组）")
        print("\n注意:")
        print("  - 输入MOBILE时输出必须OTT，反之亦然")
        print("  - MOBILE的ID类型: MD5_IDFA/MD5_IMEI/MD5_OAID/IDFA/OAID/CAID/MD5_CAID")
        print("  - OTT的ID类型: MD5_MAC")
        sys.exit(1)
    
    # 解析参数
    name = sys.argv[1]
    
    try:
        link_type = int(sys.argv[2])
    except ValueError as e:
        print(f"[PARAM_ERROR] linkType必须是整数: {str(e)}")
        sys.exit(1)
    
    input_track_type = sys.argv[3]
    
    try:
        input_id_types = json.loads(sys.argv[4])
    except json.JSONDecodeError as e:
        print(f"[PARAM_ERROR] inputIdTypes JSON格式错误: {str(e)}")
        sys.exit(1)
    
    try:
        input_audience_id = int(sys.argv[5])
    except ValueError as e:
        print(f"[PARAM_ERROR] inputAudienceId必须是整数: {str(e)}")
        sys.exit(1)
    
    output_track_type = sys.argv[6]
    
    try:
        output_id_types = json.loads(sys.argv[7])
    except json.JSONDecodeError as e:
        print(f"[PARAM_ERROR] outputIdTypes JSON格式错误: {str(e)}")
        sys.exit(1)
    
    # 格式校验
    is_valid, error_msg = validate_params(
        name, link_type, input_track_type, input_id_types, 
        input_audience_id, output_track_type, output_id_types
    )
    if not is_valid:
        print(f"[PARAM_ERROR] 参数格式错误: {error_msg}")
        sys.exit(1)
    
    # 构建请求体
    request_body = {
        "name": name,
        "linkType": link_type,
        "inputTrackType": input_track_type,
        "inputIdTypes": input_id_types,
        "inputAudienceId": input_audience_id,
        "outputTrackType": output_track_type,
        "outputIdTypes": output_id_types
    }
    
    # 调用API
    call_api("/audience/idlink/create", request_body)

if __name__ == "__main__":
    main()
