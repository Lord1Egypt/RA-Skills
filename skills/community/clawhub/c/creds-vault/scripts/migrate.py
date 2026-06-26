#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""迁移旧格式 secrets.json 到 v2 格式"""
import sys; sys.stdout.reconfigure(encoding='utf-8')
import os, json, stat
from datetime import datetime

SECRETS_FILE = os.path.expanduser("~/.openclaw/workspace/secrets.json")

def load():
    if os.path.exists(SECRETS_FILE):
        with open(SECRETS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"categories": [], "entries": {}}

def save(data):
    with open(SECRETS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.chmod(SECRETS_FILE, stat.S_IRUSR | stat.S_IWUSR)

def guess_category(key, name):
    social = ["wechat", "weixin", "wx", "微博", "微信", "twitter", "tweet", "facebook", "fb", "instagram", "ig", "telegram", "tg", "discord"]
    cloud = ["aws", "azure", "gcp", "alibaba", "aliyun", "tencent", "qcloud", "huawei", "cloud"]
    dev = ["github", "gitlab", "gitea", "bitbucket", "openai", "claude", "anthropic", "api", "token", "key"]
    marketing = ["mailchimp", "sendgrid", "sms", "aliyun sms", "tencent sms"]

    key_lower = key.lower()
    name_lower = name.lower()

    for k in social:
        if k in key_lower or k in name_lower:
            return "social"
    for k in cloud:
        if k in key_lower or k in name_lower:
            return "cloud"
    for k in dev:
        if k in key_lower or k in name_lower:
            return "dev"
    for k in marketing:
        if k in key_lower or k in name_lower:
            return "marketing"
    return "other"

def migrate():
    data = load()

    # 如果已经是 v2 格式（有 categories 和 entries），跳过
    if "categories" in data and "entries" in data:
        print("[OK] 已经是 v2 格式，无需迁移")
        return

    # 旧格式直接是 {key: {name, appid, appsecret, ...}}
    old_entries = {k: v for k, v in data.items() if isinstance(v, dict) and "name" in v}
    if not old_entries:
        print("[OK] 空文件，初始化为 v2 格式")
    else:
        print(f"发现 {len(old_entries)} 个旧格式条目，开始迁移...")

    # 构建 v2 格式
    v2 = {
        "categories": ["social", "cloud", "dev", "marketing", "other"],
        "entries": {}
    }

    now = datetime.now().isoformat()

    for key, old in old_entries.items():
        # 分离 fields 和 meta
        fields = {}
        meta = {}
        for k, v in old.items():
            if k in ("name", "category", "expire_at", "note", "created_at", "read_count", "last_read"):
                meta[k] = v
            else:
                fields[k] = v

        category = meta.get("category") or guess_category(key, meta.get("name", ""))

        entry = {
            "name": meta.get("name", key),
            "category": category,
            "fields": fields,
            "expire_at": meta.get("expire_at"),
            "note": meta.get("note", ""),
            "created_at": meta.get("created_at", now[:10]),
            "read_count": meta.get("read_count", 0),
            "last_read": meta.get("last_read")
        }
        v2["entries"][key] = entry
        print(f"  迁移: [{key}] {entry['name']} → 分类:{category}")

    save(v2)
    print(f"\n[OK] 迁移完成，共 {len(v2['entries'])} 个令牌")

if __name__ == "__main__":
    migrate()
