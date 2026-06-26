#!/usr/bin/env python3
"""列出百度网盘文件"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime

API_BASE = "https://pan.baidu.com/rest/2.0/xpan/file"

def list_files(path: str = "/", order: str = "time", desc: bool = True) -> dict:
    """列出目录内容
    
    Args:
        path: 目录路径
        order: 排序方式（time, name, size）
        desc: 是否降序
    
    Returns:
        API 响应
    """
    access_token = os.environ.get("BAIDU_PAN_ACCESS_TOKEN")
    if not access_token:
        raise ValueError("未设置 BAIDU_PAN_ACCESS_TOKEN 环境变量")
    
    params = {
        "method": "list",
        "access_token": access_token,
        "dir": path,
        "order": order,  # time, name, size
        "desc": 1 if desc else 0,
        "web": 1
    }
    
    resp = requests.get(API_BASE, params=params)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    file_list = data.get("list", [])
    if not file_list:
        return "目录为空"
    
    output = f"## 文件列表（共 {len(file_list)} 个）\n\n"
    output += "| 类型 | 文件名 | 大小 | 修改时间 |\n"
    output += "|------|--------|------|----------|\n"
    
    for item in file_list:
        is_dir = "📁" if item.get("isdir") else "📄"
        name = item.get("server_filename", "-")
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
    parser = argparse.ArgumentParser(description="列出百度网盘文件")
    parser.add_argument("--path", default="/", help="目录路径")
    parser.add_argument("--order", choices=["time", "name", "size"], default="time", help="排序方式")
    parser.add_argument("--asc", action="store_true", help="升序排列")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = list_files(args.path, args.order, not args.asc)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"获取失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
