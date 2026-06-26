#!/usr/bin/env python3
"""
Phase 1.1 - 患者旅程统一事件模型迁移

将旧的 patient_touchpoints + conversion_events 迁移到新的统一模型：
  patient_journey_events（新事件表）
  patient_journeys（旅程汇总表）

运行方式:
  python3 tools/migrate_journey_model.py        # 执行迁移
  python3 tools/migrate_journey_model.py --dry  # 预览（不写入）
"""
import sys
import uuid
import json
from pathlib import Path
from datetime import datetime
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent


def create_new_tables(conn):
    """创建新的统一事件表"""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS patient_journey_events (
            id              TEXT PRIMARY KEY,
            patient_id      TEXT NOT NULL,
            session_id      TEXT,
            journey_id      TEXT NOT NULL,
            event_type      TEXT NOT NULL,          -- 'touchpoint' | 'conversion'
            touchpoint_type TEXT,                    -- content_view / kol_recommendation 等（touchpoint时）
            channel         TEXT,
            platform        TEXT,
            content_id      TEXT,
            kol_id          TEXT,
            product_id      TEXT,
            attributed_channel TEXT,                -- conversion时填，归因渠道
            value           REAL DEFAULT 0,         -- 转化金额
            revenue         REAL DEFAULT 0,
            event_index     INTEGER,                -- 在旅程中的顺序
            timestamp       DATETIME DEFAULT CURRENT_TIMESTAMP,
            metadata        TEXT DEFAULT '{}',
            created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS patient_journeys (
            journey_id       TEXT PRIMARY KEY,
            patient_id       TEXT NOT NULL,
            first_event_at  DATETIME,
            last_event_at   DATETIME,
            conversion_flag INTEGER DEFAULT 0,
            conversion_value REAL DEFAULT 0,
            touchpoint_count INTEGER DEFAULT 0,
            channels_json    TEXT DEFAULT '[]',
            created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 索引
    conn.execute("CREATE INDEX IF NOT EXISTS idx_journey_patient ON patient_journey_events(patient_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_journey_journey ON patient_journey_events(journey_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_journey_type ON patient_journey_events(event_type)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_journey_ts ON patient_journey_events(timestamp)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_journeys_patient ON patient_journeys(patient_id)")


def migrate_from_old_tables(conn, dry_run=False):
    """从旧表迁移数据到新模型"""
    print("🔍 检查旧表数据...")

    # 检查旧数据
    tp_count = conn.execute("SELECT COUNT(*) FROM patient_touchpoints").fetchone()[0]
    conv_count = conn.execute("SELECT COUNT(*) FROM conversion_events").fetchone()[0]
    print(f"  patient_touchpoints: {tp_count} 条")
    print(f"  conversion_events: {conv_count} 条")

    if tp_count == 0 and conv_count == 0:
        print("  旧表无数据，跳过迁移")
        return 0

    migrated = 0

    # ── 迁移 patient_touchpoints → patient_journey_events (touchpoint) ──
    rows = conn.execute("""
        SELECT id, patient_id, content_id, kol_id, channel, platform,
               touchpoint_type, timestamp, session_id, metadata
        FROM patient_touchpoints
        ORDER BY patient_id, timestamp
    """).fetchall()

    journey_cache = {}  # patient_id → journey_id

    for r in rows:
        pid = r[1]
        ts = r[7]

        # 复用或新建 journey_id（同患者同日内归同一journey）
        cache_key = f"{pid}"
        if cache_key not in journey_cache:
            journey_id = f"JRN-{pid}-{ts[:10].replace('-','')}"
            journey_cache[cache_key] = journey_id
        else:
            journey_id = journey_cache[cache_key]

        event_id = f"EVT-TP-{r[0]}"
        metadata = r[9] if r[9] and r[9] != '{}' else '{}'

        event = (
            event_id, pid, r[8], journey_id, "touchpoint",
            r[6], r[4], r[5], r[2], r[3], None, None, None, None,
            0, ts, metadata, datetime.now().isoformat()
        )

        if not dry_run:
            conn.execute("""
                INSERT OR IGNORE INTO patient_journey_events
                (id, patient_id, session_id, journey_id, event_type, touchpoint_type,
                 channel, platform, content_id, kol_id, product_id, attributed_channel,
                 value, revenue, event_index, timestamp, metadata, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, event)
        migrated += 1

    print(f"  迁移 touchpoint 事件: {len(rows)} 条")

    # ── 迁移 conversion_events → patient_journey_events (conversion) ──
    rows = conn.execute("""
        SELECT id, patient_id, conversion_type, value, product_id, pharmacy_id,
               attributed_content_ids, attributed_channel, timestamp
        FROM conversion_events
        ORDER BY patient_id, timestamp
    """).fetchall()

    for r in rows:
        pid = r[1]
        ts = r[8]

        cache_key = f"{pid}"
        if cache_key not in journey_cache:
            journey_id = f"JRN-{pid}-{ts[:10].replace('-','')}"
            journey_cache[cache_key] = journey_id
        else:
            journey_id = journey_cache[cache_key]

        event_id = f"EVT-CV-{r[0]}"
        # 归因内容解析
        attributed_ids = r[6] if r[6] else '[]'
        try:
            ids_list = json.loads(attributed_ids)
            first_content = ids_list[0] if ids_list else None
        except Exception:
            first_content = None

        event = (
            event_id, pid, None, journey_id, "conversion",
            r[2], r[7], None, first_content, None, r[4],
            r[7], r[3], r[3], 1, ts, '{}', datetime.now().isoformat()
        )

        if not dry_run:
            conn.execute("""
                INSERT OR IGNORE INTO patient_journey_events
                (id, patient_id, session_id, journey_id, event_type, touchpoint_type,
                 channel, platform, content_id, kol_id, product_id, attributed_channel,
                 value, revenue, event_index, timestamp, metadata, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, event)
        migrated += 1

    print(f"  迁移 conversion 事件: {len(rows)} 条")

    # ── 构建 patient_journeys 汇总表 ──
    journey_rows = conn.execute("""
        SELECT journey_id, patient_id,
               MIN(timestamp) as first_event,
               MAX(timestamp) as last_event,
               SUM(CASE WHEN event_type = 'conversion' THEN 1 ELSE 0 END) as has_conv,
               SUM(CASE WHEN event_type = 'conversion' THEN value ELSE 0 END) as conv_value,
               SUM(CASE WHEN event_type = 'touchpoint' THEN 1 ELSE 0 END) as tp_count,
               COUNT(DISTINCT channel) as channel_count
        FROM patient_journey_events
        GROUP BY journey_id, patient_id
    """).fetchall()

    for r in journey_rows:
        if not dry_run:
            channels = conn.execute("""
                SELECT DISTINCT channel FROM patient_journey_events
                WHERE journey_id = ? AND channel IS NOT NULL
            """, (r[0],)).fetchall()
            channels_list = [c[0] for c in channels if c[0]]

            conn.execute("""
                INSERT OR REPLACE INTO patient_journeys
                (journey_id, patient_id, first_event_at, last_event_at,
                 conversion_flag, conversion_value, touchpoint_count, channels_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                r[0], r[1], r[2], r[3],
                1 if r[4] > 0 else 0,
                r[5] or 0,
                r[6] or 0,
                json.dumps(channels_list, ensure_ascii=False)
            ))
        migrated += 1

    print(f"  构建 journeys 汇总: {len(journey_rows)} 条")
    return migrated


def verify_migration(conn):
    """验证迁移结果"""
    print("\n📊 迁移验证:")

    evt_total = conn.execute("SELECT COUNT(*) FROM patient_journey_events").fetchone()[0]
    tp_count = conn.execute("SELECT COUNT(*) FROM patient_journey_events WHERE event_type='touchpoint'").fetchone()[0]
    cv_count = conn.execute("SELECT COUNT(*) FROM patient_journey_events WHERE event_type='conversion'").fetchone()[0]
    jrn_count = conn.execute("SELECT COUNT(*) FROM patient_journeys").fetchone()[0]
    conv_jrn = conn.execute("SELECT COUNT(*) FROM patient_journeys WHERE conversion_flag=1").fetchone()[0]

    print(f"  patient_journey_events: {evt_total} 条 (touchpoint={tp_count}, conversion={cv_count})")
    print(f"  patient_journeys: {jrn_count} 条 (有转化={conv_jrn})")

    # 样本
    print("\n  样本 journey_events:")
    rows = conn.execute("""
        SELECT id, patient_id, event_type, touchpoint_type, channel, value, journey_id
        FROM patient_journey_events LIMIT 5
    """).fetchall()
    for r in rows:
        print(f"    {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | ¥{r[5]} | {r[6]}")

    print("\n  样本 journeys:")
    rows = conn.execute("""
        SELECT journey_id, patient_id, conversion_flag, conversion_value, touchpoint_count
        FROM patient_journeys LIMIT 5
    """).fetchall()
    for r in rows:
        print(f"    {r[0]} | {r[1]} | conv={'是' if r[2] else '否'} | ¥{r[3]} | {r[4]}个触点")


def main():
    dry_run = "--dry" in sys.argv

    conn = get_conn()

    try:
        print(f"{'[DRY RUN] ' if dry_run else ''}Phase 1.1 - 患者旅程统一事件模型迁移")
        print(f"  目标: {DB_PATH}")

        if dry_run:
            print("  模式: 预览（不写入）\n")

        # 创建新表
        print("🔨 创建新表...")
        create_new_tables(conn)
        conn.commit()
        print("  ✅ patient_journey_events + patient_journeys 已创建")

        # 迁移数据
        print("\n📥 迁移数据...")
        migrated = migrate_from_old_tables(conn, dry_run=dry_run)
        if not dry_run:
            conn.commit()

        # 验证
        if not dry_run:
            verify_migration(conn)

        if dry_run:
            conn.rollback()
            print("\n⚠️  DRY RUN - 未写入任何数据")

        print(f"\n✅ 完成，迁移 {migrated} 条记录")

    finally:
        close_conn(conn)


if __name__ == "__main__":
    main()
