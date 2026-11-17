#!/usr/bin/env python3
"""
Pickleball ASIN 价格监控 - 每6小时检查
价格变化时推送到Discord + 每次都写入飞书多维表格

用 OpenClaw automation 的 command 定时跑，stdout 可推到 Discord
- 无价格变化时静默（empty stdout = 不推送）
- 有变化时输出到stdout → Discord推送
- 每次检查都写入飞书多维表格（不管有没有变化）

依赖：
- amazon-scraper Docker镜像
- lark-cli (飞书CLI，已认证)
- SQLite (Python内置)

飞书表格字段：ASIN, 商品标题, 当前价格, 上次价格, 价格变化, 变化幅度, 检查时间, 状态
"""
import subprocess, json, os, sqlite3, sys
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scraper_client import scrape_detail as _scrape_detail, ScrapeError

# ─── 配置 ───
ASINS = ["B0F6XSV7XB", "B0FTQWG86Q", "B0G6CTNVQT"]
DB_PATH = os.path.expanduser("~/.openclaw/amazon-scraper/pickleball_price.db")

# 飞书多维表格配置 (替换为你自己的)
BASE_TOKEN = "YOUR_BASE_TOKEN"
TABLE_ID = "YOUR_TABLE_ID"

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asin TEXT NOT NULL,
            checked_at TEXT NOT NULL,
            title TEXT,
            price REAL,
            price_str TEXT
        )
    """)
    conn.commit()
    return conn

def scrape_asin(asin):
    try:
        p = _scrape_detail(asin)
    except ScrapeError as e:
        return {"asin": asin, "error": str(e)}
    return {
        "asin": asin,
        "title": p.get("title") or "",
        "price": p.get("price"),
        "price_str": p.get("priceStr"),
    }

def get_prev_price(conn, asin):
    row = conn.execute(
        "SELECT price, price_str, title FROM price_history WHERE asin=? ORDER BY id DESC LIMIT 1",
        (asin,)
    ).fetchone()
    if not row:
        return None
    return {"price": row[0], "price_str": row[1], "title": row[2]}

def write_to_feishu(records):
    """批量写入飞书多维表格 — 使用 fields+rows 格式"""
    if not records:
        return
    field_names = ["ASIN", "商品标题", "当前价格", "上次价格", "价格变化", "变化幅度", "检查时间", "状态"]
    rows = []
    for r in records:
        rows.append([
            r["asin"],
            r["title"][:200],
            r["price"] or 0,
            r.get("prev_price") or 0,
            r.get("diff") or 0,
            r.get("pct_str") or "",
            r["check_ts"],
            r["status"],
        ])

    batch_json = json.dumps({"fields": field_names, "rows": rows}, ensure_ascii=False)
    cmd = [
        "lark-cli", "base", "+record-batch-create",
        "--base-token", BASE_TOKEN,
        "--table-id", TABLE_ID,
        "--json", batch_json,
        "--as", "user"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"❌ 飞书写入失败: {result.stderr}", file=sys.stderr)
        else:
            resp = json.loads(result.stdout)
            if resp.get("ok"):
                print(f"✅ 飞书表格已更新 {len(records)} 条记录", file=sys.stderr)
            else:
                print(f"❌ 飞书写入错误: {resp.get('error', {}).get('message', 'unknown')}", file=sys.stderr)
    except Exception as e:
        print(f"❌ 飞书写入异常: {e}", file=sys.stderr)

def main():
    conn = init_db()
    now_beijing = datetime.now(timezone(timedelta(hours=8)))
    now_str = now_beijing.strftime("%Y-%m-%d %H:%M")
    now_iso = now_beijing.isoformat(timespec="seconds")
    check_ts = int(now_beijing.timestamp() * 1000)  # 飞书datetime需毫秒时间戳

    alerts = []
    feishu_records = []

    for asin in ASINS:
        r = scrape_asin(asin)
        if "error" in r:
            print(f"❌ {asin} 抓取失败: {r['error']}", file=sys.stderr)
            feishu_records.append({
                "asin": asin, "title": "", "price": None, "prev_price": None,
                "diff": None, "pct_str": "", "check_ts": check_ts,
                "status": f"抓取失败: {r['error']}",
            })
            continue

        prev = get_prev_price(conn, asin)
        conn.execute(
            "INSERT INTO price_history (asin, checked_at, title, price, price_str) VALUES (?,?,?,?,?)",
            (asin, now_iso, r["title"], r["price"], r["price_str"])
        )
        conn.commit()

        cur_price = r["price"]
        title = (r["title"] or "")[:80]
        price_str = r["price_str"] or "N/A"
        status = "无变化"
        diff_val = 0
        pct_str = ""

        if prev and prev["price"] and cur_price:
            if cur_price < prev["price"]:
                diff = prev["price"] - cur_price
                pct = (diff / prev["price"] * 100)
                pct_str = f"↓ -{pct:.1f}%"
                diff_val = -diff
                status = "降价"
                alerts.append(
                    f"📉 **{asin}**\n"
                    f"   {title}\n"
                    f"   ⬇️ {prev['price_str']} → **{price_str}** (降${diff:.2f} / -{pct:.1f}%)"
                )
            elif cur_price > prev["price"]:
                diff = cur_price - prev["price"]
                pct = (diff / prev["price"] * 100)
                pct_str = f"↑ +{pct:.1f}%"
                diff_val = diff
                status = "涨价"
                alerts.append(
                    f"📈 **{asin}**\n"
                    f"   {title}\n"
                    f"   ⬆️ {prev['price_str']} → **{price_str}** (涨${diff:.2f} / +{pct:.1f}%)"
                )
        elif not prev:
            status = "首次记录"
            pct_str = "新监控"
            alerts.append(
                f"🆕 **{asin}**\n"
                f"   {title}\n"
                f"   💰 首次记录: **{price_str}**"
            )

        feishu_records.append({
            "asin": asin, "title": title, "price": cur_price,
            "prev_price": prev["price"] if prev else None,
            "diff": diff_val, "pct_str": pct_str,
            "check_ts": check_ts, "status": status,
        })

    conn.close()
    write_to_feishu(feishu_records)

    # Discord推送 - 有变化才推送
    if alerts:
        lines = [f"🏓 **Pickleball 价格监控** ({now_str})", ""]
        lines.extend(alerts)
        lines.append("")
        lines.append(f"监控ASIN: {', '.join(ASINS)}")
        lines.append(f"📊 飞书表格: https://your-base-url")
        print("\n".join(lines))
    else:
        return  # 静默

if __name__ == "__main__":
    main()
