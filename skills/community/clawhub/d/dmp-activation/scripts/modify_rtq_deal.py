#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
明日DMP人群投放技能 - 修改RTQ投放订单（智能参数引导版）
"""

import json
import os
import sys
import subprocess

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

def load_order_cache(deal_id):
    """从本地缓存加载订单参数"""
    try:
        cache_dir = os.path.expanduser("~/workspace/.order_cache")
        cache_file = os.path.join(cache_dir, f"order_{deal_id}.json")
        
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_params = json.load(f)
            print(f"✅ 找到订单{deal_id}的缓存信息")
            return cached_params
        else:
            print(f"⚠️ 未找到订单{deal_id}的缓存信息")
            return None
    except Exception as e:
        print(f"⚠️ 读取订单缓存失败: {e}")
        return None

def save_order_cache(deal_id, order_params):
    """保存订单缓存到本地文件"""
    try:
        cache_dir = os.path.expanduser("~/workspace/.order_cache")
        os.makedirs(cache_dir, exist_ok=True)
        
        cache_file = os.path.join(cache_dir, f"order_{deal_id}.json")
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(order_params, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 订单缓存已更新: {cache_file}")
        return True
    except Exception as e:
        print(f"\n⚠️ 更新订单缓存失败: {e}")
        return False

def convert_age_to_enum(age_input):
    """
    将用户友好的年龄段转换为API枚举值
    
    参数:
        age_input: 用户输入的年龄段，如 "18-24", "30-39" 等
    
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
        "30-39": ["102005", "102006"],  # 组合：30-34 + 35-39
        "35-39": ["102006"],
        "40-44": ["102007"],
        "35-44": ["102006", "102007"],  # 组合：35-39 + 40-44
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

def show_confirmation_table(params):
    """展示参数确认表格"""
    print("\n" + "="*80)
    print("📋 修改订单参数确认")
    print("="*80)
    print()
    print("⚠️  请仔细核对以下参数，确认无误后订单将立即修改。")
    print()
    
    # 性别映射
    gender_map = {101001: '男性', 101002: '女性', '': '不限', None: '不限'}
    gender_display = gender_map.get(params.get('gender'), str(params.get('gender')))
    
    # 年龄映射（反向映射，用于显示）
    age_list = params.get('age', [])
    age_display_map = {
        "102020": "15-17",
        "102021": "18-19",
        "102003": "20-24",
        "102004": "25-29",
        "102005": "30-34",
        "102006": "35-39",
        "102007": "40-44",
        "102008": "45-49",
        "102009": "50-54",
        "102010": "55-59",
        "102011": "60-100",
        "allAge": "全年龄"
    }
    if age_list:
        age_display = ', '.join([age_display_map.get(str(a), str(a)) for a in age_list])
    else:
        age_display = '不限'
    
    # 流量类型映射
    flow_type_map = {'mobile': 'mobile', 'pc': 'pc', 'ott': 'ott'}
    flow_type_display = flow_type_map.get(params.get('flowType'), params.get('flowType'))
    
    # 人群包信息
    audiences = params.get('audiences', [])
    audiences_display = '、'.join([f"{a.get('audienceId')}-{a.get('audienceName')}" for a in audiences]) if audiences else '无'
    
    # 打印表格
    print(f"{'参数名称':<20} | {'参数值':<50}")
    print("-"*80)
    print(f"{'订单ID':<20} | {params.get('dealId'):<50}")
    print(f"{'订单名称':<20} | {params.get('dealName'):<50}")
    print(f"{'开始日期':<20} | {params.get('startDate'):<50}")
    print(f"{'结束日期':<20} | {params.get('endDate'):<50}")
    print(f"{'流量类型':<20} | {flow_type_display:<50}")
    print(f"{'性别定向':<20} | {gender_display:<50}")
    print(f"{'年龄定向':<20} | {age_display:<50}")
    print(f"{'使用人群包':<20} | {'是' if params.get('isTag') else '否':<50}")
    if audiences:
        print(f"{'人群包列表':<20} | {audiences_display:<50}")
    print("-"*80)
    print()
    print("⚠️  重要提示：")
    print("  - 修改操作将立即生效，无法撤销")
    print("  - 请确保所有参数准确无误")
    print("  - 如需修改参数，请回复 '取消' 或 '修改'")
    print()

def get_user_confirmation():
    """获取用户确认"""
    print("是否确认修改订单？")
    print("请回复：确认 / 取消 / 修改")
    print()
    print("您的选择: ", end='', flush=True)
    
    user_input = input().strip()
    
    # 确认词
    confirm_words = ['确认', 'yes', 'y', '是', '可以', 'ok']
    # 取消词
    cancel_words = ['取消', 'cancel', 'no', 'n', '否', '修改']
    
    if user_input.lower() in confirm_words:
        return True
    elif user_input.lower() in cancel_words:
        return False
    else:
        print(f"\n⚠️ 无效输入: {user_input}")
        print("请回复：确认 / 取消 / 修改")
        return get_user_confirmation()

def modify_rtq_deal(deal_id, **kwargs):
    """
    修改RTQ投放订单（智能参数引导）
    
    参数:
        deal_id: 订单ID（必需）
        **kwargs: 要修改的参数（可选）
            - dealName: 订单名称
            - startDate: 开始时间
            - endDate: 结束时间
            - flowType: 流量类型
            - gender: 性别
            - age: 年龄段
            - isTag: 是否使用人群包
            - audiences: 人群包列表
            - cookieType: Cookie类型
    """
    
    print("=" * 60)
    print("修改RTQ投放订单")
    print("=" * 60)
    
    # 1. 尝试从本地缓存加载订单参数
    cached_params = load_order_cache(deal_id)
    
    if cached_params:
        # 场景A：找到缓存 - 智能修改
        print("\n✅ 找到订单缓存，只需提供要修改的参数")
        
        # 合并用户提供的参数和缓存的参数
        final_params = {**cached_params, **kwargs}
        final_params['dealId'] = deal_id  # 确保dealId正确
        
    else:
        # 场景B：没有缓存 - 需要完整参数
        print("\n⚠️ 未找到订单缓存")
        print("由于无法查询到订单的完整参数，需要您提供所有必需参数")
        print()
        
        # 检查是否提供了所有必需参数
        required_params = ['dealName', 'startDate', 'endDate', 'flowType', 'gender', 'age', 'isTag']
        missing_params = [p for p in required_params if p not in kwargs]
        
        if missing_params:
            print(f"❌ 缺少必需参数: {', '.join(missing_params)}")
            print()
            print("请提供以下参数：")
            print("  --name <订单名称>")
            print("  --start-date <开始日期>")
            print("  --end-date <结束日期>")
            print("  --flow-type <流量类型>")
            print("  --gender <性别>")
            print("  --age <年龄段>")
            print("  --is-tag <是否使用人群包>")
            sys.exit(1)
        
        # 获取RTQ投放凭证
        rtq_cluster, rtq_access_key = get_rtq_credentials()
        
        # 构建完整参数
        final_params = {
            'dealId': deal_id,
            'service': 'tag',
            'rtqCluster': rtq_cluster,
            'rtqAccessKey': rtq_access_key,
            **kwargs
        }
    
    # 2. 展示参数确认表格
    show_confirmation_table(final_params)
    
    # 3. 等待用户确认
    if not get_user_confirmation():
        print("\n❌ 用户取消操作")
        sys.exit(0)
    
    print("\n✅ 用户已确认，开始执行修改...")
    
    # 4. 查找鉴权技能
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
    
    # 5. 调用API修改订单
    try:
        # 准备API请求参数
        api_params = {
            'dealId': final_params['dealId'],
            'dealName': final_params['dealName'],
            'startDate': final_params['startDate'],
            'endDate': final_params['endDate'],
            'flowType': final_params['flowType'],
            'gender': final_params.get('gender', ''),
            'age': final_params.get('age', []),
            'isTag': final_params.get('isTag', False),
            'service': final_params.get('service', 'tag'),
            'rtqCluster': final_params['rtqCluster'],
            'rtqAccessKey': final_params['rtqAccessKey']
        }
        
        # 如果使用人群包，添加audiences参数
        if api_params['isTag'] and 'audiences' in final_params:
            api_params['audiences'] = final_params['audiences']
        
        # 如果是PC流量，添加cookieType参数
        if api_params['flowType'] == 'pc' and 'cookieType' in final_params:
            api_params['cookieType'] = final_params['cookieType']
        
        result = subprocess.run(
            ['python3', auth_skill_path, 'POST', '/rtq/deal/modify', 
             json.dumps(api_params, ensure_ascii=False)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        response = json.loads(result.stdout)
        
        if response.get('code') == '0':
            print("\n" + "=" * 60)
            print("✅ 订单修改成功！")
            print("=" * 60)
            print(f"\n订单ID: {final_params['dealId']}")
            print(f"订单名称: {final_params['dealName']}")
            print(f"投放时间: {final_params['startDate']} 至 {final_params['endDate']}")
            
            # 更新缓存
            save_order_cache(final_params['dealId'], final_params)
            
            return response.get('data')
        else:
            print("\n" + "=" * 60)
            print("❌ 修改失败")
            print("=" * 60)
            print(f"错误代码: {response.get('code')}")
            print(f"错误信息: {response.get('msg')}")
            sys.exit(1)
            
    except subprocess.TimeoutExpired:
        print("❌ 请求超时")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 修改失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='修改RTQ投放订单')
    parser.add_argument('--deal-id', required=True, type=int, help='订单ID')
    parser.add_argument('--name', help='订单名称')
    parser.add_argument('--start-date', help='开始时间 (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='结束时间 (YYYY-MM-DD)')
    parser.add_argument('--flow-type', choices=['mobile', 'pc', 'ott'], help='流量类型')
    parser.add_argument('--gender', help='性别 (male/female/all)')
    parser.add_argument('--age', help='年龄段，逗号分隔 (如: 25-34,35-44)')
    parser.add_argument('--is-tag', choices=['true', 'false'], help='是否使用人群包')
    parser.add_argument('--audiences', help='人群包列表 (JSON格式)')
    parser.add_argument('--cookie-type', choices=['mzuid', 'muid'], help='Cookie类型')
    
    args = parser.parse_args()
    
    # 构建kwargs
    kwargs = {}
    
    if args.name:
        kwargs['dealName'] = args.name
    if args.start_date:
        kwargs['startDate'] = args.start_date
    if args.end_date:
        kwargs['endDate'] = args.end_date
    if args.flow_type:
        kwargs['flowType'] = args.flow_type
    
    # 性别参数映射
    if args.gender:
        gender_map = {'male': '101001', 'female': '101002', 'all': ''}
        kwargs['gender'] = gender_map.get(args.gender, args.gender)
    
    # 年龄参数转换（使用convert_age_to_enum函数）
    if args.age:
        kwargs['age'] = convert_age_to_enum(args.age)
    
    if args.is_tag:
        kwargs['isTag'] = args.is_tag == 'true'
    
    if args.audiences:
        try:
            kwargs['audiences'] = json.loads(args.audiences)
        except:
            print("❌ audiences参数格式错误，应为JSON数组")
            sys.exit(1)
    
    if args.cookie_type:
        kwargs['cookieType'] = args.cookie_type
    
    modify_rtq_deal(args.deal_id, **kwargs)
