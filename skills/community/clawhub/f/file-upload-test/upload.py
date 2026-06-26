#!/usr/bin/env python3
"""
File Upload Skill - 上传文件到快手内部 BS3 存储
"""

import sys
import os
from uuid import uuid4

import boto3
from botocore import UNSIGNED
from botocore.config import Config

# ============== 配置 ==============
BS3_ENDPOINT = os.getenv("BS3_ENDPOINT", "http://bs3-hb1.internal")
BS3_BUCKET = os.getenv("BS3_BUCKET", "kim-mario-claw")
BS3_REGION = os.getenv("BS3_REGION", "hb1")

# 初始化 S3 客户端（免签名）
# 使用 S3 直接初始化，避免 boto3 自动修改 endpoint
from botocore.session import Session

botocore_session = Session()
botocore_session.set_config_variable("region", BS3_REGION)

client = botocore_session.create_client(
    "s3",
    endpoint_url=BS3_ENDPOINT,
    config=Config(signature_version=UNSIGNED),
    use_ssl=False,
)


def _unique_key(key: str) -> str:
    """
    生成唯一文件键，添加 8 位 UUID 前缀防止重名覆盖
    
    Args:
        key: 原始文件名
        
    Returns:
        带 UUID 前缀的文件名
    """
    return f"{uuid4().hex[:8]}_{key}"


def upload_file(key: str, file_path: str) -> str:
    """
    上传本地文件到 BS3
    
    Args:
        key: 文件标识名（用于生成唯一键）
        file_path: 本地文件路径
        
    Returns:
        上传后的文件 URL（含有效期提示）
        
    Raises:
        FileNotFoundError: 文件不存在
        Exception: 上传失败
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在：{file_path}")
    
    obj_key = _unique_key(key)
    
    with open(file_path, "rb") as data:
        client.put_object(
            Body=data,
            Bucket=BS3_BUCKET,
            Key=obj_key
        )
    
    url = f"https://bs3-hb1.corp.kuaishou.com/{BS3_BUCKET}/{obj_key}"
    return f"{url}\n\n⚠️ 注意：上传文件链接 7 天有效，请及时下载保存。"


def upload_bytes(key: str, data: bytes) -> str:
    """
    上传二进制数据到 BS3
    
    Args:
        key: 文件标识名（用于生成唯一键）
        data: 二进制数据
        
    Returns:
        上传后的文件 URL（含有效期提示）
    """
    obj_key = _unique_key(key)
    
    client.put_object(
        Body=data,
        Bucket=BS3_BUCKET,
        Key=obj_key
    )
    
    url = f"https://bs3-hb1.corp.kuaishou.com/{BS3_BUCKET}/{obj_key}"
    return f"{url}\n\n⚠️ 注意：上传文件链接 7 天有效，请及时下载保存。"


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("Usage: python3 upload.py <command> [args...]")
        print("")
        print("Commands:")
        print("  upload_file <key> <file_path>   - 上传文件")
        print("  upload_bytes <key> <file_path>  - 上传文件内容（二进制）")
        print("")
        print("Examples:")
        print("  python3 upload.py upload_file test.png /path/to/file.png")
        print("  python3 upload.py upload_bytes data.bin /path/to/data.bin")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "upload_file":
        if len(sys.argv) < 4:
            print("Error: upload_file requires <key> and <file_path>")
            sys.exit(1)
        key = sys.argv[2]
        file_path = sys.argv[3]
        try:
            url = upload_file(key, file_path)
            print(f"✅ Upload successful: {url}")
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            sys.exit(1)
    
    elif command == "upload_bytes":
        if len(sys.argv) < 4:
            print("Error: upload_bytes requires <key> and <file_path>")
            sys.exit(1)
        key = sys.argv[2]
        file_path = sys.argv[3]
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            url = upload_bytes(key, data)
            print(f"✅ Upload successful: {url}")
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            sys.exit(1)
    
    else:
        print(f"Error: Unknown command '{command}'")
        sys.exit(1)


if __name__ == "__main__":
    main()
