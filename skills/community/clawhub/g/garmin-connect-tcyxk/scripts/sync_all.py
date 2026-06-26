#!/usr/bin/env python3
# Author: SQ
"""
Garmin Connect 全量同步脚本 v2
把 garmin-sync.py 的数据写入 SQLite 数据库（今天 + 昨天）
支持历史补全：自动检测缺失天数，全部补齐

用法:
    python3 sync_all.py                    # 自动检测缺失天数
    python3 sync_all.py --days 7           # 指定最近7天
    python3 sync_all.py --days 7 --source manual    # 手动模式
"""
import json
import os
import sys
import sqlite3
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

DB_PATH = Path.home() / ".clawdbot" / "garmin" / "data.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


# ─────────────────────────────────────────────
# 数据库读写
# ─────────────────────────────────────────────

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库 + 迁移新字段"""
    # 调用独立 init_db.py 建完整 schema
    import subprocess as _sub
    r = _sub.run(
        ['/Users/sq/.venv/garmin/bin/python', str(Path(__file__).parent / 'init_db.py')],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        print(f"init_db: {r.stderr.strip()}")

    # 为已有表添加新列
    conn = get_connection()
    c = conn.cursor()

    new_daily = [
        'moderate_intensity_minutes INTEGER',
        'vigorous_intensity_minutes INTEGER',
        'stress_average INTEGER',
        'calories_active REAL',
        'calories_bmr REAL',
        'floors_descended REAL',
        'intensity_minutes INTEGER',
    ]
    for col_def in new_daily:
        col_name = col_def.split()[0]
        try:
            c.execute(f"ALTER TABLE daily_metrics ADD COLUMN {col_def}")
        except Exception:
            pass  # 字段已存在
    conn.close()


def write_daily_metrics(date: str, data: dict, sync_time: str):
    """写入每日健康指标"""
    conn = get_connection()
    c = conn.cursor()

    summary = data.get('summary', {})
    bb = data.get('body_battery', {})
    stress = data.get('stress', {})
    hrv = data.get('hrv', {})
    vo2 = data.get('vo2_max', {})
    fa = data.get('fitness_age', {})
    resp = data.get('respiration', {})

    c.execute("""
        INSERT OR REPLACE INTO daily_metrics (
            date, steps, distance_km, calories, active_seconds, floors,
            resting_heart_rate, min_heart_rate, max_heart_rate,
            body_battery_current, body_battery_highest, body_battery_lowest,
            body_battery_charged, body_battery_drained,
            avg_stress, max_stress, hrv_value, breathing_rate,
            vo2_max, fitness_age, last_sync_time,
            moderate_intensity_minutes, vigorous_intensity_minutes, stress_average,
            calories_active, calories_bmr, floors_descended, intensity_minutes
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        date,
        safe_int(summary.get('steps')),
        round(safe_float(summary.get('distance_km')), 2),
        safe_int(summary.get('calories')),
        safe_int(summary.get('active_minutes', 0) * 60 if summary.get('active_minutes') else None),
        safe_int(summary.get('floors_ascended')),
        safe_int(summary.get('heart_rate_resting')),
        safe_int(summary.get('heart_rate_min')),
        safe_int(summary.get('heart_rate_max')),
        safe_int(bb.get('most_recent') or bb.get('current')),
        safe_int(bb.get('highest')),
        safe_int(bb.get('lowest')),
        safe_int(bb.get('charged')),
        safe_int(bb.get('drained')),
        safe_int(stress.get('average')),
        safe_int(stress.get('max')),
        safe_int(hrv.get('hrv_last_night')),
        safe_float(resp.get('avg_respiration')),
        safe_float(vo2.get('vo2_max')),
        safe_int(fa.get('fitness_age')),
        sync_time,  # last_sync_time at position 21
        safe_int(summary.get('moderate_intensity_minutes')),
        safe_int(summary.get('vigorous_intensity_minutes')),
        safe_int(stress.get('average')),  # stress_average
        safe_float(summary.get('calories_active')),
        safe_float(summary.get('calories_bmr')),
        safe_float(summary.get('floors_descended')),
        safe_int(summary.get('intensity_minutes')),
    ))
    conn.commit()
    conn.close()


def write_sleep_data(date: str, data: dict, sync_time: str):
    """写入睡眠数据"""
    conn = get_connection()
    c = conn.cursor()

    sleep = data.get('sleep', {})
    naps = sleep.get('nap_details') or []

    c.execute("""
        INSERT OR REPLACE INTO sleep_data (
            date, total_sleep_hours, deep_sleep_hours, light_sleep_hours,
            rem_sleep_hours, awake_time_minutes, sleep_score, sleep_quality,
            avg_heart_rate, avg_spo2, last_sync_time,
            duration_minutes, nap_count, nap_total_minutes, nap_details, sleep_source
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        date,
        safe_float(sleep.get('duration_hours')),
        safe_float(sleep.get('deep_sleep_hours')),
        safe_float(sleep.get('light_sleep_hours')),
        safe_float(sleep.get('rem_sleep_hours')),
        safe_int(sleep.get('awake_minutes')),
        safe_int(sleep.get('quality_percent')),
        sleep.get('sleep_source', 'none'),
        None,  # avg_heart_rate
        None,  # avg_spo2
        sync_time,
        # 新增字段
        safe_int(sleep.get('duration_minutes')),
        len(naps) if isinstance(naps, list) else 0,
        sum(n.get('napTimeSec', 0) for n in naps) // 60 if isinstance(naps, list) else 0,
        json.dumps(naps) if isinstance(naps, list) else sleep.get('nap_details', ''),
        sleep.get('sleep_source', 'none'),
    ))
    conn.commit()
    conn.close()


def write_workouts(data: dict, sync_time: str) -> int:
    """写入运动记录"""
    conn = get_connection()
    c = conn.cursor()
    activities = data.get('workouts', []) or []
    count = 0

    for act in activities:
        act_date = act.get('date') or str(act.get('start_time', ''))[:10]
        if not act_date:
            continue

        distance = act.get('distance_km') or 0
        act_type = str(act.get('type', 'unknown'))
        duration = act.get('duration_minutes', 0)
        act_id = hash(f"{act_date}_{act_type}_{distance}_{duration}") % 10**10

        c.execute("""
            INSERT OR REPLACE INTO workouts VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (
            act_id,
            act.get('start_time') or act.get('timestamp', ''),
            act_type,
            act.get('name', ''),
            distance,
            int(safe_float(duration) * 60) if duration else None,
            act.get('calories'),
            act.get('heart_rate_avg'),
            act.get('heart_rate_max'),
            sync_time
        ))
        count += 1

    conn.commit()
    conn.close()
    return count


def log_sync(source: str, records: int, status: str, sync_time: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO sync_log (sync_time, source, records, status) VALUES (?,?,?,?)",
        (sync_time, source, records, status))
    conn.commit()
    conn.close()


def get_last_synced_date() -> Optional[str]:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT MAX(date) FROM daily_metrics")
    row = c.fetchone()
    conn.close()
    return row[0] if row and row[0] else None


# ─────────────────────────────────────────────
# Garmin API
# ─────────────────────────────────────────────

def safe_int(val, default=0):
    try:
        return int(val) if val is not None else default
    except (ValueError, TypeError):
        return default


def safe_float(val, default=0.0):
    try:
        return float(val) if val is not None else default
    except (ValueError, TypeError):
        return default


def get_garmin_client():
    from garminconnect import Garmin
    import base64

    session_file = Path.home() / ".garth" / "session.json"
    if not session_file.exists():
        print(f"❌ 未找到凭证: {session_file}")
        print("请运行: python3 garmin-auth.py <邮箱> <密码> [--cn]")
        return None

    with open(session_file, 'r') as f:
        creds = json.load(f)

    password = creds.get('password')
    if not password and creds.get('password_encrypted'):
        try:
            password = base64.b64decode(creds['password_encrypted']).decode()
        except Exception as e:
            print(f"❌ 密码解密失败: {e}")
            return None

    try:
        garmin = Garmin(
            creds.get('email', creds.get('username')),
            password,
            is_cn=creds.get('is_cn', False)
        )
        garmin.login()
        return garmin
    except Exception as e:
        print(f"❌ Garmin 登录失败: {e}")
        return None


def fetch_day_data(garmin_client, date_str: str) -> Optional[dict]:
    """获取单日完整数据"""
    print(f"  📅 获取 {date_str}...")

    summary = {}
    stats = {}
    sleep = {}
    bb = {}
    stress = {}
    hrv_data = {}
    vo2 = {}
    fa = {}
    resp = {}
    activities = []

    try:
        summary = garmin_client.get_user_summary(date_str) or {}
    except Exception as e:
        print(f"    ⚠️ get_user_summary: {e}")

    try:
        stats = garmin_client.get_stats(date_str) or {}
    except Exception as e:
        print(f"    ⚠️ get_stats: {e}")

    try:
        sleep_resp = garmin_client.get_sleep_data(date_str)
        if sleep_resp and 'dailySleepDTO' in sleep_resp:
            s = sleep_resp['dailySleepDTO']
            naps = sleep_resp.get('dailyNapDTOList') or []
            duration_sec = s.get('sleepTimeSeconds') or 0
            nap_details = []
            nap_total_min = 0
            for nap in naps:
                nap_sec = nap.get('napTimeSec', 0)
                nap_total_min += nap_sec // 60
                nap_details.append({
                    'start': nap.get('napStartTimestampGMT', ''),
                    'end': nap.get('napEndTimestampGMT', ''),
                    'napTimeSec': nap_sec,
                })
            sleep = {
                'duration_hours': round(duration_sec / 3600, 2),
                'deep_sleep_hours': safe_float(s.get('deepSleepSeconds', 0)) / 3600,
                'light_sleep_hours': safe_float(s.get('lightSleepSeconds', 0)) / 3600,
                'rem_sleep_hours': safe_float(s.get('remSleepSeconds', 0)) / 3600,
                'awake_minutes': safe_int(s.get('awakeTimeSeconds', 0)) // 60,
                'quality_percent': safe_int(s.get('sleepQualityPercentage')),
                'sleep_source': 'main',
                'nap_details': nap_details,
                'duration_minutes': duration_sec // 60,
                'nap_count': len(naps),
                'nap_total_minutes': nap_total_min,
            }
    except Exception as e:
        print(f"    ⚠️ get_sleep_data: {e}")

    try:
        bb_resp = garmin_client.get_body_battery(date_str) or {}
        if isinstance(bb_resp, dict):
            bb = {
                'most_recent': safe_int(bb_resp.get('bodyBatteryMostRecentValue')),
                'highest': safe_int(bb_resp.get('bodyBatteryHighestValue')),
                'lowest': safe_int(bb_resp.get('bodyBatteryLowestValue')),
                'charged': safe_int(bb_resp.get('bodyBatteryChargedValue')),
                'drained': safe_int(bb_resp.get('bodyBatteryDrainedValue')),
                'current': safe_int(bb_resp.get('bodyBatteryMostRecentValue')),
            }
        elif isinstance(bb_resp, list) and len(bb_resp) > 0:
            day_data = bb_resp[0]
            values_array = day_data.get('bodyBatteryValuesArray', [])
            # Filter None values and extract battery levels
            battery_values = [v[1] for v in values_array if isinstance(v, list) and len(v) >= 2 and v[1] is not None]
            bb = {
                'most_recent': battery_values[-1] if battery_values else safe_int(day_data.get('bodyBatteryMostRecentValue')),
                'highest': max(battery_values) if battery_values else safe_int(day_data.get('bodyBatteryHighestValue')),
                'lowest': min(battery_values) if battery_values else safe_int(day_data.get('bodyBatteryLowestValue')),
                'charged': safe_int(day_data.get('charged')),
                'drained': safe_int(day_data.get('drained')),
                'current': battery_values[-1] if battery_values else safe_int(day_data.get('bodyBatteryMostRecentValue')),
            }
        else:
            bb = {}
    except Exception as e:
        print(f"    ⚠️ get_body_battery: {e}")

    try:
        stress_resp = garmin_client.get_stress_data(date_str) or {}
        if isinstance(stress_resp, dict):
            stress = {
                'average': safe_int(stress_resp.get('avgStressLevel')),
                'max': safe_int(stress_resp.get('maxStressLevel')),
            }
    except Exception as e:
        print(f"    ⚠️ get_stress_data: {e}")

    try:
        hrv_resp = garmin_client.get_hrv_data(date_str) or {}
        if isinstance(hrv_resp, list) and len(hrv_resp) > 0:
            hrv_data = {'hrv_last_night': safe_int(hrv_resp[0].get('hrvValue'))}
        elif isinstance(hrv_resp, dict):
            hrv_data = {'hrv_last_night': safe_int(hrv_resp.get('hrvValue'))}
    except Exception as e:
        print(f"    ⚠️ get_hrv_data: {e}")

    try:
        vo2_resp = garmin_client.get_max_metrics(date_str) or {}
        if isinstance(vo2_resp, list) and len(vo2_resp) > 0:
            generic = vo2_resp[0].get('maxMetricGenericRatings', [{}])[0] or {}
            vo2 = {'vo2_max': safe_float(generic.get('vo2MaxValue'))}
            fa = {'fitness_age': safe_int(generic.get('fitnessAge'))}
    except Exception as e:
        print(f"    ⚠️ get_max_metrics: {e}")

    try:
        resp_resp = garmin_client.get_respiration_data(date_str) or {}
        if isinstance(resp_resp, dict):
            resp = {'avg_respiration': safe_float(resp_resp.get('averageRespirationValue'))}
    except Exception as e:
        print(f"    ⚠️ get_respiration_data: {e}")

    try:
        all_acts = garmin_client.get_activities(0, 30) or []
        activities = []
        for a in all_acts:
            act_date = (a.get('startTimeLocal', '') or a.get('startTimeGMT', ''))[:10]
            if act_date != date_str:
                continue
            atype = a.get('activityType')
            if isinstance(atype, dict):
                atype = atype.get('typeKey', 'unknown')
            activities.append({
                'date': act_date,
                'start_time': a.get('startTimeLocal', ''),
                'type': str(atype),
                'name': a.get('activityName', 'Unnamed'),
                'distance_km': round(safe_float(a.get('distanceInMeters') or a.get('distance', 0)) / 1000, 2),
                'duration_minutes': round(safe_float(a.get('durationInSeconds') or a.get('duration', 0)) / 60, 1),
                'calories': safe_int(a.get('totalCalories') or a.get('calories')),
                'heart_rate_avg': safe_int(a.get('averageHR') or a.get('averageHeartRate')),
                'heart_rate_max': safe_int(a.get('maxHR') or a.get('maxHeartRate')),
            })
    except Exception as e:
        print(f"    ⚠️ get_activities: {e}")

    return {
        'date': date_str,
        'summary': {
            'steps': safe_int(summary.get('totalSteps')),
            'distance_km': round(safe_float(summary.get('totalDistanceMeters') or summary.get('totalDistance', 0)) / 1000, 2),
            'calories': safe_int(summary.get('totalKilocalories') or summary.get('totalCalories')),
            'active_minutes': safe_int(summary.get('totalIntensityMinutes') or 0),
            'floors_ascended': safe_int(summary.get('floorsAscended') or summary.get('totalElevationGain')),
            'heart_rate_resting': safe_int(summary.get('restingHeartRate') or (isinstance(stats, dict) and stats.get('minHeartRate'))),
            'heart_rate_min': safe_int(isinstance(stats, dict) and stats.get('minHeartRate')),
            'heart_rate_max': safe_int(isinstance(stats, dict) and stats.get('maxHeartRate')),
            'moderate_intensity_minutes': safe_int(isinstance(stats, dict) and safe_int(stats.get('moderateIntensityMinutes'))),
            'vigorous_intensity_minutes': safe_int(isinstance(stats, dict) and safe_int(stats.get('vigorousIntensityMinutes'))),
            'calories_active': safe_float(isinstance(stats, dict) and safe_float(stats.get('activeKilocalories'))),
            'calories_bmr': safe_float(isinstance(stats, dict) and safe_float(stats.get('bmrKilocalories'))),
            'floors_descended': safe_float(isinstance(stats, dict) and safe_float(stats.get('floorsDescended'))),
            'intensity_minutes': safe_int(isinstance(stats, dict) and (safe_int(stats.get('moderateIntensityMinutes')) + safe_int(stats.get('vigorousIntensityMinutes')))),
        },
        'sleep': sleep,
        'workouts': activities,
        'body_battery': bb,
        'stress': stress,
        'hrv': hrv_data,
        'vo2_max': vo2,
        'fitness_age': fa,
        'respiration': resp,
    }


# ─────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────

def sync_days(days: int = 0, source: str = "manual"):
    """同步缺失的数据"""
    init_db()

    beijing_tz = timezone(timedelta(hours=8))
    now = datetime.now(beijing_tz)
    today = now - timedelta(days=1) if now.hour < 5 else now
    today_str = today.strftime("%Y-%m-%d")

    if days > 0:
        dates = []
        for i in range(days):
            d = now - timedelta(days=i)
            if d.hour < 5:
                d -= timedelta(days=1)
            dates.append(d.strftime("%Y-%m-%d"))
    else:
        last_synced = get_last_synced_date()
        if last_synced:
            last_dt = datetime.strptime(last_synced, "%Y-%m-%d")
            dates = [last_synced]
            d = last_dt + timedelta(days=1)
            while d.strftime("%Y-%m-%d") <= today_str:
                dates.append(d.strftime("%Y-%m-%d"))
                d += timedelta(days=1)
            if not dates:
                print("✅ 数据已是最新，无需同步")
                return True
            print(f"📋 待同步: {last_synced} → {today_str}，共 {len(dates)} 天")
        else:
            dates = []
            for i in range(1, 8):
                d = now - timedelta(days=i)
                if d.hour < 5:
                    d -= timedelta(days=1)
                dates.append(d.strftime("%Y-%m-%d"))
            print(f"📋 数据库为空，同步最近7天: {dates[0]} → {dates[-1]}")

    print(f"🔄 Garmin 全量同步开始（{len(dates)} 天）")

    garmin = get_garmin_client()
    if not garmin:
        return False

    sync_time = datetime.now().isoformat()
    total = 0

    for date_str in dates:
        try:
            data = fetch_day_data(garmin, date_str)
            if not data:
                continue
            write_daily_metrics(date_str, data, sync_time)
            print(f"    ✅ 每日指标: {date_str}")
            if data.get('sleep'):
                write_sleep_data(date_str, data, sync_time)
                print(f"    ✅ 睡眠数据: {date_str}")
            n = write_workouts(data, sync_time)
            if n > 0:
                print(f"    ✅ 运动记录 {n} 条: {date_str}")
            total += 1
        except Exception as e:
            print(f"    ❌ {date_str} 失败: {e}")
            continue

    log_sync(source, total, "success", sync_time)
    print(f"✅ 同步完成！{total} 天数据已写入数据库")
    return True


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Garmin Connect 全量同步")
    parser.add_argument("--days", type=int, default=0, help="同步最近N天（默认0=自动检测缺失）")
    parser.add_argument("--source", type=str, default="manual", help="来源标记")
    args = parser.parse_args()

    success = sync_days(days=args.days, source=args.source)
    sys.exit(0 if success else 1)
