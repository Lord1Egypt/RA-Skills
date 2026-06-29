#!/usr/bin/env python3
"""
EC Price Monitor Lite - 免费版
支持：淘宝、拼多多 手动价格搜索
"""
import json, os, sys, re, urllib.request, urllib.parse
from datetime import datetime

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "references", "config.yaml")

def load_config():
    import yaml
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)

def search(keyword, platform):
    headers = {"User-Agent": "Mozilla/5.0"}
    urls = {
        "taobao": f"https://s.taobao.com/search?q={urllib.parse.quote(keyword)}",
        "pdd": f"https://mobile.yangkeduo.com/search_result.html?search_key={urllib.parse.quote(keyword)}",
    }
    url = urls.get(platform)
    if not url: return []
    try:
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8", errors="ignore")
        prices = []
        for pat in [r'"price"[:\s]*"?(\d+[\.\d]*)', r'"view_price"[:\s]*"?(\d+[\.\d]*)', r'¥(\d+[\.\d]*)']:
            for m in re.findall(pat, html):
                try:
                    v = float(m)
                    if 1 < v < 999999: prices.append(v)
                except: pass
            if prices: break
        return [{"platform": platform, "price": min(prices)}] if prices else []
    except:
        return [{"platform": platform, "price": None, "error": "获取失败"}]

def main():
    config = load_config()
    keywords = [{"keyword": " ".join(sys.argv[1:])}] if len(sys.argv) > 1 else config.get("items", [])
    if not keywords:
        print("❌ 未配置商品，请在 config.yaml 的 items 中添加")
        return 1

    for item in keywords:
        kw = item["keyword"]
        print(f"📍 {kw}")
        print(f"━━ {'LITE版 · 仅限淘宝/拼多多':>25}")
        for p in ["taobao", "pdd"]:
            r = search(kw, p)
            pname = {"taobao":"淘宝","pdd":"拼多多"}.get(p, p)
            if r and r[0].get("price"):
                print(f"  {pname}: ¥{r[0]['price']:,.0f}")
            else:
                print(f"  {pname}: 获取失败")
        print()
    print("💡 升级 Pro 版可获得京东比价 + 定时监控 + 推送提醒")
    return 0

if __name__ == "__main__":
    sys.exit(main())
