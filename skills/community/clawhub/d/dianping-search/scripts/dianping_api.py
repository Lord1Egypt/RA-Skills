#!/usr/bin/env python3
"""Dianping HTTP API — zero-dependency, uses curl for HTTP.

Usage:
    python3 dianping_api.py search <keyword> [--city_id N]
    python3 dianping_api.py shop <shop_id>
    python3 dianping_api.py deals <shop_id>

All output is JSON to stdout for easy AI consumption.
No pip dependencies — only curl (pre-installed on macOS/Linux).
"""

import sys, json, re, subprocess
from pathlib import Path
from urllib.parse import quote

COOKIES_FILE = Path.home() / ".dianping" / "cookies.json"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"


def _cookies():
    if not COOKIES_FILE.exists():
        return {}
    raw = json.loads(COOKIES_FILE.read_text())
    return {c["name"]: c["value"] for c in raw} if isinstance(raw, list) else raw


def _get(url):
    """HTTP GET via curl. Returns (html, None) or (None, error_dict)."""
    ck = _cookies()
    cookie_str = "; ".join(f"{k}={v}" for k, v in ck.items()) if ck else ""
    cmd = [
        "curl", "-s", "-L", "-w", "\n%{http_code}\n%{url_effective}",
        "-b", cookie_str,
        "-H", f"User-Agent: {UA}",
        "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "-H", "Accept-Language: zh-CN,zh;q=0.9",
        "-H", "Referer: https://www.dianping.com/",
        "--max-time", "15",
        url,
    ]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        lines = p.stdout.rsplit("\n", 2)
        if len(lines) >= 3:
            body, status, final_url = lines[-3], lines[-2].strip(), lines[-1].strip()
        else:
            body, status, final_url = p.stdout, "0", url
        if status != "200" or "login" in final_url or "verify" in final_url:
            return None, {"error": "请求失败或需要重新登录", "status": int(status or 0), "url": final_url}
        return body, None
    except Exception as e:
        return None, {"error": f"curl 执行失败: {e}"}


def _re1(pattern, text, default=""):
    m = re.search(pattern, text)
    return m.group(1) if m else default


# ─── API: Search ───────────────────────────────────────────────

def api_search(keyword, city_id=1):
    """Search shops near a keyword/location. city_id: 1=上海, 2=北京, etc."""
    url = "https://www.dianping.com/search/keyword/%d/0_%s" % (city_id, quote(keyword))
    html, err = _get(url)
    if err:
        return err

    # Extract shop entries: pair each <a href="/shop/ID"> with the next <h4>name</h4>
    entries = re.findall(
        r'href="(?:https?://www\.dianping\.com)?/shop/(\w+)"[^>]*>[\s\S]*?<h4>([\s\S]*?)</h4>',
        html
    )
    stars = re.findall(r'star_(\d+)\s+star_sml', html)
    reviews = re.findall(r'(\d+)\s*条评价', html)
    prices = re.findall(r'人均\s*[￥¥]?\s*(\d+)', html)

    shops = []
    seen = set()
    idx = 0
    for shop_id, raw_name in entries:
        name = re.sub(r'<[^>]+>', '', raw_name).strip()
        if not name or shop_id in seen:
            continue
        seen.add(shop_id)
        shop = {"shop_id": shop_id, "name": name}
        if idx < len(stars):
            shop["rating"] = round(int(stars[idx]) / 10, 1)
        if idx < len(reviews):
            shop["review_count"] = reviews[idx]
        if idx < len(prices):
            shop["avg_price"] = int(prices[idx])
        shops.append(shop)
        idx += 1

    return {"keyword": keyword, "city_id": city_id, "count": len(shops), "shops": shops}


# ─── API: Shop Detail ─────────────────────────────────────────

def api_shop(shop_id):
    """Get full shop details including scores, dishes, address, transport."""
    url = "https://www.dianping.com/shop/" + shop_id
    html, err = _get(url)
    if err:
        return err

    def j(key):
        return _re1(r'"' + key + r'":"?(.*?)"?[,}\]]', html)

    dishes = re.findall(r'"dishName":"(.*?)"', html)

    result = {
        "shop_id": shop_id,
        "name": j("shopName"),
        "score_text": j("scoreText"),
        "avg_price": j("avgPrice"),
        "review_count": j("voteTotal"),
        "category": j("categoryName"),
        "region": j("regionName"),
        "address": j("address"),
        "route": j("route"),
        "phone": j("phoneNo"),
        "recommended_dishes": dishes[:10],
    }

    # Parse score_text into structured scores
    score_text = result["score_text"]
    if score_text:
        taste = _re1(r'口味[：:]?([\d.]+)', score_text)
        env = _re1(r'环境[：:]?([\d.]+)', score_text)
        svc = _re1(r'服务[：:]?([\d.]+)', score_text)
        if taste:
            result["scores"] = {"taste": float(taste), "environment": float(env), "service": float(svc)}

    return result


# ─── API: Deals / Promotions ──────────────────────────────────

def api_deals(shop_id):
    """Get deals, coupons, and set menus for a shop."""
    url = "https://www.dianping.com/shop/" + shop_id
    html, err = _get(url)
    if err:
        return err

    name = _re1(r'"shopName":"(.*?)"', html)
    titles = re.findall(r'"(?:dealTitle|title|dealName|groupName|promoTitle)":"(.*?)"', html)
    sale_prices = re.findall(r'"(?:dealPrice|price|salePrice)":\s*"?(\d+\.?\d*)"?', html)
    orig_prices = re.findall(r'"(?:dealValue|value|originalPrice|marketPrice)":\s*"?(\d+\.?\d*)"?', html)

    deals = []
    for i, t in enumerate(titles):
        if len(t) < 2 or t in ("null", "undefined", "{\\"):
            continue
        deal = {"title": t}
        if i < len(sale_prices):
            deal["price"] = float(sale_prices[i])
        if i < len(orig_prices):
            deal["original_price"] = float(orig_prices[i])
        deals.append(deal)

    # Key services
    svc_block = _re1(r'"keyServices":\s*\[(.*?)\]', html)
    services = re.findall(r'"name":"(.*?)"', svc_block) if svc_block else []

    # Shop tags
    tag_block = _re1(r'"shopTag":\s*\[(.*?)\]', html)
    tags = re.findall(r'"tagName":"(.*?)"', tag_block) if tag_block else []

    return {"shop_id": shop_id, "name": name, "deals": deals, "services": services, "tags": tags}


# ─── CLI ──────────────────────────────────────────────────────

def _print_json(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("用法:")
        print("  python3 dianping_api.py search <keyword> [--city_id N]")
        print("  python3 dianping_api.py shop <shop_id>")
        print("  python3 dianping_api.py deals <shop_id>")
        sys.exit(0)

    cmd = args[0]
    if cmd == "search" and len(args) >= 2:
        city = 1
        if "--city_id" in args:
            ci = args.index("--city_id")
            city = int(args[ci + 1])
        _print_json(api_search(args[1], city))
    elif cmd == "shop" and len(args) >= 2:
        _print_json(api_shop(args[1]))
    elif cmd == "deals" and len(args) >= 2:
        _print_json(api_deals(args[1]))
    else:
        print(json.dumps({"error": "未知命令: " + cmd}))

