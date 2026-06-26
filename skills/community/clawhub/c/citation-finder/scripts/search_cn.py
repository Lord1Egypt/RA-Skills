"""
search_cn.py — Search Chinese academic databases
Sources: Baidu Scholar (web scrape) + CNKI (web scrape fallback)
"""

import re
import requests
from urllib.parse import quote
from rapidfuzz import fuzz
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def search_baidu_scholar(query: str, limit: int = 5) -> list[dict]:
    """Scrape Baidu Scholar for Chinese/English paper results."""
    url = f"https://xueshu.baidu.com/s?wd={quote(query)}&rsv_bp=0&tn=SE_baiduxueshu_c1gjeupa&ie=utf-8&rsv_spt=3&rsv_sug3=2&bs={quote(query)}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")

        results = []
        items = soup.select(".sc_content") or soup.select(".result")

        for item in items[:limit]:
            # Title
            title_tag = item.select_one(".sc_title a") or item.select_one("h3 a")
            title = title_tag.get_text(strip=True) if title_tag else ""
            link = title_tag.get("href", "") if title_tag else ""

            # Authors
            author_tag = item.select_one(".sc_info span") or item.select_one(".author")
            authors_raw = author_tag.get_text(strip=True) if author_tag else ""
            authors = _parse_cn_authors(authors_raw)

            # Year and journal
            info_tag = item.select_one(".sc_info") or item.select_one(".source")
            info_text = info_tag.get_text(strip=True) if info_tag else ""
            year = _extract_year(info_text)
            journal = _extract_journal(info_text)

            if not title:
                continue

            results.append({
                "source": "baidu_scholar",
                "title": title,
                "authors": authors,
                "year": year,
                "journal": journal,
                "volume": "",
                "issue": "",
                "pages": "",
                "doi": "",
                "url": link,
                "type": "journal-article",
            })

        return results
    except Exception as e:
        print(f"[Baidu Scholar] Error: {e}")
        return []


def search_cnki_fallback(query: str, limit: int = 5) -> list[dict]:
    """Fallback: search CNKI via web (limited without login)."""
    url = f"https://kns.cnki.net/kns8/defaultresult/index?kw={quote(query)}&korder=desc&dbcode=CJFD"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")

        results = []
        items = soup.select(".result-table-list tr") or soup.select(".source tr")

        for item in items[1:limit+1]:  # skip header row
            cols = item.select("td")
            if len(cols) < 3:
                continue
            title_tag = cols[1].select_one("a") if len(cols) > 1 else None
            title = title_tag.get_text(strip=True) if title_tag else ""
            link = "https://kns.cnki.net" + title_tag.get("href", "") if title_tag else ""
            author_text = cols[2].get_text(strip=True) if len(cols) > 2 else ""
            authors = _parse_cn_authors(author_text)
            journal = cols[3].get_text(strip=True) if len(cols) > 3 else ""
            year_text = cols[4].get_text(strip=True) if len(cols) > 4 else ""
            year = _extract_year(year_text)

            if not title:
                continue

            results.append({
                "source": "cnki",
                "title": title,
                "authors": authors,
                "year": year,
                "journal": journal,
                "volume": "",
                "issue": "",
                "pages": "",
                "doi": "",
                "url": link,
                "type": "journal-article",
            })

        return results
    except Exception as e:
        print(f"[CNKI] Error: {e}")
        return []


def _parse_cn_authors(text: str) -> list[dict]:
    """Parse author string like '张三; 李四' or '张三,李四' into list."""
    if not text:
        return []
    text = re.sub(r"作者[：:]", "", text)
    parts = re.split(r"[;；,，]", text)
    authors = []
    for p in parts:
        name = p.strip()
        if name and len(name) <= 10:  # sanity check
            authors.append({"family": name, "given": ""})
    return authors[:10]


def _extract_year(text: str) -> int | None:
    """Extract 4-digit year from text."""
    match = re.search(r"(19|20)\d{2}", text)
    return int(match.group()) if match else None


def _extract_journal(text: str) -> str:
    """Try to extract journal name from info text."""
    # Remove authors and year, what's left is often the journal
    text = re.sub(r"(19|20)\d{2}", "", text)
    text = re.sub(r"[\u4e00-\u9fff]{2,4}[；;,，]", "", text)
    parts = re.split(r"[|｜·•]", text)
    for p in parts:
        p = p.strip()
        if len(p) > 2:
            return p
    return text.strip()[:30]


def search_chinese(query: str, limit: int = 5) -> list[dict]:
    """Search Baidu Scholar (+ CNKI fallback), score and return results."""
    results = search_baidu_scholar(query, limit)

    if len(results) < 2:
        results += search_cnki_fallback(query, limit)

    for r in results:
        score = fuzz.token_sort_ratio(query.lower(), r["title"].lower())
        r["confidence"] = score

    results.sort(key=lambda x: x["confidence"], reverse=True)
    return results[:limit]


if __name__ == "__main__":
    import json
    results = search_chinese("注意力机制在自然语言处理中的应用")
    print(json.dumps(results, indent=2, ensure_ascii=False))
