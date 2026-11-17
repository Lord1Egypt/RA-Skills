"""completion-report-generator每日完成报告生成器

来源: v4.0设计文档§3.5 Layer 5报告层
职责: 聚合task_result+daily_completion_report+30天WelcomeBackCard
R18统一入口: db_logger + atomic_write
R72保护: completion-report-generator Cron不可删除(R72.1)
BUG-ORCH-017修复: 修正所有SQL字段名和参数类型问题
"""

import os
import sys
import json
import asyncio
import argparse
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_SCRIPTS_DIR = _PROJECT_ROOT / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger

logger = get_logger("completion-report-generator", source="skills/completion-report-generator")

WELCOME_BACK_DAYS = 30
COMPLETION_RATE_WARNING = 0.60
COMPLETION_RATE_GOOD = 0.80


class ReportGenerator:
    """Report Generator 类"""
    def __init__(self, db_pool=None):
        self.db_pool = db_pool

    async def generate_daily_report(self, report_date: date, tenant_filter: Optional[str] = None) -> Dict[str, Any]:
        """生成 daily report

        Args:
            report_date (date): 参数说明
            tenant_filter (Optional[str]): 参数说明

        Returns:
            Dict[str, Any]: 返回值说明
        """
        try:
            if not self.db_pool:
                logger.warning("DB未连接,返回模拟报告")
                return {
                    "success": True,
                    "data": {"report_date": report_date.isoformat(), "tenants_reported": 0, "note": "DB未连接,模拟生成", "total_completed": 0, "total_failed": 0, "average_completion_rate": 0.0, "fairness_index": 1.0, "welcome_back_cards_generated": 0},
                    "error": None, "code": "DB_NOT_CONNECTED",
                }
            tenant_stats = await self._aggregate_task_results(report_date, tenant_filter)
            fairness = await self._read_fairness_index(report_date)
            # T-B12: 每日运营摘要增强(Cookie健康度+远程值守状态+今日扫码)
            cookie_health = await self._collect_cookie_health()
            guard_status = await self._collect_remote_guard_status(report_date)
            qr_scans = await self._count_qr_scans(report_date)
            daily_extras = {
                "cookie_health": cookie_health,
                "remote_guard_status": guard_status,
                "qr_scan_count": qr_scans,
            }
            reports_written = await self._write_daily_reports(report_date, tenant_stats, fairness, daily_extras)
            cards = await self._generate_welcome_back_cards(report_date)
            total_completed = sum(s["completed"] for s in tenant_stats)
            total_failed = sum(s["failed"] for s in tenant_stats)
            total_all = sum(s["total"] for s in tenant_stats)
            avg_rate = (total_completed / total_all) if total_all else 0.0
            # T-B12: 摘要格式 "Cookie健康度: X%(N绿/N黄/N红) | 远程值守状态: 正常 | 今日扫码: N次"
            cookie_summary = f"{cookie_health['health_pct']}%({cookie_health['green']}绿/{cookie_health['yellow']}黄/{cookie_health['red']}红)"
            result = {
                "report_date": report_date.isoformat(),
                "tenants_reported": reports_written,
                "total_completed": total_completed,
                "total_failed": total_failed,
                "average_completion_rate": round(avg_rate, 4),
                "fairness_index": fairness,
                "welcome_back_cards_generated": cards,
                # T-B12新增字段
                "cookie_health": cookie_summary,
                "remote_guard_status": guard_status,
                "qr_scan_count": qr_scans,
            }
            logger.info(f"日报生成完成 date={report_date} tenants={reports_written} cookie={cookie_summary} guard={guard_status} scans={qr_scans}")
            return {"success": True, "data": result, "error": None, "code": None}
        except Exception as e:
            logger.error(f"日报生成失败 date={report_date}: {e}")
            return {"success": False, "data": {}, "error": str(e), "code": "REPORT_EXCEPTION"}

    async def _aggregate_task_results(self, report_date: date, tenant_filter: Optional[str]) -> List[Dict]:
        """聚合任务结果 - 修复参数类型推断问题"""
        try:
            async with self.db_pool.acquire() as conn:
                if tenant_filter:
                    rows = await conn.fetch(
                        """SELECT tenant_id,
                                  COUNT(*) AS total,
                                  COUNT(*) FILTER (WHERE status='completed') AS completed,
                                  COUNT(*) FILTER (WHERE status='failed') AS failed,
                                  COUNT(*) FILTER (WHERE status NOT IN ('completed', 'failed')) AS pending
                           FROM task_result
                           WHERE created_at::date = $1 AND tenant_id = $2
                           GROUP BY tenant_id""",
                        report_date, tenant_filter,
                    )
                else:
                    rows = await conn.fetch(
                        """SELECT tenant_id,
                                  COUNT(*) AS total,
                                  COUNT(*) FILTER (WHERE status='completed') AS completed,
                                  COUNT(*) FILTER (WHERE status='failed') AS failed,
                                  COUNT(*) FILTER (WHERE status NOT IN ('completed', 'failed')) AS pending
                           FROM task_result
                           WHERE created_at::date = $1
                           GROUP BY tenant_id""",
                        report_date,
                    )
                return [dict(r) for r in rows]
        except Exception as e:
            logger.error(f"聚合任务结果失败: {e}")
            return []

    async def _read_fairness_index(self, report_date: date) -> float:
        """从fair_schedule_checkpoint计算Jain公平性指数"""
        try:
            async with self.db_pool.acquire() as conn:
                rows = await conn.fetch(
                    "SELECT served_count FROM fair_schedule_checkpoint WHERE reset_date=$1",
                    report_date,
                )
                if not rows:
                    return 1.0
                served_counts = [r["served_count"] or 0 for r in rows]
                if not served_counts:
                    return 1.0
                n = len(served_counts)
                sum_v = sum(served_counts)
                sum_sq = sum(v * v for v in served_counts)
                if sum_sq == 0:
                    return 1.0
                return round((sum_v ** 2) / (n * sum_sq), 4)
        except Exception as e:
            logger.error(f"读取公平性指数失败: {e}")
            return 1.0

    async def _write_daily_reports(self, report_date: date, stats: List[Dict], fairness: float, daily_extras: Optional[Dict] = None) -> int:
        """写入daily_completion_report表

        Args:
            daily_extras: T-B12新增的每日摘要数据(cookie_health/guard_status/qr_scans)
        """
        written = 0
        try:
            async with self.db_pool.acquire() as conn:
                for s in stats:
                    total = s["total"] or 0
                    completed = s["completed"] or 0
                    failed = s["failed"] or 0
                    pending = s.get("pending", 0) or 0
                    rate = (completed / total) if total else 0.0
                    note = self._build_note(rate)
                    # T-B12: content_metrics增加cookie_health/guard_status/qr_scans
                    metrics = {"note": note, "fairness_index": fairness}
                    if daily_extras:
                        metrics["daily_summary"] = daily_extras
                    await conn.execute(
                        """INSERT INTO daily_completion_report(report_id, tenant_id, report_date, total_tasks, completed_tasks, failed_tasks, pending_tasks, completion_rate, content_metrics, failure_breakdown, created_at)
                           VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,NOW())
                           ON CONFLICT (tenant_id, report_date) DO UPDATE SET total_tasks=$4, completed_tasks=$5, failed_tasks=$6, pending_tasks=$7, completion_rate=$8, content_metrics=$9, failure_breakdown=$10""",
                        f"rpt-{s['tenant_id']}-{report_date.isoformat()}", s["tenant_id"], report_date,
                        total, completed, failed, pending, round(rate, 4),
                        json.dumps(metrics, ensure_ascii=False),
                        json.dumps({"failed": failed}, ensure_ascii=False),
                    )
                    written += 1
        except Exception as e:
            logger.error(f"写入日报失败: {e}")
        return written

    async def _collect_cookie_health(self) -> Dict[str, int]:
        """T-B12: 收集Cookie健康度数据

        扫描Cookie目录,按文件修改时间判断健康度:
        - 绿: 7天内更新的Cookie文件
        - 黄: 7-14天前更新的Cookie文件
        - 红: 超过14天或无Cookie文件

        Returns:
            Dict: {green, yellow, red, total, health_pct}
        """
        green = yellow = red = 0
        try:
            cookie_dir = os.getenv("COOKIE_SAVE_DIR", str(_PROJECT_ROOT / "data" / "cookies"))
            if os.path.isdir(cookie_dir):
                today = date.today()
                for _root, _dirs, _files in os.walk(cookie_dir):
                    for f in _files:
                        if f.endswith('.json') or f.endswith('.json.enc'):
                            try:
                                mtime = os.path.getmtime(os.path.join(_root, f))
                                age_days = (today - date.fromtimestamp(mtime)).days
                                if age_days <= 7:
                                    green += 1
                                elif age_days <= 14:
                                    yellow += 1
                                else:
                                    red += 1
                            except Exception:
                                red += 1
        except Exception as e:
            logger.error(f"Cookie健康度收集失败: {e}")
        total = green + yellow + red
        health_pct = round(green / total * 100) if total else 0
        return {"green": green, "yellow": yellow, "red": red, "total": total, "health_pct": health_pct}

    async def _collect_remote_guard_status(self, report_date: date) -> str:
        """T-B12: 收集远程值守状态

        从alert_queue.jsonl统计当日CRITICAL/ERROR告警数量判断状态:
        - 正常: 当日0条CRITICAL告警
        - 降级: 当日1-5条CRITICAL告警
        - 异常: 当日>5条CRITICAL告警

        Returns:
            str: 正常/降级/异常
        """
        try:
            alert_file = _PROJECT_ROOT / "data" / "alert_queue.jsonl"
            if not alert_file.exists():
                return "正常"
            today_str = report_date.isoformat()
            critical_count = 0
            with open(alert_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        ts = entry.get("timestamp", "")
                        if ts.startswith(today_str) and entry.get("level") == "CRITICAL":
                            critical_count += 1
                    except (json.JSONDecodeError, KeyError):
                        continue
            if critical_count > 5:
                return "异常"
            elif critical_count > 0:
                return "降级"
            return "正常"
        except Exception as e:
            logger.error(f"远程值守状态收集失败: {e}")
            return "未知"

    async def _count_qr_scans(self, report_date: date) -> int:
        """T-B12: 统计当日扫码次数

        从alert_queue.jsonl统计当日包含扫码/QR/二维码关键词的告警数量

        Returns:
            int: 扫码次数
        """
        try:
            alert_file = _PROJECT_ROOT / "data" / "alert_queue.jsonl"
            if not alert_file.exists():
                return 0
            today_str = report_date.isoformat()
            scan_count = 0
            with open(alert_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        ts = entry.get("timestamp", "")
                        if ts.startswith(today_str):
                            msg = entry.get("message", "")
                            if "扫码" in msg or "QR" in msg or "二维码" in msg:
                                scan_count += 1
                    except (json.JSONDecodeError, KeyError):
                        continue
            return scan_count
        except Exception as e:
            logger.error(f"扫码次数统计失败: {e}")
            return 0

    def _build_note(self, rate: float) -> str:
        if rate < COMPLETION_RATE_WARNING:
            return "完成率偏低,建议增加配额或检查任务失败原因"
        if rate < COMPLETION_RATE_GOOD:
            return "完成率正常"
        return "完成率优秀"

    async def _generate_welcome_back_cards(self, report_date: date) -> int:
        """生成WelcomeBackCard通知"""
        cards = 0
        try:
            async with self.db_pool.acquire() as conn:
                rows = await conn.fetch(
                    """SELECT tenant_id,
                              SUM(total_tasks) AS total_30d,
                              SUM(completed_tasks) AS completed_30d,
                              SUM(failed_tasks) AS failed_30d
                       FROM daily_completion_report
                       WHERE report_date >= $1 AND report_date <= $2
                       GROUP BY tenant_id""",
                    report_date - timedelta(days=WELCOME_BACK_DAYS), report_date,
                )
                for r in rows:
                    total_30d = r["total_30d"] or 0
                    completed_30d = r["completed_30d"] or 0
                    rate = (completed_30d / total_30d) if total_30d else 0.0
                    pending = await self._count_pending_deferred(r["tenant_id"])
                    suggestion = self._build_suggestion(rate, pending)
                    await conn.execute(
                        """INSERT INTO tenant_notification(tenant_id, notification_type, level, message, payload)
                           VALUES($1, 'welcome_back', 'INFO', $2, $3)""",
                        r["tenant_id"],
                        f"30天完成率{rate:.0%},待处理{pending}项",
                        json.dumps({"days": WELCOME_BACK_DAYS, "total": total_30d, "completed": completed_30d, "failed": r["failed_30d"], "rate": round(rate, 4), "pending": pending, "suggestion": suggestion}, ensure_ascii=False),
                    )
                    cards += 1
        except Exception as e:
            logger.error(f"生成WelcomeBackCard失败: {e}")
        return cards

    async def _count_pending_deferred(self, tenant_id: str) -> int:
        """统计待处理的deferred任务"""
        try:
            async with self.db_pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT COUNT(*) AS cnt FROM deferred_task WHERE tenant_id=$1 AND status='deferred' AND deferred_until > NOW()",
                    tenant_id,
                )
                return int(row["cnt"]) if row else 0
        except Exception as e:
            logger.error(f"统计pending deferred失败: {e}")
            return 0

    def _build_suggestion(self, rate: float, pending: int) -> str:
        if rate < COMPLETION_RATE_WARNING:
            return f"30天完成率{rate:.0%}偏低,建议检查任务调度,当前待处理{pending}项"
        if rate < COMPLETION_RATE_GOOD:
            return f"30天完成率{rate:.0%}正常,当前待处理{pending}项"
        return f"30天完成率{rate:.0%}优秀,当前待处理{pending}项"


async def _get_db_pool():
    pg_dsn = os.getenv("PG_DSN")
    if not pg_dsn:
        return None
    try:
        import asyncpg
        return await asyncpg.create_pool(pg_dsn, min_size=2, max_size=10)
    except ImportError:
        # DOWNGRADE: asyncpg未安装,DB降级为跳过
        logger.warning("降级: asyncpg未安装,DB功能跳过")
        return None
    except Exception as e:
        logger.error(f"DB连接失败: {e}")
        return None


def main():
    """main"""
    parser = argparse.ArgumentParser(description="每日完成报告生成器")
    parser.add_argument("--date", default=None, help="报告日期 YYYY-MM-DD(默认今日)")
    parser.add_argument("--tenant", default=None, help="租户过滤")
    args = parser.parse_args()
    report_date = date.fromisoformat(args.date) if args.date else date.today()

    async def _run():
        pool = await _get_db_pool()
        try:
            gen = ReportGenerator(db_pool=pool)
            result = await gen.generate_daily_report(report_date, args.tenant)
            print(json.dumps(result, ensure_ascii=False, default=str))
        finally:
            if pool:
                await pool.close()

    asyncio.run(_run())


if __name__ == "__main__":
    main()