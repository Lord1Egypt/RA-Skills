"""
evm_knowledge — 挣值管理独立知识库接口

三库架构中的 evm.db 管理器。
每个项目一条 evm_analyses 记录，各阶段明细存 evm_periods。
独立运行不依赖 shared.db，跨库引用通过 project_id + ATTACH 实现。
"""
import json
import os
import sqlite3
from typing import Optional

# R-12 审计锚点：数据目录字面量声明
DEFAULT_DATA_DIR_RAW = "skills/.standardization/activity-duration-estimation/data/"

SKILL_DIR = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."
))
_data_path = os.path.normpath(os.path.join(
    SKILL_DIR, "..", ".standardization", "activity-duration-estimation", "data"
))
EVM_DB = os.path.join(_data_path, "evm.db")
SHARED_DB = os.path.join(_data_path, "knowledge.db")


# ═══════════════════════════════════════════════════════
# 数据库初始化
# ═══════════════════════════════════════════════════════

def _ensure_db(db_path: str = None) -> sqlite3.Connection:
    path = db_path or EVM_DB
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS evm_analyses (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id      INTEGER,
            project_name    TEXT NOT NULL,
            bac             REAL NOT NULL,
            total_plan_duration REAL NOT NULL,
            analysis_period TEXT,
            plan_progress   REAL,
            actual_progress REAL,
            ev              REAL,
            pv              REAL,
            ac              REAL,
            sv              REAL,
            spi             REAL,
            cv              REAL,
            cpi             REAL,
            eac_uncorrected REAL,
            eac_corrected   REAL,
            etc_uncorrected REAL,
            etc_corrected   REAL,
            vac_uncorrected REAL,
            vac_corrected   REAL,
            phases_json     TEXT,
            created_at      TEXT DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_evm_project ON evm_analyses(project_id);
        CREATE INDEX IF NOT EXISTS idx_evm_spi ON evm_analyses(spi);
        CREATE INDEX IF NOT EXISTS idx_evm_cpi ON evm_analyses(cpi);

        CREATE TABLE IF NOT EXISTS evm_periods (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id     INTEGER NOT NULL REFERENCES evm_analyses(id),
            phase_name      TEXT NOT NULL,
            cumulative_days REAL NOT NULL,
            pv              REAL,
            ac              REAL,
            plan_progress   REAL,
            actual_progress REAL
        );
        CREATE INDEX IF NOT EXISTS idx_evmp_analysis ON evm_periods(analysis_id);
    """)
    return conn


# ═══════════════════════════════════════════════════════
# 注册到 shared.db
# ═══════════════════════════════════════════════════════

def _register_in_shared(skill_name: str, project_id: int, record_id: int,
                        project_name: str, meta: dict):
    if not os.path.exists(SHARED_DB):
        return
    try:
        conn = sqlite3.connect(SHARED_DB)
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS skill_registry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                skill_name TEXT NOT NULL,
                project_id INTEGER,
                project_name TEXT DEFAULT '',
                record_id INTEGER,
                db_path TEXT NOT NULL,
                meta_json TEXT DEFAULT '{}',
                created_at TEXT DEFAULT (datetime('now'))
            );
            CREATE INDEX IF NOT EXISTS idx_reg_skill ON skill_registry(skill_name);
            CREATE INDEX IF NOT EXISTS idx_reg_project ON skill_registry(project_id);
        """)
        conn.execute("""
            INSERT INTO skill_registry (skill_name, project_id, project_name, record_id, db_path, meta_json)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (skill_name, project_id, project_name, record_id,
              os.path.relpath(EVM_DB), json.dumps(meta, ensure_ascii=False)))
        conn.commit()
        conn.close()
    except Exception:
        pass


# ═══════════════════════════════════════════════════════
# CRUD
# ═══════════════════════════════════════════════════════

def save_analysis(
    project_name: str,
    bac: float,
    total_plan_duration: float,
    analysis_period: str = None,
    plan_progress: float = None,
    actual_progress: float = None,
    ev: float = None,
    pv: float = None,
    ac: float = None,
    sv: float = None,
    spi: float = None,
    cv: float = None,
    cpi: float = None,
    eac_uncorrected: float = None,
    eac_corrected: float = None,
    etc_uncorrected: float = None,
    etc_corrected: float = None,
    vac_uncorrected: float = None,
    vac_corrected: float = None,
    phases: list[dict] = None,
    project_id: int = None,
    db_path: str = None,
) -> int:
    """保存挣值分析结果到 evm.db"""
    conn = _ensure_db(db_path)
    c = conn.execute("""
        INSERT INTO evm_analyses
            (project_id, project_name, bac, total_plan_duration, analysis_period,
             plan_progress, actual_progress, ev, pv, ac, sv, spi, cv, cpi,
             eac_uncorrected, eac_corrected, etc_uncorrected, etc_corrected,
             vac_uncorrected, vac_corrected, phases_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (project_id, project_name, bac, total_plan_duration, analysis_period,
          plan_progress, actual_progress, ev, pv, ac, sv, spi, cv, cpi,
          eac_uncorrected, eac_corrected, etc_uncorrected, etc_corrected,
          vac_uncorrected, vac_corrected,
          json.dumps(phases, ensure_ascii=False) if phases else None))
    analysis_id = c.lastrowid

    if phases:
        for ph in phases:
            conn.execute("""
                INSERT INTO evm_periods
                    (analysis_id, phase_name, cumulative_days, pv, ac, plan_progress, actual_progress)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (analysis_id, ph["phase_name"], ph.get("cumulative_days", 0),
                  ph.get("pv"), ph.get("ac"), ph.get("plan_progress"),
                  ph.get("actual_progress")))

    conn.commit()
    conn.close()

    meta = {"spi": spi, "cpi": cpi, "ev": ev, "pv": pv}
    _register_in_shared("evm", project_id, analysis_id, project_name, meta)

    print(f"  [EVM-KB] 挣值分析已存入 (ID={analysis_id}, project={project_name})")
    return analysis_id


def get_analysis(analysis_id: int, db_path: str = None) -> dict:
    """按 ID 查询挣值分析记录"""
    conn = _ensure_db(db_path)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM evm_analyses WHERE id = ?",
                       (analysis_id,)).fetchone()
    if not row:
        conn.close()
        return None
    result = dict(row)
    result["phases"] = [
        dict(r) for r in conn.execute(
            "SELECT * FROM evm_periods WHERE analysis_id = ? ORDER BY cumulative_days",
            (analysis_id,)).fetchall()
    ]
    conn.close()
    return result


def get_by_project(project_id: int, db_path: str = None) -> dict:
    """按 project_id 查询最新挣值分析"""
    conn = _ensure_db(db_path)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM evm_analyses WHERE project_id = ? ORDER BY created_at DESC LIMIT 1",
        (project_id,)).fetchone()
    if not row:
        conn.close()
        return None
    result = dict(row)
    result["phases"] = [
        dict(r) for r in conn.execute(
            "SELECT * FROM evm_periods WHERE analysis_id = ? ORDER BY cumulative_days",
            (result["id"],)).fetchall()
    ]
    conn.close()
    return result


def find_by_spi(min_spi: float = 0, max_spi: float = None, limit: int = 20, db_path: str = None) -> list[dict]:
    """按 SPI 区间查询（走索引）"""
    conn = _ensure_db(db_path)
    conn.row_factory = sqlite3.Row
    conditions, params = ["spi IS NOT NULL", "spi >= ?"], [min_spi]
    if max_spi is not None:
        conditions.append("spi <= ?")
        params.append(max_spi)
    rows = conn.execute(
        f"SELECT id, project_name, bac, ev, pv, ac, spi, cpi, sv, cv, created_at "
        f"FROM evm_analyses WHERE {' AND '.join(conditions)} "
        f"ORDER BY spi DESC LIMIT ?", params + [limit]).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def find_by_cpi(min_cpi: float = 0, max_cpi: float = None, limit: int = 20, db_path: str = None) -> list[dict]:
    """按 CPI 区间查询（走索引）"""
    conn = _ensure_db(db_path)
    conn.row_factory = sqlite3.Row
    conditions, params = ["cpi IS NOT NULL", "cpi >= ?"], [min_cpi]
    if max_cpi is not None:
        conditions.append("cpi <= ?")
        params.append(max_cpi)
    rows = conn.execute(
        f"SELECT id, project_name, bac, ev, pv, ac, spi, cpi, sv, cv, created_at "
        f"FROM evm_analyses WHERE {' AND '.join(conditions)} "
        f"ORDER BY cpi DESC LIMIT ?", params + [limit]).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def list_all(limit: int = 20, db_path: str = None) -> list[dict]:
    """列出所有挣值分析记录"""
    conn = _ensure_db(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT id, project_name, analysis_period, bac, ev, pv, ac, spi, cpi, created_at "
        "FROM evm_analyses ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ═══════════════════════════════════════════════════════
# 跨库：读 shared.db 的项目进度基线
# ═══════════════════════════════════════════════════════

def get_project_phases(project_id: int) -> Optional[list[dict]]:
    """从 shared.db 读取项目的阶段和计划工期"""
    if not os.path.exists(SHARED_DB):
        return None
    try:
        conn = sqlite3.connect(SHARED_DB)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT phase, task_name, o, m, p FROM work_packages WHERE project_id = ? ORDER BY id",
            (project_id,)).fetchall()
        conn.close()
        return [dict(r) for r in rows] if rows else None
    except Exception:
        return None


def get_project_info(project_id: int) -> Optional[dict]:
    """从 shared.db 读取项目概况"""
    if not os.path.exists(SHARED_DB):
        return None
    try:
        conn = sqlite3.connect(SHARED_DB)
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT id, name, total_duration, wp_count FROM projects WHERE id = ?",
            (project_id,)).fetchone()
        conn.close()
        return dict(row) if row else None
    except Exception:
        return None


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2 and sys.argv[1] == "list":
        rows = list_all()
        for r in rows:
            print(f"  [{r['id']}] {r['project_name']}: SPI={r['spi']}, CPI={r['cpi']}")
    elif len(sys.argv) >= 3 and sys.argv[1] == "get":
        r = get_analysis(int(sys.argv[2]))
        if r:
            print(f"  {r['project_name']}({r['analysis_period']}): "
                  f"EV={r['ev']}, PV={r['pv']}, AC={r['ac']}, "
                  f"SPI={r['spi']}, CPI={r['cpi']}")
    else:
        print("用法: python evm_knowledge.py <list|get id>")
