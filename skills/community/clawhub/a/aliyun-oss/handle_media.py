#!/usr/bin/env python3
"""
OpenClaw媒体处理器 - 阿里云OSS文件上传
处理文件上传并返回临时访问链接
"""

import sys
import os
from pathlib import Path

# 添加当前目录到 Python 路径
sys.path.append(str(Path(__file__).parent))

def handle_media(file_path: str) -> str:
    """
    OpenClaw标准媒体处理接口
    
    Args:
        file_path: 媒体文件路径
        
    Returns:
        临时访问链接或错误信息
    """
    try:
        from aliyun_oss_uploader import AliyunOSSUploader
        uploader = AliyunOSSUploader()
        
        # 上传文件
        result = uploader.upload_single_file(file_path)
        
        if result['status'] == 'success':
            # 由于预签名URL可能存在兼容性问题，提供两种访问方式
            oss_key = result['oss_key']
            bucket_name = uploader.config['bucket_name']
            endpoint = uploader.config['endpoint']
            
            standard_url = f"https://{bucket_name}.{endpoint}/{oss_key}"
            
            return (f"✅ 文件上传成功！\n"
                   f"📁 OSS路径: {oss_key}\n"
                   f"🔗 标准URL: {standard_url}\n"
                   f"💡 请通过OSS控制台生成临时访问链接（1小时有效）")
        else:
            return f"❌ 上传失败: {result['error']}"
            
    except Exception as e:
        return f"❌ 处理失败: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: handle_media.py <file_path>", file=sys.stderr)
        sys.exit(1)
    
    result = handle_media(sys.argv[1])
    print(result)