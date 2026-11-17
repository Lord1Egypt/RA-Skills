#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C5 公开证据基准 — coze 引擎侧采纳解析器（v5.13.32）。

定位：coze 计算节点在调用 R 引擎之前，用本模块把前端传来的
`effect_ref`（基准 JSON 字符串）+ `adopt_ref`（采纳模式）解析、校验、聚合、
兼容性检查，并把采纳值写入 params 对应键，使 R 引擎按采纳后的效应量计算。

设计红线（与 scripts/effect_ref.py 头部一致，2026-10-14 与用户确认）：
  - 数据仅来自公开已发表荟萃（用户自带），绝不连接商业策展数据库；
  - **默认仅展示、绝不静默代入**：仅当 adopt_ref 为具体模式（median/conservative/
    low/high/<index>）时才代入；off/display/none/空 → 返回 None（只展示，不代入）；
  - 尺度/终点不符（参考是 HR、当前是连续终点等）拒绝采纳，只允许展示；
  - 采纳来源写入输出（可审计）：调用方负责把 adopted 信息落入结果信封。

本模块**无平台依赖**（仅标准库 + effect_ref），可被 coze 节点直接 import，
也可被独立测试 harness 直接 import 验证，无需 langchain/langgraph 等 coze 运行时。
"""
import json
import types

from effect_ref import validate, pick, compatible, TARGET_ARG


# adopt_ref 取这些值时视为「仅展示、不代入」
_DISPLAY_ONLY = ("off", "display", "none", "false", "")


def _normalize_ref_json(raw):
    """统一化前端传来的 effect_ref：兼容三种形式 → {references:[...]}。

    支持：JSON 数组、{references:[...]} 对象、单条 {estimate:...} 对象。
    返回 (data, None) 或 (None, err_msg)。
    """
    if isinstance(raw, str):
        try:
            data = json.loads(raw)
        except Exception as e:
            return None, "effect_ref JSON 解析失败：%s" % e
    else:
        data = raw
    if isinstance(data, list):
        return {"references": data}, None
    if isinstance(data, dict):
        if isinstance(data.get("references"), list):
            return data, None
        if isinstance(data.get("estimate"), (int, float)):
            return {"references": [data]}, None
    return None, "effect_ref 需为 references 数组、或含 estimate 的单条对象"


def resolve_effect_ref(test, params):
    """解析并（必要时）代入公开证据基准。

    入参：
      test   : 当前检验名（如 ttest_ind / survival_...）
      params : 计算参数 dict（**会被原地修改**：成功时写入采纳值）
    返回（三态）：
      None                          —— 无需采纳（缺字段 / adopt_ref 为仅展示值）
      {"adopted": {...}, "warnings": [...]}  —— 成功代入，params 已被改写
      {"error": "..."}              —— 校验/聚合/兼容失败（未代入）
    """
    eff = params.get("effect_ref")
    adopt = params.get("adopt_ref")
    if not eff or not adopt:
        return None
    if str(adopt).strip().lower() in _DISPLAY_ONLY:
        return None

    data, err = _normalize_ref_json(eff)
    if err:
        return {"error": err}

    clean, errors, warnings = validate(data)
    if errors:
        return {"error": "公开证据基准校验失败：" + "；".join(errors[:5])}

    adopted, perr = pick(clean, adopt)
    if perr:
        return {"error": "采纳失败：" + perr}

    # compatible 仅用 sd 属性（MD 尺度需 sd 折算 d）
    ok, reason = compatible(adopted, test, types.SimpleNamespace(sd=params.get("sd")))
    if not ok:
        return {"error": "采纳被拒：" + reason}

    target = TARGET_ARG.get(adopted["param"], "effect")
    params[target] = adopted["value"]
    return {"adopted": adopted, "warnings": warnings}
