#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L2 声明式通用适配器：从 config/adapter_rules.json 动态生成适配器。

同事遇到新 Agent 时，只需在 config/local/adapter_rules.local.json 里加一条规则，
无需写 Python。规则格式见 config/adapter_rules.example.json。

本文件定义一个 GenericAdapter 实例列表（模块级 ALL），由 extract_tasks.py /
stat_tokens.py 合并进 discover() 的结果。为保持 discover() 纯净，这里提供
get_dynamic_adapters() 供调度脚本显式调用。
"""
import os, json
from ._declarative import DeclarativeAdapter
from .base import ROOT

RULES_PATHS = [
    os.environ.get("WORKLOG_ADAPTER_RULES", ""),
    os.path.join(ROOT, "config", "local", "adapter_rules.local.json"),
    os.path.join(ROOT, "config", "adapter_rules.json"),
]


def load_rules():
    for p in RULES_PATHS:
        if not p or not os.path.isfile(p):
            continue
        try:
            d = json.load(open(p, encoding="utf-8"))
            rules = d.get("rules") if isinstance(d, dict) else d
            if isinstance(rules, list):
                return [r for r in rules if isinstance(r, dict) and r.get("name")]
        except Exception:
            pass
    return []


def _make_class(rule):
    """根据规则动态生成一个 DeclarativeAdapter 子类。"""
    attrs = {
        "name": str(rule.get("name")),
        "dir_patterns": tuple(rule.get("dir_patterns") or ()),
        "file_globs": tuple(rule.get("file_globs") or ("*.jsonl",)),
        "data_style": str(rule.get("data_style") or "jsonl"),
        "token_spec": rule.get("token_spec") or None,
        "verified": bool(rule.get("verified", False)),
        "verification_note": rule.get("verification_note", ""),
    }
    for k in ("role_keys", "user_values", "text_keys"):
        if k in rule:
            attrs[k] = tuple(rule[k])
    return type("Dynamic_" + str(rule["name"]).replace(" ", "_"), (DeclarativeAdapter,), attrs)


def get_dynamic_adapters():
    out = []
    for rule in load_rules():
        try:
            out.append(_make_class(rule)())
        except Exception as e:
            print(f"  [generic] 规则 {rule.get('name')} 加载失败: {str(e)[:80]}")
    return out
