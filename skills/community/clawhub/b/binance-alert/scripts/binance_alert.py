#!/usr/bin/env python3
"""
BinanceAlert — openclaw 技能脚本
复用 /data/freqtrade/user_data/.secrets.env 中的 TG_BOT_TOKEN / TG_CHAT_ID
状态持久化到 /data/freqtrade/user_data/binance_alert_state.json

用法:
  python3 binance_alert.py price BTCUSDT 100000 above     # 价格预警
  python3 binance_alert.py change ETHUSDT 5               # 涨跌幅预警（%）
  python3 binance_alert.py listing                        # 检查新币上线
  python3 binance_alert.py alpha                          # Alpha空投机会
  python3 binance_alert.py announcement                   # 币安公告/HODLer空投
  python3 binance_alert.py run                            # 一次性跑全部检查（供定时任务用）
  python3 binance_alert.py status                         # 查看当前预警状态
"""

import sys, os, json, time, hashlib, urllib.request, urllib.error, gzip, re
from pathlib import Path
from datetime import datetime

# ── 配置 ──────────────────────────────────────────────────────────────────────
ENV_FILE   = Path("/data/freqtrade/user_data/.secrets.env")
STATE_FILE = Path("/data/freqtrade/user_data/binance_alert_state.json")
BINANCE_API  = "https://api.binance.com"
BINANCE_WEB3 = "https://web3.binance.com"
BINANCE_CMS  = "https://www.binance.com"

# 冷却时间（秒）
ALPHA_COOLDOWN_SEC        = 3600   # alpha 相同内容 1 小时内不重复推
ALPHA_FORCE_INTERVAL_SEC  = 14400  # 即使内容变了，4 小时内最多推一次
CHANGE_RESET_HOURS        = 24     # 涨跌幅预警触发后 24h 重置，可再次触发


def load_env():
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        if k.strip() not in os.environ:
            os.environ[k.strip()] = v.strip().strip('"').strip("'")

load_env()
TG_TOKEN = os.getenv("TG_BOT_TOKEN", "")
TG_CHAT  = os.getenv("TG_CHAT_ID", "")


# ── 工具 ──────────────────────────────────────────────────────────────────────
def http_get(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {
        "User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip"
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        raw = r.read()
        if r.info().get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
        return json.loads(raw)

def http_post(url, data):
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": "application/json", "Accept-Encoding": "identity"
    })
    with urllib.request.urlopen(req, timeout=15) as r:
        raw = r.read()
        if r.info().get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
        return json.loads(raw)

def tg_send(text):
    if not TG_TOKEN or not TG_CHAT:
        print(f"[TG未配置] {text[:80]}")
        return
    try:
        http_post(
            f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
            {"chat_id": TG_CHAT, "text": text, "parse_mode": "Markdown"}
        )
    except Exception as e:
        print(f"TG发送失败: {e}")

def fingerprint(obj):
    return hashlib.md5(json.dumps(obj, sort_keys=True).encode()).hexdigest()[:12]

def now_ts():
    return int(time.time())

def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {
        "price_alerts": [],
        "change_alerts": [],
        "known_symbols": [],
        "seen_announcements": [],
        "alpha_last_fp": "",
        "alpha_last_sent_ts": 0,
        "last_check": {}
    }

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))

def out(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


# ── 1. 价格预警 ───────────────────────────────────────────────────────────────
def add_price_alert(symbol, target_price, condition="above", note=""):
    state = load_state()
    alert = {
        "id": f"price_{symbol.upper()}_{now_ts()}",
        "symbol": symbol.upper(),
        "target_price": float(target_price),
        "condition": condition,
        "note": note,
        "created_at": datetime.now().isoformat(),
        "triggered": False
    }
    state["price_alerts"].append(alert)
    save_state(state)
    out({"action": "price_alert_added", "alert": alert})

def check_price_alerts(state):
    for alert in state.get("price_alerts", []):
        if alert.get("triggered"):
            continue
        try:
            data  = http_get(f"{BINANCE_API}/api/v3/ticker/price?symbol={alert['symbol']}")
            price = float(data["price"])
            hit   = (alert["condition"] == "above" and price >= alert["target_price"]) or \
                    (alert["condition"] == "below" and price <= alert["target_price"])
            if hit:
                tg_send(
                    f"📈 *价格预警触发*\n\n"
                    f"交易对: *{alert['symbol']}*\n"
                    f"当前价格: `{price}`\n"
                    f"目标价格: `{alert['target_price']}` ({alert['condition']})\n"
                    f"备注: {alert.get('note','')}\n"
                    f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
                alert["triggered"] = True
                print(f"[价格预警] {alert['symbol']} 触发: {price}")
        except Exception as e:
            print(f"[价格预警] {alert['symbol']} 失败: {e}")


# ── 2. 涨跌幅预警（触发后 24h 自动重置，可再次触发）────────────────────────
def add_change_alert(symbol, threshold_pct, note=""):
    state = load_state()
    alert = {
        "id": f"change_{symbol.upper()}_{now_ts()}",
        "symbol": symbol.upper(),
        "threshold_pct": float(threshold_pct),
        "note": note,
        "created_at": datetime.now().isoformat(),
        "triggered": False,
        "triggered_at": 0
    }
    state["change_alerts"].append(alert)
    save_state(state)
    out({"action": "change_alert_added", "alert": alert})

def check_change_alerts(state):
    for alert in state.get("change_alerts", []):
        # 24h 后自动重置
        if alert.get("triggered") and alert.get("triggered_at", 0):
            if now_ts() - alert["triggered_at"] > CHANGE_RESET_HOURS * 3600:
                alert["triggered"] = False
                alert["triggered_at"] = 0
                print(f"[涨跌幅预警] {alert['symbol']} 重置，可再次触发")
        if alert.get("triggered"):
            continue
        try:
            data   = http_get(f"{BINANCE_API}/api/v3/ticker/24hr?symbol={alert['symbol']}")
            change = float(data["priceChangePercent"])
            if abs(change) >= alert["threshold_pct"]:
                direction = "📈" if change > 0 else "📉"
                tg_send(
                    f"{direction} *涨跌幅预警触发*\n\n"
                    f"交易对: *{alert['symbol']}*\n"
                    f"24h涨跌: `{change:+.2f}%`\n"
                    f"阈值: `±{alert['threshold_pct']}%`\n"
                    f"当前价: `{data['lastPrice']}`\n"
                    f"备注: {alert.get('note','')}\n"
                    f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
                alert["triggered"]    = True
                alert["triggered_at"] = now_ts()
                print(f"[涨跌幅预警] {alert['symbol']} 触发: {change:+.2f}%")
        except Exception as e:
            print(f"[涨跌幅预警] {alert['symbol']} 失败: {e}")


# ── 3. 新币上线监控 ───────────────────────────────────────────────────────────
def check_new_listings(state):
    try:
        data    = http_get(f"{BINANCE_API}/api/v3/exchangeInfo")
        current = {s["symbol"] for s in data["symbols"] if s["status"] == "TRADING"}
        known   = set(state.get("known_symbols", []))
        if not known:
            state["known_symbols"] = list(current)
            save_state(state)
            print(f"[新币监控] 初始化，记录 {len(current)} 个交易对")
            return
        new_ones = current - known
        if new_ones:
            usdt_new = sorted(s for s in new_ones if s.endswith("USDT"))
            if usdt_new:
                tg_send(
                    f"🚀 *新币上线提醒*\n\n"
                    f"发现 *{len(usdt_new)}* 个新 USDT 交易对:\n"
                    + "\n".join(f"• `{s}`" for s in usdt_new) +
                    f"\n\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    f"⚠️ 新币高波动，注意风险"
                )
                print(f"[新币监控] 新币: {usdt_new}")
            state["known_symbols"] = list(current)
            save_state(state)
        else:
            print(f"[新币监控] 无新币，共 {len(current)} 个")
    except Exception as e:
        print(f"[新币监控] 失败: {e}")


# ── 4. Alpha 空投监控（带去重 + 冷却）────────────────────────────────────────
def check_alpha_airdrop(state, min_score=50, min_kyc=500):
    try:
        data = http_post(
            f"{BINANCE_WEB3}/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/unified/rank/list",
            {"rankType": 20, "period": 50, "sortBy": 80, "orderAsc": False, "page": 1, "size": 50}
        )
        if data.get("code") != "000000":
            print(f"[Alpha] API异常: {data.get('message')}")
            return

        tokens = data.get("data", {}).get("tokens", [])
        opportunities = []

        for t in tokens:
            kyc    = int(t.get("kycHolders") or 0)
            vol    = float(t.get("volume24h") or 0)
            change = float(t.get("percentChange24h") or 0)
            mcap   = float(t.get("marketCap") or 0)
            risk   = (t.get("auditInfo") or {}).get("riskLevel", 99)

            alpha_pts = 0
            for cat in (t.get("tokenTag") or {}).values():
                for tag in cat:
                    name = tag.get("tagName", "")
                    if "Alpha Points" in name or "alpha-points" in tag.get("languageKey", ""):
                        m = re.search(r"(\d+)x", name)
                        alpha_pts = int(m.group(1)) if m else 1

            score, reasons = 0, []
            if kyc / max(int(t.get("holders") or 1), 1) > 0.3:
                score += 20; reasons.append("KYC比例高")
            if vol > 1_000_000:
                score += 15; reasons.append("交易量活跃")
            if -5 < change < 50:
                score += 10; reasons.append("价格走势健康")
            if 1_000_000 < mcap < 100_000_000:
                score += 15; reasons.append("市值适中")
            if risk == 1:
                score += 10; reasons.append("合约低风险")
            if alpha_pts > 0:
                score += 30; reasons.append(f"Alpha积分{alpha_pts}x")

            if score >= min_score and kyc >= min_kyc:
                opportunities.append({
                    "symbol": t.get("symbol"),
                    "score": score,
                    "kyc_holders": kyc,
                    "alpha_pts": alpha_pts,
                    "reasons": reasons
                })

        if not opportunities:
            print(f"[Alpha] 无符合条件机会（扫描 {len(tokens)} 个）")
            return

        opportunities.sort(key=lambda x: -x["score"])

        # ── 去重逻辑 ──────────────────────────────────────────────────────────
        top_symbols = [o["symbol"] for o in opportunities[:5]]
        fp          = fingerprint(top_symbols)
        last_fp     = state.get("alpha_last_fp", "")
        last_sent   = state.get("alpha_last_sent_ts", 0)
        elapsed     = now_ts() - last_sent

        # 相同内容且在冷却期内 → 跳过
        if fp == last_fp and elapsed < ALPHA_COOLDOWN_SEC:
            print(f"[Alpha] 内容未变化，跳过推送（{elapsed//60}分钟前已推）")
            return

        # 内容变了但距上次推送不足强制间隔 → 也跳过（防止频繁刷屏）
        if elapsed < ALPHA_FORCE_INTERVAL_SEC and fp != last_fp:
            print(f"[Alpha] 内容有变化但冷却中（{elapsed//60}分钟前已推，需满{ALPHA_FORCE_INTERVAL_SEC//60}分钟）")
            return

        # ── 推送 ──────────────────────────────────────────────────────────────
        lines = []
        for o in opportunities[:5]:
            lines.append(
                f"• *${o['symbol']}* ⭐{o['score']}分\n"
                f"  KYC持有者: {o['kyc_holders']:,} | Alpha积分: {o['alpha_pts']}x\n"
                f"  亮点: {', '.join(o['reasons'][:2])}"
            )
        tg_send(
            f"🎯 *Alpha空投机会*\n\n"
            f"发现 *{len(opportunities)}* 个高潜力代币:\n\n"
            + "\n\n".join(lines) +
            f"\n\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"⚠️ 仅供参考，不构成投资建议"
        )
        state["alpha_last_fp"]      = fp
        state["alpha_last_sent_ts"] = now_ts()
        save_state(state)
        print(f"[Alpha] 推送 {len(opportunities)} 个机会，fp={fp}")

    except Exception as e:
        print(f"[Alpha] 失败: {e}")


# ── 5. 币安公告/HODLer空投监控 ───────────────────────────────────────────────
def check_announcements(state):
    seen     = set(state.get("seen_announcements", []))
    new_seen = []
    found    = []

    for catalog_id in [48, 161]:
        try:
            data = http_get(
                f"{BINANCE_CMS}/bapi/composite/v1/public/cms/article/catalog/list/query"
                f"?catalogId={catalog_id}&pageNo=1&pageSize=10",
                headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
            )
            for a in (data.get("data") or {}).get("articles") or []:
                aid   = str(a.get("id", ""))
                title = a.get("title", "")
                new_seen.append(aid)
                if aid in seen:
                    continue
                if any(kw.lower() in title.lower() for kw in ["Alpha","HODLer","空投","Airdrop","Will List","上线"]):
                    found.append({"id": aid, "title": title})
        except Exception as e:
            print(f"[公告] catalog={catalog_id} 失败: {e}")

    if found:
        tg_send(
            f"📢 *币安公告提醒*\n\n"
            f"发现 *{len(found)}* 条新公告:\n\n"
            + "\n".join(f"• {f['title']}" for f in found) +
            f"\n\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"🔗 请前往币安查看详情"
        )
        print(f"[公告] 发现 {len(found)} 条新公告")
    else:
        print(f"[公告] 无新公告")

    state["seen_announcements"] = list((seen | set(new_seen)))
    if len(state["seen_announcements"]) > 500:
        state["seen_announcements"] = state["seen_announcements"][-500:]
    save_state(state)


# ── 状态查看 ──────────────────────────────────────────────────────────────────
def show_status():
    state = load_state()
    last_sent = state.get("alpha_last_sent_ts", 0)
    out({
        "active_price_alerts":  [a for a in state.get("price_alerts", [])  if not a.get("triggered")],
        "active_change_alerts": [a for a in state.get("change_alerts", []) if not a.get("triggered")],
        "known_symbols_count":  len(state.get("known_symbols", [])),
        "seen_announcements_count": len(state.get("seen_announcements", [])),
        "alpha_last_fp":        state.get("alpha_last_fp", ""),
        "alpha_last_sent":      datetime.fromtimestamp(last_sent).isoformat() if last_sent else "never",
        "alpha_cooldown_remaining_min": max(0, (ALPHA_FORCE_INTERVAL_SEC - (now_ts() - last_sent)) // 60),
        "last_check":           state.get("last_check", {})
    })


# ── 全量检查（定时任务入口）──────────────────────────────────────────────────
def run_all():
    state = load_state()
    print(f"[BinanceAlert] 开始全量检查 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    check_price_alerts(state)
    check_change_alerts(state)
    check_new_listings(state)
    check_alpha_airdrop(state)
    check_announcements(state)
    state["last_check"]["run_all"] = datetime.now().isoformat()
    save_state(state)
    print("[BinanceAlert] 全量检查完成")


# ── 入口 ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    action = args[0]
    if action == "price":
        if len(args) < 3: print("用法: price <SYMBOL> <目标价> [above|below]")
        else: add_price_alert(args[1], args[2], args[3] if len(args) > 3 else "above", " ".join(args[4:]))
    elif action == "change":
        if len(args) < 3: print("用法: change <SYMBOL> <涨跌幅%>")
        else: add_change_alert(args[1], args[2], " ".join(args[3:]))
    elif action == "listing":
        state = load_state(); check_new_listings(state)
    elif action == "alpha":
        state = load_state(); check_alpha_airdrop(state)
    elif action == "announcement":
        state = load_state(); check_announcements(state)
    elif action == "run":
        run_all()
    elif action == "status":
        show_status()
    else:
        print(f"未知操作: {action}"); sys.exit(1)
