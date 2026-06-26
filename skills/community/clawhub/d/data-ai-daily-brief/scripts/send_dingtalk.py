# -*- coding: utf-8 -*-
"""
Data+AI Daily Brief — 钉钉推送脚本
通过钉钉群机器人 Webhook 推送日报。

用法:
  python send_dingtalk.py                     # 推送今天的日报
  python send_dingtalk.py 2026-03-10          # 推送指定日期
  python send_dingtalk.py --webhook <url>     # 自定义 webhook

环境变量:
  DINGTALK_WEBHOOK_URL — 钉钉 Webhook URL
  DINGTALK_SECRET      — 加签密钥（可选）

配置指南:
  1. 钉钉群 → 群设置 → 智能群助手 → 添加机器人 → 自定义
  2. 安全设置选一种:
     - 自定义关键词: 设 "日报" "Data" 等
     - 加签: 记下 Secret 配到 DINGTALK_SECRET
     - IP 白名单: 填服务器 IP
  3. 复制 Webhook URL 到环境变量或配置文件
  4. 限制: 每分钟最多 20 条消息
"""
import json, urllib.request, os, sys, re, time, hmac, hashlib, base64
import urllib.parse, argparse
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_FILE = PROJECT_DIR / "daily-brief-config.json"

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def get_webhook_url(args_webhook=None):
    if args_webhook: return args_webhook
    env_url = os.environ.get("DINGTALK_WEBHOOK_URL")
    if env_url: return env_url
    config = load_config()
    url = config.get("adapters", {}).get("dingtalk", {}).get("webhook_url", "")
    if url: return url
    print("[错误] 未配置钉钉 Webhook URL")
    print("  设置环境变量 DINGTALK_WEBHOOK_URL 或在配置文件中配置")
    sys.exit(1)

def get_secret():
    secret = os.environ.get("DINGTALK_SECRET")
    if secret: return secret
    return load_config().get("adapters", {}).get("dingtalk", {}).get("secret", "")

def sign_url(webhook_url, secret):
    if not secret: return webhook_url
    timestamp = str(round(time.time() * 1000))
    string_to_sign = f"{timestamp}\n{secret}"
    hmac_code = hmac.new(secret.encode("utf-8"), string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return f"{webhook_url}&timestamp={timestamp}&sign={sign}"

def find_file(date_str, ext, search_dirs=None):
    if search_dirs is None: search_dirs = [PROJECT_DIR, Path(".")]
    for d in search_dirs:
        for p in [f"Data+AI全球日报_{date_str}.{ext}", f"Data+AI全球日报_{date_str}_v3.{ext}", f"Data+AI全球日报_{date_str}_v2.{ext}"]:
            path = d / p
            if path.exists(): return path
    return None

def extract_summary(md_path, max_chars=18000):
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
    lines, summary, in_sec = content.split("\n"), [], False
    for line in lines:
        s = line.strip()
        if s.startswith("# "): summary.append(s); continue
        if s.startswith("## 今日") or s.startswith("## 🔥"): in_sec = True; summary += ["", s]; continue
        if in_sec:
            if s.startswith("## ") or s.startswith("---"): in_sec = False
            else: summary.append(line); continue
        if s.startswith("> 总判断") or s.startswith("> **总判断"): summary += ["", s]; continue
        if re.match(r"^## [A-E]\.", s) or re.match(r"^---$", s): summary += ["", s]; continue
        if re.match(r"^###\s+\d+\.", s): summary.append(re.sub(r"^###\s+", "", s)); continue
        if s.startswith("**") and any(c in s for c in "：:—"): summary.append(s); continue
        if re.match(r"^\d+\.\s+\*\*", s): summary.append(s); continue
    text = "\n".join(summary).strip() + f"\n\n> *截至 {datetime.now().strftime('%Y-%m-%d')} 08:00*"
    return text[:max_chars] if len(text) <= max_chars else text[:max_chars-30] + "\n\n...(已截断)"

def send_markdown(webhook_url, title, content):
    payload = {"msgtype": "markdown", "markdown": {"title": title, "text": content}}
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    print(f"  长度: {len(content)} 字符")
    req = urllib.request.Request(webhook_url, data=data, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        print(f"  errcode: {result.get('errcode')}, errmsg: {result.get('errmsg')}")
        return result

def send_link(webhook_url, title, text, message_url):
    payload = {"msgtype": "link", "link": {"title": title, "text": text, "messageUrl": message_url, "picUrl": ""}}
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(webhook_url, data=data, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        print(f"  [链接] errcode: {result.get('errcode')}")
        return result

def main():
    parser = argparse.ArgumentParser(description="Data+AI 日报钉钉推送")
    parser.add_argument("date", nargs="?", default=None, help="日期 YYYY-MM-DD")
    parser.add_argument("--webhook", help="钉钉 Webhook URL")
    parser.add_argument("--link-url", help="日报公开链接")
    parser.add_argument("--search-dir", action="append", help="额外搜索目录")
    args = parser.parse_args()
    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    if args.date:
        try: datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError: print(f"[错误] 日期格式无效: {args.date}"); sys.exit(1)

    webhook_url = get_webhook_url(args.webhook)
    secret = get_secret()
    signed_url = sign_url(webhook_url, secret)
    search_dirs = [PROJECT_DIR, Path(".")]
    if args.search_dir: search_dirs.extend(Path(d) for d in args.search_dir)

    print(f"{'='*55}\n  Data+AI Daily Brief — 钉钉推送\n  日期: {date_str} | 加签: {'是' if secret else '否'}\n{'='*55}")
    md_path = find_file(date_str, "md", search_dirs)
    if not md_path: print(f"[错误] 未找到 {date_str} 的日报文件"); sys.exit(1)

    title = f"Data+AI 全球日报 | {date_str}"
    print(f"\n推送 Markdown...")
    send_markdown(signed_url, title, extract_summary(md_path))
    if args.link_url:
        print(f"推送链接...")
        send_link(signed_url, title, "点击查看完整版日报", args.link_url)
    print(f"\n{'='*55}\n  推送完成!\n{'='*55}")

if __name__ == "__main__":
    main()
