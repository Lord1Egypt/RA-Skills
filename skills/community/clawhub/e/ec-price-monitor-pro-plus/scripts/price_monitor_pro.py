#!/usr/bin/env python3
"""
EC Price Monitor Pro - 付费专业版
支持：淘宝/拼多多/京东/亚马逊 比价、定时监控、价差推送、价格历史
"""
import json, os, sys, re, time, sqlite3, urllib.request, urllib.parse
from datetime import datetime, timedelta

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE, "references", "config.yaml")
DB_PATH = os.path.join(BASE, "data", "price_history.db")
DATA_DIR = os.path.join(BASE, "data")

os.makedirs(DATA_DIR, exist_ok=True)

# ── 数据库 ──
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT, platform TEXT, price REAL,
        recorded_at TEXT DEFAULT (datetime('now','localtime'))
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT, message TEXT, created_at TEXT DEFAULT (datetime('now','localtime'))
    )""")
    conn.commit()
    return conn

def save_price(conn, keyword, platform, price):
    c = conn.cursor()
    c.execute("INSERT INTO prices (keyword, platform, price) VALUES (?, ?, ?)",
              (keyword, platform, price))

def get_history(conn, keyword, days=30):
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    c = conn.cursor()
    c.execute("""SELECT platform, price, recorded_at FROM prices
                 WHERE keyword=? AND recorded_at>=? ORDER BY recorded_at""",
              (keyword, cutoff))
    return c.fetchall()

# ── 配置 ──
def load_config():
    import yaml
    try:
        with open(CONFIG_PATH) as f: return yaml.safe_load(f) or {}
    except: return {"items": [], "notify": {}, "price_diff_threshold": 50, "check_interval": 1}

# ── 多平台搜索 ──
PLATFORMS = {
    "taobao": {"name": "淘宝", "url": lambda k: f"https://s.taobao.com/search?q={urllib.parse.quote(k)}"},
    "pdd": {"name": "拼多多", "url": lambda k: f"https://mobile.yangkeduo.com/search_result.html?search_key={urllib.parse.quote(k)}"},
    "jd": {"name": "京东", "url": lambda k: f"https://search.jd.com/Search?keyword={urllib.parse.quote(k)}&enc=utf-8"},
    "amazon": {"name": "亚马逊", "url": lambda k: f"https://www.amazon.com/s?k={urllib.parse.quote(k)}"},
}

PRICE_PATTERNS = [
    r'"price"[:\s]*"?(\d+[\.\d]*)',
    r'"view_price"[:\s]*"?(\d+[\.\d]*)',
    r'price["\']?\s*[:=]\s*["\']?(\d+[\.\d]*)',
    r'¥(\d+[\.\d]*)',
    r'\$(\d+[\.\d]*)',
    r'"asin_price"[:\s]*"?(\d+[\.\d]*)',
]

def search(keyword, platform_key):
    info = PLATFORMS.get(platform_key)
    if not info: return None
    try:
        req = urllib.request.Request(info["url"](keyword),
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
        prices = []
        for pat in PRICE_PATTERNS:
            for m in re.findall(pat, html):
                try:
                    v = float(m)
                    if 1 < v < 999999: prices.append(v)
                except: pass
            if prices: break
        return min(prices) if prices else None
    except:
        return None

# ── 报告生成 ──
def generate_report(keyword, platform_prices, conn):
    lines = []
    lines.append(f"💎 EC Price Monitor Pro")
    lines.append("━" * 35)
    lines.append(f"📍 {keyword}")
    lines.append(f"   {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    prices = []
    for pk, pv in platform_prices.items():
        pname = PLATFORMS.get(pk, {}).get("name", pk)
        if pv:
            lines.append(f"  {pname}: ¥{pv:,.0f}")
            prices.append((pk, pv))
        else:
            lines.append(f"  {pname}: 获取失败")

    # 价差检测
    if len(prices) >= 2:
        min_p = min(prices, key=lambda x: x[1])
        lines.append(f"\n⚡ 最低价: {PLATFORMS.get(min_p[0],{}).get('name',min_p[0])} ¥{min_p[1]:,.0f}")
        threshold = load_config().get("price_diff_threshold", 50)
        for i in range(len(prices)):
            for j in range(i+1, len(prices)):
                diff = abs(prices[i][1] - prices[j][1])
                if diff >= threshold:
                    lines.append(f"   价差 {PLATFORMS.get(prices[i][0],{}).get('name')}↔{PLATFORMS.get(prices[j][0],{}).get('name')}: ¥{diff:,.0f}")

    # 历史趋势
    if conn:
        hist = get_history(conn, keyword, days=30)
        if hist:
            lines.append(f"\n📈 30天趋势")
            seen = set()
            for p, pl, ts in hist:
                if p not in seen:
                    seen.add(p)
                    pname = PLATFORMS.get(p, {}).get("name", p)
                    # show first and last
                    same = [(hpl, hts) for hp, hpl, hts in hist if hp == p]
                    if len(same) >= 2:
                        first_pl, last_pl = same[0][0], same[-1][0]
                        change = ((last_pl - first_pl) / first_pl) * 100 if first_pl else 0
                        arrow = "↑" if change > 0 else "↓" if change < 0 else "→"
                        lines.append(f"  {pname}: ¥{first_pl:,.0f} → ¥{last_pl:,.0f} ({arrow}{abs(change):.1f}%)")

    return "\n".join(lines)

# ── 推送 ──
def push_notify(message, config):
    notify = config.get("notify", {})
    webhook = notify.get("feishu_webhook", "")
    if webhook:
        try:
            data = json.dumps({"msg_type": "text", "content": {"text": message[:3000]}}).encode()
            urllib.request.urlopen(urllib.request.Request(webhook, data=data,
                headers={"Content-Type": "application/json"}), timeout=5)
        except: pass
    tg_token = notify.get("telegram_token", "")
    tg_chat = notify.get("telegram_chat_id", "")
    if tg_token and tg_chat:
        try:
            text = urllib.parse.quote(message[:4000])
            urllib.request.urlopen(
                f"https://api.telegram.org/bot{tg_token}/sendMessage?chat_id={tg_chat}&text={text}", timeout=5)
        except: pass

# ── 主动执行 ──
def run_monitor():
    conn = init_db()
    config = load_config()
    items = config.get("items", [])
    if not items:
        print("❌ 请在 config.yaml 中添加监控商品")
        return

    all_reports = []
    for item in items:
        kw = item["keyword"]
        platforms = item.get("platforms", ["taobao", "pdd", "jd"])
        results = {}
        for p in platforms:
            time.sleep(0.3)
            results[p] = search(kw, p)
            if results[p]:
                save_price(conn, kw, p, results[p])
        conn.commit()
        report = generate_report(kw, results, conn)
        print(report)
        print()
        all_reports.append(report)

        # 降价检测
        max_price = item.get("max_price", 0)
        for pk, pv in results.items():
            if pv and max_price and pv < max_price:
                alert = f"🎉 降价提醒！{kw} 在 {PLATFORMS.get(pk,{}).get('name',pk)} 仅 ¥{pv:,.0f}（目标价 ¥{max_price:,.0f}）"
                print(alert)
                push_notify(alert, config)

    # 推送汇总
    if all_reports and config.get("notify", {}).get("feishu_webhook"):
        push_notify("\n\n".join(all_reports), config)

# ── 入口 ──
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        run_monitor()
    elif len(sys.argv) >= 3 and sys.argv[1] == "search":
        keyword = " ".join(sys.argv[2:])
        conn = init_db()
        results = {}
        for p in PLATFORMS:
            time.sleep(0.3)
            results[p] = search(keyword, p)
            if results[p]:
                save_price(conn, keyword, p, results[p])
        conn.commit()
        print(generate_report(keyword, results, conn))
    elif len(sys.argv) >= 3 and sys.argv[1] == "history":
        keyword = " ".join(sys.argv[2:])
        conn = init_db()
        hist = get_history(conn, keyword)
        if not hist:
            print(f"📭 {keyword}: 暂无历史数据")
            return
        print(f"📈 {keyword} 价格历史")
        for p, pl, ts in hist[-20:]:
            pname = PLATFORMS.get(p, {}).get("name", p)
            print(f"  {ts} {pname}: ¥{pl:,.0f}")
    else:
        run_monitor()
    return 0

if __name__ == "__main__":
    sys.exit(main())
