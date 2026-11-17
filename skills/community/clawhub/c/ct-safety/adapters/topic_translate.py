#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""topic_translate.py — 中文检索词 → 英文检索词（供 FAERS 检索自动翻译）。

WHY THIS EXISTS
---------------
FAERS（openFDA）仅索引英文报告；把中文药物名/事件词原样送去检索必然 0 命中。
在**技能（Agent）上下文**里 LLM 在回路中，翻译是天然能力；但网页端（workbench）
是独立进程，Agent 不在回路里，用户此前只能依赖「中文药物名 / 中文事件词」专用字段——
而 ``wb-f-drug`` / ``wb-f-event`` 主输入框里的中文不会触发翻译。

翻译策略（对齐 ct-base/references/keyword_expand.md §9.1 两阶段翻译规范）
--------------------------------------------------------------------
阶段1: 本地词表（确定性、零网络、可审计）
  - ``drug_name_resolver.lookup()`` → 486 条权威 INN/通用名映射
  - ``kw_localize.localize_with_fallback()`` → term_map + _EXTRA + online
阶段2: 在线兜底（MyMemory → Google gtx，keyless，零密钥外发）
  - 复用 ``kw_localize.online_translate()``

设计约束
--------
- **零第三方依赖**：只用标准库（urllib / json / hashlib / os / re / time）。
- **不臆造、可核对**：翻译结果回传给前端展示，用户可改。
- **失败即降级**：任何异常 → None，调用方回退到原词（不阻塞流程）。
- **缓存**：同一词只翻一次（进程内 + 磁盘），省 token、避限流。
- **幂等**：多次调用同一词结果一致。
"""
import hashlib
import json
import os
import re
import sys
import time

# ── 路径常量 ───────────────────────────────────────────────────────────
_ADAPTER_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_DIR = os.path.dirname(_ADAPTER_DIR)
_WORKBENCH_DIR = os.path.join(_SKILL_DIR, "workbench")
_TRANSLATE_CACHE = os.path.join(_WORKBENCH_DIR, "translate_cache.json")

# ── 常量 ───────────────────────────────────────────────────────────────
_MAX_INPUT = 600


def _has_cjk(text):
    """True 若 text 含中日韩（CJK）字符。"""
    if not text:
        return False
    return bool(re.search(r"[\u3400-\u9fff\uf900-\ufaff\uff00-\uffef\u3040-\u30ff]", text))


# ── 本地词表查询 ──────────────────────────────────────────────────────
def _local_drug_lookup(text):
    """用 drug_name_resolver 查本地 486 条词表。有返回英文名列表，无返回 None。"""
    try:
        if _SKILL_DIR not in sys.path:
            sys.path.insert(0, _SKILL_DIR)
        from scripts.drug_name_resolver import lookup
        candidates = lookup(text)
        if candidates and isinstance(candidates, list) and candidates[0]:
            return candidates[0]
    except Exception:
        pass
    return None


def _kw_localize(text, target_lang="en"):
    """用 kw_localize 翻译（含 online fallback）。成功返回 (result, source)，失败返回 (None, 'miss')。"""
    try:
        if _SKILL_DIR not in sys.path:
            sys.path.insert(0, _SKILL_DIR)
        from scripts.kw_localize import localize_with_fallback
        result, source = localize_with_fallback(text, target_lang)
        if result and result != text and not _has_cjk(result):
            return result, source
    except Exception:
        pass
    return None, "miss"


# ── 缓存读写 ──────────────────────────────────────────────────────────
def _load_cache():
    try:
        with open(_TRANSLATE_CACHE, "r", encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def _save_cache(cache):
    try:
        os.makedirs(os.path.dirname(_TRANSLATE_CACHE), exist_ok=True)
        with open(_TRANSLATE_CACHE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


_MEM_CACHE = {}


def _cache_key(text):
    return hashlib.sha1(text.strip().encode("utf-8")).hexdigest()


def _looks_valid_english(s):
    """输出必须真像英文检索式：非空、有拉丁字母、无 CJK、不是拒答。"""
    if not s or len(s) < 2 or len(s) > 300:
        return False
    if _has_cjk(s):
        return False
    if not re.search(r"[A-Za-z]{2,}", s):
        return False
    low = s.lower()
    for bad in ("sorry", "cannot", "can't", "unable", "as an ai"):
        if low.startswith(bad):
            return False
    return True


# ── 公开 API ───────────────────────────────────────────────────────────
def translate_term(text, target="en", use_cache=True):
    """把中文检索词翻成英文检索式（对齐 ct-base §9.1 两阶段翻译规范）。

    Args:
        text: 待翻译的检索词（药物名或事件词）。
        target: 目标语言（默认 'en'；FAERS 场景固定 zh→en）。
        use_cache: 是否使用缓存。

    Returns:
        dict: {
            "source": "local_map" | "kw_localize" | "none",
            "text": 原始词,
            "translated": 英文结果 or None,
            "from": "zh" | "en",
            "to": target,
            "found": True/False,
            "note": 人类可读说明,
        }
    """
    t = (text or "").strip()
    if not t:
        return {"source": "none", "text": text, "translated": None,
                "from": "en", "to": target, "found": False, "note": "empty input"}

    # 已是英文 → 无需翻译
    if not _has_cjk(t):
        return {"source": "none", "text": t, "translated": None,
                "from": "en", "to": target, "found": False, "note": "already English"}

    if len(t) > _MAX_INPUT:
        return {"source": "none", "text": t, "translated": None,
                "from": "zh", "to": target, "found": False, "note": "input too long"}

    ck = _cache_key(t)
    if use_cache and ck in _MEM_CACHE:
        return _MEM_CACHE[ck]

    if use_cache:
        cache = _load_cache()
        hit = cache.get(ck)
        if hit and _looks_valid_english(hit.get("translated") or ""):
            _MEM_CACHE[ck] = hit
            return hit

    # ── 阶段1a: drug_name_resolver 本地词表 ─────────────────────────────
    local_result = _local_drug_lookup(t)
    if local_result and _looks_valid_english(local_result):
        result = {"source": "local_map", "text": t, "translated": local_result,
                  "from": "zh", "to": target, "found": True,
                  "note": f"auto-translated for {target} sources (local drug map)"}
        _MEM_CACHE[ck] = result
        if use_cache:
            cache = _load_cache()
            cache[ck] = result
            _save_cache(cache)
        return result

    # ── 阶段1b + 2: kw_localize（term_map + _EXTRA + online fallback）──
    kw_result, kw_source = _kw_localize(t, target)
    if kw_result and _looks_valid_english(kw_result):
        result = {"source": "kw_localize", "text": t, "translated": kw_result,
                  "from": "zh", "to": target, "found": True,
                  "note": f"auto-translated for {target} sources (kw_localize: {kw_source})"}
        _MEM_CACHE[ck] = result
        if use_cache:
            cache = _load_cache()
            cache[ck] = result
            _save_cache(cache)
        return result

    # 全部失败 → 不翻译，回退原词
    result = {"source": "none", "text": t, "translated": None,
              "from": "zh", "to": target, "found": False,
              "note": "translation failed; English sources may return 0 hits"}
    return result


def translate_drug_name(text):
    """翻译药物名（兼容旧接口）。返回英文串或 None。"""
    return translate_term(text).get("translated")


def translate_event_term(text):
    """翻译事件词（兼容旧接口）。返回英文串或 None。"""
    return translate_term(text).get("translated")


# ── CLI 自测 ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys as _sys
    arg = " ".join(_sys.argv[1:]) or "奥希替尼"
    print("input :", arg)
    import pprint
    pprint.pprint(translate_term(arg, use_cache=False))
