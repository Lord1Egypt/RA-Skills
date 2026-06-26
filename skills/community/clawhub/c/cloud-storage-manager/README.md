# Cloud Storage Manager

English | [中文](#中文说明)

## Overview

Universal cloud storage manager supporting AWS S3, Aliyun OSS, Tencent COS, and Azure Blob Storage. Simplifies multi-cloud storage operations.

## Features

- **Multi-Cloud Support**: AWS S3, Aliyun OSS, Tencent COS, Azure Blob
- **Unified API**: Same interface across all providers
- **Sync Operations**: Bidirectional sync between local and cloud
- **Cross-Provider Copy**: Transfer between different cloud providers
- **CDN Integration**: Automatic CDN URL generation
- **Multipart Upload**: Large file support with resume capability

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from cloud_storage_manager import StorageManager, Provider

# Initialize Aliyun OSS
storage = StorageManager(Provider.ALIYUN_OSS, {
    "access_key_id": "your_key",
    "access_key_secret": "your_secret",
    "endpoint": "oss-cn-hangzhou.aliyuncs.com",
    "bucket": "my-bucket"
})

# Upload file
storage.upload("local/file.txt", "remote/path/file.txt")

# Generate signed URL
url = storage.get_signed_url("private/file.txt", expires=3600)
print(f"Download URL: {url}")
```

## Supported Providers

| Provider | Service | Region Support |
|----------|---------|----------------|
| AWS | S3 | Global |
| Aliyun | OSS | China + Global |
| Tencent | COS | China + Global |
| Microsoft | Azure Blob | Global |

## License

MIT

---

# 中文说明

## 概述

通用云存储管理器，支持AWS S3、阿里云OSS、腾讯云COS和Azure Blob存储。简化多云存储操作。

## 功能特性

- **多云支持**: AWS S3、阿里云OSS、腾讯云COS、Azure Blob
- **统一API**: 所有提供商使用相同接口
- **同步操作**: 本地与云端双向同步
- **跨云复制**: 在不同云提供商之间传输
- **CDN集成**: 自动生成CDN URL
- **分片上传**: 大文件断点续传支持

## 支持的云服务商

| 服务商 | 服务 | 区域支持 |
|--------|------|----------|
| 亚马逊 | S3 | 全球 |
| 阿里云 | OSS | 中国+全球 |
| 腾讯云 | COS | 中国+全球 |
| 微软 | Azure Blob | 全球 |

## 快速开始

```python
from cloud_storage_manager import StorageManager, Provider

# 初始化阿里云OSS
storage = StorageManager(Provider.ALIYUN_OSS, config={
    "access_key_id": "你的Key",
    "access_key_secret": "你的Secret",
    "endpoint": "oss-cn-hangzhou.aliyuncs.com",
    "bucket": "存储桶名"
})

# 上传文件
storage.upload("本地文件.txt", "云端路径/文件.txt")
```

## 许可证

MIT
