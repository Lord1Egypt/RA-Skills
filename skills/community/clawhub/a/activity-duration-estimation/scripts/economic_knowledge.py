"""
economic_knowledge — 经济效益分析独立知识库接口

三库架构中的 economic.db 管理器。
每个项目一条 economic_analyses 记录，逐年现金流存 economic_cashflows。
独立运行不依赖 shared.db，跨库引用通过 project_id + ATTACH 实现。
"""
import json
import os
import sqlite3
from datetime import datetime
from typing import Optional, Any

# R-12 审计锚点：数据目录字面量声明
DEFAULT_DATA_DIR_RAW = "skills/.standardization/activity-duration-estimation/data/"

SKILL_DIR = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."
))
_data_path = os.path.normpath(os.path.join(
    SKILL_DIR, "..", ".standardization", "activity-duration-estimation", "data"
))
ECONOMIC_DB = os.path.join(_data_path, "economic.db")
SHARED_DB = os.path.join(_data_path, "knowledge.db")


# ═══════════════════════════════════════════════════════
# 数据库初始化
# ═══════════════════════════════════════════════════════

def _ensure_db(db_path: str = None) -> sqlite3.Connection:
    path = db_path or ECONOMIC_DB
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS economic_analyses (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id      INTEGER,
            project_name    TEXT NOT NULL,
            discount_rate   REAL NOT NULL,
            periods         INTEGER NOT NULL,
            initial_investment REAL NOT NULL,
            annual_revenue  REAL NOT NULL,
            annual_cost     REAL NOT NULL,
            terminal_value  REAL DEFAULT 0,
            currency        TEXT DEFAULT '¥',
            npv             REAL,
            irr             REAL,
            bcr             REAL,
            roi_static      REAL,
            roi_weighted    REAL,
            pbp_static      REAL,
            pbp_dynamic     REAL,
            cashflows_json  TEXT,
            params_json     TEXT,
            created_at      TEXT DEFAULT (datetime('now'))
        );
        CREATE INDEX IF NOT EXISTS idx_eco_project ON economic_analyses(project_id);
        CREATE INDEX IF NOT EXISTS idx_eco_npv ON economic_analyses(npv);
        CREATE INDEX IF NOT EXISTS idx_eco_irr ON economic_analyses(irr);

        CREATE TABLE IF NOT EXISTS economic_cashflows (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id     INTEGER NOT NULL REFERENCES economic_analyses(id),
            year            INTEGER NOT NULL,
            revenue         REAL NOT NULL,
            cost            REAL NOT NULL,
            net_cashflow    REAL NOT NULL,
            net_discounted  REAL NOT NULL,
            discounted_cost REAL NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_cf_analysis ON economic_cashflows(analysis_id);
    """)
    return conn


# ═══════════════════════════════════════════════════════
# 注册到 shared.db 的 skill_registry
# ═══════════════════════════════════════════════════════

def _register_in_shared(skill_name: str, project_id: int, record_id: int,
                        project_name: str, meta: dict):
    """将本库记录注册到 shared.db 的 skill_registry 表"""
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
              os.path.relpath(ECONOMIC_DB), json.dumps(meta, ensure_ascii=False)))
        conn.commit()
        conn.close()
    except Exception:
        pass  # shared.db 不存在时静默跳过


# ═══════════════════════════════════════════════════════
# CRUD
# ═══════════════════════════════════════════════════════

def save_analysis(
    project_name: str,
    discount_rate: float,
    periods: int,
    initial_investment: float,
    annual_revenue: float,
    annual_cost: float,
    terminal_value: float = 0,
    currency: str = "¥",
    project_id: int = None,
    npv: float = None,
    irr: float = None,
    bcr: float = None,
    roi_static: float = None,
    roi_weighted: float = None,
    pbp_static: float = None,
    pbp_dynamic: float = None,
    cashflows: list[dict] = None,
    params_json: str = None,
    db_path: str = None,
) -> int:
    """保存经济效益分析结果到 economic.db"""
    conn = _ensure_db(db_path)
    c = conn.execute("""
        INSERT INTO economic_analyses
            (project_id, project_name, discount_rate, periods,
             initial_investment, annual_revenue, annual_cost, terminal_value,
             currency, npv, irr, bcr, roi_static, roi_weighted,
             pbp_static, pbp_dynamic, cashflows_json, params_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (project_id, project_name, discount_rate, periods,
          initial_investment, annual_revenue, annual_cost, terminal_value,
          currency, npv, irr, bcr, roi_static, roi_weighted,
          pbp_static, pbp_dynamic,
          json.dumps(cashflows, ensure_ascii=False) if cashflows else None,
          params_json))
    analysis_id = c.lastrowid

    if cashflows:
        for cf in cashflows:
            conn.execute("""
                INSERT INTO economic_cashflows
                    (analysis_id, year, revenue, cost, net_cashflow, net_discounted, discounted_cost)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (analysis_id, cf["year"], cf["revenue"], cf["cost"],
                  cf["net_cashflow"], cf["net_discounted"], cf["discounted_cost"]))

    conn.commit()
    conn.close()

    # 注册到 shared.db
    meta = {"npv": npv, "irr": irr, "bcr": bcr, "discount_rate": discount_rate}
    _register_in_shared("economic", project_id, analysis_id, project_name, meta)

    print(f"  [ECON-KB] 经济效益分析已存入 (ID={analysis_id}, project={project_name})")
    return analysis_id


def get_analysis(analysis_id: int, db_path: str = None) -> Optional[dict]:
    """按 ID 查询经济效益分析记录"""
    conn = _ensure_db(db_path)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM economic_analyses WHERE id = ?",
                       (analysis_id,)).fetchone()
    if not row:
        conn.close()
        return None
    result = dict(row)
    result["cashflows"] = [
        dict(r) for r in conn.execute(
            "SELECT * FROM economic_cashflows WHERE analysis_id = ? ORDER BY year",
            (analysis_id,)).fetchall()
    ]
    conn.close()
    return result


def get_by_project(project_id: int, db_path: str = None) -> Optional[dict]:
    """按 project_id 查询经济效益分析记录"""
    conn = _ensure_db(db_path)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM economic_analyses WHERE project_id = ? ORDER BY created_at DESC LIMIT 1",
        (project_id,)).fetchone()
    if not row:
        conn.close()
        return None
    result = dict(row)
    result["cashflows"] = [
        dict(r) for r in conn.execute(
            "SELECT * FROM economic_cashflows WHERE analysis_id = ? ORDER BY year",
            (result["id"],)).fetchall()
    ]
    conn.close()
    return result


def find_by_irr(min_irr: float = 0, max_irr: float = None, limit: int = 20, db_path: str = None) -> list[dict]:
    """按 IRR 区间查询（走索引，无模糊搜索）"""
    conn = _ensure_db(db_path)
    conn.row_factory = sqlite3.Row
    conditions, params = ["irr IS NOT NULL"], [min_irr]
    if max_irr is not None:
        conditions.append("irr <= ?")
        params.append(max_irr)
    rows = conn.execute(
        f"SELECT id, project_name, discount_rate, npv, irr, bcr, pbp_static, created_at "
        f"FROM economic_analyses WHERE {' AND '.join(conditions)} AND irr >= ? "
        f"ORDER BY irr DESC LIMIT ?", params + [limit]).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def find_by_npv(min_npv: float = 0, limit: int = 20, db_path: str = None) -> list[dict]:
    """NPV >= min_npv 的记录（走索引）"""
    conn = _ensure_db(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT id, project_name, discount_rate, npv, irr, bcr, pbp_static, created_at "
        "FROM economic_analyses WHERE npv IS NOT NULL AND npv >= ? "
        "ORDER BY npv DESC LIMIT ?", (min_npv, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def list_all(limit: int = 20, db_path: str = None) -> list[dict]:
    """列出所有经济效益分析记录"""
    conn = _ensure_db(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT id, project_name, discount_rate, periods, npv, irr, bcr, created_at "
        "FROM economic_analyses ORDER BY created_at DESC LIMIT ?",
        (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ═══════════════════════════════════════════════════════
# 跨库：读 shared.db 的项目信息
# ═══════════════════════════════════════════════════════

def get_project_duration(project_id: int) -> Optional[float]:
    """从 shared.db 读取项目工期（活动历时估算的结果）"""
    if not os.path.exists(SHARED_DB):
        return None
    try:
        conn = sqlite3.connect(SHARED_DB)
        conn.execute("ATTACH DATABASE ? AS shared", (SHARED_DB,))
        row = conn.execute(
            "SELECT total_duration FROM shared.projects WHERE id = ?",
            (project_id,)).fetchone()
        conn.close()
        return row[0] if row else None
    except Exception:
        return None


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2 and sys.argv[1] == "list":
        rows = list_all()
        for r in rows:
            print(f"  [{r['id']}] {r['project_name']}: NPV={r['npv']}, IRR={r['irr']}%, BCR={r['bcr']}")
    elif len(sys.argv) >= 3 and sys.argv[1] == "get":
        r = get_analysis(int(sys.argv[2]))
        if r:
            print(f"  {r['project_name']}: i={r['discount_rate']}%, "
                  f"NPV={r['npv']}, IRR={r['irr']}%, BCR={r['bcr']}, "
                  f"PBP(静)={r['pbp_static']}, PBP(动)={r['pbp_dynamic']}")
    else:
        print("用法: python economic_knowledge.py <list|get id>")
