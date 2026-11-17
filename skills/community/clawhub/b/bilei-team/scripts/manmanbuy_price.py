#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
慢慢买比价查询（免登录搜索层）

用法：
    /usr/bin/python3 manmanbuy_price.py "安克智显充140W" ["图拉斯小冰块" ...]
    /usr/bin/python3 manmanbuy_price.py --json "安克智显充140W"

背景与坑（v1.0 / 2026-11-04 实测）：
  * 站点按 GBK 解析 key 参数。传 UTF-8 会被当 GBK 解读，返回乱码页
    （标题变成「瀹夊厠鏅烘樉鍏?40W」），看起来像站点挂了，其实是编码错。
  * 搜索层免登录完全可用；失效的只是历史曲线 API（history.aspx 等）。
  * 页面输出是 UTF-8，请求参数才需要 GBK。
  * python3 的 urllib 对该站 SSL 偶发 SSLEOFError，故用 curl 取页面更稳。

返回内容：爆料列表（标题 / 爆料价 / 商城 / 日期 / 价格标签 / 条目链接）
价格标签「历史最低 / 60天新低 / 低于618」即是结论，无需自行推算。

能力边界：单品完整历史曲线需 App 或登录态；拼多多覆盖弱。
"""
import json
import re
import subprocess
import sys
import urllib.parse
from html import unescape

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

NON_PRICE_TAGS = {"闭眼买"}  # 运营推荐位，不是价格标签


def build_url(keyword: str) -> str:
    q = urllib.parse.quote(keyword.encode("gbk"))
    # ss.manmanbuy.com?key= 会 302 到下面这个正式地址，直接用正式地址更稳
    return f"https://s.manmanbuy.com/pc/search/result?keyword={q}&c=discount"


def fetch(url: str) -> str:
    """用 curl 取页面，避开 python urllib 的 SSL 握手问题。"""
    proc = subprocess.run(
        ["curl", "-s", "--compressed", "-A", UA,
         "-H", "Accept-Language: zh-CN,zh;q=0.9",
         "-m", "30", "-L", url],
        capture_output=True,
    )
    return proc.stdout.decode("utf-8", "ignore")


def _clean(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


def parse(html: str) -> list:
    """解析爆料条目。标题在 <a title> 属性里，不在标签文本里。"""
    blocks = re.split(r"(?=DiscountItemPC_discountItem__)", html)
    rows = []
    for b in blocks:
        t = re.search(r'<a target="_blank" title="([^"]{5,300})"', b)
        if not t:
            continue
        sub = re.search(r"itemSubTitle[^>]*>\s*<a[^>]*>(.*?)</a>", b, re.S)
        if not sub:
            sub = re.search(r"itemSubTitle[^>]*>(.*?)</div>", b, re.S)
        tags = [_clean(x) for x in re.findall(r"itemTag__[^>]*>(.*?)</div>", b, re.S)]
        tags = [x for x in tags if x]
        mall = re.search(r"itemMall__[^>]*>(.*?)</span>", b, re.S)
        tm = re.search(r"itemTime__[^>]*>(.*?)</span>", b, re.S)
        link = re.search(r'href="(https://cu\.manmanbuy\.com/discuxiao_\d+\.aspx)"', b)
        rows.append({
            "title": unescape(t.group(1)).strip(),
            "price_text": _clean(sub.group(1)) if sub else "",
            "price_tags": [x for x in tags if x not in NON_PRICE_TAGS],
            "mall": mall.group(1).strip() if mall else "",
            "date": tm.group(1).strip() if tm else "",
            "link": link.group(1) if link else "",
        })
    return rows


def filter_relevant(rows: list, keyword: str) -> list:
    """按关键词切片过滤，避免「搜图拉斯返回华为 Vision 电视」这类噪声。"""
    core = re.sub(r"[^\u4e00-\u9fa5A-Za-z0-9]", "", keyword)
    names = [core]
    # 中文品牌/系列名做前缀切片，如「安克智显充140W」→「安克」「智显充」
    for seg in re.findall(r"[\u4e00-\u9fa5]{2,}", core):
        names.append(seg)
    out = []
    for r in rows:
        title = r["title"]
        if any(n and n in title for n in names):
            out.append(r)
    return out


def has_price_history(rows: list) -> bool:
    return any("历史最低" in r["price_tags"] or "新低" in "".join(r["price_tags"])
               for r in rows)


def render(keyword: str, rows: list) -> str:
    lines = []
    lines.append("=" * 78)
    lines.append(f"关键词：{keyword}")
    if not rows:
        lines.append("  ⚠ 无相关爆料记录。")
        lines.append("  结论：该型号在比价/爆料社区无踪迹 —— 通常意味着上市太新、")
        lines.append("        销量太小、或非主流渠道货。不是「价格正常」，是「没有参照」。")
        return "\n".join(lines)
    lines.append(f"相关条目：{len(rows)} 条")
    lines.append("-" * 78)
    for r in sorted(rows, key=lambda x: x["date"], reverse=True):
        tags = "/".join(r["price_tags"]) or "—"
        lines.append(f"[{r['date']:<11}] {r['mall']:<8} {tags}")
        lines.append(f"    {r['title'][:70]}")
        if r["price_text"]:
            lines.append(f"    价格：{r['price_text'][:70]}")
        if r["link"]:
            lines.append(f"    {r['link']}")
    if not has_price_history(rows):
        lines.append("-" * 78)
        lines.append("  ⚠ 本次结果中无「历史最低」标签 —— 只能报「已知低点」，")
        lines.append("    不得写成「历史最低」。")
    return "\n".join(lines)


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--json"]
    as_json = "--json" in sys.argv
    if not args:
        print(__doc__)
        return 1

    result = {}
    for kw in args:
        rows = filter_relevant(parse(fetch(build_url(kw))), kw)
        result[kw] = rows
        if not as_json:
            print(render(kw, rows))

    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
