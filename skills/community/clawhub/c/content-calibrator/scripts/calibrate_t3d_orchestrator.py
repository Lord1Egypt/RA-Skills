#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T+3d复盘编排脚本 — P1-19修复(S-32)

目的: 消除"自生长T+3d复盘无Cron"的断裂点。
每周一Cron调用本脚本,自动:
1. 从PG tenant_publish_records读取发布3天前到7天前的内容(即T+3d~T+7d窗口)
2. 从content_stats读取这些内容的实际互动数据
3. 从data/content-calibrator/predictions/匹配预测记录
4. 调用calibrate_review.py执行预测vs实际对比
5. 聚合复盘结果写入data/content-calibrator/reviews/

统一入口(遵循18_统一入口规则):
- db_logger: 唯一日志源
- atomic_write: 复盘结果写入
- cookie_manager: 不涉及

业务规则(来源:5轮分析报告S-32 + content-calibrator SKILL.md §Cron配置):
- T+3d窗口: 发布时间在3天前到7天前(周一Cron覆盖上周发布的内容)
- 预测记录: data/content-calibrator/predictions/pred_*.json
- 复盘结果: data/content-calibrator/reviews/review_*.json
- 实际数据: PG content_stats表(views/likes/comments/shares)

注意:
- 所有失败均为非致命,跳过单条内容,不影响整体Cron
- 无预测记录的内容跳过(首次发布无预测)
"""
import json
import sys
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_PROJECT_ROOT / "scripts"))
sys.path.insert(0, str(_PROJECT_ROOT))
from mcps.shared.db_logger import get_logger
from mcps.shared.atomic_write import atomic_read_json, atomic_write_json
logger = get_logger("content-calibrator", source="skills/content-calibrator/scripts/calibrate_t3d_orchestrator.py")

PRED_DIR = _PROJECT_ROOT / "data" / "content-calibrator" / "predictions"
REVIEW_DIR = _PROJECT_ROOT / "data" / "content-calibrator" / "reviews"
CALIBRATE_REVIEW_SCRIPT = _PROJECT_ROOT / "skills" / "content-calibrator" / "scripts" / "calibrate_review.py"


def _get_pg_conn():
    """获取PG连接

    R75.2/E-3修复: 使用db_pool统一连接(替代psycopg2.connect碎片化)
    """
    try:
        from mcps.shared.db_pool import get_connection
        return get_connection()
    except Exception as e:
        logger.error(f"PG连接失败: {e}")
        return None


def _fetch_published_content_3d() -> List[Dict]:
    """读取发布3天前到7天前的内容(T+3d复盘窗口)

    Returns:
        list[dict]: [{tenant_id, publish_record_id, title, content_text, platform, published_at, content_url}]
    """
    conn = _get_pg_conn()
    if not conn:
        return []
    try:
        now = datetime.utcnow()
        t3d_ago = now - timedelta(days=3)
        t7d_ago = now - timedelta(days=7)
        with conn.cursor(cursor_factory=__import__("psycopg2").extras.RealDictCursor) as cur:
            cur.execute(
                "SELECT id, tenant_id, title, content_text, platform, published_at, content_url "
                "FROM tenant_publish_records "
                "WHERE publish_status = 'published' "
                "AND published_at IS NOT NULL "
                "AND published_at >= %s AND published_at <= %s",
                (t7d_ago, t3d_ago)
            )
            rows = cur.fetchall()
        result = []
        for row in rows:
            item = dict(row)
            if item.get("id"):
                item["publish_record_id"] = str(item["id"])
            result.append(item)
        return result
    except Exception as e:
        logger.error(f"读取发布内容失败: {e}")
        return []
    finally:
        try:
            # R75.2/E-3修复: 使用db_pool归还连接
            from mcps.shared.db_pool import return_connection
            return_connection(conn)
        except Exception as _e:
            logger.error(f"PG连接关闭失败(复盘读取): {_e}")


def _fetch_actual_stats(tenant_id: str, content_url: str) -> Dict:
    """读取内容的实际互动数据

    Args:
        tenant_id: 租户ID
        content_url: 内容URL

    Returns:
        dict: {views, likes, comments, shares}
    """
    if not tenant_id or not content_url:
        return {}
    conn = _get_pg_conn()
    if not conn:
        return {}
    try:
        with conn.cursor() as cur:
            cur.execute("SET LOCAL app.current_tenant = %s", (tenant_id,))
            cur.execute(
                "SELECT COALESCE(SUM(view_count),0) as views, "
                "COALESCE(SUM(like_count),0) as likes, "
                "COALESCE(SUM(comment_count),0) as comments, "
                "COALESCE(SUM(share_count),0) as shares "
                "FROM content_stats WHERE tenant_id = %s AND content_url = %s",
                (tenant_id, content_url)
            )
            row = cur.fetchone()
            if row:
                return {"views": int(row[0] or 0), "likes": int(row[1] or 0),
                        "comments": int(row[2] or 0), "shares": int(row[3] or 0)}
        return {}
    except Exception as e:
        logger.error(f"读取实际数据失败(tenant={tenant_id}, url={content_url}): {e}")
        return {}
    finally:
        try:
            from mcps.shared.db_pool import return_connection
            return_connection(conn)
        except Exception as _e:
            logger.error(f"PG连接关闭失败(实际数据): {_e}")


def _match_prediction(content_text: str) -> Dict:
    """匹配预测记录(按content_preview模糊匹配)

    Args:
        content_text: 内容正文

    Returns:
        dict: 预测记录,无匹配返回空dict
    """
    if not content_text or not PRED_DIR.is_dir():
        return {}
    preview = content_text[:200]
    try:
        for pred_file in sorted(PRED_DIR.glob("pred_*.json"), reverse=True):
            try:
                record = atomic_read_json(pred_file)
                # 按content_preview前100字模糊匹配
                pred_preview = (record.get("content_preview") or "")[:100]
                if pred_preview and pred_preview in content_text:
                    return record
            except (json.JSONDecodeError, IOError):
                continue
    except Exception as e:
        logger.error(f"匹配预测记录异常: {e}")
    return {}


def _run_calibrate_review(prediction: Dict, actual: Dict) -> Dict:
    """调用calibrate_review.py执行T+3d复盘

    Args:
        prediction: 预测数据
        actual: 实际数据

    Returns:
        dict: 复盘结果
    """
    pred_str = json.dumps(prediction.get("prediction", prediction), ensure_ascii=False)
    actual_str = json.dumps(actual, ensure_ascii=False)
    try:
        result = subprocess.run(
            ["python", str(CALIBRATE_REVIEW_SCRIPT), "--prediction", pred_str, "--actual", actual_str],
            capture_output=True, text=True, timeout=120, encoding="utf-8"
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            logger.warning(f"calibrate_review.py失败(returncode={result.returncode}): {result.stderr[:200]}")
            return {"success": False, "error": result.stderr[:200]}
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError) as e:
        logger.warning(f"calibrate_review.py执行异常: {e}")
        return {"success": False, "error": str(e)}


def run_t3d_review() -> Dict:
    """T+3d复盘主函数(每周一Cron调用)

    Returns:
        dict: {success, reviewed_count, skipped_count, total_count, summary}
    """
    logger.info("calibrate_t3d_orchestrator: 启动T+3d复盘")
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    contents = _fetch_published_content_3d()
    total = len(contents)
    reviewed = 0
    skipped = 0
    results = []
    for item in contents:
        tenant_id = item.get("tenant_id", "")
        content_text = item.get("content_text", "") or ""
        content_url = item.get("content_url", "") or ""
        title = item.get("title", "")
        if not content_text or not content_url:
            skipped += 1
            continue
        actual = _fetch_actual_stats(tenant_id, content_url)
        if not actual:
            logger.debug(f"跳过(无实际数据): title={title[:30]}")
            skipped += 1
            continue
        prediction_record = _match_prediction(content_text)
        if not prediction_record:
            logger.debug(f"跳过(无预测记录): title={title[:30]}")
            skipped += 1
            continue
        review_result = _run_calibrate_review(prediction_record, actual)
        if review_result.get("success"):
            reviewed += 1
            results.append({
                "title": title,
                "accuracy": review_result.get("data", {}).get("accuracy"),
                "tenant_id": tenant_id,
            })
        else:
            skipped += 1
    summary = {
        "reviewed_count": reviewed,
        "skipped_count": skipped,
        "total_count": total,
        "timestamp": datetime.now().isoformat(),
    }
    summary_file = REVIEW_DIR / f"t3d_summary_{datetime.now().strftime('%Y%m%d')}.json"
    try:
        atomic_write_json(summary_file, summary)
    except IOError as e:
        logger.warning(f"写入汇总文件失败: {e}")
    logger.error(f"calibrate_t3d_orchestrator: T+3d复盘完成, reviewed={reviewed}, skipped={skipped}, total={total}")
    return {"success": True, "data": summary, "error": None, "code": None}


def main() -> int:
    """main

    Returns:
        int: 返回值说明
    """
    result = run_t3d_review()
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
