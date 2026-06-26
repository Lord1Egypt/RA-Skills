import argparse
import datetime as dt
import http.client
import json
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


MARKET_SOURCES = ["eastmoney", "akshare", "tushare", "pytdx", "baostock", "yfinance"]
NEWS_SOURCES = ["tavily", "serpapi", "bocha", "brave", "minimax"]
INTEL_MODES = ["info", "strategy"]
STRATEGIES = ["auto", "ma_cross", "ma_trend", "bias_guard", "wave", "cn_review", "us_regime"]
CACHE_FILE = Path(__file__).resolve().parent / ".cache" / "market_intel_cache.json"
DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
SYMBOL_ALIASES = {
    "欧菲光": "002456.SZ",
    "中国铝业": "601600.SS",
    "中国电建": "601669.SS",
    "牧原股份": "002714.SZ",
    "中证500": "000905.SS",
    "csi500": "000905.SS",
    "zz500": "000905.SS",
}


def utc_now():
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def load_cache():
    if not CACHE_FILE.exists():
        return {}
    try:
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_cache(cache_data):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache_data, ensure_ascii=False), encoding="utf-8")


def cache_get(cache_key, ttl_seconds):
    cache_data = load_cache()
    node = cache_data.get(cache_key)
    if not node:
        return None
    ts = node.get("ts", 0)
    if time.time() - ts > ttl_seconds:
        return None
    return node.get("data")


def cache_set(cache_key, value):
    cache_data = load_cache()
    cache_data[cache_key] = {"ts": time.time(), "data": value}
    if len(cache_data) > 500:
        keys = sorted(cache_data.keys(), key=lambda k: cache_data[k].get("ts", 0), reverse=True)[:300]
        cache_data = {k: cache_data[k] for k in keys}
    save_cache(cache_data)


def normalize_symbol(symbol):
    raw = str(symbol or "").strip()
    if not raw:
        return raw
    if raw in SYMBOL_ALIASES:
        return SYMBOL_ALIASES[raw]
    lower = raw.lower()
    if lower in SYMBOL_ALIASES:
        return SYMBOL_ALIASES[lower]
    if "." in raw:
        left, right = raw.split(".", 1)
        return f"{left.upper()}.{right.upper()}"
    if raw.isdigit() and len(raw) == 6:
        if raw.startswith(("6", "9", "5")):
            return f"{raw}.SS"
        if raw.startswith("0"):
            if raw in {"000300", "000905", "000852", "000016", "000001"}:
                return f"{raw}.SS"
            return f"{raw}.SZ"
        return f"{raw}.SZ"
    return raw


def to_cn_code(symbol):
    norm = normalize_symbol(symbol)
    if "." in norm:
        code, suffix = norm.split(".", 1)
        suffix = suffix.upper()
        if suffix in {"SZ"}:
            return f"0.{code}"
        if suffix in {"SH", "SS"}:
            return f"1.{code}"
    if norm.isdigit() and len(norm) == 6:
        if norm.startswith(("6", "9", "5")):
            return f"1.{norm}"
        return f"0.{norm}"
    return ""


def parse_sources(value, allowed):
    if not value:
        return allowed, []
    items = [x.strip().lower() for x in value.split(",") if x.strip()]
    valid = [x for x in items if x in allowed]
    invalid = [x for x in items if x not in allowed]
    return valid, invalid


def http_json(url, method="GET", headers=None, payload=None, timeout=15, retries=None, backoff=None, use_cache=False, cache_ttl=60):
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    retries = int(os.getenv("MARKET_INTEL_HTTP_RETRIES", "3")) if retries is None else retries
    backoff = float(os.getenv("MARKET_INTEL_HTTP_BACKOFF", "0.8")) if backoff is None else backoff
    merged_headers = dict(DEFAULT_HEADERS)
    if headers:
        merged_headers.update(headers)
    cache_key = json.dumps({"url": url, "method": method, "payload": payload}, ensure_ascii=False, sort_keys=True)
    if use_cache:
        cached = cache_get(cache_key, cache_ttl)
        if cached is not None:
            return cached
    last_error = None
    for i in range(max(1, retries + 1)):
        req = urllib.request.Request(url=url, method=method, headers=merged_headers, data=data)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8", errors="ignore")
                obj = {} if not body else json.loads(body)
                if use_cache:
                    cache_set(cache_key, obj)
                return obj
        except urllib.error.HTTPError as e:
            last_error = e
            if e.code in {429, 500, 502, 503, 504} and i < retries:
                time.sleep(backoff * (2**i) + random.uniform(0.05, 0.25))
                continue
            raise
        except (urllib.error.URLError, TimeoutError, http.client.RemoteDisconnected, ConnectionResetError) as e:
            last_error = e
            if i < retries:
                time.sleep(backoff * (2**i) + random.uniform(0.05, 0.25))
                continue
            raise
    if last_error:
        raise last_error
    return {}


def safe_call(fn):
    try:
        return {"ok": True, "data": fn()}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def fetch_yfinance_quote(symbol):
    norm = normalize_symbol(symbol)
    qs = urllib.parse.urlencode({"symbols": norm})
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?{qs}"
    data = http_json(url, use_cache=True, cache_ttl=45)
    rows = data.get("quoteResponse", {}).get("result", [])
    if not rows:
        raise RuntimeError("未获取到 yfinance 行情")
    row = rows[0]
    return {
        "symbol": row.get("symbol"),
        "short_name": row.get("shortName"),
        "currency": row.get("currency"),
        "price": row.get("regularMarketPrice"),
        "change": row.get("regularMarketChange"),
        "change_percent": row.get("regularMarketChangePercent"),
        "market_time": row.get("regularMarketTime"),
        "source": "yfinance",
    }


def fetch_yfinance_history(symbol, interval="1d", range_="1mo"):
    norm = normalize_symbol(symbol)
    qs = urllib.parse.urlencode({"interval": interval, "range": range_})
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(norm)}?{qs}"
    data = http_json(url, use_cache=True, cache_ttl=120)
    result = data.get("chart", {}).get("result", [])
    if not result:
        raise RuntimeError("未获取到 yfinance 历史K线")
    r0 = result[0]
    ts = r0.get("timestamp", [])
    quote = (r0.get("indicators", {}).get("quote", [{}]) or [{}])[0]
    rows = []
    for i, t in enumerate(ts):
        rows.append(
            {
                "time": t,
                "open": (quote.get("open") or [None] * len(ts))[i],
                "high": (quote.get("high") or [None] * len(ts))[i],
                "low": (quote.get("low") or [None] * len(ts))[i],
                "close": (quote.get("close") or [None] * len(ts))[i],
                "volume": (quote.get("volume") or [None] * len(ts))[i],
            }
        )
    return {"symbol": norm, "interval": interval, "range": range_, "rows": rows, "source": "yfinance"}


def fetch_eastmoney_quote(symbol):
    cn_code = to_cn_code(symbol)
    if not cn_code:
        raise RuntimeError("eastmoney 仅支持 A 股/指数代码")
    qs = urllib.parse.urlencode({"secid": cn_code, "fields": "f43,f57,f58,f60,f169,f170"})
    url = f"https://push2.eastmoney.com/api/qt/stock/get?{qs}"
    data = http_json(url, use_cache=True, cache_ttl=20)
    row = data.get("data")
    if not row:
        raise RuntimeError("未获取到 eastmoney 行情")
    price = to_float(row.get("f43"))
    change = to_float(row.get("f169"))
    change_percent = to_float(row.get("f170"))
    return {
        "symbol": row.get("f57"),
        "short_name": row.get("f58"),
        "price": None if price is None else round(price / 100, 4),
        "change": None if change is None else round(change / 100, 4),
        "change_percent": None if change_percent is None else round(change_percent / 100, 4),
        "last_close": None if to_float(row.get("f60")) is None else round(to_float(row.get("f60")) / 100, 4),
        "source": "eastmoney",
    }


def fetch_tavily_news(query, max_results=5):
    api_key = os.getenv("TAVILY_API_KEY", "")
    if not api_key:
        raise RuntimeError("缺少 TAVILY_API_KEY")
    payload = {"query": query, "max_results": max_results, "topic": "news"}
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    data = http_json("https://api.tavily.com/search", method="POST", headers=headers, payload=payload)
    items = []
    for r in data.get("results", []):
        items.append(
            {
                "title": r.get("title"),
                "url": r.get("url"),
                "published_at": r.get("published_date"),
                "content": r.get("content"),
                "source": "tavily",
            }
        )
    return {"query": query, "items": items}


def fetch_serpapi_news(query, max_results=5):
    api_key = os.getenv("SERPAPI_API_KEY", "")
    if not api_key:
        raise RuntimeError("缺少 SERPAPI_API_KEY")
    qs = urllib.parse.urlencode(
        {
            "engine": "google_news",
            "q": query,
            "api_key": api_key,
            "num": max_results,
            "hl": "zh-cn",
            "gl": "cn",
        }
    )
    data = http_json(f"https://serpapi.com/search.json?{qs}")
    items = []
    for r in data.get("news_results", [])[:max_results]:
        items.append(
            {
                "title": r.get("title"),
                "url": r.get("link"),
                "published_at": r.get("date"),
                "source_name": r.get("source"),
                "source": "serpapi",
            }
        )
    return {"query": query, "items": items}


def fetch_brave_news(query, max_results=5):
    api_key = os.getenv("BRAVE_API_KEY", "")
    if not api_key:
        raise RuntimeError("缺少 BRAVE_API_KEY")
    qs = urllib.parse.urlencode({"q": query, "count": max_results})
    headers = {"X-Subscription-Token": api_key, "Accept": "application/json"}
    data = http_json(f"https://api.search.brave.com/res/v1/news/search?{qs}", headers=headers)
    items = []
    for r in data.get("results", [])[:max_results]:
        items.append(
            {
                "title": r.get("title"),
                "url": r.get("url"),
                "published_at": r.get("age"),
                "source_name": (r.get("meta") or {}).get("source"),
                "source": "brave",
            }
        )
    return {"query": query, "items": items}


def fetch_custom_news(source, query, max_results=5):
    base = os.getenv(f"{source.upper()}_BASE_URL", "")
    api_key = os.getenv(f"{source.upper()}_API_KEY", "")
    if not base:
        raise RuntimeError(f"缺少 {source.upper()}_BASE_URL")
    payload = {"query": query, "max_results": max_results}
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    data = http_json(base, method="POST", headers=headers, payload=payload)
    raw_items = data.get("items", data.get("results", []))
    items = []
    for r in raw_items[:max_results]:
        items.append(
            {
                "title": r.get("title"),
                "url": r.get("url"),
                "published_at": r.get("published_at") or r.get("date"),
                "source_name": r.get("source"),
                "source": source,
            }
        )
    return {"query": query, "items": items}


def fetch_local_fallback_news(query, max_results=5):
    _ = max_results
    return {
        "query": query,
        "items": [],
        "notice": "当前新闻源不可用，已返回空新闻集，建议配置 TAVILY_API_KEY/SERPAPI_API_KEY/BRAVE_API_KEY",
        "source": "local_fallback",
    }


def is_news_source_configured(source):
    if source == "tavily":
        return bool(os.getenv("TAVILY_API_KEY", ""))
    if source == "serpapi":
        return bool(os.getenv("SERPAPI_API_KEY", ""))
    if source == "brave":
        return bool(os.getenv("BRAVE_API_KEY", ""))
    if source in {"bocha", "minimax"}:
        return bool(os.getenv(f"{source.upper()}_BASE_URL", ""))
    return True


def fetch_akshare_quote(symbol):
    import akshare as ak

    norm = normalize_symbol(symbol)
    code = norm.split(".")[0]
    df = ak.stock_zh_a_spot_em()
    if "代码" not in df.columns:
        raise RuntimeError("akshare 返回字段不符合预期")
    row = df[df["代码"].astype(str) == str(code)]
    if row.empty:
        raise RuntimeError(f"akshare 未找到代码 {code}")
    r0 = row.iloc[0]
    return {
        "symbol": str(r0.get("代码")),
        "name": r0.get("名称"),
        "price": r0.get("最新价"),
        "change_percent": r0.get("涨跌幅"),
        "volume": r0.get("成交量"),
        "source": "akshare",
    }


def fetch_tushare_quote(symbol):
    norm = normalize_symbol(symbol)
    token = os.getenv("TUSHARE_TOKEN", "")
    if not token:
        raise RuntimeError("缺少 TUSHARE_TOKEN")
    import tushare as ts

    ts.set_token(token)
    pro = ts.pro_api()
    end_date = dt.datetime.now().strftime("%Y%m%d")
    start_date = (dt.datetime.now() - dt.timedelta(days=15)).strftime("%Y%m%d")
    df = pro.daily(ts_code=norm, start_date=start_date, end_date=end_date)
    if df is None or df.empty:
        raise RuntimeError(f"tushare 未返回数据: {norm}")
    r0 = df.sort_values("trade_date", ascending=False).iloc[0]
    return {
        "symbol": r0.get("ts_code"),
        "trade_date": r0.get("trade_date"),
        "open": r0.get("open"),
        "high": r0.get("high"),
        "low": r0.get("low"),
        "close": r0.get("close"),
        "volume": r0.get("vol"),
        "source": "tushare",
    }


def fetch_pytdx_quote(symbol):
    from pytdx.config.hosts import hq_hosts
    from pytdx.hq import TdxHq_API

    if len(symbol) < 6:
        raise RuntimeError("pytdx 需要 6 位证券代码")
    code = symbol[-6:]
    market = 1 if code.startswith(("5", "6", "9")) else 0
    api = TdxHq_API()
    for _, host, port in hq_hosts[:5]:
        if api.connect(host, port):
            try:
                res = api.get_security_quotes([(market, code)])
                if not res:
                    continue
                r0 = res[0]
                return {"symbol": code, "price": r0.get("price"), "last_close": r0.get("last_close"), "source": "pytdx"}
            finally:
                api.disconnect()
    raise RuntimeError("pytdx 连接失败或无数据")


def fetch_baostock_history(symbol):
    import baostock as bs

    lg = bs.login()
    if lg.error_code != "0":
        raise RuntimeError(f"baostock 登录失败: {lg.error_msg}")
    try:
        end_date = dt.datetime.now().strftime("%Y-%m-%d")
        start_date = (dt.datetime.now() - dt.timedelta(days=30)).strftime("%Y-%m-%d")
        rs = bs.query_history_k_data_plus(
            symbol,
            "date,open,high,low,close,volume",
            start_date=start_date,
            end_date=end_date,
            frequency="d",
            adjustflag="2",
        )
        rows = []
        while rs.error_code == "0" and rs.next():
            rows.append(rs.get_row_data())
        if not rows:
            raise RuntimeError(f"baostock 无数据: {symbol}")
        return {"symbol": symbol, "fields": ["date", "open", "high", "low", "close", "volume"], "rows": rows, "source": "baostock"}
    finally:
        bs.logout()


def run_market_quote(symbol, market_sources):
    norm = normalize_symbol(symbol)
    requested = list(market_sources)
    result = {"symbol": norm, "symbol_input": symbol, "timestamp": utc_now(), "type": "quote", "results": {}}
    for source in requested:
        if source == "eastmoney":
            result["results"][source] = safe_call(lambda: fetch_eastmoney_quote(norm))
        elif source == "yfinance":
            result["results"][source] = safe_call(lambda: fetch_yfinance_quote(norm))
        elif source == "akshare":
            result["results"][source] = safe_call(lambda: fetch_akshare_quote(norm))
        elif source == "tushare":
            result["results"][source] = safe_call(lambda: fetch_tushare_quote(norm))
        elif source == "pytdx":
            result["results"][source] = safe_call(lambda: fetch_pytdx_quote(norm))
        elif source == "baostock":
            result["results"][source] = safe_call(lambda: fetch_baostock_history(norm))
    if not any(x.get("ok") for x in result["results"].values()):
        for source in ["eastmoney", "yfinance"]:
            if source in requested:
                continue
            if source == "eastmoney":
                result["results"][source] = safe_call(lambda: fetch_eastmoney_quote(norm))
            elif source == "yfinance":
                result["results"][source] = safe_call(lambda: fetch_yfinance_quote(norm))
            if result["results"][source].get("ok"):
                result["fallback_source_used"] = source
                break
    return result


def run_market_history(symbol, market_sources, interval, range_):
    norm = normalize_symbol(symbol)
    requested = list(market_sources)
    result = {"symbol": norm, "symbol_input": symbol, "timestamp": utc_now(), "type": "history", "results": {}}
    for source in market_sources:
        if source == "yfinance":
            result["results"][source] = safe_call(lambda: fetch_yfinance_history(norm, interval=interval, range_=range_))
        elif source == "baostock":
            result["results"][source] = safe_call(lambda: fetch_baostock_history(norm))
        elif source in {"akshare", "tushare", "pytdx", "eastmoney"}:
            result["results"][source] = {"ok": False, "error": "该源历史查询需本地SDK高级配置后扩展"}
    if not any(x.get("ok") for x in result["results"].values()):
        if "yfinance" not in requested:
            result["results"]["yfinance"] = safe_call(lambda: fetch_yfinance_history(norm, interval=interval, range_=range_))
            if result["results"]["yfinance"].get("ok"):
                result["fallback_source_used"] = "yfinance"
    return result


def run_news_search(query, news_sources, max_results):
    requested = list(news_sources)
    result = {"query": query, "timestamp": utc_now(), "type": "news", "results": {}}
    for source in news_sources:
        if not is_news_source_configured(source):
            result["results"][source] = {"ok": False, "error": f"{source} 未配置，已跳过"}
            continue
        if source == "tavily":
            result["results"][source] = safe_call(lambda: fetch_tavily_news(query, max_results=max_results))
        elif source == "serpapi":
            result["results"][source] = safe_call(lambda: fetch_serpapi_news(query, max_results=max_results))
        elif source == "brave":
            result["results"][source] = safe_call(lambda: fetch_brave_news(query, max_results=max_results))
        elif source in {"bocha", "minimax"}:
            result["results"][source] = safe_call(lambda s=source: fetch_custom_news(s, query, max_results=max_results))
    if not any(x.get("ok") for x in result["results"].values()):
        if "local_fallback" not in requested:
            result["results"]["local_fallback"] = safe_call(lambda: fetch_local_fallback_news(query, max_results=max_results))
            if result["results"]["local_fallback"].get("ok"):
                result["fallback_source_used"] = "local_fallback"
    return result


def to_float(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    s = str(value).strip().replace(",", "")
    if not s:
        return None
    try:
        return float(s)
    except Exception:
        return None


def calc_ma(values, window):
    if len(values) < window:
        return None
    return sum(values[-window:]) / window


def extract_price(quote_data):
    for _, packet in quote_data.get("results", {}).items():
        if not packet.get("ok"):
            continue
        data = packet.get("data", {})
        for key in ["price", "close", "最新价"]:
            val = to_float(data.get(key))
            if val is not None:
                return val
    return None


def extract_close_series(history_data):
    for source, packet in history_data.get("results", {}).items():
        if not packet.get("ok"):
            continue
        data = packet.get("data", {})
        if source == "yfinance":
            rows = data.get("rows", [])
            closes = [to_float(r.get("close")) for r in rows]
            closes = [x for x in closes if x is not None]
            if closes:
                return closes, source
        if source == "baostock":
            rows = data.get("rows", [])
            closes = []
            for r in rows:
                if isinstance(r, list) and len(r) >= 5:
                    v = to_float(r[4])
                    if v is not None:
                        closes.append(v)
            if closes:
                return closes, source
    return [], ""


def analyze_strategy(strategy, price, closes, bias_threshold):
    if not closes and price is not None:
        closes = [price]
    latest = closes[-1] if closes else price
    ma5 = calc_ma(closes, 5)
    ma10 = calc_ma(closes, 10)
    ma20 = calc_ma(closes, 20)
    bias = None
    if latest is not None and ma20:
        bias = ((latest - ma20) / ma20) * 100
    strategy_used = strategy
    if strategy == "auto":
        strategy_used = "ma_trend"
    summary = []
    signals = []
    risk = "medium"
    action = "neutral"

    if strategy_used == "ma_cross":
        prev_ma5 = calc_ma(closes[:-1], 5) if len(closes) >= 6 else None
        prev_ma20 = calc_ma(closes[:-1], 20) if len(closes) >= 21 else None
        if ma5 and ma20 and prev_ma5 and prev_ma20:
            if prev_ma5 <= prev_ma20 and ma5 > ma20:
                signals.append("出现金叉")
                action = "bullish"
            elif prev_ma5 >= prev_ma20 and ma5 < ma20:
                signals.append("出现死叉")
                action = "bearish"
            else:
                signals.append("未出现新交叉")
        else:
            signals.append("历史数据不足，无法判断交叉")
        summary.append("均线交叉用于判断趋势切换")

    elif strategy_used == "ma_trend":
        if ma5 and ma10 and ma20:
            if ma5 > ma10 > ma20:
                signals.append("MA5>MA10>MA20，多头排列")
                action = "bullish"
                risk = "low"
            elif ma5 < ma10 < ma20:
                signals.append("MA5<MA10<MA20，空头排列")
                action = "bearish"
            else:
                signals.append("均线缠绕，趋势不清晰")
                action = "neutral"
        else:
            signals.append("历史数据不足，无法判断趋势排列")
        summary.append("趋势策略关注均线排列与方向一致性")

    elif strategy_used == "bias_guard":
        if bias is None:
            signals.append("数据不足，无法计算乖离率")
        else:
            signals.append(f"当前乖离率 {round(bias, 2)}%")
            if abs(bias) >= bias_threshold:
                signals.append("乖离率超过阈值，提示追高/杀跌风险")
                risk = "high"
            else:
                signals.append("乖离率在可接受区间")
                risk = "low"
        summary.append("乖离率策略用于风险控制而非单独买卖")

    elif strategy_used == "wave":
        if len(closes) >= 10:
            start = closes[-10]
            end = closes[-1]
            move = ((end - start) / start) * 100 if start else 0
            signals.append(f"近10周期波动 {round(move, 2)}%")
            if move > 6:
                action = "bullish"
                signals.append("推进段特征增强")
            elif move < -6:
                action = "bearish"
                signals.append("调整段特征增强")
            else:
                action = "neutral"
                signals.append("波段方向不明确")
        else:
            signals.append("历史数据不足，无法判断波段")
        summary.append("波浪近似策略用于识别推进/调整节奏")

    elif strategy_used == "cn_review":
        summary.append("A股三段式复盘：进攻/均衡/防守")
        if ma5 and ma10 and ma20 and ma5 > ma10 > ma20:
            action = "offense"
            risk = "medium"
            signals.append("趋势偏强，建议进攻计划")
        elif ma20 and latest and latest >= ma20:
            action = "balance"
            signals.append("趋势中性，建议均衡计划")
        else:
            action = "defense"
            risk = "high"
            signals.append("趋势偏弱，建议防守计划")
        if bias is not None and abs(bias) >= bias_threshold:
            risk = "high"
            signals.append("乖离率过高，降低追价意愿")

    elif strategy_used == "us_regime":
        summary.append("美股 Regime：risk-on/neutral/risk-off")
        if ma5 and ma20 and latest:
            if latest > ma20 and ma5 >= ma20:
                action = "risk-on"
                risk = "medium"
                signals.append("价格与短均线位于长均线上方")
            elif latest < ma20 and ma5 <= ma20:
                action = "risk-off"
                risk = "high"
                signals.append("价格与短均线位于长均线下方")
            else:
                action = "neutral"
                signals.append("市场处于过渡区间")
        else:
            action = "neutral"
            signals.append("数据不足，默认中性")

    else:
        strategy_used = "ma_trend"
        return analyze_strategy(strategy_used, price, closes, bias_threshold)

    return {
        "strategy_used": strategy_used,
        "signals": signals,
        "summary": "；".join(summary) if summary else "",
        "action": action,
        "risk_level": risk,
        "metrics": {"price": latest, "ma5": ma5, "ma10": ma10, "ma20": ma20, "bias_pct": bias},
        "disclaimer": "仅供参考，不构成投资建议。",
    }


def run_intel(symbol, query, market_sources, news_sources, max_results, interval, range_, mode="info", strategy="auto", bias_threshold=5.0):
    quote_data = run_market_quote(symbol, market_sources)
    history_data = run_market_history(symbol, market_sources, interval, range_)
    news_data = run_news_search(query or symbol, news_sources, max_results)
    output = {
        "symbol": symbol,
        "query": query or symbol,
        "timestamp": utc_now(),
        "type": "intel",
        "mode": mode,
        "quote": quote_data,
        "history": history_data,
        "news": news_data,
    }
    if mode == "strategy":
        price = extract_price(quote_data)
        closes, close_source = extract_close_series(history_data)
        output["strategy"] = analyze_strategy(strategy, price, closes, bias_threshold)
        output["strategy"]["data_basis"] = {"price_source": "quote_multi_source", "close_source": close_source or "none"}
    return output


def print_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def build_parser():
    parser = argparse.ArgumentParser(prog="market_intel", description="OpenClaw Market Intel 查询执行器")
    sub = parser.add_subparsers(dest="command", required=True)

    p_quote = sub.add_parser("quote", help="查询最新行情")
    p_quote.add_argument("--symbol", required=True)
    p_quote.add_argument("--sources", default=",".join(MARKET_SOURCES))

    p_history = sub.add_parser("history", help="查询历史K线")
    p_history.add_argument("--symbol", required=True)
    p_history.add_argument("--interval", default="1d")
    p_history.add_argument("--range", dest="range_", default="1mo")
    p_history.add_argument("--sources", default="yfinance,baostock")

    p_news = sub.add_parser("news", help="查询新闻与搜索")
    p_news.add_argument("--query", required=True)
    p_news.add_argument("--max-results", type=int, default=5)
    p_news.add_argument("--sources", default=",".join(NEWS_SOURCES))

    p_intel = sub.add_parser("intel", help="一键生成行情+新闻情报")
    p_intel.add_argument("--symbol", required=True)
    p_intel.add_argument("--query", default="")
    p_intel.add_argument("--interval", default="1d")
    p_intel.add_argument("--range", dest="range_", default="1mo")
    p_intel.add_argument("--max-results", type=int, default=5)
    p_intel.add_argument("--market-sources", default=",".join(MARKET_SOURCES))
    p_intel.add_argument("--news-sources", default=",".join(NEWS_SOURCES))
    p_intel.add_argument("--mode", choices=INTEL_MODES, default="info")
    p_intel.add_argument("--strategy", choices=STRATEGIES, default="auto")
    p_intel.add_argument("--bias-threshold", type=float, default=5.0)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "quote":
        sources, invalid = parse_sources(args.sources, MARKET_SOURCES)
        result = run_market_quote(args.symbol, sources)
        if invalid:
            result["invalid_sources"] = invalid
        print_json(result)
        return 0

    if args.command == "history":
        sources, invalid = parse_sources(args.sources, MARKET_SOURCES)
        result = run_market_history(args.symbol, sources, args.interval, args.range_)
        if invalid:
            result["invalid_sources"] = invalid
        print_json(result)
        return 0

    if args.command == "news":
        sources, invalid = parse_sources(args.sources, NEWS_SOURCES)
        result = run_news_search(args.query, sources, args.max_results)
        if invalid:
            result["invalid_sources"] = invalid
        print_json(result)
        return 0

    if args.command == "intel":
        m_sources, m_invalid = parse_sources(args.market_sources, MARKET_SOURCES)
        n_sources, n_invalid = parse_sources(args.news_sources, NEWS_SOURCES)
        result = run_intel(
            symbol=args.symbol,
            query=args.query,
            market_sources=m_sources,
            news_sources=n_sources,
            max_results=args.max_results,
            interval=args.interval,
            range_=args.range_,
            mode=args.mode,
            strategy=args.strategy,
            bias_threshold=args.bias_threshold,
        )
        if m_invalid:
            result["invalid_market_sources"] = m_invalid
        if n_invalid:
            result["invalid_news_sources"] = n_invalid
        print_json(result)
        return 0

    return 1


if __name__ == "__main__":
    start = time.time()
    code = main()
    elapsed = round(time.time() - start, 3)
    if code != 0:
        sys.exit(code)
    sys.stderr.write(f"done in {elapsed}s\n")
