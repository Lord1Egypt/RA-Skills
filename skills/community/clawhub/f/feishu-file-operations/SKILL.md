---
name: feishu-file-operations
description: |
  飞书文件操作：发送文件到对话、创建和写入飞书云文档。适用于需要通过飞书 Bot API 发送文件或创建文档的场景。
---

# 飞书文件操作指南

本技能提供通过飞书 Bot API 发送文件和创建/写入云文档的完整方法。

## 🌟 推荐方式：OpenClaw CLI（最简单）

OpenClaw 内置 `message send` 命令支持 `--media` 参数发送文件：

```bash
openclaw message send --channel feishu --target ou_xxx --media "/path/to/file.md" --message "文件说明"
```

**参数说明：**
- `--channel feishu` - 使用飞书渠道
- `--target` - 接收者 ID（open_id 如 ou_xxx，或群聊 ID）
- `--media` - 本地文件路径或 URL
- `--message` - 可选，附带文字说明

**支持的媒体类型：**
- 图片（jpg, png, gif, webp）
- 音频（mp3, wav, ogg 等）
- 视频（mp4, mov 等）
- 文档（pdf, doc, docx, md, txt 等）

**优点：**
- 无需手动获取 token
- 自动处理文件上传
- 支持所有 OpenClaw 渠道（Telegram、Discord、WhatsApp 等）

---

## 备选方式：直接调用飞书 API

适用于需要在其他程序中调用或需要更精细控制的场景。

## 前置条件

- 飞书应用已启用，有 `appId` 和 `appSecret`
- 需要的权限：
  - `im:file` - 发送文件消息
  - `docx:document` - 创建和编辑云文档
  - `drive:drive` - 云空间访问

## 一、获取 Tenant Access Token

所有 API 调用都需要先获取 tenant_access_token：

```bash
curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "YOUR_APP_ID",
    "app_secret": "YOUR_APP_SECRET"
  }'
```

返回示例：
```json
{
  "code": 0,
  "tenant_access_token": "t-gxxxxx",
  "expire": 7200
}
```

## 二、发送文件到飞书对话

### 步骤 1：上传文件获取 file_key

```bash
curl -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TENANT_ACCESS_TOKEN" \
  -F "file=@/path/to/file.md" \
  -F "file_name=文件名.md" \
  -F "file_type=doc"
```

**参数说明：**
- `file`: 本地文件路径（使用 @ 前缀）
- `file_name`: 显示的文件名
- `file_type`: 文件类型（doc/stream 等）

**返回示例：**
```json
{
  "code": 0,
  "data": {
    "file_key": "file_v3_00100_xxx"
  }
}
```

### 步骤 2：发送文件消息

```bash
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TENANT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "receive_id": "ou_xxx",
    "msg_type": "file",
    "content": "{\"file_key\":\"file_v3_00100_xxx\"}"
  }'
```

**重要提示：**
- ⚠️ `receive_id_type` 必须作为**查询参数**传递，不能放在 JSON body 中！
- 放在 body 中会报错：`"receive_id_type is required"`

**receive_id_type 可选值：**
- `open_id` - 用户 open_id（如 ou_xxx）
- `user_id` - 用户 user_id
- `union_id` - 用户 union_id
- `chat_id` - 群聊 ID

## 三、创建和写入飞书云文档

### 步骤 1：创建文档

```bash
curl -X POST "https://open.feishu.cn/open-apis/docx/v1/documents" \
  -H "Authorization: Bearer $TENANT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "文档标题"
  }'
```

**返回示例：**
```json
{
  "code": 0,
  "data": {
    "document": {
      "document_id": "EqOQdnxWqoUW9JxL8RRckUeYn3y",
      "title": "文档标题"
    }
  }
}
```

### 步骤 2：获取文档根 block_id

```bash
curl -X GET "https://open.feishu.cn/open-apis/docx/v1/documents/$DOCUMENT_ID/blocks" \
  -H "Authorization: Bearer $TENANT_ACCESS_TOKEN"
```

返回的根 block_id 通常与 document_id 相同。

### 步骤 3：写入内容

```bash
curl -X POST "https://open.feishu.cn/open-apis/docx/v1/documents/$DOCUMENT_ID/blocks/$ROOT_BLOCK_ID/children" \
  -H "Authorization: Bearer $TENANT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {
        "block_type": 2,
        "text": {
          "elements": [
            {
              "text_run": {
                "content": "这是第一段文字内容"
              }
            }
          ]
        }
      },
      {
        "block_type": 3,
        "heading1": {
          "elements": [
            {
              "text_run": {
                "content": "这是一级标题"
              }
            }
          ]
        }
      }
    ],
    "index": 0
  }'
```

**block_type 说明：**
| 值 | 类型 |
|----|------|
| 1 | 页面（Page）|
| 2 | 文本（Text）|
| 3 | 一级标题（Heading1）|
| 4 | 二级标题（Heading2）|
| 5 | 三级标题（Heading3）|
| 6 | 四级标题（Heading4）|
| 7 | 五级标题（Heading5）|
| 8 | 六级标题（Heading6）|
| 10 | 无序列表（Bullet）|
| 11 | 有序列表（Ordered）|
| 12 | 代码块（Code）|
| 13 | 引用（Quote）|

## 四、文档分享

飞书文档 URL 格式：
```
https://[domain].feishu.cn/docx/[document_id]
```

例如：`https://tt-pc.feishu.cn/docx/EqOQdnxWqoUW9JxL8RRckUeYn3y`

可以通过消息发送文档链接：

```bash
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TENANT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "receive_id": "ou_xxx",
    "msg_type": "text",
    "content": "{\"text\":\"文档链接：https://xxx.feishu.cn/docx/xxx\"}"
  }'
```

## 五、常见错误

### 1. receive_id_type is required

**原因：** `receive_id_type` 放在了 JSON body 中

**解决：** 将 `receive_id_type` 作为查询参数传递：
```
POST /open-apis/im/v1/messages?receive_id_type=open_id
```

### 2. 权限不足

**原因：** 飞书应用缺少相应权限

**解决：** 在飞书开放平台为应用添加所需权限

### 3. Token 过期

**原因：** tenant_access_token 有效期约 2 小时

**解决：** 重新调用获取 token 的 API

## 六、完整示例（OpenClaw exec 调用）

```bash
# 1. 获取 token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"cli_xxx","app_secret":"xxx"}' | jq -r '.tenant_access_token')

# 2. 上传文件
FILE_KEY=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/path/to/file.md" \
  -F "file_name=file.md" \
  -F "file_type=doc" | jq -r '.data.file_key')

# 3. 发送文件
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"ou_xxx\",\"msg_type\":\"file\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"}"
```

## 七、参考资料

- 飞书开放平台：https://open.feishu.cn/
- 发送消息 API：https://open.feishu.cn/document/server-docs/im-v1/message/create
- 云文档 API：https://open.feishu.cn/document/server-docs/docs/docx-v1/document

---

*本技能由 OpenClaw 龙虾创建，适用于飞书 Bot 文件操作场景*