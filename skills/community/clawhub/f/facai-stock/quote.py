"""个股实时行情获取与解析（数据来源：雪球 JSON API，token 本地缓存）"""

import json
import time

import requests

from market import add_prefix, strip_prefix
from search import search_by_name

_HERE = __import__("pathlib").Path(__file__).parent
_DATA_DIR = _HERE / "data"
_TOKEN_CACHE_PATH = _DATA_DIR / "xueqiu_token.json"
_TOKEN_TTL = 6 * 3600   # token 有效期：6 小时

_XQ_QUOTE_URL = "https://stock.xueqiu.com/v5/stock/quote.json"
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
}

# 内存缓存：避免进程内重复读文件
_cache: dict = {}   # {"session": requests.Session, "ts": float}


# ---------------------------------------------------------------------------
# Token / Session 管理
# ---------------------------------------------------------------------------

def _build_session(cookies: dict) -> requests.Session:
    sess = requests.Session()
    sess.headers.update(_HEADERS)
    sess.cookies.update(cookies)
    return sess


def _refresh_token() -> requests.Session:
    """访问雪球首页获取新 token，写入缓存文件，返回就绪的 Session。"""
    sess = requests.Session()
    sess.headers.update(_HEADERS)
    sess.get("https://xueqiu.com/", timeout=15)

    cookies = {k: v for k, v in sess.cookies.items()}
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    _TOKEN_CACHE_PATH.write_text(
        json.dumps({"ts": time.time(), "cookies": cookies}, ensure_ascii=False),
        encoding="utf-8",
    )
    _cache.update({"session": sess, "ts": time.time()})
    return sess


def _get_session(force_refresh: bool = False) -> requests.Session:
    """
    返回带有效 token 的 Session。
    优先级：内存缓存 → 文件缓存 → 重新获取。
    """
    now = time.time()

    if not force_refresh:
        # 1. 内存缓存
        if _cache.get("session") and now - _cache.get("ts", 0) < _TOKEN_TTL:
            return _cache["session"]

        # 2. 文件缓存
        if _TOKEN_CACHE_PATH.exists():
            try:
                data = json.loads(_TOKEN_CACHE_PATH.read_text(encoding="utf-8"))
                if now - data.get("ts", 0) < _TOKEN_TTL:
                    sess = _build_session(data["cookies"])
                    _cache.update({"session": sess, "ts": data["ts"]})
                    return sess
            except (json.JSONDecodeError, KeyError):
                pass

    # 3. 重新获取（访问雪球首页）
    return _refresh_token()


# ---------------------------------------------------------------------------
# 解析与查询
# ---------------------------------------------------------------------------

def _safe_float(val) -> float:
    try:
        return float(val) if val is not None else 0.0
    except (TypeError, ValueError):
        return 0.0


def _parse(q: dict, code: str) -> dict:
    """从雪球 quote 对象解析行情字典。"""
    volume = _safe_float(q.get("volume"))
    return {
        "代码": code,
        "名称": str(q.get("name", code)),
        "最新价": _safe_float(q.get("current")),
        "涨跌幅": _safe_float(q.get("percent")),       # 已是百分比，如 -1.56
        "涨跌额": _safe_float(q.get("chg")),
        "成交量": volume / 100,                         # 股 → 手
        "成交额": _safe_float(q.get("amount")),
        "今开": _safe_float(q.get("open")),
        "昨收": _safe_float(q.get("last_close")),
        "最高": _safe_float(q.get("high")),
        "最低": _safe_float(q.get("low")),
        "市盈率TTM": _safe_float(q.get("pe_ttm")),
        "总市值": _safe_float(q.get("market_capital")),
        "52周最高": _safe_float(q.get("high52w")),
        "52周最低": _safe_float(q.get("low52w")),
        "股息率TTM": _safe_float(q.get("dividend_yield")),
        "市净率": _safe_float(q.get("pb")),
    }


def get_detail(code: str) -> dict:
    """
    按6位股票代码查询实时行情详情。
    数据来源：雪球 JSON API，token 本地缓存（6小时有效）。
    首次调用需访问雪球首页获取 token（约 2-3 秒），后续 < 500ms。
    """
    code = strip_prefix(code)
    symbol = add_prefix(code)
    params = {"symbol": symbol, "extend": "detail"}

    sess = _get_session()
    resp = sess.get(_XQ_QUOTE_URL, params=params, timeout=5)

    if resp.status_code == 401:
        # token 失效，强制刷新后重试
        sess = _get_session(force_refresh=True)
        resp = sess.get(_XQ_QUOTE_URL, params=params, timeout=5)

    resp.raise_for_status()
    return _parse(resp.json()["data"]["quote"], code)


def get_detail_by_name(name: str) -> dict:
    """
    按股票名称关键字查询实时行情详情。
    - 唯一匹配时直接返回行情字典。
    - 多个匹配时抛出 ValueError，附带候选列表。
    - 无匹配时抛出 ValueError。
    """
    matches = search_by_name(name)
    if not matches:
        raise ValueError(f"未找到名称包含「{name}」的股票")
    if len(matches) > 1:
        candidates = "、".join(f"{s['name']}({s['code']})" for s in matches[:10])
        more = "，仅显示前10条" if len(matches) > 10 else ""
        raise ValueError(
            f"找到 {len(matches)} 只匹配股票{more}：{candidates}。请使用更精确的名称或直接传入代码。"
        )
    return get_detail(matches[0]["code"])
