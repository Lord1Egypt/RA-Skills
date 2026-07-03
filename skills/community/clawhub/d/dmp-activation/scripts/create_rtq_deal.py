#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
明日DMP人群投放技能 - 创建RTQ投放订单
"""

import json
import os
import sys
import subprocess

def convert_age_to_enum(age_input):
    """
    将用户友好的年龄段转换为API枚举值
    
    参数:
        age_input: 用户输入的年龄段，如 "18-24", "25-34" 等
    
    返回:
        枚举值列表
    """
    # 年龄段映射表（根据明日DMP API文档）
    age_mapping = {
        "15-17": ["102020"],
        "18-19": ["102021"],
        "20-24": ["102003"],
        "18-24": ["102021", "102003"],  # 组合：18-19 + 20-24
        "25-29": ["102004"],
        "30-34": ["102005"],
        "25-34": ["102004", "102005"],  # 组合：25-29 + 30-34
        "35-39": ["102006"],
        "40-44": ["102007"],
        "35-44": ["102006", "102007"],  # 组合：35-39 + 40-44
        "25-44": ["102004", "102005", "102006", "102007"],  # 组合：25-34 + 35-44
        "45-49": ["102008"],
        "50-54": ["102009"],
        "45-54": ["102008", "102009"],  # 组合：45-49 + 50-54
        "55-59": ["102010"],
        "60-100": ["102011"],
        "55+": ["102010", "102011"],  # 组合：55-59 + 60-100
        "all": ["allAge"],
        "allage": ["allAge"]
    }
    
    result = []
    
    # 处理逗号分隔的多个年龄段
    age_segments = [seg.strip() for seg in age_input.split(',')]
    
    for segment in age_segments:
        segment_lower = segment.lower()
        
        # 如果已经是枚举值格式（102xxx），直接使用
        if segment.startswith('102') or segment_lower == 'allage':
            result.append(segment)
        # 否则从映射表中查找
        elif segment_lower in age_mapping:
            result.extend(age_mapping[segment_lower])
        else:
            # 未知格式，保持原样
            result.append(segment)
    
    return result

def get_rtq_credentials():
    """
    获取RTQ投放凭证
    
    优先级：
    1. 环境变量（RTQ_CLUSTER, RTQ_ACCESS_KEY）
    2. 凭证文件（由鉴权技能管理的路径）
    
    Returns:
        tuple: (rtq_cluster, rtq_access_key)
    """
    # 优先从环境变量读取
    env_cluster = os.environ.get("RTQ_CLUSTER")
    env_access_key = os.environ.get("RTQ_ACCESS_KEY")
    
    if env_cluster and env_access_key:
        return env_cluster, env_access_key
    
    # 从凭证文件读取（使用鉴权技能的路径逻辑）
    from pathlib import Path
    
    # 优先级：当前目录 > 用户主目录
    credentials_paths = [
        Path.cwd() / ".mingdata_credentials",
        Path.cwd() / ".mingdata_dmp_credentials",
        Path.home() / ".mingdata_credentials",
        Path.home() / ".mingdata_dmp_credentials"
    ]
    
    for cred_path in credentials_paths:
        if cred_path.exists():
            try:
                with open(cred_path, 'r', encoding='utf-8') as f:
                    credentials = json.load(f)
                
                rtq_cluster = credentials.get('rtq_cluster')
                rtq_access_key = credentials.get('rtq_access_key')
                
                if rtq_cluster and rtq_access_key:
                    return rtq_cluster, rtq_access_key
            except Exception:
                continue
    
    print("❌ 错误：未找到RTQ投放凭证")
    print("请配置以下凭证：")
    print("  方式1：设置环境变量 RTQ_CLUSTER 和 RTQ_ACCESS_KEY")
    print("  方式2：在凭证文件中添加 rtq_cluster 和 rtq_access_key 字段")
    sys.exit(1)

def save_order_cache(deal_id, order_params):
    """保存订单缓存到本地文件"""
    try:
        # 缓存目录
        cache_dir = os.path.expanduser("~/workspace/.order_cache")
        os.makedirs(cache_dir, exist_ok=True)
        
        # 缓存文件路径
        cache_file = os.path.join(cache_dir, f"order_{deal_id}.json")
        
        # 保存订单参数
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(order_params, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 订单缓存已保存: {cache_file}")
        return True
    except Exception as e:
        print(f"\n⚠️ 保存订单缓存失败: {e}")
        return False

def verify_audience(audience_ids, auth_skill_path):
    """
    验证人群ID是否有效，并获取人群详细信息
    
    参数:
        audience_ids: 人群ID列表
        auth_skill_path: 鉴权技能路径
    
    返回:
        验证成功的人群信息列表，或None（验证失败）
    """
    print("\n" + "=" * 60)
    print("⚠️ 强制执行人群ID验证...")
    print("=" * 60)
    
    try:
        # 调用人群任务状态查询接口
        request_body = {"audienceId": audience_ids[0], "pageNum": 1, "pageSize": 10}
        
        result = subprocess.run(
            ["python3", auth_skill_path, "POST", "/audience/manage/taskList", 
             json.dumps(request_body, ensure_ascii=False)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        response = json.loads(result.stdout)
        
        if response.get('code') == '0' or response.get('code') == 0:
            data = response.get('data', [])
            
            # 查找目标人群
            target_audience = None
            for aud in data:
                if aud.get('audienceId') in audience_ids:
                    target_audience = aud
                    break
            
            if not target_audience:
                print(f"\n❌ 人群ID {audience_ids} 不存在或无效")
                print("\n⚠️ 人群验证失败，无法创建订单")
                print("\n建议方案：")
                print("1. 使用属性定向（性别+年龄）创建订单")
                print("2. 查询可用的人群列表，选择正确的人群ID")
                print("3. 检查人群ID是否输入正确")
                return None
            
            # 验证人群状态
            audience_id = target_audience.get('audienceId')
            audience_name = target_audience.get('audienceName')
            audience_status = target_audience.get('audienceStatus')
            audience_amount = target_audience.get('audienceAmount', '0')
            create_time = target_audience.get('createTime')
            
            status_map = {
                0: "失败",
                1: "成功",
                2: "等待中",
                3: "计算中"
            }
            status_text = status_map.get(audience_status, "未知")
            
            print(f"\n✅ 人群验证成功！")
            print(f"  - 人群ID：{audience_id}")
            print(f"  - 人群名称：{audience_name}")
            print(f"  - 人群量级：{audience_amount}")
            print(f"  - 人群状态：{status_text}")
            print(f"  - 创建时间：{create_time}")
            
            # 检查人群量级是否为0
            audience_count = int(audience_amount) if audience_amount.isdigit() else 0
            if audience_count == 0:
                print(f"\n⚠️ 警告：人群量级为0，可能导致投放数据不准确")
                print(f"⚠️ 请确认人群ID {audience_id} 是否正确")
            
            if audience_status == 1:
                # 状态为成功，可以使用
                verified_audiences = [{
                    "audienceId": audience_id,
                    "audienceName": audience_name,
                    "audienceCount": audience_count,
                    "audienceValidity": "2026-12-31",
                    "audienceSource": 2
                }]
                
                # 强制验证：禁止使用量级为0的人群
                if audience_count == 0:
                    print(f"\n❌ 错误：人群量级为0，禁止创建订单")
                    print(f"❌ 这可能是数据错误，请检查人群ID或重新圈选人群")
                    return None
                
                return verified_audiences
            elif audience_status == 0:
                print(f"\n❌ 人群ID {audience_id} 创建失败，不能使用")
                return None
            elif audience_status in [2, 3]:
                print(f"\n⏳ 人群ID {audience_id} 正在{status_text}")
                print("\n建议：")
                print("1. 等待人群计算完成后再创建订单")
                print("2. 或者先使用属性定向创建订单")
                return None
        else:
            print(f"\n❌ 查询人群失败")
            print(f"错误代码: {response.get('code')}")
            print(f"错误信息: {response.get('msg')}")
            return None
            
    except Exception as e:
        print(f"\n❌ 验证人群失败: {e}")
        return None

def create_rtq_deal(deal_name, start_date, end_date, flow_type, 
                    gender=None, age=None, audiences=None, cookie_type=None):
    """
    创建RTQ投放订单
    
    参数:
        deal_name: 订单名称
        start_date: 开始时间 (格式: YYYY-MM-DD)
        end_date: 结束时间 (格式: YYYY-MM-DD)
        flow_type: 流量类型 (mobile/pc/ott)
        gender: 性别 (101001男/101002女/allGender，可选)
        age: 年龄段列表 (可选)
        audiences: 人群包列表 (可选)
        cookie_type: Cookie类型 (flowType=pc时需要，可选)
    """
    
    print("=" * 60)
    print("创建RTQ投放订单")
    print("=" * 60)
    
    # 获取RTQ投放凭证
    rtq_cluster, rtq_access_key = get_rtq_credentials()
    
    # 查找鉴权技能路径
    auth_skill_path = None
    from pathlib import Path
    possible_paths = [
        Path.home() / ".openclaw" / "workspace" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        Path.home() / ".openclaw" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        Path.home() / ".skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        Path.home() / ".skills" / "9126" / "scripts" / "minri_dmp_api.py",
        Path("/data/dm-agent-outputs/workspace/.skills/9126/scripts/minri_dmp_api.py"),
    ]
    for path in possible_paths:
        if path.exists():
            auth_skill_path = str(path)
            break
    # 动态扫描
    if not auth_skill_path:
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
                                        auth_skill_path = str(candidate)
                                        break
                            except:
                                continue
                if auth_skill_path:
                    break
    if not auth_skill_path:
        print("❌ 错误：未找到鉴权技能")
        print("请确保已安装 mingdata-dmp-auth 技能")
        sys.exit(1)
    
    # 如果使用人群包，必须先验证人群ID
    verified_audiences = None
    if audiences:
        # 提取人群ID列表
        audience_ids = [aud.get('audienceId') for aud in audiences if 'audienceId' in aud]
        
        if audience_ids:
            # 强制验证人群ID
            verified_audiences = verify_audience(audience_ids, auth_skill_path)
            
            if verified_audiences is None:
                print("\n" + "=" * 60)
                print("❌ 人群验证失败，无法创建订单")
                print("=" * 60)
                print("\n⚠️ 不能自动改用属性定向，请用户明确选择：")
                print("\n选项1：使用属性定向（性别+年龄）创建订单")
                print("  - 需要提供性别和年龄参数")
                print("  - 不使用人群包，仅基于基础属性定向")
                print("\n选项2：检查人群ID是否正确，或等待人群计算完成后重试")
                print("\n选项3：查询可用的人群列表，选择正确的人群ID")
                print("\n请告知用户选择哪个选项，不要自动决定。")
                sys.exit(1)
            
            # 使用验证后的完整人群信息
            audiences = verified_audiences
    
    # 构建请求参数
    params = {
        "dealName": deal_name,
        "startDate": start_date,
        "endDate": end_date,
        "flowType": flow_type,
        "rtqCluster": rtq_cluster,
        "rtqAccessKey": rtq_access_key
    }
    
    # 判断service和isTag
    if audiences:
        # 使用人群包
        params["service"] = "tag"
        params["isTag"] = "True"
        params["audiences"] = audiences
        # 人群包投放也可以添加性别和年龄定向
        if gender:
            params["gender"] = gender
        if age:
            params["age"] = age
    else:
        # 使用属性定向
        params["service"] = "tag"
        params["isTag"] = "False"
        
        # 添加可选的定向条件
        if gender:
            params["gender"] = gender
        if age:
            params["age"] = age
    
    # PC流量需要cookieType
    if flow_type == "pc" and cookie_type:
        params["cookieType"] = cookie_type
    
    print("\n订单参数:")
    print(json.dumps(params, ensure_ascii=False, indent=2))
    print()
    
    # 调用鉴权技能的API模块
    try:
        result = subprocess.run(
            ["python3", auth_skill_path, "POST", "/rtq/deal/create", 
             json.dumps(params, ensure_ascii=False)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        response = json.loads(result.stdout)
        
        if response.get('code') == '0' or response.get('code') == 0:
            print("=" * 60)
            print("✅ 投放订单创建成功！")
            print("=" * 60)
            
            data = response.get('data', {})
            deal_id = data.get('dealId')
            
            print(f"\n订单ID: {deal_id}")
            print(f"订单名称: {deal_name}")
            print(f"投放时间: {start_date} 至 {end_date}")
            print(f"流量类型: {flow_type}")
            
            if audiences:
                print(f"人群包数量: {len(audiences)}")
            else:
                if gender:
                    print(f"性别定向: {gender}")
                if age:
                    print(f"年龄定向: {age}")
            
            # 保存订单缓存（用于后续修改订单时自动补全参数）
            if deal_id:
                cache_params = {
                    "dealId": deal_id,
                    "dealName": deal_name,
                    "startDate": start_date,
                    "endDate": end_date,
                    "flowType": flow_type,
                    "gender": gender,
                    "age": age,
                    "isTag": bool(audiences),
                    "audiences": audiences,
                    "cookieType": cookie_type,
                    "rtqCluster": rtq_cluster,
                    "rtqAccessKey": rtq_access_key,
                    "service": "tag"
                }
                save_order_cache(deal_id, cache_params)
            
            return data
        else:
            print("=" * 60)
            print("❌ 创建失败")
            print("=" * 60)
            print(f"错误代码: {response.get('code')}")
            print(f"错误信息: {response.get('msg')}")
            sys.exit(1)
            
    except subprocess.TimeoutExpired:
        print("❌ 请求超时")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 创建失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='创建RTQ投放订单')
    parser.add_argument('--name', required=True, help='订单名称')
    parser.add_argument('--start-date', required=True, help='开始时间 (YYYY-MM-DD)')
    parser.add_argument('--end-date', required=True, help='结束时间 (YYYY-MM-DD)')
    parser.add_argument('--flow-type', required=True, choices=['mobile', 'pc', 'ott'], 
                        help='流量类型')
    parser.add_argument('--gender', help='性别 (101001/101002/allGender 或 male/female/all)')
    parser.add_argument('--age', help='年龄段 (支持: 18-24, 25-34, 35-44, 45-54, 55+, 或枚举值)')
    parser.add_argument('--audiences', help='人群包JSON (如: [{"audienceId":123}])')
    parser.add_argument('--cookie-type', help='Cookie类型 (pc流量时需要)')
    
    args = parser.parse_args()
    
    # 处理gender参数 - 支持用户友好的输入
    gender = args.gender
    if gender:
        gender_mapping = {
            'male': '101001',
            'female': '101002',
            'all': 'allGender'
        }
        gender = gender_mapping.get(gender.lower(), gender)
    
    # 处理age参数 - 自动转换为枚举值
    age_list = None
    if args.age:
        age_list = convert_age_to_enum(args.age)
    
    # 处理audiences参数
    audiences_list = None
    if args.audiences:
        try:
            audiences_list = json.loads(args.audiences)
        except:
            print("❌ audiences参数格式错误，应为JSON数组")
            sys.exit(1)
    
    create_rtq_deal(
        deal_name=args.name,
        start_date=args.start_date,
        end_date=args.end_date,
        flow_type=args.flow_type,
        gender=gender,
        age=age_list,
        audiences=audiences_list,
        cookie_type=args.cookie_type
    )
