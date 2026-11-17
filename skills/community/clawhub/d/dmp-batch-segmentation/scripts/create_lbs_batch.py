#!/usr/bin/env python3
"""
LBS批量圈选创建脚本
功能：根据坐标文件批量创建LBS规则人群任务
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

# 导入坐标校验模块
from validate_coordinates import validate_coordinate_file

# 导入任务记录检查模块
from check_task_logger import print_step8_reminder

# 常量
MAX_COORDINATES_PER_TASK = 200  # 单次最多200个坐标

def generate_project_id():
    """生成项目ID"""
    return f"lbs_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def split_coordinates(coordinates, batch_size=MAX_COORDINATES_PER_TASK):
    """
    将坐标列表拆分成多个批次
    
    Args:
        coordinates: 坐标列表
        batch_size: 每批次坐标数
        
    Returns:
        list: 批次列表
    """
    batches = []
    total = len(coordinates)
    batch_count = math.ceil(total / batch_size)
    
    for i in range(batch_count):
        start = i * batch_size
        end = min((i + 1) * batch_size, total)
        batches.append({
            "batch_no": i + 1,
            "coordinates": coordinates[start:end],
            "count": end - start
        })
    
    return batches

def create_lbs_task(auth_script, params, batch_coords, task_name):
    """
    创建单个LBS任务
    
    Args:
        auth_script: 鉴权脚本路径
        params: 任务参数
        batch_coords: 批次坐标列表
        task_name: 任务名称
        
    Returns:
        dict: API响应
    """
    # 构建data数组
    data = []
    for coord in batch_coords:
        data.append({
            "drawMode": "batch",
            "dataOrigin": params["crowd_type"],
            "startTime": params.get("start_time", ""),
            "endTime": params.get("end_time", ""),
            "center": {
                "lng": coord["lng"],
                "lat": coord["lat"],
                "radius": str(params["radius"])
            }
        })
    
    api_params = {
        "name": task_name,
        "trackType": params["track_type"],
        "idTypes": params["id_types"],
        "brandId": params.get("brandId", []) or [],
        "data": data
    }
    
    # 调用API
    import subprocess
    cmd = [
        sys.executable, str(auth_script),
        "--endpoint", "/api/open-api/audience/rule/create/lbs",
        "--method", "POST",
        "--params", json.dumps(api_params, ensure_ascii=False)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    try:
        response = json.loads(result.stdout)
        return response
    except json.JSONDecodeError:
        return {"code": "1", "msg": f"API调用失败: {result.stdout}"}

def save_project_plan(project_id, audience_name, suffix, params, batches, output_dir="data/plans"):
    """保存项目计划"""
    project_dir = Path(output_dir) / project_id
    project_dir.mkdir(parents=True, exist_ok=True)
    
    plan = {
        "projectId": project_id,
        "audienceName": audience_name,
        "suffix": suffix,
        "scenario": "LBS_BATCH",
        "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "params": params,
        "totalCoordinates": sum(b["count"] for b in batches),
        "batchSize": MAX_COORDINATES_PER_TASK,
        "totalBatches": len(batches),
        "batches": [
            {
                "batchNo": b["batch_no"],
                "taskName": f"{audience_name}{suffix}{b['batch_no']}",
                "coordinateCount": b["count"]
            }
            for b in batches
        ]
    }
    
    plan_file = project_dir / "plan.json"
    with open(plan_file, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    
    return plan_file

def save_project_status(project_id, status, batches_status, output_dir="data/plans"):
    """保存项目状态"""
    project_dir = Path(output_dir) / project_id
    
    status_data = {
        "projectId": project_id,
        "status": status,
        "currentBatch": 1,
        "batches": batches_status,
        "lastPollAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    status_file = project_dir / "status.json"
    with open(status_file, 'w', encoding='utf-8') as f:
        json.dump(status_data, f, ensure_ascii=False, indent=2)
    
    return status_file

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='LBS批量圈选创建')
    parser.add_argument('--coordinate-file', help='坐标文件路径')
    parser.add_argument('--audience-name', help='人群包名')
    parser.add_argument('--suffix', default='_批次', help='后缀')
    parser.add_argument('--radius', type=int, help='辐射范围(米)')
    parser.add_argument('--crowd-type', help='人群类型(recentArrive/homeAddress/workAddress)')
    parser.add_argument('--start-time', help='开始时间(选择recentArrive时必填)')
    parser.add_argument('--end-time', help='结束时间(选择recentArrive时必填)')
    parser.add_argument('--track-type', default='MOBILE', help='平台类型')
    parser.add_argument('--id-types', help='ID类型(逗号分隔)')
    parser.add_argument('--batch-size', type=int, default=6, help='每批创建任务数')
    parser.add_argument('--output-dir', default='data/plans', help='输出目录')
    # 重试相关参数
    parser.add_argument('--retry', help='重试模式: JSON格式失败任务列表')
    parser.add_argument('--project-id', help='重试时关联的原项目ID')
    parser.add_argument('--stop-on-error', action='store_true', 
                        help='创建失败时立即停止（用于AI助手询问用户）')
    parser.add_argument('--brand-id', default='', help='品牌ID列表(逗号分隔，可选；不传/空=全部品牌)')
    
    args = parser.parse_args()
    
    # 重试模式
    if args.retry:
        run_retry_mode(args)
        return
    
    # 正常模式：检查必填参数
    required = ['coordinate_file', 'audience_name', 'radius', 'crowd_type', 'id_types']
    for param in required:
        if not getattr(args, param):
            print(f"❌ 缺少必填参数: --{param.replace('_', '-')}")
            sys.exit(1)
    
    print("\n" + "="*60)
    print("LBS批量圈选创建")
    print("="*60)
    
    # 1. 校验坐标文件
    print("\n[1/4] 校验坐标文件...")
    coord_result = validate_coordinate_file(args.coordinate_file)
    
    if not coord_result["is_valid"]:
        print(f"❌ 坐标文件校验失败: {coord_result['error_msg']}")
        sys.exit(1)
    
    print(f"✅ 坐标文件校验通过，共{coord_result['total_count']}个坐标")
    
    # 2. 查找鉴权脚本
    print("\n[2/4] 查找鉴权技能...")
    auth_script = find_auth_skill_path()
    
    if not auth_script:
        print("❌ 未找到鉴权技能，请先安装 mingdata-dmp-auth")
        sys.exit(1)
    
    print(f"✅ 鉴权技能路径: {auth_script}")
    
    # 3. 拆分坐标
    print("\n[3/4] 拆分坐标批次...")
    batches = split_coordinates(coord_result["coordinates"])
    print(f"✅ 共拆分为{len(batches)}个批次")
    
    # 4. 生成项目ID
    project_id = generate_project_id()
    print(f"\n项目ID: {project_id}")
    print(f"人群包名: {args.audience_name}")
    print(f"后缀: {args.suffix}")
    
    # 保存项目计划
    brand_id_list = [b.strip() for b in args.brand_id.split(',') if b.strip()] if args.brand_id else []
    params = {
        "radius": args.radius,
        "crowd_type": args.crowd_type,
        "start_time": args.start_time or "",
        "end_time": args.end_time or "",
        "track_type": args.track_type,
        "id_types": args.id_types.split(','),
        "brandId": brand_id_list
    }
    
    plan_file = save_project_plan(
        project_id, args.audience_name, args.suffix,
        params, batches, args.output_dir
    )
    print(f"\n✅ 项目计划已保存: {plan_file}")
    
    # 🔴 硬拦截：任务数>1时，强制要求使用 --task-index 分批创建
    if len(batches) > 1 and args.task_index is None:
        print(f"\n🔴 前置校验失败：共 {len(batches)} 个任务，必须使用 --task-index 分批创建")
        print(f"   正确用法：python create_lbs_batch.py --task-index 1 ...")
        print(f"   等待任务1成功后：python create_lbs_batch.py --task-index 2 ...")
        print("\n---JSON_RESULT---")
        print(json.dumps({
            "status": "blocked",
            "reason": "multi_task_requires_index",
            "total_tasks": len(batches),
            "message": "任务数>1，必须使用 --task-index 分批创建"
        }, ensure_ascii=False))
        sys.exit(1)
    
    # 5. 创建任务
    print("\n[4/4] 创建LBS任务...")
    
    # 🔴 前置校验：检查凭证和鉴权技能
    from preflight_check import check_create_first
    preflight = check_create_first(project_id)
    if preflight["status"] == "error":
        print(f"\n🔴 前置校验失败，禁止创建任务")
        for blocker in preflight.get("blockers", []):
            print(f"   ❌ {blocker}")
        print("\n---JSON_RESULT---")
        print(json.dumps({"status": "blocked", "reason": "preflight_failed", "details": preflight}, ensure_ascii=False))
        sys.exit(1)
    print(f"✅ 前置校验通过: {preflight['message']}")
    
    created_tasks = []
    failed_tasks = []
    pending_tasks = []
    stopped_early = False
    
    for i, batch in enumerate(batches):
        task_name = f"{args.audience_name}{args.suffix}{batch['batch_no']}"
        print(f"\n  创建任务 {batch['batch_no']}/{len(batches)}: {task_name}")
        
        response = create_lbs_task(auth_script, params, batch["coordinates"], task_name)
        
        if response.get("code") == "0":
            audience_id = response.get("data", {}).get("audienceId")
            print(f"  ✅ 创建成功 - 任务ID: {audience_id}")
            created_tasks.append({
                "batch_no": batch["batch_no"],
                "task_name": task_name,
                "audience_id": audience_id,
                "status": "success"
            })
        else:
            error_msg = response.get("msg", "未知错误")
            error_code = response.get("code", "unknown")
            print(f"  ❌ 创建失败: {error_msg}")
            failed_task = {
                "batch_no": batch["batch_no"],
                "task_name": task_name,
                "error": error_msg,
                "error_code": error_code,
                "status": "failed",
                "coordinates": batch["coordinates"]  # 保存坐标以便重试
            }
            failed_tasks.append(failed_task)
            
            # --stop-on-error 模式：失败时立即停止
            if args.stop_on_error:
                stopped_early = True
                print(f"\n⚠️ 创建失败，已停止（--stop-on-error 模式）")
                print(f"   失败任务: {task_name}")
                print(f"   失败原因: {error_msg}")
                # 记录剩余待处理任务
                pending_tasks = batches[i+1:]
                break
        
        # 批次控制
        if (i + 1) % args.batch_size == 0 and i + 1 < len(batches):
            print(f"\n  ⏸️ 已创建{args.batch_size}个任务，等待确认后继续...")
            # 这里可以添加用户确认逻辑
    
    # 保存项目状态
    batches_status = created_tasks + failed_tasks
    if stopped_early:
        status = "stopped"
    else:
        status = "completed" if not failed_tasks else ("partial" if created_tasks else "failed")
    status_file = save_project_status(project_id, status, batches_status, args.output_dir)
    
    # 输出结果
    print("\n" + "="*60)
    print("创建结果汇总")
    print("="*60)
    print(f"项目ID: {project_id}")
    print(f"人群包名: {args.audience_name}")
    print(f"总坐标数: {coord_result['total_count']}个")
    print(f"总批次数: {len(batches)}个")
    print(f"成功: {len(created_tasks)}个")
    print(f"失败: {len(failed_tasks)}个")
    if stopped_early:
        print(f"待处理: {len(pending_tasks)}个（因失败停止）")
    
    if created_tasks:
        print("\n已创建任务:")
        for task in created_tasks:
            print(f"  - {task['task_name']}: 任务ID {task['audience_id']}")
    
    if failed_tasks:
        print("\n失败任务:")
        for task in failed_tasks:
            print(f"  - {task['task_name']}: {task['error']}")
    
    print("="*60)
    
    # 输出第八步提示
    if created_tasks:
        print_step8_reminder(
            project_id=project_id,
            audience_name=args.audience_name,
            task_count=len(created_tasks)
        )
    
    # 输出JSON结果
    result = {
        "project_id": project_id,
        "audience_name": args.audience_name,
        "suffix": args.suffix,
        "total_coordinates": coord_result["total_count"],
        "total_batches": len(batches),
        "created_tasks": created_tasks,
        "failed_tasks": failed_tasks,
        "pending_tasks": pending_tasks if stopped_early else [],
        "stopped_early": stopped_early,
        "status": status,
        "plan_file": str(plan_file),
        "status_file": str(status_file)
    }
    
    print("\n---JSON_RESULT---")
    print(json.dumps(result, ensure_ascii=False))
    
    sys.exit(0 if status != "failed" else 1)

def run_retry_mode(args):
    """重试模式：只重新创建失败的任务"""
    print("\n" + "="*60)
    print("LBS批量圈选 - 重试失败任务")
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
    
    project_id = args.project_id or f"lbs_retry_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
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
            "radius": args.radius,
            "crowd_type": args.crowd_type,
            "start_time": args.start_time or "",
            "end_time": args.end_time or "",
            "track_type": args.track_type,
            "id_types": args.id_types.split(',') if args.id_types else []
        }
    
    # 重试创建
    retried_tasks = []
    still_failed = []
    
    for task in failed_tasks:
        task_name = task.get('task_name', '')
        batch_no = task.get('batch_no', 0)
        coordinates = task.get('coordinates', [])
        
        print(f"\n  重试任务 {batch_no}: {task_name}")
        
        if not coordinates:
            print(f"  ⚠️ 缺少坐标信息，跳过")
            still_failed.append({
                **task,
                "error": "缺少坐标信息，无法重试",
                "retry_status": "skipped"
            })
            continue
        
        response = create_lbs_task(auth_script, params, coordinates, task_name)
        
        if response.get("code") == "0":
            audience_id = response.get("data", {}).get("audienceId")
            print(f"  ✅ 重试成功 - 任务ID: {audience_id}")
            retried_tasks.append({
                "batch_no": batch_no,
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
