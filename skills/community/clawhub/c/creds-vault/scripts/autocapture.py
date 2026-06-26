#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
autocapture.py — 对话式凭证检测模块（默认不自动保存）

检测并报告凭证，但不自动写入文件。
需要调用方显式调用 save() 才真正持久化。

使用方式（AI 在对话中调用）:
  from autocapture import detect_creds, confirm_and_save

  # 仅检测，不保存
  results = detect_creds("AppID: wxd9f577d56948e564", context="微信公众号")
  if results:
      # 询问用户确认后再保存
      confirm_and_save(results)

  # 或直接 auto_save 模式（需显式传入）
  results = detect_creds(text, auto_save=True, context="...")
"""
import sys; sys.stdout.reconfigure(encoding='utf-8')
import os, json, stat, re
from datetime import datetime

SECRETS_FILE = os.path.expanduser("~/.openclaw/workspace/secrets.json")
AUDIT_FILE   = os.path.expanduser("~/.openclaw/workspace/secrets.audit.log")

FIELD_PATTERNS = {
    "appid":      re.compile(r'appid[\s:=\"]+([a-zA-Z0-9]{16,32})', re.I),
    "appsecret":  re.compile(r'appsecret[\s:=\"]+([a-f0-9]{32})', re.I),
    "api_key":    re.compile(
        r"(?:api_key|apikey|API_KEY)[\s:=\"]+([a-zA-Z0-9_\-]{20,80})"
        r"|"
        r"(?:OPENAI_API_KEY|CLAUDE_API_KEY|GITHUB_TOKEN)[\s:=\"]+([a-zA-Z0-9_\-]{20,100})",
        re.I
    ),
    "token":      re.compile(
        r"(?:token|TOKEN|bearer|BEARER)[\s:=\"]+([a-zA-Z0-9_\-\.]{20,100})",
        re.I
    ),
    "access_key": re.compile(r'(?:access_key|access-key|aws_access_key)[\s:=\"]+([A-Z0-9]{16,32})', re.I),
    "secret_key": re.compile(r'(?:secret_key|secret-key|aws_secret_key)[\s:=\"]+([a-zA-Z0-9/+=]{40})', re.I),
    "password":   re.compile(r'password[\s:=\"]+([^\s\"\'\\]{8,64})', re.I),
}

PLATFORM_PREFIXES = {
    r'\bwechat\b|\bweixin\b':    ('wechat',  'social'),
    r'\bgithub\b|\bgh_[a-zA-Z0-9]{20,}': ('github', 'dev'),
    r'\bopenai\b':                ('openai',  'dev'),
    r'\bclaude\b|\banthropic\b': ('claude',  'dev'),
    r'\baws\b|\bamazon\b|\bs3\b': ('aws',    'cloud'),
    r'\baliyun\b|\balibaba\b':   ('aliyun',  'cloud'),
    r'\bazure\b|\bmicrosoft\b':  ('azure',   'cloud'),
    r'\bsendgrid\b|\bmailchimp\b': ('email', 'marketing'),
    r'\bsms\b|短信':              ('sms',     'marketing'),
    r'\bclawhub\b':               ('clawhub', 'dev'),
    r'\bssh\b':                  ('ssh',     'dev'),
    r'\bmysql\b|\bpostgres\b|\bmongodb\b|\bredis\b': ('db', 'dev'),
}

def _audit(action, key=None, field=None, masked=None, success=True):
    entry = {"ts": datetime.now().isoformat(), "action": action,
             "key": key, "field": field, "value_masked": masked, "success": success}
    try:
        with open(AUDIT_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        os.chmod(AUDIT_FILE, stat.S_IRUSR | stat.S_IWUSR)
    except Exception:
        pass

def load():
    if os.path.exists(SECRETS_FILE):
        with open(SECRETS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"categories": ["social", "cloud", "dev", "marketing", "other"], "entries": {}}

def save(data):
    with open(SECRETS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.chmod(SECRETS_FILE, stat.S_IRUSR | stat.S_IWUSR)

def now():
    return datetime.now().isoformat()

def _mask(val):
    s = str(val)
    return (s[:6] + "..." + s[-4:]) if len(s) > 10 else s[:2] + "**"

def guess_platform(text: str):
    for pattern, (platform, category) in PLATFORM_PREFIXES.items():
        if re.search(pattern, text, re.I):
            return platform, category
    return "unknown", "other"

def detect_fields(text: str) -> dict:
    found = {}
    for field_name, pattern in FIELD_PATTERNS.items():
        m = pattern.search(text)
        if m:
            val = None
            for g in m.groups():
                if g is not None:
                    val = g; break
            if val:
                found[field_name] = val
    return found

def detect_creds(text: str, context: str = "",
                 default_key: str = None,
                 default_name: str = None,
                 default_category: str = None) -> list:
    """
    仅检测凭证，返回检测结果列表，不自动保存。
    返回格式: [{"key": ..., "name": ..., "field": ..., "value": ..., "value_masked": ..., "category": ...}]
    """
    fields = detect_fields(text)
    if not fields:
        return []

    combined = f"{text} {context}"

    if "appid" in fields or "appsecret" in fields:
        key, category, name = "wechat", "social", "微信公众号"
    elif "api_key" in fields:
        key_name_only = re.split(r'[=:\s]+', text)[0]
        platform_text = f"{key_name_only} {context}"
        guessed_key, guessed_cat = guess_platform(platform_text)
        if guessed_key != "unknown":
            key, category = guessed_key, guessed_cat
        else:
            key, category = "openai", "dev"
        name = key.title()
    elif "token" in fields:
        key, category = guess_platform(combined)
        if key == "unknown":
            key, category = "token", "other"
        name = key.title()
    elif "access_key" in fields or "secret_key" in fields:
        key, category = guess_platform(combined)
        if key == "unknown":
            key, category = "aws", "cloud"
        name = key.title()
    else:
        first_field = list(fields.keys())[0]
        key, category, name = first_field, "other", first_field.title()

    key = default_key or key
    name = default_name or name
    category = default_category or category

    results = []
    for field_name, value in fields.items():
        results.append({
            "key": key,
            "name": name,
            "field": field_name,
            "value": value,
            "value_masked": _mask(value),
            "category": category
        })

    return results

def confirm_and_save(results: list, confirmed: bool = False) -> list:
    """
    确认并保存检测到的凭证。
    若 confirmed=False（默认），仅打印预览，不保存。
    若 confirmed=True，才真正写入 secrets.json。
    返回已保存的结果列表。
    """
    if not results:
        return []

    for r in results:
        action = "已确认" if confirmed else "待确认"
        print(f"[{action}] [{r['key']}] {r['field']} = {r['value_masked']} ({r['category']})")

    if not confirmed:
        print("\n提示: 凭证尚未保存。AI 会话中如需保存，请回复「确认」。")
        return []

    # 真正保存
    data = load()
    for r in results:
        key = r["key"]
        if key not in data["entries"]:
            data["entries"][key] = {
                "name": r["name"],
                "category": r["category"],
                "fields": {},
                "expire_at": None,
                "note": "",
                "created_at": now()[:10],
                "read_count": 0,
                "last_read": None
            }
        data["entries"][key]["fields"][r["field"]] = r["value"]
        data["entries"][key]["last_read"] = now()
        _audit("autocapture", key, r["field"], r["value_masked"], True)

    save(data)
    print(f"\n[OK] 已保存 {len(results)} 个凭证到 secrets.json")
    return results

# ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="凭证检测工具（默认仅检测，不自动保存）")
    parser.add_argument("--text", help="从文本中检测凭证")
    parser.add_argument("--context", default="", help="上下文描述")
    parser.add_argument("--key", help="指定 key")
    parser.add_argument("--name", help="指定名称")
    parser.add_argument("--category", default=None,
                        choices=["social","cloud","dev","marketing","other"])
    parser.add_argument("--list", dest="do_list", action="store_true", help="列出已保存凭证")
    parser.add_argument("--save", dest="do_save", action="store_true",
                        help="确认保存（与 --text 一起使用，否则仅检测）")
    args = parser.parse_args()

    if args.do_list:
        data = load()
        entries = data.get("entries", {})
        if not entries:
            print("暂无保存的凭证")
        else:
            for key, info in entries.items():
                print(f"\n[{key}] {info.get('name', key)} ({info.get('category')})")
                for f, v in info.get("fields", {}).items():
                    print(f"  {f}: {_mask(v)}")
        sys.exit(0)

    if args.text:
        results = detect_creds(
            args.text, context=args.context,
            default_key=args.key, default_name=args.name,
            default_category=args.category
        )
        if results:
            print(f"\n检测到 {len(results)} 个凭证：")
            confirm_and_save(results, confirmed=args.do_save)
        else:
            print("[!] 未检测到任何凭证")
        sys.exit(0)

    parser.print_help()
