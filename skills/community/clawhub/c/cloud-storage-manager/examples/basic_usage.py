#!/usr/bin/env python3
"""
Cloud Storage Manager - Basic Usage Example
云存储管理器 - 基础使用示例

This example demonstrates basic file operations with cloud storage.
本示例展示云存储的基础文件操作。

Note: This example uses mock mode. For real usage, configure credentials.
注意：本示例使用模拟模式。实际使用时需要配置凭证。
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cloud_storage_manager import StorageManager, Provider
from cloud_storage_manager.config import load_config


def main():
    """Main example function"""
    print("=" * 60)
    print("Cloud Storage Manager - Basic Usage Example")
    print("云存储管理器 - 基础使用示例")
    print("=" * 60)
    
    # Initialize storage manager (mock mode for demo)
    # 初始化存储管理器（示例使用模拟模式）
    print("\n[1] Initializing storage manager...")
    print("   Provider: Mock Storage (for demonstration)")
    print("   提供商：模拟存储（用于演示）")
    
    # In real usage:
    # storage = StorageManager(Provider.ALIYUN_OSS, {
    #     "access_key_id": "your_key",
    #     "access_key_secret": "your_secret",
    #     "endpoint": "oss-cn-hangzhou.aliyuncs.com",
    #     "bucket": "my-bucket"
    # })
    
    print("✓ Storage manager initialized")
    
    # Simulate operations
    # 模拟操作
    print("\n[2] Simulated Operations / 模拟操作：")
    
    operations = [
        ("Upload file", "upload('local/report.pdf', 'documents/2024/report.pdf')"),
        ("Download file", "download('documents/2024/report.pdf', 'local/downloaded.pdf')"),
        ("List objects", "list_objects(prefix='documents/2024/')"),
        ("Check existence", "exists('documents/2024/report.pdf')"),
        ("Get file size", "get_size('documents/2024/report.pdf')"),
        ("Generate signed URL", "get_signed_url('private/file.txt', expires=3600)"),
        ("Delete file", "delete('temp/old_file.txt')"),
    ]
    
    for op_name, op_code in operations:
        print(f"   ✓ {op_name}")
        print(f"     Code: storage.{op_code}")
    
    # Sync operations
    # 同步操作
    print("\n[3] Sync Operations / 同步操作：")
    
    sync_examples = [
        ("Sync to cloud", "sync.sync_to_cloud('/local/data', 'backup/2024/')"),
        ("Sync from cloud", "sync.sync_from_cloud('data/export/', '/local/download')"),
        ("Compare directories", "sync.compare('/local/data', 'backup/2024/')"),
    ]
    
    for op_name, op_code in sync_examples:
        print(f"   ✓ {op_name}")
        print(f"     Code: {op_code}")
    
    # Multi-provider copy
    # 多云复制
    print("\n[4] Cross-Provider Copy / 跨云复制：")
    print("   # Copy from AWS S3 to Aliyun OSS")
    print("   source = StorageManager(Provider.AWS_S3, aws_config)")
    print("   dest = StorageManager(Provider.ALIYUN_OSS, oss_config)")
    print("   copier = CrossProviderCopy(source, dest)")
    print("   copier.copy('s3/file.zip', 'oss/file.zip')")
    
    # Configuration example
    # 配置示例
    print("\n[5] Configuration Example / 配置示例：")
    print("""
    # .env file / 环境变量文件
    ALIYUN_ACCESS_KEY_ID=your_access_key
    ALIYUN_ACCESS_KEY_SECRET=your_secret_key
    ALIYUN_OSS_ENDPOINT=oss-cn-hangzhou.aliyuncs.com
    ALIYUN_OSS_BUCKET=my-bucket
    
    # Or initialize from environment / 或从环境初始化
    config = load_config('aliyun_oss')
    storage = StorageManager(Provider.ALIYUN_OSS, config)
    """)
    
    print("\n" + "=" * 60)
    print("Example completed!")
    print("For real usage, configure your cloud provider credentials.")
    print("示例完成！实际使用时请配置云服务商凭证。")
    print("=" * 60)


if __name__ == "__main__":
    main()
