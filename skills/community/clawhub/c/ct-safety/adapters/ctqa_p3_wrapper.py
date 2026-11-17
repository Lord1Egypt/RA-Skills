#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ct-safety · P3 出站构造 wrapper（ct-base §27.6 条 6）。

**为什么需要 wrapper**：本技能的出站 payload 是在 `coze_dispatch.dispatch()` **内部**
拼装的（药名/事件词翻译 → payload dict → billing → coze 契约注入），没有独立的
`build_payload()` 函数供 P3 调用。

**为什么不复制一份构造逻辑**：复制即漂移——SSE 快速路径、billing、coze 契约任一侧改动，
副本会立刻失真，而 P3 的意义正是守住**真实**出站链路。

**做法**：以 `run=False` 调 `dispatch()`（SAFE PREVIEW：只打印 payload、零网络 I/O），
从 `[PREVIEW] … payload={...}` 行回收真实 payload 并解析成 dict。
这样 P3 的占位符 / 字面量 / env 污染 / 脱敏 / 幂等五项检查作用在生产同一份构造代码上。

**零出站前提**：`dispatch(run=False)` 在拼装完成后即返回，不发任何 HTTP。
采样输入用英文 INN/事件词，避免触发中文→英文的在线翻译兜底。
"""
from __future__ import annotations

import contextlib
import copy
import io
import json
import os
import re
import sys

_ADAPTERS_DIR = os.path.dirname(os.path.abspath(__file__))
if _ADAPTERS_DIR not in sys.path:
    sys.path.insert(0, _ADAPTERS_DIR)

_PREVIEW_RE = re.compile(r"payload=(\{.*?\})\s*\(no network", re.S)


def build_payload(env: dict):
    """P3 入口：dict -> 真实 dispatch(run=False) -> 出站 payload dict。"""
    import coze_dispatch

    e = copy.deepcopy(env or {})
    source = e.get("source") or "faers"
    drug = e.get("drug") or ""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        coze_dispatch.dispatch(
            source, drug,
            event=e.get("event"),
            date_from=e.get("date_from"),
            date_to=e.get("date_to"),
            run=False,                       # SAFE PREVIEW：零出站
            out=None,
            token=e.get("token"),
            endpoint=e.get("endpoint"),
            account_id=e.get("account_id"),
            billing_token=e.get("billing_token"),
            extra=e.get("extra"),
        )
    m = _PREVIEW_RE.search(buf.getvalue())
    if not m:
        raise RuntimeError("未从 dispatch 预览输出中回收到 payload；stdout=%r"
                           % buf.getvalue()[:400])
    return json.loads(m.group(1))


def sanitize(payload):
    """P3 脱敏入口：复用出站真实脱敏实现（nmpa_coze._sanitize）。"""
    import nmpa_coze
    return nmpa_coze._sanitize(payload)
