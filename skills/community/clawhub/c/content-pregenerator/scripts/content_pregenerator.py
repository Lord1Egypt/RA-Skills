#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""内容预生成器 v1.0 -- 凌晨低谷期批量预生成内容(ADR-004, R72.3/R20/R74.4/R25)"""
import argparse, json, os, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
_PROJECT_ROOT = Path(__file__).resolve().parents[3]  # skills/content-pregenerator/scripts/ → project root
sys.path.insert(0, str(_PROJECT_ROOT))
try:
    from dotenv import load_dotenv; load_dotenv(str(_PROJECT_ROOT / ".env"))
except ImportError:
    pass
from psycopg2.extras import Json
from mcps.shared.db_pool import get_connection, return_connection
from mcps.shared.db_logger import get_logger
from mcps.shared.atomic_write import atomic_read_json
from mcps.shared.constants import TENANTS_CACHE_PATH
logger = get_logger("system", source="skills/content-pregenerator/scripts/content_pregenerator.py")
# R75.1统一路径: data/agency/tenants_cache.json→TENANTS_CACHE_PATH(mcps.shared.constants权威源)
TENANT_REGISTRY = Path(TENANTS_CACHE_PATH)
ORCHESTRATOR_SCRIPT = str(_PROJECT_ROOT / "skills" / "content-orchestrator" / "scripts" / "content_orchestrator.py")
DEGRADATION_CHAIN = ["PL-VIDEO", "PL-IMAGE", "PL-ARTICLE-BATCH"]
RETRY_DELAYS = [5, 15, 45]
MAX_RETRIES = 3
JAIN_THRESHOLD = 0.8
# P0修复(BUG-088): "TEXT"不是有效管道类型,改为PL-ARTICLE-BATCH
# 支持的管道: PL-VIDEO/PL-IMAGE/PL-ARTICLE-BATCH/PL-NOVEL/PL-NEWS/PL-COMIC等
TASK_TYPE_MAP = {"content_video": "PL-VIDEO", "video_generation": "PL-VIDEO",
                 "content_image": "PL-IMAGE", "content_article": "PL-ARTICLE-BATCH",
                 "content_generation": "PL-ARTICLE-BATCH"}
def load_active_tenants() -> List[Dict[str, Any]]:
    """加载活跃租户(PG优先+JSON降级, R75.2统一连接)

    P0修复(BUG-086): 原仅读tenants_cache.json(可能为空/过期)
    修复: 优先从PG加载(通过tenant_store), 降级到JSON文件
    """
    try:
        from mcps.shared.tenant_store import load_all_tenants
        all_tenants = load_all_tenants()
        if isinstance(all_tenants, dict):
            tenants = list(all_tenants.values())
        elif isinstance(all_tenants, list):
            tenants = all_tenants
        else:
            tenants = []
        active = [t for t in tenants if t.get("status") == "active"]
        if active:
            return active
        logger.warning("[PREGEN] tenant_store返回0活跃租户,降级到JSON文件")
    except Exception as e:
        logger.warning(f"[PREGEN] tenant_store加载失败(降级到JSON): {e}")
    # 降级: 读取tenants_cache.json
    if not TENANT_REGISTRY.exists():
        return []
    data = atomic_read_json(str(TENANT_REGISTRY), default={})
    tenants = data.get("tenants", []) if isinstance(data, dict) else []
    if isinstance(tenants, dict):
        tenants = list(tenants.values())
    return [t for t in tenants if t.get("status") == "active"]
def load_tasks(mode: str, tenant_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """加载任务(batch=daily_plan+task_queue, retry=content_pre_cache失败任务)"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            if mode == "retry":
                sql = ("SELECT content_id, tenant_id, pipeline_type, task_id, retry_count "
                       "FROM content_pre_cache WHERE plan_date = CURRENT_DATE "
                       "AND status IN ('generate_failed', 'timeout')")
                p: tuple = ()
                if tenant_filter:
                    sql += " AND tenant_id = %s"; p = (tenant_filter,)
                cur.execute(sql, p)
                return [{"content_id": r[0], "tenant_id": r[1], "pipeline_id": r[2], "task_id": r[3],
                         "retry_count": r[4] or 0, "task_type": "", "priority": 5,
                         "scheduled_at": None, "payload": {}} for r in cur.fetchall()]
            if tenant_filter:
                cur.execute("SELECT plan_id FROM daily_plan WHERE plan_date = CURRENT_DATE "
                            "AND status = 'pending' AND tenant_id = %s", (tenant_filter,))
            else:
                cur.execute("SELECT plan_id FROM daily_plan WHERE plan_date = CURRENT_DATE AND status = 'pending'")
            plan_ids = [r[0] for r in cur.fetchall()]
            if not plan_ids:
                return []
            cur.execute("SELECT task_id, tenant_id, plan_id, task_type, pipeline_id, priority, "
                        "scheduled_at, payload FROM task_queue WHERE plan_id = ANY(%s) AND status = 'pending' "
                        "AND task_type IN ('content_video', 'video_generation', 'content_image', "
                        "'content_article', 'content_generation')", (plan_ids,))
            return [{"task_id": r[0], "tenant_id": r[1], "plan_id": r[2], "task_type": r[3], "pipeline_id": r[4],
                     "priority": r[5], "scheduled_at": r[6], "payload": r[7] or {}} for r in cur.fetchall()]
    finally:
        return_connection(conn)
def drr_schedule(tasks: List[Dict], tenants: List[Dict]) -> List[Dict]:
    """DRR三阶段调度(R72.3): 保障→公平→竞争, 合并去重"""
    if not tasks:
        return []
    tenant_ids = {t.get("tenant_id") for t in tenants}
    task_map = {t["task_id"]: t for t in tasks}
    # Phase 1: 保障 -- 每租户至少1个任务(防饥饿)
    guarantee = [next((t["task_id"] for t in tasks if t["tenant_id"] == tid), None) for tid in tenant_ids]
    guarantee = [g for g in guarantee if g]
    # Phase 2: 公平 -- JOIN fair_schedule_checkpoint ORDER BY deficit DESC, served_count ASC
    fair: List[str] = []
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT t.task_id FROM task_queue t LEFT JOIN fair_schedule_checkpoint f "
                        "ON t.tenant_id = f.tenant_id WHERE t.task_id = ANY(%s) AND t.status = 'pending' "
                        "ORDER BY COALESCE(f.deficit, 0) DESC, COALESCE(f.served_count, 0) ASC",
                        ([t["task_id"] for t in tasks],))
            fair = [r[0] for r in cur.fetchall()]
    finally:
        return_connection(conn)
    # Phase 3: 竞争 -- ORDER BY priority DESC, scheduled_at ASC
    compete = sorted([t["task_id"] for t in tasks],
                     key=lambda tid: (-task_map[tid].get("priority", 5),
                                      task_map[tid].get("scheduled_at") or datetime.min))
    seen, scheduled = set(), []
    for tid_list in (guarantee, fair, compete):
        for tid in tid_list:
            if tid not in seen and tid in task_map:
                seen.add(tid); scheduled.append(task_map[tid])
    return scheduled
# BUG-V43-CRON-020修复: 表名白名单校验,防止SQL注入(f-string插值表名)
_ALLOWED_TABLES = {"content_pre_cache", "task_queue"}

def _db_update(table: str, set_fields: Dict[str, Any], where: str, where_vals: tuple) -> None:
    """通用DB更新(自动处理NOW()/Json)"""
    if table not in _ALLOWED_TABLES:
        raise ValueError(f"非法表名: {table}")
    parts, vals = [], []
    for k, v in set_fields.items():
        if v == "NOW()":
            parts.append(f"{k} = NOW()")
        elif isinstance(v, (dict, list)):
            parts.append(f"{k} = %s"); vals.append(Json(v))
        else:
            parts.append(f"{k} = %s"); vals.append(v)
    vals.extend(where_vals)
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(f"UPDATE {table} SET {', '.join(parts)} WHERE {where}", vals)
        conn.commit()
    except Exception as e:
        logger.error(f"_db_update更新失败: {e}")
        conn.rollback(); raise
    finally:
        return_connection(conn)
def insert_pre_cache(task: Dict) -> str:
    """插入content_pre_cache(status='generating'), 返回content_id"""
    content_id = f"pre_{task['task_id']}_{int(time.time())}"
    pipe = task.get("pipeline_id") or TASK_TYPE_MAP.get(task["task_type"], "TEXT")
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO content_pre_cache (content_id, tenant_id, plan_date, pipeline_type, "
                        "task_id, status) VALUES (%s, %s, CURRENT_DATE, %s, %s, 'generating') "
                        "ON CONFLICT (content_id) DO NOTHING",
                        (content_id, task["tenant_id"], pipe, task["task_id"]))
        conn.commit()
    except Exception as e:
        logger.error(f"insert_pre_cache插入失败: {e}")
        conn.rollback(); raise
    finally:
        return_connection(conn)
    return content_id
def execute_pipeline(pipeline_type: str, tenant_id: str) -> Dict[str, Any]:
    """调用content-orchestrator执行管道(仅生成,跳过发布)"""
    # P0修复(BUG-087): 原调用参数错误(--tenant应为--params中tenant_id, 缺少--action)
    # 正确调用: --action orchestrate --pipeline TYPE --params '{"tenant_id":"xxx"}'
    params = json.dumps({"tenant_id": tenant_id})
    cmd = [sys.executable, ORCHESTRATOR_SCRIPT, "--action", "orchestrate", "--pipeline", pipeline_type, "--params", params]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=300,
                           encoding="utf-8", errors="replace", cwd=str(_PROJECT_ROOT))
        if r.returncode == 0 and r.stdout.strip():
            try:
                return json.loads(r.stdout)
            except json.JSONDecodeError:
                return {"success": False, "error": f"非JSON: {r.stdout.strip()[:200]}", "code": "INVALID_OUTPUT"}
        return {"success": False, "error": (r.stderr or r.stdout)[:200] or "无输出", "code": "ORCHESTRATOR_FAIL"}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "管道执行超时(300s)", "code": "PIPELINE_TIMEOUT"}
    except Exception as e:
        logger.error(f"run_pipeline subprocess failed: {e}")
        return {"success": False, "error": str(e)[:200], "code": "SUBPROCESS_ERROR"}
def process_task(task: Dict, content_id: str) -> Dict[str, Any]:
    """执行单任务(含重试+降级链 PL-VIDEO→PL-IMAGE→TEXT)"""
    pipe = task.get("pipeline_id") or TASK_TYPE_MAP.get(task["task_type"], "TEXT")
    degrade_path = DEGRADATION_CHAIN[DEGRADATION_CHAIN.index(pipe):] if pipe in DEGRADATION_CHAIN else [pipe]
    result = {"content_id": content_id, "task_id": task["task_id"], "tenant_id": task["tenant_id"],
              "status": "generate_failed", "downgraded": False, "downgraded_from": None, "downgraded_to": None}
    total_attempts = 0
    for idx, current_pipe in enumerate(degrade_path):
        if idx > 0:  # 降级(R74.4: downgraded+downgraded_from+downgraded_to)
            result.update(downgraded=True, downgraded_from=degrade_path[0], downgraded_to=current_pipe)
            _db_update("content_pre_cache", {"downgraded": True, "downgraded_from": degrade_path[0],
                        "downgraded_to": current_pipe}, "content_id = %s", (content_id,))
            logger.warning(f"[PREGEN] 任务{task['task_id']}降级: {degrade_path[0]}->{current_pipe}")
        for attempt in range(MAX_RETRIES):  # 指数退避 5s/15s/45s
            if attempt > 0:
                time.sleep(RETRY_DELAYS[min(attempt - 1, len(RETRY_DELAYS) - 1)])
            total_attempts += 1
            pr = execute_pipeline(current_pipe, task["tenant_id"])
            if pr.get("success"):
                data = pr.get("data", {})
                final = data.get("final_output", {}) if isinstance(data, dict) else {}
                url = final.get("content_url") or final.get("url") or ""
                score = final.get("quality_score") or final.get("score")
                meta = {"pipeline_name": data.get("pipeline_name"), "steps_completed": data.get("steps_completed"),
                        "final_output": final}
                fields: Dict[str, Any] = {"status": "ready", "content_url": url, "content_meta": meta,
                                           "ready_at": "NOW()", "retry_count": total_attempts - 1}
                if score is not None:
                    fields["quality_score"] = score
                _db_update("content_pre_cache", fields, "content_id = %s", (content_id,))
                # P0修复(BUG-084): 同步更新task_queue.content_ready=TRUE
                # 根因: content_pre_cache.status='ready'但task_queue.content_ready仍为FALSE
                # 导致DRR调度器跳过所有content_publish任务(content_ready=FALSE被过滤)
                # 修复: 生成成功后同步标记task_queue.content_ready=TRUE,使发布任务可被调度
                # BUG-110修复: 同时标记status=completed,防止dispatcher重复执行已预生成的任务
                try:
                    _db_update("task_queue", {"content_ready": True, "status": "completed", "completed_at": "NOW()"}, "task_id = %s", (task["task_id"],))
                    logger.info(f"[CONTENT-READY] task_queue标记完成: task_id={task['task_id']}, tenant={task['tenant_id']}, content_ready=TRUE, status=completed")
                except Exception as e:
                    logger.warning(f"[CONTENT-READY] 更新task_queue失败({task['task_id']}): {e}")
                # P0修复(BUG-084续): 同步标记同租户的content_publish任务content_ready=TRUE
                # 根因: content_generation和content_publish是task_queue中两条独立记录
                # 预生成器只处理content_generation任务,但content_publish任务也需要content_ready=TRUE
                # 否则DRR调度器永远跳过content_publish任务(content_ready=FALSE被过滤)
                # 修复: 生成成功后,同步设置同租户+系统级content_publish任务为content_ready=TRUE
                # 系统级content_publish任务(tenant_id='system')负责发布所有租户的内容,也需标记
                # BUG-124修复: 原使用`scheduled_at::date = CURRENT_DATE`导致跨日任务无法同步
                # 根因: 预生成器在08-13凌晨运行为08-14生成内容时,CURRENT_DATE=08-13,
                #        但content_publish任务的scheduled_at=08-14,WHERE条件不匹配→content_ready永远为FALSE
                # 修复: 移除日期过滤,内容已生成则同租户所有pending的content_publish任务均标记为ready
                # R7日志埋点: 先查询待更新数量,再执行更新,排查content_ready同步是否生效
                try:
                    _publish_count = 0
                    _conn = get_connection()
                    try:
                        with _conn.cursor() as _cur:
                            _cur.execute("SELECT COUNT(*) FROM task_queue WHERE tenant_id = %s AND task_type = %s AND status = %s AND content_ready = FALSE",
                                        (task["tenant_id"], "content_publish", "pending"))
                            _publish_count = _cur.fetchone()[0]
                    finally:
                        return_connection(_conn)
                    logger.info(f"[CONTENT-READY] 待同步content_publish: tenant={task['tenant_id']}, pending_unready={_publish_count}")
                    _db_update("task_queue", {"content_ready": True},
                               "tenant_id = %s AND task_type = %s AND status = %s",
                               (task["tenant_id"], "content_publish", "pending"))
                    logger.info(f"[CONTENT-READY] 同租户content_publish同步完成: tenant={task['tenant_id']}, synced={_publish_count}")
                except Exception as e:
                    logger.warning(f"[CONTENT-READY] 同步content_publish content_ready失败(tenant={task['tenant_id']}): {e}")
                try:
                    _sys_count = 0
                    _conn = get_connection()
                    try:
                        with _conn.cursor() as _cur:
                            _cur.execute("SELECT COUNT(*) FROM task_queue WHERE tenant_id = %s AND task_type = %s AND status = %s AND content_ready = FALSE",
                                        ("system", "content_publish", "pending"))
                            _sys_count = _cur.fetchone()[0]
                    finally:
                        return_connection(_conn)
                    logger.info(f"[CONTENT-READY] 待同步系统级content_publish: pending_unready={_sys_count}")
                    _db_update("task_queue", {"content_ready": True},
                               "tenant_id = %s AND task_type = %s AND status = %s",
                               ("system", "content_publish", "pending"))
                    logger.info(f"[CONTENT-READY] 系统级content_publish同步完成: synced={_sys_count}")
                except Exception as e:
                    logger.warning(f"[CONTENT-READY] 同步系统级content_publish content_ready失败: {e}")
                result["status"] = "ready"
                return result
            logger.warning(f"[PREGEN] {task['task_id']}管道{current_pipe}第{attempt+1}次失败: {pr.get('error', '')[:100]}")
    _db_update("content_pre_cache", {"status": "generate_failed", "fail_category": "PIPELINE_EXHAUSTED",
                "retry_count": total_attempts}, "content_id = %s", (content_id,))
    return result
def calculate_jain_index(counts: Dict[str, int]) -> float:
    """Jain公平性指数: (sum(x))^2 / (n * sum(x^2)), 均匀=1.0"""
    vals = list(counts.values())
    n = len(vals)
    if n == 0:
        return 1.0
    s, s2 = sum(vals), sum(v * v for v in vals)
    return (s * s) / (n * s2) if s2 > 0 else 1.0
def run_pregenerator(args) -> Dict[str, Any]:
    """主执行: 加载→DRR调度→并发执行→Jain→摘要"""
    start = time.time()
    deadline = start + args.timeout
    tenants = load_active_tenants()
    if args.tenant:
        tenants = [t for t in tenants if t.get("tenant_id") == args.tenant]
    if not tenants:
        return {"success": True, "data": {"total_tasks": 0, "generated": 0, "failed": 0, "downgraded": 0,
                "timeout": 0, "jain_index": 1.0, "tenants_served": 0, "duration_ms": 0}, "error": None, "code": None}
    tasks = load_tasks(args.mode, args.tenant)
    if not tasks:
        logger.info("[PREGEN] 当日无pending内容任务")
        return {"success": True, "data": {"total_tasks": 0, "generated": 0, "failed": 0, "downgraded": 0,
                "timeout": 0, "jain_index": 1.0, "tenants_served": len(tenants),
                "duration_ms": int((time.time() - start) * 1000)}, "error": None, "code": None}
    scheduled = drr_schedule(tasks, tenants)
    logger.info(f"[PREGEN] DRR调度: {len(scheduled)}个任务, {len(tenants)}个租户")
    tenant_ids = {t.get("tenant_id") for t in tenants}
    semaphores = {tid: threading.Semaphore(args.max_concurrent) for tid in tenant_ids}
    results: List[Dict] = []
    def _worker(task: Dict) -> Dict:
        tid = task["tenant_id"]
        sem = semaphores.get(tid)
        if sem:
            sem.acquire()
        try:
            # BUG-123修复(R2-Risk1): 预生成开始时设置task_queue.status='generating',
            # 防止dispatcher-cycle在02:00重复调度同一任务(竞态条件)
            _db_update("task_queue", {"status": "generating"}, "task_id = %s", (task["task_id"],))
            if "content_id" in task:  # retry模式: 复用已有content_id
                cid = task["content_id"]
                _db_update("content_pre_cache", {"status": "generating"}, "content_id = %s", (cid,))
            else:
                cid = insert_pre_cache(task)
            return process_task(task, cid)
        except Exception as e:
            logger.error(f"[PREGEN] 任务{task['task_id']}异常: {e}", exc_info=True)
            # 异常时回退status为pending,允许retry Cron补生成
            try:
                _db_update("task_queue", {"status": "pending"}, "task_id = %s", (task["task_id"],))
            except Exception:
                pass
            return {"task_id": task["task_id"], "tenant_id": tid, "status": "generate_failed"}
        finally:
            if sem:
                sem.release()
    # BUG-112修复: 并发worker数受DB连接池大小约束,防止"connection pool exhausted"
    # 根因: max_workers=min(2*11,16)=16,但DB_POOL_MAXCONN=3,4个并发任务即耗尽连接池
    _db_pool_max = int(os.environ.get("DB_POOL_MAXCONN", "3"))
    max_workers = min(args.max_concurrent * len(tenant_ids), 16, _db_pool_max)
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_map = {pool.submit(_worker, t): t for t in scheduled}
        for future in as_completed(future_map):
            if time.time() > deadline:  # 总体窗口超时(14400s=4h)
                for f in future_map:
                    f.cancel()
                break
            try:
                results.append(future.result(timeout=max(1, int(deadline - time.time()))))
            except Exception as e:
                logger.error(f"pregenerator worker task failed (task_id={future_map[future].get('task_id', '?')}): {e}")
                t = future_map[future]
                results.append({"task_id": t["task_id"], "tenant_id": t["tenant_id"],
                                "status": "generate_failed", "error": str(e)[:200]})
    # 标记超时任务(未出现在结果中的)
    processed = {r.get("task_id") for r in results}
    timeout_ids = [t["task_id"] for t in scheduled if t["task_id"] not in processed]
    timeout_count = 0
    if timeout_ids:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("UPDATE content_pre_cache SET status = 'timeout' WHERE task_id = ANY(%s) "
                            "AND status = 'generating'", (timeout_ids,))
            conn.commit()
            timeout_count = cur.rowcount
        except Exception as e:
            logger.error(f"标记超时任务失败: {e}")
            conn.rollback()
        finally:
            return_connection(conn)
    # 统计 + Jain公平性指数(R72.3)
    generated = sum(1 for r in results if r.get("status") == "ready")
    failed = sum(1 for r in results if r.get("status") == "generate_failed")
    downgraded = sum(1 for r in results if r.get("downgraded"))
    tenant_gen: Dict[str, int] = {tid: 0 for tid in tenant_ids}
    for r in results:
        if r.get("status") == "ready":
            tenant_gen[r.get("tenant_id", "")] = tenant_gen.get(r.get("tenant_id", ""), 0) + 1
    jain = calculate_jain_index(tenant_gen)
    if jain < JAIN_THRESHOLD:
        logger.warning(f"[PREGEN] Jain={jain:.3f} < {JAIN_THRESHOLD}, 调度极不均匀")
    duration_ms = int((time.time() - start) * 1000)
    total = len(scheduled)
    success = failed == 0 and timeout_count == 0
    logger.info(f"[PREGEN] 完成: total={total} gen={generated} fail={failed} down={downgraded} timeout={timeout_count} jain={jain:.3f} {duration_ms}ms")
    return {"success": success, "data": {"total_tasks": total, "generated": generated, "failed": failed,
            "downgraded": downgraded, "timeout": timeout_count, "jain_index": round(jain, 4),
            "tenants_served": len(tenant_ids), "duration_ms": duration_ms},
            "error": None if success else f"{failed}失败,{timeout_count}超时",
            "code": None if success else "PARTIAL_FAIL"}
def main() -> int:
    parser = argparse.ArgumentParser(description="内容预生成器 (凌晨低谷期批量预生成)")
    parser.add_argument("--mode", choices=["batch", "retry"], default="batch", help="batch=全量, retry=补生成失败")
    parser.add_argument("--tenant", help="指定租户ID(不指定则全部)")
    parser.add_argument("--max-concurrent", type=int, default=2, help="租户级并发上限(默认2)")
    parser.add_argument("--timeout", type=int, default=14400, help="总体超时秒数(默认14400=4小时)")
    args = parser.parse_args()
    try:
        result = run_pregenerator(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["success"] else 1
    except ValueError as e:
        logger.error(f"[PREGEN] 参数错误: {e}"); print(json.dumps({"success": False, "data": {}, "error": str(e)[:200], "code": "VALUE_ERROR"})); return 1
    except Exception as e:
        logger.error(f"[PREGEN] 预生成异常: {e}", exc_info=True); print(json.dumps({"success": False, "data": {}, "error": f"{type(e).__name__}: {e}"[:200], "code": "EXEC_ERROR"})); return 2
if __name__ == "__main__":
    try: sys.exit(main())
    except KeyboardInterrupt: sys.exit(130)
