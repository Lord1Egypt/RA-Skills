# -*- coding: utf-8 -*-
"""
Data+AI Daily Brief — Slack 推送脚本
通过 Slack Incoming Webhook 推送日报。

用法:
  python send_slack.py                        # 推送今天的日报
  python send_slack.py 2026-03-10             # 推送指定日期

环境变量:
  SLACK_WEBHOOK_URL — Slack Incoming Webhook URL

配置指南:
  1. 访问 https://api.slack.com/apps → 创建 App
  2. Features → Incoming Webhooks → 启用 → Add New Webhook
  3. 选择目标频道 → 复制 Webhook URL
  4. 配置到环境变量或 daily-brief-config.json
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
    env_url = os.environ.get("SLACK_WEBHOOK_URL")
    if env_url: return env_url
    url = load_config().get("adapters", {}).get("slack", {}).get("webhook_url", "")
    if url: return url
    print("[错误] 未配置 Slack Webhook URL"); sys.exit(1)

def find_file(date_str, ext, search_dirs=None):
    if search_dirs is None: search_dirs = [PROJECT_DIR, Path(".")]
    for d in search_dirs:
        for p in [f"Data+AI全球日报_{date_str}.{ext}", f"Data+AI全球日报_{date_str}_v3.{ext}", f"Data+AI全球日报_{date_str}_v2.{ext}"]:
            path = d / p
            if path.exists(): return path
    return None

def extract_summary(md_path):
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
    return "\n".join(summary).strip()

def md_to_mrkdwn(md_text, max_chars=3000):
    """转换为 Slack mrkdwn 格式（*粗体*, _斜体_, <url|文本>）"""
    lines, result = md_text.split("\n"), []
    for line in lines:
        s = line.strip()
        if s.startswith("# "): result.append(f"*{s.lstrip('# ').strip()}*")
        elif s.startswith("## "): result.append(f"\n*{s.lstrip('# ').strip()}*")
        elif s.startswith("### "): result.append(f"*{s.lstrip('# ').strip()}*")
        elif s.startswith("> "): result.append(f">{s[2:]}")
        elif s.startswith("---"): result.append("─" * 30)
        else:
            c = re.sub(r'\*\*(.+?)\*\*', r'*\1*', s)
            c = re.sub(r'\[(.+?)\]\((.+?)\)', r'<\2|\1>', c)
            result.append(c)
    text = "\n".join(result).strip()
    return text[:max_chars] if len(text) <= max_chars else text[:max_chars-30] + "\n...(已截断)"

def build_blocks(title, mrkdwn_text, link_url=None):
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": title, "emoji": True}},
        {"type": "divider"},
        {"type": "section", "text": {"type": "mrkdwn", "text": mrkdwn_text[:3000]}},
    ]
    if link_url:
        blocks.append({"type": "actions", "elements": [{"type": "button", "text": {"type": "plain_text", "text": "📖 查看完整日报"}, "url": link_url, "style": "primary"}]})
    blocks.append({"type": "context", "elements": [{"type": "mrkdwn", "text": f"_Data+AI Daily Brief · {datetime.now().strftime('%Y-%m-%d %H:%M')}_"}]})
    return blocks

def send_webhook(webhook_url, text, blocks=None):
    payload = {"text": text}
    if blocks: payload["blocks"] = blocks
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    print(f"  长度: {len(text)} 字符")
    req = urllib.request.Request(webhook_url, data=data, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"  [推送] 响应: {resp.read().decode('utf-8')}")
    except urllib.error.HTTPError as e:
        print(f"  [失败] HTTP {e.code}: {e.read().decode('utf-8')}"); sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Data+AI 日报 Slack 推送")
    parser.add_argument("date", nargs="?", default=None, help="日期 YYYY-MM-DD")
    parser.add_argument("--webhook", help="Slack Webhook URL")
    parser.add_argument("--link-url", help="日报公开链接")
    parser.add_argument("--search-dir", action="append", help="额外搜索目录")
    args = parser.parse_args()
    date_str = args.date or datetime.now().strftime("%Y-%m-%d")

    webhook_url = get_webhook_url(args.webhook)
    search_dirs = [PROJECT_DIR, Path(".")]
    if args.search_dir: search_dirs.extend(Path(d) for d in args.search_dir)

    print(f"{'='*55}\n  Data+AI Daily Brief — Slack 推送\n  日期: {date_str}\n{'='*55}")
    md_path = find_file(date_str, "md", search_dirs)
    if not md_path: print(f"[错误] 未找到 {date_str} 的日报文件"); sys.exit(1)

    title = f"📊 Data+AI 全球日报 | {date_str}"
    mrkdwn = md_to_mrkdwn(extract_summary(md_path))
    blocks = build_blocks(title, mrkdwn, args.link_url)
    print(f"\n推送消息...")
    send_webhook(webhook_url, mrkdwn, blocks)
    print(f"\n{'='*55}\n  推送完成!\n{'='*55}")

if __name__ == "__main__":
    main()
