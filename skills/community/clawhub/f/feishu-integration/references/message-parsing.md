# 飞书消息解析完整指南

## 概述

本模块提供完整的飞书消息解析功能，支持：
- 富文本消息（post）
- 纯文本消息（text）
- 交互式卡片（interactive）
- 图片消息 + OCR 识别（image）
- 引用回复消息

## 快速开始

### 1. 解析消息（纯文本输出）

```bash
# 获取 token
source ~/mo-hub/skills/feishu-integration/scripts/feishu-auth.sh
TOKEN=$(get_feishu_token)

# 解析消息（传入完整的消息 JSON）
python3 ~/mo-hub/skills/feishu-integration/scripts/feishu-message-parser.py \
  "$TOKEN" \
  '{"msg_type":"text","body":{"content":"{\"text\":\"Hello\"}"}}'
```

### 2. 解析消息（结构化输出）

```bash
# 返回 JSON 格式（包含 images、mentions、links 列表）
python3 ~/mo-hub/skills/feishu-integration/scripts/feishu-message-parser.py \
  "$TOKEN" \
  '{"msg_type":"post","body":{"content":"{\"title\":\"标题\",\"elements\":[[{\"tag\":\"text\",\"text\":\"内容\"}]]}"}}' \
  --format json
```

**输出示例**：
```json
{
  "title": "标题",
  "text_content": "内容",
  "markdown_content": "# 标题\n\n内容",
  "images": ["img_v3_xxx"],
  "mentions": [{"id": "ou_123", "name": "张三"}],
  "links": [{"text": "链接", "url": "https://..."}]
}
```

### 3. OCR 图片识别

```bash
# 识别图片中的文字
python3 ~/mo-hub/skills/feishu-integration/scripts/feishu-ocr.py \
  "img_v3_xxx" \
  "$TOKEN"
```

## 消息类型详解

### 纯文本消息（text）

**输入**：
```json
{
  "msg_type": "text",
  "body": {
    "content": "{\"text\":\"Hello World\"}"
  }
}
```

**输出**：
```
Hello World
```

### 富文本消息（post）

**输入**：
```json
{
  "msg_type": "post",
  "body": {
    "content": "{\"title\":\"标题\",\"content\":[[{\"tag\":\"text\",\"text\":\"内容\"}]]}"
  }
}
```

**输出**：
```
# 标题

内容
```

### 引用回复消息

**输入**：
```json
{
  "msg_type": "text",
  "body": {
    "content": "{\"text\":\"我的回复\"}"
  },
  "quoted_message_content": "原始消息内容"
}
```

**输出**：
```
【引用】原始消息内容
【回复】我的回复
```

### 图片消息 + OCR

**输入**：
```json
{
  "msg_type": "image",
  "body": {
    "content": "{\"image_key\":\"img_v3_xxx\"}"
  }
}
```

**输出**：
```
[图片]: 识别出的文字内容
```

## 支持的富文本标签

| 标签 | 说明 | 示例 |
|------|------|------|
| `text` | 纯文本 | `{"tag":"text","text":"内容"}` |
| `lark_md` | Markdown | `{"tag":"lark_md","content":"**粗体**"}` |
| `at` | @提及 | `{"tag":"at","user_name":"张三"}` |
| `a` | 链接 | `{"tag":"a","text":"链接","href":"https://..."}` |
| `img` | 图片 | `{"tag":"img","image_key":"img_v3_xxx"}` |

## Python API 使用

### 纯文本输出

```python
from feishu_message_parser import FeishuMessageParser

# 初始化解析器
parser = FeishuMessageParser(tenant_token="your_token")

# 解析消息
message_data = {
    "msg_type": "text",
    "body": {"content": '{"text":"Hello"}'}
}
result = parser.parse(message_data)
print(result)  # 输出: Hello
```

### 结构化输出

```python
# 解析富文本（返回结构化数据）
rich_content = {
    "title": "标题",
    "elements": [
        [
            {"tag": "text", "text": "第一行"},
            {"tag": "at", "user_id": "ou_123", "user_name": "张三"}
        ],
        [{"tag": "img", "image_key": "img_v3_xxx"}]
    ]
}

result = parser.parse_rich_text(rich_content, return_structured=True)
print(result)
# 输出:
# {
#   "title": "标题",
#   "text_content": "第一行",
#   "markdown_content": "# 标题\n\n第一行@张三\n[图片:img_v3_xxx]",
#   "images": ["img_v3_xxx"],
#   "mentions": [{"id": "ou_123", "name": "张三"}],
#   "links": []
# }
```

### OCR 识别
image_text = parser.get_image_text("img_v3_xxx")
print(image_text)
```

## 必需的飞书权限

在飞书开放平台配置以下权限：

- `im:message` - 读取消息内容
- `im:message:group_at_msg` - 接收群消息
- `im:resource` - 获取图片资源
- `optical_char_recognition:basic` - OCR 识别

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `[文本解析失败]` | JSON 格式错误 | 检查消息格式 |
| `[图片，无key]` | 图片 key 缺失 | 检查消息内容 |
| `OCR 失败` | 权限不足或 API 错误 | 检查权限配置 |

## 性能优化

### 批量解析

```python
parser = FeishuMessageParser(tenant_token)

messages = [msg1, msg2, msg3]
results = [parser.parse(msg) for msg in messages]
```

### OCR 缓存

对于重复的图片，可以缓存 OCR 结果：

```python
ocr_cache = {}

def get_image_text_cached(image_key):
    if image_key not in ocr_cache:
        ocr_cache[image_key] = parser.get_image_text(image_key)
    return ocr_cache[image_key]
```

## 参考资料

- [飞书开放平台 - 消息格式](https://open.feishu.cn/document/server-docs/im-v1/message/message-content)
- [飞书开放平台 - OCR API](https://open.feishu.cn/document/server-docs/ai/optical_char_recognition-v1/image/recognize_basic)
- 教程文档：https://uniquecapital.feishu.cn/docx/BZTvd4SMSo6OzsxodHnckHh8nZb

## 示例脚本

完整示例见 `examples/` 目录：
- `parse_text.sh` - 解析纯文本
- `parse_rich_text.sh` - 解析富文本
- `ocr_image.sh` - OCR 识别
