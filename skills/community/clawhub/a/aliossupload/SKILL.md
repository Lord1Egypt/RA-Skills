---
name: aliossupload
description: "阿里云 OSS 文件上传工具。支持单文件上传，适用于将本地文件上传到阿里云 OSS 并获取访问链接。"
metadata:
  tags: [aliyun, oss, storage, upload]
  requires:
    env: [ALIYUN_OSS_ACCESS_KEY_ID, ALIYUN_OSS_ACCESS_KEY_SECRET]
    python_packages: [oss2]
---

# AliOSSUpload - 阿里云 OSS 上传工具

## 功能

- 单文件上传到阿里云 OSS
- 返回文件的访问 URL
- 自动读取环境变量配置

## 环境变量

```bash
export ALIYUN_OSS_ACCESS_KEY_ID="your-access-key-id"
export ALIYUN_OSS_ACCESS_KEY_SECRET="your-access-key-secret"
export ALIYUN_OSS_ENDPOINT="oss-cn-beijing.aliyuncs.com"
export ALIYUN_OSS_BUCKET="your-bucket-name"
```

## 使用示例

```python
from aliossupload import AliOSSUploader

uploader = AliOSSUploader()
result = uploader.upload_file("/path/to/file.mp4", "videos/file.mp4")
print(result['url'])
```
