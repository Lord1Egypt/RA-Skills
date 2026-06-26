#!/usr/bin/env python3
"""
Zeelin Deep Research - Check Task Status
检查任务状态，支持轮询模式
"""

import argparse
import json
import os
import sys
import time
import requests
from datetime import datetime

API_BASE_URL = "https://desearch.zeelin.cn/api"

# 任务状态
STATUS_PENDING = "pending"
STATUS_PROCESSING = "processing"
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"


def check_status(task_id: str, api_key: str = None) -> dict:
    """检查任务状态"""
    
    if not api_key:
        api_key = os.environ.get("ZEELIN_API_KEY")
        if not api_key:
            config_path = os.path.expanduser("~/.openclaw/zeelin-config.json")
            if os.path.exists(config_path):
                with open(config_path) as f:
                    config = json.load(f)
                    api_key = config.get("api_key")
    
    if not api_key:
        raise ValueError("请设置ZEELIN_API_KEY环境变量或配置文件")
    
    url = f"{API_BASE_URL}/deep-research/status/{task_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json()


def wait_for_completion(
    task_id: str,
    interval: int = 30,
    timeout: int = 3600,
    api_key: str = None,
    on_progress: callable = None
) -> dict:
    """
    等待任务完成（轮询模式）
    
    Args:
        task_id: 任务ID
        interval: 检查间隔（秒）
        timeout: 超时时间（秒）
        api_key: API Key
        on_progress: 进度回调函数
    
    Returns:
        任务结果
    """
    start_time = time.time()
    last_status = None
    
    print(f"开始监控任务: {task_id}")
    print(f"检查间隔: {interval}秒, 超时时间: {timeout}秒")
    print("-" * 50)
    
    while True:
        # 检查超时
        elapsed = time.time() - start_time
        if elapsed > timeout:
            raise TimeoutError(f"任务超时 ({timeout}秒)")
        
        try:
            result = check_status(task_id, api_key)
            data = result.get("data", {})
            status = data.get("status", STATUS_PENDING)
            
            # 状态变化时打印
            if status != last_status:
                last_status = status
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 状态: {status}")
            
            # 进度回调
            if on_progress:
                on_progress(status, data)
            
            # 任务完成
            if status == STATUS_COMPLETED:
                print("-" * 50)
                print("任务完成!")
                return data
            
            # 任务失败
            if status == STATUS_FAILED:
                error = data.get("error", "未知错误")
                raise RuntimeError(f"任务失败: {error}")
            
            # 等待下次检查
            time.sleep(interval)
            
        except requests.exceptions.RequestException as e:
            print(f"网络错误: {e}, 5秒后重试...")
            time.sleep(5)


def main():
    parser = argparse.ArgumentParser(description="检查Zeelin深度研究任务状态")
    parser.add_argument("--task-id", "-t", required=True, help="任务ID")
    parser.add_argument("--api-key", help="API Key")
    parser.add_argument("--interval", "-i", type=int, default=30, help="检查间隔(秒)")
    parser.add_argument("--timeout", "-o", type=int, default=3600, help="超时时间(秒)")
    parser.add_argument("--watch", "-w", action="store_true", help="持续监控直到完成")
    parser.add_argument("--output", help="结果保存到文件")
    
    args = parser.parse_args()
    
    try:
        if args.watch:
            # 轮询模式
            result = wait_for_completion(
                args.task_id,
                interval=args.interval,
                timeout=args.timeout,
                api_key=args.api_key
            )
            
            # 保存结果
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f"\n结果已保存到: {args.output}")
            
            # 打印结果
            print("\n" + "=" * 50)
            print("研究结果:")
            print("=" * 50)
            content = result.get("content", "")
            print(content[:5000] if content else "无内容")
            
        else:
            # 单次查询
            result = check_status(args.task_id, args.api_key)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
            # 保存到文件
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                print(f"\n结果已保存到: {args.output}")
    
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
