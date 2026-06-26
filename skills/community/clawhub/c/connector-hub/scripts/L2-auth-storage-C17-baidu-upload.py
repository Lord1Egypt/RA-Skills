#!/usr/bin/env python3
"""上传文件到百度网盘"""

import os
import sys
import json
import argparse
import hashlib
import requests
from pathlib import Path

API_BASE = "https://pan.baidu.com/rest/2.0/xpan/file"
UPLOAD_API = "https://d.pcs.baidu.com/rest/2.0/pcs/superfile2"

def upload_file(local_path: str, remote_path: str, rtype: int = 3) -> dict:
    """上传文件（支持分片）
    
    Args:
        local_path: 本地文件路径
        remote_path: 网盘目标路径
        rtype: 重名处理（1-重命名 2-覆盖 3-覆盖）
    
    Returns:
        API 响应
    """
    access_token = os.environ.get("BAIDU_PAN_ACCESS_TOKEN")
    if not access_token:
        raise ValueError("未设置 BAIDU_PAN_ACCESS_TOKEN 环境变量")
    
    file_path = Path(local_path)
    if not file_path.exists():
        raise FileNotFoundError(f"文件不存在：{local_path}")
    
    file_size = file_path.stat().st_size
    
    # 1. 预上传
    params = {
        "method": "precreate",
        "access_token": access_token,
        "path": remote_path,
        "size": file_size,
        "isdir": 0,
        "autoinit": 1,
        "rtype": rtype  # 1-重命名 2-覆盖 3-覆盖
    }
    
    resp = requests.post(f"{API_BASE}/precreate", params=params)
    resp.raise_for_status()
    pre_data = resp.json()
    
    if pre_data.get("errno") != 0:
        raise Exception(f"预上传失败：{pre_data.get('errmsg')}")
    
    upload_key = pre_data.get("uploadid")
    block_list = pre_data.get("block_list", [])
    
    # 2. 分片上传
    uploaded_blocks = []
    with open(local_path, "rb") as f:
        for i, _ in enumerate(block_list):
            chunk = f.read(4 * 1024 * 1024)  # 4MB 分片
            chunk_md5 = hashlib.md5(chunk).hexdigest()
            
            params = {
                "method": "upload",
                "access_token": access_token,
                "type": "tmpfile",
                "path": remote_path,
                "uploadid": upload_key,
                "partseq": i
            }
            
            resp = requests.post(
                UPLOAD_API,
                params=params,
                files={"file": ("chunk", chunk)}
            )
            resp.raise_for_status()
            uploaded_blocks.append(chunk_md5)
    
    # 3. 创建文件
    params = {
        "method": "create",
        "access_token": access_token,
        "path": remote_path,
        "size": file_size,
        "isdir": 0,
        "rtype": rtype,
        "uploadid": upload_key,
        "block_list": json.dumps(uploaded_blocks)
    }
    
    resp = requests.post(f"{API_BASE}/create", params=params)
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    return f"""
上传成功：

| 字段 | 值 |
|------|-----|
| 文件路径 | {data.get('path', '-')} |
| 文件大小 | {data.get('size', '-')} |
| 文件 ID | {data.get('fs_id', '-')} |
| MD5 | {data.get('md5', '-')} |
"""

def main():
    parser = argparse.ArgumentParser(description="上传文件到百度网盘")
    parser.add_argument("local_path", help="本地文件路径")
    parser.add_argument("remote_path", help="网盘目标路径")
    parser.add_argument("--rtype", type=int, choices=[1, 2, 3], default=3, 
                       help="重名处理：1-重命名 2-覆盖 3-覆盖")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = upload_file(args.local_path, args.remote_path, args.rtype)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"上传失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
