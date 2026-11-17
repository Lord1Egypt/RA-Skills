#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""内容管线状态机 v2.0 - 统一编排器状态管理(P2-1迁移)

从content_pipeline.py迁移,新增PG优先存储+多租户支持。
11步状态机(来源:DEF-U47 P1-4管线补全):
  hotspot→copywrite→marketing_inject→material_gen→seo_optimize_pre
  →geo_optimize→qa→publish→schedule→analytics→seo_optimize

存储策略: PG优先(POSTGRES_CONNECTION_STRING/DATABASE_URL),降级到JSON文件(data/content_pipelines/)
向后兼容: 保留与content_pipeline.py完全兼容的CLI接口和函数名

来源: 31文档P2-1(合并3个内容编排器) + 05文档DEF-U46(P1/P2架构重构路线图) + 18_统一入口规则(编排→content-orchestrator)
"""
import json

import os
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

# 导入基础设施模块(paths+atomic_write,来源:scripts/目录)
_SCRIPTS_DIR = str(_PROJECT_ROOT / "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.atomic_write import atomic_write_text  # noqa: E402
from mcps.shared.db_logger import get_logger  # noqa: E402

logger = get_logger("content-orchestrator", source="skills/content-orchestrator/scripts/pipeline_state.py")

# 加载.env环境变量(确保POSTGRES_CONNECTION_STRING等可用,来源:DEF-U30)
try:
    from dotenv import load_dotenv
    _env_path = _PROJECT_ROOT / ".env"
    if _env_path.exists():
        load_dotenv(str(_env_path))
except ImportError as e:
    logger.error(f"pipeline_state: dotenv未安装,跳过.env加载: {e}")

from paths import DATA_PIPELINE as JSON_DIR  # noqa: E402

JUEJIN_HOME = Path(os.environ.get("JUEJIN_HOME", str(_PROJECT_ROOT)))
JSON_DIR.mkdir(parents=True, exist_ok=True)

# 11步状态定义(来源:DEF-U47 P1-4管线补全)
STEPS = [
    "hotspot", "copywrite", "marketing_inject", "material_gen",
    "seo_optimize_pre", "geo_optimize", "qa", "publish",
    "schedule", "analytics", "seo_optimize",
]
VALID_STEP_STATES = ["pending", "in_progress", "completed", "failed", "skipped"]

# ─── PG连接与表管理 ───────────────────────────────────────

def _get_db_conn():
    """获取PG连接,失败返回None(降级到JSON)

    R75.2/E-3修复: 使用db_pool统一连接池(替代psycopg2.connect碎片化)
    """
    try:
        from mcps.shared.db_pool import get_connection
        return get_connection()
    except Exception as e:
        logger.error(f"PG连接失败(降级到JSON): {e}")
    return None

def _ensure_pg_table(conn):
    """确保PG表存在"""
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS content_pipelines (
                    id VARCHAR(64) PRIMARY KEY,
                    title TEXT,
                    pipeline_type VARCHAR(32) DEFAULT 'manual',
                    tenant_id VARCHAR(64) DEFAULT '',
                    items_count INTEGER DEFAULT 0,
                    source VARCHAR(32) DEFAULT 'manual',
                    current_step VARCHAR(32),
                    steps JSONB DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                )
            """)
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"PG表创建失败(降级到JSON): {e}")
        return False

def _pg_store(pipeline: dict) -> bool:
    """存储管线到PG(upsert)"""
    conn = _get_db_conn()
    if not conn:
        return False
    try:
        _ensure_pg_table(conn)
        try:
            from psycopg2.extras import Json
        except ImportError:
            Json = lambda x: json.dumps(x, ensure_ascii=False)  # noqa: E731
        with conn.cursor() as cur:
            # P0-6: 设置租户上下文确保RLS生效(来源:多租户隔离规范)
            cur.execute("SET app.current_tenant = %s", (pipeline.get("tenant_id", ""),))
            cur.execute("""
                INSERT INTO content_pipelines
                    (id, title, pipeline_type, tenant_id, items_count, source, current_step, steps, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    title=EXCLUDED.title, pipeline_type=EXCLUDED.pipeline_type,
                    tenant_id=EXCLUDED.tenant_id, items_count=EXCLUDED.items_count,
                    source=EXCLUDED.source, current_step=EXCLUDED.current_step,
                    steps=EXCLUDED.steps, updated_at=EXCLUDED.updated_at
            """, (
                pipeline["id"], pipeline.get("title", ""),
                pipeline.get("pipeline_type", "manual"),
                pipeline.get("tenant_id", ""),
                pipeline.get("items_count", 0),
                pipeline.get("source", "manual"),
                pipeline.get("current_step", ""),
                Json(pipeline.get("steps", [])),
                pipeline.get("created_at", datetime.now().isoformat()),
                pipeline.get("updated_at", datetime.now().isoformat()),
            ))
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"PG存储失败(降级到JSON): {e}")
        try:
            conn.rollback()
        except Exception as rb_err:

            logger.error(f"pipeline_state: {rb_err}")
        return False
    finally:
        try:
            # R75.2/E-3修复: 使用db_pool归还连接(替代conn.close碎片化)
            from mcps.shared.db_pool import return_connection
            return_connection(conn)
        except Exception as e:

            logger.error(f"pipeline_state: {e}")

def _pg_get(pipeline_id: str, tenant_id: str = "") -> Optional[dict]:
    """从PG获取管线"""
    conn = _get_db_conn()
    if not conn:
        return None
    try:
        _ensure_pg_table(conn)
        with conn.cursor() as cur:
            # P0-6: 设置租户上下文确保RLS生效(优先使用函数参数,回退环境变量)
            # R7修复: 与line 194保持一致,添加tenant_id参数回退
            cur.execute("SET app.current_tenant = %s", (tenant_id or os.environ.get("JUEJIN_TENANT_ID", ""),))
            cur.execute("""
                SELECT id, title, pipeline_type, tenant_id, items_count,
                       source, current_step, steps, created_at, updated_at
                FROM content_pipelines WHERE id = %s
            """, (pipeline_id,))
            row = cur.fetchone()
            if not row:
                return None
            return {
                "id": row[0], "title": row[1], "pipeline_type": row[2],
                "tenant_id": row[3], "items_count": row[4], "source": row[5],
                "current_step": row[6], "steps": row[7] if isinstance(row[7], list) else json.loads(row[7] or "[]"),
                "created_at": str(row[8]) if row[8] else "", "updated_at": str(row[9]) if row[9] else "",
            }
    except Exception as e:
        logger.error(f"PG查询失败(降级到JSON): {e}")
        return None
    finally:
        try:
            from mcps.shared.db_pool import return_connection
            return_connection(conn)
        except Exception as e:

            logger.error(f"pipeline_state: {e}")

def _pg_list_active(tenant_id: str = "") -> List[dict]:
    """从PG列出活跃管线"""
    conn = _get_db_conn()
    if not conn:
        return []
    try:
        _ensure_pg_table(conn)
        with conn.cursor() as cur:
            # P0-6: 设置租户上下文确保RLS生效(来源:多租户隔离规范)
            cur.execute("SET app.current_tenant = %s", (tenant_id or os.environ.get("JUEJIN_TENANT_ID", ""),))
            if tenant_id:
                cur.execute("""
                    SELECT id, title, pipeline_type, tenant_id, items_count,
                           source, current_step, steps, created_at, updated_at
                    FROM content_pipelines
                    WHERE tenant_id = %s AND current_step IS NOT NULL
                    ORDER BY updated_at DESC
                """, (tenant_id,))
            else:
                cur.execute("""
                    SELECT id, title, pipeline_type, tenant_id, items_count,
                           source, current_step, steps, created_at, updated_at
                    FROM content_pipelines
                    WHERE current_step IS NOT NULL
                    ORDER BY updated_at DESC
                """)
            rows = cur.fetchall()
            results = []
            for row in rows:
                steps = row[7] if isinstance(row[7], list) else json.loads(row[7] or "[]")
                has_incomplete = any(s.get("status") not in ("completed",) for s in steps)
                if has_incomplete:
                    results.append({
                        "id": row[0], "title": row[1], "pipeline_type": row[2],
                        "tenant_id": row[3], "items_count": row[4], "source": row[5],
                        "current_step": row[6], "steps": steps,
                        "created_at": str(row[8]) if row[8] else "", "updated_at": str(row[9]) if row[9] else "",
                    })
            return results
    except Exception as e:
        logger.error(f"PG列表查询失败(降级到JSON): {e}")
        return []
    finally:
        try:
            from mcps.shared.db_pool import return_connection
            return_connection(conn)
        except Exception as e:

            logger.error(f"pipeline_state: {e}")

# ─── JSON降级存储 ─────────────────────────────────────────

def _pipeline_file(pipeline_id: str) -> Path:
    return JSON_DIR / f"{pipeline_id}.json"

def _json_store(pipeline: dict) -> bool:
    """存储管线到JSON文件"""
    try:
        f = _pipeline_file(pipeline["id"])
        atomic_write_text(str(f), json.dumps(pipeline, ensure_ascii=False, indent=2))
        return True
    except Exception as e:
        logger.error(f"JSON存储失败: {e}")
        return False

def _json_get(pipeline_id: str) -> Optional[dict]:
    """从JSON文件获取管线"""
    f = _pipeline_file(pipeline_id)
    if not f.exists():
        return None
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        logger.warning(f"JSON读取失败: {e}")
        return None

def _json_list_active() -> List[dict]:
    """从JSON文件列出活跃管线"""
    results = []
    for f in JSON_DIR.glob("CP-*.json"):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            has_incomplete = any(s.get("status") not in ("completed",) for s in d.get("steps", []))
            if has_incomplete:
                results.append(d)
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"损坏的pipeline文件跳过: {f.name}: {e}")
    results.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
    return results

# ─── 统一存储接口(PG优先,JSON降级) ──────────────────────

def _store(pipeline: dict) -> bool:
    """统一存储: PG优先,同时持久化JSON确保降级可用

    PG写入成功也会同步写入JSON,防止后续按ID读取时因RLS租户上下文
    (app.current_tenant)与写入时不一致导致读取失败,从而保证PG不可读
    时仍能降级到JSON。
    """
    pg_ok = _pg_store(pipeline)
    json_ok = _json_store(pipeline)
    return pg_ok or json_ok

def _fetch(pipeline_id: str) -> Optional[dict]:
    """统一获取: PG优先,失败降级到JSON"""
    p = _pg_get(pipeline_id)
    if p:
        return p
    return _json_get(pipeline_id)

def _fetch_active(tenant_id: str = "") -> List[dict]:
    """统一列出活跃: PG优先,失败降级到JSON"""
    pg_results = _pg_list_active(tenant_id)
    if pg_results:
        return pg_results
    json_results = _json_list_active()
    if tenant_id:
        json_results = [r for r in json_results if r.get("tenant_id", "") == tenant_id]
    return json_results

# ─── 核心API函数 ──────────────────────────────────────────

def create_pipeline(title: str, pipeline_type: str = "manual", tenant_id: str = "",
                    items_count: int = 0, source: str = "",
                    custom_steps: Optional[List[str]] = None) -> Optional[dict]:
    """创建管线状态记录(PG优先,JSON降级)

    Args:
        title: 管线标题
        pipeline_type: 管道类型(PL-VIDEO/E2E-DAILY等,默认manual)
        tenant_id: 租户ID(多租户隔离)
        items_count: 内容项数量
        source: 来源(manual/cron/auto等)
        custom_steps: 自定义步骤列表(为None时使用默认11步)

    Returns:
        管线dict,失败返回None
    """
    try:
        pid = f"CP-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"
        step_names = custom_steps if custom_steps else STEPS
        steps = []
        for s in step_names:
            steps.append({
                "id": s, "status": "pending",
                "started_at": None, "completed_at": None,
                "progress": "", "checkpoints": [],
                "output": None, "error": None,
            })
        pipeline = {
            "id": pid, "title": title,
            "pipeline_type": pipeline_type,
            "tenant_id": tenant_id,
            "items_count": items_count,
            "source": source or "manual",
            "current_step": step_names[0] if step_names else "",
            "steps": steps,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        if _store(pipeline):
            logger.info(f"Pipeline创建: {pid} | {title} | {len(steps)}步 | type={pipeline_type}")
            return pipeline
        return None
    except Exception as e:
        logger.error(f"Pipeline创建失败: {e}")
        logger.error(f"Exception in except block: {e}");
        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "CREATE_ERROR"}, ensure_ascii=False))
        return None

def get_pipeline(pipeline_id: str) -> Optional[dict]:
    """获取管线状态(PG优先,JSON降级)"""
    return _fetch(pipeline_id)

def update_step(pipeline_id: str, step_name: str, status: Optional[str] = None,
                progress: str = "", output: Optional[Any] = None, error: Optional[Any] = None,
                checkpoint: Optional[dict] = None) -> Optional[dict]:
    """更新步骤状态(PG优先,JSON降级)

    Args:
        pipeline_id: 管线ID
        step_name: 步骤名称(必须在管线的steps列表中)
        status: 步骤状态(pending/in_progress/completed/failed/skipped)
        progress: 进度描述
        output: 步骤输出
        error: 错误信息
        checkpoint: 检查点数据

    Returns:
        更新后的管线dict,失败返回None
    """
    try:
        p = _fetch(pipeline_id)
        if not p:
            print(f"Pipeline {pipeline_id} 不存在", file=sys.stderr)
            return None
        step_idx = None
        for i, s in enumerate(p["steps"]):
            if s["id"] == step_name:
                step_idx = i
                break
        if step_idx is None:
            print(f"无效步骤: {step_name}, 有效值: {[s['id'] for s in p['steps']]}", file=sys.stderr)
            return None
        step = p["steps"][step_idx]
        if status:
            if status not in VALID_STEP_STATES:
                print(f"无效状态: {status}, 有效值: {VALID_STEP_STATES}", file=sys.stderr)
                return None
            old_status = step["status"]
            step["status"] = status
            if status == "in_progress" and old_status != "in_progress":
                step["started_at"] = datetime.now().isoformat()
            elif status == "completed" and old_status != "completed":
                step["completed_at"] = datetime.now().isoformat()
            if status == "in_progress":
                p["current_step"] = step_name
        if progress:
            step["progress"] = progress
        if checkpoint:
            step.setdefault("checkpoints", []).append({**checkpoint, "at": datetime.now().isoformat()})
        if output:
            step["output"] = output
        if error:
            step["error"] = error
        p["updated_at"] = datetime.now().isoformat()
        if _store(p):
            completed = sum(1 for s in p["steps"] if s["status"] == "completed")
            total = len(p["steps"])
            print(f"Pipeline {pipeline_id}: Step[{step_name}]={status} | 进度: {completed}/{total}", file=sys.stderr)
            return p
        return None
    except Exception as e:
        logger.error(f"Pipeline更新失败: {e}")
        logger.error(f"Exception in except block: {e}");
        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "UPDATE_ERROR"}, ensure_ascii=False))
        return None

def list_active(tenant_id: str = "") -> List[dict]:
    """列出活跃管线(PG优先,JSON降级)

    Args:
        tenant_id: 租户ID(为空时列出所有租户的活跃管线)

    Returns:
        活跃管线列表
    """
    return _fetch_active(tenant_id)

def recover(pipeline_id: str) -> Optional[dict]:
    """恢复中断的管线 - 输出恢复报告和建议

    Args:
        pipeline_id: 管线ID

    Returns:
        管线dict,失败返回None
    """
    p = _fetch(pipeline_id)
    if not p:
        print(f"Pipeline {pipeline_id} 不存在", file=sys.stderr)
        return None
    print(f"\nPipeline {p['id']} 恢复报告", file=sys.stderr)
    print("=" * 60, file=sys.stderr)
    print(f"标题: {p['title']}", file=sys.stderr)
    print(f"类型: {p.get('pipeline_type', 'manual')}", file=sys.stderr)
    print(f"租户: {p.get('tenant_id', '(无)')}", file=sys.stderr)
    print(f"当前步骤: {p.get('current_step', '?')}", file=sys.stderr)
    print(f"创建: {p.get('created_at', '?')}", file=sys.stderr)
    print(f"更新: {p.get('updated_at', '?')}", file=sys.stderr)
    print(f"\n各步骤状态:", file=sys.stderr)
    for i, s in enumerate(p["steps"]):
        icon = {"pending": "..", "in_progress": ">>", "completed": "OK",
                "failed": "!!", "skipped": "--"}.get(s["status"], "?")
        line = f"  [{icon}] [{i+1}/{len(p['steps'])}] {s['id']}"
        if s.get("progress"):
            line += f" | {s['progress']}"
        if s.get("error"):
            line += f" | ERR:{str(s['error'])[:40]}"
        print(line, file=sys.stderr)
    next_pending = None
    for s in p["steps"]:
        if s["status"] in ("pending", "failed"):
            next_pending = s["id"]
            break
    if next_pending:
        print(f"\n建议恢复操作:", file=sys.stderr)
        print(f"  当前卡在步骤: '{p.get('current_step', '?')}'", file=sys.stderr)
        print(f"  下一步应执行: '{next_pending}'", file=sys.stderr)
        print(f"  恢复命令: pipeline_state.py update {pipeline_id} --step {next_pending} --status in_progress", file=sys.stderr)
    else:
        all_done = all(s["status"] in ("completed", "skipped") for s in p["steps"])
        if all_done:
            print(f"\nPipeline已完成所有步骤!", file=sys.stderr)
            print(f"  执行: pipeline_state.py complete {pipeline_id}", file=sys.stderr)
    return p

def complete(pipeline_id: str) -> Optional[dict]:
    """标记管线完成

    Args:
        pipeline_id: 管线ID

    Returns:
        管线dict,失败返回None
    """
    try:
        p = _fetch(pipeline_id)
        if not p:
            print(f"Pipeline {pipeline_id} 不存在", file=sys.stderr)
            return None
        p["updated_at"] = datetime.now().isoformat()
        p["current_step"] = "completed"
        if _store(p):
            print(f"Pipeline {pipeline_id} 标记完成", file=sys.stderr)
            return p
        return None
    except Exception as e:
        logger.error(f"Pipeline完成标记失败: {e}")
        return None

def redo_step(pipeline_id: str, step_name: str, clear_checkpoint: bool = True) -> dict:
    """分镜节点级重试 - 重置指定步骤及后续步骤为pending,保留已完成步骤的输出

    FE-06: 支持对失败步骤进行节点级重试。
    重试步骤后,下游步骤也需要重置(output依赖链: R43全局影响)。
    已完成步骤的输出不删除(上下文保留),checkpoint数据归档到history_checkpoints(审计追踪)。

    Args:
        pipeline_id: 管线ID
        step_name: 要重试的步骤名称(必须处于failed状态)
        clear_checkpoint: 是否清除检查点(默认True,检查点数据归档到history_checkpoints后清除)

    Returns:
        {success:bool, data:{reset_steps:list, preserved_steps:list}, error:str|null, code:str|null}
        - reset_steps: 被重置为pending的步骤ID列表(目标步骤+下游步骤)
        - preserved_steps: 目标步骤之前且已完成的步骤ID列表(输出上下文保留)
    """
    try:
        p = _fetch(pipeline_id)
        if not p:
            return {"success": False, "data": {}, "error": f"管线 '{pipeline_id}' 不存在", "code": "PIPELINE_NOT_FOUND"}

        # 定位目标步骤
        step_idx = None
        for i, s in enumerate(p["steps"]):
            if s["id"] == step_name:
                step_idx = i
                break
        if step_idx is None:
            valid_steps = [s["id"] for s in p["steps"]]
            return {"success": False, "data": {},
                    "error": f"步骤 '{step_name}' 不存在, 有效步骤: {valid_steps}",
                    "code": "STEP_NOT_FOUND"}

        # 前置检查: 只允许重试failed状态的步骤
        target_step = p["steps"][step_idx]
        if target_step["status"] != "failed":
            return {"success": False, "data": {},
                    "error": f"步骤 '{step_name}' 当前状态为 '{target_step['status']}', 仅允许重试failed状态的步骤",
                    "code": "INVALID_STEP_STATUS"}

        reset_steps = []
        preserved_steps = []

        # 收集目标步骤之前已完成的步骤(输出上下文保留,不重置)
        for i in range(step_idx):
            if p["steps"][i].get("status") == "completed":
                preserved_steps.append(p["steps"][i]["id"])

        # 重置目标步骤及所有下游步骤为pending(output依赖链: R43)
        for i in range(step_idx, len(p["steps"])):
            step = p["steps"][i]
            was_completed = step.get("status") == "completed"

            # checkpoint数据归档到history_checkpoints(保留审计追踪,非直接删除)
            if clear_checkpoint and step.get("checkpoints"):
                step.setdefault("history_checkpoints", [])
                step["history_checkpoints"].extend(step["checkpoints"])
                step["checkpoints"] = []

            # 重置状态字段
            step["status"] = "pending"
            step["started_at"] = None
            step["completed_at"] = None
            step["error"] = None
            step["progress"] = ""

            # 上下文保留: 已完成步骤的输出不删除(R74反敷衍: 真实保留,非注释/pass)
            if not was_completed:
                step["output"] = None

            reset_steps.append(step["id"])

        # 更新current_step指向重试的步骤
        p["current_step"] = step_name
        p["updated_at"] = datetime.now().isoformat()

        if _store(p):
            logger.info(f"Pipeline {pipeline_id}: redo_step('{step_name}') | "
                        f"reset={reset_steps} | preserved={preserved_steps}")
            return {
                "success": True,
                "data": {
                    "reset_steps": reset_steps,
                    "preserved_steps": preserved_steps,
                },
                "error": None,
                "code": None,
            }
        return {"success": False, "data": {}, "error": "管线存储失败", "code": "STORE_ERROR"}
    except Exception as e:
        logger.error(f"redo_step失败: {e}")
        return {"success": False, "data": {}, "error": str(e), "code": "REDO_ERROR"}

# ─── 向后兼容别名(供content_pipeline.py薄包装层使用) ──────

def create(title: str, items_count: int = 0, source: str = "") -> Optional[dict]:
    """[向后兼容] 创建管线 - 委托给create_pipeline"""
    return create_pipeline(title=title, items_count=items_count, source=source)

def get(pipeline_id: str) -> Optional[dict]:
    """[向后兼容] 获取管线 - 委托给get_pipeline"""
    return get_pipeline(pipeline_id)

# ─── CLI入口(与content_pipeline.py完全兼容) ──────────────

def main():
    """CLI入口(与content_pipeline.py完全兼容)

    供content_pipeline.py薄包装层调用。
    """
    if len(sys.argv) < 2:
        print("用法:", file=sys.stderr)
        print("  pipeline_state.py create --title '标题' [--items-count N] [--pipeline-type PL-VIDEO] [--tenant-id xxx]", file=sys.stderr)
        print("  pipeline_state.py update <id> --step <step_id> [--status pending|in_progress|completed|failed] [--progress '文本'] [--checkpoint '{json}']", file=sys.stderr)
        print("  pipeline_state.py list [--active] [--tenant-id xxx]", file=sys.stderr)
        print("  pipeline_state.py recover <id>", file=sys.stderr)
        print("  pipeline_state.py complete <id>", file=sys.stderr)
        print("  pipeline_state.py redo <id> <step_id> [--no-clear-checkpoint]", file=sys.stderr)
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "create":
        title = ""
        count = 0
        ptype = "manual"
        tenant = ""
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--title" and i + 1 < len(sys.argv):
                title = sys.argv[i + 1]; i += 2
            elif sys.argv[i] == "--items-count" and i + 1 < len(sys.argv):
                count = int(sys.argv[i + 1]); i += 2
            elif sys.argv[i] == "--pipeline-type" and i + 1 < len(sys.argv):
                ptype = sys.argv[i + 1]; i += 2
            elif sys.argv[i] == "--tenant-id" and i + 1 < len(sys.argv):
                tenant = sys.argv[i + 1]; i += 2
            else:
                i += 1
        create_pipeline(title or "未命名Pipeline", ptype, tenant, count)

    elif cmd == "update":
        pid = sys.argv[2]
        step = status = progress = None
        checkpoint = None
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--step" and i + 1 < len(sys.argv):
                step = sys.argv[i + 1]; i += 2
            elif sys.argv[i] == "--status" and i + 1 < len(sys.argv):
                status = sys.argv[i + 1]; i += 2
            elif sys.argv[i] == "--progress" and i + 1 < len(sys.argv):
                progress = sys.argv[i + 1]; i += 2
            elif sys.argv[i] == "--checkpoint" and i + 1 < len(sys.argv):
                raw_cp = sys.argv[i + 1]
                if raw_cp.startswith("@"):
                    checkpoint = json.loads(Path(raw_cp[1:]).read_text(encoding="utf-8-sig"))
                else:
                    try:
                        checkpoint = json.loads(raw_cp)
                    except json.JSONDecodeError:
                        logger.error(f"--checkpoint JSON格式无效,建议使用 --checkpoint @filepath")
                        sys.exit(1)
                i += 2
            else:
                i += 2
        update_step(pid, step, status, progress, checkpoint=checkpoint)

    elif cmd == "list":
        active = "--active" in sys.argv
        tenant = ""
        for j, arg in enumerate(sys.argv):
            if arg == "--tenant-id" and j + 1 < len(sys.argv):
                tenant = sys.argv[j + 1]
        if active:
            items = list_active(tenant)
            print(json.dumps({"success": True, "data": {"pipelines": items[:20], "count": len(items)}}, ensure_ascii=False))
        else:
            all_pipelines = []
            for f in sorted(JSON_DIR.glob("CP-*.json")):
                try:
                    d = json.loads(f.read_text(encoding="utf-8"))
                    all_pipelines.append(d)
                except Exception as e:

                    logger.error(f"pipeline_state: {e}")
            print(json.dumps({"success": True, "data": {"pipelines": all_pipelines, "count": len(all_pipelines)}}, ensure_ascii=False))

    elif cmd == "recover":
        recover(sys.argv[2])

    elif cmd == "complete":
        complete(sys.argv[2])

    elif cmd == "redo":
        if len(sys.argv) < 4:
            print("用法: pipeline_state.py redo <id> <step_id> [--no-clear-checkpoint]", file=sys.stderr)
            sys.exit(1)
        pid = sys.argv[2]
        step = sys.argv[3]
        clear_ckpt = "--no-clear-checkpoint" not in sys.argv
        result = redo_step(pid, step, clear_checkpoint=clear_ckpt)
        print(json.dumps(result, ensure_ascii=False))

    else:
        print(f"未知命令: {cmd}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
