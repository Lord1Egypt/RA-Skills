"""成本聚合与账单（第 7 类：AI 成本 / 用量可观测）。

每次调用落本地 SQLite（calls 表），聚合出日 / 周 / 月报、各家花费、成功率、P95 延迟。
纯标准库（sqlite3），零密钥、零联网。

表结构 calls：
  id, ts(ISO), provider, model, task, in_tokens, out_tokens, cost, elapsed_ms, success(0/1), error
"""

import os
import json
import sqlite3
import time
from datetime import datetime, timedelta

DEFAULT_DB = os.path.join(os.path.expanduser("~"), ".cn_llm_router", "calls.db")


def _conn(db_path=None):
    db = db_path or DEFAULT_DB
    if db == ":memory:":
        return sqlite3.connect(":memory:")
    os.makedirs(os.path.dirname(db), exist_ok=True)
    c = sqlite3.connect(db)
    c.execute(
        """CREATE TABLE IF NOT EXISTS calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT, provider TEXT, model TEXT, task TEXT,
            in_tokens INTEGER, out_tokens INTEGER, cost REAL,
            elapsed_ms INTEGER, success INTEGER, error TEXT,
            fallback_from TEXT
        )"""
    )
    # 兼容旧表无 fallback_from 列
    try:
        c.execute("ALTER TABLE calls ADD COLUMN fallback_from TEXT")
    except Exception:
        pass
    # v2.2 竞技场表
    c.execute(
        """CREATE TABLE IF NOT EXISTS arena_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            prompt TEXT NOT NULL,
            task_type TEXT NOT NULL,
            models_json TEXT NOT NULL,
            voted_provider TEXT,
            voted_model TEXT,
            vote_ts TEXT
        )"""
    )
    c.commit()
    return c
    c.commit()
    return c


def log_call(provider, model, task, in_tokens, out_tokens, cost,
             elapsed_ms, success, error="", fallback_from=None, db_path=None):
    """记录一次调用。参数化写入，防注入。
    
    fallback_from: 若本次调用为降级触发，记录原主模型 "provider:model"。
    """
    c = _conn(db_path)
    try:
        c.execute(
            "INSERT INTO calls (ts, provider, model, task, in_tokens, out_tokens, cost, elapsed_ms, success, error, fallback_from) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (datetime.now().isoformat(timespec="seconds"), provider, model, task,
             int(in_tokens or 0), int(out_tokens or 0), float(cost or 0.0),
             int(elapsed_ms or 0), 1 if success else 0, error or "",
             fallback_from or ""),
        )
        c.commit()
    finally:
        c.close()


def compute_cost(model_price, in_tokens, out_tokens):
    """按 models.yaml 中的价格（每 1M token）计算花费（元）。

    model_price: dict {"in": 价格, "out": 价格}，单位 元/1M tokens。
    若缺价格信息返回 0.0（不臆造花费）。
    """
    if not model_price:
        return 0.0
    pin = float(model_price.get("in", 0) or 0)
    pout = float(model_price.get("out", 0) or 0)
    return round(in_tokens / 1_000_000 * pin + out_tokens / 1_000_000 * pout, 6)


def _period_filter(period):
    now = datetime.now()
    if period == "day":
        start = now - timedelta(days=1)
    elif period == "week":
        start = now - timedelta(days=7)
    elif period == "month":
        start = now - timedelta(days=30)
    else:
        start = now - timedelta(days=30)
    return start.isoformat(timespec="seconds")


def aggregate(period="month", db_path=None):
    """聚合指定周期的花费 / 调用量 / 成功率 / P95 延迟。"""
    c = _conn(db_path)
    try:
        start = _period_filter(period)
        rows = c.execute(
            "SELECT provider, model, task, in_tokens, out_tokens, cost, elapsed_ms, success "
            "FROM calls WHERE ts >= ?", (start,)
        ).fetchall()
    finally:
        c.close()

    total_cost = 0.0
    total_in = total_out = 0
    total_calls = len(rows)
    success_calls = 0
    by_provider = {}
    latencies = []
    for provider, model, task, it, ot, cost, el, succ in rows:
        total_cost += cost or 0
        total_in += it or 0
        total_out += ot or 0
        if succ:
            success_calls += 1
        if el:
            latencies.append(el)
        key = provider or "unknown"
        d = by_provider.setdefault(key, {"cost": 0.0, "calls": 0, "in": 0, "out": 0})
        d["cost"] += cost or 0
        d["calls"] += 1
        d["in"] += it or 0
        d["out"] += ot or 0

    latencies.sort()
    p95 = latencies[int(len(latencies) * 0.95) - 1] if latencies else 0
    success_rate = (success_calls / total_calls * 100) if total_calls else 0.0

    return {
        "period": period,
        "total_cost": round(total_cost, 4),
        "total_in": total_in,
        "total_out": total_out,
        "total_calls": total_calls,
        "success_rate": round(success_rate, 1),
        "p95_ms": p95,
        "by_provider": {k: {kk: round(vv, 4) if isinstance(vv, float) else vv
                            for kk, vv in v.items()} for k, v in by_provider.items()},
    }


def budget_check(budget_monthly, db_path=None):
    """检查本月花费是否超预算。返回 (exceeded: bool, spent: float, budget: float)。"""
    agg = aggregate("month", db_path)
    spent = agg["total_cost"]
    budget = float(budget_monthly or 0)
    if budget <= 0:
        return (False, spent, budget)
    return (spent > budget, spent, budget)


def clear_old(days=30, db_path=None):
    """清理 N 天前的记录（可选维护）。"""
    c = _conn(db_path)
    try:
        cutoff = (datetime.now() - timedelta(days=days)).isoformat(timespec="seconds")
        n = c.execute("DELETE FROM calls WHERE ts < ?", (cutoff,)).rowcount
        c.commit()
        return n
    finally:
        c.close()


# ───────────────────────── 竞技场 ─────────────────────────
def log_arena_vote(prompt, task_type, models, voted_provider, voted_model, db_path=None):
    """记录一次竞技场投票。"""
    c = _conn(db_path)
    try:
        c.execute(
            "INSERT INTO arena_sessions (ts, prompt, task_type, models_json, voted_provider, voted_model, vote_ts) "
            "VALUES (?,?,?,?,?,?,?)",
            (datetime.now().isoformat(timespec="seconds"), prompt, task_type,
             json.dumps(models, ensure_ascii=False),
             voted_provider or "", voted_model or "",
             datetime.now().isoformat(timespec="seconds")),
        )
        c.commit()
    finally:
        c.close()


def win_rates(db_path=None):
    """统计各模型在不同任务类型下的胜率。"""
    c = _conn(db_path)
    try:
        rows = c.execute(
            "SELECT task_type, voted_provider, voted_model, COUNT(*) as wins "
            "FROM arena_sessions WHERE voted_provider IS NOT NULL AND voted_provider != '' "
            "GROUP BY task_type, voted_provider, voted_model ORDER BY task_type, wins DESC"
        ).fetchall()
    finally:
        c.close()
    result = {}
    for task_type, prov, model, wins in rows:
        result.setdefault(task_type, []).append({
            "provider": prov, "model": model, "wins": wins
        })
    return result
