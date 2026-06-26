#!/usr/bin/env python3
"""
Agent P2P 文件传输客户端（简化版）
无需接收方确认，直接上传
"""

import os
import sys
import json
import base64
import hashlib
import requests
from pathlib import Path
import math
import time

# 配置
CHUNK_SIZE = 10 * 1024 * 1024  # 10MB 分片大小
MAX_RETRIES = 3


def get_config():
    """获取配置"""
    api_key = os.environ.get("AGENTP2P_API_KEY")
    hub_url = os.environ.get("AGENTP2P_HUB_URL")
    
    if not api_key or not hub_url:
        gateway_env = Path.home() / ".openclaw" / "gateway.env"
        if gateway_env.exists():
            for line in gateway_env.read_text().splitlines():
                if line.startswith("AGENTP2P_API_KEY="):
                    api_key = line.split("=", 1)[1].strip()
                elif line.startswith("AGENTP2P_HUB_URL="):
                    hub_url = line.split("=", 1)[1].strip()
    
    return api_key, hub_url


def get_contact(contact_id: int, api_key: str, hub_url: str):
    """获取联系人信息"""
    try:
        resp = requests.get(
            f"{hub_url}/api/contacts",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10
        )
        if resp.status_code == 200:
            contacts = resp.json().get("contacts", [])
            for c in contacts:
                if c.get("id") == contact_id:
                    return c
        return None
    except Exception as e:
        print(f"❌ 获取联系人失败: {e}")
        return None


def calculate_md5(file_path: str) -> str:
    """计算文件MD5"""
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


def calculate_chunk_md5(data: bytes) -> str:
    """计算分片MD5"""
    return hashlib.md5(data).hexdigest()


def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / 1024 / 1024:.2f} MB"
    else:
        return f"{size_bytes / 1024 / 1024 / 1024:.2f} GB"


def print_progress(current: int, total: int, prefix: str = "Progress"):
    """打印进度条"""
    percent = 100 * (current / float(total))
    filled_len = int(50 * current // total)
    bar = '█' * filled_len + '-' * (50 - filled_len)
    print(f'\r{prefix}: |{bar}| {percent:.1f}%', end='', flush=True)
    if current == total:
        print()


def initiate_transfer(api_key: str, to_portal: str, filename: str,
                     file_size: int, file_md5: str, chunks_total: int) -> str:
    """初始化文件传输（简化版：直接返回file_id，无需确认）"""
    try:
        resp = requests.post(
            f"{to_portal}/api/file/initiate",
            json={
                "api_key": api_key,
                "filename": filename,
                "size": file_size,
                "md5": file_md5,
                "to_portal": to_portal,
                "chunks_total": chunks_total
            },
            timeout=30
        )
        
        if resp.status_code == 200:
            result = resp.json()
            return result.get("file_id")
        else:
            print(f"❌ 初始化失败: {resp.status_code} - {resp.text}")
            return None
            
    except Exception as e:
        print(f"❌ 初始化传输失败: {e}")
        return None


def upload_chunk(api_key: str, to_portal: str, file_id: str, chunk_index: int,
                chunk_data: bytes, max_retries: int = MAX_RETRIES) -> bool:
    """上传单个分片"""
    chunk_md5 = calculate_chunk_md5(chunk_data)
    chunk_base64 = base64.b64encode(chunk_data).decode('utf-8')

    for attempt in range(max_retries):
        try:
            resp = requests.post(
                f"{to_portal}/api/file/chunk/{file_id}/{chunk_index}",
                json={
                    "api_key": api_key,
                    "file_id": file_id,
                    "chunk_index": chunk_index,
                    "chunk_md5": chunk_md5,
                    "data": chunk_base64
                },
                timeout=60
            )
            
            if resp.status_code == 200:
                return True
                
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(1)
    
    return False


def upload_file(file_path: str, to_contact: int):
    """发送文件（简化版：直接上传，无需确认）"""
    # 获取配置
    api_key, hub_url = get_config()
    if not api_key or not hub_url:
        print("❌ 配置不完整")
        return False
    
    # 检查文件
    file_path = Path(file_path)
    if not file_path.exists():
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 获取联系人
    contact = get_contact(to_contact, api_key, hub_url)
    if not contact:
        print(f"❌ 找不到联系人: {to_contact}")
        return False
    
    contact_name = contact.get("agent_name", contact.get("portal_url"))
    print(f"📤 发送文件到: {contact_name}")
    print(f"   文件: {file_path.name}")
    
    # 计算文件信息
    file_size = file_path.stat().st_size
    file_md5 = calculate_md5(str(file_path))
    chunks_total = math.ceil(file_size / CHUNK_SIZE)
    
    print(f"   大小: {format_size(file_size)}")
    print(f"   分片: {chunks_total} 个")
    
    # 获取接收方 Portal URL 和 SHARED_KEY
    to_portal = contact.get("portal_url")
    shared_key = contact.get("SHARED_KEY")
    if not to_portal:
        print(f"❌ 联系人没有 portal_url")
        return False
    if not shared_key:
        print(f"❌ 联系人没有 SHARED_KEY")
        return False

    # 初始化传输（使用 SHARED_KEY 发送到接收方 Portal）
    file_id = initiate_transfer(shared_key, to_portal, file_path.name,
                               file_size, file_md5, chunks_total)
    if not file_id:
        return False

    print(f"   文件ID: {file_id}")
    print(f"\n📤 开始上传...")

    # 上传分片（使用 SHARED_KEY 上传到接收方 Portal）
    success_count = 0
    with open(file_path, "rb") as f:
        for chunk_index in range(chunks_total):
            f.seek(chunk_index * CHUNK_SIZE)
            chunk_data = f.read(CHUNK_SIZE)

            print_progress(chunk_index + 1, chunks_total, "上传进度")

            if upload_chunk(shared_key, to_portal, file_id, chunk_index, chunk_data):
                success_count += 1
            else:
                print(f"\n❌ 分片 {chunk_index} 上传失败")
                return False
    
    print(f"\n✅ 文件发送完成！")
    print(f"   对方会收到通知")
    return True


def download_file(file_id: str, output_dir: str = "."):
    """下载文件"""
    api_key, hub_url = get_config()
    if not api_key or not hub_url:
        print("❌ 配置不完整")
        return False
    
    try:
        # 查询状态
        resp = requests.get(
            f"{hub_url}/api/file/status/{file_id}",
            params={"api_key": api_key},
            timeout=10
        )
        
        if resp.status_code != 200:
            print(f"❌ 查询失败: {resp.status_code}")
            return False
        
        status = resp.json()
        if status.get("status") != "completed":
            print(f"⏳ 文件未准备好: {status.get('status')}")
            return False
        
        filename = status.get("filename")
        print(f"📥 下载文件: {filename}")
        
        # 下载
        resp = requests.get(
            f"{hub_url}/api/file/download/{file_id}",
            params={"api_key": api_key},
            stream=True,
            timeout=300
        )
        
        if resp.status_code != 200:
            print(f"❌ 下载失败: {resp.status_code}")
            return False
        
        output_path = Path(output_dir) / filename
        with open(output_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"✅ 已保存: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return False


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Agent P2P 文件传输")
    parser.add_argument("-f", "--file", help="要发送的文件")
    parser.add_argument("-t", "--to", type=int, help="接收方联系人ID")
    parser.add_argument("-d", "--download", help="下载文件（file_id）")
    parser.add_argument("-o", "--output", default=".", help="下载保存目录")
    
    args = parser.parse_args()
    
    if args.file and args.to:
        upload_file(args.file, args.to)
    elif args.download:
        download_file(args.download, args.output)
    else:
        parser.print_help()
        print("\n示例:")
        print("  发送: python3 send_file.py -f doc.pdf -t 1")
        print("  下载: python3 send_file.py -d <file_id> -o ./downloads/")


if __name__ == "__main__":
    main()