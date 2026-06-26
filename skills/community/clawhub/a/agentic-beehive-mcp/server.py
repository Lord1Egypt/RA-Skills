"""
Agentic Beehive MCP Server
蜂巢动态调度中枢 — 态势感知 + 分支调度 + 外在群落管理
"""

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastmcp import FastMCP

# ─── 常量 ───

BEEHIVE_DIR = Path(__file__).parent
SKILLS_DIR = BEEHIVE_DIR.parent  # agentic-engineering/
WORKSPACE_DIR = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.home() / ".openclaw" / "workspace"))
DB_PATH = BEEHIVE_DIR / "beehive.db"

# ─── 数据库 ───

def get_db():
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    return db

def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS branches (
            name TEXT PRIMARY KEY,
            status TEXT DEFAULT 'idle',
            paradigm TEXT DEFAULT '',
            description TEXT DEFAULT '',
            last_used TEXT,
            use_count INTEGER DEFAULT 0,
            effectiveness REAL DEFAULT 0.0,
            updated_at TEXT
        );
        CREATE TABLE IF NOT EXISTS colonies (
            name TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            endpoint TEXT DEFAULT '',
            status TEXT DEFAULT 'unknown',
            last_poll TEXT,
            metadata TEXT DEFAULT '{}'
        );
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            level TEXT DEFAULT 'info',
            message TEXT NOT NULL,
            created_at TEXT,
            resolved_at TEXT
        );
        CREATE TABLE IF NOT EXISTS evolution_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            target TEXT NOT NULL,
            detail TEXT DEFAULT '',
            created_at TEXT
        );
    """)
    db.commit()
    db.close()

init_db()

# ─── MCP Server ───

mcp = FastMCP(
    "agentic-beehive",
    version="1.0.0",
    instructions="蜂巢动态调度中枢 — 态势感知、分支调度、外在群落管理",
)

# ═══════════════════════════════════════
# 🏠 蜂巢工具（内部）
# ═══════════════════════════════════════

@mcp.tool()
def skill_list() -> dict:
    """列出蜂巢所有分支及其状态"""
    db = get_db()
    # 确保分支和 SKILL.md 同步
    _sync_branches(db)
    rows = db.execute("SELECT * FROM branches ORDER BY name").fetchall()
    db.close()
    return {
        "branches": [dict(r) for r in rows],
        "total": len(rows),
    }

@mcp.tool()
def skill_query(task: str, context: str = "") -> dict:
    """根据任务描述推荐最适合的分支和范式
    
    Args:
        task: 任务描述
        context: 额外上下文（可选）
    """
    db = get_db()
    _sync_branches(db)
    
    task_lower = task.lower()
    recommendations = []
    
    # 关键词匹配
    BRANCH_KEYWORDS = {
        "coding": ["代码", "编程", "开发", "code", "deploy", "bug", "实现", "build", "api", "重构"],
        "composing": ["创作", "歌曲", "音乐", "文案", "歌词", "compose", "song", "music", "写作"],
        "supervising": ["编排", "协调", "监控", "supervis", "orchestrat", "多agent", "工作流", "workflow"],
        "量化交易": ["交易", "策略", "量化", "trading", "金融", "风控", "回测", "期权", "期货"],
    }
    
    PARADIGM_KEYWORDS_TASK_DELIVERY = ["生成", "创建", "产出", "交付", "一次性", "端到端", "generate", "create", "deliver"]
    PARADIGM_KEYWORDS_STATE_MAINTENANCE = ["监控", "持续", "实时", "事件驱动", "长期", "状态机", "monitor", "stream", "event", "daemon"]
    
    for branch, keywords in BRANCH_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in task_lower)
        if score > 0:
            row = db.execute("SELECT * FROM branches WHERE name = ?", (branch,)).fetchone()
            recommendations.append({
                "branch": branch,
                "score": score,
                "status": dict(row)["status"] if row else "unknown",
                "description": dict(row)["description"] if row else "",
            })
    
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    
    # 范式判断
    paradigm = "undetermined"
    td_score = sum(1 for kw in PARADIGM_KEYWORDS_TASK_DELIVERY if kw in task_lower)
    sm_score = sum(1 for kw in PARADIGM_KEYWORDS_STATE_MAINTENANCE if kw in task_lower)
    if td_score > sm_score:
        paradigm = "task-delivery"
    elif sm_score > td_score:
        paradigm = "state-maintenance"
    
    db.close()
    
    return {
        "task": task,
        "recommended_paradigm": paradigm,
        "recommendations": recommendations[:3],
        "note": "如果 paradigm=undetermined，由 operator 根据上下文判断",
    }

@mcp.tool()
def skill_update(branch: str, status: str = None, effectiveness: float = None, description: str = None) -> dict:
    """更新分支状态
    
    Args:
        branch: 分支名称 (coding/composing/supervising/量化交易)
        status: 状态 (idle/active/completed/evolving)
        effectiveness: 效果评分 (0.0-1.0)
        description: 更新描述
    """
    db = get_db()
    row = db.execute("SELECT * FROM branches WHERE name = ?", (branch,)).fetchone()
    if not row:
        db.close()
        return {"error": f"分支 {branch} 不存在"}
    
    now = datetime.now(timezone.utc).isoformat()
    updates = {"updated_at": now}
    if status:
        updates["status"] = status
    if effectiveness is not None:
        updates["effectiveness"] = max(0.0, min(1.0, effectiveness))
    if description:
        updates["description"] = description
    if status == "active":
        updates["last_used"] = now
        db.execute("UPDATE branches SET use_count = use_count + 1 WHERE name = ?", (branch,))
    
    set_clause = ", ".join(f"{k} = ?" for k in updates)
    db.execute(f"UPDATE branches SET {set_clause} WHERE name = ?", list(updates.values()) + [branch])
    db.commit()
    
    # 记录进化日志
    db.execute(
        "INSERT INTO evolution_log (action, target, detail, created_at) VALUES (?, ?, ?, ?)",
        ("update", branch, json.dumps(updates, ensure_ascii=False), now)
    )
    db.commit()
    
    updated = db.execute("SELECT * FROM branches WHERE name = ?", (branch,)).fetchone()
    db.close()
    return {"updated": dict(updated)}

@mcp.tool()
def skill_evolve(branch: str, new_capability: str, detail: str = "") -> dict:
    """触发分支进化 — 添加新能力
    
    Args:
        branch: 分支名称
        new_capability: 新能力描述
        detail: 详细说明
    """
    db = get_db()
    now = datetime.now(timezone.utc).isoformat()
    
    db.execute(
        "INSERT INTO evolution_log (action, target, detail, created_at) VALUES (?, ?, ?, ?)",
        ("evolve", branch, json.dumps({"new_capability": new_capability, "detail": detail}, ensure_ascii=False), now)
    )
    db.execute("UPDATE branches SET status = 'evolving', updated_at = ? WHERE name = ?", (now, branch))
    db.commit()
    db.close()
    
    return {
        "branch": branch,
        "action": "evolving",
        "new_capability": new_capability,
        "note": "进化请求已记录，operator 决定是否实施",
    }


# ═══════════════════════════════════════
# 🌍 生态工具（外部）
# ═══════════════════════════════════════

@mcp.tool()
def colony_list() -> dict:
    """列出所有已注册的外在群落"""
    db = get_db()
    rows = db.execute("SELECT * FROM colonies ORDER BY type, name").fetchall()
    db.close()
    
    by_type = {}
    for r in rows:
        t = r["type"]
        if t not in by_type:
            by_type[t] = []
        by_type[t].append(dict(r))
    
    return {
        "colonies": by_type,
        "total": len(rows),
    }

@mcp.tool()
def colony_register(name: str, colony_type: str, endpoint: str = "", metadata: str = "{}") -> dict:
    """注册新的外在群落
    
    Args:
        name: 群落名称
        colony_type: 群落类型 (hive/flower_field/manuka Grove/river)
        endpoint: 连接地址（MCP/ACP URL）
        metadata: 额外元数据 JSON
    """
    TYPE_MAP = {
        "hive": "🏠 另一个蜂巢",
        "flower_field": "🌼 油菜花群落（数据源）",
        "manuka_grove": "🌿 麦卢卡树丛（专业知识）",
        "river": "🌊 河流（流式信息）",
    }
    
    if colony_type not in TYPE_MAP:
        return {"error": f"无效类型 {colony_type}，可选: {list(TYPE_MAP.keys())}"}
    
    db = get_db()
    now = datetime.now(timezone.utc).isoformat()
    
    try:
        meta = json.loads(metadata)
    except json.JSONDecodeError:
        meta = {}
    
    db.execute(
        "INSERT OR REPLACE INTO colonies (name, type, endpoint, status, last_poll, metadata) VALUES (?, ?, ?, 'registered', ?, ?)",
        (name, colony_type, endpoint, now, json.dumps(meta, ensure_ascii=False))
    )
    db.execute(
        "INSERT INTO evolution_log (action, target, detail, created_at) VALUES (?, ?, ?, ?)",
        ("colony_register", name, json.dumps({"type": colony_type, "endpoint": endpoint}, ensure_ascii=False), now)
    )
    db.commit()
    db.close()
    
    return {
        "registered": name,
        "type": colony_type,
        "display": TYPE_MAP[colony_type],
        "endpoint": endpoint,
    }

@mcp.tool()
def colony_poll(name: str) -> dict:
    """探测外在群落状态
    
    Args:
        name: 群落名称
    """
    db = get_db()
    row = db.execute("SELECT * FROM colonies WHERE name = ?", (name,)).fetchone()
    if not row:
        db.close()
        return {"error": f"群落 {name} 未注册"}
    
    now = datetime.now(timezone.utc).isoformat()
    
    # 尝试探测 endpoint
    status = "unknown"
    if row["endpoint"]:
        try:
            import httpx
            resp = httpx.get(row["endpoint"], timeout=5.0)
            status = "alive" if resp.status_code < 500 else "degraded"
        except Exception as e:
            status = f"unreachable: {type(e).__name__}"
    else:
        status = "no_endpoint"
    
    db.execute("UPDATE colonies SET status = ?, last_poll = ? WHERE name = ?", (status, now, name))
    db.commit()
    db.close()
    
    return {
        "name": name,
        "type": row["type"],
        "status": status,
        "last_poll": now,
    }

@mcp.tool()
def colony_forage(name: str, query: str) -> dict:
    """从外在群落采蜜（取数据）
    
    Args:
        name: 群落名称
        query: 查询内容
    """
    db = get_db()
    row = db.execute("SELECT * FROM colonies WHERE name = ?", (name,)).fetchone()
    if not row:
        db.close()
        return {"error": f"群落 {name} 未注册"}
    
    if not row["endpoint"]:
        db.close()
        return {"error": f"群落 {name} 没有 endpoint，无法采蜜", "suggestion": "由 operator 手动获取数据后调用 skill_update 记录结果"}
    
    # 实际采蜜逻辑根据群落类型定制
    now = datetime.now(timezone.utc).isoformat()
    db.execute("UPDATE colonies SET last_poll = ? WHERE name = ?", (now, name))
    db.commit()
    db.close()
    
    return {
        "name": name,
        "query": query,
        "note": "采蜜请求已记录。endpoint 的实际调用由 operator 或外部 pipeline 执行",
    }


# ═══════════════════════════════════════
# 📡 态势工具（全局）
# ═══════════════════════════════════════

@mcp.tool()
def status_summary() -> dict:
    """蜂巢全局态势摘要"""
    db = get_db()
    _sync_branches(db)
    
    branches = db.execute("SELECT name, status, paradigm, last_used, use_count, effectiveness FROM branches").fetchall()
    colonies = db.execute("SELECT name, type, status, last_poll FROM colonies").fetchall()
    unresolved = db.execute("SELECT * FROM alerts WHERE resolved_at IS NULL ORDER BY created_at DESC LIMIT 10").fetchall()
    recent_evolutions = db.execute("SELECT * FROM evolution_log ORDER BY created_at DESC LIMIT 5").fetchall()
    
    db.close()
    
    active_branches = [b["name"] for b in branches if b["status"] == "active"]
    alive_colonies = [c["name"] for c in colonies if c["status"] == "alive"]
    
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "branches": {
            "total": len(branches),
            "active": active_branches,
            "idle": [b["name"] for b in branches if b["status"] == "idle"],
            "evolving": [b["name"] for b in branches if b["status"] == "evolving"],
        },
        "colonies": {
            "total": len(colonies),
            "alive": alive_colonies,
            "registered": [c["name"] for c in colonies],
        },
        "alerts": {
            "unresolved_count": len(unresolved),
            "latest": [dict(a) for a in unresolved[:3]],
        },
        "recent_evolutions": [dict(e) for e in recent_evolutions],
    }

@mcp.tool()
def status_decide(task: str) -> dict:
    """范式判断 — 任务交付型 vs 状态维持型
    
    Args:
        task: 任务描述
    """
    TD_KEYWORDS = ["生成", "创建", "产出", "交付", "一次性", "端到端", "模板", "报告", "generate", "create", "deliver", "one-time", "batch"]
    SM_KEYWORDS = ["监控", "持续", "实时", "事件驱动", "长期", "状态机", "守护", "daemon", "monitor", "stream", "event", "persistent", "watch", "cron"]
    
    task_lower = task.lower()
    td = sum(1 for kw in TD_KEYWORDS if kw in task_lower)
    sm = sum(1 for kw in SM_KEYWORDS if kw in task_lower)
    
    if td > sm:
        paradigm = "task-delivery"
        framework = "CrewAI / AutoGen"
        philosophy = "做完了"
    elif sm > td:
        paradigm = "state-maintenance"
        framework = "LangGraph"
        philosophy = "一直 ready"
    else:
        paradigm = "operator-judgment"
        framework = "由 operator 根据上下文判断"
        philosophy = "—"
    
    return {
        "task": task,
        "paradigm": paradigm,
        "recommended_framework": framework,
        "philosophy": philosophy,
        "scores": {"task_delivery": td, "state_maintenance": sm},
        "insight": "状态机的存在不是为了 close task，而是为了 trigger task",
    }

@mcp.tool()
def alert_add(source: str, message: str, level: str = "info") -> dict:
    """添加告警
    
    Args:
        source: 来源
        message: 告警内容
        level: 级别 (info/warning/critical)
    """
    db = get_db()
    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        "INSERT INTO alerts (source, level, message, created_at) VALUES (?, ?, ?, ?)",
        (source, level, message, now)
    )
    db.commit()
    db.close()
    return {"created": True, "source": source, "level": level}

@mcp.tool()
def alert_resolve(alert_id: int) -> dict:
    """解决告警
    
    Args:
        alert_id: 告警 ID
    """
    db = get_db()
    now = datetime.now(timezone.utc).isoformat()
    affected = db.execute("UPDATE alerts SET resolved_at = ? WHERE id = ?", (now, alert_id)).rowcount
    db.commit()
    db.close()
    return {"resolved": affected > 0, "alert_id": alert_id}


# ═══════════════════════════════════════
# 🔧 内部工具
# ═══════════════════════════════════════

def _sync_branches(db):
    """同步 SKILL.md 中定义的分支到数据库"""
    PARADIGMS = {
        "coding": "task-delivery",
        "composing": "task-delivery",
        "supervising": "state-maintenance",
        "量化交易": "state-maintenance",
    }
    DESCRIPTIONS = {
        "coding": "代码交付、contract-first、PACT loop",
        "composing": "创作（歌曲/文案）、DeepSeek thinker → MiniMax maker 双模型管线",
        "supervising": "Agent 监督、编排逻辑、状态监控",
        "量化交易": "量化策略、交易执行、风险控制",
    }
    
    existing = {r["name"] for r in db.execute("SELECT name FROM branches").fetchall()}
    now = datetime.now(timezone.utc).isoformat()
    
    for branch, paradigm in PARADIGMS.items():
        if branch not in existing:
            db.execute(
                "INSERT INTO branches (name, status, paradigm, description, updated_at) VALUES (?, 'idle', ?, ?, ?)",
                (branch, paradigm, DESCRIPTIONS.get(branch, ""), now)
            )
    db.commit()


# ─── 入口 ───

if __name__ == "__main__":
    mcp.run()
