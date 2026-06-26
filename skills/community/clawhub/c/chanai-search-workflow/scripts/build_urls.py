#!/usr/bin/env python3
import json
import sys
import urllib.parse


def enc(s: str) -> str:
    return urllib.parse.quote_plus(s)


def build_dynamic_urls(query: str, route: str, subtype: str | None):
    q = enc(query)
    urls = []
    if subtype == "flight":
        urls.extend([
            {"name": "Ctrip flight search", "url": f"https://flights.ctrip.com/online/list/oneway-{q}"},
            {"name": "Trip flight search", "url": f"https://www.trip.com/flights/showfarefirst?searchType=OW&dcity={q}"},
            {"name": "Baidu", "url": f"https://www.baidu.com/s?wd={q}"},
            {"name": "Bing CN", "url": f"https://cn.bing.com/search?q={q}&ensearch=0"},
        ])
    elif subtype == "hotel":
        urls.extend([
            {"name": "Ctrip hotel search", "url": f"https://hotels.ctrip.com/hotels/list?keyword={q}"},
            {"name": "Trip hotel search", "url": f"https://www.trip.com/hotels/list?keyword={q}"},
            {"name": "Baidu", "url": f"https://www.baidu.com/s?wd={q}"},
            {"name": "Bing CN", "url": f"https://cn.bing.com/search?q={q}&ensearch=0"},
        ])
    elif subtype == "product-price":
        urls.extend([
            {"name": "JD search", "url": f"https://search.jd.com/Search?keyword={q}"},
            {"name": "Tmall search", "url": f"https://list.tmall.com/search_product.htm?q={q}"},
            {"name": "Taobao search", "url": f"https://s.taobao.com/search?q={q}"},
            {"name": "Baidu", "url": f"https://www.baidu.com/s?wd={q}"},
        ])
    elif subtype == "ticketing":
        urls.extend([
            {"name": "Damai search", "url": f"https://search.damai.cn/search.htm?keyword={q}"},
            {"name": "Baidu", "url": f"https://www.baidu.com/s?wd={q}"},
            {"name": "Bing CN", "url": f"https://cn.bing.com/search?q={q}&ensearch=0"},
        ])
    elif subtype == "finance-news":
        urls.extend([
            {"name": "WolframAlpha", "url": f"https://www.wolframalpha.com/input?i={q}"},
            {"name": "Google News", "url": f"https://www.google.com/search?q={q}&tbm=nws"},
            {"name": "Baidu News style", "url": f"https://www.baidu.com/s?wd={q}"},
        ])
    else:
        if route in ("domestic-first", "mixed"):
            urls.extend([
                {"name": "Baidu", "url": f"https://www.baidu.com/s?wd={q}"},
                {"name": "Bing CN", "url": f"https://cn.bing.com/search?q={q}&ensearch=0"},
            ])
        if route in ("global-first", "mixed"):
            urls.extend([
                {"name": "Google", "url": f"https://www.google.com/search?q={q}"},
                {"name": "DuckDuckGo", "url": f"https://duckduckgo.com/html/?q={q}"},
            ])
    return urls


def build(query: str, route: str, intent: str, subtype: str | None = None):
    q = enc(query)
    urls = []

    # Dynamic queries should prioritize pages humans would actually use for final decisions.
    if intent == "dynamic":
        return build_dynamic_urls(query, route, subtype)

    if route in ("domestic-first", "mixed"):
        urls.extend([
            {"name": "Baidu", "url": f"https://www.baidu.com/s?wd={q}"},
            {"name": "Bing CN", "url": f"https://cn.bing.com/search?q={q}&ensearch=0"},
        ])
        if intent == "experience":
            urls.extend([
                {"name": "Zhihu", "url": f"https://www.zhihu.com/search?type=content&q={q}"},
                {"name": "Bilibili", "url": f"https://search.bilibili.com/all?keyword={q}"},
            ])
    if route in ("global-first", "mixed"):
        urls.extend([
            {"name": "Google", "url": f"https://www.google.com/search?q={q}"},
            {"name": "DuckDuckGo", "url": f"https://duckduckgo.com/html/?q={q}"},
            {"name": "Brave", "url": f"https://search.brave.com/search?q={q}"},
        ])
    if intent == "document":
        urls.extend([
            {"name": "Google filetype PDF", "url": f"https://www.google.com/search?q={q}+filetype:pdf"},
            {"name": "Google Scholar", "url": f"https://scholar.google.com/scholar?q={q}"},
        ])
    return urls


def main():
    if len(sys.argv) < 4:
        print("Usage: build_urls.py <route> <intent> <query>", file=sys.stderr)
        sys.exit(1)
    route = sys.argv[1]
    intent = sys.argv[2]
    query = " ".join(sys.argv[3:])
    print(json.dumps({"query": query, "route": route, "intent": intent, "urls": build(query, route, intent)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
