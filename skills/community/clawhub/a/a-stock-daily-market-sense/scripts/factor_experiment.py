# -*- coding: utf-8 -*-
"""因子挖掘实验台账（factor_experiment_log）读写层。

由 factor_backtest.py（挖矿收尾自动登记确定性列）与 factor_lab.py（查询 / 人工判分）
共用。存储走仓库共享 shared/data/db_core（PostgreSQL 默认，sqlite 离线）。

脑/手边界：脚本只写确定性列（组、窗口、spec、命中/过闸计数、证据路径）。判断列
verdict / verdict_note 是**模型判断后由人**经 set_verdict 落库，脚本从不自动写。

DDL 镜像 shared/data/init_alpha_data.sql §14；本模块自带 ensure_table，全新库不依赖先跑
schema 文件。
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
_BUNDLED_SHARED = HERE / "_shared"
_DEV_SHARED = HERE.parents[2] / "shared" / "data"
sys.path.insert(0, str(_BUNDLED_SHARED if _BUNDLED_SHARED.exists() else _DEV_SHARED))

from db_core import BACKEND, Backend, get_connection, placeholder  # noqa: E402

VERDICT_ENUM = ("adopted", "rejected", "observing")

DDL = """
CREATE TABLE IF NOT EXISTS factor_experiment_log (
    group_key        TEXT NOT NULL,
    window_end       TEXT NOT NULL,
    spec_hash        TEXT NOT NULL,
    run_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    group_label      TEXT,
    window_start     TEXT,
    objective_cell   TEXT,
    min_n            INTEGER,
    spec_json        JSONB,
    n_signals        INTEGER,
    n_unique_stocks  INTEGER,
    n_singles_passed INTEGER,
    n_pairs_passed   INTEGER,
    evidence_path    TEXT,
    verdict          TEXT,
    verdict_note     TEXT,
    PRIMARY KEY (group_key, window_end, spec_hash)
)
"""

# sqlite 没有 TIMESTAMPTZ / JSONB，退化为 TEXT（仅离线调试用）。
DDL_SQLITE = (
    DDL.replace("TIMESTAMPTZ NOT NULL DEFAULT NOW()", "TEXT NOT NULL DEFAULT (datetime('now'))")
       .replace("JSONB", "TEXT")
)


def ensure_table(conn: Any) -> None:
    cur = conn.cursor()
    cur.execute(DDL if BACKEND == Backend.POSTGRESQL else DDL_SQLITE)
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_factor_experiment_group "
        "ON factor_experiment_log(group_key, window_end)"
    )


def _json_param(value: Any) -> Any:
    if value is None:
        return None
    if BACKEND == Backend.POSTGRESQL:
        from psycopg2.extras import Json
        return Json(value, dumps=lambda v: json.dumps(v, ensure_ascii=False))
    return json.dumps(value, ensure_ascii=False)


def build_spec(args: Any, meta: Dict[str, Any]) -> Tuple[Dict[str, Any], str]:
    """从挖矿参数派生可复现 spec 与其 sha1。

    builtin 组：group-defining 阈值 + min_n + 目标格；custom：spec 文件内容 + min_n + 目标格。
    """
    group = getattr(args, "group", "custom")
    common = {"min_n": getattr(args, "min_n", None),
              "entry": getattr(args, "entry", None), "horizon": getattr(args, "horizon", None)}
    if group == "custom":
        payload = {"kind": "custom", "spec": meta.get("spec") or {}, **common}
    else:
        payload = {
            "kind": "builtin", "group": group,
            "market_cap": getattr(args, "market_cap", None), "amount": getattr(args, "amount", None),
            "pct": getattr(args, "pct", None),
            "discount_min": getattr(args, "discount_min", None),
            "discount_max": getattr(args, "discount_max", None),
            "contraction_max": getattr(args, "contraction_max", None),
            "expansion_min": getattr(args, "expansion_min", None),
            "lookback": getattr(args, "lookback", None),
            "low_recency": getattr(args, "low_recency", None),
            **common,
        }
    digest = hashlib.sha1(
        json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    return payload, digest


def log_experiment(evidence: Dict[str, Any], args: Any, group_key: str, asof: str,
                   evidence_path: Optional[str] = None) -> None:
    """挖矿收尾登记（best-effort）：只写确定性列，upsert 主键防重。DB 不可用只告警不中断。"""
    meta = evidence.get("meta", {})
    payload, spec_hash = build_spec(args, meta)
    singles_passed = sum(1 for c in evidence.get("overlay_singles", []) if c.get("passes_guardrails"))
    pairs_passed = sum(1 for c in evidence.get("overlay_pairs", []) if c.get("passes_guardrails"))
    win = meta.get("signal_day_window") or [None, None]
    cols = {
        "group_key": group_key,
        "window_end": asof,
        "spec_hash": spec_hash,
        "group_label": meta.get("group_label"),
        "window_start": win[0],
        "objective_cell": meta.get("objective_cell"),
        "min_n": getattr(args, "min_n", None),
        "spec_json": payload,
        "n_signals": meta.get("n_signals"),
        "n_unique_stocks": meta.get("n_unique_stocks"),
        "n_singles_passed": singles_passed,
        "n_pairs_passed": pairs_passed,
        "evidence_path": evidence_path,
    }
    try:
        with get_connection() as conn:
            ensure_table(conn)
            _upsert(conn, cols)
        print(f"[experiment] logged {group_key}@{asof} spec={spec_hash[:8]} "
              f"(singles_passed={singles_passed}, pairs_passed={pairs_passed})")
    except Exception as exc:  # noqa: BLE001 - 实验登记失败不阻断挖矿主产物
        print(f"[experiment] skip (best-effort, DB 不可用): {exc}")


def _upsert(conn: Any, cols: Dict[str, Any]) -> None:
    keys = list(cols.keys())
    ph = placeholder()
    vals = [_json_param(cols[k]) if k == "spec_json" else cols[k] for k in keys]
    collist = ", ".join(keys)
    phlist = ", ".join([ph] * len(keys))
    cur = conn.cursor()
    if BACKEND == Backend.POSTGRESQL:
        # 主键冲突 = 同组同窗同参重跑：刷新确定性列与 run_at，绝不动人工判断列。
        upd = ", ".join(f"{k}=EXCLUDED.{k}" for k in keys
                        if k not in ("group_key", "window_end", "spec_hash"))
        sql = (f"INSERT INTO factor_experiment_log ({collist}) VALUES ({phlist}) "
               f"ON CONFLICT (group_key, window_end, spec_hash) "
               f"DO UPDATE SET {upd}, run_at=NOW()")
    else:
        # sqlite：读出旧判断列后 REPLACE 回填，保住人工 verdict。
        cur.execute(
            "SELECT verdict, verdict_note FROM factor_experiment_log "
            "WHERE group_key=? AND window_end=? AND spec_hash=?",
            (cols["group_key"], cols["window_end"], cols["spec_hash"]),
        )
        old = cur.fetchone()
        if old:
            cols = {**cols, "verdict": old[0], "verdict_note": old[1]}
            keys = list(cols.keys())
            vals = [_json_param(cols[k]) if k == "spec_json" else cols[k] for k in keys]
            collist = ", ".join(keys)
            phlist = ", ".join([ph] * len(keys))
        sql = f"INSERT OR REPLACE INTO factor_experiment_log ({collist}) VALUES ({phlist})"
    cur.execute(sql, vals)


def list_experiments(recent: int = 20) -> List[Dict[str, Any]]:
    """最近 N 条实验（决策摘要，不含 spec_json 全文）。"""
    ph = placeholder()
    with get_connection() as conn:
        ensure_table(conn)
        cur = conn.cursor()
        cur.execute(
            "SELECT group_key, window_end, spec_hash, run_at, group_label, window_start, "
            "objective_cell, min_n, n_signals, n_unique_stocks, n_singles_passed, "
            "n_pairs_passed, evidence_path, verdict, verdict_note "
            f"FROM factor_experiment_log ORDER BY run_at DESC LIMIT {ph}",
            (recent,),
        )
        rows = cur.fetchall()
    fields = ["group_key", "window_end", "spec_hash", "run_at", "group_label", "window_start",
              "objective_cell", "min_n", "n_signals", "n_unique_stocks", "n_singles_passed",
              "n_pairs_passed", "evidence_path", "verdict", "verdict_note"]
    out = []
    for r in rows:
        rec = dict(zip(fields, r))
        rec["run_at"] = str(rec["run_at"])
        out.append(rec)
    return out


def set_verdict(selector: str, verdict: Optional[str], note: Optional[str] = None) -> Dict[str, Any]:
    """人工判分：更新 verdict/verdict_note 两列，其余列一律不动。

    selector = "<group_key>@<window_end>@<spec_hash 前缀>"（前缀 ≥6 位，唯一即可）。
    """
    parts = selector.split("@")
    if len(parts) != 3:
        raise SystemExit("selector 格式应为 <group_key>@<window_end>@<spec_hash前缀>")
    group_key, window_end, hash_prefix = parts
    if len(hash_prefix) < 6:
        raise SystemExit("spec_hash 前缀至少 6 位，避免误匹配")
    if verdict is not None and verdict not in VERDICT_ENUM:
        raise SystemExit(f"verdict 只能是 {VERDICT_ENUM} 或留空")
    ph = placeholder()
    with get_connection() as conn:
        ensure_table(conn)
        cur = conn.cursor()
        cur.execute(
            f"SELECT spec_hash FROM factor_experiment_log "
            f"WHERE group_key={ph} AND window_end={ph} AND spec_hash LIKE {ph}",
            (group_key, window_end, hash_prefix + "%"),
        )
        matches = [r[0] for r in cur.fetchall()]
        if not matches:
            raise SystemExit(f"未匹配到实验：{selector}")
        if len(matches) > 1:
            raise SystemExit(f"前缀 {hash_prefix} 匹配到多条 {matches}，请给更长前缀")
        full_hash = matches[0]
        # 只更新两个判断列（白名单硬编码，杜绝脚本改确定性列）。
        cur.execute(
            f"UPDATE factor_experiment_log SET verdict={ph}, verdict_note={ph} "
            f"WHERE group_key={ph} AND window_end={ph} AND spec_hash={ph}",
            (verdict, note, group_key, window_end, full_hash),
        )
    return {"group_key": group_key, "window_end": window_end, "spec_hash": full_hash,
            "verdict": verdict, "verdict_note": note}
