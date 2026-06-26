---
name: feishu-image-sender
description: 直接通过飞书开放平台 API 发送图片（绕过 OpenClaw 插件的限制），而非以文件附件形式发送。使用场景：需要发送截图、二维码等图片给用户时。
---

# feishu-image-sender

通过飞书开放平台 API 直接发送图片到用户，图片以内嵌方式显示，而非文件附件。

## 核心逻辑

两步走：
1. 上传图片到飞书服务器，获取 `image_key`
2. 用 `image_key` 发一条 image 类型消息

## 操作步骤

### 第一步：获取 Access Token

```bash
curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"<APP_ID>","app_secret":"<APP_SECRET>"}'
```

响应：`{"code":0,"tenant_access_token":"t-xxx","expire":3339}`

记录返回的 `tenant_access_token`。

### 第二步：上传图片

```bash
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/images" \
  -H "Authorization: Bearer <tenant_access_token>" \
  -F "image_type=message" \
  -F "image=@/path/to/image.png"
```

响应：`{"code":0,"data":{"image_key":"img_v3_xxx"},"msg":"success"}`

记录返回的 `image_key`。

### 第三步：发送图片消息

```bash
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer <tenant_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "receive_id": "<open_id>",
    "msg_type": "image",
    "content": "{\"image_key\":\"<image_key>\"}"
  }'
```

`receive_id` 可选 `open_id`（用户唯标识）、`chat_id`（群会话）、`user_id`、`union_id`。

响应成功：`{"code":0,"data":{"message_id":"om_xxx",...}}`

## 完整示例（单次执行）

```bash
#!/bin/bash
# 参数
IMAGE_PATH="$1"
OPEN_ID="$2"
APP_ID="cli_a924632610b8dbd9"
APP_SECRET="c3TXscIJPF1f8jcQ4mJJegNVk72ktbwK"

# 1. 获取 token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['tenant_access_token'])")

# 2. 上传图片
IMAGE_KEY=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/images" \
  -H "Authorization: Bearer $TOKEN" \
  -F "image_type=message" \
  -F "image=@$IMAGE_PATH" | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['data']['image_key'])")

# 3. 发送图片
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"$OPEN_ID\",\"msg_type\":\"image\",\"content\":\"{\\\"image_key\\\":\\\"$IMAGE_KEY\\\"}\"}"

echo "Done: $IMAGE_KEY"
```

## 工具调用封装（Node.js）

```javascript
const fs = require('fs');
const path = require('path');

async function feishuSendImage(imagePath, openId, appId, appSecret) {
  // 1. get token
  const tokenRes = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: appId, app_secret: appSecret })
  });
  const { tenant_access_token } = await tokenRes.json();

  // 2. upload image
  const imageBuffer = fs.readFileSync(imagePath);
  const uploadRes = await fetch('https://open.feishu.cn/open-apis/im/v1/images', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${tenant_access_token}` },
    body: (() => {
      const form = new FormData();
      form.append('image_type', 'message');
      form.append('image', new Blob([imageBuffer]), path.basename(imagePath));
      return form;
    })()
  });
  const { data: { image_key } } = await uploadRes.json();

  // 3. send image message
  const sendRes = await fetch(`https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${tenant_access_token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      receive_id: openId,
      msg_type: 'image',
      content: JSON.stringify({ image_key })
    })
  });
  return sendRes.json();
}
```

## 限制与注意事项

- 图片大小限制：每个文件最大 30MB
- 支持格式：jpg、png、gif、webp、bmp、heic
- token 有效期 2 小时，超时需重新获取
- `receive_id_type` 必须与 `receive_id` 匹配（open_id / user_id / chat_id / union_id）
- 图片消息不能通过 web 预览，必须是桌面端或手机端才能直接查看
