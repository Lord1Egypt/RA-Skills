#!/usr/bin/env python3
"""
Feishu Card Sender - Send interactive cards directly via Feishu Open API

Author: OpenClaw Community
Version: 1.1.0
"""

import json
import argparse
import requests
import os
import sys
from typing import Optional, List, Dict

APP_ID = os.environ.get("FEISHU_APP_ID", "cli_a9f13ef641f8dcd9")
APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "z7Aq63KvIUJNVRA5UbtOkd48on8rmA26")


class FeishuCardSender:
    def __init__(self, app_id=None, app_secret=None):
        self.app_id = app_id or APP_ID
        self.app_secret = app_secret or APP_SECRET
        self._token = None
    
    def get_token(self):
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        resp = requests.post(url, json={"app_id": self.app_id, "app_secret": self.app_secret})
        result = resp.json()
        if result.get("code") == 0:
            self._token = result.get("tenant_access_token")
            return self._token
        raise Exception(f"Token error: {result.get('msg')}")
    
    def build_card(self, title, content, buttons=None, template="blue", note=None):
        elements = [{"tag": "div", "text": {"tag": "plain_text", "content": content}}]
        if buttons:
            actions = []
            for i, btn in enumerate(buttons):
                actions.append({
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": btn},
                    "type": "primary" if i == 0 else "default",
                    "url": f"https://example.com/{btn}"
                })
            elements.append({"tag": "action", "actions": actions})
        if note:
            elements.append({"tag": "note", "elements": [{"tag": "plain_text", "content": "ℹ️ "}, {"tag": "plain_text", "content": note}]})
        return {"config": {"wide_screen_mode": True}, "header": {"tag": "header", "title": {"tag": "plain_text", "content": title}, "template": template}, "elements": elements}
    
    def send(self, recipient_id, recipient_type="open_id", title="", content="", buttons=None, template="blue", note=None):
        if not self._token:
            self.get_token()
        card = self.build_card(title, content, buttons, template, note)
        msg = {"receive_id": recipient_id, "msg_type": "interactive", "content": json.dumps(card, ensure_ascii=False)}
        id_type = recipient_type if recipient_type == "chat_id" else "open_id"
        url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={id_type}"
        resp = requests.post(url, json=msg, headers={"Authorization": f"Bearer {self._token}", "Content-Type": "application/json"})
        result = resp.json()
        if result.get("code") == 0:
            return {"success": True, "message_id": result["data"]["message_id"]}
        raise Exception(f"Send error: {result.get('msg')}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--to", required=True)
    p.add_argument("--type", default="open_id", choices=["open_id", "user_id", "chat_id"])
    p.add_argument("--title", required=True)
    p.add_argument("--content", required=True)
    p.add_argument("--buttons", help="comma-separated")
    p.add_argument("--template", default="blue")
    p.add_argument("--note")
    args = p.parse_args()
    sender = FeishuCardSender()
    try:
        result = sender.send(args.to, args.type, args.title, args.content, args.buttons.split(",") if args.buttons else None, args.template, args.note)
        print(f"✅ Sent! {result}")
    except Exception as e:
        print(f"❌ {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
