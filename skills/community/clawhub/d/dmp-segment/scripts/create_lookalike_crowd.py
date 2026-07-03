#!/usr/bin/env python3
"""
创建拓展人群（Lookalike）
功能：基于种子人群，通过相似算法拓展更多相似用户
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


def validate_params(name, id_types, seed_audience_id, expand_type, expand_scale=None, confidence_min=None, confidence_max=None, negative_seed_audience_id=None):
    """
    参数格式校验（严格按照API文档要求）
    
    Returns:
        tuple: (is_valid, error_message)
    """
    # 1. 人群名称格式校验
    if not name or not isinstance(name, str):
        return False, "人群名称不能为空"
    
    # 2. ID类型格式校验
    if not isinstance(id_types, list) or len(id_types) == 0:
        return False, "idTypes必须是非空数组"
    
    # 校验ID类型枚举值
    valid_mobile_ids = ["MD5_IDFA", "MD5_IMEI", "MD5_OAID", "IDFA", "OAID", "CAID", "MD5_CAID"]
    for id_type in id_types:
        if id_type not in valid_mobile_ids:
            return False, f"idTypes只能包含: {', '.join(valid_mobile_ids)}"
    
    # 3. 种子人群ID格式校验
    if not isinstance(seed_audience_id, int) or seed_audience_id <= 0:
        return False, "seedAudienceId必须是正整数"
    
    # 4. 负样本人群ID格式校验（可选）
    if negative_seed_audience_id is not None:
        if not isinstance(negative_seed_audience_id, int) or negative_seed_audience_id <= 0:
            return False, "negativeSeedAudienceId必须是正整数"
    
    # 5. 拓展方式格式校验
    if expand_type not in [0, 1]:
        return False, "expandType必须是 0(按量级)/1(按置信度) 之一"
    
    # 6. 按量级拓展参数校验
    if expand_type == 0:
        if expand_scale is None:
            return False, "expandType=0时必须提供expandScale参数"
        
        if not isinstance(expand_scale, int):
            return False, "expandScale必须是整数"
        
        if expand_scale < 50 or expand_scale > 30000:
            return False, "expandScale必须在50-30000万之间"
    
    # 7. 按置信度拓展参数校验
    if expand_type == 1:
        if confidence_min is None or confidence_max is None:
            return False, "expandType=1时必须提供confidenceMin和confidenceMax参数"
        
        if not isinstance(confidence_min, (int, float)) or not isinstance(confidence_max, (int, float)):
            return False, "confidenceMin和confidenceMax必须是数字"
        
        if confidence_min < 0.1 or confidence_min > 0.9:
            return False, "confidenceMin必须在0.1-0.9之间"
        
        if confidence_max < 0.1 or confidence_max > 0.9:
            return False, "confidenceMax必须在0.1-0.9之间"
        
        if confidence_min >= confidence_max:
            return False, "confidenceMin必须小于confidenceMax"
    
    return True, ""

def main():
    if len(sys.argv) < 6:
        print("[PARAM_ERROR] 缺少必需参数")
        print("用法: python create_lookalike_crowd.py <name> <idTypes_JSON> <seedAudienceId> <expandType> <expandScale|confidenceMin confidenceMax> [negativeSeedAudienceId]")
        print("\n参数说明:")
        print("  name: 人群名称")
        print("  idTypes_JSON: ID类型列表（JSON数组）")
        print("  seedAudienceId: 种子人群ID（正样本）")
        print("  expandType: 拓展方式（0=按量级, 1=按置信度）")
        print("  expandScale: 目标量级（当expandType=0时，50-30000万）")
        print("  confidenceMin confidenceMax: 置信度范围（当expandType=1时，0.1-0.9）")
        print("  negativeSeedAudienceId: 负样本人群ID（可选）")
        print("\n注意:")
        print("  - 种子人群状态需为成功且非拓展人群")
        sys.exit(1)
    
    # 解析基础参数
    name = sys.argv[1]
    
    try:
        id_types = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(f"[PARAM_ERROR] idTypes JSON格式错误: {str(e)}")
        sys.exit(1)
    
    try:
        seed_audience_id = int(sys.argv[3])
        expand_type = int(sys.argv[4])
    except ValueError as e:
        print(f"[PARAM_ERROR] seedAudienceId和expandType必须是整数: {str(e)}")
        sys.exit(1)
    
    # 根据expandType解析不同参数
    expand_scale = None
    confidence_min = None
    confidence_max = None
    negative_seed_audience_id = None
    
    if expand_type == 0:
        # 按量级拓展
        if len(sys.argv) < 6:
            print("[PARAM_ERROR] 按量级拓展需要提供expandScale参数")
            sys.exit(1)
        
        try:
            expand_scale = int(sys.argv[5])
        except ValueError as e:
            print(f"[PARAM_ERROR] expandScale必须是整数: {str(e)}")
            sys.exit(1)
        
        # 可选的负样本人群ID
        if len(sys.argv) >= 7:
            try:
                negative_seed_audience_id = int(sys.argv[6])
            except ValueError as e:
                print(f"[PARAM_ERROR] negativeSeedAudienceId必须是整数: {str(e)}")
                sys.exit(1)
    
    elif expand_type == 1:
        # 按置信度拓展
        if len(sys.argv) < 7:
            print("[PARAM_ERROR] 按置信度拓展需要提供confidenceMin和confidenceMax参数")
            sys.exit(1)
        
        try:
            confidence_min = float(sys.argv[5])
            confidence_max = float(sys.argv[6])
        except ValueError as e:
            print(f"[PARAM_ERROR] confidenceMin和confidenceMax必须是数字: {str(e)}")
            sys.exit(1)
        
        # 可选的负样本人群ID
        if len(sys.argv) >= 8:
            try:
                negative_seed_audience_id = int(sys.argv[7])
            except ValueError as e:
                print(f"[PARAM_ERROR] negativeSeedAudienceId必须是整数: {str(e)}")
                sys.exit(1)
    
    # 格式校验
    is_valid, error_msg = validate_params(
        name, id_types, seed_audience_id, expand_type,
        expand_scale, confidence_min, confidence_max, negative_seed_audience_id
    )
    if not is_valid:
        print(f"[PARAM_ERROR] 参数格式错误: {error_msg}")
        sys.exit(1)
    
    # 构建请求体
    request_body = {
        "name": name,
        "idTypes": id_types,
        "seedAudienceId": seed_audience_id,
        "expandType": expand_type
    }
    
    # 添加可选参数
    if negative_seed_audience_id is not None:
        request_body["negativeSeedAudienceId"] = negative_seed_audience_id
    
    if expand_type == 0:
        request_body["expandScale"] = expand_scale
    else:
        request_body["confidenceMin"] = confidence_min
        request_body["confidenceMax"] = confidence_max
    
    # 调用API
    call_api("/audience/expand/create", request_body)

if __name__ == "__main__":
    main()
