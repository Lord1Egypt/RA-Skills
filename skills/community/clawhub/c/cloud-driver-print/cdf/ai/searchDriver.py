from __future__ import annotations

import json
import re
from typing import Any
from urllib import error, request

from cdf.ai.config import SEARCH_DRIVER_URL
DEFAULT_TIMEOUT = 30


def guess_model(user_text: str) -> str:
    """从用户输入中提取更像型号的片段，用于提升模糊搜索命中率。"""
    cleaned = re.sub(r"\s+", " ", user_text.strip())
    match = re.search(r"([A-Za-z]{1,10}[- ]?[A-Za-z0-9]{2,}(?:[- ][A-Za-z0-9]{2,})*)", cleaned)
    return match.group(1).strip() if match else cleaned


def _build_driver_url() -> str:
    """返回驱动查询接口地址。"""
    base_url = SEARCH_DRIVER_URL.strip()
    if not base_url:
        raise RuntimeError("未配置驱动查询接口地址。")
    return base_url


def _post_json(model: str, timeout: int = DEFAULT_TIMEOUT) -> Any:
    """以 JSON 方式提交 model 参数并解析响应。"""
    body = json.dumps({"model": model}, ensure_ascii=False).encode("utf-8")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=utf-8",
    }
    req = request.Request(_build_driver_url(), data=body, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"驱动搜索接口返回 HTTP {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"驱动搜索接口调用失败: {exc}") from exc
    return json.loads(raw) if raw else {}


def _normalize_driver_item(item: dict[str, Any], query: str, guessed_model: str) -> dict[str, object]:
    """将云端返回字段规范化为技能内部使用的统一结构。"""
    driver = str(item.get("driver", "")).strip()
    manufacturer = str(item.get("manufacturer", "")).strip()
    product = str(item.get("product", "")).strip()
    match_level = str(item.get("matchLevel", "")).strip().upper()
    installed = item.get("installed")
    desc = str(item.get("desc", "")).strip()
    matched_text = product or guessed_model or query
    score_map = {"EXACT": 1.0, "LIKELY": 0.7, "NONE": 0.0}
    return {
        "driver": driver,
        "score": score_map.get(match_level, 0.0),
        "matched_text": matched_text,
        "manufacturer": manufacturer,
        "product": product,
        "match_level": match_level,
        "installed": installed,
        "desc": desc,
    }


def _extract_items(response: Any) -> list[dict[str, Any]]:
    """兼容对象、数组以及包裹型响应。"""
    if isinstance(response, list):
        return [item for item in response if isinstance(item, dict)]
    if isinstance(response, dict):
        if "results" in response and isinstance(response["results"], list):
            return [item for item in response["results"] if isinstance(item, dict)]
        if "data" in response and isinstance(response["data"], list):
            return [item for item in response["data"] if isinstance(item, dict)]
        if "driver" in response or "product" in response or "manufacturer" in response:
            return [response]
    raise RuntimeError("驱动搜索接口返回格式不正确，无法解析驱动候选。")


def search_driver(query: str, guessed_model: str, limit: int = 5) -> list[dict[str, object]]:
    """调用云端 JSON 接口搜索驱动候选列表。"""
    model = guessed_model.strip() or query.strip()
    response = _post_json(model)
    items = _extract_items(response)
    normalized = [_normalize_driver_item(item, query=query, guessed_model=guessed_model) for item in items]
    return normalized[:limit]
