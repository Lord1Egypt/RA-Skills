#!/usr/bin/env python3
"""
Fruit Pi - Global Fruit Price Collector v1.0.0

Manages fruit price tracking:
  - Maintains a fruit pool with configured price sources
  - Collects prices from configured websites
  - Converts prices to RMB/kg with foreign currency preserved
  - Auto-discovers new sources when existing ones fail
  - Recommends seasonal fruits outside the pool

Usage:
    python3 fruit-pi.py                              # Collect all prices (main mode)
    python3 fruit-pi.py --collect <fruit_name>       # Collect price for one fruit
    python3 fruit-pi.py --list                       # List fruit pool
    python3 fruit-pi.py --add <name> [options]       # Add fruit to pool
    python3 fruit-pi.py --remove <name>              # Remove fruit from pool
    python3 fruit-pi.py --recommend                  # Show seasonal recommendations
    python3 fruit-pi.py --status                     # Check pool health
    python3 fruit-pi.py --refresh-sources <name>     # Find new sources for a fruit
"""

import json
import os
import re
import sys
import subprocess
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
FRUIT_POOL_PATH = os.path.join(WORKSPACE, "memory", "fruit-pool.json")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Exchange rate cache (1h TTL)
EXCHANGE_RATE_CACHE_PATH = os.path.join(SCRIPT_DIR, ".rate_cache.json")
EXCHANGE_RATE_API = "https://api.frankfurter.app/latest?from=USD"
EXCHANGE_RATE_CACHE_TTL = 3600  # 1 hour

# ─── Currency Config ──────────────────────────────────────────────────
CURRENCY_SYMBOLS = {
    "CNY": "¥", "USD": "$", "EUR": "€", "GBP": "£",
    "THB": "฿", "JPY": "¥", "KRW": "₩", "HKD": "HK$",
    "TWD": "NT$", "SGD": "S$", "MYR": "RM", "VND": "₫",
    "INR": "₹", "IDR": "Rp", "PHP": "₱", "AUD": "A$",
    "CAD": "C$", "NZD": "NZ$", "BRL": "R$", "CHF": "Fr",
}

DEFAULT_EXCHANGE_RATES = {
    "CNY": 1.0, "USD": 7.24, "EUR": 7.85, "GBP": 9.12,
    "THB": 0.20, "JPY": 0.048, "KRW": 0.0053, "HKD": 0.93,
    "TWD": 0.23, "SGD": 5.38, "MYR": 1.55, "VND": 0.00029,
    "INR": 0.087, "IDR": 0.00045, "PHP": 0.13, "AUD": 4.74,
    "CAD": 5.32, "NZD": 4.40, "BRL": 1.32, "CHF": 8.04,
}

# ─── Helpers ──────────────────────────────────────────────────────────

def log(msg):
    print(f"[FruitPi] {msg}", file=sys.stderr)


def utcnow():
    return datetime.now(timezone.utc)


def load_fruit_pool():
    """Load fruit pool, create default if not exists."""
    os.makedirs(os.path.dirname(FRUIT_POOL_PATH), exist_ok=True)
    if not os.path.exists(FRUIT_POOL_PATH):
        pool = {
            "fruits": {},
            "seasonal_fruits": [
                {"name": "荔枝", "season": "5-7月", "en_name": "Lychee"},
                {"name": "樱桃", "season": "5-7月", "en_name": "Cherry"},
                {"name": "杨梅", "season": "5-6月", "en_name": "Waxberry"},
                {"name": "榴莲", "season": "5-8月", "en_name": "Durian"},
                {"name": "芒果", "season": "4-7月", "en_name": "Mango"},
                {"name": "山竹", "season": "5-9月", "en_name": "Mangosteen"},
            ],
            "metadata": {
                "version": 1,
                "created": utcnow().isoformat(),
                "last_collected": None,
            }
        }
        save_fruit_pool(pool)
        log(f"Created default fruit pool at {FRUIT_POOL_PATH}")
    else:
        with open(FRUIT_POOL_PATH, "r", encoding="utf-8") as f:
            pool = json.load(f)
    return pool


def save_fruit_pool(pool):
    os.makedirs(os.path.dirname(FRUIT_POOL_PATH), exist_ok=True)
    with open(FRUIT_POOL_PATH, "w", encoding="utf-8") as f:
        json.dump(pool, f, ensure_ascii=False, indent=2)


def get_default_pool_path():
    return FRUIT_POOL_PATH


def get_exchange_rate(from_currency, to_currency="CNY"):
    """Get exchange rate, uses cache for 1h."""
    if from_currency == to_currency:
        return 1.0
    rate = get_cached_rate(from_currency, to_currency)
    if rate:
        return rate
    # Try API
    try:
        url = f"https://api.frankfurter.app/latest?from={from_currency}&to={to_currency}"
        req = urllib.request.Request(url, headers={"User-Agent": "FruitPi/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            rate = data["rates"][to_currency]
            cache_rate(from_currency, to_currency, rate)
            return rate
    except Exception as e:
        log(f"Exchange rate API failed for {from_currency}→{to_currency}: {e}")
        # Fallback to default
        rate = get_fallback_rate(from_currency, to_currency)
        if rate:
            return rate
        log(f"No fallback rate for {from_currency}→{to_currency}, assuming 1.0")
        return 1.0


def get_fallback_rate(from_curr, to_curr):
    """Use DEFAULT_EXCHANGE_RATES for fallback."""
    if from_curr in DEFAULT_EXCHANGE_RATES and to_curr in DEFAULT_EXCHANGE_RATES:
        # from_curr to CNY, then CNY to to_curr... actually we just want from_curr to to_curr
        # Rate: 1 from_curr = ? to_curr
        # 1 from_curr = X CNY, 1 to_curr = Y CNY
        # So: 1 from_curr = X/Y to_curr
        rate_to_cny_from = DEFAULT_EXCHANGE_RATES.get(from_curr, 1.0)
        rate_to_cny_to = DEFAULT_EXCHANGE_RATES.get(to_curr, 1.0)
        if rate_to_cny_to > 0:
            return round(rate_to_cny_from / rate_to_cny_to, 6)
    return None


def cache_rate(from_curr, to_curr, rate):
    """Cache exchange rate with timestamp."""
    cache = {}
    if os.path.exists(EXCHANGE_RATE_CACHE_PATH):
        try:
            with open(EXCHANGE_RATE_CACHE_PATH) as f:
                cache = json.load(f)
        except:
            pass
    key = f"{from_curr}→{to_curr}"
    cache[key] = {"rate": rate, "ts": utcnow().isoformat()}
    with open(EXCHANGE_RATE_CACHE_PATH, "w") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def get_cached_rate(from_curr, to_curr):
    """Get cached rate if not expired."""
    if not os.path.exists(EXCHANGE_RATE_CACHE_PATH):
        return None
    try:
        with open(EXCHANGE_RATE_CACHE_PATH) as f:
            cache = json.load(f)
        key = f"{from_curr}→{to_curr}"
        entry = cache.get(key)
        if entry:
            ts = datetime.fromisoformat(entry["ts"])
            if (utcnow() - ts).total_seconds() < EXCHANGE_RATE_CACHE_TTL:
                return entry["rate"]
    except:
        pass
    return None


def convert_price(price, from_currency, to_currency="CNY"):
    """Convert price to target currency."""
    rate = get_exchange_rate(from_currency, to_currency)
    return round(price * rate, 2), rate


def fetch_url(url, timeout=10):
    """Fetch URL content with basic headers."""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                              "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
            }
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="replace")
            return html
    except Exception as e:
        log(f"fetch_url failed for {url}: {e}")
        return None


def extract_price_from_text(text, fruit_name=""):
    """
    Try to extract price info from text.
    Returns list of (price, unit, currency) tuples.
    """
    results = []

    # Common patterns: 价格: 12.5元/kg, ￥15/斤, $5.99/kg, ฿120/kg
    patterns = [
        # RMB patterns - 元/公斤, 元/kg etc (already per kg)
        (r"(\d+\.?\d*)\s*元\s*[/每]?\s*(公斤|kg|千克)", "CNY", "kg"),
        (r"[¥￥]\s*(\d+\.?\d*)\s*[/每]?\s*(公斤|kg|千克)", "CNY", "kg"),
        (r"均价\s*(\d+\.?\d*)\s*元", "CNY", "kg"),
        # RMB patterns - 元/斤 (need ×2 to kg)
        (r"(\d+\.?\d*)\s*元\s*[/每]?\s*斤", "CNY", "jin"),
        (r"[¥￥]\s*(\d+\.?\d*)\s*[/每]?\s*斤", "CNY", "jin"),
        # USD patterns - only with explicit $ + unit
        (r"\$\s*(\d+\.?\d*)\s*[/每]?\s*(公斤|kg|千克|kilogram)", "USD", "kg"),
        (r"\$\s*(\d+\.?\d*)\s*[/每]?\s*(lb|pound|磅)", "USD", "lb"),
        # THB patterns - only with explicit ฿ + unit
        (r"[฿₮]\s*(\d+\.?\d*)\s*[/每]?\s*(公斤|kg|千克)", "THB", "kg"),
        (r"(\d+\.?\d*)\s*[฿₮]\s*[/每]?\s*(公斤|kg|千克)", "THB", "kg"),
        # Generic CNY price declarations (must be preceded by 价格/售价/批发价/行情/报价)
        (r"(?:价格|售价|批发价|行情|报价)[：:]\s*(\d+\.?\d*)\s*[¥￥元]", "CNY", "unit"),
    ]

    for pattern, currency, unit in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for m in matches:
            try:
                price_val = float(m[0]) if isinstance(m, tuple) else float(m)
                if price_val > 0.5 and price_val < 2000:  # Reasonable fruit price range
                    results.append((price_val, unit, currency))
            except ValueError:
                continue

    return results


def normalise_to_kg(price, unit, currency, from_unit="unit"):
    """
    Normalise price to per-kg.
    unit: kg, jin, lb, or 'unit' (unknown, keep as-is)
    """
    if unit == "kg" or unit == "千克" or unit == "公斤":
        return price, unit, currency, 1.0
    elif unit == "jin" or unit == "斤":
        # 1 斤 = 0.5 kg
        return price / 0.5, "kg", currency, 0.5
    elif unit == "lb" or unit == "pound" or unit == "磅":
        # 1 lb = 0.4536 kg
        return price / 0.4536, "kg", currency, 0.4536
    elif unit == "unit":
        # Unknown unit, keep as-is
        return price, unit, currency, 1.0
    else:
        return price, "kg", currency, 1.0


def currency_symbol(code):
    return CURRENCY_SYMBOLS.get(code, code)


# ─── Main Functions ──────────────────────────────────────────────────

def collect_price(fruit_name, fruit_data):
    """
    Collect price for a specific fruit from its configured sources.
    Returns dict with price info or error message.
    """
    sources = fruit_data.get("sources", [])
    results = {
        "name": fruit_name,
        "en_name": fruit_data.get("en_name", ""),
        "prices": [],
        "errors": [],
        "sources_used": [],
        "search_hints": [],
        "status": "ok",
    }

    for src in sources:
        url = src.get("url", "")
        source_name = src.get("name", "")
        currency = src.get("currency", "CNY")

        if not url:
            results["errors"].append(f"{source_name}: 未配置URL")
            continue

        html = fetch_url(url)
        if not html:
            results["errors"].append(f"{source_name}: 无法访问")
            results["search_hints"].append(f"{fruit_name} {currency.lower()} price 2026")
            continue

        # Try to extract price
        extracted = extract_price_from_text(html, fruit_name)
        if extracted:
            for price_val, unit, found_currency in extracted:
                # Normalize unit to kg
                price_per_kg, norm_unit, norm_currency, _ = normalise_to_kg(
                    price_val, unit, found_currency
                )
                # Convert to RMB
                price_cny, rate = convert_price(price_per_kg, norm_currency, "CNY")

                results["prices"].append({
                    "source": source_name,
                    "original_price": price_val,
                    "original_currency": norm_currency,
                    "original_unit": unit,
                    "price_per_kg": round(price_per_kg, 2),
                    "currency_per_kg": norm_currency,
                    "price_rmb": round(price_cny, 2),
                    "exchange_rate": round(rate, 4),
                    "unit": "kg",
                    "fetched_at": utcnow().isoformat(),
                })
                results["sources_used"].append(source_name)
        else:
            # Try alternative source
            results["errors"].append(f"{source_name}: 无法从页面提取价格")
            results["search_hints"].append(f"{fruit_name} {currency.lower()} wholesale price 2026 {source_name}")

    # If no prices found, provide search hint for agent
    if not results["prices"]:
        results["status"] = "no_price"
        if not results["search_hints"]:
            # Season-based search
            month = utcnow().month
            results["search_hints"].append(
                f"{fruit_name} fruit wholesale price {month} 2026"
            )

    return results


def collect_all_prices(pool):
    """Collect prices for all fruits in the pool."""
    fruits = pool.get("fruits", {})
    all_results = {}
    all_status = "ok"

    for name, data in fruits.items():
        result = collect_price(name, data)
        all_results[name] = result
        if result["status"] != "ok":
            all_status = "partial"

    seasonal = pool.get("seasonal_fruits", [])
    # Get current season recommendations
    now = utcnow()
    current_month = now.month
    seasonal_out = []
    for sf in seasonal:
        if sf["name"] not in fruits:  # Only if not already tracked
            seasonal_out.append(sf)

    return {
        "collected_fruits": all_results,
        "seasonal_fruits": seasonal_out,
        "pool_fruit_count": len(fruits),
        "collected_at": utcnow().isoformat(),
        "pool_path": FRUIT_POOL_PATH,
        "status": all_status,
    }


def list_fruits(pool):
    """List all fruits in the pool with their sources."""
    fruits = pool.get("fruits", {})
    if not fruits:
        return {"message": "水果池为空，使用 --add 添加水果", "fruits": {}}
    
    result = {}
    for name, data in fruits.items():
        sources = []
        for s in data.get("sources", []):
            sources.append({
                "name": s.get("name", ""),
                "url": s.get("url", ""),
                "currency": s.get("currency", "CNY"),
            })
        result[name] = {
            "en_name": data.get("en_name", ""),
            "sources": sources,
            "last_price": data.get("last_price"),
            "last_updated": data.get("last_updated"),
        }
    return result


def add_fruit(pool, name, en_name="", sources=None):
    """Add a fruit to the pool."""
    name = name.strip()
    if not name:
        return {"error": "请输入水果名称"}

    fruits = pool.setdefault("fruits", {})
    if name in fruits:
        return {"error": f"{name} 已在水果池中", "action": "duplicate"}

    fruits[name] = {
        "en_name": en_name or "",
        "sources": sources or [],
        "last_price": None,
        "last_updated": None,
        "added_at": utcnow().isoformat(),
    }
    save_fruit_pool(pool)
    return {"message": f"✅ {name} 已加入水果池", "action": "added"}


def remove_fruit(pool, name):
    """Remove a fruit from the pool."""
    fruits = pool.get("fruits", {})
    if name not in fruits:
        return {"error": f"{name} 不在水果池中"}
    del fruits[name]
    save_fruit_pool(pool)
    return {"message": f"✅ {name} 已从水果池移除", "action": "removed"}


def add_source(pool, fruit_name, source_name, url, currency="CNY"):
    """Add a price source to an existing fruit."""
    fruits = pool.get("fruits", {})
    if fruit_name not in fruits:
        return {"error": f"{fruit_name} 不在水果池中，请先 --add"}
    
    sources = fruits[fruit_name].setdefault("sources", [])
    for s in sources:
        if s.get("name") == source_name:
            s["url"] = url
            s["currency"] = currency
            save_fruit_pool(pool)
            return {"message": f"✅ {fruit_name} 的报价来源已更新: {source_name}"}
    
    sources.append({
        "name": source_name,
        "url": url,
        "currency": currency,
    })
    save_fruit_pool(pool)
    return {"message": f"✅ {fruit_name} 已添加报价来源: {source_name}"}


def get_status(pool):
    """Check pool health."""
    fruits = pool.get("fruits", {})
    total = len(fruits)
    with_price = sum(1 for f in fruits.values() if f.get("last_price"))
    without_sources = sum(1 for f in fruits.values() if not f.get("sources"))
    
    return {
        "total_fruits": total,
        "with_price_data": with_price,
        "without_price_data": total - with_price,
        "without_sources": without_sources,
        "seasonal_recommendations": len(pool.get("seasonal_fruits", [])),
        "pool_path": FRUIT_POOL_PATH,
    }


def get_seasonal_recommendations(pool, max_items=5):
    """Get seasonal fruit recommendations (not in pool)."""
    tracked = set(pool.get("fruits", {}).keys())
    # Simple season detection by month
    now = utcnow()
    month = now.month
    season_map = {
        (5, 6, 7): ["荔枝", "樱桃", "杨梅", "榴莲", "芒果"],
        (6, 7, 8): ["榴莲", "山竹", "荔枝", "水蜜桃", "芒果"],
        (7, 8, 9): ["葡萄", "水蜜桃", "火龙果", "石榴"],
        (9, 10, 11): ["猕猴桃", "石榴", "柿子", "柚子"],
        (12, 1, 2): ["草莓", "车厘子", "砂糖橘", "脐橙"],
        (3, 4, 5): ["菠萝", "草莓", "芒果", "枇杷"],
    }
    
    all_seasonal = pool.get("seasonal_fruits", [])
    current_season = []
    for sf in all_seasonal:
        if sf["name"] not in tracked:
            current_season.append(sf)
    
    # If no season data in pool, use month-based suggestions
    if not current_season:
        for months, names in season_map.items():
            if month in months:
                for n in names:
                    if n not in tracked and n not in [s["name"] for s in current_season]:
                        current_season.append({"name": n, "en_name": ""})
    return current_season[:max_items]


# ─── CLI ──────────────────────────────────────────────────────────────

def main():
    pool = load_fruit_pool()
    
    if len(sys.argv) == 1:
        # Default: collect all prices
        result = collect_all_prices(pool)
        # Output JSON for agent to process
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    cmd = sys.argv[1]

    if cmd == "--list":
        result = list_fruits(pool)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "--add":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "用法: --add <水果名> [--en <英文名>]"}, ensure_ascii=False))
            return
        name = sys.argv[2]
        en_name = ""
        if "--en" in sys.argv:
            idx = sys.argv.index("--en")
            if idx + 1 < len(sys.argv):
                en_name = sys.argv[idx + 1]
        result = add_fruit(pool, name, en_name)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "--add-source":
        # --add-source <fruit> <name> <url> [currency]
        if len(sys.argv) < 5:
            print(json.dumps({"error": "用法: --add-source <水果名> <来源名> <URL> [currency]"}, ensure_ascii=False))
            return
        fruit_name = sys.argv[2]
        source_name = sys.argv[3]
        url = sys.argv[4]
        currency = sys.argv[5] if len(sys.argv) > 5 else "CNY"
        result = add_source(pool, fruit_name, source_name, url, currency)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "--remove":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "用法: --remove <水果名>"}, ensure_ascii=False))
            return
        result = remove_fruit(pool, sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "--status":
        result = get_status(pool)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "--recommend":
        result = get_seasonal_recommendations(pool)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "--collect":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "用法: --collect <水果名>"}, ensure_ascii=False))
            return
        name = sys.argv[2]
        fruits = pool.get("fruits", {})
        if name not in fruits:
            print(json.dumps({"error": f"{name} 不在水果池中"}, ensure_ascii=False))
            return
        result = collect_price(name, fruits[name])
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "--pool-path":
        print(FRUIT_POOL_PATH)

    elif cmd == "--refresh-sources":
        if len(sys.argv) < 3:
            print(json.dumps({"error": "用法: --refresh-sources <水果名>"}, ensure_ascii=False))
            return
        name = sys.argv[2]
        fruits = pool.get("fruits", {})
        if name not in fruits:
            print(json.dumps({"error": f"{name} 不在水果池中"}, ensure_ascii=False))
            return
        # Output search hints for agent to find new sources
        hints = fruits[name].get("categories", "")
        month = utcnow().month
        print(json.dumps({
            "fruit": name,
            "search_hints": [
                f"{name} wholesale price 2026",
                f"{name} market price per kg {month} 2026",
                f"{name} agricultural wholesale market quote",
            ],
            "message": f"请搜索以上关键词，找到{name}的价格来源后使用 --add-source 添加"
        }, ensure_ascii=False, indent=2))

    else:
        print(json.dumps({"error": f"未知命令: {cmd}"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
