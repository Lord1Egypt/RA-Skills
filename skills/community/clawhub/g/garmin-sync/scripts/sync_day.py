#!/usr/bin/env python3
"""写入当天 Garmin 数据到本地和服务器 DB"""
import sqlite3, sys

DATE = sys.argv[1] if len(sys.argv) > 1 else None
if not DATE:
    from datetime import date
    DATE = date.today().strftime('%Y-%m-%d')

# 从 arguments 读取
data = {
    'date': DATE,
    'steps': int(sys.argv[2]) if len(sys.argv) > 2 else None,
    'distance_km': float(sys.argv[3]) if len(sys.argv) > 3 else None,
    'calories_kcal': float(sys.argv[4]) if len(sys.argv) > 4 else None,
    'active_minutes': int(sys.argv[5]) if len(sys.argv) > 5 else None,
    'resting_hr': int(sys.argv[6]) if len(sys.argv) > 6 else None,
    'floors': float(sys.argv[7]) if len(sys.argv) > 7 else None,
}

# 只更新非空值
dbs = [
    "/root/.openclaw/workspace/workplan-repo/projects/运动与健康/佳明数据/garmin.db",
    "/var/www/workplan-backend/projects/运动与健康/佳明数据/garmin.db",
]
for db in dbs:
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        set_parts = []
        vals = []
        for k, v in data.items():
            if v is not None:
                set_parts.append(f"{k}=?")
                vals.append(v)
        vals.append(data['date'])
        c.execute(f"UPDATE daily_summary SET {','.join(set_parts)} WHERE date=?", vals)
        conn.commit()
        c.execute(f"SELECT steps,distance_km,calories_kcal,active_minutes FROM daily_summary WHERE date=?", (data['date'],))
        print(f"✓ {db.split('/')[-1]}: {c.fetchone()}")
        conn.close()
    except Exception as e:
        print(f"✗ {db}: {e}")

print("Done")