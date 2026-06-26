---
name: feishu-sender
description: Send messages and files to Feishu (Lark) via Open API. Supports text, markdown, any file format, and images. Use when user needs to send notifications, reports, or any content to Feishu/Lark groups or chats.
metadata:
  openclaw:
    requires:
      env:
        - FEISHU_APP_ID
        - FEISHU_APP_SECRET
        - FEISHU_CHAT_ID
---

# Feishu Sender

飞书（Lark）消息发送工具，支持主动推送文本、文件和图片到指定群聊。

## Quick Start

```python
from feishu_sender import FeishuSender

sender = FeishuSender()
sender.send_text("Hello Feishu!")
sender.send_file("report.pdf")
```

## CLI Usage

```bash
python3 scripts/send.py --text "Hello"
python3 scripts/send.py --file report.pdf
python3 scripts/send.py --text "Report" --files "a.docx,b.pdf"
```

## Configuration

Set environment variables or create `.env`:

```bash
FEISHU_APP_ID=cli_xxxxx
FEISHU_APP_SECRET=xxxxxxxx
FEISHU_CHAT_ID=oc_xxxxxx
```

Get credentials from [Feishu Open Platform](https://open.feishu.cn/app).

## Resources

- `feishu_sender.py` - Core module with FeishuSender class
- `scripts/send.py` - CLI entry point
