#!/usr/bin/env python3
"""
任务状态轮询脚本
功能：后台定期检查任务状态，完成后输出结果

使用方式：
    python poll_task_status.py <audienceId1> [audienceId2] ... [--interval 60] [--timeout 1800]

参数说明：
    audienceId: 人群任务ID（可以查询多个）
    --interval: 轮询间隔（秒），默认60秒
    --timeout: 超时时间（秒），默认1800秒（30分钟）

示例：
    python poll_task_status.py 135404 --interval 60
    python poll_task_status.py 135404 135405 --interval 30 --timeout 3600
"""

import sys
import json
import time
import os
from pathlib import Path
from datetime import datetime

def find_auth_skill_path():
    """查找鉴权技能的API脚本路径"""
    possible_paths = [
        Path.home() / ".skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        Path.home() / ".openclaw" / "workspace" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
        Path.home() / ".openclaw" / "skills" / "mingdata-dmp-auth" / "scripts" / "minri_dmp_api.py",
    ]
    for path in possible_paths:
        if path.exists():
            return path
    return None

def query_task_status(audience_ids):
    """查询任务状态"""
    auth_path = find_auth_skill_path()
    if not auth_path:
        return {"error": "找不到鉴权技能"}
    
    # 添加鉴权技能路径到sys.path
    sys.path.insert(0, str(auth_path.parent))
    
    try:
        from minri_dmp_api import call_api
        
        request_body = {"audienceIds": audience_ids}
        
        # 捕获stdout输出
        import io
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        try:
            with redirect_stdout(f):
                call_api("/audience/manage/taskList", request_body)
            output = f.getvalue()
            return json.loads(output)
        except SystemExit:
            # call_api可能调用sys.exit
            output = f.getvalue()
            if output:
                try:
                    return json.loads(output)
                except:
                    return {"error": "解析响应失败", "raw": output}
            return {"error": "API调用失败"}
    except Exception as e:
        return {"error": str(e)}

def parse_args(args):
    """解析命令行参数"""
    audience_ids = []
    interval = 60  # 默认60秒
    timeout = 1800  # 默认30分钟
    
    i = 0
    while i < len(args):
        if args[i] == "--interval" and i + 1 < len(args):
            interval = int(args[i + 1])
            i += 2
        elif args[i] == "--timeout" and i + 1 < len(args):
            timeout = int(args[i + 1])
            i += 2
        else:
            try:
                audience_ids.append(int(args[i]))
            except ValueError:
                pass
            i += 1
    
    return audience_ids, interval, timeout

def main():
    if len(sys.argv) < 2:
        print("用法: python poll_task_status.py <audienceId1> [audienceId2] ... [--interval 60] [--timeout 1800]")
        sys.exit(1)
    
    audience_ids, interval, timeout = parse_args(sys.argv[1:])
    
    if not audience_ids:
        print("错误: 请提供至少一个任务ID")
        sys.exit(1)
    
    print(f"🔄 开始轮询任务状态")
    print(f"   任务ID: {audience_ids}")
    print(f"   轮询间隔: {interval}秒")
    print(f"   超时时间: {timeout}秒")
    print(f"   开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    start_time = time.time()
    completed_tasks = {}
    
    while True:
        elapsed = time.time() - start_time
        
        # 检查超时
        if elapsed > timeout:
            print(f"\n⏰ 轮询超时（{timeout}秒）")
            print(f"未完成的任务: {[aid for aid in audience_ids if aid not in completed_tasks]}")
            break
        
        # 查询任务状态
        result = query_task_status(audience_ids)
        
        if "error" in result:
            print(f"\n❌ 查询失败: {result['error']}")
            print(f"   等待{interval}秒后重试...")
            time.sleep(interval)
            continue
        
        # 解析响应
        if result.get("code") == "0" and "data" in result:
            tasks = result["data"]
            
            all_completed = True
            for task in tasks:
                task_id = task.get("audienceId")
                status = task.get("audienceStatus")
                name = task.get("audienceName", "未知")
                amount = task.get("audienceAmount", "未知")
                
                # 状态: 0=失败, 1=成功, 2=等待中, 3=计算中
                status_map = {0: "❌ 失败", 1: "✅ 成功", 2: "⏳ 等待中", 3: "🔄 计算中"}
                status_text = status_map.get(status, f"未知({status})")
                
                if task_id not in completed_tasks:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] 任务 {task_id} ({name}): {status_text}")
                    
                    if status == 1:  # 成功
                        completed_tasks[task_id] = {
                            "name": name,
                            "amount": amount,
                            "status": "成功"
                        }
                        print(f"   ✅ 任务完成！人群规模: {amount}")
                    elif status == 0:  # 失败
                        completed_tasks[task_id] = {
                            "name": name,
                            "status": "失败"
                        }
                        print(f"   ❌ 任务失败")
                    else:
                        all_completed = False
                else:
                    # 已完成的不再检查
                    pass
            
            # 检查是否所有任务都完成
            if len(completed_tasks) == len(audience_ids):
                print("\n" + "=" * 50)
                print("🎉 所有任务已完成！")
                print("=" * 50)
                print("\n任务汇总:")
                for task_id, info in completed_tasks.items():
                    print(f"  - 任务ID: {task_id}")
                    print(f"    名称: {info['name']}")
                    print(f"    状态: {info['status']}")
                    if info['status'] == '成功':
                        print(f"    人群规模: {info['amount']}")
                print("=" * 50)
                break
        else:
            print(f"\n⚠️ 响应格式异常: {result}")
        
        # 等待下一次轮询
        time.sleep(interval)

if __name__ == "__main__":
    main()
