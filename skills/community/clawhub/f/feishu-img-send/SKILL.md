---
name: feishu-image-sender
description: 飞书图片发送 - 使用API直接发送图片到飞书 / Send images to Feishu via API
metadata:
  version: 1.0.0
---

# 飞书图片发送 / Feishu Image Sender

通过飞书开放平台API发送图片。

## 使用方法 / Usage

### 命令行
```bash
# 发送图片
./scripts/send.sh <图片路径> <用户ID>

# 示例
./scripts/send.sh /tmp/test.png ou_xxxxxxxx
```

### Python
```python
from feishu_image import FeishuImageSender

sender = FeishuImageSender()
sender.send_image("/tmp/test.png", "ou_xxxxxxxx")
```

## 配置 / Configuration

脚本已内置APP_ID和APP_SECRET，无需额外配置。

## 原理 / How It Works

1. 获取 tenant_access_token
2. 上传图片到飞书获取 image_key
3. 使用 image_key 发送图片消息

## API调用

```
POST /open-apis/auth/v3/tenant_access_token/internal
POST /open-apis/im/v1/images
POST /open-apis/im/v1/messages
```

## 权限要求

- im:resource
- im:message

## 更新日志
- v1.0.0: 初始版本

