# -*- coding: utf-8 -*-
"""爬虫脚本：当用户提供的信息缺失或不足时，从互联网爬取公开教学资料辅助设计。

实现仅使用 Python 标准库（urllib + html.parser），不依赖第三方包；
优先使用 Bing，失败或结果为空时回退到 DuckDuckGo。

用法：
    python crawl_info.py "查询词1" ["查询词2" ...] [--top 5] [--json]

示例：
    python crawl_info.py "数据结构 树与二叉树 课程大纲"
    python crawl_info.py "高等数学 导数 教学内容" --top 8 --json

输出：默认打印结构化文本（标题/链接/摘要），--json 时输出 JSON，供 AI 读取后补充设计内容。
"""
import argparse
import html
import json
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser

UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9",
}


def fetch(url, timeout=15):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")


# ---------- Bing 解析 ----------
class BingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self.cur = None
        self.in_algo = False
        self.in_h2 = False
        self.in_p = False
        self.buf = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        cls = attrs.get("class", "") or ""
        if tag == "li" and "b_algo" in cls.split():
            self.in_algo = True
            self.cur = {"title": "", "url": "", "snippet": ""}
        if self.in_algo and tag == "h2":
            self.in_h2 = True
            self.buf = []
        if self.in_algo and tag == "a" and self.in_h2 and self.cur and not self.cur["url"]:
            href = attrs.get("href", "")
            if href.startswith("http"):
                self.cur["url"] = href
        if self.in_algo and tag == "p":
            self.in_p = True
            self.buf = []

    def handle_data(self, data):
        if self.cur and (self.in_h2 or self.in_p):
            self.buf.append(data)

    def handle_endtag(self, tag):
        if tag == "h2" and self.in_h2:
            self.in_h2 = False
            if self.cur:
                self.cur["title"] = "".join(self.buf).strip()
            self.buf = []
        if tag == "p" and self.in_p:
            self.in_p = False
            if self.cur:
                self.cur["snippet"] = " ".join("".join(self.buf).split()).strip()
            self.buf = []
        if tag == "li" and self.in_algo:
            self.in_algo = False
            if self.cur and (self.cur["title"] or self.cur["snippet"]):
                self.results.append(self.cur)
            self.cur = None


# ---------- DuckDuckGo 解析（正则提取） ----------
def search_ddg(query, top):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    page = fetch(url)
    # DDG 页面结构简单，直接用正则提取
    results = []
    for m in re.finditer(
            r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>'
            r'(?s).*?(?:<a[^>]+class="result__snippet"[^>]*>(.*?)</a>)?', page):
        href, title, snippet = m.group(1), m.group(2), m.group(3) or ""
        title = html.unescape(re.sub(r"<[^>]+>", "", title)).strip()
        snippet = html.unescape(re.sub(r"<[^>]+>", "", snippet)).strip()
        if title:
            results.append({"title": title, "url": href, "snippet": snippet})
        if len(results) >= top:
            break
    return results


def search(query, top):
    try:
        page = fetch("https://www.bing.com/search?q=" + urllib.parse.quote(query) + "&setlang=zh-CN")
        p = BingParser()
        p.feed(page)
        if p.results:
            return p.results[:top]
    except Exception:
        pass
    # 回退 DuckDuckGo
    try:
        return search_ddg(query, top)
    except Exception:
        return []


def main():
    ap = argparse.ArgumentParser(description="爬取公开教学资料辅助混合式教学设计")
    ap.add_argument("queries", nargs="+", help="一个或多个查询词")
    ap.add_argument("--top", type=int, default=5, help="每个查询返回结果数（默认 5）")
    ap.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    args = ap.parse_args()

    all_results = {}
    errors = []
    for q in args.queries:
        try:
            all_results[q] = search(q, args.top)
        except Exception as e:
            errors.append("%s: %s" % (q, e))
            all_results[q] = []

    if args.json:
        print(json.dumps(all_results, ensure_ascii=False, indent=2))
    else:
        for q, res in all_results.items():
            print("=" * 60)
            print("查询：%s" % q)
            if not res:
                print("（未获取到结果，可尝试更换关键词或由 AI 依据通用知识撰写示例内容）")
            for i, r in enumerate(res, 1):
                print("  [%d] %s" % (i, r["title"]))
                print("      链接：%s" % r["url"])
                sn = r["snippet"][:150]
                if sn:
                    print("      摘要：%s" % sn)
        if errors:
            print("\n（部分查询出错：%s）" % "；".join(errors))

    return 0


if __name__ == "__main__":
    sys.exit(main())
