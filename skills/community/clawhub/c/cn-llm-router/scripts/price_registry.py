"""价格档案本地化（v2.7.0 新增）。

从 models.yaml 加载各厂商主力模型基准价（含采集日期），
提供价格查询、缓存、与实测价格对比能力。
纯标准库、零密钥、零联网。
"""

import os
import sys
import json
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import yaml_simple

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS_YAML = os.path.join(HERE, "..", "references", "models.yaml")

# 内存缓存
_cache = None
_cache_ts = 0
CACHE_TTL = 300  # 5 分钟缓存


def load_pricing(force=False):
    """加载 models.yaml 中的价格档案。
    
    返回 dict: { model_name: { "in": float, "out": float, "date": str, "source": str } }
    """
    global _cache, _cache_ts
    if not force and _cache and (time.time() - _cache_ts) < CACHE_TTL:
        return _cache

    reg = yaml_simple.load_file(MODELS_YAML)
    pricing = {}
    for provider, pinfo in reg.get("providers", {}).items():
        # v2.7.0: priced_at 在 provider 层级
        provider_date = pinfo.get("priced_at", "")
        provider_source = pinfo.get("price_source", "")
        for m in pinfo.get("models", []):
            name = m.get("name")
            if not name:
                continue
            entry = {
                "in": float(m.get("price_in", 0) or 0),
                "out": float(m.get("price_out", 0) or 0),
                "date": provider_date,
                "source": provider_source,
                "provider": provider,
            }
            pricing[name] = entry

    _cache = pricing
    _cache_ts = time.time()
    return pricing


def get_model_price(model_name):
    """查询单个模型的价格档案。
    
    返回 dict 或 None。
    """
    pricing = load_pricing()
    return pricing.get(model_name)


def estimate_cost(model_name, in_tokens, out_tokens):
    """按档案价估算花费。
    
    返回 float（元）。档案缺失返回 0.0。
    """
    p = get_model_price(model_name)
    if not p:
        return 0.0
    return round(
        in_tokens / 1_000_000 * p["in"] + out_tokens / 1_000_000 * p["out"],
        6,
    )


def all_prices():
    """返回全部价格档案（供报表/检测用）。"""
    return load_pricing()


def get_stale_models(days=30):
    """返回超过 days 天未更新价格的模型列表。
    
    用于提醒用户更新档案。
    """
    pricing = load_pricing()
    stale = []
    now = time.time()
    for name, info in pricing.items():
        date_str = info.get("date", "")
        if not date_str:
            stale.append({"name": name, "reason": "无采集日期"})
            continue
        try:
            # 简单日期解析 YYYY-MM-DD
            parts = date_str.split("-")
            if len(parts) == 3:
                year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
                ts = time.mktime((year, month, day, 0, 0, 0, 0, 0, -1))
                if now - ts > days * 86400:
                    stale.append({"name": name, "date": date_str, "reason": f"超过 {days} 天未更新"})
        except (ValueError, OverflowError):
            stale.append({"name": name, "date": date_str, "reason": "日期格式异常"})
    return stale
