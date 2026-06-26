"""
浏览器备用抓取工具
当 API 请求失败时，通过抓取网页 HTML 解析数据。
纯 requests + BeautifulSoup，不依赖 Selenium。
"""
import requests
import time
import io
import contextlib
from typing import Optional, Callable, Any


class FetchError(Exception):
    """抓取失败异常"""
    pass


def fetch_with_retry(
    url: str,
    headers: Optional[dict] = None,
    timeout: int = 10,
    retries: int = 3,
    backoff: float = 1.5,
    encoding: Optional[str] = None,
    parser: Optional[str] = "html.parser",
    session: Optional[requests.Session] = None,
) -> Any:
    """
    带重试的抓取，同时返回 (text, soup)。

    Args:
        url: 目标URL
        headers: 请求头
        timeout: 单次超时（秒）
        retries: 最大重试次数
        backoff: 退避倍数
        encoding: 响应编码（默认自动检测）
        parser: BeautifulSoup 解析器
        session: requests.Session（可复用连接）
    Returns:
        (response_text, BeautifulSoup)
    Raises:
        FetchError: 所有重试失败后
    """
    default_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    if headers:
        default_headers.update(headers)

    if session is None:
        session = requests.Session()

    last_error = None
    for attempt in range(retries):
        try:
            r = session.get(url, headers=default_headers, timeout=timeout)
            r.raise_for_status()
            text = r.text
            if encoding:
                text = text.encode(r.encoding or "utf-8").decode(encoding, errors="replace")
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(text, parser)
            except ImportError:
                soup = None
            return text, soup
        except Exception as e:
            last_error = e
            if attempt < retries - 1:
                wait = backoff ** attempt
                time.sleep(wait)
            continue

    raise FetchError(f"全部{retries}次重试失败: {last_error}")


def parse_eastmoney_table(url: str, retries: int = 2) -> list:
    """
    抓取东方财富网页表格数据。

    Args:
        url: 东方财富页面URL
        retries: 重试次数
    Returns:
        list[dict]，每行一个字典
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        raise FetchError("需要安装 bs4: pip install beautifulsoup4")

    text, soup = fetch_with_retry(url, retries=retries, parser="lxml")
    tables = soup.find_all("table")
    results = []
    for table in tables:
        try:
            import pandas as pd
            dfs = pd.read_html(io.StringIO(str(table)))
            if dfs:
                results.extend(dfs)
        except Exception:
            continue
    return results


# ─── 常用东方财富行情页面 ────────────────────────────────────────────

INDEX_PAGE = "https://quote.eastmoney.com/center/gridlist.html"


def fetch_eastmoney_index() -> dict:
    """
    备用：从东方财富网页抓取A股主要指数。
    当 Sina hq API 不可用时调用。
    Returns: dict {代码: {"name": str, "price": float, "chg": float, "pct": float}}
    """
    from bs4 import BeautifulSoup

    # 东方财富 A股指数页面
    url = "https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=20&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:1+t:2&fields=f2,f3,f4,f12,f14"
    headers = {"Referer": "https://quote.eastmoney.com/", "User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        items = data.get("data", {}).get("diff", [])
        result = {}
        name_map = {
            "000001": "上证指数", "399001": "深证成指", "399006": "创业板指",
            "000688": "科创50", "000300": "沪深300", "399905": "中证500",
        }
        for item in items:
            code = str(item.get("f12", ""))
            if code in name_map:
                result[code] = {
                    "name": name_map[code],
                    "price": item.get("f2", 0),
                    "pct": item.get("f3", 0),
                }
        return result
    except Exception:
        pass

    # 兜底：直接解析 Eastmoney 行情页 HTML
    try:
        text, soup = fetch_with_retry(
            "https://quote.eastmoney.com/center/gridlist.html",
            headers={"Referer": "https://www.eastmoney.com/"},
            retries=2,
        )
        # 解析指数名称和价格
        import re
        indices = {}
        # 东方财富页面里含实时数据在 JS 变量中
        script_texts = soup.find_all("script")
        for script in script_texts:
            content = script.string or ""
            # 找 hq_str_xxx 格式的数据
            matches = re.findall(r'hq_str_(sh\d{6}|sz\d{6})="([^"]+)"', content)
            for code, data in matches:
                parts = data.split(",")
                if len(parts) > 4:
                    try:
                        price = float(parts[3])
                        prev = float(parts[2])
                        pct = (price - prev) / prev * 100 if prev else 0
                        indices[code] = {"price": price, "pct": pct}
                    except ValueError:
                        continue
        return indices
    except Exception:
        return {}


if __name__ == "__main__":
    # 测试
    print("测试 browser_fetch...")
    result = fetch_eastmoney_index()
    print(f"获取到 {len(result)} 个指数")
    for v in result.values():
        print(v)
