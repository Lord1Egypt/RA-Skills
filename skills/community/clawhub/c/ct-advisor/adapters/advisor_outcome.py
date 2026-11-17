# -*- coding: utf-8 -*-
"""回传落库适配器（2026-11-11 Fix B）

本地在产出**真实答案 + 调用方法**后，回调 Coze 的 `/advisor_outcome` 端点，由云端 upsert
权威 advisorlog 记录（替换 handoff 路径下空/非实质的路由记录），落实「日志留下实质性回答
与调用方法」。

设计约束（与 entry.py HARD GATE 一致）：出站逻辑统一下沉到本 adapters/ 目录，entry.py 只调用，
不含任何 urllib 出站代码。本适配器 best-effort、零阻断：任何异常 / 超时均吞掉并返回 False，
绝不阻塞或影响答案交付。
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path
import sys

# 确保 scripts/（orchestrate 等兄弟模块）与技能根可 import
_SKILL_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS_DIR = _SKILL_ROOT / "scripts"
for _p in (str(_SCRIPTS_DIR), str(_SKILL_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def _endpoint_base(refiner_endpoint: str) -> str:
    """从 config 的 refiner.endpoint（如 https://x.coze.site/run）截取 base。

    回传走同一 Coze 部署的 /advisor_outcome 路径。
    """
    s = (refiner_endpoint or "").rstrip("/")
    if not s:
        return ""
    if s.endswith("/run"):
        return s[: -len("/run")]
    return s


def report_outcome(refiner_endpoint: str, payload: dict, timeout: float = 5.0) -> bool:
    """回调 Coze 落库真实答案 + 调用方法。best-effort：失败返回 False，不抛。

    仅在「真实出站且产出非空答案」时调用；同步阻塞（timeout 上限 5s）以保证在 entry.py
    退出前完成，但绝不因超时/异常影响答案交付。
    """
    try:
        base = _endpoint_base(refiner_endpoint)
        if not base:
            return False
        url = base + "/advisor_outcome"
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        from adapters.coze_token_embedded import get_token
        req = urllib.request.Request(
            url,
            data=body,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "Authorization": f"Bearer {get_token()}",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status == 200
    except Exception:  # noqa: BLE001 - 回传失败绝不阻断主流程
        return False
