#!/usr/bin/env python3
"""
法大大 FASC API 5.0 签名工具
用法: python3 fadada_sign.py <app_id> <app_secret>
"""
import hashlib
import time
import uuid
import json
import sys

def make_headers(app_id: str, app_secret: str) -> dict:
    """生成法大大 API 请求 Header"""
    msg_id = uuid.uuid4().hex.upper()
    timestamp = str(int(time.time()))
    raw = app_id + timestamp + msg_id + app_secret
    sign = hashlib.md5(raw.encode("utf-8")).hexdigest().upper()
    return {
        "AppId": app_id,
        "MsgId": msg_id,
        "Timestamp": timestamp,
        "Sign": sign,
        "Content-Type": "application/json"
    }

def verify_callback(app_id: str, app_secret: str, headers: dict) -> bool:
    """验证法大大回调签名"""
    msg_id = headers.get("MsgId", "")
    timestamp = headers.get("Timestamp", "")
    sign = headers.get("Sign", "")
    raw = app_id + timestamp + msg_id + app_secret
    expected = hashlib.md5(raw.encode("utf-8")).hexdigest().upper()
    return sign == expected

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python3 fadada_sign.py <app_id> <app_secret>")
        sys.exit(1)
    app_id = sys.argv[1]
    app_secret = sys.argv[2]
    headers = make_headers(app_id, app_secret)
    print(json.dumps(headers, ensure_ascii=False, indent=2))
