"""自选股管理：增删查清，持久化到 watchlist.json。"""

import json
from pathlib import Path

from market import is_valid_code, strip_prefix
from quote import get_detail, get_detail_by_name

_DATA_DIR = Path(__file__).parent / "data"
WATCHLIST_PATH = _DATA_DIR / "watchlist.json"


# ---------------------------------------------------------------------------
# 文件读写
# ---------------------------------------------------------------------------

def _load() -> list[dict]:
    if not WATCHLIST_PATH.exists():
        return []
    try:
        return json.loads(WATCHLIST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def _save(stocks: list[dict]) -> None:
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    WATCHLIST_PATH.write_text(
        json.dumps(stocks, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _monitor_status() -> str:
    from monitor import is_running
    return "监控已启动" if is_running() else "监控未启动"


# ---------------------------------------------------------------------------
# 公开 API
# ---------------------------------------------------------------------------

def list_all() -> list[dict]:
    """返回完整自选股列表：[{"code": "000001", "name": "平安银行"}, ...]"""
    return _load()


def add(query: str) -> dict:
    """
    添加自选股。query 可以是6位股票代码或名称（须精确匹配唯一股票）。
    返回已添加的股票信息（含 monitor_status 字段）；若已在列表中则直接返回。
    """
    stocks = _load()

    if is_valid_code(query):
        code = strip_prefix(query)
        detail = get_detail(code)
    else:
        detail = get_detail_by_name(query)
        code = detail["代码"]

    name = detail["名称"]

    if not any(s["code"] == code for s in stocks):
        stocks.append({"code": code, "name": name})
        _save(stocks)

    return {"code": code, "name": name, "monitor_status": _monitor_status()}


def remove(query: str) -> dict | None:
    """
    删除自选股。query 可以是6位代码或名称（精确匹配）。
    返回被删除的股票信息（含 monitor_status 字段）；未找到返回 None。
    """
    stocks = _load()

    if is_valid_code(query):
        code = strip_prefix(query)
        target = next((s for s in stocks if s["code"] == code), None)
    else:
        target = next((s for s in stocks if s["name"] == query), None)

    if target is None:
        return None

    stocks = [s for s in stocks if s["code"] != target["code"]]
    _save(stocks)
    return {**target, "monitor_status": _monitor_status()}


def clear() -> dict:
    """
    清空自选股列表。
    返回 {"cleared": N, "monitor_status": "..."}。
    """
    stocks = _load()
    count = len(stocks)
    if count:
        _save([])
    return {"cleared": count, "monitor_status": _monitor_status()}
