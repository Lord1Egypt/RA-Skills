# -*- coding: utf-8 -*-
"""
Data+AI Daily Brief — Microsoft Teams 推送脚本
通过 Teams Incoming Webhook 推送日报。

用法:
  python send_teams.py                        # 推送今天的日报
  python send_teams.py 2026-03-10             # 推送指定日期

环境变量:
  TEAMS_WEBHOOK_URL — Teams Incoming Webhook URL

配置指南:
  方式 A: Workflows（新版 Teams 推荐）
  - 频道 → ··· → Workflows → "Post to a channel when a webhook request is received"
  方式 B: Incoming Webhook Connector（经典版）
  - 频道 → ··· → Connectors → Incoming Webhook → 配置
  限制: Adaptive Card ~28KB, 每秒约 4 次
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
    env_url = os.environ.get("TEAMS_WEBHOOK_URL")
    if env_url: return env_url
    url = load_config().get("adapters", {}).get("teams", {}).get("webhook_url", "")
    if url: return url
    print("[错误] 未配置 Teams Webhook URL"); sys.exit(1)

def find_file(date_str, ext, search_dirs=None):
    if search_dirs is None: search_dirs = [PROJECT_DIR, Path(".")]
    for d in search_dirs:
        for p in [f"Data+AI全球日报_{date_str}.{ext}", f"Data+AI全球日报_{date_str}_v3.{ext}", f"Data+AI全球日报_{date_str}_v2.{ext}"]:
            path = d / p
            if path.exists(): return path
    return None

def extract_summary(md_path, max_chars=5000):
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

def build_adaptive_card(title, summary, date_str, link_url=None):
    body = [
        {"type": "TextBlock", "text": title, "weight": "Bolder", "size": "Large", "wrap": True},
        {"type": "TextBlock", "text": f"生成: {datetime.now().strftime('%Y-%m-%d %H:%M')}", "isSubtle": True, "size": "Small"},
        {"type": "TextBlock", "text": summary, "wrap": True}
    ]
    actions = []
    if link_url: actions.append({"type": "Action.OpenUrl", "title": "📖 查看完整版", "url": link_url, "style": "positive"})
    card = {"type": "message", "attachments": [{"contentType": "application/vnd.microsoft.card.adaptive", "content": {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json", "type": "AdaptiveCard", "version": "1.4", "body": body
    }}]}
    if actions: card["attachments"][0]["content"]["actions"] = actions
    return card

def build_message_card(title, summary, link_url=None):
    card = {"@type": "MessageCard", "@context": "http://schema.org/extensions", "themeColor": "0076D7", "summary": title,
            "sections": [{"activityTitle": title, "text": summary, "markdown": True}]}
    if link_url: card["potentialAction"] = [{"@type": "OpenUri", "name": "查看完整版", "targets": [{"os": "default", "uri": link_url}]}]
    return card

def send_card(webhook_url, payload):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    print(f"  大小: {len(data)} 字节")
    req = urllib.request.Request(webhook_url, data=data, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            result = resp.read().decode("utf-8")
            print(f"  [推送] {'成功' if result == '1' or resp.status in (200,202) else result[:100]}")
    except urllib.error.HTTPError as e:
        print(f"  [失败] HTTP {e.code}: {e.read().decode('utf-8')[:300]}")
        if e.code == 429: print("  达到频率限制")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Data+AI 日报 Teams 推送")
    parser.add_argument("date", nargs="?", default=None, help="日期 YYYY-MM-DD")
    parser.add_argument("--webhook", help="Teams Webhook URL")
    parser.add_argument("--link-url", help="日报公开链接")
    parser.add_argument("--legacy", action="store_true", help="旧版 MessageCard 格式")
    parser.add_argument("--search-dir", action="append", help="额外搜索目录")
    args = parser.parse_args()
    date_str = args.date or datetime.now().strftime("%Y-%m-%d")

    webhook_url = get_webhook_url(args.webhook)
    search_dirs = [PROJECT_DIR, Path(".")]
    if args.search_dir: search_dirs.extend(Path(d) for d in args.search_dir)

    print(f"{'='*55}\n  Data+AI Daily Brief — Teams 推送\n  日期: {date_str} | 格式: {'MessageCard' if args.legacy else 'Adaptive Card'}\n{'='*55}")
    md_path = find_file(date_str, "md", search_dirs)
    if not md_path: print(f"[错误] 未找到 {date_str} 的日报文件"); sys.exit(1)

    title = f"📊 Data+AI 全球日报 | {date_str}"
    summary = extract_summary(md_path)
    print(f"\n推送消息...")
    card = build_message_card(title, summary, args.link_url) if args.legacy else build_adaptive_card(title, summary, date_str, args.link_url)
    send_card(webhook_url, card)
    print(f"\n{'='*55}\n  推送完成!\n{'='*55}")

if __name__ == "__main__":
    main()
