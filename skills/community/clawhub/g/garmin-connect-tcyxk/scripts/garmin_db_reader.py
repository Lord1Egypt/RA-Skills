#!/usr/bin/env python3
# Author: SQ
"""
从SQLite数据库读取佳明健康数据
替代直接API调用，提供更快的响应和完整的历史数据
"""

import sys
import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, List


class GarminDataReader:
    """佳明数据库读取器"""

    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path.home() / '.clawdbot' / 'garmin' / 'data.db'

        self.db_path = Path(db_path)

        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found: {self.db_path}")

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_last_sync(self) -> Optional[datetime]:
        """获取最后同步时间"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT MAX(last_sync_time) as last_sync FROM daily_metrics
        """)
        result = cursor.fetchone()
        conn.close()

        if result and result['last_sync']:
            return datetime.fromisoformat(result['last_sync'])
        return None

    def get_today_metrics(self) -> Optional[Dict]:
        """获取今日健康数据"""
        conn = self.get_connection()
        cursor = conn.cursor()

        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("SELECT * FROM daily_metrics WHERE date = ?", (today,))
        row = cursor.fetchone()

        conn.close()

        if row:
            return dict(row)
        return None

    def get_metrics_by_date(self, date: str) -> Optional[Dict]:
        """获取指定日期的健康数据"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM daily_metrics WHERE date = ?", (date,))
        row = cursor.fetchone()

        conn.close()

        if row:
            return dict(row)
        return None

    def get_metrics_history(self, days: int = 30) -> List[Dict]:
        """获取历史健康数据"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT * FROM daily_metrics
            ORDER BY date DESC
            LIMIT {days}
        """)
        rows = cursor.fetchall()

        conn.close()

        return [dict(row) for row in rows]

    def get_latest_sleep(self) -> Optional[Dict]:
        """获取最新睡眠数据"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sleep_data ORDER BY date DESC LIMIT 1")
        row = cursor.fetchone()

        conn.close()

        if row:
            data = dict(row)
            if data.get('nap_details'):
                data['nap_details'] = json.loads(data['nap_details'])
            return data
        return None

    def get_sleep_by_date(self, date: str) -> Optional[Dict]:
        """获取指定日期的睡眠数据"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sleep_data WHERE date = ?", (date,))
        row = cursor.fetchone()

        conn.close()

        if row:
            data = dict(row)
            if data.get('nap_details'):
                data['nap_details'] = json.loads(data['nap_details'])
            return data
        return None

    def get_sleep_history(self, days: int = 7) -> List[Dict]:
        """获取睡眠历史数据"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT * FROM sleep_data
            ORDER BY date DESC
            LIMIT {days}
        """)
        rows = cursor.fetchall()

        conn.close()

        result = []
        for row in rows:
            data = dict(row)
            if data.get('nap_details'):
                data['nap_details'] = json.loads(data['nap_details'])
            result.append(data)

        return result

    def get_recent_workouts(self, limit: int = 10) -> List[Dict]:
        """获取最近运动记录"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM workouts ORDER BY timestamp DESC LIMIT {limit}")
        rows = cursor.fetchall()

        conn.close()

        return [dict(row) for row in rows]

    def get_workouts_by_type(self, workout_type: str, limit: int = 10) -> List[Dict]:
        """获取指定类型的运动记录"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM workouts
            WHERE type = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (workout_type, limit))
        rows = cursor.fetchall()

        conn.close()

        return [dict(row) for row in rows]

    def get_sync_status(self) -> Dict:
        """获取同步状态"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # 最后同步时间
        cursor.execute("SELECT MAX(sync_time) as last_sync FROM sync_log")
        last_sync_row = cursor.fetchone()
        last_sync = last_sync_row['last_sync'] if last_sync_row else None

        # 同步次数
        cursor.execute("SELECT COUNT(*) as count FROM sync_log WHERE sync_time >= datetime('now', '-1 hour')")
        recent_syncs = cursor.fetchone()['count']

        # 数据记录数
        cursor.execute("SELECT COUNT(*) as count FROM daily_metrics")
        daily_count = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM sleep_data")
        sleep_count = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM workouts")
        workout_count = cursor.fetchone()['count']

        conn.close()

        return {
            'last_sync': last_sync,
            'recent_syncs_last_hour': recent_syncs,
            'daily_metrics_count': daily_count,
            'sleep_data_count': sleep_count,
            'workouts_count': workout_count,
        }



def safe_int(v, default=None):
    try: return int(v) if v is not None else default
    except: return default

def safe_float(v, default=None):
    try: return float(v) if v is not None else default
    except: return default

def safe(v, default=None):
    return v if v is not None else default


def trigger_sync_if_needed(max_age_minutes: int = 5) -> bool:
    """如果数据太旧，触发同步

    Args:
        max_age_minutes: 数据最大允许年龄（分钟）

    Returns:
        是否触发了同步
    """
    reader = GarminDataReader()
    last_sync = reader.get_last_sync()

    if last_sync:
        age = datetime.now() - last_sync
        if age < timedelta(minutes=max_age_minutes):
            # 数据新鲜，不需要同步
            return False

    # 数据太旧或没有数据，触发同步
    import subprocess
    sync_script = Path.home() / '.clawdbot' / 'garmin' / 'sync_all.py'

    try:
        subprocess.run(
            ['/usr/bin/python3', str(sync_script), '--source', 'lobster'],
            capture_output=True,
            timeout=60,
        )
        return True
    except Exception as e:
        print(f"❌ Failed to trigger sync: {e}")
        return False


# 兼容性接口（与garmin-sync.py保持一致）

def get_daily_summary(garmin_client, date: str) -> Dict:
    """获取每日健康数据（从数据库）"""
    reader = GarminDataReader()
    data = reader.get_metrics_by_date(date)

    if data:
        return {
            'steps': data.get('steps', 0),
            'heart_rate_resting': data.get('heart_rate_resting', 0),
            'heart_rate_min': data.get('heart_rate_min', 0),
            'heart_rate_max': data.get('heart_rate_max', 0),
            'calories': data.get('calories', 0),
            'calories_active': data.get('calories_active', 0),
            'calories_bmr': data.get('calories_bmr', 0),
            'active_minutes': data.get('active_minutes', 0),
            'distance_km': data.get('distance_km', 0),
            'floors_ascended': data.get('floors_ascended', 0),
            'floors_descended': data.get('floors_descended', 0),
            'intensity_minutes': data.get('intensity_minutes', 0),
            'moderate_intensity_minutes': data.get('moderate_intensity_minutes', 0),
            'vigorous_intensity_minutes': data.get('vigorous_intensity_minutes', 0),
            # 扩展字段
            'body_battery_current': data.get('body_battery_current', 0),
            'body_battery_highest': data.get('body_battery_highest', 0),
            'body_battery_lowest': data.get('body_battery_lowest', 0),
            'stress_average': data.get('stress_average', 0),
            'hrv_last_night': data.get('hrv_last_night', 0),
            'vo2_max': data.get('vo2_max', 0),
            'fitness_age': data.get('fitness_age', 0),
        }
    else:
        # 数据库中没有，返回默认值
        return {
            'steps': 0,
            'heart_rate_resting': 0,
            'calories': 0,
            'active_minutes': 0,
            'distance_km': 0,
        }


def get_sleep_data(garmin_client, date: str) -> Dict:
    """获取睡眠数据（从数据库）"""
    reader = GarminDataReader()
    data = reader.get_sleep_by_date(date)

    if data:
        return {
            'duration_hours': data.get('duration_hours', 0),
            'duration_minutes': data.get('duration_minutes', 0),
            'sleep_score': data.get('sleep_score', 0),
            'quality_percent': data.get('quality_percent', 0),
            'deep_sleep_hours': data.get('deep_sleep_hours', 0),
            'rem_sleep_hours': data.get('rem_sleep_hours', 0),
            'light_sleep_hours': data.get('light_sleep_hours', 0),
            'awake_minutes': data.get('awake_minutes', 0),
            'nap_count': data.get('nap_count', 0),
            'nap_total_minutes': data.get('nap_total_minutes', 0),
            'nap_details': data.get('nap_details', []),
            'sleep_source': data.get('sleep_source', 'none'),
        }
    else:
        return {
            'duration_hours': 0,
            'sleep_score': 0,
            'nap_details': [],
        }


def get_workouts(garmin_client) -> List[Dict]:
    """获取运动记录（从数据库）"""
    reader = GarminDataReader()
    workouts = reader.get_recent_workouts(20)

    return [
        {
            'timestamp': w['timestamp'],
            'type': w['type'],
            'name': w['name'],
            'distance_km': w['distance_km'],
            'duration_minutes': w['duration_minutes'],
            'calories': w['calories'],
            'heart_rate_avg': w['heart_rate_avg'],
            'heart_rate_max': w['heart_rate_max'],
        }
        for w in workouts
    ]


if __name__ == '__main__':
    # 测试代码
    reader = GarminDataReader()

    print("最后同步时间:", reader.get_last_sync())
    print("\n今日数据:")
    today = reader.get_today_metrics()
    if today:
        print(f"  步数: {today['steps']}")
        print(f"  身体电量: {today['body_battery_current']}")
        print(f"  VO2 Max: {today['vo2_max']}")

    print("\n最近运动:")
    workouts = reader.get_recent_workouts(3)
    for w in workouts:
        print(f"  {w['name']}: {w['distance_km']}km")
