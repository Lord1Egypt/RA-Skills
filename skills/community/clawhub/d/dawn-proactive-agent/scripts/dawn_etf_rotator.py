# -*- coding: utf-8 -*-
"""
================================================================================
曙光 ETF 轮动调仓系统 v1.4
================================================================================
数据源:
  - HTSC模拟交易API: getQuote/getPositions/getAccountBalance/submitOrder
  - 妙想搜索 (东方财富新闻API): 自动抓取金融资讯, 提取资金流向关键词
  - 腾讯GT行情: 备用指数数据

每日循环:
import os, sys, json, subprocess, argparse
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import sys as _sys
_sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from dawn_reflect import load_lessons_for_prompt, reflect, load_json, LEARNINGS_DIR

  python dawn_etf_rotator.py --execute    # 执行调仓
  python dawn_etf_rotator.py --dry-run    # 只看新闻不评分
================================================================================
"""
import os
import sys
import json
import subprocess
import argparse
from datetime import datetime
from typing import Dict, List, Tuple, Optional

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTSC_SKILL = os.path.join(os.path.expanduser("~"), ".openclaw", "skills", "a-share-paper-trading", "a_share_paper_trading.py")
MX_SEARCH = os.path.join(os.path.expanduser("~"), ".openclaw", "skills", "mx-search", "mx_search.py")

# 当前持仓 (运行时自动从HTSC获取)
current_holdings = {}
total_assets = 0

# 核心 ETF 池
ETF_POOL = {
    # --- 科技主线 ---
    "515580": {"name": "科技100ETF", "sectors": ["电子", "半导体", "科技"], "themes": ["人工智能", "ChatGPT概念", "算力", "芯片"], "type": "科技", "tier": 1, "exchange": "SH"},
    "588090": {"name": "科创50ETF", "sectors": ["半导体", "电子", "信息技术"], "themes": ["科创", "芯片", "人工智能", "生物医药"], "type": "科技", "tier": 1, "exchange": "SH"},
    "512480": {"name": "半导体ETF", "sectors": ["半导体", "电子"], "themes": ["芯片", "半导体"], "type": "科技", "tier": 2, "exchange": "SH"},
    "515880": {"name": "通信ETF", "sectors": ["通信", "通信设备"], "themes": ["5G", "通信", "算力"], "type": "科技", "tier": 2, "exchange": "SH"},
    "159819": {"name": "人工智能ETF", "sectors": ["软件", "计算机"], "themes": ["人工智能", "ChatGPT概念", "算力"], "type": "科技", "tier": 2, "exchange": "SZ"},
    "512760": {"name": "芯片ETF", "sectors": ["半导体", "电子"], "themes": ["芯片", "半导体"], "type": "科技", "tier": 2, "exchange": "SH"},
    "515000": {"name": "科技ETF", "sectors": ["电子", "计算机", "通信"], "themes": ["科技", "人工智能"], "type": "科技", "tier": 2, "exchange": "SH"},

    # --- 新能源 ---
    "560910": {"name": "电池ETF", "sectors": ["电力设备", "电池"], "themes": ["锂电池", "固态电池", "储能", "新能源车"], "type": "新能源", "tier": 1, "exchange": "SH"},
    "515030": {"name": "新能源车ETF", "sectors": ["汽车", "汽车零部件"], "themes": ["新能源车", "锂电池", "比亚迪概念"], "type": "新能源", "tier": 2, "exchange": "SH"},
    "515790": {"name": "光伏ETF", "sectors": ["光伏", "电力设备"], "themes": ["光伏", "新能源", "储能"], "type": "新能源", "tier": 2, "exchange": "SH"},
    "159611": {"name": "电力ETF", "sectors": ["电力", "公用事业"], "themes": ["电力", "绿电", "新能源"], "type": "电力", "tier": 2, "exchange": "SZ"},

    # --- 周期/资源 ---
    "560490": {"name": "工业有色ETF", "sectors": ["有色金属", "工业金属"], "themes": ["铜", "铝", "小金属", "稀有金属"], "type": "周期", "tier": 1, "exchange": "SH"},
    "516780": {"name": "稀土ETF", "sectors": ["有色金属", "稀土永磁"], "themes": ["稀土永磁", "小金属", "有色金属"], "type": "周期", "tier": 2, "exchange": "SH"},
    "518880": {"name": "黄金ETF", "sectors": ["贵金属", "黄金"], "themes": ["黄金", "贵金属", "避险"], "type": "周期", "tier": 2, "exchange": "SH"},
    "159980": {"name": "有色ETF", "sectors": ["有色金属", "工业金属"], "themes": ["有色金属", "铜", "铝", "小金属"], "type": "周期", "tier": 2, "exchange": "SZ"},

    # --- 跨境/防御 ---
    "513110": {"name": "纳指100ETF", "sectors": ["跨境"], "themes": ["美股", "纳斯达克", "科技巨头"], "type": "跨境", "tier": 2, "exchange": "SH"},
    "513100": {"name": "标普500ETF", "sectors": ["跨境"], "themes": ["美股", "标普500"], "type": "跨境", "tier": 2, "exchange": "SH"},
    "159928": {"name": "消费ETF", "sectors": ["食品饮料", "消费"], "themes": ["消费", "白酒", "食品饮料"], "type": "消费", "tier": 2, "exchange": "SZ"},
}


# 新闻→关键词映射规则
NEWS_KEYWORD_RULES = {
    # 利多关键词 → 对应ETF主题
    "涨": ["买入", "利好", "加仓", "净流入", "走强", "大涨", "涨停", "领涨", "上涨", "拉涨"],
    "黄金": ["黄金", "贵金属", "避险"],
    "有色金属": ["有色金属", "铜", "铝", "小金属", "稀土", "工业金属"],
    "新能源": ["新能源", "锂电池", "固态电池", "光伏", "电动车"],
    "半导体": ["半导体", "芯片", "集成电路"],
    "人工智能": ["人工智能", "AI", "算力", "大模型", "机器人"],
    "电力": ["电力", "绿电", "公用事业"],
    "消费": ["消费", "白酒", "食品饮料", "零售"],

    # 利空关键词
    "利空_半导体": ["半导体大跌", "芯片大跌", "光刻", "存储芯片"],
    "利空_科技": ["科技股大跌", "AI大跌", "算力过剩", "电子净流出", "通信净流出"],
    "利空_美股": ["美股大跌", "费半暴跌", "科技巨头回调"],
    "利空_金": ["黄金大跌", "贵金属大跌"],
}


def mx_search_news(query: str, max_items: int = 8) -> List[Dict]:
    """调用妙想搜索获取新闻"""
    try:
        sys.path.insert(0, os.path.dirname(MX_SEARCH))
        from mx_search import MXSearch
        mx = MXSearch()
        result = mx.search(query)
        items = result.get("data", {}).get("data", {}).get("llmSearchResponse", {}).get("data", [])
        return items[:max_items]
    except Exception as e:
        print(f"[WARN] 妙想新闻搜索失败: {e}")
        return []


def extract_news_keywords(items: List[Dict]) -> Tuple[List[str], List[str]]:
    """从新闻标题+内容提取利多/利空关键词"""
    bullish = set()
    bearish = set()
    
    full_text = ""
    for item in items:
        title = item.get("title", "")
        content = item.get("content", "")[:500]
        full_text += " " + title + " " + content
    
    full_text = full_text.lower()
    
    # 关键字检测
    if any(k in full_text for k in ["净流入", "获主力", "资金涌入", "加仓", "涨停", "走强", "逆势上涨"]):
        # 找具体板块
        for kw in ["黄金","有色金属","贵金属","电力","新能源","稀土","铜","铝","汽车"]:
            if kw in full_text:
                bullish.add(kw)
    
    if any(k in full_text for k in ["净流出","出逃","大跌","暴跌","抛售","调整"]):
        for kw in ["电子","半导体","芯片","通信","科技","金融"]:
            if kw in full_text:
                bearish.add(kw)
        if "美股" in full_text or "费半" in full_text or "韩国" in full_text or "熔断" in full_text:
            bearish.add("美股科技")
    
    return list(bullish), list(bearish)


# ==================== HTSC API 调用 ====================

def htsc_call(*args: str) -> dict:
    cmd = ["python", HTSC_SKILL] + list(args)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if r.returncode != 0:
            return {"ok": False, "error": {"message": f"CLI exit {r.returncode}: {r.stderr[:200]}"}}
        if not r.stdout or not r.stdout.strip():
            return {"ok": False, "error": {"message": "empty response from CLI"}}
        return json.loads(r.stdout)
    except json.JSONDecodeError as e:
        return {"ok": False, "error": {"message": f"JSON parse error: {e} | stdout={r.stdout[:200]}"}}
    except Exception as e:
        return {"ok": False, "error": {"message": str(e)}}


def fetch_htsc_quotes() -> Dict[str, Dict]:
    result = {}
    for code, info in ETF_POOL.items():
        resp = htsc_call("getQuote", "--stock-code", code, "--exchange", info["exchange"])
        if resp.get("ok"):
            d = resp["data"]
            result[code] = {
                "name": d["stockName"],
                "price": d["currentPrice"],
                "prev_close": d["prevClose"],
                "limit_up": d.get("limitUp"),
                "limit_down": d.get("limitDown"),
                "bid": d.get("bidPrice1"),
                "ask": d.get("askPrice1"),
                "change_pct": d["change"],
                "is_suspended": d["isSuspended"],
            }
    return result


def fetch_htsc_account() -> Tuple[float, Dict[str, Dict]]:
    global total_assets, current_holdings
    total = 0
    holdings = {}
    
    resp = htsc_call("getAccountBalance")
    if resp.get("ok"):
        total = resp["data"].get("totalAssets", 0)
        print(f"  账户: CNY{total:,.0f} | 可用{resp['data'].get('availableBalance',0):,.0f}")
    
    resp2 = htsc_call("getPositions")
    if resp2.get("ok") and resp2["data"].get("positions"):
        for pos in resp2["data"]["positions"]:
            code = pos["stockCode"]
            holdings[code] = {
                "weight": pos.get("positionPct", 0),
                "cost": pos.get("costPrice", 0),
                "profit_pct": pos.get("profitPct", 0),
                "qty": pos.get("quantity", 0),
                "avail_qty": pos.get("availableQuantity", 0),
                "cur_price": pos.get("currentPrice", 0),
            }
            info = ETF_POOL.get(code, {"name": code})
            print(f"  {code} {info['name']}: {pos['positionPct']:.1f}% | 盈亏{pos['profitPct']:+.2f}%")
    
    total_assets, current_holdings = total, holdings
    return total, holdings


def htsc_buy(code: str, exchange: str, amount_pct: float):
    if amount_pct <= 0:
        return
    target = total_assets * amount_pct / 100
    resp = htsc_call("getQuote", "--stock-code", code, "--exchange", exchange)
    if not resp.get("ok"):
        return
    price = resp["data"]["currentPrice"]
    qty = int(target / price / 100) * 100
    if qty < 100:
        print(f"  [SKIP] {code} {ETF_POOL.get(code,{}).get('name','')}: {qty}股 < 1手")
        return
    order = htsc_call("submitOrder", "--direction", "buy", "--stock-code", code,
                      "--exchange", exchange, "--quantity", str(qty), "--order-type", "market")
    if order.get("ok"):
        print(f"  [BUY] {code} x{qty} @~{price:.3f} | #{order['data']['orderId']}")
    else:
        print(f"  [BUY FAIL] {code}: {order.get('error',{}).get('message','')}")


def htsc_sell(code: str, exchange: str, qty: int = None):
    if qty is not None:
        if qty <= 0:
            print(f"  [SKIP] {code}: sell qty {qty} <= 0")
            return
        order = htsc_call("submitOrder", "--direction", "sell", "--stock-code", code,
                          "--exchange", exchange, "--quantity", str(int(qty)), "--order-type", "market")
        if order.get("ok"):
            print(f"  [SELL] {code} x{int(qty)} | #{order['data']['orderId']}")
        else:
            print(f"  [SELL FAIL] {code}: {order.get('error',{}).get('message','')}")
        return
    resp = htsc_call("getPositions")
    if not resp.get("ok"):
        return
    for pos in resp["data"].get("positions", []):
        if pos["stockCode"] == code:
            qty = pos.get("availableQuantity", 0)
            if qty <= 0:
                print(f"  [SKIP] {code}: 无可用可卖")
                return
            order = htsc_call("submitOrder", "--direction", "sell", "--stock-code", code,
                              "--exchange", exchange, "--quantity", str(qty), "--order-type", "market")
            if order.get("ok"):
                print(f"  [SELL] {code} x{qty} | #{order['data']['orderId']}")
            else:
                print(f"  [SELL FAIL] {code}: {order.get('error',{}).get('message','')}")
            return


# ==================== ETF 评分 ====================

def score_etfs(quotes: Dict[str, Dict], bullish: List[str], bearish: List[str]) -> Tuple[List[Dict], str, str]:
    raw = []
    for code, info in ETF_POOL.items():
        q = quotes.get(code)
        if not q or q["is_suspended"]:
            continue
        
        chg = q["change_pct"]
        news_score = 0
        hit = []
        
        for k in bullish:
            if any(k in t for t in info["themes"] + info["sectors"]):
                news_score += 12
                hit.append(f"+{k}")
        for k in bearish:
            if any(k in t for t in info["themes"] + info["sectors"]):
                news_score -= 12
                hit.append(f"-{k}")
        
        raw.append({
            "code": code,
            "name": info["name"],
            "type": info["type"],
            "tier": info["tier"],
            "exchange": info["exchange"],
            "price": q["price"],
            "change_pct": chg,
            "news_score": max(-30, min(30, news_score)),
            "chg_score": round(max(-30, min(30, chg * 2.5)), 1),
            "total_score": 0,
            "hit_news": hit,
        })
    
    for s in raw:
        s["total_score"] = round(s["chg_score"] + s["news_score"], 1)
    
    raw.sort(key=lambda x: x["total_score"], reverse=True)
    
    if raw:
        avg = sum(s["change_pct"] for s in raw) / len(raw)
        if avg > 1:
            bias, note = "bullish", f"平均{avg:+.2f}%, 偏多"
        elif avg < -1:
            bias, note = "bearish", f"平均{avg:+.2f}%, 偏空"
        else:
            bias, note = "neutral", f"平均{avg:+.2f}%, 震荡"
    else:
        bias, note = "neutral", "无数据"
    
    return raw, bias, note


def generate_recommendation(scores: List[Dict], market_bias: str) -> Dict:
    recs = []
    target_total = {"bullish": 95, "neutral": 80, "bearish": 50}.get(market_bias, 80)
    
    # 当前持仓处理
    for code, h in current_holdings.items():
        cur = h.get("weight", 0)
        if cur <= 0:
            continue
        s = next((x for x in scores if x["code"] == code), None)
        if not s:
            continue
        if s["total_score"] < -15 and market_bias != "bullish":
            recs.append({"action": "卖出", "code": code, "name": s["name"], "reason": f"得分{s['total_score']:.1f}, 涨幅{s['change_pct']:+.2f}%", "target_weight": 0})
        elif s["total_score"] < 0:
            recs.append({"action": "减仓", "code": code, "name": s["name"], "reason": f"得分{s['total_score']:.1f}, 偏弱", "target_weight": round(cur / 2, 1)})
        else:
            recs.append({"action": "持有", "code": code, "name": s["name"], "reason": f"得分{s['total_score']:.1f}", "target_weight": round(cur, 1)})
    
    # 新开仓: 非熊市且得分>0
    if market_bias != "bearish":
        for s in scores[:5]:
            if s["code"] not in current_holdings and s["total_score"] > 0:
                max_w = 30 if s["tier"] == 1 else 15
                target = min(max_w, max(5, s["total_score"] / 3))
                recs.append({"action": "买入", "code": s["code"], "name": s["name"],
                            "reason": f"得分{s['total_score']:.1f}, 新闻{s['news_score']:+d}",
                            "target_weight": round(target, 1)})
                # duoge, you cangwei kongzhi
    
    # 仓位压缩
    total = sum(r["target_weight"] for r in recs)
    if total > target_total:
        change = [r for r in recs if r["action"] in ("买入", "加仓", "减仓")]
        hold_sum = sum(r["target_weight"] for r in recs if r["action"] == "持有")
        if change and sum(r["target_weight"] for r in change) > 0:
            scale = max(0, (target_total - hold_sum)) / sum(r["target_weight"] for r in change)
            for r in change:
                r["target_weight"] = round(max(0, r["target_weight"] * scale), 1)
    
    return {"recommendations": recs, "market_bias": market_bias, "target_total_weight": target_total}


# ==================== 主入口 ====================

def main():
    parser = argparse.ArgumentParser(description="曙光ETF轮动调仓 v1.4")
    parser.add_argument("--execute", action="store_true", help="自动执行调仓")
    parser.add_argument("--dry-run", action="store_true", help="只看新闻不评分")
    parser.add_argument("--news", type=str, default="", help="手动指定新闻关键词覆盖自动搜索")
    args = parser.parse_args()
    
    print("=" * 70)
    print(f"  曙光 ETF 轮动调仓系统 v1.4 | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("  数据源: HTSC + 妙想新闻搜索 + 腾讯GT")
    print("=" * 70)
    
    # --- 第一步: 妙想新闻 + 提取关键词 ---
    print("\n[STEP 1] 妙想新闻搜索...")
    bullish, bearish = [], []
    if args.news:
        parts = args.news.split("|")
        bullish = [k.strip() for k in parts[0].split(",") if k.strip()]
        bearish = [k.strip() for k in parts[1].split(",") if k.strip()] if len(parts) > 1 else []
        print(f"  [手动关键词] 利多: {bullish} 利空: {bearish}")
    else:
        news = mx_search_news("今日A股资金流向 热点板块 主力净流入")
        if news:
            print(f"  获取 {len(news)} 条新闻")
            for i, item in enumerate(news[:5], 1):
                print(f"  {i}. {item.get('title','')[:60]}")
            bullish, bearish = extract_news_keywords(news)
            print(f"  [自动提取] 利多: {bullish} | 利空: {bearish}")
        else:
            print("  新闻获取失败, 跳过关键词")
    
    if args.dry_run:
        print("\n[SKIP] dry-run模式, 仅输出新闻")
        return
    
    # --- 第二步: 获取账户 ---
    print("\n[STEP 2] 获取账户 (HTSC)...")
    fetch_htsc_account()
    
    # --- 第三步: 获取ETF行情 ---
    print("\n[STEP 3] 获取ETF行情 (HTSC)...")
    quotes = fetch_htsc_quotes()
    print(f"  获取 {len(quotes)}/{len(ETF_POOL)} 只")
    
    # --- 第四步: 评分 ---
    print("\n[STEP 4] ETF评分...")
    scores, bias, note = score_etfs(quotes, bullish, bearish)
    print(f"  市场: {bias.upper()} | {note}")
    
    # --- 第五步: 建议 ---
    print("\n[STEP 5] 调仓建议...")
    rec = generate_recommendation(scores, bias)
    
    # 输出
    print("\n" + "-" * 70)
    print(f"市场: {bias.upper()} | {note}")
    print()
    
    # 候选买入
    not_held = [s for s in scores if s["code"] not in current_holdings]
    print("候选买入 (未持有):")
    for i, s in enumerate(not_held[:5], 1):
        print(f"  {i}. {s['code']} {s['name']:<16s} 得分{s['total_score']:+.1f} 涨幅{s['change_pct']:+.2f}% | 新闻: {' '.join(s['hit_news']) if s['hit_news'] else '无'}")
    
    print()
    print("持仓评分:")
    for code, h in current_holdings.items():
        s = next((x for x in scores if x["code"] == code), None)
        if s:
            news_str = " ".join(s['hit_news']) if s['hit_news'] else "-"
            print(f"  {code} {s['name']:<16s} 仓位{h['weight']:.1f}% 得分{s['total_score']:+.1f} 涨{s['change_pct']:+.2f}% 盈{h.get('profit_pct',0):+.2f}% | {news_str}")
    
    print("\n" + "=" * 70)
    print("调仓建议")
    print("=" * 70)
    if not rec["recommendations"]:
        print("  暂无")
    else:
        for r in rec["recommendations"]:
            print(f"  [{r['action']:4s}] {r['code']} {r['name']:<16s} -> {r['target_weight']:.1f}% | {r['reason']}")
            _actions_log.append({"code": r["code"], "action": r["action"], "reason": r["reason"], "result": "executed"})
        print(f"\n  总仓位: {sum(r['target_weight'] for r in rec['recommendations']):.1f}% (上限{rec['target_total_weight']}%)")
    
    # --- [自进化] 保存执行前状态 ---
    _before_assets = total_assets
    _before_holdings = {code: h.get("weight",0) for code, h in current_holdings.items()}
    _actions_log = []
    # 保存
    out_dir = os.path.join(WORKSPACE, "data")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f"etf_rotator_{datetime.now().strftime('%Y%m%d_%H%M')}.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"bullish": bullish, "bearish": bearish, "bias": bias, "note": note,
                    "holdings": {code: h["weight"] for code, h in current_holdings.items()},
                    "recommendations": rec["recommendations"]}, f, ensure_ascii=False, indent=2)
        pend = htsc_call("listPendingOrders")
        if pend.get("ok") and pend["data"].get("orders"):
            for o in pend["data"]["orders"]:
                pn = o.get("stockName", "")
                di = o.get("direction", "")
                fi = o.get("filledQuantity", 0)
                qn = o.get("quantity", 0)
                oi = o.get("orderId", "")
                print(f"  [PENDING] {pn} {di} {fi}/{qn} | #{oi}")
        else:
            print("  [OK] no pending orders")
        pos2 = htsc_call("getPositions")
        if pos2.get("ok") and pos2["data"].get("positions"):
            mv = pos2["data"].get("totalMarketValue", 0)
            pnl = pos2["data"].get("totalProfit", 0)
            print(f"  pos value: {mv:,.0f} | pnl: {pnl:,.0f}")
    print(f"\n[OK] 结果: {out_file}")
    
    # 执行
    if args.execute:
        print("\n" + "*" * 70)
        print("  执行调仓...")
        print("*" * 70)
        for r in rec["recommendations"]:
            info = ETF_POOL.get(r["code"])
            if not info:
                continue
            if r["action"] == "卖出":
                htsc_sell(r["code"], info["exchange"])
            elif r["action"] == "买入" and r["target_weight"] > 0:
                htsc_buy(r["code"], info["exchange"], r["target_weight"])
            elif r["action"] == "\u51cf\u4ed3":
                cur_w = current_holdings.get(r["code"], {}).get("weight", 0)
                if cur_w - r["target_weight"] > 5:
                    h = current_holdings.get(r["code"], {})
                    cq = h.get("avail_qty", 0) or h.get("qty", 0)
                    cp = h.get("cur_price", 0)
                    if cq > 0 and cp > 0:
                        cv = cq * cp
                        tv = total_assets * r["target_weight"] / 100
                        sq = int((cv - tv) / cp / 100) * 100
                        if sq >= 100:
                            htsc_sell(r["code"], info["exchange"], qty=sq)
                        else:
                            print(f"  [SKIP] {r['code']}: sell {sq} < 1 lot")
                    else:
                        htsc_sell(r["code"], info["exchange"])
    
    if args.execute:
        pend = htsc_call("listPendingOrders")
        if pend.get("ok") and pend.get("data",{}).get("orders"):
            for o in pend["data"]["orders"]:
                sn = o.get("stockName", "")
                dr = o.get("direction", "")
                fi = o.get("filledQuantity", 0)
                qn = o.get("quantity", 0)
                oi = o.get("orderId", "")
                print(f"  [PENDING] " + sn + " " + dr + " " + str(fi) + "/" + str(qn) + " | #" + str(oi))
        else:
            print("  [OK] no pending orders")
        pos2 = htsc_call("getPositions")
        if pos2.get("ok") and pos2.get("data",{}).get("positions"):
            mv = pos2["data"]["totalMarketValue"]
            pnl = pos2["data"]["totalProfit"]
            print(f"  pos value: {mv:,.0f} | pnl: {pnl:,.0f}")
    if args.execute:
        print("\n[POST-CHECK] done, checking...")
        pend = htsc_call("listPendingOrders")
        if pend.get("ok") and pend.get("data",{}).get("orders"):
            for o in pend["data"]["orders"]:
                sn = o.get("stockName", "")
                dr = o.get("direction", "")
                fi = str(o.get("filledQuantity", 0))
                qn = str(o.get("quantity", 0))
                oi = str(o.get("orderId", ""))
                print("  [PENDING] " + sn + " " + dr + " " + fi + "/" + qn + " | #" + oi)
        else:
            print("  [OK] all orders filled")
        pos2 = htsc_call("getPositions")
        if pos2.get("ok") and pos2.get("data",{}).get("positions"):
            mv = str(pos2["data"]["totalMarketValue"])  
            pnl = str(pos2["data"]["totalProfit"])  
            print("  pos value: " + mv + " | pnl: " + pnl)
    print("\n[OK]")


if __name__ == "__main__":
    main()
