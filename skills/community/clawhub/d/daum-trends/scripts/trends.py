#!/usr/bin/env python3
"""Daum 실시간 트렌드 TOP10 브리핑 — garibong-labs 리라이트."""
import argparse
import json
import re
import sys
from html import unescape, escape
from urllib.parse import quote
from urllib.request import Request, urlopen

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
DAUM_HOME = "https://www.daum.net/"
SEARCH_URL = "https://search.daum.net/search?w=tot&DA=RT1&rtmaxcoll=AIO,NNS,DNS&q="


def fetch(url: str, timeout: int = 10) -> str:
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=timeout) as res:
        return res.read().decode("utf-8", errors="replace")


def extract_trends(html: str) -> tuple[list[dict], str]:
    """Parse REALTIME_TREND_TOP from Daum homepage HTML."""
    marker = '"uiType":"REALTIME_TREND_TOP"'
    idx = html.find(marker)
    if idx < 0:
        raise ValueError("REALTIME_TREND_TOP not found in HTML")

    updated_at = ""
    ua_match = re.search(r'"updatedAt"\s*:\s*"([^"]+)"', html[idx:])
    if ua_match:
        updated_at = ua_match.group(1)

    kw_start = html.find('"keywords"', idx)
    if kw_start < 0:
        raise ValueError("keywords not found")

    bracket = html.find("[", kw_start)
    if bracket < 0:
        raise ValueError("keywords array not found")

    depth, end = 0, bracket
    for i in range(bracket, min(bracket + 50000, len(html))):
        if html[i] == "[":
            depth += 1
        elif html[i] == "]":
            depth -= 1
            if depth == 0:
                end = i + 1
                break

    keywords = json.loads(html[bracket:end])
    return keywords[:10], updated_at


SKIP_WORDS = {"검색", "javascript", "function", "var ", "재생시간", "닫기",
              "배송비", "원  ", "11번가", "쿠팡", "투데이", "beta", "안내"}


def extract_title(html: str) -> str:
    """Extract first news-like title from Daum search result page."""
    all_a = re.findall(r"<a[^>]*>(.*?)</a>", html[:200000], re.DOTALL)
    for raw in all_a:
        clean = re.sub(r"<[^>]+>", "", raw).strip()
        text = unescape(clean)
        if len(text) < 15 or len(text) > 120:
            continue
        if any(s in text for s in SKIP_WORDS):
            continue
        return text[:80]
    return ""


def search_url(keyword: str) -> str:
    return SEARCH_URL + quote(keyword)


def fmt_line_plain(rank, kw, title, url):
    short = (title[:45] + "…") if len(title) > 48 else title
    if short:
        return f"{rank}. {kw} — {short}"
    return f"{rank}. {kw}"


def fmt_line_markdown(rank, kw, title, url):
    short = (title[:45] + "…") if len(title) > 48 else title
    if short:
        return f"{rank}. [{kw}]({url}) — {short}"
    return f"{rank}. [{kw}]({url})"


def fmt_line_html(rank, kw, title, url):
    short = (title[:45] + "…") if len(title) > 48 else title
    kw_esc = escape(kw)
    short_esc = escape(short) if short else ""
    if short_esc:
        return f'{rank}. <a href="{url}">{kw_esc}</a> — {short_esc}'
    return f'{rank}. <a href="{url}">{kw_esc}</a>'


FORMATTERS = {
    "plain": fmt_line_plain,
    "markdown": fmt_line_markdown,
    "html": fmt_line_html,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--format", choices=["plain", "markdown", "html"], default="markdown")
    args = ap.parse_args()

    fmt = FORMATTERS[args.format]

    try:
        home_html = fetch(DAUM_HOME)
        keywords, updated_at = extract_trends(home_html)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    if not keywords:
        print("트렌드 데이터 없음", file=sys.stderr)
        sys.exit(1)

    items = []
    for i, kw in enumerate(keywords):
        word = kw.get("keyword", kw.get("text", f"#{i+1}"))
        url = search_url(word)
        title = ""
        try:
            search_html = fetch(url)
            title = extract_title(search_html)
        except Exception:
            pass
        items.append({"rank": i + 1, "keyword": word, "title": title, "url": url})

    ts_short = updated_at
    ts_match = re.match(r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})", updated_at)
    if ts_match:
        ts_short = f"{ts_match.group(2)}/{ts_match.group(3)} {ts_match.group(4)}:{ts_match.group(5)}"

    lines = []
    lines.append(f"📊 Daum 실시간 트렌드 TOP10 ({ts_short})")
    lines.append("")
    for it in items:
        lines.append(fmt(it["rank"], it["keyword"], it["title"], it["url"]))

    print("\n".join(lines))


if __name__ == "__main__":
    main()
