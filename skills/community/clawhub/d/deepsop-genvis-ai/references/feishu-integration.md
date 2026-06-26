# 飞书图片发送指南

## 飞书支持的图片发送方式

### 方式 1: 使用 message 工具发送图片（推荐）

通过 `message` 工具的 `buffer` 参数直接发送图片：

```python
import base64

# 读取图片文件
with open("image.png", "rb") as f:
    image_data = f.read()

# 使用 message 工具发送
# message(
#     action="send",
#     buffer=base64.b64encode(image_data).decode(),
#     filename="image.png",
#     mimeType="image/png"
# )
```

### 方式 2: 使用飞书卡片消息（富文本）

飞书支持发送带有图片的交互式卡片：

```python
{
    "msg_type": "interactive",
    "card": {
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "✅ 图片生成成功"
            },
            "template": "green"
        },
        "elements": [
            {
                "tag": "img",
                "img_key": "",  # 需要先在飞书上传图片获取 img_key
                "alt": {
                    "tag": "plain_text",
                    "content": "生成的图片"
                }
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "**提示词**: 风景画"
                }
            }
        ]
    }
}
```

**注意**：使用 `img_key` 需要先将图片上传到飞书平台。

### 方式 3: 使用 Markdown 图片链接

飞书支持 Markdown 图片语法，但图片需要是公开可访问的 URL：

```markdown
![风景画](https://example.com/image.png)
```

**限制**：
- 图片 URL 必须是公网可访问的
- 不支持 base64 内嵌图片

## 最佳实践

### 对于 AI 图片生成场景

1. **生成图片后获取公开 URL**（如阿里云 OSS、AWS S3 等）
2. **使用 Markdown 语法发送**：
   ```markdown
   生成成功！🎨
   
   ![风景画](https://your-cdn.com/image.png)
   
   图片链接：https://your-cdn.com/image.png
   ```

3. **或者使用 message 工具直接发送图片数据**

### 代码示例

```python
from scripts.generate_image import generate_image

# 生成图片
result = generate_image(prompt="风景画")

if result and result["status"] == "SUCCESS":
    # 方式 1: 使用 Markdown 发送图片 URL
    reply = f"""生成成功！🎨

![风景画]({result['url']})

图片链接：{result['url']}"""
    
    # 方式 2: 下载后使用 message 工具发送
    # result = generate_image(prompt="风景画", download=True)
    # with open(result["local_path"], "rb") as f:
    #     image_data = f.read()
    # message(action="send", buffer=base64.b64encode(image_data).decode(), ...)
```

## 平台对比

| 平台 | Markdown 图片 | Base64 图片 | 卡片消息 | 说明 |
|------|--------------|-------------|----------|------|
| WebChat | ✅ 支持 | ✅ 支持 | ❌ 不支持 | 最灵活 |
| Discord | ✅ 支持 | ⚠️ 有限 | ✅ 支持 | 支持 embed |
| Telegram | ✅ 支持 | ✅ 支持 | ✅ 支持 | 支持多种方式 |
| **飞书** | ✅ 支持 | ❌ 不支持 | ✅ 支持 | 需公开 URL 或上传 |
| WhatsApp | ❌ 不支持 | ✅ 支持 | ❌ 不支持 | 需发送文件 |

## 飞书特殊说明

1. **Base64 图片不支持**：飞书不支持直接通过 base64 内嵌图片
2. **需要先上传**：使用卡片消息的 `img_key` 需要先将图片上传到飞书
3. **公开 URL 最方便**：使用 CDN 或对象存储的公开链接最简单
4. **Webhook 发送**：通过 Webhook 发送时，图片需要是公开可访问的

## 推荐的飞书集成方案

```python
# 方案 1: 使用公开 URL（最简单）
def send_image_to_feishu(image_url, prompt):
    content = f"""✅ 图片生成成功

**提示词**: {prompt}

![生成的图片]({image_url})

[打开图片]({image_url})"""
    
    # 使用 message 工具发送 Markdown
    # message(action="send", message=content)

# 方案 2: 下载后作为文件发送
def send_image_file(image_path):
    with open(image_path, "rb") as f:
        image_data = f.read()
    
    # 使用 message 工具发送文件
    # message(
    #     action="send",
    #     buffer=base64.b64encode(image_data).decode(),
    #     filename="generated_image.png",
    #     mimeType="image/png"
    # )
```
