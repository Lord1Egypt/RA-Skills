#!/usr/bin/env python3
"""
Generic failure notification for book-to-learn.
Sends a webhook message (Feishu format) when any pipeline stage fails.

Usage:
  python notify_failure.py --book <slug> --stage <stage> --reason "<error>"
  python notify_failure.py --book <slug> --stage <stage> --reason "<error>" --config <config.json>

Reads notifyWebhook from config.json. Falls back to env BOOK_LEARN_WEBHOOK.
"""
import json, sys, os, argparse, urllib.request, datetime

def load_config(path):
    try:
        return json.load(open(path, encoding='utf-8'))
    except Exception:
        return {}

def send(webhook_url, book_title, stage, reason):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = (
        f"⚠️ Book-to-Learn 推送失败通知\n"
        f"时间：{now}\n"
        f"书名：{book_title}\n"
        f"失败阶段：{stage}\n"
        f"错误详情：{reason}\n\n"
        f"本次推送未完成，不计入进度。\n"
        f"请检查配置后重试，下次将自动重推同一张卡片。"
    )
    body = json.dumps({
        "msg_type": "text",
        "content": {"text": text}
    }, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(webhook_url, data=body, headers={
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "Mozilla/5.0"
    })
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.load(resp)
        ok = data.get("code") == 0 or data.get("StatusCode") == 0
        print(json.dumps({"sent": True, "ok": ok, "resp": data}, ensure_ascii=False))
        return 0 if ok else 1
    except Exception as e:
        print(json.dumps({"sent": False, "error": str(e)}, ensure_ascii=False))
        return 1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--book', required=True, help='book slug')
    ap.add_argument('--stage', required=True, help='failed stage: extract/translate/pdf/upload/feishu')
    ap.add_argument('--reason', required=True, help='error description')
    ap.add_argument('--config', help='config.json path')
    args = ap.parse_args()

    # resolve webhook + book title
    webhook = os.environ.get('BOOK_LEARN_WEBHOOK', '')
    book_title = args.book
    if args.config:
        cfg = load_config(args.config)
        webhook = cfg.get('notifyWebhook', webhook)
        book_title = cfg.get('bookTitle', book_title)
    if not webhook:
        print(json.dumps({"sent": False, "error": "no webhook configured (set notifyWebhook in config.json or BOOK_LEARN_WEBHOOK env)"}, ensure_ascii=False))
        sys.exit(1)
    sys.exit(send(webhook, book_title, args.stage, args.reason))

if __name__ == '__main__':
    main()
