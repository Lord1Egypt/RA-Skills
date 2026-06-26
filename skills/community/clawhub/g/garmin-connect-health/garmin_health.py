#!/usr/bin/env python3
"""
Garmin Connect full health data fetcher.

Usage:
  python3 garmin_health.py                        # Fetch today's data
  python3 garmin_health.py --date 2026-03-16      # Fetch specific date
  python3 garmin_health.py --show                 # Show latest cached data
  python3 garmin_health.py --email you@example.com --password yourpass

Auth priority:
  1. --email / --password CLI args
  2. GARMIN_EMAIL / GARMIN_PASSWORD environment variables
  3. macOS Keychain: security find-generic-password -s 'garmin_connect'
  4. ~/.garmin_credentials (format: email=..., password=...)

Default data location:
  JSON:   ~/.garmin_health/YYYY-MM-DD.json
  SQLite: ~/.garmin_health/garmin.db
  Latest: ~/.garmin_health/latest.json

You can override paths with GARMIN_DATA_DIR and GARMIN_TOKENSTORE.
"""

import argparse
import json
import os
import sqlite3
import subprocess
import sys
from datetime import date, timedelta, datetime

try:
    from garminconnect import Garmin
except ImportError:
    print("请先安装: pip install garminconnect")
    sys.exit(1)

DATA_DIR = os.environ.get("GARMIN_DATA_DIR", os.path.expanduser("~/.garmin_health"))
TOKENSTORE = os.environ.get("GARMIN_TOKENSTORE", os.path.expanduser("~/.garminconnect"))
DB_PATH = os.path.join(DATA_DIR, "garmin.db")

# 需要拉取详情的运动类型
DETAIL_ACTIVITY_TYPES = {
    "strength_training",
    "running", "treadmill_running", "indoor_running",
    "cardio_training", "fitness_equipment",
    "badminton", "racquet_sports",
    "cycling", "indoor_cycling",
    "walking", "hiking",
}


# ── SQLite ─────────────────────────────────────────────────────────────────

def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS daily_summary (
        date TEXT PRIMARY KEY,
        fetched_at TEXT,
        steps INTEGER,
        calories REAL,
        active_calories REAL,
        bmr_calories REAL,
        distance_meters REAL,
        active_seconds INTEGER,
        sedentary_seconds INTEGER,
        resting_heart_rate INTEGER,
        avg_stress INTEGER,
        max_stress INTEGER,
        floors_climbed REAL,
        floors_descended REAL,
        moderate_intensity_minutes INTEGER,
        vigorous_intensity_minutes INTEGER,
        heart_rate_max INTEGER,
        heart_rate_min INTEGER,
        sleep_hours REAL,
        sleep_score INTEGER,
        sleep_deep_seconds INTEGER,
        sleep_light_seconds INTEGER,
        sleep_rem_seconds INTEGER,
        sleep_awake_seconds INTEGER,
        stress_avg INTEGER,
        stress_max INTEGER,
        body_battery_start INTEGER,
        body_battery_end INTEGER,
        body_battery_max INTEGER,
        body_battery_min INTEGER,
        respiration_avg_waking REAL,
        respiration_avg_sleep REAL,
        hrv_weekly_avg INTEGER,
        hrv_last_night_avg INTEGER,
        hrv_last_night_5min_high INTEGER,
        hrv_status TEXT,
        hrv_baseline_balanced_low INTEGER,
        hrv_baseline_balanced_high INTEGER,
        training_readiness_score INTEGER,
        training_status TEXT,
        training_load_acute REAL,
        training_load_chronic REAL,
        training_load_ratio REAL,
        training_load_ratio_status TEXT,
        training_load_balance_feedback TEXT,
        endurance_score INTEGER,
        weekly_steps_total INTEGER,
        weekly_steps_avg INTEGER
    );

    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY,
        date TEXT,
        name TEXT,
        type TEXT,
        start_time TEXT,
        duration_seconds REAL,
        distance_meters REAL,
        calories REAL,
        avg_hr REAL,
        max_hr REAL,
        avg_pace REAL,
        elevation_gain REAL,
        training_effect_aerobic REAL,
        training_effect_anaerobic REAL,
        total_reps INTEGER,
        active_sets INTEGER,
        training_load REAL,
        avg_cadence REAL,
        avg_power REAL,
        detail_json TEXT
    );

    CREATE TABLE IF NOT EXISTS activity_sets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity_id INTEGER,
        date TEXT,
        set_index INTEGER,
        set_type TEXT,
        start_time TEXT,
        duration_seconds REAL,
        rep_count INTEGER,
        weight_kg REAL,
        exercise_category TEXT,
        exercise_name TEXT,
        exercise_probability REAL,
        FOREIGN KEY (activity_id) REFERENCES activities(id)
    );

    CREATE INDEX IF NOT EXISTS idx_daily_date ON daily_summary(date);
    CREATE INDEX IF NOT EXISTS idx_activities_date ON activities(date);
    CREATE INDEX IF NOT EXISTS idx_activities_type ON activities(type);
    CREATE INDEX IF NOT EXISTS idx_sets_activity ON activity_sets(activity_id);
    """)
    conn.commit()
    return conn


def upsert_daily(conn, result):
    fields = [
        "date", "fetched_at", "steps", "calories", "active_calories", "bmr_calories",
        "distance_meters", "active_seconds", "sedentary_seconds", "resting_heart_rate",
        "avg_stress", "max_stress", "floors_climbed", "floors_descended",
        "moderate_intensity_minutes", "vigorous_intensity_minutes",
        "heart_rate_max", "heart_rate_min",
        "sleep_hours", "sleep_score", "sleep_deep_seconds", "sleep_light_seconds",
        "sleep_rem_seconds", "sleep_awake_seconds",
        "stress_avg", "stress_max",
        "body_battery_start", "body_battery_end", "body_battery_max", "body_battery_min",
        "respiration_avg_waking", "respiration_avg_sleep",
        "hrv_weekly_avg", "hrv_last_night_avg", "hrv_last_night_5min_high",
        "hrv_status", "hrv_baseline_balanced_low", "hrv_baseline_balanced_high",
        "training_readiness_score", "training_status",
        "training_load_acute", "training_load_chronic",
        "training_load_ratio", "training_load_ratio_status", "training_load_balance_feedback",
        "endurance_score", "weekly_steps_total", "weekly_steps_avg",
    ]
    vals = [result.get(f) for f in fields]
    placeholders = ", ".join(["?" ] * len(fields))
    cols = ", ".join(fields)
    updates = ", ".join([f"{f}=excluded.{f}" for f in fields if f != "date"])
    conn.execute(
        f"INSERT INTO daily_summary ({cols}) VALUES ({placeholders}) "
        f"ON CONFLICT(date) DO UPDATE SET {updates}",
        vals
    )
    conn.commit()


def upsert_activity(conn, act_dict, date_str):
    detail = act_dict.get("detail", {})
    conn.execute("""
        INSERT INTO activities (
            id, date, name, type, start_time, duration_seconds, distance_meters,
            calories, avg_hr, max_hr, avg_pace, elevation_gain,
            training_effect_aerobic, training_effect_anaerobic,
            total_reps, active_sets, training_load, avg_cadence, avg_power, detail_json
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(id) DO UPDATE SET
            detail_json=excluded.detail_json,
            total_reps=excluded.total_reps,
            active_sets=excluded.active_sets,
            training_load=excluded.training_load
    """, (
        act_dict["id"], date_str, act_dict.get("name"), act_dict.get("type"),
        act_dict.get("start_time"), act_dict.get("duration_seconds"),
        act_dict.get("distance_meters"), act_dict.get("calories"),
        act_dict.get("avg_hr"), act_dict.get("max_hr"), act_dict.get("avg_pace"),
        act_dict.get("elevation_gain"), act_dict.get("training_effect_aerobic"),
        act_dict.get("training_effect_anaerobic"),
        detail.get("total_reps"), detail.get("active_sets"), detail.get("training_load"),
        detail.get("avg_cadence"), detail.get("avg_power"),
        json.dumps(detail, ensure_ascii=False),
    ))
    conn.commit()


def upsert_sets(conn, activity_id, date_str, sets):
    # 先删旧的，再插入
    conn.execute("DELETE FROM activity_sets WHERE activity_id=?", (activity_id,))
    for i, s in enumerate(sets):
        if s.get("setType") != "ACTIVE":
            continue
        exes = s.get("exercises", [])
        top = exes[0] if exes else {}
        conn.execute("""
            INSERT INTO activity_sets (
                activity_id, date, set_index, set_type, start_time,
                duration_seconds, rep_count, weight_kg,
                exercise_category, exercise_name, exercise_probability
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (
            activity_id, date_str, i, s.get("setType"), s.get("startTime"),
            s.get("duration"), s.get("repetitionCount"),
            (s.get("weight") or 0) / 1000 if s.get("weight") else None,
            top.get("category"), top.get("name"), top.get("probability"),
        ))
    conn.commit()


# ── Garmin Client ──────────────────────────────────────────────────────────

def _load_credentials(email_arg=None, password_arg=None):
    """Load credentials from args -> env -> macOS keychain -> file."""
    email = email_arg or os.environ.get("GARMIN_EMAIL")
    password = password_arg or os.environ.get("GARMIN_PASSWORD")

    if not password:
        try:
            kc = subprocess.run(
                ["security", "find-generic-password", "-s", "garmin_connect", "-w"],
                capture_output=True,
                text=True,
            )
            if kc.returncode == 0:
                password = kc.stdout.strip()
        except FileNotFoundError:
            pass

    if not password:
        cred_file = os.path.expanduser("~/.garmin_credentials")
        if os.path.exists(cred_file):
            import stat

            mode = os.stat(cred_file).st_mode
            if mode & (stat.S_IRWXG | stat.S_IRWXO):
                print(f"⚠️ Warning: {cred_file} is readable by others. Run: chmod 600 {cred_file}")
            with open(cred_file, encoding="utf-8") as f:
                for line in f:
                    k, _, v = line.strip().partition("=")
                    if k == "email":
                        email = v
                    if k == "password":
                        password = v

    if not email or not password:
        print("❌ Credentials not found. Provide --email/--password, env vars,")
        print("   macOS Keychain, or ~/.garmin_credentials")
        sys.exit(1)

    return email, password


def get_client(email=None, password=None, is_cn=None):
    if is_cn is None:
        is_cn = os.environ.get("GARMIN_IS_CN", "").lower() in ("1", "true", "yes")

    client = Garmin(is_cn=is_cn)
    try:
        client.garth.load(TOKENSTORE)
        profile = client.garth.profile
        client.display_name = profile.get("displayName") if profile else None
        if client.display_name:
            return client
    except Exception:
        pass

    email, password = _load_credentials(email, password)
    client = Garmin(email, password, is_cn=is_cn)
    try:
        client.login(TOKENSTORE)
    except Exception:
        client.login()
        client.garth.dump(TOKENSTORE)
    return client


def safe_get(fn, label, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        print(f"  ⚠️ {label}: {e}")
        return None


# ── 活动详情拉取 ───────────────────────────────────────────────────────────

def fetch_activity_detail(client, act_id, act_type):
    """根据运动类型拉取对应详情，返回 detail dict"""
    detail = {}

    # 通用活动摘要。garminconnect has exposed this as either
    # get_activity() or get_activity_details() across releases.
    get_activity_summary = getattr(client, "get_activity", None) or getattr(client, "get_activity_details", None)
    summary = safe_get(get_activity_summary, f"活动摘要({act_id})", act_id) if get_activity_summary else None
    if summary:
        s = summary.get("summaryDTO") or summary.get("activitySummary") or summary.get("summary") or {}
        detail["total_reps"] = s.get("totalExerciseReps")
        detail["active_sets"] = s.get("activeSets")
        detail["training_load"] = s.get("activityTrainingLoad")
        detail["avg_cadence"] = s.get("averageRunningCadenceInStepsPerMinute") or s.get("averageBikingCadenceInRevPerMinute")
        detail["avg_power"] = s.get("avgPower")
        detail["moderate_intensity_minutes"] = s.get("moderateIntensityMinutes")
        detail["vigorous_intensity_minutes"] = s.get("vigorousIntensityMinutes")

    # 力量训练：拉每组动作明细
    if act_type in ("strength_training", "fitness_equipment"):
        sets = safe_get(client.get_activity_exercise_sets, f"动作组({act_id})", act_id)
        if sets and isinstance(sets, dict):
            raw_sets = sets.get("exerciseSets", [])
            active = [s for s in raw_sets if s.get("setType") == "ACTIVE"]
            detail["exercise_sets_raw"] = raw_sets
            detail["sets_summary"] = _summarize_strength_sets(active)
            detail["active_sets"] = detail.get("active_sets") or len(active)
            detail["total_reps"] = detail.get("total_reps") or sum(s.get("repetitionCount") or 0 for s in active)

    # 跑步/跑步机：拉分段数据
    elif act_type in ("running", "treadmill_running", "indoor_running"):
        splits = safe_get(client.get_activity_splits, f"分段({act_id})", act_id)
        if splits:
            detail["laps"] = _summarize_laps(splits.get("lapDTOs", []))

    # 有氧运动：拉 splits
    elif act_type in ("cardio_training",):
        splits = safe_get(client.get_activity_splits, f"分段({act_id})", act_id)
        if splits:
            detail["laps"] = _summarize_laps(splits.get("lapDTOs", []))

    # 羽毛球：拉 splits
    elif act_type in ("badminton", "racquet_sports"):
        splits = safe_get(client.get_activity_splits, f"分段({act_id})", act_id)
        if splits:
            detail["laps"] = _summarize_laps(splits.get("lapDTOs", []))

    return detail


def _summarize_strength_sets(active_sets):
    """汇总力量训练各动作的组数/次数"""
    from collections import defaultdict
    groups = defaultdict(list)
    for s in active_sets:
        exes = s.get("exercises", [])
        cat = exes[0].get("category", "UNKNOWN") if exes else "UNKNOWN"
        groups[cat].append({
            "reps": s.get("repetitionCount"),
            "weight_kg": (s.get("weight") or 0) / 1000 if s.get("weight") else None,
            "duration": s.get("duration"),
        })
    return {cat: {"sets": len(v), "total_reps": sum(x["reps"] or 0 for x in v),
                  "weight_kg": v[0]["weight_kg"]}
            for cat, v in groups.items()}


def _summarize_laps(laps):
    return [{
        "lap": i + 1,
        "duration_seconds": l.get("duration"),
        "distance_meters": l.get("distance"),
        "avg_hr": l.get("averageHR"),
        "max_hr": l.get("maxHR"),
        "avg_speed": l.get("averageSpeed"),
        "calories": l.get("calories"),
    } for i, l in enumerate(laps)]


# ── 主流程 ─────────────────────────────────────────────────────────────────

def fetch_all(target_date: str = None, email=None, password=None, is_cn=None, quiet: bool = False):
    def p(*args):
        if not quiet:
            print(*args)

    if not target_date:
        target_date = str(date.today())

    os.makedirs(DATA_DIR, exist_ok=True)
    cache_file = os.path.join(DATA_DIR, f"{target_date}.json")

    region = "CN" if (is_cn if is_cn is not None else os.environ.get("GARMIN_IS_CN", "").lower() in ("1", "true", "yes")) else "GLOBAL"
    p(f"🔐 Connecting to Garmin Connect [{region}]...")
    client = get_client(email=email, password=password, is_cn=is_cn)
    p(f"✅ Connected, fetching full data for {target_date}...\n")

    result = {"date": target_date, "fetched_at": datetime.now().isoformat()}

    # ── 每日摘要 ──────────────────────────────
    p("📊 每日摘要...")
    daily = safe_get(client.get_stats, "每日摘要", target_date)
    if daily:
        result["steps"] = daily.get("totalSteps")
        result["calories"] = daily.get("totalKilocalories")
        result["active_calories"] = daily.get("activeKilocalories")
        result["bmr_calories"] = daily.get("bmrKilocalories")
        result["distance_meters"] = daily.get("totalDistanceMeters")
        result["active_seconds"] = daily.get("highlyActiveSeconds", 0)
        result["sedentary_seconds"] = daily.get("sedentarySeconds")
        result["resting_heart_rate"] = daily.get("restingHeartRate")
        result["avg_stress"] = daily.get("averageStressLevel")
        result["max_stress"] = daily.get("maxStressLevel")
        result["floors_climbed"] = daily.get("floorsAscended")
        result["floors_descended"] = daily.get("floorsDescended")
        result["intensity_minutes_goal"] = daily.get("intensityMinutesGoal")
        result["moderate_intensity_minutes"] = daily.get("moderateIntensityMinutes")
        result["vigorous_intensity_minutes"] = daily.get("vigorousIntensityMinutes")
        p(f"  👟 步数: {result['steps']:,}" if result['steps'] else "  👟 步数: 无")
        p(f"  🔥 卡路里: {result['calories']} kcal (活动 {result['active_calories']}, 基础代谢 {result['bmr_calories']})")
        p(f"  📍 距离: {(result['distance_meters'] or 0)/1000:.2f} km")
        p(f"  🏢 楼层: +{result['floors_climbed']} / -{result['floors_descended']}")
        p(f"  ⏱️  中强度: {result['moderate_intensity_minutes']}min  高强度: {result['vigorous_intensity_minutes']}min")

    # ── 心率 ──────────────────────────────────
    p("❤️  心率...")
    hr = safe_get(client.get_heart_rates, "心率", target_date)
    if hr:
        result["heart_rate_max"] = hr.get("maxHeartRate")
        result["heart_rate_min"] = hr.get("minHeartRate")
        result["heart_rate_resting"] = hr.get("restingHeartRate")
        p(f"  范围: {result['heart_rate_min']}-{result['heart_rate_max']} bpm (静息 {result['heart_rate_resting']})")
        # 保存心率分时数据 [[timestamp_ms, hr_value], ...]
        raw_hr_vals = hr.get("heartRateValues", [])
        result["hr_timeline"] = [
            [v[0], v[1]] for v in raw_hr_vals if v and len(v) >= 2 and v[1] is not None
        ]
        p(f"  分时心率点: {len(result['hr_timeline'])} 个")

    # ── 睡眠 ──────────────────────────────────
    p("😴 睡眠...")
    sleep = safe_get(client.get_sleep_data, "睡眠", target_date)
    if sleep and "dailySleepDTO" in sleep:
        dto = sleep["dailySleepDTO"]
        sleep_seconds = dto.get("sleepTimeSeconds")
        result["sleep_seconds"] = sleep_seconds
        result["sleep_hours"] = round(sleep_seconds / 3600, 1) if sleep_seconds is not None else None
        result["sleep_score"] = dto.get("sleepScores", {}).get("overall", {}).get("value")
        result["sleep_deep_seconds"] = dto.get("deepSleepSeconds")
        result["sleep_light_seconds"] = dto.get("lightSleepSeconds")
        result["sleep_rem_seconds"] = dto.get("remSleepSeconds")
        result["sleep_awake_seconds"] = dto.get("awakeSleepSeconds")
        result["sleep_start"] = dto.get("sleepStartTimestampLocal")
        result["sleep_end"] = dto.get("sleepEndTimestampLocal")
        result["avg_sleep_stress"] = dto.get("avgSleepStress")
        result["sleep_need_minutes"] = dto.get("sleepNeed", {}).get("totalSleepSeconds", 0) // 60 if dto.get("sleepNeed") else None
        if result["sleep_hours"] is None:
            p("  时长: --  评分: 睡眠数据尚未同步完成")
        else:
            p(f"  时长: {result['sleep_hours']}h  评分: {result['sleep_score']}")
        p(f"  深睡: {(result['sleep_deep_seconds'] or 0)//60}min  浅睡: {(result['sleep_light_seconds'] or 0)//60}min  REM: {(result['sleep_rem_seconds'] or 0)//60}min  清醒: {(result['sleep_awake_seconds'] or 0)//60}min")

    # ── 压力 ──────────────────────────────────
    p("😰 压力...")
    stress = safe_get(client.get_stress_data, "压力", target_date)
    if stress:
        result["stress_avg"] = stress.get("avgStressLevel")
        result["stress_max"] = stress.get("maxStressLevel")
        result["rest_stress_duration"] = stress.get("restStressDuration")
        result["low_stress_duration"] = stress.get("lowStressDuration")
        result["medium_stress_duration"] = stress.get("mediumStressDuration")
        result["high_stress_duration"] = stress.get("highStressDuration")
        p(f"  平均: {result['stress_avg']}  最高: {result['stress_max']}")
        # 保存压力分时数据，-1 表示休息/无数据，保留为 null
        raw_stress = stress.get("stressValuesArray", [])
        result["stress_timeline"] = [
            [v[0], v[1] if v[1] != -1 else None] for v in raw_stress if v and len(v) >= 2
        ]
        p(f"  分时压力点: {len(result['stress_timeline'])} 个")
        # 从 stress 接口获取更密集的 BB 分时数据 [ts, status, bb_value, drain_rate]
        raw_bb_from_stress = stress.get("bodyBatteryValuesArray", [])
        if raw_bb_from_stress and len(raw_bb_from_stress) > 10:
            result["bb_timeline"] = [
                [v[0], v[2]] for v in raw_bb_from_stress
                if v and len(v) >= 3 and v[2] is not None
            ]
            p(f"  分时电量点(from stress): {len(result['bb_timeline'])} 个")

    # ── Body Battery ───────────────────────────
    p("🔋 Body Battery...")
    bb_list = safe_get(client.get_body_battery, "Body Battery", target_date, target_date)
    if bb_list and isinstance(bb_list, list) and len(bb_list) > 0:
        day_data = bb_list[0] if isinstance(bb_list[0], dict) and "bodyBatteryValuesArray" in bb_list[0] else None
        if day_data:
            vals = [v[1] for v in day_data.get("bodyBatteryValuesArray", []) if v[1] is not None]
            result["body_battery_start"] = vals[0] if vals else None
            result["body_battery_end"] = vals[-1] if vals else None
            result["body_battery_max"] = max(vals) if vals else None
            result["body_battery_min"] = min(vals) if vals else None
            p(f"  当前: {result['body_battery_end']}  今日范围: {result['body_battery_min']}-{result['body_battery_max']}")
            # 保存 body battery 分时数据（仅当 stress 接口未提供更密集数据时使用）
            if "bb_timeline" not in result or len(result.get("bb_timeline", [])) < 10:
                raw_bb = day_data.get("bodyBatteryValuesArray", [])
                result["bb_timeline"] = [
                    [v[0], v[1]] for v in raw_bb if v and len(v) >= 2 and v[1] is not None
                ]
                p(f"  分时电量点(fallback): {len(result['bb_timeline'])} 个")

    # ── 血氧 SpO2 ──────────────────────────────
    spo2 = safe_get(client.get_spo2_data, "血氧", target_date)
    if spo2:
        result["spo2_avg"] = spo2.get("averageSpO2")
        result["spo2_min"] = spo2.get("lowestSpO2")

    # ── 呼吸频率 ───────────────────────────────
    p("💨 呼吸频率...")
    resp = safe_get(client.get_respiration_data, "呼吸频率", target_date)
    if resp:
        result["respiration_avg_waking"] = resp.get("avgWakingRespirationValue")
        result["respiration_avg_sleep"] = resp.get("avgSleepRespirationValue")
        result["respiration_highest_waking"] = resp.get("highestRespirationValue")
        result["respiration_lowest_waking"] = resp.get("lowestRespirationValue")
        p(f"  清醒均值: {result['respiration_avg_waking']} 次/分  睡眠均值: {result['respiration_avg_sleep']} 次/分")

    # ── HRV ────────────────────────────────────
    p("📈 HRV...")
    hrv = safe_get(client.get_hrv_data, "HRV", target_date)
    if hrv and "hrvSummary" in hrv:
        s = hrv["hrvSummary"]
        result["hrv_weekly_avg"] = s.get("weeklyAvg")
        result["hrv_last_night_avg"] = s.get("lastNightAvg")
        result["hrv_last_night_5min_high"] = s.get("lastNight5MinHigh")
        result["hrv_status"] = s.get("status")
        result["hrv_feedback"] = s.get("feedbackPhrase")
        baseline = s.get("baseline", {})
        result["hrv_baseline_low"] = baseline.get("lowUpper")
        result["hrv_baseline_balanced_low"] = baseline.get("balancedLow")
        result["hrv_baseline_balanced_high"] = baseline.get("balancedUpper")
        p(f"  昨晚均值: {result['hrv_last_night_avg']} ms  5min峰值: {result['hrv_last_night_5min_high']} ms  周均: {result['hrv_weekly_avg']} ms")
        p(f"  状态: {result['hrv_status']}  基线范围: {result['hrv_baseline_balanced_low']}-{result['hrv_baseline_balanced_high']} ms")

    # ── 训练准备度 ─────────────────────────────
    p("🎯 训练准备度...")
    readiness = safe_get(client.get_training_readiness, "训练准备度", target_date)
    if readiness and isinstance(readiness, list) and len(readiness) > 0:
        r = readiness[0] if isinstance(readiness[0], dict) else {}
        result["training_readiness_score"] = r.get("score")
        level_info = r.get("levelInfo") or {}
        result["training_readiness_level"] = level_info.get("level") or r.get("level")
        result["training_readiness_feedback"] = (
            level_info.get("feedbackPhrase") or r.get("feedbackLong") or r.get("feedbackShort")
        )
        p(f"  评分: {result['training_readiness_score']}  级别: {result['training_readiness_level']}")
    elif isinstance(readiness, dict):
        result["training_readiness_score"] = readiness.get("score")
        p(f"  评分: {result['training_readiness_score']}")

    # ── 训练状态 ───────────────────────────────
    p("📊 训练状态...")
    tstatus = safe_get(client.get_training_status, "训练状态", target_date)
    if tstatus and isinstance(tstatus, dict):
        mrt = tstatus.get("mostRecentTrainingStatus") or {}
        latest = mrt.get("latestTrainingStatusData") or {}
        device_data = next(iter(latest.values()), {}) if isinstance(latest, dict) and latest else {}
        if device_data:
            ts_code = device_data.get("trainingStatus")
            ts_map = {1:"超负荷", 2:"高负荷", 3:"适当", 4:"维持", 5:"恢复中", 6:"减负中", 7:"无训练"}
            result["training_status"] = ts_map.get(ts_code, str(ts_code))
            result["training_status_feedback"] = device_data.get("trainingStatusFeedbackPhrase")
            acwr = device_data.get("acuteTrainingLoadDTO", {}) or {}
            result["training_load_acute"] = acwr.get("dailyTrainingLoadAcute")
            result["training_load_chronic"] = acwr.get("dailyTrainingLoadChronic")
            result["training_load_ratio"] = acwr.get("dailyAcuteChronicWorkloadRatio")
            result["training_load_ratio_status"] = acwr.get("acwrStatus")
            p(f"  状态: {result['training_status']} ({result['training_status_feedback']})")
            p(f"  急性负荷: {result['training_load_acute']}  慢性负荷: {result['training_load_chronic']}  比值: {result['training_load_ratio']} ({result['training_load_ratio_status']})")
        else:
            p("  今日暂未生成训练状态明细")

        mlb = tstatus.get("mostRecentTrainingLoadBalance") or {}
        balance_map = mlb.get("metricsTrainingLoadBalanceDTOMap") or {}
        balance_data = next(iter(balance_map.values()), {}) if isinstance(balance_map, dict) and balance_map else {}
        result["training_load_balance_feedback"] = balance_data.get("trainingBalanceFeedbackPhrase")
        result["training_load_aerobic_low"] = balance_data.get("monthlyLoadAerobicLow")
        result["training_load_aerobic_high"] = balance_data.get("monthlyLoadAerobicHigh")
        result["training_load_anaerobic"] = balance_data.get("monthlyLoadAnaerobic")
        if balance_data:
            p(f"  负荷均衡: {result['training_load_balance_feedback']}")

    # ── 体能指标 ───────────────────────────────
    p("🏆 体能指标...")
    max_metrics = safe_get(client.get_max_metrics, "体能指标", target_date)
    if max_metrics and isinstance(max_metrics, list) and len(max_metrics) > 0:
        m = max_metrics[0] if isinstance(max_metrics[0], dict) else {}
        generic = m.get("generic") or {}
        result["vo2max_running"] = generic.get("vo2MaxPreciseValue") or m.get("vo2MaxPreciseValue") or m.get("vo2MaxValue")
        result["fitness_age"] = generic.get("fitnessAge") or m.get("fitnessAge")
        p(f"  VO2 Max: {result.get('vo2max_running')}  体能年龄: {result.get('fitness_age')}")

    # ── 耐力评分 ───────────────────────────────
    p("💪 耐力评分...")
    endurance = safe_get(client.get_endurance_score, "耐力评分", target_date)
    if endurance:
        if isinstance(endurance, dict):
            result["endurance_score"] = endurance.get("overallScore")
        elif isinstance(endurance, (int, float)):
            result["endurance_score"] = endurance
        p(f"  评分: {result.get('endurance_score')}")

    # ── 爬坡能力 ───────────────────────────────
    hill = safe_get(client.get_hill_score, "爬坡能力", target_date)
    if hill:
        result["hill_score"] = hill.get("overallScore") if isinstance(hill, dict) else None

    # ── 比赛预测 ───────────────────────────────
    race_pred = safe_get(client.get_race_predictions, "比赛预测")
    if race_pred:
        if isinstance(race_pred, list):
            rp = race_pred[0] if race_pred and isinstance(race_pred[0], dict) else {}
        elif isinstance(race_pred, dict):
            rp = race_pred
        else:
            rp = {}
        result["race_prediction_5k_seconds"] = rp.get("time5K")
        result["race_prediction_10k_seconds"] = rp.get("time10K")
        result["race_prediction_half_seconds"] = rp.get("timeHalfMarathon")
        result["race_prediction_marathon_seconds"] = rp.get("timeMarathon")

    # ── 个人记录 ───────────────────────────────
    pr = safe_get(client.get_personal_record, "个人记录")
    if pr and isinstance(pr, list):
        result["personal_records"] = [
            {"type": r.get("typeId"), "value": r.get("value"), "activity_id": r.get("activityId")}
            for r in pr[:10]
        ]
        p(f"🏅 个人记录: 共 {len(pr)} 条")

    # ── 体重 ───────────────────────────────────
    weight = safe_get(client.get_weigh_ins, "体重", target_date, target_date)
    if weight:
        daily_w = weight.get("dailyWeightSummaries", [])
        if daily_w:
            latest_w = daily_w[-1].get("allWeightMetrics", {})
            result["weight_kg"] = (latest_w.get("weight") or 0) / 1000 if latest_w.get("weight") else None

    # ── 体成分 ─────────────────────────────────
    body_comp = safe_get(client.get_body_composition, "体成分", target_date, target_date)
    if body_comp and isinstance(body_comp, dict):
        entries = body_comp.get("totalAverage", {})
        result["body_fat_percent"] = entries.get("fatPercent")
        result["muscle_mass_grams"] = entries.get("muscleMass")
        result["bone_mass_grams"] = entries.get("boneMass")
        result["bmi"] = entries.get("bmi")

    # ── 饮水 ───────────────────────────────────
    hydration = safe_get(client.get_hydration_data, "饮水", target_date)
    if hydration:
        result["hydration_ml"] = hydration.get("valueInML")
        result["hydration_goal_ml"] = hydration.get("dailyIntakeGoalInML")

    # ── 今日活动（含详情） ──────────────────────
    p("🏃 活动记录...")
    activities = safe_get(client.get_activities_by_date, "活动", target_date, target_date)
    result["activities"] = []
    if activities:
        conn = init_db()
        for act in activities:
            act_type = act.get("activityType", {}).get("typeKey", "")
            a = {
                "id": act.get("activityId"),
                "name": act.get("activityName"),
                "type": act_type,
                "start_time": act.get("startTimeLocal"),
                "duration_seconds": act.get("duration"),
                "distance_meters": act.get("distance"),
                "calories": act.get("calories"),
                "avg_hr": act.get("averageHR"),
                "max_hr": act.get("maxHR"),
                "avg_pace": act.get("averageSpeed"),
                "elevation_gain": act.get("elevationGain"),
                "training_effect_aerobic": act.get("aerobicTrainingEffect"),
                "training_effect_anaerobic": act.get("anaerobicTrainingEffect"),
            }

            # 拉详情
            if act_type in DETAIL_ACTIVITY_TYPES and a["id"]:
                p(f"  📋 拉取详情: {a['name']} ({act_type})...")
                detail = fetch_activity_detail(client, a["id"], act_type)
                a["detail"] = detail

                # 力量训练：额外存 activity_sets 表
                if act_type in ("strength_training", "fitness_equipment"):
                    sets_raw = detail.get("exercise_sets_raw", [])
                    if sets_raw:
                        upsert_sets(conn, a["id"], target_date, sets_raw)
                        p(f"    💪 存入 {len([s for s in sets_raw if s.get('setType')=='ACTIVE'])} 组动作数据")
            else:
                a["detail"] = {}

            result["activities"].append(a)

            dur_min = int((a['duration_seconds'] or 0) / 60)
            p(f"  ✅ {a['name']} ({act_type}) {dur_min}min  HR: {a['avg_hr']}-{a['max_hr']} bpm  消耗: {a['calories']} kcal")

            # 写入 activities 表
            upsert_activity(conn, a, target_date)

        conn.close()

    # ── 周汇总 ─────────────────────────────────
    p("📅 周汇总...")
    today = date.fromisoformat(target_date)
    week_start = str(today - timedelta(days=today.weekday()))
    try:
        week_steps = client.get_daily_steps(week_start, target_date)
        if week_steps and isinstance(week_steps, list):
            result["weekly_steps_total"] = sum(w.get("totalSteps", 0) for w in week_steps)
            result["weekly_steps_avg"] = result["weekly_steps_total"] // max(len(week_steps), 1)
            p(f"  本周总步数: {result['weekly_steps_total']:,}  日均: {result['weekly_steps_avg']:,}")
    except Exception as e:
        p(f"  ⚠️ 周步数: {e}")

    intensity = safe_get(client.get_intensity_minutes_data, "强度分钟", target_date)
    if intensity and isinstance(intensity, dict):
        result["weekly_moderate_minutes"] = intensity.get("weeklyModerateIntensityMinutes")
        result["weekly_vigorous_minutes"] = intensity.get("weeklyVigorousIntensityMinutes")
        result["weekly_intensity_goal"] = intensity.get("weeklyIntensityMinutesGoal")
        p(f"  本周运动: 中强度 {result.get('weekly_moderate_minutes')}min  高强度 {result.get('weekly_vigorous_minutes')}min / 目标 {result.get('weekly_intensity_goal')}min")

    # ── 保存 JSON ──────────────────────────────
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    if target_date == str(date.today()):
        latest_file = os.path.join(DATA_DIR, "latest.json")
        with open(latest_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    # ── 写入 SQLite daily_summary ──────────────
    conn = init_db()
    upsert_daily(conn, result)
    conn.close()

    p(f"\n✅ 全量数据已保存: {cache_file}")
    p(f"✅ 已同步到 SQLite: {DB_PATH}")

    return result


def show_latest():
    latest_file = os.path.join(DATA_DIR, "latest.json")
    if not os.path.exists(latest_file):
        print("❌ 暂无缓存，请先运行拉取")
        return
    with open(latest_file) as f:
        data = json.load(f)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch full Garmin Connect health data")
    parser.add_argument("--date", help="Date YYYY-MM-DD (default: today)")
    parser.add_argument("--email", help="Garmin account email")
    parser.add_argument("--password", help="Garmin account password (prefer GARMIN_PASSWORD env var to avoid shell history exposure)")
    parser.add_argument("--show", action="store_true", help="Show latest cached data")
    parser.add_argument("--cn", action="store_true", help="Use Garmin Connect CN (or set GARMIN_IS_CN=true)")
    parser.add_argument("--quiet", action="store_true", help="Quiet mode for batch usage")
    args = parser.parse_args()

    if args.password:
        print("⚠️ Note: passing --password via CLI may expose it in shell history.")
        print("   Prefer GARMIN_PASSWORD or macOS Keychain.\n")

    if args.show:
        show_latest()
    else:
        fetch_all(args.date, args.email, args.password, is_cn=args.cn or None, quiet=args.quiet)
