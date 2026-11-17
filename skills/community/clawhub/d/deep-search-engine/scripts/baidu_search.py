#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""百度搜索抓取 + 中转链接解析。

中文站点核验必备通道（Hard Rule 1）：Google News/WebSearch 对 chinadaily 等站存在结构性盲区，
百度一搜即得。百度结果链接是中转链接（baidu.com/link?url=...），--resolve 解析为真实直链。

用法：
  python baidu_search.py --query "中国日报 企业搜索 上下文基础设施"
  python baidu_search.py --query "..." --resolve --top 5
  python baidu_search.py --query "..." --out result.json

输出：JSON {query, count, items: [{rank, title, baidu_link, real_url?}]}

注意：
- 解析中转链接每条一次请求，较慢；先看标题筛掉无关项再 --resolve
- 只解析首页结果（约 10 条）；需要翻页时换更具体查询词，不模拟翻页
- 查询词组合建议：媒体名 + 主题关键词；或 媒体名 + 独特长句片段
"""
import argparse
import json
import re
import sys
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def fetch(url: str, timeout: int = 25):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "zh-CN,zh;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.geturl(), r.read().decode("utf-8", "ignore")


def search(query: str) -> list[dict]:
    url = "https://www.baidu.com/s?wd=" + urllib.parse.quote(query)
    _, html = fetch(url)
    items = []
    # 结果标题块：<h3 ...><a href="http(s)://www.baidu.com/link?url=...">标题（可能含<em>高亮）</a></h3>
    pat = re.compile(
        r'<h3[^>]*>\s*<a[^>]+href="(https?://www\.baidu\.com/link\?url=[^"]+)"[^>]*>(.*?)</a>',
        re.S)
    for m in pat.finditer(html):
        title = re.sub(r"<[^>]+>", "", m.group(2))
        title = re.sub(r"\s+", " ", title).strip()
        if title and not any(i["title"] == title for i in items):
            items.append({"title": title, "baidu_link": m.group(1)})
    return items


def resolve(link: str) -> str | None:
    """解析百度中转链接为真实 URL（跟随 302 取最终地址）。"""
    try:
        final, _ = fetch(link, timeout=20)
        return final if "baidu.com/link" not in final else None
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Baidu search + link resolution")
    ap.add_argument("--query", required=True)
    ap.add_argument("--resolve", action="store_true", help="解析中转链接为真实直链（较慢）")
    ap.add_argument("--top", type=int, default=10, help="最多处理条数（默认 10）")
    ap.add_argument("--out", help="结果另存 JSON 文件路径")
    a = ap.parse_args()

    try:
        raw = search(a.query)
    except Exception as e:
        print(json.dumps({"query": a.query, "error": f"{type(e).__name__}: {e}",
                          "hint": "重试一次；连续失败换 curl 抓百度结果页交叉验证"},
                         ensure_ascii=False))
        return 1

    if not raw:
        print(json.dumps({"query": a.query, "count": 0, "items": [],
                          "hint": "零结果不是结论：换查询词组合（媒体名+主题片段/独特长句）重试 2 次"},
                         ensure_ascii=False))
        return 0

    items = []
    for i, it in enumerate(raw[: a.top], 1):
        entry = {"rank": i, "title": it["title"], "baidu_link": it["baidu_link"]}
        if a.resolve:
            entry["real_url"] = resolve(it["baidu_link"])
        items.append(entry)

    result = {"query": a.query, "count": len(items), "resolved": bool(a.resolve), "items": items}
    out = json.dumps(result, ensure_ascii=False, indent=1)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(out)
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
