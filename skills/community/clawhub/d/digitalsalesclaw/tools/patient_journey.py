#!/usr/bin/env python3
"""
DigitalSalesClaw - patient_journey.py
患者旅程统一事件查询工具

基于 patient_journey_events + patient_journeys 统一模型，
提供：
  - 旅程重建（任意患者的完整触达→转化路径）
  - 旅程列表（按患者/转化状态筛选）
  - 多旅程对比（横向对比多个患者旅程）

输入: {"action": "reconstruct|list|compare|summary", "patient_id": "...", "journey_id": "..."}
输出: {journey, events, analysis}
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent


# ─────────────────────────────────────────
# 查询
# ─────────────────────────────────────────

def reconstruct_journey(patient_id: str = None, journey_id: str = None, conn=None) -> dict:
    """
    重现患者从首次触达到转化的完整旅程
    输入 patient_id 或 journey_id
    """
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        if journey_id:
            jrn = conn.execute(
                "SELECT * FROM patient_journeys WHERE journey_id = ?", (journey_id,)
            ).fetchone()
            jid = journey_id
        elif patient_id:
            jrn = conn.execute(
                "SELECT * FROM patient_journeys WHERE patient_id = ? ORDER BY first_event_at DESC LIMIT 1",
                (patient_id,)
            ).fetchone()
            jid = jrn["journey_id"] if jrn else None
        else:
            return {"error": "patient_id or journey_id required"}

        if not jrn:
            return {"error": f"Journey not found: {journey_id or patient_id}"}

        cols = [d[0] for d in conn.execute("SELECT * FROM patient_journeys LIMIT 0").description]
        journey = dict(zip(cols, jrn))

        # 获取该旅程所有事件（按时间顺序）
        events = conn.execute("""
            SELECT * FROM patient_journey_events
            WHERE journey_id = ?
            ORDER BY timestamp ASC, event_index ASC
        """, (jid,)).fetchall()

        cols = [d[0] for d in conn.execute("SELECT * FROM patient_journey_events LIMIT 0").description]
        event_list = [dict(zip(cols, r)) for r in events]

        # 旅程分析
        touchpoints = [e for e in event_list if e["event_type"] == "touchpoint"]
        conversions = [e for e in event_list if e["event_type"] == "conversion"]

        # 渠道分析
        channels = defaultdict(lambda: {"count": 0, "first": None, "last": None})
        for e in touchpoints:
            ch = e.get("channel") or "unknown"
            channels[ch]["count"] += 1
            if channels[ch]["first"] is None:
                channels[ch]["first"] = e["timestamp"]
            channels[ch]["last"] = e["timestamp"]

        # 时长分析
        if journey.get("first_event_at") and journey.get("last_event_at"):
            try:
                first = datetime.fromisoformat(journey["first_event_at"])
                last = datetime.fromisoformat(journey["last_event_at"])
                duration_days = (last - first).days
            except Exception:
                duration_days = None
        else:
            duration_days = None

        # 首次触达渠道
        first_touch = touchpoints[0] if touchpoints else None

        # 末次触达渠道（转化前最后一个）
        last_touch_before_conv = None
        if conversions and touchpoints:
            first_conv_ts = min(datetime.fromisoformat(c["timestamp"]) for c in conversions)
            for t in reversed(touchpoints):
                if datetime.fromisoformat(t["timestamp"]) < first_conv_ts:
                    last_touch_before_conv = t
                    break

        # 归因推断（简化：末次触达归因）
        attributed_channel = last_touch_before_conv["channel"] if last_touch_before_conv else (touchpoints[-1]["channel"] if touchpoints else None)

        return {
            "journey_id": jid,
            "patient_id": journey.get("patient_id"),
            "conversion": {
                "converted": bool(journey.get("conversion_flag")),
                "value": journey.get("conversion_value") or 0,
                "count": len(conversions),
            },
            "touchpoints": {
                "total": len(touchpoints),
                "channels": {ch: dict(v) for ch, v in channels.items()},
            },
            "timeline": {
                "duration_days": duration_days,
                "first_event": journey.get("first_event_at"),
                "last_event": journey.get("last_event_at"),
            },
            "attribution": {
                "model": "last_touch",
                "attributed_channel": attributed_channel,
                "first_touch_channel": first_touch["channel"] if first_touch else None,
            },
            "events": [
                {
                    "id": e["id"],
                    "event_type": e["event_type"],
                    "channel": e["channel"],
                    "platform": e["platform"],
                    "touchpoint_type": e.get("touchpoint_type"),
                    "timestamp": e["timestamp"],
                    "value": e.get("value"),
                }
                for e in event_list
            ],
            "suggestions": [
                f"患者旅程共 {len(touchpoints)} 个触点 + {len(conversions)} 次转化",
                f"首次触达渠道: {first_touch['channel'] if first_touch else '未知'}",
                f"末次触达归因: {attributed_channel}",
                f"转化价值: ¥{journey.get('conversion_value', 0):.2f}" if journey.get("conversion_flag") else "未转化",
            ]
        }
    finally:
        if own_conn:
            conn.close()


def list_journeys(patient_id: str = None, converted_only: bool = False,
                   limit: int = 50, conn=None) -> dict:
    """查询旅程列表"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        sql = "SELECT * FROM patient_journeys WHERE 1=1"
        params = []
        if patient_id:
            sql += " AND patient_id = ?"
            params.append(patient_id)
        if converted_only:
            sql += " AND conversion_flag = 1"
        sql += " ORDER BY last_event_at DESC LIMIT ?"
        params.append(limit)

        rows = conn.execute(sql, params).fetchall()
        cols = [d[0] for d in conn.execute("SELECT * FROM patient_journeys LIMIT 0").description]
        journeys = [dict(zip(cols, r)) for r in rows]

        converted = [j for j in journeys if j.get("conversion_flag")]
        not_converted = [j for j in journeys if not j.get("conversion_flag")]

        # 汇总统计
        if converted:
            total_conv_value = sum(j.get("conversion_value", 0) for j in converted)
            avg_conv_value = total_conv_value / len(converted)
        else:
            total_conv_value = avg_conv_value = 0

        return {
            "total": len(journeys),
            "converted": len(converted),
            "not_converted": len(not_converted),
            "total_conversion_value": round(total_conv_value, 2),
            "avg_conversion_value": round(avg_conv_value, 2),
            "journeys": [
                {
                    "journey_id": j["journey_id"],
                    "patient_id": j["patient_id"],
                    "first_event": j["first_event_at"],
                    "last_event": j["last_event_at"],
                    "converted": bool(j["conversion_flag"]),
                    "conversion_value": j.get("conversion_value") or 0,
                    "touchpoint_count": j.get("touchpoint_count") or 0,
                    "channels": json.loads(j.get("channels_json") or "[]"),
                }
                for j in journeys
            ],
            "suggestions": [
                f"共 {len(journeys)} 条旅程，{len(converted)} 条已转化",
                f"平均转化价值: ¥{avg_conv_value:.2f}",
            ]
        }
    finally:
        if own_conn:
            conn.close()


def compare_journeys(journey_ids: list[str] = None, conn=None) -> dict:
    """横向对比多条旅程"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        if not journey_ids:
            # 默认取最近5条
            rows = conn.execute("""
                SELECT journey_id FROM patient_journeys
                ORDER BY last_event_at DESC LIMIT 5
            """).fetchall()
            journey_ids = [r[0] for r in rows]

        journeys = []
        for jid in journey_ids:
            jrn = conn.execute(
                "SELECT * FROM patient_journeys WHERE journey_id = ?", (jid,)
            ).fetchone()
            if jrn:
                cols = [d[0] for d in conn.execute("SELECT * FROM patient_journeys LIMIT 0").description]
                journeys.append(dict(zip(cols, jrn)))

        # 计算指标对比
        metrics = []
        for j in journeys:
            metrics.append({
                "journey_id": j["journey_id"],
                "patient_id": j["patient_id"],
                "converted": bool(j["conversion_flag"]),
                "conversion_value": j.get("conversion_value") or 0,
                "touchpoint_count": j.get("touchpoint_count") or 0,
                "channels": json.loads(j.get("channels_json") or "[]"),
                "duration_days": None,
            })

            if j.get("first_event_at") and j.get("last_event_at"):
                try:
                    first = datetime.fromisoformat(j["first_event_at"])
                    last = datetime.fromisoformat(j["last_event_at"])
                    metrics[-1]["duration_days"] = (last - first).days
                except Exception:
                    pass

        # 统计
        converted = [m for m in metrics if m["converted"]]
        not_converted = [m for m in metrics if not m["converted"]]
        avg_touchpoints = sum(m["touchpoint_count"] for m in metrics) / len(metrics) if metrics else 0

        return {
            "journey_count": len(journeys),
            "converted_count": len(converted),
            "avg_touchpoints": round(avg_touchpoints, 1),
            "metrics": sorted(metrics, key=lambda x: -x["conversion_value"]),
            "comparison": {
                "converted_rate": round(len(converted) / len(metrics) * 100, 1) if metrics else 0,
                "total_value": sum(m["conversion_value"] for m in converted),
                "avg_touchpoints_converted": (
                    sum(m["touchpoint_count"] for m in converted) / len(converted)
                    if converted else 0
                ),
                "avg_touchpoints_not_converted": (
                    sum(m["touchpoint_count"] for m in not_converted) / len(not_converted)
                    if not_converted else 0
                ),
            },
            "insights": [
                f"已转化旅程 {len(converted)}/{len(metrics)} 条",
                f"已转化旅程平均触点: {sum(m['touchpoint_count'] for m in converted)/len(converted):.1f} 个"
                if converted else "暂无转化数据",
                f"未转化旅程平均触点: {sum(m['touchpoint_count'] for m in not_converted)/len(not_converted):.1f} 个"
                if not_converted else "",
                "触点越多不一定转化越高，需关注触达质量而非数量"
            ]
        }
    finally:
        if own_conn:
            conn.close()


def journey_summary(conn=None) -> dict:
    """全局旅程汇总统计"""
    own_conn = False
    if conn is None:
        conn = get_conn()
        own_conn = True

    try:
        total = conn.execute("SELECT COUNT(*) FROM patient_journeys").fetchone()[0]
        converted = conn.execute("SELECT COUNT(*) FROM patient_journeys WHERE conversion_flag=1").fetchone()[0]
        total_value = conn.execute("SELECT SUM(conversion_value) FROM patient_journeys WHERE conversion_flag=1").fetchone()[0] or 0
        total_touchpoints = conn.execute("SELECT SUM(touchpoint_count) FROM patient_journeys").fetchone()[0] or 0

        avg_tp = total_touchpoints / total if total > 0 else 0
        avg_value = total_value / converted if converted > 0 else 0
        conv_rate = converted / total * 100 if total > 0 else 0

        # 渠道分布
        channel_dist = conn.execute("""
            SELECT channel, COUNT(*) as cnt
            FROM patient_journey_events
            WHERE event_type='touchpoint' AND channel IS NOT NULL
            GROUP BY channel
            ORDER BY cnt DESC
        """).fetchall()

        # 触点类型分布
        type_dist = conn.execute("""
            SELECT touchpoint_type, COUNT(*) as cnt
            FROM patient_journey_events
            WHERE event_type='touchpoint' AND touchpoint_type IS NOT NULL
            GROUP BY touchpoint_type
            ORDER BY cnt DESC
        """).fetchall()

        return {
            "total_journeys": total,
            "converted_journeys": converted,
            "conversion_rate": round(conv_rate, 2),
            "total_conversion_value": round(total_value, 2),
            "avg_conversion_value": round(avg_value, 2),
            "avg_touchpoints_per_journey": round(avg_tp, 1),
            "channel_distribution": [{"channel": r[0], "count": r[1]} for r in channel_dist],
            "touchpoint_type_distribution": [{"type": r[0], "count": r[1]} for r in type_dist],
            "suggestions": [
                f"整体转化率: {conv_rate:.1f}%",
                f"平均触点: {avg_tp:.1f}个/旅程",
                f"平均转化价值: ¥{avg_value:.2f}",
                f"主要渠道: {channel_dist[0][0] if channel_dist else 'N/A'}"
            ]
        }
    finally:
        if own_conn:
            conn.close()


# ─────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────

def _parse_args():
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            return {}
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return {}
    return {}


if __name__ == "__main__":
    args = _parse_args()
    action = args.get("action", "summary")

    if action == "reconstruct":
        result = reconstruct_journey(
            patient_id=args.get("patient_id"),
            journey_id=args.get("journey_id"),
        )
    elif action == "list":
        result = list_journeys(
            patient_id=args.get("patient_id"),
            converted_only=args.get("converted_only", False),
            limit=args.get("limit", 50),
        )
    elif action == "compare":
        result = compare_journeys(journey_ids=args.get("journey_ids"))
    elif action == "summary":
        result = journey_summary()
    else:
        result = {"error": f"Unknown action: {action}"}

    print(json.dumps(result, ensure_ascii=False, indent=2))
