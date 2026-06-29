"""
project_knowledge — 通用知识库引擎

功能：
1. 存储项目数据（WBS/OMP/依赖/风险/文档）
2. 存储任意知识条目（文章/资料/笔记/行业数据）
3. FTS 全文检索
4. 支持连接外部 SQLite 数据库
5. 导出/导入知识库

用法：
  # 保存项目数据
  save_project(state)
  
  # 保存任意知识条目
  save_knowledge(title, content, source="", entry_type="note",
                 tags="", domain="")
  
  # 搜索
  search(query, limit=10)
  
  # 连接外部数据库
  connect_external(db_path)  # 返回连接对象，可直接执行 SQL
  
  # 批量导入外部数据
  import_external_knowledge(db_path, table_name, mapping)
"""
import os
import json
import sqlite3
import re
from datetime import datetime
from typing import Optional, Any

# ═══════════════════════════════════════════════════════
# R-12 审计锚点：数据目录字面量声明
DEFAULT_DATA_DIR_RAW = "skills/.standardization/activity-duration-estimation/data/"
# 路径配置
# ═══════════════════════════════════════════════════════

SKILL_DIR = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".."
))
_data_path = os.path.normpath(os.path.join(
    SKILL_DIR, "..", ".standardization", "activity-duration-estimation", "data"
))
DEFAULT_DB = os.path.join(_data_path, "knowledge.db")


# ═══════════════════════════════════════════════════════
# 数据库初始化
# ═══════════════════════════════════════════════════════

def _ensure_db(db_path: str = None):
    """确保数据库结构和 FTS 索引存在"""
    path = db_path or DEFAULT_DB
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")

    conn.executescript("""
        -- ═══════════════════════════════════════════
        -- 1. 项目表
        -- ═══════════════════════════════════════════
        CREATE TABLE IF NOT EXISTS projects (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            name            TEXT NOT NULL,
            description     TEXT DEFAULT '',
            domain          TEXT DEFAULT '',
            scale           TEXT DEFAULT 'medium',
            total_duration  REAL DEFAULT 0,
            wp_count        INTEGER DEFAULT 0,
            critical_count  INTEGER DEFAULT 0,
            mc_p50          REAL DEFAULT 0,
            mc_p90          REAL DEFAULT 0,
            created_at      TEXT DEFAULT (datetime('now')),
            tags            TEXT DEFAULT ''
        );

        CREATE INDEX IF NOT EXISTS idx_proj_domain  ON projects(domain);
        CREATE INDEX IF NOT EXISTS idx_proj_created ON projects(created_at DESC);

        -- ═══════════════════════════════════════════
        -- 2. 工作包表（每个项目的任务分解）
        -- ═══════════════════════════════════════════
        CREATE TABLE IF NOT EXISTS work_packages (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id  INTEGER NOT NULL REFERENCES projects(id),
            task_name   TEXT NOT NULL,
            phase       TEXT DEFAULT '',
            o           REAL DEFAULT 0,
            m           REAL DEFAULT 0,
            p           REAL DEFAULT 0,
            deliverable TEXT DEFAULT '',
            is_critical INTEGER DEFAULT 0
        );

        CREATE INDEX IF NOT EXISTS idx_wp_project ON work_packages(project_id);

        -- ═══════════════════════════════════════════
        -- 3. 依赖关系表
        -- ═══════════════════════════════════════════
        CREATE TABLE IF NOT EXISTS dependencies (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id      INTEGER NOT NULL REFERENCES projects(id),
            task_id         INTEGER NOT NULL,
            predecessor_id  INTEGER NOT NULL,
            dep_type        TEXT DEFAULT 'FS'
        );

        CREATE INDEX IF NOT EXISTS idx_dep_project ON dependencies(project_id);

        -- ═══════════════════════════════════════════
        -- 4. 风险档案表
        -- ═══════════════════════════════════════════
        CREATE TABLE IF NOT EXISTS risk_profiles (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id  INTEGER NOT NULL REFERENCES projects(id),
            risk_type   TEXT NOT NULL,
            severity    TEXT DEFAULT 'medium',
            description TEXT DEFAULT '',
            mitigation  TEXT DEFAULT ''
        );

        -- ═══════════════════════════════════════════
        -- 5. 通用知识条目表（文章/资料/笔记/行业数据）
        -- ═══════════════════════════════════════════
        CREATE TABLE IF NOT EXISTS knowledge_entries (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            content     TEXT DEFAULT '',
            source      TEXT DEFAULT '',       -- 来源(URL/书名/人名)
            entry_type  TEXT DEFAULT 'note',   -- note/article/benchmark/industry/project_ref
            tags        TEXT DEFAULT '',       -- 逗号分隔
            domain      TEXT DEFAULT '',
            ref_link    TEXT DEFAULT '',       -- 引用链接
            created_at  TEXT DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_know_tags  ON knowledge_entries(tags);
        CREATE INDEX IF NOT EXISTS idx_know_domain ON knowledge_entries(domain);
        CREATE INDEX IF NOT EXISTS idx_know_type   ON knowledge_entries(entry_type);

        -- ═══════════════════════════════════════════
        -- 6. 任务基准表（OMP 基准积累）
        -- ═══════════════════════════════════════════
        CREATE TABLE IF NOT EXISTS task_benchmarks (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            task_pattern    TEXT NOT NULL,      -- 任务模式（如"模型微调""土方开挖"）
            domain          TEXT DEFAULT '',
            typical_o       REAL DEFAULT 0,
            typical_m       REAL DEFAULT 0,
            typical_p       REAL DEFAULT 0,
            sample_count    INTEGER DEFAULT 1,
            source_project  TEXT DEFAULT '',    -- 来源项目名
            source_id       INTEGER DEFAULT 0, -- 来源项目ID
            created_at      TEXT DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_bm_task  ON task_benchmarks(task_pattern);
        CREATE INDEX IF NOT EXISTS idx_bm_domain ON task_benchmarks(domain);

        -- ═══════════════════════════════════════════
        -- 7. FTS 全文搜索虚拟表
        -- ═══════════════════════════════════════════
        CREATE VIRTUAL TABLE IF NOT EXISTS knowledge_fts USING fts5(
            title, content, tags,
            content='knowledge_entries',
            content_rowid='id'
        );

        -- FTS 初始同步（仅首次建表时）
        INSERT OR IGNORE INTO knowledge_fts(knowledge_fts)
        SELECT 'rebuild' FROM knowledge_entries LIMIT 0;
    """)

    conn.commit()
    return conn


# ═══════════════════════════════════════════════════════
# 通用知识条目管理
# ═══════════════════════════════════════════════════════

def save_knowledge(
    title: str,
    content: str = "",
    source: str = "",
    entry_type: str = "note",
    tags: str = "",
    domain: str = "",
    ref_link: str = "",
    db_path: str = None
) -> int:
    """
    保存任意知识条目到知识库。
    
    可存任何内容：文章摘要、行业报告笔记、OMP 数据、经验总结等。
    entry_type 分类: note(笔记), article(文章), benchmark(基准数据),
                     industry(行业报告), project_ref(项目参考)
    """
    conn = _ensure_db(db_path)
    cursor = conn.execute("""
        INSERT INTO knowledge_entries (title, content, source, entry_type, tags, domain, ref_link)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (title, content, source, entry_type, tags, domain, ref_link))
    entry_id = cursor.lastrowid

    # 同步 FTS
    try:
        conn.execute("""
            INSERT INTO knowledge_fts (rowid, title, content, tags)
            VALUES (?, ?, ?, ?)
        """, (entry_id, title, content, tags))
    except sqlite3.IntegrityError:
        pass

    conn.commit()
    conn.close()
    print(f"  [KB] 已存入知识条目 (ID={entry_id}, type={entry_type}, tags={tags})")
    return entry_id


def save_knowledge_batch(
    entries: list[dict],
    db_path: str = None
) -> list[int]:
    """批量保存知识条目"""
    ids = []
    for entry in entries:
        eid = save_knowledge(
            title=entry.get("title", ""),
            content=entry.get("content", ""),
            source=entry.get("source", ""),
            entry_type=entry.get("entry_type", "note"),
            tags=entry.get("tags", ""),
            domain=entry.get("domain", ""),
            ref_link=entry.get("ref_link", ""),
            db_path=db_path
        )
        ids.append(eid)
    return ids


# ═══════════════════════════════════════════════════════
# 搜索
# ═══════════════════════════════════════════════════════

def search(
    query: str,
    limit: int = 10,
    entry_type: str = None,
    domain: str = None,
    db_path: str = None
) -> list[dict]:
    """
    全文搜索知识库。
    
    支持：
    - 通用全文搜索（标题+内容+标签）
    - 按类型过滤（entry_type）
    - 按领域过滤（domain）
    """
    conn = _ensure_db(db_path)
    conn.row_factory = sqlite3.Row

    conditions = []
    params = []

    # FTS 搜索（优先），中文内容退化为 LIKE
    if query.strip():
        try:
            conditions.append("ke.rowid IN (SELECT rowid FROM knowledge_fts WHERE knowledge_fts MATCH ?)")
            params.append(query)
        except sqlite3.OperationalError:
            # FTS5 不支持中文分词时退化
            conditions.append("(ke.title LIKE ? OR ke.content LIKE ? OR ke.tags LIKE ?)")
            params.extend([f"%{query}%"] * 3)
    if entry_type:
        conditions.append("ke.entry_type = ?")
        params.append(entry_type)
    if domain:
        conditions.append("ke.domain LIKE ?")
        params.append(f"%{domain}%")

    where = " AND ".join(conditions) if conditions else "1"
    rows = conn.execute(f"""
        SELECT ke.id, ke.title, substr(ke.content, 1, 200) as content_preview,
               ke.source, ke.entry_type, ke.tags, ke.domain, ke.created_at
        FROM knowledge_entries ke
        WHERE {where}
        ORDER BY ke.created_at DESC
        LIMIT ?
    """, params + [limit]).fetchall()

    conn.close()
    return [dict(r) for r in rows]


def search_projects(
    query: str = "",
    domain: str = "",
    limit: int = 10,
    db_path: str = None
) -> list[dict]:
    """搜索历史项目"""
    conn = _ensure_db(db_path)
    conn.row_factory = sqlite3.Row

    conditions = []
    params = []
    if query:
        conditions.append("(name LIKE ? OR description LIKE ? OR tags LIKE ?)")
        params.extend([f"%{query}%"] * 3)
    if domain:
        conditions.append("domain LIKE ?")
        params.append(f"%{domain}%")

    where = " AND ".join(conditions) if conditions else "1"
    rows = conn.execute(f"""
        SELECT id, name, domain, total_duration, wp_count, critical_count,
               mc_p50, mc_p90, created_at, tags
        FROM projects WHERE {where}
        ORDER BY created_at DESC LIMIT ?
    """, params + [limit]).fetchall()

    conn.close()
    return [dict(r) for r in rows]


# ═══════════════════════════════════════════════════════
# 项目数据管理
# ═══════════════════════════════════════════════════════

def save_project(state, db_path: str = None) -> int:
    """保存 PipelineState 中的项目数据到知识库"""
    conn = _ensure_db(db_path)
    conn.row_factory = sqlite3.Row

    domain = _infer_domain(state.project_name or "", state.phases or [])
    mc_p50, mc_p90 = 0, 0
    if hasattr(state, 'mc_results') and state.mc_results:
        q = state.mc_results.get("pert", {}).get("quantiles", {})
        mc_p50, mc_p90 = q.get("p50", 0), q.get("p90", 0)
    total_dur = state.cpm_result.project_duration if hasattr(state, 'cpm_result') and state.cpm_result else 0
    cp_count = len(state.cpm_result.critical_ids) if hasattr(state, 'cpm_result') and state.cpm_result and state.cpm_result.critical_ids else 0
    tags = ",".join(_extract_tags(state.project_name or "", state.phases or []))

    cursor = conn.execute("""
        INSERT INTO projects (name, description, domain, scale, total_duration,
                              wp_count, critical_count, mc_p50, mc_p90, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (state.project_name or "未命名", state.description or "", domain,
          "large" if len(state.phases or []) > 20 else "medium",
          total_dur, len(state.phases or []), cp_count, mc_p50, mc_p90, tags))
    pid = cursor.lastrowid

    # 存工作包 + 积累基准
    if hasattr(state, 'phases') and state.phases:
        cp_ids = set(state.cpm_result.critical_ids) if hasattr(state, 'cpm_result') and state.cpm_result and state.cpm_result.critical_ids else set()
        for i, p in enumerate(state.phases, 1):
            name = p.get("name", "")
            ph = re.match(r'^(\d+)\.', name.strip())
            phase = ph.group(1) if ph else ""
            conn.execute("""INSERT INTO work_packages (project_id, task_name, phase, o, m, p, deliverable, is_critical)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                         (pid, name, phase, p.get("o", 0), p.get("m", 0), p.get("p", 0),
                          p.get("deliverable", ""), 1 if i in cp_ids else 0))
            # 写入基准：提取核心任务名（去掉 WBS 编码前缀）
            task_core = re.sub(r'^[\d.\s]+', '', name).strip()
            if task_core and p.get("m", 0) > 0:
                _accumulate_benchmark(conn, task_core, domain, p.get("o", 0), p.get("m", 0), p.get("p", 0),
                                      state.project_name or "", pid)

    # 存依赖
    if hasattr(state, 'dependencies') and state.dependencies:
        for tid, deps in state.dependencies.items():
            for dep in (deps if isinstance(deps, list) else [deps]):
                pd = dep[0] if isinstance(dep, (list, tuple)) else dep
                dt = dep[1] if isinstance(dep, (list, tuple)) and len(dep) >= 2 else "FS"
                conn.execute("INSERT INTO dependencies (project_id, task_id, predecessor_id, dep_type) VALUES (?, ?, ?, ?)",
                             (pid, tid, pd, dt))

    conn.commit()
    conn.close()
    print(f"  [KB] 项目已存入知识库 (ID={pid}, domain={domain})")
    return pid


def _accumulate_benchmark(conn, task_pattern: str, domain: str, o: float, m: float, p: float,
                           source_project: str, source_id: int):
    """积累或更新任务基准"""
    existing = conn.execute("""
        SELECT id, typical_o, typical_m, typical_p, sample_count
        FROM task_benchmarks WHERE task_pattern=? AND domain=?
    """, (task_pattern, domain)).fetchone()

    if existing:
        n = existing["sample_count"]
        new_o = (existing["typical_o"] * n + o) / (n + 1)
        new_m = (existing["typical_m"] * n + m) / (n + 1)
        new_p = (existing["typical_p"] * n + p) / (n + 1)
        conn.execute("""
            UPDATE task_benchmarks SET typical_o=?, typical_m=?, typical_p=?,
                   sample_count=?, source_project=?, source_id=?
            WHERE id=?
        """, (new_o, new_m, new_p, n + 1, source_project, source_id, existing["id"]))
    else:
        conn.execute("""
            INSERT INTO task_benchmarks (task_pattern, domain, typical_o, typical_m, typical_p,
                                         sample_count, source_project, source_id)
            VALUES (?, ?, ?, ?, ?, 1, ?, ?)
        """, (task_pattern, domain, o, m, p, source_project, source_id))


# ═══════════════════════════════════════════════════════
# 基准查询
# ═══════════════════════════════════════════════════════

def get_benchmarks(task_pattern: str = "", domain: str = "", db_path: str = None) -> list[dict]:
    """获取任务估算基准"""
    conn = _ensure_db(db_path)
    conn.row_factory = sqlite3.Row
    conditions, params = [], []
    if task_pattern:
        conditions.append("task_pattern LIKE ?")
        params.append(f"%{task_pattern}%")
    if domain:
        conditions.append("domain LIKE ?")
        params.append(f"%{domain}%")
    where = " AND ".join(conditions) if conditions else "1"
    rows = conn.execute(f"""
        SELECT task_pattern, domain, typical_o, typical_m, typical_p, sample_count, source_project
        FROM task_benchmarks WHERE {where}
        ORDER BY sample_count DESC LIMIT 20
    """, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_dependency_patterns(domain: str = "", db_path: str = None) -> list[dict]:
    """获取最常见的依赖类型分布"""
    conn = _ensure_db(db_path)
    conn.row_factory = sqlite3.Row
    p = [f"%{domain}%"] if domain else []
    w = "p.domain LIKE ?" if domain else "1"
    rows = conn.execute(f"""
        SELECT d.dep_type, COUNT(*) as freq
        FROM dependencies d JOIN projects p ON d.project_id = p.id WHERE {w}
        GROUP BY d.dep_type ORDER BY freq DESC
    """, p).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ═══════════════════════════════════════════════════════
# 外部数据库对接
# ═══════════════════════════════════════════════════════

def connect_external(db_path: str) -> sqlite3.Connection:
    """
    连接外部 SQLite 数据库，返回连接对象。
    
    用法：
        conn = connect_external("/path/to/other.db")
        rows = conn.execute("SELECT * FROM my_table").fetchall()
        
    外部数据库可以是任意结构的 SQLite 文件，
    调用者可以自行执行 SQL 查询。
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"外部数据库不存在: {db_path}")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def import_external_knowledge(
    external_db: str,
    table_name: str,
    mapping: dict[str, str],
    db_path: str = None
) -> int:
    """
    从外部 SQLite 数据库导入知识条目。
    
    参数：
        external_db: 外部数据库路径
        table_name:  外部表名
        mapping:     字段映射 {目标字段: 外部字段}
                     支持的目标字段: title, content, source, entry_type, tags, domain, ref_link
        db_path:     目标知识库路径（默认 skill 自己的知识库）
    
    返回值: 导入的条目数
    
    示例：
        import_external_knowledge(
            "old_projects.db", "documents",
            {"title": "doc_name", "content": "doc_body", "tags": "category"}
        )
    """
    conn_ext = connect_external(external_db)
    conn_ext.row_factory = sqlite3.Row

    target_fields = ["title", "content", "source", "entry_type", "tags", "domain", "ref_link"]
    ext_cols = ", ".join(set(mapping.values()))
    rows = conn_ext.execute(f"SELECT {ext_cols} FROM {table_name}").fetchall()
    conn_ext.close()

    if not rows:
        print(f"  [KB] 外部表 {table_name} 无数据")
        return 0

    entries = []
    for row in rows:
        entry = {}
        for target, ext_field in mapping.items():
            if target in target_fields:
                entry[target] = row[ext_field] if row[ext_field] else ""
        # 补缺省值
        entry.setdefault("title", "未命名")
        entry.setdefault("content", "")
        entry.setdefault("source", external_db)
        entry.setdefault("entry_type", "imported")
        entry.setdefault("tags", "")
        entry.setdefault("domain", "")
        entry.setdefault("ref_link", "")
        entries.append(entry)

    ids = save_knowledge_batch(entries, db_path)
    print(f"  [KB] 从 {external_db}.{table_name} 导入了 {len(ids)} 条知识")
    return len(ids)


def export_knowledge(export_path: str, db_path: str = None):
    """导出知识库到指定路径（供其他工具使用）"""
    import shutil
    src = db_path or DEFAULT_DB
    if os.path.exists(src):
        shutil.copy2(src, export_path)
        print(f"  [KB] 知识库已导出: {export_path}")
        return True
    print(f"  [KB] 源知识库不存在: {src}")
    return False


# ═══════════════════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════════════════

def _infer_domain(name: str, phases: list) -> str:
    text = f"{name} {' '.join(p.get('name', '') for p in phases)}".lower()
    domains = {
        "ai-enterprise": ["ai", "智能体", "agent", "大模型", "llm", "skill", "工作流"],
        "software": ["软件", "开发", "前端", "后端", "app", "saas", "系统"],
        "construction": ["建筑", "施工", "工程", "土建", "装修", "基坑"],
        "manufacturing": ["制造", "生产", "流水线", "工厂", "装配"],
        "event": ["活动", "展会", "会议", "演出", "庆典"],
        "research": ["研究", "研发", "实验", "科研"],
    }
    for d, kws in domains.items():
        if any(k in text for k in kws):
            return d
    return "general"


def _extract_tags(name: str, phases: list) -> list[str]:
    text = f"{name} {' '.join(p.get('name', '') for p in phases)}".lower()
    tags = []
    if any(k in text for k in ["ai", "智能体", "llm", "agent"]):
        tags.append("ai")
    if any(k in text for k in ["管理", "oa", "审批", "企业"]):
        tags.append("enterprise")
    if any(k in text for k in ["开发", "架构", "编码", "测试"]):
        tags.append("software")
    if any(k in text for k in ["建筑", "施工", "装修"]):
        tags.append("construction")
    return tags


# ═══════════════════════════════════════════════════════
# 知识库管理
# ═══════════════════════════════════════════════════════

def print_summary(db_path: str = None):
    """打印知识库概览"""
    conn = _ensure_db(db_path)
    pc = conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
    kc = conn.execute("SELECT COUNT(*) FROM knowledge_entries").fetchone()[0]
    bc = conn.execute("SELECT COUNT(*) FROM task_benchmarks").fetchone()[0]
    domains = conn.execute("SELECT domain, COUNT(*) as cnt FROM projects GROUP BY domain ORDER BY cnt DESC").fetchall()
    types = conn.execute("SELECT entry_type, COUNT(*) as cnt FROM knowledge_entries GROUP BY entry_type ORDER BY cnt DESC").fetchall()
    conn.close()

    print(f"\n─── 知识库概览 ({db_path or DEFAULT_DB}) ───")
    print(f"  项目数: {pc}")
    print(f"  知识条目: {kc}")
    print(f"  任务基准: {bc} 条")
    if domains:
        print(f"  项目领域:")
        for d, c in domains:
            print(f"    {d}: {c}个")
    if types:
        print(f"  知识类型:")
        for t, c in types:
            print(f"    {t}: {c}条")


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        cmd = sys.argv[1]
        if cmd == "summary":
            print_summary()
        elif cmd == "search" and len(sys.argv) >= 3:
            rows = search(sys.argv[2], limit=20)
            for r in rows:
                print(f"[{r['entry_type']}] {r['title']} ({r['domain']})")
                print(f"    {r.get('content_preview','')[:100]}")
                print()
        elif cmd == "import" and len(sys.argv) >= 4:
            import_external_knowledge(sys.argv[2], sys.argv[3], {"title": "title", "content": "content"})
        elif cmd == "benchmarks":
            rows = get_benchmarks(domain=sys.argv[2] if len(sys.argv) > 2 else "")
            for r in rows:
                print(f"  {r['task_pattern']} ({r['domain']}): O={r['typical_o']:.1f} M={r['typical_m']:.1f} P={r['typical_p']:.1f} (n={r['sample_count']})")
        else:
            print("用法: python project_knowledge.py <summary|search|import|benchmarks>")
    else:
        print_summary()
