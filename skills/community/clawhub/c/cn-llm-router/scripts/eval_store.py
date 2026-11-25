"""评测历史 SQLite 存档与对比（v2.9.0 新增）。

每次 arena --suite 评测存档（模型版本 + 四维得分 + 日期），
「新模型发布值不值得换」= 重跑后自动生成对比报告。
纯标准库（sqlite3），零密钥、零联网。

进度库默认 ~/.cn_llm_router/evals.db（运行时产物，不进技能包）。
"""

import os
import sys
import json
import sqlite3
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DEFAULT_DB = os.path.join(os.path.expanduser("~"), ".cn_llm_router", "evals.db")
DIMENSIONS = ("code", "reason", "translate", "summarize")


def _conn(db_path=None):
    db = db_path or DEFAULT_DB
    if db != ":memory:":
        os.makedirs(os.path.dirname(db), exist_ok=True)
    c = sqlite3.connect(db)
    c.row_factory = sqlite3.Row
    c.execute(
        """CREATE TABLE IF NOT EXISTS eval_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            suite TEXT,
            model_key TEXT NOT NULL,
            provider TEXT,
            model TEXT,
            code REAL, reason REAL, translate REAL, summarize REAL,
            total REAL, cases INTEGER,
            detail_json TEXT
        )"""
    )
    c.execute("CREATE INDEX IF NOT EXISTS idx_eval_model ON eval_runs(model_key, ts)")
    c.commit()
    return c


def save_run(result, db_path=None):
    """保存一次完整评测（每模型一行）。返回写入行数。"""
    c = _conn(db_path)
    ts = datetime.now().isoformat(timespec="seconds")
    n = 0
    details = json.dumps(result.get("details", []), ensure_ascii=False)
    for mkey, d in result.get("by_model", {}).items():
        s = d["scores"]
        c.execute(
            "INSERT INTO eval_runs (ts, suite, model_key, provider, model, code, reason, translate, summarize, total, cases, detail_json) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (ts, result.get("suite", ""), mkey, d["provider"], d["model"],
             s.get("code", 0), s.get("reason", 0), s.get("translate", 0), s.get("summarize", 0),
             d["total"], d["cases"], details),
        )
        n += 1
    c.commit()
    c.close()
    return n


def history(model_key=None, limit=50, db_path=None):
    """查询历史记录（可按模型过滤）。"""
    c = _conn(db_path)
    if model_key:
        rows = c.execute(
            "SELECT * FROM eval_runs WHERE model_key=? ORDER BY ts DESC LIMIT ?", (model_key, limit)
        ).fetchall()
    else:
        rows = c.execute(
            "SELECT * FROM eval_runs ORDER BY ts DESC LIMIT ?", (limit,)
        ).fetchall()
    c.close()
    return [dict(r) for r in rows]


def best_by_model(db_path=None):
    """每个模型的历史最佳总分（用于对比报告基线）。"""
    c = _conn(db_path)
    rows = c.execute(
        "SELECT model_key, MAX(total) best, COUNT(*) runs FROM eval_runs GROUP BY model_key"
    ).fetchall()
    c.close()
    return {r["model_key"]: {"best": r["best"], "runs": r["runs"]} for r in rows}


def recent_models(limit=20, db_path=None):
    """返回最近参评过的模型 key 列表。"""
    c = _conn(db_path)
    rows = c.execute(
        "SELECT DISTINCT model_key FROM eval_runs ORDER BY ts DESC LIMIT ?", (limit,)
    ).fetchall()
    c.close()
    return [r["model_key"] for r in rows]


def compare(current, db_path=None):
    """生成对比报告文本（当前结果 vs 历史最佳）。"""
    lines = ["📈 评测历史对比报告"]
    base = best_by_model(db_path)
    if not base:
        lines.append("  暂无历史基线，本次结果已作为基线存档。")
        return "\n".join(lines)
    lines.append("  %-26s %8s %8s %8s" % ("模型", "本次总分", "历史最佳", "变化"))
    lines.append("  " + "-" * 54)
    for mkey, d in sorted(current["by_model"].items(), key=lambda x: -x[1]["total"]):
        b = base.get(mkey)
        if not b:
            lines.append("  %-26s %8.2f %8s %8s" % (mkey[:26], d["total"], "-", "新"))
        else:
            delta = d["total"] - b["best"]
            tag = "↑+%.2f" % delta if delta > 0.005 else ("↓%.2f" % delta if delta < -0.005 else "持平")
            lines.append("  %-26s %8.2f %8.2f %8s" % (mkey[:26], d["total"], b["best"], tag))
    return "\n".join(lines)
