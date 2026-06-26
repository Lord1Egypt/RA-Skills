#!/usr/bin/env python3
"""列出微云文件"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime

API_BASE = "https://api.weiyun.com/v1"

def list_files(path: str = "/") -> dict:
    """列出目录内容
    
    Args:
        path: 目录路径
    
    Returns:
        API 响应
    """
    access_token = os.environ.get("WEIYUN_ACCESS_TOKEN")
    if not access_token:
        raise ValueError("未设置 WEIYUN_ACCESS_TOKEN 环境变量")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    params = {
        "path": path
    }
    
    resp = requests.get(f"{API_BASE}/files", headers=headers, params=params)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    file_list = data.get("files", [])
    if not file_list:
        return "目录为空"
    
    output = f"## 文件列表（共 {len(file_list)} 个）\n\n"
    output += "| 类型 | 文件名 | 大小 | 修改时间 |\n"
    output += "|------|--------|------|----------|\n"
    
    for item in file_list:
        is_dir = "📁" if item.get("is_dir") else "📄"
        name = item.get("name", "-")
        size = item.get("size", 0)
        mtime = item.get("mtime", 0)
        
        # 格式化大小
        if size < 1024:
            size_str = f"{size} B"
        elif size < 1024 * 1024:
            size_str = f"{size / 1024:.1f} KB"
        elif size < 1024 * 1024 * 1024:
            size_str = f"{size / (1024 * 1024):.1f} MB"
        else:
            size_str = f"{size / (1024 * 1024 * 1024):.1f} GB"
        
        # 格式化时间
        mtime_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M") if mtime else "-"
        
        output += f"| {is_dir} | {name} | {size_str} | {mtime_str} |\n"
    
    return output

def main():
    parser = argparse.ArgumentParser(description="列出微云文件")
    parser.add_argument("--path", default="/", help="目录路径")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = list_files(args.path)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"获取失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
