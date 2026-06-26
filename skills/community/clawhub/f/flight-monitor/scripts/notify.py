#!/usr/bin/env python3
"""
notify.py — Mobile push notifications for flight price alerts.

Supports three free push services (configure one):
  - Bark       (iOS, install Bark app from App Store)
  - Server酱   (WeChat notification, Android & iOS, https://sct.ftqq.com)
  - PushDeer   (open source Android & iOS, https://www.pushdeer.com)

Usage:
    # Send a notification
    python notify.py --title "低价提醒" --body "北京→三亚 ¥500" --url "https://..."

    # Configure push service
    python notify.py --setup bark --key <YOUR_BARK_KEY>
    python notify.py --setup serverchan --key <YOUR_SENDKEY>
    python notify.py --setup pushdeer --key <YOUR_PUSHKEY>

    # Show current config
    python notify.py --status
"""

import argparse
import json
import sys
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

CONFIG_DIR = Path.home() / ".workbuddy" / "flight-monitor"
CONFIG_FILE = CONFIG_DIR / "notify_config.json"


# ── Config helpers ────────────────────────────────────────────────────────────

def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def save_config(cfg: dict):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


# ── Push backends ─────────────────────────────────────────────────────────────

def push_bark(key: str, title: str, body: str, url: str = None) -> bool:
    """
    Bark push (iOS only).
    API: https://bark.day.app/{key}/{title}/{body}?url=...
    """
    t = urllib.parse.quote(title, safe="")
    b = urllib.parse.quote(body, safe="")
    api_url = f"https://api.day.app/{key}/{t}/{b}"
    if url:
        api_url += "?url=" + urllib.parse.quote(url, safe="")
    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": "flight-monitor/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
            return result.get("code") == 200
    except Exception as e:
        print(f"  Bark error: {e}", file=sys.stderr)
        return False


def push_serverchan(key: str, title: str, body: str, url: str = None) -> bool:
    """
    Server酱 / ServerChan3 push (WeChat notification).
    API: https://sctapi.ftqq.com/{SENDKEY}.send
    """
    desp = body
    if url:
        desp += f"\n\n[立即预订]({url})"
    data = urllib.parse.urlencode({
        "title": title,
        "desp": desp,
    }).encode("utf-8")
    api_url = f"https://sctapi.ftqq.com/{key}.send"
    try:
        req = urllib.request.Request(api_url, data=data,
                                     headers={"Content-Type": "application/x-www-form-urlencoded"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
            return result.get("data", {}).get("errno", -1) == 0
    except Exception as e:
        print(f"  Server酱 error: {e}", file=sys.stderr)
        return False


def push_pushdeer(key: str, title: str, body: str, url: str = None) -> bool:
    """
    PushDeer push (open source, Android & iOS).
    API: https://api2.pushdeer.com/message/push
    """
    text = f"**{title}**\n\n{body}"
    if url:
        text += f"\n\n[立即预订]({url})"
    data = urllib.parse.urlencode({
        "pushkey": key,
        "title": title,
        "desp": text,
        "type": "markdown",
    }).encode("utf-8")
    api_url = "https://api2.pushdeer.com/message/push"
    try:
        req = urllib.request.Request(api_url, data=data,
                                     headers={"Content-Type": "application/x-www-form-urlencoded"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
            return result.get("code") == 0
    except Exception as e:
        print(f"  PushDeer error: {e}", file=sys.stderr)
        return False


# ── Main send function ────────────────────────────────────────────────────────

def send_notification(title: str, body: str, url: str = None) -> bool:
    """
    Send a push notification using the configured service.
    Returns True on success, False on failure.
    """
    cfg = load_config()
    service = cfg.get("service")

    if not service:
        print("⚠️  未配置推送服务。")
        print()
        print("请选择以下任一方式配置：")
        print()
        print("  【Bark】适合 iPhone 用户，App Store 搜索 Bark 安装后获取 Key：")
        print("    python scripts/notify.py --setup bark --key <YOUR_KEY>")
        print()
        print("  【Server酱】适合希望收到微信通知的用户，访问 https://sct.ftqq.com 获取 SendKey：")
        print("    python scripts/notify.py --setup serverchan --key <YOUR_SENDKEY>")
        print()
        print("  【PushDeer】开源推送，Android & iOS，访问 https://www.pushdeer.com 获取 Key：")
        print("    python scripts/notify.py --setup pushdeer --key <YOUR_KEY>")
        return False

    key = cfg.get("key", "")
    print(f"📤 正在通过 {service} 发送推送通知…")

    if service == "bark":
        ok = push_bark(key, title, body, url)
    elif service == "serverchan":
        ok = push_serverchan(key, title, body, url)
    elif service == "pushdeer":
        ok = push_pushdeer(key, title, body, url)
    else:
        print(f"  未知推送服务: {service}", file=sys.stderr)
        return False

    if ok:
        print(f"✅ 推送成功（{service}）")
    else:
        print(f"❌ 推送失败（{service}）— 请检查 Key 是否正确，或网络是否可用")
    return ok


# ── Setup ─────────────────────────────────────────────────────────────────────

def setup(service: str, key: str):
    valid = {"bark", "serverchan", "pushdeer"}
    if service not in valid:
        print(f"❌ 不支持的服务: {service}，可选: {', '.join(valid)}")
        sys.exit(1)
    cfg = load_config()
    cfg["service"] = service
    cfg["key"] = key
    save_config(cfg)
    print(f"✅ 已配置推送服务：{service}")
    print(f"   Key: {key[:6]}{'*' * max(0, len(key) - 6)}")
    print()
    print("发送测试推送…")
    ok = send_notification(
        "Flight Monitor 测试通知",
        "推送配置成功！机票低价时将通过此渠道通知您。",
    )
    if not ok:
        print("⚠️  测试推送失败，请检查 Key 是否正确。")


def show_status():
    cfg = load_config()
    if not cfg:
        print("未配置推送服务。运行 `python notify.py --setup <service> --key <key>` 配置。")
        return
    service = cfg.get("service", "未知")
    key = cfg.get("key", "")
    masked = key[:6] + "*" * max(0, len(key) - 6)
    print(f"推送服务：{service}")
    print(f"Key：{masked}")
    print(f"配置文件：{CONFIG_FILE}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Mobile push notification for flight alerts")
    parser.add_argument("--title", help="Notification title")
    parser.add_argument("--body", help="Notification body text")
    parser.add_argument("--url", help="URL to open when notification is tapped")
    parser.add_argument("--setup", metavar="SERVICE",
                        help="Configure push service: bark / serverchan / pushdeer")
    parser.add_argument("--key", help="API key / SendKey for the push service")
    parser.add_argument("--status", action="store_true", help="Show current push config")
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    if args.setup:
        if not args.key:
            print("❌ --setup requires --key")
            sys.exit(1)
        setup(args.setup, args.key)
        return

    if not args.title or not args.body:
        print("❌ --title and --body are required for sending notifications")
        parser.print_help()
        sys.exit(1)

    ok = send_notification(args.title, args.body, args.url)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    main()
