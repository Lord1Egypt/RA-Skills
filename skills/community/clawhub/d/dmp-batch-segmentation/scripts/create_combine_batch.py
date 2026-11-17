#!/usr/bin/env python3
"""
组合人群批量创建脚本
功能：根据标签列表批量创建组合人群任务
支持三种拆分模式：多对一、一对多、多对多
"""

import sys
import os
import json
import math
from pathlib import Path
from datetime import datetime

# 添加脚本目录到路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

# 导入鉴权模块
from find_auth_skill import find_auth_skill_path

# 导入cron硬约束模块
from cron_helper import check_cron_setup, generate_cron_params_combine, get_lock_file

# 导入标签校验模块
from validate_tags import parse_tags_input, validate_tags, determine_split_mode, MAX_TAGS_PER_GROUP

# 导入任务记录检查模块
from check_task_logger import print_step8_reminder

def generate_project_id():
    """生成项目ID"""
    return f"combine_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def split_tags(tags, per_group=MAX_TAGS_PER_GROUP):
    """
    将标签列表拆分成多个组
    
    Args:
        tags: 标签ID列表
        per_group: 每组标签数
        
    Returns:
        list: 标签组列表
    """
    groups = []
    total = len(tags)
    group_count = math.ceil(total / per_group)
    
    for i in range(group_count):
        start = i * per_group
        end = min((i + 1) * per_group, total)
        groups.append({
            "group_no": i + 1,
            "tags": tags[start:end],
            "count": end - start
        })
    
    return groups

def generate_combinations(a_groups, b_groups, split_mode, audience_name, suffix, logic, split_by_dimension=False, a_tags_original=None, b_tags_original=None, a_audiences=None, b_audiences=None):
    """
    生成组合任务列表
    
    Args:
        a_groups: A规则标签组
        b_groups: B规则标签组
        split_mode: 拆分模式
        audience_name: 人群包名
        suffix: 后缀
        logic: 组合逻辑
        split_by_dimension: 是否按维度拆分
        a_tags_original: 原始A标签列表
        b_tags_original: 原始B标签列表
        a_audiences: A规则人群ID列表（固定，不拆分）
        b_audiences: B规则人群ID列表（固定，不拆分）
    
    Returns:
        list: 组合任务列表
    """
    combinations = []
    task_id = 1
    
    # 按维度拆分模式：每个A标签分别创建独立任务
    if split_by_dimension and a_tags_original:
        for a_tag in a_tags_original:
            combinations.append({
                "task_id": task_id,
                "task_name": f"{audience_name}{suffix}{task_id}",
                "a_tags": [a_tag],
                "b_tags": b_tags_original if b_tags_original else [],
                "a_audiences": a_audiences or [],
                "b_audiences": b_audiences or [],
                "logic": logic
            })
            task_id += 1
        return combinations
    
    if split_mode == "many_to_one":
        for a_group in a_groups:
            combinations.append({
                "task_id": task_id,
                "task_name": f"{audience_name}{suffix}{task_id}",
                "a_tags": a_group["tags"],
                "b_tags": b_groups[0]["tags"] if b_groups else [],
                "a_audiences": a_audiences or [],
                "b_audiences": b_audiences or [],
                "logic": logic
            })
            task_id += 1
    
    elif split_mode == "one_to_many":
        for b_group in b_groups:
            combinations.append({
                "task_id": task_id,
                "task_name": f"{audience_name}{suffix}{task_id}",
                "a_tags": a_groups[0]["tags"] if a_groups else [],
                "b_tags": b_group["tags"],
                "a_audiences": a_audiences or [],
                "b_audiences": b_audiences or [],
                "logic": logic
            })
            task_id += 1
    
    elif split_mode == "many_to_many":
        for a_group in a_groups:
            for b_group in b_groups:
                combinations.append({
                    "task_id": task_id,
                    "task_name": f"{audience_name}{suffix}{task_id}",
                    "a_tags": a_group["tags"],
                    "b_tags": b_group["tags"],
                    "a_audiences": a_audiences or [],
                    "b_audiences": b_audiences or [],
                    "logic": logic
                })
                task_id += 1
    
    else:  # one_to_one
        combinations.append({
            "task_id": task_id,
            "task_name": f"{audience_name}{suffix}{task_id}",
            "a_tags": a_groups[0]["tags"] if a_groups else [],
            "b_tags": b_groups[0]["tags"] if b_groups else [],
            "a_audiences": a_audiences or [],
            "b_audiences": b_audiences or [],
            "logic": logic
        })
    
    return combinations

def build_group_rules(tags, audiences, inner_logic):
    """
    构建单个组内的rule列表（框内OR，框间and/not）
    
    Args:
        tags: 标签ID列表
        audiences: 人群ID列表
        inner_logic: 组内框间逻辑（and/not，末位noop）
    
    Returns:
        list: rule数组（可直接放入group字段）
    """
    rules = []
    has_content = bool(tags or audiences)
    
    if not has_content:
        rules.append({"op": "noop", "rule": {"audience": [], "tag": []}})
        return rules
    
    # 每个标签单独一个rule（框间AND/NOT），第一个rule带audience
    for i, tag in enumerate(tags):
        is_last = (i == len(tags) - 1)
        aud = audiences if i == 0 else []
        rules.append({
            "op": "noop" if is_last else inner_logic,
            "rule": {"audience": aud, "tag": [tag]}
        })
    
    # 有audience但没有tag时，单独加audience rule
    if audiences and not tags:
        rules.append({"op": "noop", "rule": {"audience": audiences, "tag": []}})
    
    return rules


def create_combine_task(auth_script, params, combination):
    """
    创建单个组合人群任务（支持多组组间交并差，v1.4 group层级）
    
    combination结构（v1.4多组）：
    {
        "task_id": int,
        "task_name": str,
        "groups": [  # 最多10组
            {
                "tags": [int],         # 本组标签（框内OR）
                "audiences": [int],    # 本组人群（框内OR）
                "op": "and"|"or"|"not"|"noop"  # 连向下一组的方式
            },
            ...
        ]
    }
    
    兼容旧结构（a_tags/b_tags/logic）：自动转换为单组/双组
    """
    groups = []
    
    # 兼容旧结构：如果有groups字段直接使用，否则从a/b规则构建
    if "groups" in combination:
        groups = combination["groups"]
    else:
        # 旧结构转换：A规则为第1组，B规则为第2组（通过logic连接）
        logic = combination.get("logic", "and").lower()
        a_tags = combination.get("a_tags", [])
        b_tags = combination.get("b_tags", [])
        a_audiences = combination.get("a_audiences", [])
        b_audiences = combination.get("b_audiences", [])
        
        if b_tags or b_audiences:
            # 双组场景：第1组op=logic连向第2组，第2组op=noop
            groups = [
                {
                    "tags": a_tags,
                    "audiences": a_audiences,
                    "op": logic
                },
                {
                    "tags": b_tags,
                    "audiences": b_audiences,
                    "op": "noop"
                }
            ]
        else:
            # 单组场景
            groups = [
                {
                    "tags": a_tags,
                    "audiences": a_audiences,
                    "op": "noop"
                }
            ]
    
    # 校验组数（最多10组）
    if len(groups) > 10:
        return {"code": "1", "msg": f"组数超限：最多10组，当前{len(groups)}组"}
    
    # 校验末组op必须为noop
    if groups[-1].get("op") != "noop":
        groups[-1]["op"] = "noop"
    
    # 构建v1.4 data结构
    data = []
    for g in groups:
        inner_logic = "and"  # 组内框间默认AND（NOT场景由组间op控制）
        group_rules = build_group_rules(g.get("tags", []), g.get("audiences", []), inner_logic)
        data.append({
            "op": g["op"],
            "group": group_rules
        })
    
    api_params = {
        "name": combination["task_name"],
        "trackType": params["track_type"],
        "idTypes": params["id_types"],
        "brandId": params.get("brandId", []) or [],
        "data": data
    }
    
    # 调用API
    import subprocess
    cmd = [
        sys.executable, str(auth_script),
        "POST",
        "/audience/manage/combine/create",
        json.dumps(api_params, ensure_ascii=False)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    try:
        response = json.loads(result.stdout)
        return response
    except json.JSONDecodeError:
        error_detail = result.stdout or result.stderr or "无输出"
        return {"code": "1", "msg": f"API调用失败: {error_detail}"}

def save_project_plan(project_id, audience_name, suffix, params, split_mode, combinations, output_dir="data/plans"):
    """保存项目计划"""
    project_dir = Path(output_dir) / project_id
    project_dir.mkdir(parents=True, exist_ok=True)
    
    plan = {
        "projectId": project_id,
        "audienceName": audience_name,
        "suffix": suffix,
        "scenario": "COMBINE_MULTI_RULE",
        "splitMode": split_mode,
        "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "params": params,
        "totalTasks": len(combinations),
        "combinations": [
            {
                "taskId": c["task_id"],
                "taskName": c["task_name"],
                "aTagCount": len(c["a_tags"]),
                "bTagCount": len(c["b_tags"]),
                "logic": c["logic"]
            }
            for c in combinations
        ]
    }
    
    plan_file = project_dir / "plan.json"
    with open(plan_file, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    
    return plan_file

def save_project_status(project_id, status, tasks_status, output_dir="data/plans", flow_lock=None):
    """保存项目状态（含步骤锁）"""
    project_dir = Path(output_dir) / project_id
    
    status_data = {
        "projectId": project_id,
        "status": status,
        "tasks": tasks_status,
        "lastPollAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 加入步骤锁
    if flow_lock:
        status_data["flow_lock"] = flow_lock
    
    status_file = project_dir / "status.json"
    with open(status_file, 'w', encoding='utf-8') as f:
        json.dump(status_data, f, ensure_ascii=False, indent=2)
    
    return status_file

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='组合人群批量创建')
    parser.add_argument('--a-tags', help='A规则标签(逗号分隔或文件路径)')
    parser.add_argument('--b-tags', help='B规则标签(逗号分隔或文件路径)')
    parser.add_argument('--a-audiences', help='A规则人群ID(逗号分隔或文件路径)')
    parser.add_argument('--b-audiences', help='B规则人群ID(逗号分隔或文件路径)')
    parser.add_argument('--audience-name', help='人群包名')
    parser.add_argument('--suffix', default='_组合', help='后缀')
    parser.add_argument('--logic', default='and', choices=['and', 'or', 'not'], help='组合逻辑')
    parser.add_argument('--track-type', default='MOBILE', help='平台类型')
    parser.add_argument('--id-types', help='ID类型(逗号分隔)')
    parser.add_argument('--split-mode', choices=['auto', 'many_to_one', 'one_to_many', 'many_to_many'], 
                        default='auto', help='拆分模式')
    parser.add_argument('--split-by-dimension', action='store_true', 
                        help='按维度拆分：每个A标签分别创建独立任务')
    parser.add_argument('--tags-per-group', type=int, default=50, help='每组标签数(最多50)')
    parser.add_argument('--batch-size', type=int, default=1, help='每批任务数（默认5，最大5；逐个串行创建，批间等计算完成）')
    parser.add_argument('--task-index', type=int, help='[兼容旧用法] 指定创建单个任务（从1开始）')
    parser.add_argument('--batch-start', type=int, help='本批起始任务索引（从1开始，含），如1表示从第1个任务开始')
    parser.add_argument('--batch-end', type=int, help='本批结束任务索引（从1开始，含），如5表示到第5个任务')
    parser.add_argument('--output-dir', default='data/plans', help='输出目录')
    # 重试相关参数
    parser.add_argument('--retry', help='重试模式: JSON格式失败任务列表')
    parser.add_argument('--project-id', help='关联已有项目ID（用于追加批次或重试）')
    parser.add_argument('--stop-on-error', action='store_true', 
                        help='本批次中有任务创建失败时立即停止（pause策略使用）')
    parser.add_argument('--brand-id', default='', help='品牌ID列表(逗号分隔，可选；不传/空=全部品牌；投放订单仅支持单选string，其余接口为数组)')
    parser.add_argument('--groups-json', default='', help='[v1.4多组] 直接传入多组定义JSON字符串，格式：[{"tags":[id...],"audiences":[id...],"op":"and/or/not/noop"},...]，最多10组；传入后忽略--a-tags/--b-tags/--logic')
    
    args = parser.parse_args()
    
    # 重试模式
    if args.retry:
        run_retry_mode(args)
        return
    
    # v1.4多组模式优先检查
    if args.groups_json:
        # 多组模式只需要audience_name和id_types
        if not (args.audience_name and args.id_types):
            missing = []
            if not args.audience_name: missing.append('--audience-name')
            if not args.id_types: missing.append('--id-types')
            print(f"❌ 缺少必填参数: {', '.join(missing)}")
            sys.exit(1)
    else:
        # 旧模式：A规则和B规则各自至少需要有标签或人群ID
        has_a = bool(args.a_tags or args.a_audiences)
        has_b = bool(args.b_tags or args.b_audiences)
        if not (args.audience_name and args.id_types and (has_a or has_b)):
            missing = []
            if not args.audience_name:
                missing.append('--audience-name')
            if not args.id_types:
                missing.append('--id-types')
            if not (has_a or has_b):
                missing.append('--a-tags/--a-audiences 或 --b-tags/--b-audiences')
            print(f"❌ 缺少必填参数: {', '.join(missing)}")
            sys.exit(1)
    
    print("\n" + "="*60)
    print("组合人群批量创建")
    print("="*60)
    
    brand_id_list = [b.strip() for b in args.brand_id.split(',') if b.strip()] if args.brand_id else []
    
    # 1. 解析标签和人群ID
    print("\n[1/4] 解析规则...")
    
    a_tags = []
    b_tags = []
    a_audiences = []
    b_audiences = []
    
    # v1.4多组模式：直接从--groups-json生成单个任务，不走A/B拆分
    if args.groups_json:
        try:
            groups_def = json.loads(args.groups_json)
            if not isinstance(groups_def, list) or len(groups_def) == 0:
                print("❌ groups-json格式错误：需要非空数组")
                sys.exit(1)
            if len(groups_def) > 10:
                print(f"❌ 组数超限：最多10组，当前{len(groups_def)}组")
                sys.exit(1)
            # 校验末组op为noop
            if groups_def[-1].get("op") != "noop":
                groups_def[-1]["op"] = "noop"
            # 校验组间op枚举
            valid_ops = {"and", "or", "not", "noop"}
            for i, g in enumerate(groups_def):
                if g.get("op") not in valid_ops:
                    print(f"❌ 第{i+1}组op无效：{g.get('op')}，必须为and/or/not/noop")
                    sys.exit(1)
                if not isinstance(g.get("tags", []), list) or not isinstance(g.get("audiences", []), list):
                    print(f"❌ 第{i+1}组tags/audiences必须为数组")
                    sys.exit(1)
            # 直接生成单个combination
            combinations = [{
                "task_id": 1,
                "task_name": args.audience_name,
                "groups": [
                    {
                        "tags": [int(t) for t in g.get("tags", [])],
                        "audiences": [int(a) for a in g.get("audiences", [])],
                        "op": g["op"]
                    }
                    for g in groups_def
                ]
            }]
            print(f"✅ v1.4多组模式：{len(groups_def)}组，组间op=[{', '.join(g['op'] for g in groups_def)}]")
            # 跳过A/B拆分流程，直接进入项目创建
            project_id = generate_project_id()
            params = {
                "track_type": args.track_type,
                "id_types": args.id_types.split(','),
                "brandId": brand_id_list,
                "logic": "multi_group",
                "groups_count": len(groups_def)
            }
            plan = {
                "projectId": project_id,
                "audienceName": args.audience_name,
                "suffix": args.suffix,
                "scenario": "COMBINE_MULTI_GROUP_v14",
                "createdAt": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "params": params,
                "totalTasks": 1,
                "combinations": [{"taskId": 1, "taskName": args.audience_name, "groups": groups_def}]
            }
            project_dir = Path(args.output_dir) / project_id
            project_dir.mkdir(parents=True, exist_ok=True)
            with open(project_dir / "plan.json", 'w', encoding='utf-8') as f:
                json.dump(plan, f, ensure_ascii=False, indent=2)
            print(f"✅ 项目计划已保存: {project_dir/'plan.json'}")
            # 直接跳到任务创建
            auth_script = find_auth_skill_path()
            if not auth_script:
                print("❌ 未找到鉴权技能")
                sys.exit(1)
            print(f"✅ 鉴权技能路径: {auth_script}")
            combination = combinations[0]
            response = create_combine_task(auth_script, params, combination)
            print(json.dumps(response, ensure_ascii=False, indent=2))
            if isinstance(response, dict) and response.get("code") == "0":
                audience_id = response.get("data", {}).get("audienceId") or response.get("data", {}).get("taskId")
                save_project_status(project_id, "created", [{
                    "taskId": 1, "taskName": combination["task_name"],
                    "audienceId": audience_id, "status": "submitted"
                }])
                print(f"\n✅ 任务已提交，audienceId={audience_id}")
            return
        except json.JSONDecodeError as e:
            print(f"❌ groups-json解析失败: {e}")
            sys.exit(1)
    
    try:
        if args.a_tags:
            a_tags = parse_tags_input(args.a_tags)
        if args.b_tags:
            b_tags = parse_tags_input(args.b_tags)
        if args.a_audiences:
            a_audiences = parse_tags_input(args.a_audiences)  # 复用同样的整数解析逻辑
        if args.b_audiences:
            b_audiences = parse_tags_input(args.b_audiences)
    except Exception as e:
        print(f"❌ 规则解析失败: {e}")
        sys.exit(1)
    
    print(f"✅ A规则: {len(a_tags)}个标签, {len(a_audiences)}个人群包")
    print(f"✅ B规则: {len(b_tags)}个标签, {len(b_audiences)}个人群包")
    
    # 2. 确定拆分模式（基于标签数拆分，人群ID作为固定条件不参与拆分）
    print("\n[2/4] 确定拆分模式...")
    
    # 维度拆分判断：
    if args.split_mode == 'auto':
        if len(a_tags) == 1 and len(b_tags) > 1:
            split_mode = "one_to_many"
        elif len(b_tags) <= 1 and len(a_tags) > 1:
            split_mode = "many_to_one"
        elif len(a_tags) > 1 and len(b_tags) > 1:
            split_mode = "many_to_many"
        else:
            split_mode = "one_to_one"
    else:
        split_mode = args.split_mode  # 用户明确指定的模式
    
    # 如果一侧完全没有标签（只有人群ID），视为固定1个
    if not a_tags and a_audiences and b_tags:
        split_mode = "one_to_many"  # A固定（只有人群），B标签拆分
    elif not b_tags and b_audiences and a_tags:
        split_mode = "many_to_one"  # A标签拆分，B固定（只有人群）
    elif not a_tags and not b_tags and (a_audiences or b_audiences):
        split_mode = "one_to_one"  # 纯人群组合
    
    mode_names = {
        "many_to_one": "多对一（A拆分，B固定）",
        "one_to_many": "一对多（A固定，B拆分）",
        "many_to_many": "多对多（A拆分，B拆分）",
        "one_to_one": "一对一（都不需要拆分）"
    }
    print(f"✅ 拆分模式: {mode_names.get(split_mode, split_mode)}")
    if args.split_by_dimension:
        print(f"✅ 按维度拆分: 每个A标签分别创建独立任务")
    
    # 3. 拆分规则组
    print("\n[3/4] 拆分规则组...")
    
    # B规则拆分
    if not b_tags and b_audiences:
        # B只有人群没有标签，作为固定条件，不拆分
        b_groups = [{"group_no": 1, "tags": [], "count": 0}]
    elif split_mode in ("one_to_many", "many_to_many"):
        # 维度拆分：B侧每个标签单独一组（分别求交/笛卡尔积）
        b_groups = [{"group_no": i+1, "tags": [tag], "count": 1} for i, tag in enumerate(b_tags)]
    elif len(b_tags) > MAX_TAGS_PER_GROUP:
        # 超过50标签上限：按MAX_TAGS_PER_GROUP拆组（组内OR）
        b_groups = split_tags(b_tags, args.tags_per_group)
    else:
        b_groups = [{"group_no": 1, "tags": b_tags, "count": len(b_tags)}]
    
    # A规则拆分
    if not a_tags and a_audiences:
        # A只有人群没有标签，作为固定条件，不拆分
        a_groups = [{"group_no": 1, "tags": [], "count": 0}]
    elif split_mode in ("many_to_one", "many_to_many"):
        # 维度拆分：A侧每个标签单独一组
        a_groups = [{"group_no": i+1, "tags": [tag], "count": 1} for i, tag in enumerate(a_tags)]
    elif len(a_tags) > MAX_TAGS_PER_GROUP:
        # 超过50标签上限：按MAX_TAGS_PER_GROUP拆组（组内OR）
        a_groups = split_tags(a_tags, args.tags_per_group)
    else:
        a_groups = [{"group_no": 1, "tags": a_tags, "count": len(a_tags)}]
    
    print(f"✅ A规则拆分为{len(a_groups)}组")
    print(f"✅ B规则拆分为{len(b_groups)}组")
    
    # 4. 生成组合任务
    combinations = generate_combinations(
        a_groups, b_groups, split_mode,
        args.audience_name, args.suffix, args.logic,
        split_by_dimension=args.split_by_dimension,
        a_tags_original=a_tags,
        b_tags_original=b_tags,
        a_audiences=a_audiences,
        b_audiences=b_audiences
    )
    
    print(f"✅ 共生成{len(combinations)}个组合任务")
    
    # 查找鉴权脚本
    print("\n[4/4] 查找鉴权技能...")
    auth_script = find_auth_skill_path()
    
    if not auth_script:
        print("❌ 未找到鉴权技能，请先安装 mingdata-dmp-auth")
        sys.exit(1)
    
    print(f"✅ 鉴权技能路径: {auth_script}")
    
    # 生成项目ID
    project_id = generate_project_id()
    print(f"\n项目ID: {project_id}")
    print(f"人群包名: {args.audience_name}")
    print(f"后缀: {args.suffix}")
    print(f"A规则: {len(a_tags)}个标签 + {len(a_audiences)}个人群包")
    print(f"B规则: {len(b_tags)}个标签 + {len(b_audiences)}个人群包")
    
    brand_id_list = [b.strip() for b in args.brand_id.split(',') if b.strip()] if args.brand_id else []
    
    # 保存项目计划
    params = {
        "track_type": args.track_type,
        "id_types": args.id_types.split(','),
        "brandId": brand_id_list,
        "logic": args.logic,
        "a_tag_count": len(a_tags),
        "b_tag_count": len(b_tags),
        "a_audience_count": len(a_audiences),
        "b_audience_count": len(b_audiences)
    }
    
    plan_file = save_project_plan(
        project_id, args.audience_name, args.suffix,
        params, split_mode, combinations, args.output_dir
    )
    print(f"\n✅ 项目计划已保存: {plan_file}")
    
    # 创建任务
    print("\n创建组合人群任务...")
    
    # 确定批次范围
    MAX_BATCH = 5
    batch_size = min(args.batch_size, MAX_BATCH)
    
    if args.batch_start is not None and args.batch_end is not None:
        # 新用法：--batch-start/--batch-end 指定一批任务范围
        bs = max(1, args.batch_start)
        be = min(args.batch_end, len(combinations))
        if bs > be:
            print(f"❌ 无效的批次范围: {args.batch_start}-{args.batch_end}")
            sys.exit(1)
        if be - bs + 1 > MAX_BATCH:
            print(f"\n🔴 前置校验失败：每批最多创建{MAX_BATCH}个超限")
            print(f"   请拆分：--batch-start {bs} --batch-end {bs+MAX_BATCH} ...")
            print("\n---JSON_RESULT---")
            print(json.dumps({"status":"blocked","reason":"batch_size_exceeded","max_batch":MAX_BATCH}, ensure_ascii=False))
            sys.exit(1)
        # 使用已有项目ID（如果传入了）
        if args.project_id:
            project_id = args.project_id
            # 读取已有计划和状态
            plan_file = Path(args.output_dir) / project_id / "plan.json"
            status_file = Path(args.output_dir) / project_id / "status.json"
            if status_file.exists():
                with open(status_file) as f:
                    existing_status = json.load(f)
            else:
                existing_status = None
        combinations_to_create = combinations[bs-1:be]
        batch_info = f"批次任务{bs}~{be}（共{be-bs+1}个，本批最大并发{MAX_BATCH}）"
        is_new_project = False
        batch_start_idx = bs
        print(f"\n📌 创建{batch_info}")
        
    elif args.task_index is not None:
        # 兼容旧用法：--task-index 创建单个任务
        if args.task_index < 1 or args.task_index > len(combinations):
            print(f"❌ 无效的任务索引: {args.task_index}，有效范围: 1-{len(combinations)}")
            sys.exit(1)
        if args.project_id:
            project_id = args.project_id
            status_file = Path(args.output_dir) / project_id / "status.json"
            existing_status = json.loads(status_file.read_text()) if status_file.exists() else None
        combinations_to_create = [combinations[args.task_index - 1]]
        batch_info = f"单个任务{args.task_index}"
        is_new_project = False
        batch_start_idx = args.task_index
        print(f"\n📌 指定创建第 {args.task_index} 个任务（共 {len(combinations)} 个）")
        
    elif len(combinations) <= MAX_BATCH:
        # 总任务数≤5：全部直接创建
        combinations_to_create = combinations
        batch_info = f"全部{len(combinations)}个任务（≤{MAX_BATCH}，直接并发创建）"
        is_new_project = True
        batch_start_idx = 1
        existing_status = None
        print(f"\n📌 {batch_info}")
        
    else:
        # 🔴 任务数>5且未指定批次范围，拦截
        total_batches = (len(combinations) + MAX_BATCH) // MAX_BATCH
        print(f"\n🔴 前置校验失败：共 {len(combinations)} 个任务（超过{MAX_BATCH}个），必须分{total_batches}批创建")
        print(f"   正确用法（每批最多{MAX_BATCH}个并发创建，不需要等计算完成）:")
        for b in range(total_batches):
            s = b*MAX_BATCH
            e = min((b+1)*MAX_BATCH, len(combinations))
            print(f"   第{b+1}批：--batch-start {s} --batch-end {e} --project-id {project_id}")
        print("\n---JSON_RESULT---")
        print(json.dumps({
            "status": "blocked",
            "reason": "multi_task_requires_batch",
            "max_batch_size": MAX_BATCH,
            "total_tasks": len(combinations),
            "total_batches": total_batches,
            "suggested_batches": [
                {"batch": b+1, "start": b*MAX_BATCH, "end": min((b+1)*MAX_BATCH, len(combinations))}
                for b in range(total_batches)
            ],
            "message": f"任务数>{MAX_BATCH}，必须使用 --batch-start/--batch-end 分批创建（每批最多{MAX_BATCH}个并发，无需等计算完成）"
        }, ensure_ascii=False))
        sys.exit(1)
    
    created_tasks = []
    failed_tasks = []
    stopped_early = False
    
    # 确定本次创建在全局任务中的起始偏移
    start_offset = batch_start_idx - 1
    
    # 🔴 硬拦截：非新项目（推进下一批/重试）必须先检查cron锁文件
    if not is_new_project and args.project_id:
        cron_check = check_cron_setup(args.project_id, args.output_dir)
        if not cron_check["setup"]:
            print("\n" + "="*60)
            print("🔴 硬拦截：cron监控未设置，拒绝继续创建下一批")
            print("="*60)
            print("\n你必须先创建cron监控任务（不是exec background、不是命令行）：\n")
            # 生成cron参数供AI直接使用
            skill_dir = str(script_dir.parent)
            existing_aids = [t.get('audience_id') for t in (existing_status.get('tasks',[]) if existing_status else []) if t.get('status')=='success']
            cron_params = generate_cron_params_combine(args.project_id, existing_aids, skill_dir)
            cron_check["cron_params"] = cron_params
            print(json.dumps(cron_check, ensure_ascii=False, indent=2))
            print("\n创建cron后运行：python3 scripts/cron_helper.py --project-id", args.project_id, "mark-cron-set --cron-name", cron_params["name"])
            sys.exit(2)
    
    for i, combination in enumerate(combinations_to_create):
        actual_task_index = start_offset + i + 1
        print(f"\n  创建任务 {actual_task_index}/{len(combinations)}: {combination['task_name']}")
        
        response = create_combine_task(auth_script, params, combination)
        
        if response.get("code") == "0":
            audience_id = response.get("data", {}).get("audienceId")
            print(f"  ✅ 创建成功 - 任务ID: {audience_id}")
            created_tasks.append({
                "task_id": actual_task_index,
                "task_name": combination['task_name'],
                "audience_id": audience_id,
                "status": "success"
            })
        else:
            error_msg = response.get("msg", "未知错误")
            error_code = response.get("code", "unknown")
            print(f"  ❌ 创建失败: {error_msg}")
            
            failed_task = {
                "task_id": actual_task_index,
                "task_name": combination['task_name'],
                "error": error_msg,
                "error_code": error_code,
                "status": "failed",
                "a_tags": combination["a_tags"],
                "b_tags": combination["b_tags"],
                "logic": combination["logic"]
            }
            failed_tasks.append(failed_task)
            
            # 如果设置了 --stop-on-error，立即停止本批次
            if args.stop_on_error:
                print(f"\n⚠️ 创建失败，已停止本批次（--stop-on-error 模式）")
                print(f"   失败任务: {combination['task_name']}")
                print(f"   错误信息: {error_msg}")
                stopped_early = True
                break
    
    # 保存/更新项目状态
    tasks_status = created_tasks + failed_tasks
    
    if existing_status:
        # 追加到已有状态（批次模式）
        existing_aids = {t.get('audience_id') for t in existing_status.get('tasks', [])}
        for t in created_tasks:
            if t['audience_id'] not in existing_aids:
                existing_status['tasks'].append(t)
        for t in failed_tasks:
            existing_status['tasks'].append(t)
        all_tasks = existing_status['tasks']
        created_so_far = sum(1 for t in all_tasks if t.get('status') == 'success')
        failed_so_far = sum(1 for t in all_tasks if t.get('status') == 'failed')
        total = len(combinations)
        status = "completed" if (created_so_far + failed_so_far) >= total and not stopped_early else ("stopped" if stopped_early else "partial")
        existing_status['status'] = status
        existing_status['lastPollAt'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        flow_lock = existing_status.get('flow_lock', {})
        flow_lock['current_task_index'] = start_offset + len(created_tasks) + len(failed_tasks)
        flow_lock['total_tasks'] = total
        flow_lock['last_created_at'] = datetime.now().isoformat()
        flow_lock['last_status'] = status
        existing_status['flow_lock'] = flow_lock
        with open(status_file, 'w', encoding='utf-8') as f:
            json.dump(existing_status, f, ensure_ascii=False, indent=2)
        tasks_status = all_tasks
    else:
        # 新项目首次创建
        created_so_far = len(created_tasks)
        failed_so_far = len(failed_tasks)
        total = len(combinations)
        status = "completed" if not failed_tasks and not stopped_early and (start_offset + len(combinations_to_create)) >= total else ("stopped" if stopped_early else ("partial" if created_tasks else "failed"))
        flow_lock = {
            "current_task_index": start_offset + len(created_tasks) + len(failed_tasks),
            "total_tasks": total,
            "last_created_at": datetime.now().isoformat(),
            "last_status": status
        }
        save_project_status(project_id, status, tasks_status, args.output_dir, flow_lock)
    
    # 计算剩余未创建的任务
    all_created_ids = {t['task_id'] for t in (existing_status['tasks'] if existing_status else tasks_status) if t.get('status') == 'success'}
    all_failed_ids = {t['task_id'] for t in (existing_status['tasks'] if existing_status else tasks_status) if t.get('status') == 'failed'}
    pending_task_ids = [c['task_id'] for c in combinations if c['task_id'] not in all_created_ids and c['task_id'] not in all_failed_ids]
    pending_tasks = [c for c in combinations if c['task_id'] in pending_task_ids]
    
    # 输出结果
    print("\n" + "="*60)
    print("创建结果汇总")
    print("="*60)
    print(f"项目ID: {project_id}")
    print(f"人群包名: {args.audience_name}")
    print(f"拆分模式: {mode_names.get(split_mode, split_mode)}")
    print(f"A规则: {len(a_tags)}个标签 + {len(a_audiences)}个人群包")
    print(f"B规则: {len(b_tags)}个标签 + {len(b_audiences)}个人群包")
    print(f"总任务数: {len(combinations)}个")
    if args.batch_start is not None:
        print(f"本次批次: 任务{args.batch_start}~{args.batch_end}（共{len(combinations_to_create)}个）")
    elif args.task_index is not None:
        print(f"本次创建: 第 {args.task_index} 个任务")
    else:
        print(f"本次创建: 全部{len(combinations_to_create)}个任务（≤{MAX_BATCH}，逐个串行创建）")
    print(f"本批创建成功: {len(created_tasks)}个")
    print(f"本批创建失败: {len(failed_tasks)}个")
    
    total_created = sum(1 for t in tasks_status if t.get('status') == 'success')
    total_failed = sum(1 for t in tasks_status if t.get('status') == 'failed')
    print(f"累计进度: 已创建{total_created}个 / 失败{total_failed}个 / 待创建{len(pending_tasks)}个")
    
    if pending_tasks:
        next_start = total_created + total_failed + 1
        next_end = min(next_start + MAX_BATCH, len(combinations))
        print(f"\n⏳ 等待本批所有任务计算完成后，创建下一批（任务{next_start}~{next_end}）")
        print(f"   下一批命令：--batch-start {next_start} --batch-end {next_end} --project-id {project_id}")
    else:
        print(f"\n⏳ 这是最后一批，等待所有任务计算完成...")
    
    if created_tasks:
        print("\n本次创建成功:")
        for task in created_tasks:
            print(f"  - 任务{task['task_id']} {task['task_name']}: audienceId {task['audience_id']}")
    
    if failed_tasks:
        print("\n本次创建失败:")
        for task in failed_tasks:
            print(f"  - 任务{task['task_id']} {task['task_name']}: {task['error']}")
    
    print("="*60)
    
    # 输出第八步提示（只在成功创建任务时）
    if created_tasks and not stopped_early:
        print_step8_reminder(
            project_id=project_id,
            audience_name=args.audience_name,
            task_count=len(created_tasks)
        )
    
    # 输出JSON结果
    all_audience_ids = [t['audience_id'] for t in tasks_status if t.get('status') == 'success' and 'audience_id' in t]
    
    result = {
        "project_id": project_id,
        "audience_name": args.audience_name,
        "suffix": args.suffix,
        "split_mode": split_mode,
        "a_tag_count": len(a_tags),
        "b_tag_count": len(b_tags),
        "total_tasks": len(combinations),
        "max_batch_size": MAX_BATCH,
        "this_batch": {
            "batch_start": batch_start_idx,
            "batch_end": batch_start_idx + len(combinations_to_create) - 1,
            "created": len(created_tasks),
            "failed": len(failed_tasks)
        },
        "created_tasks": created_tasks,
        "failed_tasks": failed_tasks,
        "progress": {
            "created": total_created,
            "failed": total_failed,
            "pending": len(pending_tasks)
        },
        "all_audience_ids": all_audience_ids,
        "pending_batches": [],
        "stopped_early": stopped_early,
        "status": status,
        "plan_file": str(plan_file),
        "status_file": str(Path(args.output_dir) / project_id / "status.json")
    }
    
    # 生成剩余批次建议
    if pending_tasks:
        remaining_ids = [c['task_id'] for c in pending_tasks]
        batches = []
        for bi in range(0, len(remaining_ids), MAX_BATCH):
            batch_ids = remaining_ids[bi:bi+MAX_BATCH]
            batches.append({
                "batch": bi//MAX_BATCH + 2,  # 批次号（下一批）
                "start": batch_ids[0],
                "end": batch_ids[-1],
                "cmd": f"--batch-start {batch_ids[0]} --batch-end {batch_ids[-1]} --project-id {project_id}"
            })
        result["pending_batches"] = batches
    
    # 🔴 输出监控指令：所有批次提交完成后启动监控（不等计算完成）
    all_submitted = len(pending_tasks) == 0 and not stopped_early
    if created_tasks and not stopped_early:
        aid_list_str = ','.join(str(aid) for aid in all_audience_ids)
        skill_dir = str(script_dir.parent)
        
        # 🔴🔴🔴 强制使用cron工具的监控指令 🔴🔴🔴
        CRON_FORBIDDEN_WARN = (
            "🔴 严格禁止以下错误做法："
            "(1) 使用 exec(background=true)+sleep 轮询（session断连后AI无法被唤醒，会导致任务完成后不通知用户，已发生过故障）；"
            "(2) 使用 openclaw cron add 命令行（无法设置sessionTarget=current，监控无法触发）。"
            "必须使用 cron(action='add', job={...}) 工具，sessionTarget='current', delivery={'mode':'none'}。"
        )
        
        # 生成cron参数对象（供AI直接使用）
        cron_params = generate_cron_params_combine(project_id, all_audience_ids, skill_dir)
        result["requires_cron_setup"] = True
        result["cron_forbidden"] = CRON_FORBIDDEN_WARN
        result["cron_params"] = cron_params
        result["cron_setup_instructions"] = (
            f"🔴 你必须立即执行以下3步（不要跳过，不要用exec background轮询）：\n"
            f"1. 调用 cron(action='add', job=cron_params) 创建监控任务\n"
            f"2. 运行: python3 scripts/cron_helper.py --project-id {project_id} mark-cron-set --cron-name {cron_params['name']}\n"
            f"3. 告诉用户'监控已启动'\n"
            f"cron每60秒自动触发推进后续批次/通知结果，完成后会自动删除。"
        )
        
        if all_submitted:
            # 所有批次的任务都已提交创建（项目最后一批），启动全量监控
            result["monitor_instruction"] = {
                "action": "create_cron_monitor",
                "mandatory": True,
                "forbidden": CRON_FORBIDDEN_WARN,
                "tool": "cron",
                "when": "最后一批全部创建完成后立即启动",
                "description": "所有任务已提交DMP平台，启动cron定时监控（每60秒触发一次agent turn），等待计算完成",
                "cron_params": {
                    "action": "add",
                    "job": {
                        "name": f"DMP圈包监控-{project_id}",
                        "schedule": {"kind": "every", "everyMs": 60000},
                        "payload": {
                            "kind": "agentTurn",
                            "message": f"检查DMP圈包项目{project_id}的任务状态，audienceIds=[{aid_list_str}]，共{len(all_audience_ids)}个任务。运行 cd ~/.openclaw/skills/明日dmp批量圈包 && python3 scripts/poll_task_status.py {aid_list_str} --interval 60 --timeout 1800 查询状态。若所有任务audienceStatus=1（成功）或=0（失败）：完成第八步任务记录检查、汇总结果通知用户、调用cron(action='remove',...)删除本监控任务。若有失败按failureStrategy处理。"
                        },
                        "sessionTarget": "current",
                        "delivery": {"mode": "none"}
                    }
                },
                "note": "这是最后一批，创建阶段已全部完成，监控计算状态即可"
            }
        else:
            # 本批创建完成，但还有下一批 → 必须等本批全部计算完成才能创建下一批
            next_b = result["pending_batches"][0] if result["pending_batches"] else None
            this_batch_aids = [t['audience_id'] for t in created_tasks]
            this_batch_aid_str = ','.join(str(aid) for aid in this_batch_aids)
            if next_b:
                result["wait_batch_instruction"] = {
                    "action": "create_cron_monitor_wait_then_next",
                    "mandatory": True,
                    "forbidden": CRON_FORBIDDEN_WARN,
                    "tool": "cron",
                    "when": "本批所有任务创建API返回成功后立即启动cron监控",
                    "description": f"本批任务已逐个创建完成（{len(created_tasks)}个），必须等待这批所有任务计算完成（audienceStatus=1）才能创建下一批。禁止立即创建下一批！",
                    "cron_params": {
                        "action": "add",
                        "job": {
                            "name": f"DMP圈包监控-{project_id}-批{batch_start_idx//MAX_BATCH}",
                            "schedule": {"kind": "every", "everyMs": 60000},
                            "payload": {
                                "kind": "agentTurn",
                                "message": f"监控DMP圈包项目{project_id}，本批audienceIds=[{this_batch_aid_str}]。查询POST /audience/manage/taskList，等待所有任务audienceStatus=1或=0。全部成功后：通知用户本批完成，运行下一批命令 cd ~/.openclaw/skills/明日dmp批量圈包 && python3 scripts/create_combine_batch.py --project-id {project_id} --batch-start {next_b['start']} --batch-end {next_b['end']}，然后继续监控。如有失败按failureStrategy处理。全部批次完成后删除此cron任务。"
                            },
                            "sessionTarget": "current",
                            "delivery": {"mode": "none"}
                        }
                    },
                    "next_batch_cmd": f'cd ~/.openclaw/skills/明日dmp批量圈包 && python3 scripts/create_combine_batch.py --a-tags "{args.a_tags or ""}" --b-tags "{args.b_tags or ""}" --audience-name "{args.audience_name}" --suffix "{args.suffix}" --logic {args.logic} --track-type {args.track_type} --id-types "{args.id_types}" --split-mode {split_mode} --batch-start {next_b["start"]} --batch-end {next_b["end"]} --project-id {project_id}',
                    "forbidden": "禁止在本批任务未全部计算完成时创建下一批！禁止使用exec background轮询！"
                }
    
    print("="*60)
    
    # 输出第八步提示（所有任务都提交完成时）
    if created_tasks and all_submitted:
        print_step8_reminder(
            project_id=project_id,
            audience_name=args.audience_name,
            task_count=len(all_audience_ids)
        )
    
    print("\n---JSON_RESULT---")
    print(json.dumps(result, ensure_ascii=False))
    
    sys.exit(0 if status != "failed" else 1)

def run_retry_mode(args):
    """重试模式：只重新创建失败的任务"""
    print("\n" + "="*60)
    print("组合人群批量创建 - 重试失败任务")
    print("="*60)
    
    # 解析重试任务列表
    try:
        retry_data = json.loads(args.retry)
        failed_tasks = retry_data.get('failed_tasks', [])
    except json.JSONDecodeError as e:
        print(f"❌ 重试参数解析失败: {e}")
        sys.exit(1)
    
    if not failed_tasks:
        print("❌ 没有需要重试的任务")
        sys.exit(1)
    
    project_id = args.project_id or f"combine_retry_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    print(f"\n项目ID: {project_id}")
    print(f"待重试任务: {len(failed_tasks)}个")
    
    # 查找鉴权脚本
    auth_script = find_auth_skill_path()
    if not auth_script:
        print("❌ 未找到鉴权技能")
        sys.exit(1)
    
    # 从原项目读取参数
    original_project_dir = Path(args.output_dir) / (args.project_id or '')
    plan_file = original_project_dir / "plan.json"
    
    if plan_file.exists():
        with open(plan_file, 'r', encoding='utf-8') as f:
            plan = json.load(f)
        params = plan.get('params', {})
    else:
        # 如果没有原计划文件，使用命令行参数
        params = {
            "track_type": args.track_type,
            "id_types": args.id_types.split(',') if args.id_types else [],
            "logic": args.logic
        }
    
    # 重试创建
    retried_tasks = []
    still_failed = []
    
    for task in failed_tasks:
        task_name = task.get('task_name', '')
        task_id = task.get('task_id', 0)
        a_tags = task.get('a_tags', [])
        b_tags = task.get('b_tags', [])
        logic = task.get('logic', 'and')
        
        print(f"\n  重试任务 {task_id}: {task_name}")
        
        if not a_tags and not b_tags:
            print(f"  ⚠️ 缺少标签信息，跳过")
            still_failed.append({
                **task,
                "error": "缺少标签信息，无法重试",
                "retry_status": "skipped"
            })
            continue
        
        # 构建重试任务
        combination = {
            "task_id": task_id,
            "task_name": task_name,
            "a_tags": a_tags,
            "b_tags": b_tags,
            "logic": logic
        }
        
        response = create_combine_task(auth_script, params, combination)
        
        if response.get("code") == "0":
            audience_id = response.get("data", {}).get("audienceId")
            print(f"  ✅ 重试成功 - 任务ID: {audience_id}")
            retried_tasks.append({
                "task_id": task_id,
                "task_name": task_name,
                "audience_id": audience_id,
                "status": "success",
                "retry_status": "success"
            })
        else:
            error_msg = response.get("msg", "未知错误")
            print(f"  ❌ 重试失败: {error_msg}")
            still_failed.append({
                **task,
                "error": error_msg,
                "retry_status": "failed"
            })
    
    # 输出重试结果
    print("\n" + "="*60)
    print("重试结果汇总")
    print("="*60)
    print(f"重试任务数: {len(failed_tasks)}个")
    print(f"重试成功: {len(retried_tasks)}个")
    print(f"仍然失败: {len(still_failed)}个")
    
    if retried_tasks:
        print("\n重试成功的任务:")
        for task in retried_tasks:
            print(f"  - {task['task_name']}: 任务ID {task['audience_id']}")
    
    if still_failed:
        print("\n仍然失败的任务:")
        for task in still_failed:
            print(f"  - {task['task_name']}: {task['error']}")
    
    print("="*60)
    
    # 输出JSON结果
    result = {
        "project_id": project_id,
        "original_project_id": args.project_id,
        "retry_mode": True,
        "retried_tasks": retried_tasks,
        "still_failed": still_failed,
        "retry_success": len(retried_tasks),
        "retry_failed": len(still_failed)
    }
    
    print("\n---JSON_RESULT---")
    print(json.dumps(result, ensure_ascii=False))
    
    sys.exit(0 if not still_failed else 1)

if __name__ == "__main__":
    main()
