# -*- coding: utf-8 -*-
"""
Data+AI Daily Brief — 飞书推送脚本
通过飞书群机器人 Webhook 推送日报。

用法:
  python send_feishu.py                       # 推送今天的日报
  python send_feishu.py 2026-03-10            # 推送指定日期
  python send_feishu.py --webhook <url>       # 自定义 webhook

环境变量:
  FEISHU_WEBHOOK_URL — 飞书 Webhook URL
  FEISHU_SECRET      — 签名密钥（可选）

配置指南:
  1. 飞书群 → 设置 → 群机器人 → 添加机器人 → 自定义机器人
  2. 安全设置:
     - 签名校验: 记下 Secret → FEISHU_SECRET（推荐）
     - 自定义关键词: 设 "日报" "Data" 等
     - IP 白名单: 填服务器 IP
  3. 复制 Webhook URL 到环境变量或配置文件
  4. 限制: 每分钟 5 条, 每小时 100 条
"""
import json, urllib.request, os, sys, re, time, hmac, hashlib, base64, argparse
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
    env_url = os.environ.get("FEISHU_WEBHOOK_URL")
    if env_url: return env_url
    url = load_config().get("adapters", {}).get("feishu", {}).get("webhook_url", "")
    if url: return url
    print("[错误] 未配置飞书 Webhook URL"); sys.exit(1)

def get_secret():
    s = os.environ.get("FEISHU_SECRET")
    if s: return s
    return load_config().get("adapters", {}).get("feishu", {}).get("secret", "")

def gen_sign(secret):
    if not secret: return None, None
    timestamp = str(int(time.time()))
    hmac_code = hmac.new(f"{timestamp}\n{secret}".encode("utf-8"), digestmod=hashlib.sha256).digest()
    return timestamp, base64.b64encode(hmac_code).decode("utf-8")

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
    text = "\n".join(summary).strip() + f"\n\n> *截至 {datetime.now().strftime('%Y-%m-%d')} 08:00*"
    return text[:max_chars] if len(text) <= max_chars else text[:max_chars-30] + "\n\n...(已截断)"

def md_to_post_content(md_text):
    """将 Markdown 转为飞书 post 富文本格式。"""
    lines, content_lines = md_text.split("\n"), []
    for line in lines:
        s = line.strip()
        if not s: continue
        if s.startswith("# "):
            content_lines.append([{"tag": "text", "text": s.lstrip("# ").strip(), "style": ["bold"]}])
        elif s.startswith("## "):
            content_lines.append([{"tag": "text", "text": f"\n📌 {s.lstrip('# ').strip()}", "style": ["bold"]}])
        elif s.startswith("### "):
            content_lines.append([{"tag": "text", "text": f"  {s.lstrip('# ').strip()}", "style": ["bold"]}])
        elif s.startswith("> "):
            content_lines.append([{"tag": "text", "text": f"💡 {s[2:].strip()}"}])
        elif s.startswith("---"):
            content_lines.append([{"tag": "text", "text": "─" * 20}])
        else:
            content_lines.append([{"tag": "text", "text": s}])
    return content_lines

def send_post(webhook_url, title, md_content, secret=""):
    payload = {"msg_type": "post", "content": {"post": {"zh_cn": {"title": title, "content": md_to_post_content(md_content)}}}}
    if secret:
        ts, sign = gen_sign(secret)
        if ts: payload["timestamp"] = ts; payload["sign"] = sign
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    print(f"  长度: {len(md_content)} 字符")
    req = urllib.request.Request(webhook_url, data=data, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        print(f"  code: {result.get('code', result.get('StatusCode', -1))}")
        return result

def send_card(webhook_url, title, summary, link_url, secret=""):
    """推送飞书交互卡片（含按钮）。"""
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {"title": {"tag": "plain_text", "content": title}, "template": "blue"},
            "elements": [
                {"tag": "markdown", "content": summary[:2000]},
                {"tag": "action", "actions": [{"tag": "button", "text": {"tag": "plain_text", "content": "📖 查看完整日报"}, "type": "primary", "url": link_url}]}
            ]
        }
    }
    if secret:
        ts, sign = gen_sign(secret)
        if ts: payload["timestamp"] = ts; payload["sign"] = sign
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(webhook_url, data=data, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        print(f"  [卡片] code: {result.get('code', -1)}")
        return result

def main():
    parser = argparse.ArgumentParser(description="Data+AI 日报飞书推送")
    parser.add_argument("date", nargs="?", default=None, help="日期 YYYY-MM-DD")
    parser.add_argument("--webhook", help="飞书 Webhook URL")
    parser.add_argument("--link-url", help="日报公开链接")
    parser.add_argument("--card", action="store_true", help="交互卡片模式（需 --link-url）")
    parser.add_argument("--search-dir", action="append", help="额外搜索目录")
    args = parser.parse_args()
    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    if args.date:
        try: datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError: print(f"[错误] 日期格式无效"); sys.exit(1)

    webhook_url = get_webhook_url(args.webhook)
    secret = get_secret()
    search_dirs = [PROJECT_DIR, Path(".")]
    if args.search_dir: search_dirs.extend(Path(d) for d in args.search_dir)

    print(f"{'='*55}\n  Data+AI Daily Brief — 飞书推送\n  日期: {date_str} | 签名: {'是' if secret else '否'} | 模式: {'卡片' if args.card else '富文本'}\n{'='*55}")
    md_path = find_file(date_str, "md", search_dirs)
    if not md_path: print(f"[错误] 未找到 {date_str} 的日报文件"); sys.exit(1)

    title = f"📊 Data+AI 全球日报 | {date_str}"
    summary = extract_summary(md_path)
    if args.card and args.link_url:
        print(f"\n推送交互卡片..."); send_card(webhook_url, title, summary, args.link_url, secret)
    else:
        print(f"\n推送富文本..."); send_post(webhook_url, title, summary, secret)
    print(f"\n{'='*55}\n  推送完成!\n{'='*55}")

if __name__ == "__main__":
    main()
