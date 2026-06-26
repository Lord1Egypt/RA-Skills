# -*- coding: utf-8 -*-
"""
Data+AI Daily Brief — Discord 推送脚本
通过 Discord Webhook 推送日报。

用法:
  python send_discord.py                      # 推送今天的日报
  python send_discord.py 2026-03-10           # 推送指定日期

环境变量:
  DISCORD_WEBHOOK_URL — Discord Webhook URL

配置指南:
  1. 频道 → 编辑频道(⚙️) → 整合 → Webhooks → 新建 Webhook
  2. 自定义名称和头像 → 复制 Webhook URL
  3. 配置到环境变量或 daily-brief-config.json
  4. 限制: Embed 描述 4096 字符, 消息 2000 字符, 每秒 5 次
"""
import json, urllib.request, urllib.error, os, sys, re, argparse
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_FILE = PROJECT_DIR / "daily-brief-config.json"

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return {}

def get_webhook_url(args_webhook=None):
    if args_webhook: return args_webhook
    env_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if env_url: return env_url
    url = load_config().get("adapters", {}).get("discord", {}).get("webhook_url", "")
    if url: return url
    print("[错误] 未配置 Discord Webhook URL"); sys.exit(1)

def find_file(date_str, ext, search_dirs=None):
    if search_dirs is None: search_dirs = [PROJECT_DIR, Path(".")]
    for d in search_dirs:
        for p in [f"Data+AI全球日报_{date_str}.{ext}", f"Data+AI全球日报_{date_str}_v3.{ext}", f"Data+AI全球日报_{date_str}_v2.{ext}"]:
            path = d / p
            if path.exists(): return path
    return None

def extract_summary(md_path, max_chars=3900):
    with open(md_path, "r", encoding="utf-8") as f: content = f.read()
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
    text = "\n".join(summary).strip()
    return text[:max_chars] if len(text) <= max_chars else text[:max_chars-30] + "\n...(已截断)"

def send_embed(webhook_url, title, description, date_str, link_url=None):
    embed = {
        "title": title, "description": description[:4096],
        "color": 3447003, "timestamp": f"{date_str}T08:00:00.000Z",
        "footer": {"text": "Data+AI Daily Brief Skill"},
        "author": {"name": "📊 Data+AI Global Daily Report"}
    }
    if link_url:
        embed["url"] = link_url
        embed["fields"] = [{"name": "🔗 完整版", "value": f"[点击查看]({link_url})", "inline": False}]
    payload = {"embeds": [embed]}
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    print(f"  大小: {len(data)} 字节")
    req = urllib.request.Request(webhook_url, data=data, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"  [推送] 状态: {resp.status}")
    except urllib.error.HTTPError as e:
        print(f"  [失败] HTTP {e.code}: {e.read().decode('utf-8')[:300]}")
        if e.code == 429: print("  达到频率限制，请稍后重试")
        sys.exit(1)

def send_file(webhook_url, filepath, content_text=""):
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f: file_data = f.read()
    boundary = "----DiscordBoundary"
    body = b""
    if content_text: body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"content\"\r\n\r\n{content_text}\r\n".encode("utf-8")
    body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{filename}\"\r\nContent-Type: text/html\r\n\r\n".encode("utf-8")
    body += file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(webhook_url, data=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}, method="POST")
    try:
        with urllib.request.urlopen(req) as resp: print(f"  [上传] 状态: {resp.status}")
    except urllib.error.HTTPError as e: print(f"  [上传失败] {e.code}")

def main():
    parser = argparse.ArgumentParser(description="Data+AI 日报 Discord 推送")
    parser.add_argument("date", nargs="?", default=None, help="日期 YYYY-MM-DD")
    parser.add_argument("--webhook", help="Discord Webhook URL")
    parser.add_argument("--link-url", help="日报公开链接")
    parser.add_argument("--upload-html", action="store_true", help="上传 HTML 文件")
    parser.add_argument("--search-dir", action="append", help="额外搜索目录")
    args = parser.parse_args()
    date_str = args.date or datetime.now().strftime("%Y-%m-%d")

    webhook_url = get_webhook_url(args.webhook)
    search_dirs = [PROJECT_DIR, Path(".")]
    if args.search_dir: search_dirs.extend(Path(d) for d in args.search_dir)

    print(f"{'='*55}\n  Data+AI Daily Brief — Discord 推送\n  日期: {date_str}\n{'='*55}")
    md_path = find_file(date_str, "md", search_dirs)
    if not md_path: print(f"[错误] 未找到 {date_str} 的日报文件"); sys.exit(1)

    title = f"📊 Data+AI 全球日报 | {date_str}"
    print(f"\n推送 Embed...")
    send_embed(webhook_url, title, extract_summary(md_path), date_str, args.link_url)

    if args.upload_html:
        html_path = find_file(date_str, "html", search_dirs)
        if html_path: print(f"上传 HTML..."); send_file(webhook_url, str(html_path), f"📎 {title}")
    print(f"\n{'='*55}\n  推送完成!\n{'='*55}")

if __name__ == "__main__":
    main()
