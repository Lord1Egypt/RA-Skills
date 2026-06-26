---
version: 1.0.0
name: cloud-upload-tencent
description: 腾讯云对象存储（COS）上传工具。将本地文件上传至腾讯云 COS，生成下载链接和图片预览。适用于备份文件、生成公开分享链接、存储静态资源。跨平台支持（macOS/Linux/Windows），支持 CLI 和 Python 两种方式。
metadata: {"openclaw": {"emoji": "☁️"}}
---

# Cloud Upload — Tencent COS ☁️

腾讯云对象存储上传，跨平台支持。

## 触发条件

- 用户要求上传文件到云存储
- 需要生成文件下载链接
- 备份本地文件到云端
- 需要公开分享文件（图片/文档）

## 前提条件

### 必需配置
```
TENCENT_COS_SECRET_ID=你的SecretId
TENCENT_COS_SECRET_KEY=你的SecretKey
TENCENT_COS_BUCKET=你的Bucket名称
TENCENT_COS_REGION=Bucket地域（如 ap-guangzhou）
```

### Bucket 地域对照
| 地域 | Region ID |
|------|-----------|
| 北京 | ap-beijing |
| 上海 | ap-shanghai |
| 广州 | ap-guangzhou |
| 成都 | ap-chengdu |
| 新加坡 | ap-singapore |

## 跨平台用法

### macOS / Linux（CLI 方式）

```bash
# 安装腾讯云 COS CLI
# pip 安装（Python 3.6+）
pip3 install cos-python-sdk-v5

# 上传文件（Python）
python3 << 'EOF'
from qcloud_cos import CosConfig, CosS3Client
import os

secret_id = os.getenv('TENCENT_COS_SECRET_ID')
secret_key = os.getenv('TENCENT_COS_SECRET_KEY')
bucket = os.getenv('TENCENT_COS_BUCKET')
region = os.getenv('TENCENT_COS_REGION')

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
client = CosS3Client(config)

# 上传
response = client.upload_file(
    Bucket=bucket,
    Key='filename.txt',
    LocalFilePath='/local/path/file.txt'
)
print(response['ETag'])
EOF

# 生成分享链接（3600秒有效期）
# 腾讯云 COS 控制台设置 bucket 公有读私有写或公有读写
# 链接格式：https://{bucket}.cos.{region}.myqcloud.com/{key}
```

### Linux（CLI 方式）
```bash
# 安装 coscmd CLI 工具
pip3 install coscmd

# 配置（交互式）
coscmd config -a SECRET_ID -s SECRET_KEY -b BUCKET -r REGION

# 上传
coscmd upload /local/file.txt remote/path/file.txt

# 生成分享链接（需要 bucket 设置公有读）
coscmd generate-download-link remote/path/file.txt
```

### Windows (PowerShell)
```powershell
# 安装 Python（从 python.org 下载）
# 安装 SDK
pip install cos-python-sdk-v5

# 上传（Python）
python -c "
from qcloud_cos import CosConfig, CosS3Client
import os

config = CosConfig(
    Region=os.getenv('TENCENT_COS_REGION'),
    SecretId=os.getenv('TENCENT_COS_SECRET_ID'),
    SecretKey=os.getenv('TENCENT_COS_SECRET_KEY')
)
client = CosS3Client(config)

response = client.upload_file(
    Bucket=os.getenv('TENCENT_COS_BUCKET'),
    Key='filename.txt',
    LocalFilePath='C:\path\to\file.txt'
)
print(response['ETag'])
"
```

## 使用决策树

```
1. 用户要上传文件？
   → 确认文件路径和目标名称

2. 是否有腾讯云配置？
   → 无 → 引导用户获取 SecretId/Key/Bucket

3. 文件大小？
   → < 20MB → 直接上传
   → > 20MB → 分片上传

4. 需要多久有效期？
   → 临时链接 → 预签名 URL（可设置过期时间）
   → 永久链接 → 公有读 bucket 设置
```

## 输出格式

```markdown
## ☁️ 上传结果

**文件名**: example.txt
**大小**: 1.2 MB
**Bucket**: my-bucket
**Region**: ap-guangzhou
**COS 路径**: remote/path/example.txt

### 🔗 访问链接

**直接下载**（公有读 bucket）：
https://my-bucket.cos.ap-guangzhou.myqcloud.com/remote/path/example.txt

**预签名链接**（私有 bucket，7天有效）：
[生成签名链接]

**预览**（图片/文档）：
[在线预览链接]
```

## 注意事项

- 预签名链接可设置过期时间（建议临时文件用短过期时间）
- Bucket 设置公有读后，链接永久有效
- 敏感文件不要设置公有读，用预签名链接
- 分片上传适合大文件（> 20MB）
- 腾讯云 COS 费用：存储 0.118元/GB/月，流量 0.5元/GB

## 备选方案（无腾讯云账号）

如无腾讯云账号，可用以下免费方案：
- **飞书云盘**：免费 10GB，直接通过 feishu_drive_file 上传
- **火山引擎 S3**（Coze 环境）：通过 Coze TTS 插件的 S3Storage 上传
