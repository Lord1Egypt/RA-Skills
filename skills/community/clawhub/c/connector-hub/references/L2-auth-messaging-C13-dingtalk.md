# C13 - 钉钉

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C13 |
| 连接器名 | dingtalk |
| 显示名 | 钉钉 |
| 层级 | L2 鉴权便利型 |
| 可替代 | ✅ 可替代（Skill） |
| 分类 | 消息/通讯 |
| 替代难度 | 简单 |

## 连接器能力

| 能力 | 说明 |
|------|------|
| 发送消息 | 文本/Markdown/ActionCard |
| 群组管理 | 创建/管理群组 |
| 机器人 | 自定义机器人 |
| 审批流 | 创建/查询审批 |
| 日历 | 日程管理 |

## Skill 替代方案

### 脚本位置

使用 connector-hub 技能中的脚本：

```
scripts/
├── L2-auth-messaging-C13-dingtalk-send-text.py
├── L2-auth-messaging-C13-dingtalk-send-markdown.py
└── L2-auth-messaging-C13-dingtalk-send-action-card.py
```

### 鉴权方式

**Webhook + 加签**：
1. 在钉钉群组添加自定义机器人
2. 获取 Webhook URL（格式：`https://oapi.dingtalk.com/robot/send?access_token={access_token}`）
3. 选择安全配置：自定义关键词、IP 白名单、加签（推荐）
4. 如果使用加签，获取密钥（secret）
5. 请求时携带签名和时间戳

**环境变量配置**：
```bash
export DINGTALK_WEBHOOK_URL="https://oapi.dingtalk.com/robot/send?access_token=xxx"
export DINGTALK_SECRET="SECxxxxxxxxxxxxxxxx"
```

### 核心脚本示例

**L2-auth-messaging-C13-dingtalk-send-text.py**：
```python
#!/usr/bin/env python3
"""发送钉钉文本消息"""

import os
import sys
import json
import time
import hmac
import hashlib
import base64
import argparse
import requests
from urllib.parse import quote_plus

WEBHOOK_URL = os.environ.get("DINGTALK_WEBHOOK_URL")
SECRET = os.environ.get("DINGTALK_SECRET")

def generate_sign() -> tuple:
    """生成签名"""
    if not SECRET:
        return None, None
    
    timestamp = str(round(time.time() * 1000))
    string_to_sign = f"{timestamp}\n{SECRET}"
    hmac_code = hmac.new(
        SECRET.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        digestmod=hashlib.sha256
    ).digest()
    sign = quote_plus(base64.b64encode(hmac_code))
    
    return timestamp, sign

def send_text(content: str, at_mobiles: list = None, at_all: bool = False) -> dict:
    """发送文本消息"""
    if not WEBHOOK_URL:
        raise ValueError("未设置 DINGTALK_WEBHOOK_URL 环境变量")
    
    # 构建请求 URL
    url = WEBHOOK_URL
    if SECRET:
        timestamp, sign = generate_sign()
        url = f"{url}&timestamp={timestamp}&sign={sign}"
    
    # 构建请求体
    payload = {
        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {
            "isAtAll": at_all
        }
    }
    
    if at_mobiles:
        payload["at"]["atMobiles"] = at_mobiles
    
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    
    return resp.json()

def send_markdown(title: str, text: str, at_mobiles: list = None, at_all: bool = False) -> dict:
    """发送 Markdown 消息"""
    if not WEBHOOK_URL:
        raise ValueError("未设置 DINGTALK_WEBHOOK_URL 环境变量")
    
    # 构建请求 URL
    url = WEBHOOK_URL
    if SECRET:
        timestamp, sign = generate_sign()
        url = f"{url}&timestamp={timestamp}&sign={sign}"
    
    # 构建请求体
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": text
        },
        "at": {
            "isAtAll": at_all
        }
    }
    
    if at_mobiles:
        payload["at"]["atMobiles"] = at_mobiles
    
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    
    return resp.json()

def send_action_card(title: str, text: str, buttons: list) -> dict:
    """发送 ActionCard 消息"""
    if not WEBHOOK_URL:
        raise ValueError("未设置 DINGTALK_WEBHOOK_URL 环境变量")
    
    # 构建请求 URL
    url = WEBHOOK_URL
    if SECRET:
        timestamp, sign = generate_sign()
        url = f"{url}&timestamp={timestamp}&sign={sign}"
    
    # 构建请求体
    payload = {
        "msgtype": "actionCard",
        "actionCard": {
            "title": title,
            "text": text,
            "btnOrientation": "0",
            "btns": buttons
        }
    }
    
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    
    return resp.json()

def main():
    parser = argparse.ArgumentParser(description="发送钉钉消息")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 文本消息
    text_parser = subparsers.add_parser("text", help="文本消息")
    text_parser.add_argument("content", help="消息内容")
    text_parser.add_argument("--at-mobiles", nargs="+", help="@手机号")
    text_parser.add_argument("--at-all", action="store_true", help="@所有人")
    
    # Markdown 消息
    md_parser = subparsers.add_parser("markdown", help="Markdown 消息")
    md_parser.add_argument("title", help="消息标题")
    md_parser.add_argument("text", help="Markdown 内容")
    md_parser.add_argument("--at-mobiles", nargs="+", help="@手机号")
    md_parser.add_argument("--at-all", action="store_true", help="@所有人")
    
    # ActionCard 消息
    card_parser = subparsers.add_parser("action-card", help="ActionCard 消息")
    card_parser.add_argument("title", help="消息标题")
    card_parser.add_argument("text", help="消息内容")
    card_parser.add_argument("--buttons", required=True, help="按钮列表（JSON 格式）")
    
    args = parser.parse_args()
    
    try:
        if args.command == "text":
            result = send_text(args.content, args.at_mobiles, args.at_all)
        elif args.command == "markdown":
            result = send_markdown(args.title, args.text, args.at_mobiles, args.at_all)
        elif args.command == "action-card":
            buttons = json.loads(args.buttons)
            result = send_action_card(args.title, args.text, buttons)
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
| 加签密钥 | 更新 secret |
| 工作流 | 无需修改 |

### 对比

| 维度 | 连接器 | Skill |
|------|--------|-------|
| 鉴权 | 平台托管 | 用户自管 |
| 消息类型 | 固定 | 可自定义模板 |
| 多步编排 | 不支持 | 支持 |
| 迁移 | 重配连接器 | 改 URL/密钥 |
