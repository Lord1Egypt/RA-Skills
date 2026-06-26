#!/usr/bin/env python3
"""
Finance Monitor - Fetch 18 financial indicators from CNBC via web_fetch.
Writes to SQLite database.
"""

import sqlite3, json, re, os, sys, argparse, pathlib, warnings, time
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# ── Error Classes ──────────────────────────────────────────────────────────────
class FetchError(Exception):
    """Raised when fetching fails after all retries."""
    pass

class RateLimitError(Exception):
    """Raised when API rate limit is hit."""
    def __init__(self, retry_after=60):
        self.retry_after = retry_after
        super().__init__(f"Rate limited, retry after {retry_after}s")

class DatabaseError(Exception):
    """Raised when database operation fails."""
    pass

# Fix Windows console encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ── Indicators Config ─────────────────────────────────────────────────────────
# CNBC URLs for each indicator
INDICATORS = [
    # -- 宏观经济指标 --
    {"code": "US10YTIP", "name_cn": "美国10年期TIPS", "url": "https://www.cnbc.com/quotes/US10YTIP"},
    {"code": "US10Y",    "name_cn": "美国10年期国债", "url": "https://www.cnbc.com/quotes/US10Y"},
    {"code": "GC",       "name_cn": "黄金 COMEX",     "url": "https://www.cnbc.com/quotes/@GC.1"},
    {"code": "CL",       "name_cn": "WTI 原油",       "url": "https://www.cnbc.com/quotes/@CL.1"},
    # -- 指数 ETF --
    {"code": "SPY",      "name_cn": "标普500 ETF",    "url": "https://www.cnbc.com/quotes/SPY"},
    {"code": "SPX",      "name_cn": "标普500指数",    "url": "https://www.cnbc.com/quotes/SPX"},
    {"code": "QQQ",      "name_cn": "纳斯达克100 ETF","url": "https://www.cnbc.com/quotes/QQQ"},
    {"code": "NDX",      "name_cn": "纳斯达克100指数", "url": "https://www.cnbc.com/quotes/NDX"},
    # -- 美元 & VIX --
    {"code": "DXY",      "name_cn": "美元指数 DXY",   "url": "https://www.cnbc.com/quotes/.DXY"},
    {"code": "VIX",      "name_cn": "恐慌指数 VIX",   "url": "https://www.cnbc.com/quotes/.VIX"},
    # -- 美股个股（Magnificent 7 + 核心股）--
    {"code": "AAPL",     "name_cn": "苹果",           "url": "https://www.cnbc.com/quotes/AAPL"},
    {"code": "MSFT",     "name_cn": "微软",           "url": "https://www.cnbc.com/quotes/MSFT"},
    {"code": "NVDA",     "name_cn": "英伟达",         "url": "https://www.cnbc.com/quotes/NVDA"},
    {"code": "AMZN",     "name_cn": "亚马逊",         "url": "https://www.cnbc.com/quotes/AMZN"},
    {"code": "META",     "name_cn": "Meta",           "url": "https://www.cnbc.com/quotes/META"},
    {"code": "UNH",      "name_cn": "联合健康",       "url": "https://www.cnbc.com/quotes/UNH"},
    {"code": "KO",       "name_cn": "可口可乐",       "url": "https://www.cnbc.com/quotes/KO"},
    {"code": "BRK.B",    "name_cn": "伯克希尔哈撒韦", "url": "https://www.cnbc.com/quotes/BRK.B"},
]

PROTECTED = (
    "/etc/", "/usr/", "/bin/", "/sbin/", "/lib/", "/System/",
    "/Windows/System32/", "/Windows/SysWOW64/",
    "C:\\Windows\\", "C:\\Program Files\\", "C:\\Program Files (x86)\\",
)

def check_path_safe(path_str, name):
    p = pathlib.Path(path_str).resolve()
    for pat in PROTECTED:
        if pat in str(p):
            raise PermissionError(f"Refusing {name}='{path_str}' — system path detected.")

# ── Config ────────────────────────────────────────────────────────────────────
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds
RATE_LIMIT_DELAY = 60  # seconds

# ── HTML Fetch ────────────────────────────────────────────────────────────────
def fetch_html(url, retries=MAX_RETRIES):
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml",
    })
    last_err = None
    for attempt in range(retries):
        try:
            with urlopen(req, timeout=15) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except HTTPError as e:
            last_err = e
            if e.code == 429:
                # Rate limited, respect Retry-After header
                retry_after = int(e.headers.get('Retry-After', RATE_LIMIT_DELAY))
                if attempt < retries - 1:
                    warnings.warn(f"Rate limited (429) for {url}, waiting {retry_after}s (attempt {attempt+1}/{retries})", UserWarning)
                    time.sleep(retry_after)
                    continue
                else:
                    # All retries exhausted on rate limit
                    raise RateLimitError(retry_after)
            elif e.code >= 500:
                # Server error, retry
                warnings.warn(f"Server error {e.code} for {url}, attempt {attempt+1}/{retries}", UserWarning)
                if attempt < retries - 1:
                    time.sleep(RETRY_DELAY * (attempt + 1))
                continue
            else:
                # Client error (4xx), don't retry
                raise FetchError(f"HTTP {e.code} for {url}: {e.reason}")
        except URLError as e:
            last_err = e
            warnings.warn(f"URL error for {url}, attempt {attempt+1}/{retries}: {e.reason}", UserWarning)
            if attempt < retries - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
        except TimeoutError as e:
            last_err = e
            warnings.warn(f"Timeout for {url}, attempt {attempt+1}/{retries}", UserWarning)
            if attempt < retries - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
        except Exception as e:
            last_err = e
            warnings.warn(f"Unexpected error for {url}: {type(e).__name__}: {e}", UserWarning)
            raise FetchError(f"Unexpected error: {e}") from e

    raise FetchError(f"Failed after {retries} attempts: {last_err}")

# ── Parsing ──────────────────────────────────────────────────────────────────
def parse_float(s):
    s = str(s).strip().replace(",", "").replace("%", "").replace("$", "")
    try:
        return float(s)
    except:
        return None

def parse_price_and_change(text):
    """Parse '4,291.90-283.00 (-6.19%)' or '648.57-9.43 (-1.43%)' or '642.91-5.66 (-0.87%)'"""
    # Pattern: price change (changepct)
    m = re.search(r'([\d,]+\.?\d*)\s*([+-]?\d+\.?\d*)\s*\(([%+-]?\d+\.?\d*)%\)', text)
    if m:
        price = parse_float(m.group(1))
        change = parse_float(m.group(2))
        chg_pct = parse_float(m.group(3))
        return price, change, chg_pct
    # Pattern: just price (maybe with %)
    m = re.search(r'^([\d,]+\.?\d+)', text.strip().replace('%', ''))
    if m:
        return parse_float(m.group(1)), None, None
    return None, None, None

def parse_html_content(html, code):
    """Extract price data from raw CNBC HTML."""
    result = {
        "prev_close": None, "current_price": None, "after_hours": None,
        "change_pct": None, "week52_high": None, "dist_from_high_pct": None,
        "week52_low": None, "dist_from_low_pct": None,
    }

    # Plain text version of HTML for regex matching (used by multiple sections)
    all_text = re.sub(r'<[^>]+>', ' ', html)

    # Try JSON embedded in HTML (FinancialQuote JSON-LD blocks)
    # Find each <script type="application/ld+json">, extract top-level
    # JSON objects via depth-counting, check for ticker match, extract price fields
    for script_m in re.finditer(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>', html):
        script_content_start = script_m.end()
        script_end_m = re.search(r'</script>', html[script_content_start:])
        if not script_end_m:
            continue
        script_content_end = script_content_start + script_end_m.start()
        json_str = html[script_content_start:script_content_end]
        # Extract top-level JSON objects using depth-counting
        i = 0
        while i < len(json_str):
            if json_str[i] == '{':
                # Start of a top-level JSON object
                obj_start = i
                depth = 0
                obj_end = obj_start
                for j in range(obj_start, len(json_str)):
                    if json_str[j] == '{':
                        depth += 1
                    elif json_str[j] == '}':
                        depth -= 1
                        if depth == 0:
                            obj_end = j + 1
                            break
                obj = json_str[obj_start:obj_end]
                # Check if this object contains our ticker's tickerSymbol
                # Handle special cases: .DXY, .VIX have dot-prefixed tickerSymbols
                dot_prefix_codes = {'DXY', 'VIX'}
                tp_variants = [re.escape(code)]
                if code in dot_prefix_codes:
                    tp_variants.append('\\' + re.escape(code))  # e.g. .DXY → \.DXY
                tp_variants.append('@' + re.escape(code) + r'\.[0-9]+')
                ticker_found = False
                for tp_pat in tp_variants:
                    if re.search(r'"tickerSymbol"\s*:\s*"' + tp_pat + r'"', obj):
                        ticker_found = True
                        break
                if ticker_found:
                    price_m = re.search(r'"price"\s*:\s*"([0-9.,]+%?)"', obj)
                    if price_m:
                        result["current_price"] = parse_float(price_m.group(1).rstrip('%').replace(',', ''))
                        pcp_m = re.search(r'"priceChangePercent"\s*:\s*"([+-]?[0-9.]+)"', obj)
                        pc_m = re.search(r'"priceChange"\s*:\s*"([+-]?[0-9.-]+)"', obj)
                        if pcp_m: result["change_pct"] = parse_float(pcp_m.group(1))
                        elif pc_m: result["change_pct"] = parse_float(pc_m.group(1))
                        pp_m = re.search(r'"previousPrice"\s*:\s*"([0-9.,]+)"', obj)
                        if pp_m:
                            result["prev_close"] = parse_float(pp_m.group(1).replace(',', ''))
                        else:
                            # Compute prev_close from price and priceChange
                            price_val = result.get("current_price")
                            pc_m2 = re.search(r'"priceChange"\s*:\s*"([+-]?[0-9.]+)"', obj)
                            if price_val is not None and pc_m2:
                                pc_val = parse_float(pc_m2.group(1))
                                if pc_val is not None:
                                    result["prev_close"] = round(price_val - pc_val, 4)
                        # If we have price+pcp, extract 52-week data then return
                        if result["current_price"] is not None and result["change_pct"] is not None:
                            # 52w range from HTML
                            m52 = re.search(r'52 week range\s*([\d,]+\.?\d*)\s*[-–]\s*([\d,]+\.?\d*)', all_text, re.IGNORECASE)
                            if m52:
                                result["week52_low"] = parse_float(m52.group(1))
                                result["week52_high"] = parse_float(m52.group(2))
                            return result
                i = obj_end
            else:
                i += 1

    # Try last price from QuoteStrip (set current_price)
    # Must match class="QuoteStrip-lastPrice" exactly to avoid matching CSS selectors
    # in <style> tags (where "QuoteStrip-lastPrice{...}>" would incorrectly cross into HTML)
    quote_m = re.search(r'class="QuoteStrip-lastPrice"[^>]*>\s*([\d,]+\.?\d*)', html)
    if quote_m:
        result["current_price"] = parse_float(quote_m.group(1))

    # Try after hours separately (does NOT overwrite current_price)
    # Handle newlines/child elements: label is followed by tag containing the value
    ah_m = re.search(r'After Hours:[\s\S]*?>([\d,]+\.?\d*)', html)
    if ah_m:
        result["after_hours"] = parse_float(ah_m.group(1))

    # If no current_price yet, try Last | pattern as fallback
    # IMPORTANT: sanity check — "Last | 7:40 AM EDT" must NOT give us 7.0 as price
    if result["current_price"] is None:
        last_m = re.search(r'Last\s*\|\s*[^0-9]*([\d,]+\.?\d*)', html)
        if last_m:
            val = parse_float(last_m.group(1))
            # Reject absurdly small values (likely time like "7" from "7:40 AM")
            if val is not None and val > 10:
                result["current_price"] = val

    # Try to find price-change pattern anywhere
    # "4,291.90-283.00 (-6.19%)" or "648.57-9.43 (-1.43%)"
    for m in re.finditer(r'([\d,]+\.\d+)\s*([+-][\d,]+\.\d+)\s*\(([%+-]?\d+\.\d+)%\)', all_text):
        price, change, chg_pct = parse_float(m.group(1)), parse_float(m.group(2)), parse_float(m.group(3))
        if price and chg_pct and abs(chg_pct) < 50:  # sanity check
            result["current_price"] = price
            result["change_pct"] = chg_pct
            break

    # Prev Close
    for pat in [r'Prev[iI]?[ ]?[Cc]lose\s*([\d,]+\.?\d*)', r'Previous\s*Close\s*([\d,]+\.?\d*)']:
        m = re.search(pat, all_text)
        if m:
            result["prev_close"] = parse_float(m.group(1))
            break

    # 52w range
    m = re.search(r'52 week range\s*([\d,]+\.?\d*)\s*[-–]\s*([\d,]+\.?\d*)', all_text, re.IGNORECASE)
    if m:
        result["week52_low"] = parse_float(m.group(1))
        result["week52_high"] = parse_float(m.group(2))

    return result

# ── Fetch one indicator ───────────────────────────────────────────────────────
def fetch_cnbc(indicator):
    url = indicator["url"]
    try:
        html = fetch_html(url)
    except RateLimitError:
        # Rate limit is a retriable error; let caller handle it
        raise
    except FetchError as e:
        warnings.warn(f"Failed to fetch {indicator['code']}: {e}", UserWarning)
        return None
    except Exception as e:
        warnings.warn(f"Failed to fetch {indicator['code']}: {e}", UserWarning)
        return None

    data = parse_html_content(html, indicator["code"])

    if data.get("current_price") is None:
        warnings.warn(f"No price extracted for {indicator['code']}", UserWarning)

    return {
        "code": indicator["code"],
        "name_cn": indicator["name_cn"],
        **data,
        "source": "cnbc",
    }

# ── DB ────────────────────────────────────────────────────────────────────────
def init_db(db_path):
    os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS indicators (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fetch_date TEXT NOT NULL, fetch_time TEXT NOT NULL,
        name_cn TEXT NOT NULL, code TEXT NOT NULL,
        prev_close REAL, current_price REAL, after_hours REAL,
        change_pct REAL, week52_high REAL, dist_from_high_pct REAL,
        week52_low REAL, dist_from_low_pct REAL,
        source TEXT DEFAULT 'cnbc',
        created_at TEXT DEFAULT (datetime('now', 'localtime'))
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS fetch_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fetch_date TEXT NOT NULL, fetch_time TEXT NOT NULL,
        source TEXT NOT NULL, indicators_count INTEGER,
        created_at TEXT DEFAULT (datetime('now', 'localtime'))
    )""")
    c.execute("CREATE INDEX IF NOT EXISTS idx_code ON indicators(code)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_fetch_time ON indicators(fetch_time)")
    conn.commit()
    return conn

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    args = parse_args()
    db_path = args.db_path
    check_path_safe(db_path, "db-path")
    log_path = args.log_path or str(pathlib.Path(db_path).resolve().parent / "fetch.log")
    check_path_safe(log_path, "log-path")

    now = datetime.now()
    fetch_date = now.strftime("%Y-%m-%d")
    fetch_time = now.strftime("%Y-%m-%d %H:%M")

    # Fetch data with error tracking
    all_data = []
    errors = []
    for ind in INDICATORS:
        try:
            r = fetch_cnbc(ind)
            if r and r.get("current_price") is not None:
                # Calculate dist from 52w high/low
                if r.get("current_price") and r.get("week52_high"):
                    r["dist_from_high_pct"] = round((r["current_price"] - r["week52_high"]) / r["week52_high"] * 100, 4)
                if r.get("current_price") and r.get("week52_low"):
                    r["dist_from_low_pct"] = round((r["current_price"] - r["week52_low"]) / r["week52_low"] * 100, 4)
                all_data.append(r)
            elif r:
                errors.append(f"{ind['code']}: No price extracted")
        except FetchError as e:
            errors.append(f"{ind['code']}: {e}")
        except RateLimitError as e:
            errors.append(f"{ind['code']}: Rate limited, retry after {e.retry_after}s")
        except Exception as e:
            errors.append(f"{ind['code']}: {type(e).__name__}: {e}")

    # Check if all sources failed
    if not all_data:
        error_msg = f"All sources failed. Errors: {'; '.join(errors) if errors else 'Unknown'}"
        warnings.warn(error_msg, UserWarning)
        os.makedirs(os.path.dirname(log_path) or ".", exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{fetch_time}] ERROR: {error_msg}\n")
        print(f"\n❌ Failed | {fetch_time}")
        print(f"Errors: {error_msg}")
        sys.exit(1)

    # Write to database with error handling
    try:
        conn = init_db(db_path)
        c = conn.cursor()
        for d in all_data:
            c.execute("""INSERT INTO indicators
                (fetch_date, fetch_time, name_cn, code, prev_close, current_price,
                 after_hours, change_pct, week52_high, dist_from_high_pct,
                 week52_low, dist_from_low_pct, source)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (fetch_date, fetch_time, d["name_cn"], d["code"],
                 d["prev_close"], d["current_price"], d["after_hours"],
                 d["change_pct"], d["week52_high"], d["dist_from_high_pct"],
                 d["week52_low"], d["dist_from_low_pct"], d["source"]))
        c.execute("INSERT INTO fetch_log (fetch_date,fetch_time,source,indicators_count) VALUES (?,?,?,?)",
            (fetch_date, fetch_time, "cnbc", len(all_data)))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        error_msg = f"Database error: {e}"
        warnings.warn(error_msg, UserWarning)
        print(f"\n❌ Database error | {fetch_time}")
        print(f"Error: {error_msg}")
        sys.exit(1)

    # Write log
    log_msg = f"[{fetch_time}] Fetched {len(all_data)} indicators -> {db_path}"
    if errors:
        log_msg += f" | Errors: {'; '.join(errors)}"
    os.makedirs(os.path.dirname(log_path) or ".", exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(log_msg + "\n")

    print(f"\n✅ Data fetched | {fetch_time}")
    print(f"📂 DB: {db_path}")
    if errors:
        print(f"⚠️  {len(errors)} indicators failed (see log)")
    print()
    print(f"{'Indicator':<18} {'Code':<10} {'Price':>12} {'Change':>8}")
    print("-" * 52)
    for d in all_data:
        curr = d.get("current_price")
        curr_str = f"{curr:.4f}" if curr is not None and curr < 100 else f"{curr:.2f}" if curr is not None else "N/A"
        chg = d.get("change_pct")
        chg_str = f"{chg:+.2f}%" if chg is not None else "N/A"
        print(f"{d['name_cn']:<18} {d['code']:<10} {curr_str:>12} {chg_str:>8}")

def parse_args():
    p = argparse.ArgumentParser(description="Finance Monitor — fetch 18 indicators from CNBC")
    p.add_argument("--db-path", required=True)
    p.add_argument("--log-path", default=None)
    return p.parse_args()

if __name__ == "__main__":
    main()
