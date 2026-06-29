"""hkex_announcements.py — HKEX 披露易公告

接口:
- 反查 stockId: https://www1.hkexnews.hk/search/prefix.do?callback=cb&lang=EN&type=A&name={公司名}&market=SEHK
- 公告列表: https://www1.hkexnews.hk/search/titleSearchServlet.do?stockId={id}&fromDate={YYYYMMDD}&toDate={YYYYMMDD}&market=SEHK&category=0&rowRange=100&lang=EN
- PDF 提取: pdftotext
"""
import os, json, sys, re, subprocess, time, tempfile
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

sys.path.insert(0, os.path.dirname(__file__))
from _base import BaseFetcher, FetchResult

CACHE_PATH = os.path.join(os.path.dirname(__file__), "..", "state", "hkex_stockid_cache.json")



def load_stockid_cache():
    try:
        with open(CACHE_PATH) as f:
            return json.load(f)
    except Exception:
        return {}


def save_stockid_cache(cache):
    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f)


def lookup_stockid(query: str, exact_code: str | None = None) -> str | None:
    """使用 HKEX prefix.do 反查 stockId。

    exact_code: 5位零填充港股代码(如 "00700")。提供时只接受 code 完全匹配的结果,
    避免 prefix 模糊搜索取错股票(例如 name=5 返回10个候选)。
    """
    url = f"https://www1.hkexnews.hk/search/prefix.do?callback=callback&lang=EN&type=A&name={query}&market=SEHK"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return None
        text = resp.text.strip()
        match = re.search(r'callback\((.+)\);?\s*$', text, re.DOTALL)
        if not match:
            return None
        data = json.loads(match.group(1))
        stock_info = data.get("stockInfo", [])
        if not stock_info:
            return None
        if exact_code:
            for si in stock_info:
                if str(si.get("code", "")).zfill(5) == exact_code:
                    return str(si.get("stockId", ""))
            return None  # 没有精确匹配 = 宁可不要,也不取错的
        return str(stock_info[0].get("stockId", ""))
    except Exception:
        pass
    return None


class Fetcher(BaseFetcher):
    name = "hkex_announcements"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hk_symbols = self._get_hk_symbols()

    def _get_hk_symbols(self):
        try:
            wl_path = os.path.join(os.path.dirname(__file__), "watchlist.yaml")
            if os.path.exists(wl_path):
                import yaml
                with open(wl_path) as f:
                    data = yaml.safe_load(f) or {}
                symbols = []
                for section in ["positions", "focus"]:
                    for item in data.get(section, []):
                        if ".HK" in item["symbol"]:
                            symbols.append(item["symbol"])
                return symbols if symbols else ["0700.HK"]
        except Exception:
            pass
        return ["0700.HK"]

    def fetch_raw(self):
        today = datetime.now()
        from_date = (today - timedelta(days=7)).strftime("%Y%m%d")
        to_date = today.strftime("%Y%m%d")

        cache = load_stockid_cache()
        cache_dirty = False
        # 整体时间预算,确保在 data_daily 的 180s kill 之前安全收尾
        deadline = time.time() + 150

        # ---- Phase 1: 解析 stockId。已缓存的免费,未缓存的并发反查 ----
        symbol_to_id = {}
        uncached = []
        for symbol in self.hk_symbols:
            if symbol in cache:
                if cache[symbol]:
                    symbol_to_id[symbol] = cache[symbol]
            else:
                uncached.append(symbol)

        if uncached and time.time() < deadline:
            def _resolve(symbol):
                code5 = symbol.replace(".HK", "").zfill(5)
                query = code5.lstrip("0") or "0"
                return symbol, lookup_stockid(query, exact_code=code5)
            with ThreadPoolExecutor(max_workers=8) as ex:
                futures = {ex.submit(_resolve, s): s for s in uncached}
                for fut in as_completed(futures):
                    try:
                        symbol, sid = fut.result()
                    except Exception:
                        continue
                    cache_dirty = True
                    cache[symbol] = sid or ""  # 缓存空值避免重复反查
                    if sid:
                        symbol_to_id[symbol] = sid

        if cache_dirty:
            save_stockid_cache(cache)

        # ---- Phase 2: 并发拉取公告列表 ----
        all_announcements = {}

        def _fetch_titles(symbol, stock_id):
            url = (
                f"https://www1.hkexnews.hk/search/titleSearchServlet.do?"
                f"stockId={stock_id}&fromDate={from_date}&toDate={to_date}"
                f"&market=SEHK&category=0&rowRange=50&lang=EN"
            )
            resp = requests.get(url, timeout=12)
            if resp.status_code == 200:
                return symbol, resp.text
            return symbol, None

        with ThreadPoolExecutor(max_workers=8) as ex:
            futures = {
                ex.submit(_fetch_titles, s, sid): s
                for s, sid in symbol_to_id.items()
            }
            for fut in as_completed(futures):
                remaining = deadline - time.time()
                if remaining <= 0:
                    break
                try:
                    symbol, text = fut.result(timeout=max(1, remaining))
                except Exception:
                    continue
                if text:
                    all_announcements[symbol] = text

        if not all_announcements:
            return None

        return json.dumps(all_announcements, ensure_ascii=False)

    def parse(self, raw):
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError(f"Expected JSON object, got {type(data).__name__}")
        records = []
        for symbol, response_text in data.items():
            try:
                resp_data = json.loads(response_text)
                # result 字段是嵌套的 JSON 字符串
                result_str = resp_data.get("result", "[]")
                items = json.loads(result_str) if isinstance(result_str, str) else result_str
                for item in items[:20]:
                    file_link = item.get("FILE_LINK", "")
                    if file_link and not file_link.startswith("http"):
                        file_link = f"https://www1.hkexnews.hk{file_link}"
                    records.append({
                        "symbol": symbol,
                        "title": item.get("TITLE", "").replace("<br/>", " ").strip(),
                        "date": item.get("DATE_TIME", ""),
                        "category": item.get("LONG_TEXT", ""),
                        "stock_name": item.get("STOCK_NAME", "").replace("<br/>", "/"),
                        "file_type": item.get("FILE_TYPE", ""),
                        "url": file_link,
                    })
            except Exception:
                continue

        return records

    def validate(self, records):
        # HKEX 可能某天没有新公告，空列表正常
        if len(records) > 500:
            raise ValueError(f"Abnormal count: {len(records)}")
        for r in records[:10]:
            if not r.get("symbol"):
                raise ValueError("Missing symbol")
        return True


if __name__ == '__main__':
    from _base import cli_main
    cli_main(Fetcher)
