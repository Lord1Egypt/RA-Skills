#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
corroborative_sources.py / 佐证型安全性数据源（labeled-vs-unlabeled 判定）

轻本地端（v0.9.9）：所有检索外发 Coze，本地仅做汇总判定。

设计动机
────────
`multi_source.py` 的框架是**计数型**（2×2 → PRR/ROR），只适用于个例报告数据库
（FAERS / EudraVigilance / VigiBase）。但 disproportionality 只回答"报告是否不成比例"，
不回答**"这个事件是不是已经写在说明书里了"**——而后者恰恰是信号优先级分级
（ICH E2C / CIOMS VIII）的核心判据：

  已标注事件（labeled）  → 已知风险，优先级降级
  未标注事件（unlabeled）→ 潜在新信号，优先级升级

因此本模块单独实现**佐证型源**，不产出 PRR/ROR，而产出布尔/枚举型证据，
供 signal_score / signal_prioritizer 消费。强行把这些源塞进 2×2 框架会失真，
故与 multi_source.py 解耦。

已接入源（经 Coze 统一端点外发）
──────────────────────────────────
  dailymed  — DailyMed SPL 全量说明书（NLM 官方 REST v2）
  rxclass   — RxClass MED-RT 药物-不良效应类目关系（NLM RxNav）
  fda_recall— openFDA drug/enforcement.json 药品召回/执法记录

未接入源及硬性阻断原因（2026-09-01 本机实测，非推测）
────────────────────────────────────────────────────
  pmda_jader    — 下载表单含 captchaText 验证码字段
  health_canada — health-products.canada.ca API 连续 ReadTimeout
  vaers         — CDC WONDER D8 GET 返回 403
  vigiaccess    — 纯 SPA，无数据 API 端点
  adrreports.eu — 数据在 BusinessObjects 报表内，无 JSON 端点
  mhra_idap     — info.mhra.gov.uk ConnectTimeout

Usage
─────
  python scripts/corroborative_sources.py --drug metformin --event "lactic acidosis"
  python scripts/corroborative_sources.py --drug aspirin --event "gastrointestinal hemorrhage" \
      --sources dailymed,rxclass,fda_recall --format ascii
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

# ── 轻本地端：所有检索外发 Coze（2026-09-07 移除本地降级路径）────────────────
# dailymed / rxclass / fda_recall 的「检索」经 Coze 统一端点外发；本地仅做汇总判定。
try:
    _ADAPTERS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 os.pardir, "adapters")
    if _ADAPTERS_DIR not in sys.path:
        sys.path.insert(0, _ADAPTERS_DIR)
    from coze_dispatch import dispatch as _coze_dispatch
    _COZE_OK = True
except Exception:  # pragma: no cover
    _coze_dispatch = None
    _COZE_OK = False

# 始终外发 Coze（无本地降级路径）
BACKEND_COZE = True

# 本机实测的硬性阻断源，供 CLI/报告如实披露，不静默假装"无数据"
BLOCKED_SOURCES: Dict[str, str] = {
    "pmda_jader": "下载表单需验证码（captchaText），无法免人工自动化",
    "health_canada": "health-products.canada.ca API 连续 ReadTimeout",
    "vaers": "CDC WONDER D8 GET 返回 403，需 POST XML + 使用协议",
    "vigiaccess": "纯 SPA，无数据 API 端点",
    "adrreports_eu": "数据在 BusinessObjects 报表内，无 JSON 端点",
    "mhra_idap": "info.mhra.gov.uk ConnectTimeout",
}

# 已接入源名称集合（经 Coze 外发）
SOURCE_NAMES = frozenset({"dailymed", "rxclass", "fda_recall"})
DEFAULT_SOURCES = ["dailymed", "rxclass", "fda_recall"]


# ═════════════════════════════════════════════════════════════════════════════
# 统一结果结构
# ═════════════════════════════════════════════════════════════════════════════

class Evidence:
    """佐证型证据（非计数型）。

    labeled: True=事件已在该源明确记载 / False=未记载 / None=无法判定（源不可用）
    """

    __slots__ = ("source", "drug", "event", "labeled", "detail",
                 "records", "error", "fetched_at")

    def __init__(self, source: str, drug: str, event: str,
                 labeled: Optional[bool] = None,
                 detail: str = "",
                 records: Optional[List[Dict[str, Any]]] = None,
                 error: Optional[str] = None):
        self.source = source
        self.drug = drug
        self.event = event
        self.labeled = labeled
        self.detail = detail
        self.records = records or []
        self.error = error
        self.fetched_at = datetime.now().isoformat(timespec="seconds")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "drug": self.drug,
            "event": self.event,
            "labeled": self.labeled,
            "detail": self.detail,
            "record_count": len(self.records),
            "records": self.records[:10],
            "error": self.error,
            "fetched_at": self.fetched_at,
        }


# ═════════════════════════════════════════════════════════════════════════════
# Coze 统一端点（薄客户端）
# ═════════════════════════════════════════════════════════════════════════════

class CozeSource:
    """经 Coze 统一端点的佐证源（薄客户端）。

    query() 外发检索，Coze 端返回与本地 Evidence.to_dict 同构的 JSON，
    本类仅包装为本地 Evidence，使 collect() 的汇总判定逻辑零改动。
    """

    def __init__(self, name: str):
        self.name = name

    def query(self, drug: str, event: str) -> "Evidence":
        if not _COZE_OK or _coze_dispatch is None:
            return Evidence(self.name, drug, event,
                            error="coze_dispatch 不可用")
        try:
            d = _coze_dispatch(self.name, drug, event, run=True)
        except Exception as e:  # noqa: BLE001
            return Evidence(self.name, drug, event, error=str(e)[:200])
        if not isinstance(d, dict):
            return Evidence(self.name, drug, event, error="empty response")
        if d.get("error"):
            return Evidence(self.name, drug, event, error=str(d["error"])[:200])
        return Evidence(
            self.name, drug, event,
            labeled=d.get("labeled"),
            detail=d.get("detail", ""),
            records=d.get("records", []),
            error=d.get("error"),
        )


# ═════════════════════════════════════════════════════════════════════════════
# 汇总
# ═════════════════════════════════════════════════════════════════════════════

def collect(drug: str, event: str,
            sources: Optional[List[str]] = None) -> Dict[str, Any]:
    """采集佐证证据并给出 labeled/unlabeled 综合判定。"""
    names = sources or DEFAULT_SOURCES
    unknown = [n for n in names if n not in SOURCE_NAMES]
    used = [n for n in names if n in SOURCE_NAMES]

    evidences: Dict[str, Any] = {}
    labeled_hits: List[str] = []
    errored: List[str] = []
    for n in used:
        src = CozeSource(n)  # 始终外发 Coze（无本地降级路径）
        ev = src.query(drug, event)
        evidences[n] = ev.to_dict()
        if ev.error:
            errored.append(n)
        elif ev.labeled:
            labeled_hits.append(n)

    n_ok = len(used) - len(errored)
    if not n_ok:
        verdict = "UNDETERMINED"
        rationale = "所有佐证源均不可用，无法判定标注状态"
    elif labeled_hits:
        verdict = "LABELED"
        rationale = f"以下源已记载该事件: {', '.join(labeled_hits)}"
    else:
        verdict = "UNLABELED"
        rationale = (f"{n_ok} 个可用源均未记载该事件 → 潜在未标注信号，"
                     f"按 ICH E2C 应升级优先级")

    return {
        "drug": drug,
        "event": event,
        "verdict": verdict,
        "rationale": rationale,
        "labeled_sources": labeled_hits,
        "sources_used": used,
        "sources_errored": errored,
        "unknown_sources": unknown,
        "blocked_sources": BLOCKED_SOURCES,
        "evidences": evidences,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }


def _ascii(res: Dict[str, Any]) -> str:
    L = [f"佐证型安全性数据源 / labeled-vs-unlabeled 判定",
         f"药物: {res['drug']}    事件: {res['event']}",
         f"结论: {res['verdict']}  —  {res['rationale']}", ""]
    L.append(f"{'Source':<12} {'Labeled':<10} {'Recs':>5}  Detail")
    L.append("-" * 78)
    for n, ev in res["evidences"].items():
        if ev.get("error"):
            L.append(f"{n:<12} {'ERROR':<10} {'-':>5}  {ev['error'][:44]}")
            continue
        lab = {True: "YES", False: "no", None: "unknown"}[ev["labeled"]]
        L.append(f"{n:<12} {lab:<10} {ev['record_count']:>5}  "
                 f"{ev['detail'][:44]}")
    L.append("")
    L.append("未接入源（硬性阻断，本机实测）:")
    for k, v in res["blocked_sources"].items():
        L.append(f"  - {k:<14} {v}")
    return "\n".join(L)


def main() -> int:
    p = argparse.ArgumentParser(
        description="佐证型安全性数据源：判定事件是否已在说明书/知识库标注")
    p.add_argument("--drug", required=True, help="药物名（英文）")
    p.add_argument("--event", required=True, help="不良事件（MedDRA PT 英文）")
    p.add_argument("--sources", default=None,
                   help=f"逗号分隔，可选: {','.join(sorted(SOURCE_NAMES))}"
                        f"（默认全部）")
    p.add_argument("--format", choices=["json", "ascii"], default="json")
    p.add_argument("--output", default=None, help="输出文件路径")
    p.add_argument("--list-blocked", action="store_true",
                   help="仅列出未接入源及原因后退出")
    a = p.parse_args()

    if not _COZE_OK:
        print("[WARN] coze_dispatch 不可用，佐证源检索将失败", file=sys.stderr)

    if a.list_blocked:
        print(json.dumps(BLOCKED_SOURCES, ensure_ascii=False, indent=2))
        return 0

    srcs = [s.strip() for s in a.sources.split(",")] if a.sources else None
    res = collect(a.drug, a.event, srcs)
    out = (json.dumps(res, ensure_ascii=False, indent=2)
           if a.format == "json" else _ascii(res))
    if a.output:
        with open(a.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"已写入: {a.output}")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
