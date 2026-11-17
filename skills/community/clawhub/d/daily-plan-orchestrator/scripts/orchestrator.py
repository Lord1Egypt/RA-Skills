"""daily-plan-orchestrator每日计划编排器

来源: v4.0设计文档§3.3 Layer 2计划层
职责: 从task_template实例化daily_plan+carryover30天+DRR重置+熔断HALF_OPEN
R18统一入口: db_logger + atomic_write
R72保护: daily-plan-generator Cron不可删除(R72.1) + daily_plan表不可删除(R72.2) + carryover30天不可降级(R72.5)
"""

import os
import sys
import json
import asyncio
import uuid
import argparse
from datetime import datetime, date, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_SCRIPTS_DIR = _PROJECT_ROOT / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
try:
    from dotenv import load_dotenv; load_dotenv(str(Path(__file__).resolve().parents[3] / ".env"))
except ImportError:
    pass
from mcps.shared.db_logger import get_logger

logger = get_logger("daily-plan-orchestrator", source="skills/daily-plan-orchestrator")

MAX_CARRYOVER_DAYS = 30  # R72.5保护: 30天不可降级
MAX_CARRYOVER_PER_DAY = 5


class DailyPlanOrchestrator:
    """每日计划编排器"""

    def __init__(self, db_pool=None):
        self.db_pool = db_pool

    async def generate_daily_plan(self, plan_date: date, tenant_filter: Optional[str] = None, trigger: str = "cron") -> Dict[str, Any]:
        """生成当日计划(每日0:00 Cron触发)

        Args:
            plan_date (date): 参数说明
            tenant_filter (Optional[str]): 参数说明
            trigger (str): 参数说明

        Returns:
            Dict[str, Any]: 返回值说明
        """
        try:
            if not self.db_pool:
                logger.error("DB未连接，daily plan生成失败")
                return {
                    "success": False,
                    "data": {},
                    "error": "数据库未连接，无法生成日计划",
                    "code": "DB_NOT_CONNECTED",
                }

            templates = await self._load_active_templates(tenant_filter)
            plans_created = 0
            tenants_served = set()
            # P0修复(BUG-085): 构建tenant_id→plan_id映射,传递给task_queue创建
            # 根因: _create_task_queue_entries不设置plan_id,导致content_pregenerator
            # 的WHERE plan_id = ANY(%s)过滤返回0条结果,内容预生成链路完全断裂
            tenant_to_plan_id: Dict[str, str] = {}

            for template in templates:
                # 系统级模板(tenant_id='system')跳过daily_plan创建,仅创建task_queue
                if template.get("tenant_id") == "system":
                    continue
                plan_id = f"plan-{template['tenant_id']}-{plan_date.isoformat()}-{uuid.uuid4().hex[:6]}"
                carryover = await self._calculate_carryover(template["tenant_id"], plan_date)
                quota_total = template.get("quota_daily", 3) + carryover

                await self._create_daily_plan(
                    plan_id=plan_id,
                    tenant_id=template["tenant_id"],
                    plan_date=plan_date,
                    template_id=template["template_id"],
                    quota_total=quota_total,
                    missed_quota_carryover=carryover,
                )
                # BUG-111修复: 从DB查询实际plan_id(ON CONFLICT DO NOTHING时plan_id可能不同)
                # 根因: daily_plan已从之前运行中存在,新plan_id不会插入,但tenant_to_plan_id存的是不存在的新ID
                # 导致task_queue FK约束失败,内容预生成链路断裂
                async with self.db_pool.acquire() as conn:
                    actual_plan_id = await conn.fetchval(
                        "SELECT plan_id FROM daily_plan WHERE tenant_id = $1 AND plan_date = $2",
                        template["tenant_id"], plan_date
                    )
                if actual_plan_id:
                    tenant_to_plan_id[template["tenant_id"]] = actual_plan_id
                plans_created += 1
                tenants_served.add(template["tenant_id"])

            # 架构纠正(v10.9): scanner负责template→queue转换
            # 用户要求: "cron硬写的主要是去扫描并触发这个任务编排系统的任务"
            # daily-plan-orchestrator作为scanner,将task_template实例化为task_queue条目
            queue_created = await self._create_task_queue_entries(templates, plan_date, tenant_to_plan_id)

            carryover_count = await self._process_carryover(plan_date)
            deferred_count = await self._create_deferred_tasks(plan_date)
            expired_count = await self._expire_old_deferred(plan_date)
            await self._reset_drr_state()
            circuit_reset = await self._reset_circuit_breakers()
            # R9自生长: 应用自生长引擎积累的经验,动态调整任务优先级
            growth_adjustments = await self._apply_growth_insights(plan_date)

            logger.info(
                "daily_plan生成完成",
                extra={
                    "plan_date": plan_date.isoformat(),
                    "plans_created": plans_created,
                    "carryover": carryover_count,
                },
            )
            return {
                "success": True,
                "data": {
                    "plans_created": plans_created,
                    "tenants_served": list(tenants_served),
                    "queue_created": queue_created,
                    "carryover_count": carryover_count,
                    "deferred_count": deferred_count,
                    "expired_count": expired_count,
                    "drr_reset": True,
                    "circuit_breaker_reset": circuit_reset,
                    "growth_adjustments": growth_adjustments,
                },
                "error": None,
                "code": None,
            }
        except Exception as e:
            logger.error(f"daily_plan生成失败: {e}")
            return {"success": False, "data": {}, "error": str(e), "code": "PLAN_GENERATION_EXCEPTION"}

    async def _load_active_templates(self, tenant_filter: str = None) -> List[Dict]:
        """加载活跃模板(架构纠正v10.9: 按task_mode过滤)

        3种任务模式:
        - recurring: 每日活跃(默认模式)
        - date_range: 仅在start_date..end_date范围内活跃
        - once: 仅在execute_once_at当天活跃,且未执行过

        系统级模板(tenant_id='system')对所有租户生效,与租户模板一并加载
        """
        try:
            base_sql = """
                SELECT * FROM task_template
                WHERE is_active = TRUE
                AND (
                    (task_mode = 'recurring' OR task_mode IS NULL)
                    OR (task_mode = 'date_range'
                        AND CURRENT_DATE >= COALESCE(start_date, CURRENT_DATE)
                        AND CURRENT_DATE <= COALESCE(end_date, CURRENT_DATE))
                    OR (task_mode = 'once'
                        AND execute_once_at IS NOT NULL
                        AND execute_once_at::date = CURRENT_DATE
                        AND NOT EXISTS (
                            SELECT 1 FROM task_queue q
                            WHERE q.template_id = task_template.template_id
                            AND q.status IN ('scheduled', 'active', 'completed')
                        ))
                )
            """
            async with self.db_pool.acquire() as conn:
                if tenant_filter:
                    rows = await conn.fetch(
                        base_sql + " AND (tenant_id = $1 OR tenant_id = 'system')",
                        tenant_filter,
                    )
                else:
                    rows = await conn.fetch(base_sql)
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"加载模板失败: {e}")
            return []

    async def _create_task_queue_entries(self, templates: List[Dict], plan_date: date, plan_id_map: Dict[str, str] = None) -> int:
        """从模板创建task_queue条目(scanner核心: template→queue转换)

        架构纠正(v10.9): daily-plan-orchestrator作为scanner,将task_template实例化为task_queue条目
        用户要求: "所有定时任务应该是管理员和租户设置到数据库存储的任务编排系统,
        cron硬写的主要是去扫描并触发这个任务编排系统的任务"

        P1-ORCH修复(v10.9.2): 生成→发布时序编排
        根因: 原代码所有任务scheduled_at=midnight,不区分生成/发布时序
        用户场景: "每天11点发搞笑短视频"——生成需在11点前完成
        修复: 解析schedule_cron获取发布时间,生成任务scheduled_at=发布时间-lead_time_minutes

        P0修复(BUG-085): 设置plan_id
        根因: INSERT不包含plan_id,导致content_pregenerator的WHERE plan_id = ANY(%s)返回0条
        修复: 从plan_id_map查找tenant_id对应的plan_id并写入task_queue

        幂等性: 同一模板同一天不重复创建(检查scheduled_at::date)
        """
        created = 0
        # P1-ORCH: 第一遍创建所有任务,记录template_id→task_id映射
        template_task_map: Dict[str, str] = {}
        for template in templates:
            try:
                template_id = template["template_id"]
                tenant_id = template["tenant_id"]
                task_type = template.get("task_type", "unknown")
                pipeline_id = template.get("pipeline_id")
                priority = template.get("priority", 5)
                config = template.get("config", {})
                if isinstance(config, str):
                    config = json.loads(config)

                async with self.db_pool.acquire() as conn:
                    # 幂等检查: 同一模板同一天不重复创建
                    existing = await conn.fetchval(
                        """SELECT COUNT(*) FROM task_queue
                        WHERE template_id = $1 AND scheduled_at::date = $2""",
                        template_id,
                        plan_date,
                    )
                    if existing and existing > 0:
                        continue

                    task_id = f"tq-{tenant_id}-{plan_date.isoformat()}-{uuid.uuid4().hex[:8]}"
                    # P1-ORCH修复: 根据任务类型和依赖关系计算scheduled_at
                    scheduled_ts = self._calculate_scheduled_time(template, templates, plan_date)

                    # P0修复(BUG-085): 从plan_id_map查找plan_id
                    # 系统级模板(tenant_id='system')无daily_plan,plan_id为NULL
                    plan_id_val = plan_id_map.get(tenant_id) if plan_id_map else None

                    # P1-ORCH: 确定content_ready初始值(生成任务默认FALSE,发布任务也FALSE)
                    content_ready = False
                    # 生成任务(content_video/content_image/content_article)创建时content_ready=FALSE
                    # 发布任务(content_publish)创建时content_ready=FALSE,等生成完成后再设为TRUE
                    if task_type not in ("content_publish", "video_generation", "content_video", "content_image", "content_article", "content_generation"):
                        content_ready = True  # 非内容任务不需要等待内容就绪

                    await conn.execute(
                        """INSERT INTO task_queue
                        (task_id, tenant_id, template_id, task_type, pipeline_id,
                         status, scheduled_at, priority, payload, content_ready, plan_id)
                        VALUES ($1, $2, $3, $4, $5, 'pending', $6, $7, $8, $9, $10)""",
                        task_id,
                        tenant_id,
                        template_id,
                        task_type,
                        pipeline_id,
                        scheduled_ts,
                        priority,
                        json.dumps(config, ensure_ascii=False, default=str),
                        content_ready,
                        plan_id_val,
                    )
                    template_task_map[template_id] = task_id
                    created += 1
                    logger.info(f"task_queue条目已创建: task_id={task_id}, template={template_id}, type={task_type}, scheduled_at={scheduled_ts}")
            except Exception as e:
                logger.error(f"创建task_queue条目失败(template={template.get('template_id')}): {e}")

        # P1-ORCH: 第二遍更新依赖关系(depends_on_task_id)
        for template in templates:
            depends_on = template.get("depends_on")
            if not depends_on:
                continue
            template_id = template["template_id"]
            task_id = template_task_map.get(template_id)
            dep_task_id = template_task_map.get(depends_on)
            if task_id and dep_task_id:
                try:
                    async with self.db_pool.acquire() as conn:
                        await conn.execute(
                            "UPDATE task_queue SET depends_on_task_id = $1 WHERE task_id = $2",
                            dep_task_id,
                            task_id,
                        )
                        logger.info(f"依赖关系已建立: {task_id} depends_on {dep_task_id}")
                except Exception as e:
                    logger.warning(f"更新依赖关系失败({template_id}→{depends_on}): {e}")
        return created

    def _calculate_scheduled_time(self, template: Dict, all_templates: List[Dict], plan_date: date) -> datetime:
        """P1-ORCH: 根据任务类型和依赖关系计算scheduled_at

        逻辑:
        1. 有depends_on + lead_time_minutes: 找到依赖模板的schedule_cron,减去lead_time得到生成时间
        2. 有schedule_cron: 解析cron获取当天时间
        3. 都没有: 默认midnight UTC(保持原有行为)
        """
        from datetime import time as dt_time
        try:
            depends_on = template.get("depends_on")
            lead_time = template.get("lead_time_minutes", 0) or 0
            schedule_cron = template.get("schedule_cron", "")

            if depends_on and lead_time > 0:
                # 生成任务: 找到发布模板,解析其schedule_cron,减去lead_time
                dep_template = None
                for t in all_templates:
                    if t.get("template_id") == depends_on:
                        dep_template = t
                        break
                if dep_template:
                    dep_cron = dep_template.get("schedule_cron", "")
                    dep_time = self._parse_cron_to_datetime(dep_cron, plan_date)
                    if dep_time:
                        gen_time = dep_time - timedelta(minutes=lead_time)
                        logger.info(f"生成任务时序: {template.get('template_id')} scheduled_at={gen_time} (publish={dep_time}, lead={lead_time}min)")
                        return gen_time

            if schedule_cron:
                # 发布任务: 直接解析schedule_cron
                cron_time = self._parse_cron_to_datetime(schedule_cron, plan_date)
                if cron_time:
                    return cron_time
        except Exception as e:
            logger.warning(f"_calculate_scheduled_time失败,降级为midnight: {e}")

        # 默认: midnight UTC(保持原有行为)
        return datetime.combine(plan_date, datetime.min.time(), tzinfo=timezone.utc)

    @staticmethod
    def _parse_cron_to_datetime(cron_expr: str, plan_date: date) -> Optional[datetime]:
        """解析5字段cron表达式,返回plan_date当天的datetime

        T8修复: 支持所有cron格式(包括*/N, *, 逗号, 范围)
        支持:
        - "0 11 * * *" → 11:00 UTC
        - "30 9 * * 1" → 09:30 UTC(忽略weekday)
        - "0 */4 * * *" → 00:00 UTC(*/N首次出现=0)
        - "*/15 * * * *" → 00:00 UTC
        - "0 9,15,21 * * *" → 09:00 UTC(逗号取第一个)
        """
        if not cron_expr:
            return None
        parts = cron_expr.strip().split()
        if len(parts) < 2:
            return None

        def _parse_cron_field(field: str, max_val: int = 59) -> int:
            """解析cron字段,返回首次出现值"""
            # 取逗号前第一个值
            field = field.split(',')[0]
            # 取范围起始
            field = field.split('-')[0]
            # 处理步进: */N或N/M → 取步进前的值
            if '/' in field:
                field = field.split('/')[0]
            # 通配符 → 0
            if field == '*' or field == '':
                return 0
            return int(field)

        try:
            minute = _parse_cron_field(parts[0], 59)
            hour = _parse_cron_field(parts[1], 23)
            if 0 <= minute <= 59 and 0 <= hour <= 23:
                from datetime import time as dt_time
                return datetime.combine(plan_date, dt_time(hour=hour, minute=minute), tzinfo=timezone.utc)
        except (ValueError, IndexError):
            pass
        return None

    async def _calculate_carryover(self, tenant_id: str, plan_date: date) -> int:
        """计算carryover(前一日未完成配额)

        修复: missed=quota_total-quota_completed-quota_failed, 否则已失败任务会被
        重复计算到carryover中, 租户获得过多配额补偿
        """
        try:
            yesterday = plan_date - timedelta(days=1)
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT quota_total, quota_completed, quota_failed FROM daily_plan WHERE tenant_id=$1 AND plan_date=$2",
                    tenant_id,
                    yesterday,
                )
                if not row:
                    return 0
                quota_failed = row["quota_failed"] or 0
                missed = row["quota_total"] - row["quota_completed"] - quota_failed
                return min(max(0, missed), MAX_CARRYOVER_PER_DAY)
        except Exception as e:
            logger.error(f"计算carryover失败: {e}")
            return 0

    async def _create_daily_plan(self, plan_id, tenant_id, plan_date, template_id, quota_total, missed_quota_carryover):
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute(
                    """INSERT INTO daily_plan(plan_id, tenant_id, plan_date, template_id, quota_total, missed_quota_carryover, max_carryover_per_day, status)
                    VALUES($1, $2, $3, $4, $5, $6, $7, 'pending')
                    ON CONFLICT (tenant_id, plan_date) DO NOTHING""",
                    plan_id,
                    tenant_id,
                    plan_date,
                    template_id,
                    quota_total,
                    missed_quota_carryover,
                    MAX_CARRYOVER_PER_DAY,
                )
        except Exception as e:
            logger.error(f"创建daily_plan失败: {e}")

    async def _process_carryover(self, plan_date: date) -> int:
        """处理carryover任务(前一日未完成)

        修复: failed任务必须重置为pending+retry_count归零+清除错误信息,
        否则task-dispatcher只调度status='pending'的任务,failed任务永远不会被重新执行
        """
        try:
            yesterday = plan_date - timedelta(days=1)
            async with self.db_pool.acquire() as conn:
                rows = await conn.fetch(
                    """SELECT task_id, tenant_id, status FROM task_queue
                    WHERE status IN ('pending', 'failed')
                    AND scheduled_at::date = $1""",
                    yesterday,
                )
                for row in rows:
                    if row["status"] == "failed":
                        await conn.execute(
                            """UPDATE task_queue
                            SET status='pending', scheduled_at=$1, retry_count=0,
                                fail_category=NULL, error_message=NULL, started_at=NULL, completed_at=NULL
                            WHERE task_id=$2""",
                            datetime.now(timezone.utc),
                            row["task_id"],
                        )
                    else:
                        await conn.execute(
                            "UPDATE task_queue SET scheduled_at=$1 WHERE task_id=$2",
                            datetime.now(timezone.utc),
                            row["task_id"],
                        )
                return len(rows)
        except Exception as e:
            logger.error(f"处理carryover失败: {e}")
            return 0

    async def _create_deferred_tasks(self, plan_date: date) -> int:
        """创建deferred_task记录(超过当日未完成的)

        修复: deferred_until应基于原始deadline+1天, 而非now()+1天。
        否则延期截止日期可能比原始deadline更早, 任务被立即视为过期。
        """
        try:
            async with self.db_pool.acquire() as conn:
                rows = await conn.fetch(
                    """SELECT task_id, tenant_id, deadline FROM task_queue
                    WHERE status='pending' AND deadline < $1""",
                    plan_date,
                )
                for row in rows:
                    original_deadline = row["deadline"] or datetime.now(timezone.utc)
                    if hasattr(original_deadline, "date"):
                        deferred_until = datetime.combine(original_deadline.date() + timedelta(days=1), datetime.min.time(), tzinfo=timezone.utc)
                    else:
                        deferred_until = original_deadline + timedelta(days=1)
                    await conn.execute(
                        """INSERT INTO deferred_task(task_id, tenant_id, original_deadline, deferred_until, defer_reason, max_defer_days)
                        VALUES($1, $2, $3, $4, 'daily_carryover', $5)""",
                        row["task_id"],
                        row["tenant_id"],
                        original_deadline,
                        deferred_until,
                        MAX_CARRYOVER_DAYS,
                    )
                return len(rows)
        except Exception as e:
            logger.error(f"创建deferred_task失败: {e}")
            return 0

    async def _expire_old_deferred(self, plan_date: date) -> int:
        """过期超过30天的deferred_task(R72.5)

        修复: 应使用deferred_until字段判断过期, 而非created_at字段。
        created_at是deferred_task创建时间, deferred_until是延期截止日期。
        语义上"超过30天carryover上限"指延期截止日期已超30天。
        """
        try:
            expire_before = plan_date - timedelta(days=MAX_CARRYOVER_DAYS)
            async with self.db_pool.acquire() as conn:
                rows = await conn.fetch(
                    "UPDATE deferred_task SET status='expired' WHERE deferred_until::date < $1 AND status='deferred' RETURNING deferred_id, task_id, tenant_id",
                    expire_before,
                )
                for row in rows:
                    await conn.execute(
                        """INSERT INTO tenant_notification(tenant_id, notification_type, level, message)
                        VALUES($1, 'task_expired', 'WARNING', '任务已过期(超过30天carryover上限): ' || $2)""",
                        row["tenant_id"],
                        row["task_id"],
                    )
                return len(rows)
        except Exception as e:
            logger.error(f"过期deferred_task失败: {e}")
            return 0

    async def _reset_drr_state(self):
        """每日0:00重置DRR状态(served_count归零, deficit保留)

        修复: 增加WHERE reset_date < CURRENT_DATE条件, 防止同日Cron多次触发时重复重置served_count。
        若同日重复触发, served_count被错误归零, 会破坏DRR公平性。
        """
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute(
                    "UPDATE fair_schedule_checkpoint SET served_count=0, reset_date=CURRENT_DATE, updated_at=NOW() WHERE reset_date < CURRENT_DATE"
                )
        except Exception as e:
            logger.error(f"DRR重置失败: {e}")

    async def _reset_circuit_breakers(self) -> int:
        """每日0:00扫描熔断OPEN→HALF_OPEN

        修复: 原实现只清空fail_category字段, 但status仍为'failed'未被改为'pending'。
        task-dispatcher只调度status='pending'的任务, 因此熔断恢复机制完全无效。
        正确做法: 重置status='pending', retry_count=0, scheduled_at=NOW(), 清除错误信息。
        同时移除completed_at < NOW()-24h条件, 因为failed任务的completed_at可能为NULL。
        """
        try:
            async with self.db_pool.acquire() as conn:
                rows = await conn.fetch(
                    """UPDATE task_queue
                    SET fail_category=NULL, status='pending', retry_count=0,
                        scheduled_at=NOW(), started_at=NULL, completed_at=NULL, error_message=NULL
                    WHERE fail_category LIKE 'CIRCUIT_%' AND status='failed'
                    RETURNING task_id, tenant_id"""
                )
                for row in rows:
                    await conn.execute(
                        """INSERT INTO tenant_notification(tenant_id, notification_type, level, message)
                        VALUES($1, 'circuit_reset', 'INFO', '熔断已重置,任务已恢复调度: ' || $2)""",
                        row["tenant_id"],
                        row["task_id"],
                    )
                return len(rows)
        except Exception as e:
            logger.error(f"熔断重置失败: {e}")
            return 0

    async def _apply_growth_insights(self, plan_date: date) -> Dict[str, Any]:
        """R9新增: 从自生长引擎(agent_memory表)读取经验洞察,动态调整当日任务

        自优化+自生长闭环:
        1. 读取agent_memory中最近7天的error类经验(高重要度)→降低对应task_type优先级
        2. 读取agent_memory中最近7天的pattern类经验(高重要度)→提升对应task_type优先级
        3. 统计task_execution_log中各task_type的7天成功率→作为调度参考
        4. 将调整记录写入task_audit_log(可追溯)

        Returns:
            {"error_adjusted": int, "pattern_boosted": int, "success_rate_stats": dict}
        """
        result = {"error_adjusted": 0, "pattern_boosted": 0, "success_rate_stats": {}}
        try:
            if not self.db_pool:
                return result
            async with self.db_pool.acquire() as conn:
                # R10-P1-FIX7: 设置RLS上下文为system,允许跨租户读取agent_memory
                # 原因: orchestrator是系统级组件,需要读取所有租户的经验数据进行全局优化
                # 风险: 不设置RLS上下文可能导致查询被RLS策略拦截返回空结果
                await conn.execute("SET LOCAL app.current_tenant = 'system'")
                # 1. 查询最近7天高重要度错误经验
                error_experiences = await conn.fetch(
                    """SELECT content, summary, importance_score, owner
                    FROM agent_memory
                    WHERE category = 'error'
                      AND is_active = TRUE
                      AND created_at >= NOW() - INTERVAL '7 days'
                      AND importance_score >= 7
                      AND content::text LIKE '%task_type%'
                    ORDER BY importance_score DESC, created_at DESC
                    LIMIT 20"""
                )
                for exp in error_experiences:
                    try:
                        content = json.loads(exp["content"]) if isinstance(exp["content"], str) else exp["content"]
                        task_type = content.get("task_type", "")
                        if task_type:
                            # 降低该task_type的当日pending任务优先级
                            updated = await conn.execute(
                                "UPDATE task_queue SET priority = GREATEST(priority - 2, 1) "
                                "WHERE task_type = $1 AND status = 'pending' "
                                "AND scheduled_at::date = $2",
                                task_type, plan_date,
                            )
                            if updated and updated != "UPDATE 0":
                                result["error_adjusted"] += 1
                                # 记录审计日志
                                await conn.execute(
                                    "INSERT INTO task_audit_log (task_id, tenant_id, action, operator_type, details) "
                                    "VALUES ('SYSTEM', 'system', 'growth_priority_down', 'self_growth_engine', $1)",
                                    json.dumps({
                                        "task_type": task_type,
                                        "reason": exp["summary"][:200],
                                        "importance": exp["importance_score"]
                                    }),
                                )
                    except Exception as parse_e:
                        logger.debug(f"解析经验内容异常: {parse_e}")

                # 2. 查询最近7天高重要度成功模式
                pattern_experiences = await conn.fetch(
                    """SELECT content, summary, importance_score
                    FROM agent_memory
                    WHERE category = 'pattern'
                      AND is_active = TRUE
                      AND created_at >= NOW() - INTERVAL '7 days'
                      AND importance_score >= 8
                      AND content::text LIKE '%task_type%'
                    ORDER BY importance_score DESC
                    LIMIT 10"""
                )
                for exp in pattern_experiences:
                    try:
                        content = json.loads(exp["content"]) if isinstance(exp["content"], str) else exp["content"]
                        task_type = content.get("task_type", "")
                        if task_type:
                            updated = await conn.execute(
                                "UPDATE task_queue SET priority = LEAST(priority + 1, 10) "
                                "WHERE task_type = $1 AND status = 'pending' "
                                "AND scheduled_at::date = $2",
                                task_type, plan_date,
                            )
                            if updated and updated != "UPDATE 0":
                                result["pattern_boosted"] += 1
                    except Exception:
                        pass

                # 3. 统计task_execution_log中各task_type的7天成功率
                stats = await conn.fetch(
                    """SELECT task_type,
                           COUNT(*) FILTER (WHERE status='completed')::float /
                           NULLIF(COUNT(*), 0) as success_rate,
                           AVG(duration_ms) as avg_duration_ms
                    FROM task_execution_log
                    WHERE created_at >= NOW() - INTERVAL '7 days'
                    GROUP BY task_type"""
                )
                for s in stats:
                    result["success_rate_stats"][s["task_type"]] = {
                        "success_rate": round(float(s["success_rate"] or 0), 2),
                        "avg_duration_ms": int(s["avg_duration_ms"] or 0),
                    }

                logger.info(
                    f"[GROWTH-INSIGHTS] 自生长经验应用: "
                    f"error_adjusted={result['error_adjusted']}, "
                    f"pattern_boosted={result['pattern_boosted']}, "
                    f"stats_types={len(result['success_rate_stats'])}"
                )
        except Exception as e:
            logger.error(f"自生长经验应用失败(不影响计划生成): {e}")
        return result


async def main_async(args) -> Any:
    """main async

    Args:
        args: 参数说明

    Returns:
        Any: 返回值说明
    """
    try:
        plan_date = datetime.strptime(args.plan_date, "%Y-%m-%d").date() if args.plan_date else date.today()
    except ValueError:
        return {"success": False, "data": {}, "error": "invalid_date_format", "code": "INVALID_DATE"}

    db_pool = None
    try:
        import asyncpg
        # R7修复(DEF-ORCH-002): PG_DSN未设置时降级到DATABASE_URL(容器环境使用DATABASE_URL)
        # 根因: 与task_dispatcher_main.py相同的bug——Docker容器只有DATABASE_URL,无PG_DSN
        # 修复: 添加DATABASE_URL作为fallback,最后才用hardcoded localhost
        dsn = os.environ.get("PG_DSN", "") or os.environ.get("DATABASE_URL", "") or "postgres://postgres@localhost:15432/juejin"
        db_pool = await asyncpg.create_pool(dsn, min_size=1, max_size=5)
    except ImportError:
        logger.error("asyncpg未安装，使用模拟模式")
    except Exception as e:
        logger.error(f"DB连接失败: {e}")

    orchestrator = DailyPlanOrchestrator(db_pool)
    result = await orchestrator.generate_daily_plan(plan_date, args.tenant, args.trigger)

    if db_pool:
        await db_pool.close()
    return result


def main():
    """main"""
    parser = argparse.ArgumentParser(description="daily-plan-orchestrator每日计划编排器")
    parser.add_argument("--trigger", default="cron", choices=["cron", "manual"])
    parser.add_argument("--plan-date", default=None, help="计划日期 YYYY-MM-DD")
    parser.add_argument("--tenant", default=None)
    args = parser.parse_args()

    result = asyncio.run(main_async(args))
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
