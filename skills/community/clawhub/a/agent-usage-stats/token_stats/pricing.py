"""Model price loading and cost helpers."""

from __future__ import annotations

import os
import re
import sys

_USD_TO_CNY = 7.25
_model_prices_cache = None


def _parse_simple_toml(path: str) -> dict:
    """极简 TOML 解析器，仅支持 [section] + key = value（兼容 Python < 3.11）"""
    data = {}
    current_section = None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            line = re.sub(r'\s+#.*$', '', line)
            m = re.match(r'^\[(.+)\]$', line)
            if m:
                section = m.group(1).strip()
                if section.startswith('"') and section.endswith('"'):
                    section = section[1:-1]
                elif section.startswith("'") and section.endswith("'"):
                    section = section[1:-1]
                if section not in data:
                    data[section] = {}
                current_section = data[section]
                continue
            if "=" in line and current_section is not None:
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip()
                if val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                elif val.startswith("'") and val.endswith("'"):
                    val = val[1:-1]
                else:
                    try:
                        val = float(val)
                        if val == int(val):
                            val = int(val)
                    except ValueError:
                        pass
                current_section[key] = val
    return data


def load_model_prices(project_root: str, cwd: str | None = None) -> dict:
    """加载 model_prices.toml，失败返回 {}。结果缓存。"""
    global _model_prices_cache
    if _model_prices_cache is not None:
        return _model_prices_cache
    candidates = [
        os.path.join(project_root, "model_prices.toml"),
        os.path.join(cwd or os.getcwd(), "model_prices.toml"),
    ]
    for cp in candidates:
        if os.path.isfile(cp):
            try:
                if sys.version_info >= (3, 11):
                    import tomllib
                    with open(cp, "rb") as f:
                        data = tomllib.load(f)
                else:
                    data = _parse_simple_toml(cp)
            except Exception:
                data = {}
            _model_prices_cache = data
            return data
    _model_prices_cache = {}
    return {}


def get_model_price(model: str, prices: dict) -> dict | None:
    """获取指定模型的价格配置。先精确匹配，再前缀匹配"""
    if not prices:
        return None
    if model in prices:
        return prices[model]
    for key in sorted(prices.keys(), key=lambda k: -len(k)):
        if model.startswith(key):
            return prices[key]
    return None


def calc_cost(inp: int, out: int, cache: int, price: dict) -> float:
    """计算预估费用。自适应缓存模型：cache>inp 时 inp=cacheMiss，否则 inp 含 cacheHit"""
    if cache > inp:
        no_cache = inp
        cache_tokens = cache
    else:
        no_cache = inp - cache
        cache_tokens = cache
    return (no_cache * price.get("input_no_cache_price", 0) +
            cache_tokens * price.get("input_cache_price", 0) +
            out * price.get("output_price", 0)) / 1_000_000


def to_cny(cost: float, currency: str) -> float:
    """将费用统一转为人民币"""
    return cost * _USD_TO_CNY if currency == "USD" else cost


def fmt_cost(inp: int, out: int, cache: int, price: dict) -> str:
    """格式化预估费用，统一为人民币"""
    total = to_cny(calc_cost(inp, out, cache, price), price.get("currency", "CNY"))
    return f"≈¥{total:.2f}"


def calc_total_cost(per_model_list: list, get_price) -> dict[str, float]:
    """计算 per_model 列表中所有有价格模型的费用总和。返回 {currency: cost}"""
    totals: dict[str, float] = {}
    for pm in (per_model_list or []):
        if pm.get("token_mode") == "total":
            continue
        pc = get_price(pm.get("model", ""))
        if pc:
            inp = pm.get("input", 0) or 0
            out = pm.get("output", 0) or 0
            cache = pm.get("cache", 0) or 0
            cur = pc.get('currency', 'CNY')
            totals[cur] = totals.get(cur, 0.0) + calc_cost(inp, out, cache, pc)
    return totals


def fmt_total_cost(totals: dict[str, float]) -> str:
    """格式化总费用，统一转人民币。eg: ≈¥87.29"""
    if not totals:
        return ""
    total_cny = totals.get("CNY", 0.0) + totals.get("USD", 0.0) * _USD_TO_CNY
    if total_cny <= 0:
        return ""
    return f"≈¥{total_cny:.2f}"
