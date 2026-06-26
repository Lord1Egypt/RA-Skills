# C12 - 飞书

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C12 |
| 连接器名 | feishu |
| 显示名 | 飞书 |
| 层级 | L2 鉴权便利型 |
| 可替代 | ✅ 可替代（Skill） |
| 分类 | 消息/通讯 |
| 替代难度 | 简单 |

## 连接器能力

| 能力 | 说明 |
|------|------|
| 发送消息 | 文本/富文本/卡片消息 |
| 群组管理 | 创建/管理群组 |
| 机器人 | 自定义机器人 |
| 审批流 | 创建/查询审批 |
| 日历 | 日程管理 |

## Skill 替代方案

### 脚本位置

使用 connector-hub 技能中的脚本：

```
scripts/
├── L2-auth-messaging-C12-feishu-send-text.py     # 发送文本消息
├── L2-auth-messaging-C12-feishu-send-post.py     # 发送富文本消息
└── L2-auth-messaging-C12-feishu-send-card.py     # 发送卡片消息
```

### 鉴权方式

**方式一：Webhook（最简单）**
1. 在飞书群组添加自定义机器人
2. 获取 Webhook URL（格式：`https://open.feishu.cn/open-apis/bot/v2/hook/{webhook_key}`）
3. 可选安全配置：自定义关键词、IP 白名单、签名校验
4. 直接 POST 请求

**方式二：自建应用（功能更全）**
1. 在飞书开放平台 (https://open.feishu.cn) 创建应用
2. 获取 `app_id` + `app_secret`
3. 获取 `tenant_access_token`
4. Token 有效期 2 小时

**环境变量配置**：
```bash
# Webhook 方式
export FEISHU_WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"

# 自建应用方式
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
```

### 核心脚本示例

**L2-auth-messaging-C12-feishu-send-post.py**：
```python
#!/usr/bin/env python3
"""通过 Webhook 发送飞书消息"""

import os
import sys
import json
import hmac
import hashlib
import base64
import argparse
import requests
from datetime import datetime

WEBHOOK_URL = os.environ.get("FEISHU_WEBHOOK_URL")
WEBHOOK_SECRET = os.environ.get("FEISHU_WEBHOOK_SECRET")

def gen_sign(secret: str) -> tuple:
    """生成签名（如果启用了签名校验）"""
    import time
    timestamp = str(int(time.time()))
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return timestamp, sign

def send_text(content: str, at_user: str = None) -> dict:
    """发送文本消息"""
    if not WEBHOOK_URL:
        raise ValueError("未设置 FEISHU_WEBHOOK_URL 环境变量")
    
    payload = {
        "msg_type": "text",
        "content": {
            "text": content
        }
    }
    
    # 如果启用了签名校验
    if WEBHOOK_SECRET:
        timestamp, sign = gen_sign(WEBHOOK_SECRET)
        payload["timestamp"] = timestamp
        payload["sign"] = sign
    
    if at_user:
        payload["content"]["text"] = f"<at user_id=\"{at_user}\">用户</at> {content}"
    
    resp = requests.post(WEBHOOK_URL, json=payload)
    resp.raise_for_status()
    return resp.json()

def send_post(title: str, content_lines: list) -> dict:
    """发送富文本消息"""
    if not WEBHOOK_URL:
        raise ValueError("未设置 FEISHU_WEBHOOK_URL 环境变量")
    
    content = []
    for line in content_lines:
        content.append([{"tag": "text", "text": line}])
    
    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": content
                }
            }
        }
    }
    
    if WEBHOOK_SECRET:
        timestamp, sign = gen_sign(WEBHOOK_SECRET)
        payload["timestamp"] = timestamp
        payload["sign"] = sign
    
    resp = requests.post(WEBHOOK_URL, json=payload)
    resp.raise_for_status()
    return resp.json()

def send_card(title: str, content: str, color: str = "blue") -> dict:
    """发送卡片消息"""
    if not WEBHOOK_URL:
        raise ValueError("未设置 FEISHU_WEBHOOK_URL 环境变量")
    
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": title
                },
                "template": color
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": content
                }
            ]
        }
    }
    
    if WEBHOOK_SECRET:
        timestamp, sign = gen_sign(WEBHOOK_SECRET)
        payload["timestamp"] = timestamp
        payload["sign"] = sign
    
    resp = requests.post(WEBHOOK_URL, json=payload)
    resp.raise_for_status()
    return resp.json()

def main():
    parser = argparse.ArgumentParser(description="发送飞书消息")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 文本消息
    text_parser = subparsers.add_parser("text", help="发送文本消息")
    text_parser.add_argument("content", help="消息内容")
    text_parser.add_argument("--at", help="@用户 ID")
    
    # 富文本消息
    post_parser = subparsers.add_parser("post", help="发送富文本消息")
    post_parser.add_argument("title", help="标题")
    post_parser.add_argument("content", nargs="+", help="内容行")
    
    # 卡片消息
    card_parser = subparsers.add_parser("card", help="发送卡片消息")
    card_parser.add_argument("title", help="卡片标题")
    card_parser.add_argument("content", help="卡片内容（Markdown）")
    card_parser.add_argument("--color", default="blue", help="卡片颜色")
    
    args = parser.parse_args()
    
    try:
        if args.command == "text":
            result = send_text(args.content, args.at)
        elif args.command == "post":
            result = send_post(args.title, args.content)
        elif args.command == "card":
            result = send_card(args.title, args.content, args.color)
        else:
            parser.print_help()
            return
        
        if result.get("code") == 0:
            print("消息发送成功")
        else:
            print(f"发送失败：{result.get('msg')}")
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
| 自建应用 | 改应用凭证 |
| 工作流 | 无需修改 |

### 对比

| 维度 | 连接器 | Skill |
|------|--------|-------|
| 鉴权 | 平台托管 | 用户自管 |
| 消息类型 | 固定 | 可自定义模板 |
| 多步编排 | 不支持 | 支持（查→发→记录） |
| 迁移 | 重配连接器 | 改 URL/凭证 |
