#!/usr/bin/env python3
"""
轮询批量任务结果
配合 batch_generate.py 使用
"""
import sys
import json
import argparse
import time
from digen_ai_client import DigenAIClient


def main():
    parser = argparse.ArgumentParser(description="DigenAI 批量结果轮询")
    parser.add_argument("token", help="DIGEN_TOKEN")
    parser.add_argument("session_id", help="DIGEN_SESSION_ID")
    parser.add_argument("input", help="batch_generate.py 生成的任务文件")
    parser.add_argument("--timeout", "-t", type=int, default=120,
                        help="单任务超时(秒)")
    parser.add_argument("--interval", "-i", type=int, default=3,
                        help="轮询间隔(秒)")
    parser.add_argument("--output", "-o", default="batch_results_final.json",
                        help="最终结果输出文件")
    
    args = parser.parse_args()
    
    # 加载任务列表
    with open(args.input, "r") as f:
        tasks = json.load(f)
    
    client = DigenAIClient(token=args.token, session_id=args.session_id)
    
    pending = [t for t in tasks if t.get("success") and t.get("task_id")]
    completed = []
    
    print(f"开始轮询 {len(pending)} 个任务...")
    
    while pending:
        still_pending = []
        
        for task in pending:
            task_id = task["task_id"]
            print(f"检查 {task_id[:20]}...", end=" ")
            
            result = client.get_image_status(task_id)
            
            if result["success"]:
                status = result["status"]
                if status == 4:  # 完成
                    task["images"] = result["images"]
                    task["finished"] = True
                    completed.append(task)
                    print(f"完成! URL: {result['images'][0][:50]}...")
                elif status == 5:  # 失败
                    task["finished"] = True
                    task["error"] = "Generation failed"
                    completed.append(task)
                    print("失败")
                else:
                    still_pending.append(task)
                    print(f"进行中 (status={status})")
            else:
                still_pending.append(task)
                print(f"查询失败: {result.get('error')}")
        
        if still_pending:
            print(f"\n等待 {len(still_pending)} 个任务完成...")
            time.sleep(args.interval)
            pending = still_pending
        else:
            pending = []
    
    # 保存最终结果
    with open(args.output, "w") as f:
        json.dump(completed, f, indent=2)
    
    success_count = len([t for t in completed if t.get("images")])
    print(f"\n完成! 成功 {success_count}/{len(completed)}")
    print(f"结果保存到 {args.output}")


if __name__ == "__main__":
    main()
