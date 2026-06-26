# C14 - 企业微信

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C14 |
| 连接器名 | wecom |
| 显示名 | 企业微信 |
| 层级 | L2 鉴权便利型 |
| 可替代 | ✅ 可替代（Skill） |
| 分类 | 消息/通讯 |
| 替代难度 | 简单 |

## 连接器能力

| 能力 | 说明 |
|------|------|
| 发送消息 | 文本/Markdown/图文 |
| 群组管理 | 创建/管理群组 |
| 机器人 | 自定义机器人 |
| 应用消息 | 企业应用推送 |

## Skill 替代方案

### 脚本位置

使用 connector-hub 技能中的脚本：

```
scripts/
├── L2-auth-messaging-C14-wecom-send-text.py
├── L2-auth-messaging-C14-wecom-send-markdown.py
└── L2-auth-messaging-C14-wecom-send-news.py
```

### 鉴权方式

**Webhook URL**（最简单）：
1. 在企业微信群组添加机器人
2. 获取 Webhook URL（格式：`https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}`）
3. 直接 POST 请求，无需额外鉴权
4. 频率限制：每个机器人 20 条/分钟

**安全警告**：妥善保管 Webhook URL，避免泄露

**环境变量配置**：
```bash
export WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
```

### 核心脚本示例

**L2-auth-messaging-C14-wecom-send-text.py**：
```python
#!/usr/bin/env python3
"""发送企业微信文本消息"""

import os
import sys
import json
import argparse
import requests

WEBHOOK_URL = os.environ.get("WECOM_WEBHOOK_URL")

def send_text(content: str, mentioned_list: list = None, mentioned_mobile_list: list = None) -> dict:
    """发送文本消息"""
    if not WEBHOOK_URL:
        raise ValueError("未设置 WECOM_WEBHOOK_URL 环境变量")
    
    payload = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    
    # @指定用户
    if mentioned_list or mentioned_mobile_list:
        payload["text"]["mentioned_list"] = mentioned_list or []
        payload["text"]["mentioned_mobile_list"] = mentioned_mobile_list or []
    
    resp = requests.post(WEBHOOK_URL, json=payload)
    resp.raise_for_status()
    return resp.json()

def send_markdown(content: str) -> dict:
    """发送 Markdown 消息"""
    if not WEBHOOK_URL:
        raise ValueError("未设置 WECOM_WEBHOOK_URL 环境变量")
    
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    }
    
    resp = requests.post(WEBHOOK_URL, json=payload)
    resp.raise_for_status()
    return resp.json()

def send_news(articles: list) -> dict:
    """发送图文消息"""
    if not WEBHOOK_URL:
        raise ValueError("未设置 WECOM_WEBHOOK_URL 环境变量")
    
    payload = {
        "msgtype": "news",
        "news": {
            "articles": articles
        }
    }
    
    resp = requests.post(WEBHOOK_URL, json=payload)
    resp.raise_for_status()
    return resp.json()

def main():
    parser = argparse.ArgumentParser(description="发送企业微信消息")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 文本消息
    text_parser = subparsers.add_parser("text", help="发送文本消息")
    text_parser.add_argument("content", help="消息内容")
    text_parser.add_argument("--at", nargs="+", help="@用户列表")
    text_parser.add_argument("--at-mobile", nargs="+", help="@手机号列表")
    
    # Markdown 消息
    md_parser = subparsers.add_parser("markdown", help="发送 Markdown 消息")
    md_parser.add_argument("content", help="Markdown 内容")
    
    # 图文消息
    news_parser = subparsers.add_parser("news", help="发送图文消息")
    news_parser.add_argument("articles", help="文章列表（JSON 格式）")
    
    args = parser.parse_args()
    
    try:
        if args.command == "text":
            result = send_text(args.content, args.at, args.at_mobile)
        elif args.command == "markdown":
            result = send_markdown(args.content)
        elif args.command == "news":
            articles = json.loads(args.articles)
            result = send_news(articles)
        else:
            parser.print_help()
            return
        
        if result.get("errcode") == 0:
            print("消息发送成功")
        else:
            print(f"发送失败：{result.get('errmsg')}")
    except Exception as e:
        print(f"发送失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### 迁移成本

| 项目 | 说明 |
|------|------|
| Webhook | 改 URL 即可 |
| 工作流 | 无需修改 |

### 对比

| 维度 | 连接器 | Skill |
|------|--------|-------|
| 鉴权 | 平台托管 | 用户自管 |
| 功能 | 固定 | 可自定义 |
| 迁移 | 重配连接器 | 改 API 地址 |
