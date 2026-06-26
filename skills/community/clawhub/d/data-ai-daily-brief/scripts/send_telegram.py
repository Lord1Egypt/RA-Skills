# -*- coding: utf-8 -*-
"""
Data+AI Daily Brief — Telegram 推送脚本
通过 Telegram Bot API 推送日报。

用法:
  python send_telegram.py                     # 推送今天的日报
  python send_telegram.py 2026-03-10          # 推送指定日期

环境变量:
  TELEGRAM_BOT_TOKEN — Bot Token（@BotFather 获取）
  TELEGRAM_CHAT_ID   — 目标 Chat ID

配置指南:
  1. Telegram 搜索 @BotFather → /newbot → 获取 Token
  2. 获取 Chat ID:
     - 群组: 添加 @userinfobot 或用 getUpdates API
     - 频道: @频道用户名 或数字 ID（Bot 需为管理员）
     - 个人: 发消息给 @userinfobot
  3. 限制: 消息 4096 字符, 每秒 30 条, 群每分钟 20 条
"""
import json, urllib.request, urllib.error, os, sys, re, argparse
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
CONFIG_FILE = PROJECT_DIR / "daily-brief-config.json"
TG_API = "https://api.telegram.org"

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f: return json.load(f)
    return {}

def get_config():
    cfg = load_config().get("adapters", {}).get("telegram", {})
    token = os.environ.get("TELEGRAM_BOT_TOKEN") or cfg.get("bot_token", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID") or cfg.get("chat_id", "")
    if not token: print("[错误] 未配置 TELEGRAM_BOT_TOKEN"); sys.exit(1)
    if not chat_id: print("[错误] 未配置 TELEGRAM_CHAT_ID"); sys.exit(1)
    return token, str(chat_id)

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

def md_to_html(md_text):
    """转为 Telegram HTML: <b>粗体</b>, <i>斜体</i>, <a href="">链接</a>"""
    lines, result = md_text.split("\n"), []
    for line in lines:
        s = line.strip()
        esc = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if s.startswith("# "):
            t = s.lstrip("# ").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            result.append(f"<b>{t}</b>")
        elif s.startswith("## "):
            t = s.lstrip("# ").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            result.append(f"\n<b>{t}</b>")
        elif s.startswith("### "):
            t = s.lstrip("# ").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            result.append(f"<b>{t}</b>")
        elif s.startswith("> "):
            t = s[2:].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            result.append(f"💡 <i>{t}</i>")
        elif s.startswith("---"):
            result.append("─" * 20)
        else:
            c = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', esc)
            c = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', c)
            result.append(c)
    return "\n".join(result).strip()

def split_msg(text, max_len=4000):
    if len(text) <= max_len: return [text]
    chunks, cur = [], ""
    for line in text.split("\n"):
        if len(cur) + len(line) + 1 > max_len:
            if cur: chunks.append(cur)
            cur = line
        else: cur = cur + "\n" + line if cur else line
    if cur: chunks.append(cur)
    return chunks

def send_msg(token, chat_id, text, parse_mode="HTML"):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode, "disable_web_page_preview": True}
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(f"{TG_API}/bot{token}/sendMessage", data=data, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            r = json.loads(resp.read().decode("utf-8"))
            print(f"  ok: {r.get('ok')}, msg_id: {r.get('result',{}).get('message_id','N/A')}")
            return r
    except urllib.error.HTTPError as e:
        err = json.loads(e.read().decode("utf-8"))
        print(f"  [失败] {e.code}: {err.get('description','')}")
        if e.code == 400 and "parse" in err.get("description", "").lower():
            print("  [重试] 纯文本模式...")
            return send_msg(token, chat_id, text, parse_mode=None)
        sys.exit(1)

def send_doc(token, chat_id, filepath, caption=""):
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f: file_data = f.read()
    boundary = "----TGBoundary"
    body = f"--{boundary}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{chat_id}\r\n".encode("utf-8")
    if caption: body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"caption\"\r\n\r\n{caption}\r\n".encode("utf-8")
    body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"document\"; filename=\"{filename}\"\r\nContent-Type: text/html\r\n\r\n".encode("utf-8")
    body += file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(f"{TG_API}/bot{token}/sendDocument", data=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"  [文件] ok: {json.loads(resp.read().decode('utf-8')).get('ok')}")
    except urllib.error.HTTPError as e: print(f"  [上传失败] {e.code}")

def main():
    parser = argparse.ArgumentParser(description="Data+AI 日报 Telegram 推送")
    parser.add_argument("date", nargs="?", default=None, help="日期 YYYY-MM-DD")
    parser.add_argument("--link-url", help="日报公开链接")
    parser.add_argument("--upload-html", action="store_true", help="上传 HTML 文件")
    parser.add_argument("--search-dir", action="append", help="额外搜索目录")
    args = parser.parse_args()
    date_str = args.date or datetime.now().strftime("%Y-%m-%d")
    token, chat_id = get_config()
    search_dirs = [PROJECT_DIR, Path(".")]
    if args.search_dir: search_dirs.extend(Path(d) for d in args.search_dir)

    print(f"{'='*55}\n  Data+AI Daily Brief — Telegram 推送\n  日期: {date_str}\n{'='*55}")
    md_path = find_file(date_str, "md", search_dirs)
    if not md_path: print(f"[错误] 未找到 {date_str} 的日报文件"); sys.exit(1)

    html_text = md_to_html(extract_summary(md_path))
    if args.link_url: html_text += f'\n\n🔗 <a href="{args.link_url}">查看完整版日报</a>'
    html_text += f"\n\n<i>截至 {datetime.now().strftime('%Y-%m-%d')} 08:00</i>"

    chunks = split_msg(html_text)
    print(f"\n推送消息（{len(chunks)} 段）...")
    for i, chunk in enumerate(chunks):
        print(f"  段 {i+1}/{len(chunks)} ({len(chunk)} 字符):")
        send_msg(token, chat_id, chunk)

    if args.upload_html:
        html_path = find_file(date_str, "html", search_dirs)
        if html_path: print(f"上传 HTML..."); send_doc(token, chat_id, str(html_path), f"📊 Data+AI 全球日报 | {date_str}")
    print(f"\n{'='*55}\n  推送完成!\n{'='*55}")

if __name__ == "__main__":
    main()
