#!/usr/bin/env python3
"""
Zeelin Deep Research - Submit Research Task
提交深度研究任务，返回task_id用于后续查询
"""

import argparse
import json
import os
import requests
import sys

API_BASE_URL = "https://desearch.zeelin.cn/api"

def submit_research(query: str, mode: str = "deep", api_key: str = None, **kwargs) -> dict:
    """提交深度研究任务"""
    
    # 获取API Key
    if not api_key:
        api_key = os.environ.get("ZEELIN_API_KEY")
        if not api_key:
            # 尝试从配置文件读取
            config_path = os.path.expanduser("~/.openclaw/zeelin-config.json")
            if os.path.exists(config_path):
                with open(config_path) as f:
                    config = json.load(f)
                    api_key = config.get("api_key")
    
    if not api_key:
        raise ValueError("请设置ZEELIN_API_KEY环境变量或配置文件")
    
    url = f"{API_BASE_URL}/deep-research/submit"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": query,
        "mode": mode,
        **kwargs
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    return response.json()


def main():
    parser = argparse.ArgumentParser(description="提交Zeelin深度研究任务")
    parser.add_argument("--query", "-q", required=True, help="研究主题")
    parser.add_argument("--mode", "-m", default="deep", 
                       choices=["basic", "deep", "industry", "expert"],
                       help="研究模式")
    parser.add_argument("--api-key", help="API Key (可选，默认从环境变量读取)")
    parser.add_argument("--output", "-o", help="保存任务ID到文件")
    
    args = parser.parse_args()
    
    try:
        result = submit_research(args.query, args.mode, args.api_key)
        
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        # 保存task_id到文件
        if args.output:
            task_id = result.get("data", {}).get("task_id")
            if task_id:
                with open(args.output, "w") as f:
                    f.write(task_id)
                print(f"\n任务ID已保存到: {args.output}")
        
        # 输出task_id
        task_id = result.get("data", {}).get("task_id")
        if task_id:
            print(f"\n任务ID: {task_id}")
            print(f"查询状态: python3 scripts/check_status.py --task-id {task_id}")
        
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
