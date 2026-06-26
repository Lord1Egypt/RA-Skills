#!/usr/bin/env python3
"""
Expense Tracker — Core Ledger Script
Bilingual expense tracking. Handles add / list / search / report / balance.
Run: python3 ledger.py <action> [json_args]
"""

import json
import sys
import os
import uuid
import re
import csv
from datetime import datetime, date
from pathlib import Path
from typing import Optional, Dict, List, Any

LEDGER_DIR = Path.home() / ".qclaw" / "workspace" / "expense-ledger"
CONFIG_FILE = LEDGER_DIR / "config.json"
LEDGER_FILE = LEDGER_DIR / "ledger.json"

CATEGORY_MAP = {
    # Main categories (zh → id)
    "餐饮": "food", "food": "food",
    "购物": "shopping", "shopping": "shopping",
    "住房": "housing", "housing": "housing",
    "交通": "transport", "汽车": "transport", "transport": "transport",
    "通讯": "comm", "communication": "comm",
    "医疗": "medical", "medical": "medical",
    "人情": "social", "social": "social",
    "娱乐": "entertain", "entertainment": "entertain",
    "学习": "education", "education": "education",
    "育儿": "childcare", "childcare": "childcare",
    "旅行": "travel", "travel": "travel",
    "投资": "investment", "investment": "investment",
    "其他": "other", "other": "other",
}

SUBCATEGORY_KEYWORDS = {
    "food": {
        "breakfast": ["早餐", "早饭", "breakfast"],
        "lunch": ["午餐", "午饭", "中餐", "lunch"],
        "dinner": ["晚餐", "晚饭", "晚餐", "dinner"],
        "fruit": ["水果", "fruit", "apple", "banana"],
        "dairy": ["奶", "牛奶", "酸奶", "yogurt", "dairy", "milk"],
        "snacks": ["零食", "snacks", "chips", "candy"],
        "nuts": ["坚果", "nuts", "almonds", "瓜子"],
        "groceries": ["食材", "买菜", "菜钱", "grocery", "market"],
        "condiments": ["油盐酱醋", "调料", "调味品", "sauce"],
        "sweets": ["甜点", "蛋糕", "dessert", "烟酒", "wine", "beer", "酒"],
    },
    "shopping": {
        "household": ["日用品", "household", "tissue", "纸巾", "洗衣液", "detergent"],
        "clothing": ["鞋", "衣服", "服装", "外套", "dress", "clothing", "clothes"],
        "beauty": ["美妆", "化妆品", "护肤", "makeup", "cosmetics", "skincare"],
        "appliances": ["电器", "微波炉", "fridge", "电饭煲", "appliance"],
        "sports": ["运动", "瑜伽垫", "yoga", "gym", "sports"],
        "jewelry": ["饰品", "手表", "jewelry", "ring", "necklace"],
        "electronics": ["数码", "手机", "电脑", "laptop", "iPad", "electronics"],
        "kitchenware": ["厨具", "锅", "pots", "pans", "kitchenware"],
        "baby-items": ["儿童", "尿布", "diaper", "玩具", "baby"],
        "pregnancy": ["孕期", "孕妇", "pregnancy"],
        "general": ["购物", "购物-其他", "shopping"],
    },
    "transport": {
        "ride": ["打车", "的士", "taxi", "uber", "cab"],
        "flight": ["机票", "flight", "plane", "飞机"],
        "train": ["火车", "高铁", "train", "railway"],
        "bus": ["公交", "地铁", "bus", "subway", "metro"],
        "bike": ["单车", "共享单车", "bike", "scooter"],
        "car-maintenance": ["保养", "维修", "maintenance", "repair"],
        "parking": ["停车", "parking"],
        "fuel": ["加油", "fuel", "gas"],
        "fines": ["罚款", "fine", "ticket"],
        "insurance": ["车险", "car insurance"],
    },
    "housing": {
        "furniture": ["家具", "沙发", "sofa", "bed", "furniture"],
        "textiles": ["家纺", "被子", "床单", "窗帘", "curtain"],
        "utilities": ["物业水电", "物业费", "水费", "电费", "utilities"],
        "renovation": ["装修", "建材", "renovation"],
        "rent": ["房租", "租金", "rent"],
        "mortgage": ["房贷", "贷款", "mortgage", "loan"],
    },
    "comm": {
        "broadband": ["宽带", "internet", "broadband"],
        "phone": ["话费", "手机费", "phone", "SIM"],
        "fees": ["手续费", "刷卡手续费", "fee", "surcharge"],
    },
    "medical": {
        "hospital": ["住院", "hospital"],
        "healthcare": ["保健", "healthcare", "supplement"],
        "clinic": ["就诊", "挂号", "clinic", "doctor"],
        "medicine": ["药品", "药", "medicine", "pharmacy"],
        "dental": ["牙齿", "牙科", "dental"],
    },
    "social": {
        "gift-money": ["礼金", "gift money", "红包"],
        "gifts": ["礼品", "礼物", "gift", "present"],
        "dining-out": ["请客", "treat", "宴请", "dining-out"],
        "parents": ["孝敬爸妈", "孝敬", "爸妈", "parents"],
    },
    "entertain": {
        "gaming": ["游戏", "steam", "switch", "PS5", "game", "gaming"],
        "movies": ["电影", "cinema", "Netflix", "movie"],
        "party": ["聚会", "party", "gathering"],
        "ktv": ["KTV", "卡拉OK", "karaoke", "K歌"],
        "culture": ["演唱会", "演出", "concert", "show", "文娱"],
    },
    "education": {
        "materials": ["素材", "materials"],
        "training": ["培训", "课程", "course", "training"],
        "exam": ["考试", "exam", "test"],
        "stationery": ["文具", "stationery", "pen", "笔"],
        "books": ["书刊", "书籍", "books", "book"],
    },
    "childcare": {
        "formula": ["奶粉", "formula", "milk powder"],
        "sleepwear": ["寝居", "睡袋", "pajamas"],
        "toiletries": ["洗护", "shampoo", "toiletries"],
        "toys": ["玩具", "toys", "toy"],
        "kids-clothing": ["童装", "kids clothing"],
        "solid-food": ["辅食", "solid food"],
        "pregnancy-items": ["孕妇用品", "pregnancy items"],
    },
    "travel": {
        "team-building": ["团建", "team building"],
        "attractions": ["景点", "门票", "attractions"],
        "travel-fare": ["路费", "travel fare"],
        "hotel": ["酒店", "hotel", "住宿"],
        "souvenirs": ["纪念品", "souvenirs"],
        "travel-food": ["旅行吃饭", "travel dining"],
        "travel-services": ["服务", "导游", "tips"],
    },
    "investment": {
        "insurance": ["保险", "insurance"],
        "wealth-mgmt": ["理财", "fund", "wealth"],
        "stocks": ["股票", "shares", "stocks"],
    },
    "other": {
        "lending": ["借出", "lending", "借款"],
        "misc": ["其他", "misc"],
    },
}

# Reverse lookup: keyword → (main_cat, sub_cat)
_KEYWORD_TO_CAT = {}
for main_cat, sub_map in SUBCATEGORY_KEYWORDS.items():
    for sub_cat, keywords in sub_map.items():
        for kw in keywords:
            _KEYWORD_TO_CAT[kw.lower()] = (main_cat, sub_cat)


def ensure_dir():
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    if not LEDGER_FILE.exists():
        _init_ledger()


def _init_ledger():
    ledger = {
        "version": "2.0",
        "account": "default",
        "currency": "CNY",
        "created": datetime.now().isoformat(),
        "entries": [],
        "accounts": {
            "default": {"name": "Default / 默认账户", "currency": "CNY"},
            "cash": {"name": "Cash / 现金", "currency": "CNY"},
            "wechat": {"name": "WeChat Pay / 微信", "currency": "CNY"},
            "alipay": {"name": "Alipay / 支付宝", "currency": "CNY"},
            "visa": {"name": "Visa / 信用卡", "currency": "USD"},
        }
    }
    with open(LEDGER_FILE, "w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)


def load_ledger():
    ensure_dir()
    with open(LEDGER_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_ledger(ledger):
    with open(LEDGER_FILE, "w", encoding="utf-8") as f:
        json.dump(ledger, f, ensure_ascii=False, indent=2)


# ─── Parsing ─────────────────────────────────────────────────────────────────

def parse_expense(text: str) -> Optional[Dict]:
    """Parse natural language into expense dict. Returns None if not matched."""
    text = text.strip()
    if not text:
        return None

    amount = None
    currency = "CNY"

    # Currency patterns: ¥23, $23.5, USD 23, CNY 23, 23元, 23.5元
    patterns = [
        r'[\$¥€£]\s*([\d,]+\.?\d*)',
        r'([\d,]+\.?\d*)\s*(?:元|块|USD|CNY|EUR|GBP)',
        r'(?:USD|CNY|EUR|GBP)\s*([\d,]+\.?\d*)',
    ]
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            raw_amt = m.group(1).replace(',', '')
            amount = round(float(raw_amt), 2)
            break

    if amount is None:
        # Try plain number at end or after common words
        m = re.search(r'(?:花了|spent|消费|花费|用了|买|买了|花)\s*([\d]+\.?\d*)', text, re.I)
        if m:
            amount = round(float(m.group(1).replace(',', '')), 2)

    if amount is None or amount <= 0:
        return None

    # Currency detection
    if '$' in text or re.search(r'\bUSD\b', text, re.I):
        currency = "USD"
    elif '€' in text or re.search(r'\bEUR\b', text, re.I):
        currency = "EUR"
    elif '£' in text or re.search(r'\bGBP\b', text, re.I):
        currency = "GBP"
    else:
        currency = "CNY"

    # Category detection
    cat, subcat = _detect_category(text)

    # Member detection
    member = _detect_member(text)

    # Note: strip amount and common prefixes
    note = text
    note = re.sub(r'[\$¥€£]\s*[\d,]+\.?\d*', '', note)
    note = re.sub(r'[\d,]+\.?\d*\s*(?:元|块)', '', note)
    note = re.sub(r'(?:花了|spent|消费|花费|用了|买|买了|花)', '', note, flags=re.I)
    note = re.sub(r'[（(]成员[-_]?\w+[)）]', '', note)
    note = re.sub(r',\s*member[-\w]+', '', note, flags=re.I)
    note = re.sub(r'\b(今天|昨天|本周|月|年)\b', '', note)
    note = re.sub(r'[，。,\s]+', ' ', note).strip()
    if not note:
        note = cat.capitalize()

    return {
        "amount": amount,
        "currency": currency,
        "category": cat,
        "subcategory": subcat,
        "note": note,
        "member": member,
        "raw": text,
        "lang": "zh" if any('\u4e00' <= c <= '\u9fff' for c in text) else "en",
    }


def _detect_category(text: str) -> tuple:
    text_lower = text.lower()
    # Try direct main category match first
    for key, cat_id in CATEGORY_MAP.items():
        if key.lower() in text_lower:
            subcat = _detect_subcategory(text_lower, cat_id)
            return cat_id, subcat

    # Try keyword lookup
    words = re.findall(r'[\w]+', text_lower)
    for word in words:
        if word in _KEYWORD_TO_CAT:
            cat, subcat = _KEYWORD_TO_CAT[word]
            return cat, subcat

    # Sub-word matching
    for kw, (cat, subcat) in _KEYWORD_TO_CAT.items():
        if kw in text_lower:
            return cat, subcat

    return "other", "misc"


def _detect_subcategory(text_lower: str, main_cat: str) -> str:
    sub_map = SUBCATEGORY_KEYWORDS.get(main_cat, {})
    for subcat, keywords in sub_map.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                return subcat
    return list(sub_map.keys())[0] if sub_map else "misc"


def _detect_member(text: str) -> Optional[str]:
    patterns = [
        r'[（(]成员[-_]?(\w+)[)）]',
        r',\s*member[-_]?(\w+)',
        r'\bfor\s+(\w+)\b',
        r'给(\w+)买',
        r'帮(\w+)买',
    ]
    for pat in patterns:
        m = re.search(pat, text, re.I)
        if m:
            return m.group(1)
    return None


# ─── Actions ─────────────────────────────────────────────────────────────────

def action_add(args: dict) -> dict:
    ensure_dir()
    ledger = load_ledger()

    entry = {
        "id": str(uuid.uuid4())[:8],
        "date": args.get("date", date.today().isoformat()),
        "category": args["category"],
        "subcategory": args.get("subcategory", "misc"),
        "amount": float(args["amount"]),
        "currency": args.get("currency", "CNY"),
        "account": args.get("account", "default"),
        "note": args.get("note", ""),
        "member": args.get("member"),
        "tags": args.get("tags", []),
        "lang": args.get("lang", "zh"),
        "raw": args.get("raw", ""),
        "created_at": datetime.now().isoformat(),
    }

    ledger["entries"].append(entry)
    save_ledger(ledger)

    return {
        "ok": True,
        "entry": entry,
        "message": _fmt_confirm(entry),
    }


def action_list(args: dict) -> dict:
    ledger = load_ledger()
    entries = ledger["entries"]

    # Filter by date range
    start = args.get("start")
    end = args.get("end")
    if start:
        entries = [e for e in entries if e["date"] >= start]
    if end:
        entries = [e for e in entries if e["date"] <= end]

    # Filter by category
    cat = args.get("category")
    if cat:
        entries = [e for e in entries if e["category"] == cat]

    # Filter by account
    acc = args.get("account")
    if acc:
        entries = [e for e in entries if e.get("account") == acc]

    # Sort desc by date
    entries.sort(key=lambda x: x["date"], reverse=True)
    limit = args.get("limit", 100)
    entries = entries[:limit]

    return {
        "ok": True,
        "count": len(entries),
        "entries": entries,
    }


def action_report(args: dict) -> dict:
    """Generate expense report."""
    ledger = load_ledger()
    entries = ledger["entries"]

    # Filter by period
    period = args.get("period", "month")  # day / week / month / year / custom
    today = date.today()

    if period == "day":
        start = today.isoformat()
        end = today.isoformat()
    elif period == "week":
        from datetime import timedelta
        start = (today - timedelta(days=6)).isoformat()
        end = today.isoformat()
    elif period == "month":
        start = today.replace(day=1).isoformat()
        end = today.isoformat()
    elif period == "year":
        start = today.replace(month=1, day=1).isoformat()
        end = today.isoformat()
    else:
        start = args.get("start", date(2000, 1, 1).isoformat())
        end = args.get("end", today.isoformat())

    filtered = [e for e in entries if start <= e["date"] <= end]

    # Aggregate (convert into default currency)
    config = {}
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, encoding="utf-8") as f:
            config = json.load(f)
    report_currency = str(config.get("default_currency", "CNY")).upper()
    exchange_rates = config.get("exchange_rates", {}) or {}
    warnings: List[str] = []

    def convert_amount(amount: float, entry_currency: str) -> float:
        cur = str(entry_currency).upper()
        if cur == report_currency:
            return float(amount)

        # Preferred: <entry>_<report> (e.g. USD_CNY means 1 USD = X CNY)
        key = f"{cur}_{report_currency}"
        if key in exchange_rates:
            return float(amount) * float(exchange_rates[key])

        # Fallback: reverse rate (e.g. CNY_USD then amount_CNY -> USD requires division)
        rev_key = f"{report_currency}_{cur}"
        if rev_key in exchange_rates and float(exchange_rates[rev_key]) != 0:
            return float(amount) / float(exchange_rates[rev_key])

        # If missing rate, we assume the amount is already in report currency.
        # This avoids mixing currencies silently, but we still tell the caller.
        warnings.append(f"Missing exchange rate: {cur}->{report_currency}; assumed already {report_currency}.")
        return float(amount)

    total = 0.0
    by_cat = {}
    by_subcat = {}
    daily = {}

    for e in filtered:
        conv = convert_amount(e["amount"], e.get("currency", "CNY"))
        total += conv
        by_cat[e["category"]] = by_cat.get(e["category"], 0) + conv
        sub = f"{e['category']}-{e.get('subcategory', 'misc')}"
        by_subcat[sub] = by_subcat.get(sub, 0) + conv
        daily[e["date"]] = daily.get(e["date"], 0) + conv

    # Top category
    top_cat = max(by_cat, key=by_cat.get) if by_cat else None
    top_amt = by_cat[top_cat] if top_cat else 0

    return {
        "ok": True,
        "period": {"start": start, "end": end, "kind": period},
        "currency": report_currency,
        "total": round(total, 2),
        "count": len(filtered),
        "by_category": {k: round(v, 2) for k, v in sorted(by_cat.items(), key=lambda x: -x[1])},
        "by_subcategory": {k: round(v, 2) for k, v in sorted(by_subcat.items(), key=lambda x: -x[1])},
        "daily": {k: round(v, 2) for k, v in sorted(daily.items())},
        "top_category": top_cat,
        "top_amount": round(top_amt, 2),
        "top_pct": round(top_amt / total * 100, 1) if total > 0 else 0,
        "entries": filtered,
        "warnings": warnings,
    }


def action_balance(args: dict) -> dict:
    """Get balance across all accounts."""
    ledger = load_ledger()
    accounts = ledger.get("accounts", {})

    result = {}
    for acc_id, acc_info in accounts.items():
        acc_entries = [e for e in ledger["entries"] if e.get("account", "default") == acc_id]
        total = sum(e["amount"] for e in acc_entries)
        result[acc_id] = {
            "name": acc_info.get("name", acc_id),
            "currency": acc_info.get("currency", "CNY"),
            "count": len(acc_entries),
            "total": round(total, 2),
        }

    return {"ok": True, "accounts": result}


def action_config(args: dict) -> dict:
    """Update config."""
    ensure_dir()
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, encoding="utf-8") as f:
            config = json.load(f)
    else:
        config = {}

    if "budgets" in args:
        config["budgets"] = args["budgets"]
    if "default_account" in args:
        config["default_account"] = args["default_account"]
    if "default_currency" in args:
        config["default_currency"] = args["default_currency"]
    if "language" in args:
        config["language"] = args["language"]

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    return {"ok": True, "config": config}


def _fmt_confirm(entry: dict) -> str:
    cat_zh = {
        "food": "餐饮", "shopping": "购物", "housing": "住房", "transport": "交通",
        "comm": "通讯", "medical": "医疗", "social": "人情", "entertain": "娱乐",
        "education": "学习", "childcare": "育儿", "travel": "旅行",
        "investment": "投资", "other": "其他",
    }
    sym = {"CNY": "¥", "USD": "$", "EUR": "€", "GBP": "£"}.get(entry["currency"], "¥")
    cat = cat_zh.get(entry["category"], entry["category"])
    date_str = entry["date"]
    return f"✅ 记账完成 | Recorded: {date_str} {cat} {entry.get('subcategory','')} {sym}{entry['amount']} — {entry.get('note','')}"


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: ledger.py <action> [json_args]"}))
        sys.exit(1)

    action = sys.argv[1]
    args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

    handlers = {
        "add": action_add,
        "list": action_list,
        "report": action_report,
        "balance": action_balance,
        "config": action_config,
    }

    if action not in handlers:
        print(json.dumps({"error": f"Unknown action: {action}"}))
        sys.exit(1)

    result = handlers[action](args)
    print(json.dumps(result, ensure_ascii=False, indent=2))
