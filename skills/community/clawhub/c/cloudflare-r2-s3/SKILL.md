---
name: cloudflare-r2-s3
description: Cloudflare R2 S3 兼容存储工具，支持配置 API 密钥、上传文件并获取公开访问地址。使用当需要上传文件到 Cloudflare R2 获取公开链接时。
---

# Cloudflare R2 S3 存储工具

Cloudflare R2 提供 10GB 免费存储额度，兼容 S3 API，可以用来存储文件并生成公开访问地址。

## 功能特性

- ✅ 支持配置 S3 API 端点、访问密钥和存储桶
- ✅ 上传本地文件到 R2 存储桶
- ✅ 自动生成公开访问 URL
- ✅ 支持列出存储桶中的文件
- ✅ 支持删除文件
- ✅ 兼容其他 S3 兼容存储服务（如 MinIO）

## 配置方式

在使用前需要配置以下环境变量或配置文件：

```bash
# ~/.openclaw/config/cloudflare-r2.env
CLOUDFLARE_R2_ACCOUNT_ID=your-account-id
CLOUDFLARE_R2_ACCESS_KEY_ID=your-access-key
CLOUDFLARE_R2_SECRET_ACCESS_KEY=your-secret-key
CLOUDFLARE_R2_BUCKET_NAME=your-bucket-name
CLOUDFLARE_R2_PUBLIC_DOMAIN=your-public-domain  # 可选，自定义公开域名
```

或者在调用时传入参数。

## 使用方法

### 上传文件

```python
from scripts.r2_uploader import R2Uploader

uploader = R2Uploader()
result = uploader.upload_file(local_path, object_name=None, public=True)
print(result['public_url'])  # 获取公开访问地址
```

### 命令行使用

```bash
# 上传文件
python skills/cloudflare-r2-s3/scripts/r2_uploader.py upload /path/to/file.jpg [object-name]

# 列出文件
python skills/cloudflare-r2-s3/scripts/r2_uploader.py list

# 删除文件
python skills/cloudflare-r2-s3/scripts/r2_uploader.py delete object-name
```

## Cloudflare R2 配置步骤

1. **创建 R2 存储桶**
   - 登录 Cloudflare 控制台 → R2 → 创建存储桶
   - 记住存储桶名称

2. **创建 API 令牌**
   - R2 → 管理 R2 API 令牌 → 创建 API 令牌
   - 授予 `Object Read + Write` 权限
   - 保存 Access Key ID 和 Secret Access Key

3. **配置公开访问**（可选但推荐）
   - 在存储桶设置 → "Public Access" → 启用
   - 可以使用 Cloudflare 提供的 `pub-${bucket-name}.r2.dev` 域名
   - 或者绑定自定义域名

## 依赖

需要安装 boto3:
```bash
pip install boto3
```

## 脚本说明

- `scripts/r2_uploader.py` - 主上传工具，支持命令行和 API 调用
- `references/config_example.env` - 配置文件示例
