#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ct-registry · P3 出站构造 wrapper（ct-base §27.6 条 6）。

**为什么需要 wrapper**：P3 需要一个签名是 `build_payload(env: dict) -> dict` 的独立函数，
而本技能的出站构造是 `search_ictrp.build_payload(args)`，吃的是 argparse Namespace
（内部直接 `args.q` / `args.who_*`，缺属性即 AttributeError）。
wrapper 负责：① 用「全量默认 Namespace」兜底所有被访问的属性；② 用 P3 传入的 env 覆盖；
③ 返回 build_payload 的结果。这样 P3 的占位符 / 字面量 / env 污染 / 脱敏 / 幂等五项
检查才能作用到真实出站链路上。

**零出站**：只做 dict 构造，不发任何网络请求。
"""
from __future__ import annotations

import argparse
import copy
import os
import sys

_ADAPTERS_DIR = os.path.dirname(os.path.abspath(__file__))
if _ADAPTERS_DIR not in sys.path:
    sys.path.insert(0, _ADAPTERS_DIR)

# `search_ictrp.py` 中被 `args.<x>` 访问的全部属性（缺一个就 AttributeError）。
# 值取 CLI 默认语义：字符串类 None、开关类 False、数值类取默认值。
_BASE_ARGS = {
    "q": None,
    "cond": None,
    "intr": None,
    "sponsor": None,
    "status": None,
    "mode": "search",
    "source": "who",
    "who_title": None,
    "who_title_operator": None,
    "who_condition": None,
    "who_intervention": None,
    "who_intervention_operator": None,
    "who_sponsor": None,
    "who_country": None,
    "who_phase": None,
    "who_recruitment_status": None,
    "who_secondary_id": None,
    "who_date_start": None,
    "who_date_end": None,
    "multi_keywords": None,
    "project_list": None,
    "page_start": 1,
    "max_pages": 1,
    "max": 20,
    "fetch_mode": "search",
    "stream": False,
    "run": False,
    "auto_confirm": False,
    "out": "ctqa_p3_out.json",
    "timeout": 600,
    "token": None,
    "endpoint": "https://api.coze.cn/v1/workflows/ct-registry/run",
    "demand_id": None,
    "fallback_keyword": None,
}


def build_payload(env: dict):
    """P3 入口：dict -> argparse.Namespace -> 真实出站 payload。"""
    import search_ictrp

    merged = dict(_BASE_ARGS)
    merged.update(env or {})
    # 深拷贝：P3 会断言「构造过程不就地修改调用方 env」，Namespace 不得反向写回 dict
    args = argparse.Namespace(**copy.deepcopy(merged))
    return search_ictrp.build_payload(args)


def sanitize(payload):
    """P3 脱敏入口：复用出站真实脱敏实现（extsvc_client._sanitize_payload）。"""
    import extsvc_client
    return extsvc_client._sanitize_payload(payload)
