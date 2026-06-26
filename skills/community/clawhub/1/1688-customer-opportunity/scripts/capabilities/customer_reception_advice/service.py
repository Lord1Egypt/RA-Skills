import os
import sys
import json
import re

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _http import api_post

BATCH_SIZE = 40  # 单次请求最多 40 个买家，超出自动分批串行调用


def _clean_tpp_text(text: str) -> str:
    """清除 TPP [p]/[/p] 标注:[p] 去掉,[/p] 换成换行,去除多余空行"""
    if not text:
        return text
    text = re.sub(r'\[p\]', '', text)
    text = re.sub(r'\[/p\]', '\n', text)
    text = re.sub(r'\n{2,}', '\n', text)
    return text.strip()


def _extract_results(data: dict) -> list:
    """BotTool 返回格式有两层 data,取 data.data.results,并清洗文本"""
    inner = data.get("data") if isinstance(data.get("data"), dict) else data
    results = inner.get("results") or []
    for r in results:
        if r.get("buyer_profile"):
            r["buyer_profile"] = _clean_tpp_text(r["buyer_profile"])
        if r.get("follow_suggestion"):
            r["follow_suggestion"] = _clean_tpp_text(r["follow_suggestion"])
    return results


def _call_single_batch(batch: list) -> dict:
    """单批调用（≤ BATCH_SIZE），返回扁平 dict。"""
    body = {"buyers": json.dumps(batch, ensure_ascii=False)}
    data = api_post("/api/newton_customer_reception_advice/1.0.0", body)
    inner = data.get("data") if isinstance(data.get("data"), dict) else data
    return {
        "results": _extract_results(data),
        "unresolved_login_ids": inner.get("unresolved_login_ids") or [],
        "unresolved_phones": inner.get("unresolved_phones") or [],
        "invalid_entries": inner.get("invalid_entries") or [],
    }


def customer_reception_advice(buyers: list) -> dict:
    """统一入口：buyers 对象数组 → 画像 + 跟进建议。

    每个对象通过字段名声明类型：
        [{"login_id": "abc"}, {"phone": "13800138000"}, {"login_id": "def"}]

    Java 侧负责字段识别 → userId 解析（一手机号可能多账号会拆多条结果）。

    超过 BATCH_SIZE 时自动按 40/批 串行调用并合并结果，agent 一次传 N 个买家即可。

    Returns:
        dict 含 results / unresolved_login_ids / unresolved_phones / invalid_entries / batch_count
    """
    if not buyers:
        raise ValueError("buyers 不能为空")
    if not isinstance(buyers, list):
        raise ValueError("buyers 必须是对象数组")
    for idx, b in enumerate(buyers):
        if not isinstance(b, dict):
            raise ValueError(f"buyers[{idx}] 必须是对象 {{login_id|phone: '...'}}")
        if not (b.get("login_id") or b.get("phone")):
            raise ValueError(f"buyers[{idx}] 必须含 login_id 或 phone 字段")

    batches = [buyers[i:i + BATCH_SIZE] for i in range(0, len(buyers), BATCH_SIZE)]
    merged = {
        "results": [],
        "unresolved_login_ids": [],
        "unresolved_phones": [],
        "invalid_entries": [],
        "batch_count": len(batches),
        "total_input": len(buyers),
    }
    for batch in batches:
        part = _call_single_batch(batch)
        merged["results"].extend(part["results"])
        merged["unresolved_login_ids"].extend(part["unresolved_login_ids"])
        merged["unresolved_phones"].extend(part["unresolved_phones"])
        merged["invalid_entries"].extend(part["invalid_entries"])
    return merged
