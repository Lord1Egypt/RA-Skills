#!/usr/bin/env python3
"""
deal-hunter-alert-claw: 商业捡漏预警虾 - 多平台信息采集与预警脚本

用法:
  python3 monitor.py --config rules.json          # 按规则文件启动监控（单次扫描）
  python3 monitor.py --rule '{"platform":"xianyu","keyword":"iPhone 15","price_max":5000}'
  python3 monitor.py --list-platforms             # 列出支持的平台

输出:
  - 符合条件的标的以 JSON 格式打印到 stdout
  - 每条记录包含: id, platform, title, price, url, discount_rate, risk_level, detail
"""

import argparse
import json
import sys
import time
import random
import hashlib
import os
from datetime import datetime
from pathlib import Path

# ── 数据目录 ──────────────────────────────────────────────────────────────────
DATA_DIR = Path(os.environ.get("DEAL_HUNTER_DATA", Path.home() / ".openclaw/workspace/deal-hunter-data"))
SEEN_IDS_FILE = DATA_DIR / "seen_ids.json"
ALERTS_LOG = DATA_DIR / "alerts_log.jsonl"

SUPPORTED_PLATFORMS = {
    "xianyu":    "闲鱼 - 二手商品",
    "zhuanzhuan":"转转 - 二手商品",
    "lianjia":   "链家 - 二手房/急售",
    "ke":        "贝壳 - 二手房/急售",
    "paimai":    "阿里拍卖 - 法拍房/资产",
    "jd_auction":"京东拍卖 - 法拍房/资产",
    "ccgp":      "政府采购网 - 招标",
    "bidding":   "中国招标投标公共服务平台 - 招标",
}

# ── 工具函数 ──────────────────────────────────────────────────────────────────

def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_seen_ids() -> set:
    if SEEN_IDS_FILE.exists():
        return set(json.loads(SEEN_IDS_FILE.read_text()))
    return set()

def save_seen_ids(seen: set):
    SEEN_IDS_FILE.write_text(json.dumps(list(seen)))

def log_alert(alert: dict):
    with open(ALERTS_LOG, "a") as f:
        f.write(json.dumps(alert, ensure_ascii=False) + "\n")

def make_id(platform: str, item_id: str) -> str:
    return f"{platform}:{item_id}"

def random_sleep(min_s=3, max_s=8):
    time.sleep(random.uniform(min_s, max_s))

# ── 模拟采集（实际部署时替换为真实爬虫逻辑）────────────────────────────────────

def fetch_xianyu(keyword: str, price_max: float = None, price_min: float = None) -> list:
    """
    闲鱼采集（示例实现）
    实际部署：使用 Selenium 模拟登录后抓取搜索结果页
    API: https://2.taobao.com/search?q={keyword}
    """
    print(f"[采集] 闲鱼 | 关键词: {keyword} | 价格上限: {price_max}", file=sys.stderr)
    random_sleep(2, 5)
    # 返回示例数据结构（实际替换为真实抓取结果）
    return [
        {
            "id": f"xianyu_demo_{hashlib.md5(keyword.encode()).hexdigest()[:8]}",
            "platform": "xianyu",
            "title": f"[示例] {keyword} 九成新 低价出",
            "price": price_max * 0.6 if price_max else 3000,
            "market_price": price_max * 0.9 if price_max else 5000,
            "url": f"https://2.taobao.com/item/demo",
            "seller_score": 120,
            "location": "上海",
            "published_at": datetime.now().isoformat(),
            "description": "个人闲置，九成新，支持验货",
            "_demo": True,
        }
    ]

def fetch_lianjia(city: str, district: str = None, price_max: float = None) -> list:
    """
    链家急售房源采集（示例实现）
    实际部署：抓取 https://city.lianjia.com/ershoufang/jijia/
    """
    print(f"[采集] 链家 | 城市: {city} | 区域: {district} | 价格上限: {price_max}万", file=sys.stderr)
    random_sleep(3, 6)
    return [
        {
            "id": f"lianjia_demo_{hashlib.md5(city.encode()).hexdigest()[:8]}",
            "platform": "lianjia",
            "title": f"[示例] {city}{district or ''}急售 精装修 满五唯一",
            "price": (price_max or 500) * 0.72,
            "market_price": price_max or 500,
            "area": 89,
            "unit_price": int(((price_max or 500) * 0.72 * 10000) / 89),
            "market_unit_price": int(((price_max or 500) * 10000) / 89),
            "url": "https://lianjia.com/ershoufang/demo",
            "district": district or "朝阳区",
            "published_at": datetime.now().isoformat(),
            "description": "业主急售，价格可谈",
            "_demo": True,
        }
    ]

def fetch_paimai(city: str, district: str = None, price_max: float = None) -> list:
    """
    阿里拍卖法拍房采集（示例实现）
    实际部署：抓取 https://paimai.taobao.com/
    """
    print(f"[采集] 阿里拍卖 | 城市: {city} | 区域: {district} | 价格上限: {price_max}万", file=sys.stderr)
    random_sleep(3, 7)
    return [
        {
            "id": f"paimai_demo_{hashlib.md5(city.encode()).hexdigest()[:8]}",
            "platform": "paimai",
            "title": f"[示例] {city}{district or ''}法拍房 住宅",
            "price": (price_max or 500) * 0.65,
            "market_price": price_max or 500,
            "area": 102,
            "auction_start": datetime.now().isoformat(),
            "url": "https://paimai.taobao.com/demo",
            "district": district or "海淀区",
            "published_at": datetime.now().isoformat(),
            "description": "法院拍卖，带租约，需自行核实产权",
            "_demo": True,
        }
    ]

def fetch_ccgp(keyword: str, budget_min: float = None, budget_max: float = None) -> list:
    """
    政府采购网招标信息采集（示例实现）
    实际部署：抓取 https://search.ccgp.gov.cn/bxsearch
    """
    print(f"[采集] 政府采购网 | 关键词: {keyword}", file=sys.stderr)
    random_sleep(2, 4)
    return [
        {
            "id": f"ccgp_demo_{hashlib.md5(keyword.encode()).hexdigest()[:8]}",
            "platform": "ccgp",
            "title": f"[示例] {keyword}系统建设项目采购",
            "budget": budget_max * 0.8 if budget_max else 500000,
            "buyer": "某市政府部门",
            "deadline": "2026-04-30",
            "url": "https://ccgp.gov.cn/demo",
            "published_at": datetime.now().isoformat(),
            "description": "公开招标，需具备相关资质",
            "_demo": True,
        }
    ]

# ── 筛选与估值 ────────────────────────────────────────────────────────────────

def calculate_discount(price: float, market_price: float) -> float:
    """计算折扣率（相对市场价低多少）"""
    if not market_price or market_price <= 0:
        return 0
    return (market_price - price) / market_price * 100

def assess_risk(item: dict, platform: str) -> tuple[str, list]:
    """
    风险评估，返回 (risk_level, risk_notes)
    risk_level: "low" | "medium" | "high"
    """
    risk_notes = []
    risk_level = "low"

    desc = (item.get("description", "") + " " + item.get("title", "")).lower()

    # 高风险关键词
    high_risk_keywords = ["凶宅", "事故房", "无产权证", "小产权", "违建"]
    for kw in high_risk_keywords:
        if kw in desc:
            risk_notes.append(f"⚠️ 高风险：含关键词「{kw}」")
            risk_level = "high"

    # 中风险关键词
    medium_risk_keywords = {
        "带租约": "存在租约，需核实租客情况",
        "共有产权": "共有产权，需所有人同意出售",
        "换过屏": "可能为翻新机",
        "换过电池": "电池已更换，注意续航",
        "私下交易": "⚠️ 疑似诈骗话术",
    }
    for kw, note in medium_risk_keywords.items():
        if kw in desc:
            risk_notes.append(f"⚡ 注意：{note}")
            if risk_level == "low":
                risk_level = "medium"

    # 卖家信誉检查（二手商品）
    if platform in ("xianyu", "zhuanzhuan"):
        seller_score = item.get("seller_score", 999)
        if seller_score < 50:
            risk_notes.append(f"⚡ 卖家信誉分较低（{seller_score}）")
            if risk_level == "low":
                risk_level = "medium"

    return risk_level, risk_notes

def filter_and_score(items: list, rule: dict) -> list:
    """根据规则筛选并评分"""
    results = []
    for item in items:
        platform = item.get("platform", "")

        # 价格筛选
        price = item.get("price", 0)
        price_max = rule.get("price_max")
        price_min = rule.get("price_min", 0)
        if price_max and price > price_max:
            continue
        if price < price_min:
            continue

        # 折扣率计算
        market_price = item.get("market_price") or item.get("budget")
        discount_rate = calculate_discount(price, market_price) if market_price else None

        # 折扣阈值筛选
        min_discount = rule.get("min_discount_pct", 0)
        if discount_rate is not None and discount_rate < min_discount:
            continue

        # 风险评估
        risk_level, risk_notes = assess_risk(item, platform)
        if risk_level == "high":
            continue  # 高风险直接过滤

        item["discount_rate"] = round(discount_rate, 1) if discount_rate else None
        item["risk_level"] = risk_level
        item["risk_notes"] = risk_notes
        results.append(item)

    return results

# ── 主流程 ────────────────────────────────────────────────────────────────────

def run_rule(rule: dict, seen_ids: set) -> list:
    """执行单条监控规则，返回新发现的符合条件标的"""
    platform = rule.get("platform", "").lower()
    new_alerts = []

    # 根据平台调用对应采集函数
    if platform == "xianyu":
        items = fetch_xianyu(
            keyword=rule.get("keyword", ""),
            price_max=rule.get("price_max"),
            price_min=rule.get("price_min"),
        )
    elif platform == "lianjia":
        items = fetch_lianjia(
            city=rule.get("city", "beijing"),
            district=rule.get("district"),
            price_max=rule.get("price_max"),
        )
    elif platform == "paimai":
        items = fetch_paimai(
            city=rule.get("city", "beijing"),
            district=rule.get("district"),
            price_max=rule.get("price_max"),
        )
    elif platform == "ccgp":
        items = fetch_ccgp(
            keyword=rule.get("keyword", ""),
            budget_min=rule.get("budget_min"),
            budget_max=rule.get("budget_max"),
        )
    else:
        print(f"[警告] 不支持的平台: {platform}", file=sys.stderr)
        return []

    # 筛选
    filtered = filter_and_score(items, rule)

    # 去重
    for item in filtered:
        uid = make_id(platform, item["id"])
        if uid not in seen_ids:
            seen_ids.add(uid)
            new_alerts.append(item)

    return new_alerts

def format_alert_message(item: dict) -> str:
    """格式化预警消息"""
    platform_names = {
        "xianyu": "闲鱼", "zhuanzhuan": "转转",
        "lianjia": "链家", "ke": "贝壳",
        "paimai": "阿里拍卖", "jd_auction": "京东拍卖",
        "ccgp": "政府采购网", "bidding": "招标平台",
    }
    platform_name = platform_names.get(item.get("platform", ""), item.get("platform", ""))

    lines = [
        f"🦞 **捡漏预警** | {platform_name}",
        f"📌 {item.get('title', '未知标的')}",
        f"💰 价格：{item.get('price', '?')}",
    ]

    if item.get("market_price"):
        lines.append(f"📊 市场价：{item.get('market_price')} | 折扣：{item.get('discount_rate', '?')}%")

    if item.get("url"):
        lines.append(f"🔗 {item.get('url')}")

    if item.get("risk_notes"):
        lines.append("⚡ 风险提示：" + "；".join(item["risk_notes"]))

    if item.get("_demo"):
        lines.append("*(示例数据，实际部署后替换为真实采集)*")

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="商业捡漏预警虾 - 多平台监控脚本")
    parser.add_argument("--config", help="监控规则 JSON 文件路径")
    parser.add_argument("--rule", help="单条规则 JSON 字符串")
    parser.add_argument("--list-platforms", action="store_true", help="列出支持的平台")
    parser.add_argument("--output", choices=["json", "text"], default="text", help="输出格式")
    args = parser.parse_args()

    if args.list_platforms:
        print("支持的平台：")
        for k, v in SUPPORTED_PLATFORMS.items():
            print(f"  {k:15} {v}")
        return

    ensure_data_dir()
    seen_ids = load_seen_ids()
    all_alerts = []

    if args.rule:
        rule = json.loads(args.rule)
        alerts = run_rule(rule, seen_ids)
        all_alerts.extend(alerts)
    elif args.config:
        config_path = Path(args.config)
        if not config_path.exists():
            print(f"[错误] 规则文件不存在: {config_path}", file=sys.stderr)
            sys.exit(1)
        rules = json.loads(config_path.read_text())
        if isinstance(rules, dict):
            rules = [rules]
        for rule in rules:
            alerts = run_rule(rule, seen_ids)
            all_alerts.extend(alerts)
            if len(rules) > 1:
                random_sleep(2, 4)
    else:
        parser.print_help()
        return

    save_seen_ids(seen_ids)

    # 记录日志
    for alert in all_alerts:
        log_alert(alert)

    # 输出结果
    if args.output == "json":
        print(json.dumps(all_alerts, ensure_ascii=False, indent=2))
    else:
        if not all_alerts:
            print("✅ 本次扫描未发现新的符合条件标的")
        else:
            print(f"\n🎯 发现 {len(all_alerts)} 个新标的：\n")
            for item in all_alerts:
                print(format_alert_message(item))
                print("─" * 50)

if __name__ == "__main__":
    main()
