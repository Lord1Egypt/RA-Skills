#!/usr/bin/env python3
"""
竞品ASIN定时监控脚本 — 抓取 + SQLite存储 + HTML面板生成 + Discord推送

用法:
  python3 asin_monitor.py

配置:
  1. 修改下方 ASINS 列表为目标竞品ASIN
  2. 确保 amazon-scraper Docker 镜像已 build (bash scripts/setup.sh)
  3. 确保 config/proxies.json 配置了 ISP/Residential 代理（非 DDC）

输出:
  - SQLite DB: ~/.openclaw/amazon-scraper/asin_monitor.db (全部历史记录)
  - HTML面板: ~/.openclaw/amazon-scraper/monitor-output/monitor_panel.html
  - JSON数据: ~/.openclaw/amazon-scraper/monitor-output/monitor_data.json
  - stdout: Markdown 格式摘要（automation 可推送到 Discord/Telegram）

异动检测字段:
  价格(涨跌+百分比) / 评分(变化≥0.1) / 评论数(增减) /
  月销量(区间变化) / 标题(文本修改) / 五点描述(数量+内容变化)

定时任务（北京时间每天 9:00，只跑脚本，不另起一轮模型）:
  openclaw automations create "0 9 * * *" \\
    --name "竞品ASIN监控" --tz Asia/Shanghai \\
    --command "python3 ~/.openclaw/skills/amazon-scraper/scripts/asin_monitor.py" \\
    --session isolated --announce
"""
import json, sys, os, sqlite3
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scraper_client import scrape_detail as _scrape_detail, ScrapeError

# ═══════════════════════════════════════════
# 配置区
# ═══════════════════════════════════════════
ASINS = [
    "B0D1XD1ZV3",  # Apple AirPods Pro 2
    "B0CHWRXH8B",  # Apple AirPods Pro 2nd Gen
    "B09XS7NSWH",  # Sony WF-1000XM4
]

DB_PATH = os.path.expanduser("~/.openclaw/amazon-scraper/asin_monitor.db")
OUTPUT_DIR = os.path.expanduser("~/.openclaw/amazon-scraper/monitor-output")

# ═══════════════════════════════════════════
# 核心逻辑
# ═══════════════════════════════════════════

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asin TEXT NOT NULL,
            checked_at TEXT NOT NULL,
            title TEXT,
            price REAL,
            price_str TEXT,
            rating REAL,
            reviews INTEGER,
            bullets_count INTEGER,
            bullets_json TEXT,
            bought_past_month TEXT,
            raw_json TEXT
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_asin_date ON price_history(asin, checked_at)")
    conn.commit()
    return conn


def scrape_asin(asin: str) -> dict:
    """用 amazon-scraper Docker 镜像抓取单个 ASIN 详情页"""
    try:
        p = _scrape_detail(asin)
    except ScrapeError as e:
        return {"asin": asin, "error": str(e)}
    return {
            "asin": asin,
            "title": p.get("title") or "",
            "price": p.get("price"),
            "priceStr": p.get("priceStr"),
            "rating": p.get("rating"),
            "reviews": p.get("reviews"),
            "bullets": p.get("bullets") or [],
            "bullets_count": len(p.get("bullets", [])),
            "boughtPastMonth": p.get("boughtPastMonth"),
            "raw_json": json.dumps(p, ensure_ascii=False),
    }


def save_to_db(conn, record: dict):
    conn.execute("""
        INSERT INTO price_history
            (asin, checked_at, title, price, price_str, rating, reviews,
             bullets_count, bullets_json, bought_past_month, raw_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record["asin"],
        datetime.now(timezone.utc).isoformat(timespec="seconds"),
        record.get("title"),
        record.get("price"),
        record.get("priceStr"),
        record.get("rating"),
        record.get("reviews"),
        record.get("bullets_count"),
        json.dumps(record.get("bullets", []), ensure_ascii=False),
        record.get("boughtPastMonth"),
        record.get("raw_json"),
    ))
    conn.commit()


def get_previous_record(conn, asin: str, current_id: int) -> dict:
    row = conn.execute("""
        SELECT title, price, price_str, rating, reviews, bullets_count, bullets_json,
               bought_past_month, checked_at
        FROM price_history
        WHERE asin = ? AND id < ?
        ORDER BY id DESC LIMIT 1
    """, (asin, current_id)).fetchone()
    if not row:
        return {}
    return {
        "title": row[0], "price": row[1], "priceStr": row[2], "rating": row[3],
        "reviews": row[4], "bullets_count": row[5], "bullets": json.loads(row[6] or "[]"),
        "boughtPastMonth": row[7], "checked_at": row[8],
    }


def detect_changes(current: dict, previous: dict) -> list:
    """检测异动，返回异动列表"""
    changes = []
    if not previous:
        return changes

    # 价格变化
    cur_price = current.get("price")
    prev_price = previous.get("price")
    if cur_price and prev_price and cur_price != prev_price:
        diff = cur_price - prev_price
        pct = (diff / prev_price * 100) if prev_price else 0
        arrow = "📈" if diff > 0 else "📉"
        changes.append({
            "field": "价格", "old": f"${prev_price:.2f}", "new": f"${cur_price:.2f}",
            "diff": f"{arrow} {'+' if diff > 0 else ''}{diff:.2f} ({pct:+.1f}%)",
            "type": "danger" if diff > 0 else "good",
        })

    # 评分变化
    cur_r = current.get("rating")
    prev_r = previous.get("rating")
    if cur_r and prev_r and abs(cur_r - prev_r) >= 0.1:
        changes.append({
            "field": "评分", "old": f"{prev_r}", "new": f"{cur_r}",
            "diff": f"{'⬆️' if cur_r > prev_r else '⬇️'} {cur_r - prev_r:+.1f}",
            "type": "good" if cur_r > prev_r else "warn",
        })

    # 评论数变化
    cur_rev = current.get("reviews") or 0
    prev_rev = previous.get("reviews") or 0
    if prev_rev and cur_rev != prev_rev:
        diff = cur_rev - prev_rev
        changes.append({
            "field": "评论数", "old": f"{prev_rev:,}", "new": f"{cur_rev:,}",
            "diff": f"{'➕' if diff > 0 else '➖'} {diff:+,}",
            "type": "info",
        })

    # 月销量变化
    cur_b = current.get("boughtPastMonth")
    prev_b = previous.get("boughtPastMonth")
    if cur_b and prev_b and cur_b != prev_b:
        changes.append({
            "field": "月销量", "old": prev_b, "new": cur_b,
            "diff": f"📦 {prev_b} → {cur_b}", "type": "info",
        })

    # 标题变化
    cur_title = current.get("title", "")
    prev_title = previous.get("title", "")
    if cur_title and prev_title and cur_title != prev_title:
        changes.append({
            "field": "标题", "old": prev_title[:80], "new": cur_title[:80],
            "diff": "📝 标题已修改", "type": "warn",
        })

    # 五点描述变化
    cur_bc = current.get("bullets_count", 0)
    prev_bc = previous.get("bullets_count", 0)
    cur_bullets = current.get("bullets", [])
    prev_bullets = previous.get("bullets", [])
    if cur_bc != prev_bc:
        changes.append({
            "field": "五点数量", "old": f"{prev_bc}条", "new": f"{cur_bc}条",
            "diff": f"📝 {prev_bc} → {cur_bc}", "type": "warn",
        })
    elif cur_bullets and prev_bullets:
        changed_items = sum(1 for a, b in zip(cur_bullets, prev_bullets) if a != b)
        if changed_items > 0:
            changes.append({
                "field": "五点内容", "old": f"{prev_bc}条", "new": f"{cur_bc}条",
                "diff": f"📝 {changed_items}条内容已修改", "type": "warn",
            })

    return changes


def build_json_data(conn) -> dict:
    """从DB读取全部历史，构建HTML面板所需的JSON"""
    products = []
    for asin in ASINS:
        rows = conn.execute("""
            SELECT id, asin, checked_at, title, price, price_str, rating, reviews,
                   bullets_count, bullets_json, bought_past_month
            FROM price_history WHERE asin = ? ORDER BY id DESC
        """, (asin,)).fetchall()

        if not rows:
            products.append({"asin": asin, "error": "暂无数据", "history": [], "changes": []})
            continue

        latest = rows[0]
        prev = get_previous_record(conn, asin, latest[0])

        current = {
            "title": latest[3], "price": latest[4], "priceStr": latest[5],
            "rating": latest[6], "reviews": latest[7], "bullets_count": latest[8],
            "bullets": json.loads(latest[9] or "[]"), "boughtPastMonth": latest[10],
        }
        changes = detect_changes(current, prev)

        history = []
        for r in rows:
            history.append({
                "checked_at": r[2], "price": r[4], "priceStr": r[5],
                "rating": r[6], "reviews": r[7], "boughtPastMonth": r[10],
            })

        products.append({
            "asin": asin,
            "title": latest[3] or "",
            "price": latest[4], "priceStr": latest[5],
            "rating": latest[6], "reviews": latest[7],
            "bullets_count": latest[8],
            "bullets": json.loads(latest[9] or "[]"),
            "boughtPastMonth": latest[10],
            "latest_check": latest[2],
            "changes": changes,
            "history": history,
        })

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total_asins": len(ASINS),
        "products": products,
    }


# ═══════════════════════════════════════════
# HTML面板生成
# ═══════════════════════════════════════════

def embed_json(data: dict) -> str:
    """Serialize for embedding inside a <script> block.

    Listing titles, bullets and seller names are attacker-controlled: a competitor
    can put `</script>` or a JS string breaker in their own listing, which we then
    scrape and write into the panel. Escaping these characters keeps the payload
    inside the string literal.
    """
    # These characters only ever occur inside JSON string literals, so rewriting them
    # as \uXXXX escapes preserves the value while neutering the tag breakout.
    raw = json.dumps(data, ensure_ascii=False)
    return (raw.replace("<", "\\u003c")
               .replace(">", "\\u003e")
               .replace("&", "\\u0026")
               .replace("\u2028", "\\u2028")
               .replace("\u2029", "\\u2029"))


def generate_html(data: dict, output_path: str):
    """生成自包含HTML监控面板（JSON内嵌）。

    模板是普通字符串 + __MONITOR_DATA__ 占位符，不是 f-string：原来的 f-string 把
    JS 模板字面量 `${p.title}` 当成 Python 替换字段，整个文件 SyntaxError 无法导入。
    渲染全部走 textContent / createElement，不拼 innerHTML —— listing 标题、五点、
    卖家名是卖家可控内容，拼 innerHTML 等于让竞品往你的面板里注入 JS。
    """
    html_content = HTML_TEMPLATE.replace("__MONITOR_DATA__", embed_json(data))
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)


HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>竞品Listing与价格异动监控</title>
<style>
:root{--bg:#0d1117;--card:#161b22;--border:#30363d;--text:#e6edf3;--muted:#8b949e;--accent:#f78166;--green:#7ee787;--red:#ff7b72;--yellow:#e3b341;--blue:#79c0ff;--code-bg:#1c2128}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--text);line-height:1.6;padding:20px}
.header{text-align:center;padding:30px 20px;border-bottom:2px solid var(--border);margin-bottom:30px}
.header h1{font-size:2em;background:linear-gradient(135deg,var(--accent),var(--blue));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.header .meta{color:var(--muted);margin-top:8px;font-size:0.9em}
.summary{display:flex;gap:16px;justify-content:center;flex-wrap:wrap;margin:20px 0}
.summary-card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:16px 28px;text-align:center;min-width:120px}
.summary-card .num{font-size:1.8em;font-weight:800}
.summary-card .label{color:var(--muted);font-size:0.85em;margin-top:4px}
.product{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:24px;margin-bottom:20px}
.product.has-changes{border-left:4px solid var(--yellow)}
.product-header{display:flex;align-items:center;gap:12px;margin-bottom:16px;flex-wrap:wrap}
.asin-tag{background:var(--code-bg);border:1px solid var(--border);border-radius:6px;padding:3px 10px;font-family:monospace;font-size:0.9em;color:var(--blue)}
.product-title{font-size:1em;color:var(--text);flex:1;min-width:200px}
.stamp{color:var(--muted);font-size:0.8em}
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:12px;margin-bottom:16px}
.metric{background:var(--code-bg);border-radius:8px;padding:12px;text-align:center}
.metric .val{font-size:1.3em;font-weight:700}
.metric .lbl{color:var(--muted);font-size:0.78em;margin-top:2px}
.metric.price .val{color:var(--green)}.metric.rating .val{color:var(--yellow)}.metric.reviews .val{color:var(--blue)}
.changes-section{margin-top:16px}
.changes-title{color:var(--yellow);font-size:0.95em;margin-bottom:10px;font-weight:600}
.change-item{background:var(--code-bg);border-radius:8px;padding:10px 14px;margin-bottom:8px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.change-field{font-weight:600;min-width:80px;color:var(--accent)}
.change-diff{color:var(--text)}.change-old{color:var(--muted);text-decoration:line-through;font-size:0.88em}.change-arrow{color:var(--muted)}.change-new{color:var(--green)}
.change-item.danger{border-left:3px solid var(--red)}.change-item.good{border-left:3px solid var(--green)}.change-item.warn{border-left:3px solid var(--yellow)}.change-item.info{border-left:3px solid var(--blue)}
.bullets{margin-top:12px;padding:12px;background:var(--code-bg);border-radius:8px}
.bullets h4{color:var(--muted);font-size:0.85em;margin-bottom:8px}
.bullets ul{margin-left:20px}.bullets li{font-size:0.88em;margin-bottom:4px;color:var(--text)}
.history-chart{margin-top:16px;padding:16px;background:var(--code-bg);border-radius:8px;overflow-x:auto}
.history-chart h4{color:var(--muted);font-size:0.85em;margin-bottom:10px}
.chart-bar{display:flex;align-items:end;gap:4px;height:80px;min-width:300px}
.bar{flex:1;background:linear-gradient(180deg,var(--accent),var(--red));border-radius:3px 3px 0 0;min-height:4px;position:relative;opacity:0.8}
.bar:hover{opacity:1}
.bar-label{position:absolute;bottom:-20px;left:50%;transform:translateX(-50%);font-size:0.65em;color:var(--muted);white-space:nowrap}
.bar-value{position:absolute;top:-18px;left:50%;transform:translateX(-50%);font-size:0.65em;color:var(--green);white-space:nowrap}
.err{color:var(--red)}
.footer{text-align:center;color:var(--muted);font-size:0.82em;margin-top:30px;padding:20px;border-top:1px solid var(--border)}
</style>
</head>
<body>
<div class="header"><h1>竞品Listing与价格异动监控</h1><div class="meta">数据更新时间: <span id="gen-time"></span></div></div>
<div class="summary" id="summary"></div>
<div id="products"></div>
<div class="footer">Amazon Scraper + SQLite</div>
<script>
const DATA = __MONITOR_DATA__;

// Scraped Amazon text is untrusted. Everything below sets textContent and never
// assigns a scraped value into innerHTML or an attribute that can execute script.
const el = (tag, cls, text) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text !== undefined && text !== null) n.textContent = String(text);
  return n;
};
const num = v => (typeof v === 'number' && isFinite(v)) ? v.toLocaleString() : 'N/A';
const str = v => (v === null || v === undefined || v === '') ? 'N/A' : String(v);

document.getElementById('gen-time').textContent =
  new Date(DATA.generated_at).toLocaleString('zh-CN');

const products = Array.isArray(DATA.products) ? DATA.products : [];
const totalChanges = products.reduce((s, p) => s + ((p.changes || []).length), 0);
const validProducts = products.filter(p => !p.error).length;

const summary = document.getElementById('summary');
[['监控ASIN', DATA.total_asins, 'var(--blue)'],
 ['抓取成功', validProducts, 'var(--green)'],
 ['异动总数', totalChanges, 'var(--yellow)']].forEach(([label, value, color]) => {
  const card = el('div', 'summary-card');
  const n = el('div', 'num', value);
  n.style.color = color;
  card.append(n, el('div', 'label', label));
  summary.append(card);
});

const metric = (cls, value, label) => {
  const m = el('div', 'metric ' + cls);
  m.append(el('div', 'val', value), el('div', 'lbl', label));
  return m;
};

const container = document.getElementById('products');
products.forEach(p => {
  const hasChanges = (p.changes || []).length > 0;
  const card = el('div', 'product' + (hasChanges ? ' has-changes' : ''));

  const header = el('div', 'product-header');
  header.append(el('span', 'asin-tag', p.asin));
  if (p.error) {
    header.append(el('span', 'product-title err', p.error));
    card.append(header);
    container.append(card);
    return;
  }
  header.append(el('span', 'product-title', (p.title || '').slice(0, 100)));
  header.append(el('span', 'stamp', '最后更新: ' + str(p.latest_check)));
  card.append(header);

  const metrics = el('div', 'metrics');
  metrics.append(
    metric('price', str(p.priceStr), '价格'),
    metric('rating', str(p.rating), '评分'),
    metric('reviews', num(p.reviews), '评论数'),
    metric('', str(p.boughtPastMonth), '月销量'),
    metric('', p.bullets_count || 0, '五点数量')
  );
  card.append(metrics);

  if (hasChanges) {
    const sec = el('div', 'changes-section');
    sec.append(el('div', 'changes-title', '检测到异动'));
    p.changes.forEach(c => {
      const kind = ['danger', 'good', 'warn', 'info'].includes(c.type) ? c.type : 'info';
      const item = el('div', 'change-item ' + kind);
      item.append(el('span', 'change-field', c.field));
      if (c.old && c.old !== 'None') {
        item.append(el('span', 'change-old', c.old),
                    el('span', 'change-arrow', '→'),
                    el('span', 'change-new', c.new));
      }
      item.append(el('span', 'change-diff', c.diff));
      sec.append(item);
    });
    card.append(sec);
  }

  if ((p.bullets || []).length > 0) {
    const box = el('div', 'bullets');
    box.append(el('h4', '', '五点描述'));
    const ul = el('ul');
    p.bullets.forEach(b => ul.append(el('li', '', String(b).slice(0, 150))));
    box.append(ul);
    card.append(box);
  }

  const prices = (p.history || []).map(h => h.price).filter(v => typeof v === 'number');
  if (prices.length > 0) {
    const minP = Math.min(...prices), maxP = Math.max(...prices);
    const range = (maxP - minP) || 1;
    const chart = el('div', 'history-chart');
    chart.append(el('h4', '', '价格趋势'));
    const row = el('div', 'chart-bar');
    p.history.slice(-15).reverse().forEach(h => {
      if (typeof h.price !== 'number') return;
      const bar = el('div', 'bar');
      bar.style.height = ((h.price - minP) / range * 70 + 10) + 'px';
      bar.append(el('span', 'bar-value', h.priceStr || ''),
                 el('span', 'bar-label', String(h.checked_at || '').slice(5, 10)));
      row.append(bar);
    });
    chart.append(row);
    card.append(chart);
  }

  container.append(card);
});
</script>
</body>
</html>
'''

# ═══════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    conn = init_db()

    # 1. 抓取所有ASIN
    results = []
    for asin in ASINS:
        r = scrape_asin(asin)
        results.append(r)
        status = "✅" if "error" not in r else "❌"
        print(f"{status} {asin}", file=sys.stderr)

    # 2. 存入DB
    for r in results:
        if "error" not in r:
            save_to_db(conn, r)

    # 3. 生成JSON + HTML面板
    data = build_json_data(conn)
    json_path = os.path.join(OUTPUT_DIR, "monitor_data.json")
    with open(json_path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    html_path = os.path.join(OUTPUT_DIR, "monitor_panel.html")
    generate_html(data, html_path)

    conn.close()

    # 4. 输出摘要到stdout（推送到Discord）
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [f"📊 **竞品Listing与价格异动监控** ({today})", ""]
    total_changes = 0
    for p in data["products"]:
        if p.get("error"):
            lines.append(f"❌ `{p['asin']}` — {p['error']}")
            continue
        changes = p.get("changes", [])
        total_changes += len(changes)
        price = p.get("priceStr") or "N/A"
        title = (p.get("title") or "")[:60]
        change_summary = ""
        if changes:
            change_summary = " | ".join(c["diff"] for c in changes)
            change_summary = f" ⚡ **{change_summary}**"
        reviews_val = p.get('reviews') or 0
        lines.append(f"**`{p['asin']}`** {title}")
        lines.append(f"  💰 {price} | ⭐ {p.get('rating') or 'N/A'} | 💬 {reviews_val:,}{change_summary}")
        lines.append("")

    lines.append(f"📁 完整监控面板: `{html_path}`")
    lines.append(f"📈 异动总数: {total_changes} | 数据库: `{DB_PATH}`")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
