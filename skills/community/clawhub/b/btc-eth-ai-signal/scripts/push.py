"""Push trading report to Feishu, Telegram, Discord, and WeCom (企业微信)"""
import json, os, time, http.client, signal, urllib.request

def generate_report(timeout_sec=20):
    signal.signal(signal.SIGALRM, lambda x,y: (_ for _ in ()).throw(TimeoutError()))
    signal.alarm(timeout_sec)
    try:
        from advise import generate_full_report
        r = generate_full_report()
        signal.alarm(0)
        return r
    except:
        signal.alarm(0)
        return "⚠️ 报告生成超时，请检查网络"

CFG = os.path.join(os.path.dirname(__file__), "..", "config.json")

def load_config():
    with open(CFG) as f:
        return json.load(f)

# ── 各平台推送 ──

def push_feishu(cfg, text):
    """飞书消息推送"""
    f = cfg.get("feishu", {})
    if not f.get("app_id") or f["app_id"].startswith("your_"):
        return False, "飞书未配置"
    try:
        # Get token
        conn = http.client.HTTPSConnection("open.feishu.cn")
        body = json.dumps({"app_id": f["app_id"], "app_secret": f["secret"]})
        conn.request("POST", "/open-apis/auth/v3/tenant_access_token/internal", body, {"Content-Type": "application/json"})
        r = conn.getresponse()
        token = json.loads(r.read()).get("tenant_access_token") if r.status == 200 else None
        conn.close()
        if not token:
            return False, "飞书Token获取失败"
        
        conn = http.client.HTTPSConnection("open.feishu.cn")
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload = json.dumps({
            "receive_id": f["user_id"],
            "msg_type": "text",
            "content": json.dumps({"text": text})
        })
        conn.request("POST", "/open-apis/im/v1/messages?receive_id_type=open_id", payload, headers)
        r = conn.getresponse()
        conn.close()
        return r.status == 200, "飞书OK" if r.status == 200 else f"飞书HTTP {r.status}"
    except Exception as e:
        return False, f"飞书异常: {e}"

def push_telegram(cfg, text):
    """Telegram Bot 推送"""
    t = cfg.get("telegram", {})
    if not t.get("bot_token") or t["bot_token"].startswith("your_"):
        return False, "Telegram未配置"
    try:
        # TG消息不能太长，截断
        msg = text[:3000] if len(text) > 3000 else text
        url = f"https://api.telegram.org/bot{t['bot_token']}/sendMessage"
        data = json.dumps({"chat_id": t["chat_id"], "text": msg, "parse_mode": "Markdown"}).encode()
        r = urllib.request.urlopen(urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}), timeout=10)
        return r.status == 200, "Telegram OK" if r.status == 200 else f"TG HTTP {r.status}"
    except Exception as e:
        return False, f"TG异常: {e}"

def push_discord(cfg, text):
    """Discord Webhook 推送"""
    d = cfg.get("discord", {})
    if not d.get("webhook_url") or d["webhook_url"].startswith("your_"):
        return False, "Discord未配置"
    try:
        msg = text[:1800] if len(text) > 1800 else text
        data = json.dumps({"content": f"```{msg}```"}).encode()
        r = urllib.request.urlopen(urllib.request.Request(d["webhook_url"], data=data, headers={"Content-Type": "application/json"}), timeout=10)
        return r.status == 204, "Discord OK"
    except Exception as e:
        return False, f"Discord异常: {e}"

def push_wecom(cfg, text):
    """企业微信机器人推送"""
    w = cfg.get("wecom", {})
    if not w.get("webhook_url") or w["webhook_url"].startswith("your_"):
        return False, "企业微信未配置"
    try:
        msg = text[:2000] if len(text) > 2000 else text
        data = json.dumps({"msgtype": "text", "text": {"content": msg}}).encode()
        r = urllib.request.urlopen(urllib.request.Request(w["webhook_url"], data=data, headers={"Content-Type": "application/json"}), timeout=10)
        return r.status == 200, "企微OK"
    except Exception as e:
        return False, f"企微异常: {e}"

def main():
    cfg = load_config()
    report = generate_report()
    
    results = []
    platforms = [
        ("飞书", push_feishu),
        ("Telegram", push_telegram),
        ("Discord", push_discord),
        ("企业微信", push_wecom),
    ]
    
    for name, fn in platforms:
        ok, msg = fn(cfg, report)
        icon = "✅" if ok else "⏸"
        results.append(f"{icon} {name}: {msg}")
        print(f"{icon} {name}: {msg}")
    
    # 取价格信息展示
    import re
    prices = re.findall(r'\$(\d[\d,.]*)', report[:300])
    p_str = " | ".join(prices[:4]) if prices else "?"
    print(f"\n📊 {p_str}")
    print("\n".join(results))

if __name__ == "__main__":
    main()
