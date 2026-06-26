#!/usr/bin/env python3
"""Garmin Connect CN (佳明中国) CLI wrapper.

Connects to connect.garmin.cn (China region).

Examples:
  garmin_cli.py login user@example.com mypassword
  garmin_cli.py summary
  garmin_cli.py activities --start 2026-01-01 --end 2026-01-31 --type running
  garmin_cli.py health --days 7 --metrics hrv,rhr
  garmin_cli.py export 12345678 --format gpx
"""

import argparse
import json
import os
import shutil
import sys
import zipfile
from datetime import datetime, timedelta

try:
    from garminconnect import Garmin
except ImportError:
    Garmin = None

CONFIG_DIR = os.path.expanduser("~/.config/garmin-cn")
CREDENTIALS_FILE = os.path.join(CONFIG_DIR, "credentials.json")


# ── Helpers ───────────────────────────────────────────────────────────


def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_credentials(email, password):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
        json.dump({"email": email, "password": password}, f)
    os.chmod(CREDENTIALS_FILE, 0o600)


def clear_garth_cache():
    """清除 garth 库的 SSO 缓存，避免过期 token 导致 401。"""
    garth_dir = os.path.expanduser("~/.garth")
    if os.path.isdir(garth_dir):
        shutil.rmtree(garth_dir, ignore_errors=True)


def get_client(retries=1):
    creds = load_credentials()
    if not creds:
        return None, f"未登录。请先运行: garmin_cli.py login <email> <password> (凭据存储于 {CREDENTIALS_FILE})"

    client = Garmin(creds["email"], creds["password"], is_cn=True)
    try:
        client.login()
        return client, None
    except Exception as exc:
        if retries > 0:
            clear_garth_cache()
            return get_client(retries=retries - 1)
        return None, f"登录失败: {exc}"


def validate_date(date_str):
    """校验日期格式 YYYY-MM-DD，返回 datetime 或抛出 ValueError。"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"日期格式错误: '{date_str}'，应为 YYYY-MM-DD")


def resolve_date_range(args):
    """从 --start/--end/--days 参数解析出 (start_str, end_str) 日期字符串对。"""
    today = datetime.now()

    if args.start:
        start_dt = validate_date(args.start)
    elif args.days:
        start_dt = today - timedelta(days=args.days - 1)
    else:
        start_dt = today - timedelta(days=6)

    if args.end:
        end_dt = validate_date(args.end)
    else:
        end_dt = today

    if start_dt > end_dt:
        raise ValueError(f"起始日期 ({start_dt:%Y-%m-%d}) 不能晚于结束日期 ({end_dt:%Y-%m-%d})")

    return start_dt.strftime("%Y-%m-%d"), end_dt.strftime("%Y-%m-%d"), start_dt, end_dt


def date_range_iter(start_dt, end_dt):
    """生成从 start_dt 到 end_dt 的每一天（含两端）。"""
    current = start_dt
    while current <= end_dt:
        yield current.strftime("%Y-%m-%d")
        current += timedelta(days=1)


def safe_round(value, ndigits=1):
    if value is None:
        return None
    try:
        return round(float(value), ndigits)
    except (TypeError, ValueError):
        return None


def format_duration(seconds):
    if seconds is None:
        return "N/A"
    seconds = float(seconds)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    return f"{minutes}m {secs}s"


def format_pace(seconds_per_km):
    if seconds_per_km is None or seconds_per_km <= 0:
        return "N/A"
    minutes = int(seconds_per_km // 60)
    secs = int(seconds_per_km % 60)
    return f"{minutes}:{secs:02d}"


def output_json(result):
    print(json.dumps(result, ensure_ascii=False, default=str))


# ── Data Parsers ──────────────────────────────────────────────────────


def parse_sleep_data(sleep_data):
    if not isinstance(sleep_data, dict):
        return None

    daily = sleep_data.get("dailySleepDTO") or {}
    total_sec = daily.get("sleepTimeSeconds")
    if total_sec is None or total_sec == 0:
        deep = daily.get("deepSleepSeconds")
        light = daily.get("lightSleepSeconds")
        rem = daily.get("remSleepSeconds")
        if any(v is not None and v > 0 for v in [deep, light, rem]):
            total_sec = sum(v or 0 for v in [deep, light, rem])

    return {
        "total_seconds": total_sec or 0,
        "total_formatted": format_duration(total_sec),
        "deep_seconds": daily.get("deepSleepSeconds", 0),
        "light_seconds": daily.get("lightSleepSeconds", 0),
        "rem_seconds": daily.get("remSleepSeconds", 0),
        "awake_seconds": daily.get("awakeSleepSeconds", 0),
        "resting_heart_rate": sleep_data.get("restingHeartRate"),
        "avg_overnight_hrv": sleep_data.get("avgOvernightHrv"),
        "hrv_status": sleep_data.get("hrvStatus"),
        "sleep_score": (daily.get("sleepScores") or {}).get("overall", {}).get("value"),
    }


def _simplify_phrase(phrase):
    if not phrase:
        return None
    base = phrase.split("_")[0]
    return base.replace("-", "_").replace(" ", "_").title().replace("_", " ")


def parse_training_status(training_status):
    if not isinstance(training_status, dict):
        return {"training_status": None, "training_load": None}

    status_block = (training_status.get("mostRecentTrainingStatus") or {}).get("latestTrainingStatusData") or {}
    device_payload = next(iter(status_block.values()), None)

    training_status_out = None
    training_load_out = None

    if isinstance(device_payload, dict):
        phrase = device_payload.get("trainingStatusFeedbackPhrase")
        training_status_out = {
            "phrase": phrase,
            "label": _simplify_phrase(phrase),
            "since_date": device_payload.get("sinceDate"),
            "sport": device_payload.get("sport"),
        }

        acute = device_payload.get("acuteTrainingLoadDTO") or {}
        if isinstance(acute, dict) and acute:
            training_load_out = {
                "acute_load": acute.get("dailyTrainingLoadAcute"),
                "chronic_load": acute.get("dailyTrainingLoadChronic"),
                "target_min": acute.get("minTrainingLoadChronic"),
                "target_max": acute.get("maxTrainingLoadChronic"),
                "ratio": acute.get("dailyAcuteChronicWorkloadRatio"),
                "acwr_percent": acute.get("acwrPercent"),
                "acwr_status": acute.get("acwrStatus"),
            }

    return {"training_status": training_status_out, "training_load": training_load_out}


def parse_training_readiness(training_readiness):
    if isinstance(training_readiness, list) and training_readiness:
        item = training_readiness[0]
    elif isinstance(training_readiness, dict):
        item = training_readiness
    else:
        return None

    if not isinstance(item, dict):
        return None

    return {
        "score": item.get("score"),
        "level": item.get("level"),
        "timestamp_local": item.get("timestampLocal"),
        "sleep_score": item.get("sleepScore"),
        "recovery_time_min": item.get("recoveryTime"),
        "acute_load": item.get("acuteLoad"),
        "feedback_short": item.get("feedbackShort"),
    }


# ── Commands ──────────────────────────────────────────────────────────


def cmd_login(args):
    clear_garth_cache()
    client = Garmin(args.email, args.password, is_cn=True)
    try:
        client.login()
        save_credentials(args.email, args.password)
        return {"status": "success", "message": f"已登录: {args.email} (Garmin Connect CN)"}
    except Exception as exc:
        return {"status": "error", "command": "login", "message": f"登录失败: {exc}"}


def cmd_status(args):
    client, err = get_client()
    if err:
        return {"status": "error", "command": "status", "message": err}
    return {"status": "success", "logged_in": True, "region": "CN"}


def cmd_summary(args):
    client, err = get_client()
    if err:
        return {"status": "error", "command": "summary", "message": err}

    date = args.date or datetime.now().strftime("%Y-%m-%d")
    try:
        validate_date(date)
    except ValueError as exc:
        return {"status": "error", "command": "summary", "message": str(exc)}

    try:
        user_summary = client.get_user_summary(date)
        if not user_summary:
            return {"status": "success", "command": "summary", "data": None, "message": f"{date} 无数据"}

        sleep_data = None
        training_status_raw = None
        training_readiness_raw = None
        weekly_intensity_raw = None
        warnings = []

        try:
            sleep_data = client.get_sleep_data(date)
        except Exception as exc:
            warnings.append(f"睡眠数据获取失败: {exc}")

        try:
            training_status_raw = client.get_training_status(date)
        except Exception as exc:
            warnings.append(f"训练状态获取失败: {exc}")

        try:
            training_readiness_raw = client.get_training_readiness(date)
        except Exception as exc:
            warnings.append(f"训练准备度获取失败: {exc}")

        week_start = week_end = None
        try:
            dt = datetime.strptime(date, "%Y-%m-%d")
            week_start_dt = dt - timedelta(days=dt.weekday())
            week_start = week_start_dt.strftime("%Y-%m-%d")
            week_end = dt.strftime("%Y-%m-%d")
            weekly_intensity_raw = client.get_weekly_intensity_minutes(week_start, week_end)
        except Exception as exc:
            warnings.append(f"强度分钟获取失败: {exc}")

        ts_parsed = parse_training_status(training_status_raw)

        intensity_minutes = None
        if weekly_intensity_raw and isinstance(weekly_intensity_raw, list) and weekly_intensity_raw:
            item = weekly_intensity_raw[-1]
            if isinstance(item, dict):
                moderate = item.get("moderateValue")
                vigorous = item.get("vigorousValue")
                total = None
                if moderate is not None and vigorous is not None:
                    total = int(moderate) + int(vigorous) * 2
                intensity_minutes = {
                    "week_start": item.get("calendarDate") or week_start,
                    "week_end": week_end,
                    "goal": item.get("weeklyGoal"),
                    "moderate": moderate,
                    "vigorous": vigorous,
                    "total": total,
                }

        result = {
            "date": date,
            "steps": user_summary.get("totalSteps") or 0,
            "distance_km": safe_round((user_summary.get("totalDistanceMeters") or 0) / 1000),
            "calories": user_summary.get("totalKilocalories") or 0,
            "heart_rate": {
                "resting": user_summary.get("restingHeartRate", 0),
                "max": user_summary.get("maxHeartRate", 0),
            },
            "body_battery": {
                "highest": user_summary.get("bodyBatteryHighestValue", 0),
                "lowest": user_summary.get("bodyBatteryLowestValue", 0),
                "most_recent": user_summary.get("bodyBatteryMostRecentValue"),
            },
            "stress": {
                "average": user_summary.get("averageStressLevel"),
                "qualifier": user_summary.get("stressQualifier"),
            },
            "sleep": parse_sleep_data(sleep_data) if sleep_data else None,
            "vo2_max": (
                (training_status_raw or {}).get("mostRecentVO2Max", {}).get("generic", {}).get("vo2MaxValue")
                if training_status_raw
                else None
            ),
            "training_status": ts_parsed.get("training_status"),
            "training_load": ts_parsed.get("training_load"),
            "training_readiness": parse_training_readiness(training_readiness_raw),
            "intensity_minutes": intensity_minutes,
            "last_sync": user_summary.get("lastSyncTimestampGMT"),
        }

        resp = {"status": "success", "command": "summary", "data": result}
        if warnings:
            resp["warnings"] = warnings
        return resp
    except Exception as exc:
        return {"status": "error", "command": "summary", "message": str(exc)}


def cmd_activities(args):
    client, err = get_client()
    if err:
        return {"status": "error", "command": "activities", "message": err}

    try:
        start_str, end_str, _, _ = resolve_date_range(args)
    except ValueError as exc:
        return {"status": "error", "command": "activities", "message": str(exc)}

    try:
        activity_type = getattr(args, "type", None)
        raw_activities = client.get_activities_by_date(start_str, end_str, activity_type)

        if not raw_activities:
            return {
                "status": "success",
                "command": "activities",
                "data": [],
                "message": f"{start_str} ~ {end_str} 范围内无活动" + (f" (类型: {activity_type})" if activity_type else ""),
            }

        activities = []
        for act in raw_activities:
            dist = act.get("distance") or 0
            dur = act.get("duration") or 0
            pace = (dur / dist * 1000) if dist > 0 else None
            activities.append({
                "activity_id": act.get("activityId"),
                "name": act.get("activityName"),
                "type": (act.get("activityType") or {}).get("typeKey"),
                "date": (act.get("startTimeLocal") or "")[:10],
                "start_time": act.get("startTimeLocal"),
                "distance_km": safe_round(dist / 1000, 2),
                "duration_sec": safe_round(dur, 0),
                "duration_formatted": format_duration(dur),
                "pace_formatted": format_pace(pace) if pace else None,
                "avg_hr": act.get("averageHR"),
                "max_hr": act.get("maxHR"),
                "calories": act.get("calories"),
                "avg_speed_kmh": safe_round((act.get("averageSpeed") or 0) * 3.6, 1) if act.get("averageSpeed") else None,
                "elevation_gain": act.get("elevationGain"),
                "aerobic_te": safe_round(act.get("aerobicTrainingEffect")),
                "anaerobic_te": safe_round(act.get("anaerobicTrainingEffect")),
            })

        return {
            "status": "success",
            "command": "activities",
            "count": len(activities),
            "date_range": f"{start_str} ~ {end_str}",
            "data": activities,
        }
    except Exception as exc:
        return {"status": "error", "command": "activities", "message": str(exc)}


def cmd_detail(args):
    client, err = get_client()
    if err:
        return {"status": "error", "command": "detail", "message": err}

    activity_id = args.activity_id
    try:
        activity = client.get_activity(activity_id)
        if not activity:
            return {"status": "error", "command": "detail", "message": f"未找到活动 {activity_id}"}

        details = None
        hr_zones = None
        weather = None
        gear = None
        splits = None
        warnings = []

        try:
            details = client.get_activity_details(activity_id)
        except Exception as exc:
            warnings.append(f"详情获取失败: {exc}")

        try:
            hr_zones = client.get_activity_hr_in_timezones(activity_id)
        except Exception as exc:
            warnings.append(f"心率分区获取失败: {exc}")

        try:
            weather = client.get_activity_weather(activity_id)
        except Exception as exc:
            warnings.append(f"天气获取失败: {exc}")

        try:
            gear = client.get_activity_gear(activity_id)
        except Exception as exc:
            warnings.append(f"装备获取失败: {exc}")

        try:
            splits = client.get_activity_splits(activity_id)
        except Exception as exc:
            warnings.append(f"分段获取失败: {exc}")

        # Parse basic info from activity summary
        summary = activity.get("summaryDTO") or activity
        dist = summary.get("distance") or 0
        dur = summary.get("duration") or summary.get("elapsedDuration") or 0
        pace = (dur / dist * 1000) if dist > 0 else None

        result = {
            "activity_id": activity_id,
            "name": activity.get("activityName"),
            "type": (activity.get("activityTypeDTO") or {}).get("typeKey"),
            "date": activity.get("summaryDTO", {}).get("startTimeLocal") or activity.get("startTimeLocal"),
            "distance_km": safe_round(dist / 1000, 2),
            "duration_sec": safe_round(dur, 0),
            "duration_formatted": format_duration(dur),
            "pace_formatted": format_pace(pace) if pace else None,
            "avg_hr": summary.get("averageHR") or summary.get("averageHeartRate"),
            "max_hr": summary.get("maxHR") or summary.get("maxHeartRate"),
            "calories": summary.get("calories"),
            "avg_power": summary.get("averagePower"),
            "max_power": summary.get("maxPower"),
            "avg_cadence": safe_round(summary.get("averageRunCadence") or summary.get("averageBikeCadence")),
            "elevation_gain": summary.get("elevationGain"),
            "elevation_loss": summary.get("elevationLoss"),
            "avg_speed_kmh": safe_round((summary.get("averageSpeed") or 0) * 3.6, 1) if summary.get("averageSpeed") else None,
            "max_speed_kmh": safe_round((summary.get("maxSpeed") or 0) * 3.6, 1) if summary.get("maxSpeed") else None,
            "aerobic_te": safe_round(summary.get("aerobicTrainingEffect") or activity.get("aerobicTrainingEffect")),
            "anaerobic_te": safe_round(summary.get("anaerobicTrainingEffect") or activity.get("anaerobicTrainingEffect")),
            "training_load": safe_round(summary.get("activityTrainingLoad") or activity.get("activityTrainingLoad")),
            "vo2_max": summary.get("vO2MaxValue") or activity.get("vO2MaxValue"),
        }

        # Splits / Laps
        if splits and isinstance(splits, dict):
            laps = []
            for lap in splits.get("lapDTOs") or []:
                lap_dist = lap.get("distance") or 0
                lap_dur = lap.get("duration") or 0
                lap_pace = (lap_dur / lap_dist * 1000) if lap_dist > 0 else None
                laps.append({
                    "lap": lap.get("lapIndex"),
                    "distance_m": safe_round(lap_dist, 0),
                    "duration_formatted": format_duration(lap_dur),
                    "pace_formatted": format_pace(lap_pace) if lap_pace else None,
                    "avg_hr": lap.get("averageHR"),
                    "max_hr": lap.get("maxHR"),
                    "avg_power": lap.get("averagePower"),
                    "cadence": safe_round(lap.get("averageRunCadence") or lap.get("averageBikeCadence")),
                    "elevation_gain": lap.get("elevationGain"),
                })
            result["laps"] = laps

        # HR Zones
        if hr_zones and isinstance(hr_zones, list):
            result["hr_zones"] = hr_zones

        # Weather
        if weather and isinstance(weather, dict):
            result["weather"] = {
                "temperature": weather.get("temp"),
                "condition": weather.get("weatherTypeDTO", {}).get("desc") if isinstance(weather.get("weatherTypeDTO"), dict) else None,
                "humidity": weather.get("relativeHumidity"),
                "wind_speed": weather.get("windSpeed"),
                "wind_direction": weather.get("windDirection"),
            }

        # Gear
        if gear and isinstance(gear, list):
            result["gear"] = [{"name": g.get("displayName"), "uuid": g.get("uuid")} for g in gear]

        resp = {"status": "success", "command": "detail", "data": result}
        if warnings:
            resp["warnings"] = warnings
        return resp
    except Exception as exc:
        return {"status": "error", "command": "detail", "message": str(exc)}


def cmd_run(args):
    client, err = get_client()
    if err:
        return {"status": "error", "command": "run", "message": err}

    try:
        activity_id = getattr(args, "activity_id", None)

        if activity_id is None:
            today = datetime.now()
            found = None
            for i in range(30):
                date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
                day_acts = client.get_activities_by_date(date, date, "running")
                if day_acts:
                    found = day_acts[0]
                    break
            if not found:
                return {"status": "error", "command": "run", "message": "最近30天内未找到跑步活动"}
            activity_id = found.get("activityId")
            activity = found
        else:
            acts = client.get_activities_by_date(
                (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
                datetime.now().strftime("%Y-%m-%d"),
                "running",
            )
            activity = next((a for a in acts if str(a.get("activityId")) == str(activity_id)), None)
            if not activity:
                # Try fetching directly
                try:
                    activity = client.get_activity(activity_id)
                    if activity:
                        # Normalize: get_activity returns different structure
                        summary = activity.get("summaryDTO") or {}
                        activity["distance"] = summary.get("distance", 0)
                        activity["duration"] = summary.get("duration", 0)
                        activity["averageHR"] = summary.get("averageHR")
                        activity["maxHR"] = summary.get("maxHR")
                        activity["calories"] = summary.get("calories")
                except Exception:
                    pass
            if not activity:
                return {"status": "error", "command": "run", "message": f"未找到活动 {activity_id}"}

        warnings = []
        splits = None
        try:
            splits = client.get_activity_splits(activity_id)
        except Exception as exc:
            warnings.append(f"分段获取失败: {exc}")

        laps = []
        if splits and isinstance(splits, dict):
            for lap in splits.get("lapDTOs") or []:
                distance = lap.get("distance") or 0
                duration = lap.get("duration") or 0
                pace_sec = (duration / distance * 1000) if distance > 0 else 0
                laps.append({
                    "lap": lap.get("lapIndex"),
                    "distance_m": safe_round(distance, 0),
                    "duration_formatted": format_duration(duration),
                    "pace_formatted": format_pace(pace_sec),
                    "avg_hr": lap.get("averageHR"),
                    "max_hr": lap.get("maxHR"),
                    "avg_power": lap.get("averagePower"),
                    "cadence": safe_round(lap.get("averageRunCadence")),
                    "elevation_gain": lap.get("elevationGain"),
                })

        # Recent runs for comparison
        recent_runs = []
        try:
            today = datetime.now()
            recent_acts = client.get_activities_by_date(
                (today - timedelta(days=60)).strftime("%Y-%m-%d"),
                today.strftime("%Y-%m-%d"),
                "running",
            )
            for act in (recent_acts or []):
                if str(act.get("activityId")) == str(activity_id):
                    continue
                if len(recent_runs) >= 5:
                    break
                dist = act.get("distance") or 0
                dur = act.get("duration") or 0
                pace = (dur / dist * 1000) if dist > 0 else 0
                recent_runs.append({
                    "date": (act.get("startTimeLocal") or "")[:10],
                    "name": act.get("activityName"),
                    "distance_km": safe_round(dist / 1000, 2),
                    "duration_min": safe_round(dur / 60),
                    "pace_formatted": format_pace(pace),
                    "avg_hr": act.get("averageHR"),
                    "aerobic_te": safe_round(act.get("aerobicTrainingEffect")),
                    "vo2_max": act.get("vO2MaxValue"),
                })
        except Exception as exc:
            warnings.append(f"近期跑步对比获取失败: {exc}")

        dist = activity.get("distance") or 0
        dur = activity.get("duration") or 0
        pace = (dur / dist * 1000) if dist > 0 else 0

        result = {
            "activity_id": activity_id,
            "name": activity.get("activityName"),
            "date": activity.get("startTimeLocal"),
            "distance_km": safe_round(dist / 1000, 2),
            "duration_sec": safe_round(dur, 0),
            "duration_formatted": format_duration(dur),
            "pace_formatted": format_pace(pace),
            "avg_hr": activity.get("averageHR"),
            "max_hr": activity.get("maxHR"),
            "calories": activity.get("calories"),
            "avg_power": activity.get("avgPower"),
            "cadence": safe_round(activity.get("averageRunningCadenceInStepsPerMinute")),
            "elevation_gain": activity.get("elevationGain"),
            "aerobic_te": safe_round(activity.get("aerobicTrainingEffect")),
            "anaerobic_te": safe_round(activity.get("anaerobicTrainingEffect")),
            "vo2_max": activity.get("vO2MaxValue"),
            "training_load": safe_round(activity.get("activityTrainingLoad")),
            "laps": laps,
            "recent_runs": recent_runs,
        }

        resp = {"status": "success", "command": "run", "data": result}
        if warnings:
            resp["warnings"] = warnings
        return resp
    except Exception as exc:
        return {"status": "error", "command": "run", "message": str(exc)}


def cmd_sleep(args):
    client, err = get_client()
    if err:
        return {"status": "error", "command": "sleep", "message": err}

    try:
        start_str, end_str, start_dt, end_dt = resolve_date_range(args)
    except ValueError as exc:
        return {"status": "error", "command": "sleep", "message": str(exc)}

    try:
        records = []
        warnings = []

        for date in date_range_iter(start_dt, end_dt):
            try:
                sleep_data = client.get_sleep_data(date)
                parsed = parse_sleep_data(sleep_data)
                if parsed is None:
                    continue
                parsed["date"] = date

                # HRV details
                try:
                    hrv_data = client.get_hrv_data(date)
                    if isinstance(hrv_data, dict):
                        hrv_summary = hrv_data.get("hrvSummary") or {}
                        parsed["hrv_weekly_avg"] = hrv_summary.get("weeklyAvg")
                        parsed["hrv_last_night_avg"] = hrv_summary.get("lastNightAvg")
                        parsed["hrv_last_night_5min_high"] = hrv_summary.get("lastNight5MinHigh")
                        parsed["hrv_status"] = hrv_summary.get("status")
                except Exception:
                    pass

                # Body battery
                try:
                    daily = client.get_user_summary(date)
                    parsed["body_battery_high"] = daily.get("bodyBatteryHighestValue")
                    parsed["body_battery_low"] = daily.get("bodyBatteryLowestValue")
                except Exception:
                    parsed["body_battery_high"] = None
                    parsed["body_battery_low"] = None

                records.append(parsed)
            except Exception as exc:
                warnings.append(f"{date}: {exc}")

        if not records:
            resp = {
                "status": "success",
                "command": "sleep",
                "data": {"records": [], "averages": None},
                "message": f"{start_str} ~ {end_str} 范围内无睡眠数据",
            }
            if warnings:
                resp["warnings"] = warnings
            return resp

        def avg(key):
            values = [r.get(key) for r in records if r.get(key) is not None]
            return round(sum(values) / len(values), 1) if values else None

        averages = {
            "sleep_score": avg("sleep_score"),
            "total_seconds_avg": avg("total_seconds"),
            "total_formatted_avg": format_duration(avg("total_seconds")),
            "avg_overnight_hrv": avg("avg_overnight_hrv"),
            "body_battery_high": avg("body_battery_high"),
            "resting_heart_rate": avg("resting_heart_rate"),
            "days_with_data": len(records),
        }

        resp = {
            "status": "success",
            "command": "sleep",
            "date_range": f"{start_str} ~ {end_str}",
            "data": {"records": records, "averages": averages},
        }
        if warnings:
            resp["warnings"] = warnings
        return resp
    except Exception as exc:
        return {"status": "error", "command": "sleep", "message": str(exc)}


def cmd_health(args):
    client, err = get_client()
    if err:
        return {"status": "error", "command": "health", "message": err}

    try:
        start_str, end_str, start_dt, end_dt = resolve_date_range(args)
    except ValueError as exc:
        return {"status": "error", "command": "health", "message": str(exc)}

    all_metrics = {"hrv", "rhr", "stress", "bb", "spo2", "respiration"}
    if args.metrics:
        requested = set(m.strip().lower() for m in args.metrics.split(","))
        invalid = requested - all_metrics
        if invalid:
            return {
                "status": "error",
                "command": "health",
                "message": f"无效指标: {', '.join(invalid)}。可用: {', '.join(sorted(all_metrics))}",
            }
    else:
        requested = all_metrics

    try:
        records = []
        warnings = []

        for date in date_range_iter(start_dt, end_dt):
            day_data = {"date": date}
            day_warnings = []

            if "hrv" in requested:
                try:
                    hrv = client.get_hrv_data(date)
                    if isinstance(hrv, dict):
                        summary = hrv.get("hrvSummary") or {}
                        baseline = summary.get("baseline") or {}
                        day_data["hrv"] = {
                            "weekly_avg": summary.get("weeklyAvg"),
                            "last_night_avg": summary.get("lastNightAvg"),
                            "last_night_5min_high": summary.get("lastNight5MinHigh"),
                            "status": summary.get("status"),
                            "baseline_low": baseline.get("lowUpper"),
                            "baseline_balanced_low": baseline.get("balancedLow"),
                            "baseline_balanced_upper": baseline.get("balancedUpper"),
                        }
                    else:
                        day_data["hrv"] = None
                except Exception as exc:
                    day_data["hrv"] = None
                    day_warnings.append(f"HRV: {exc}")

            if "rhr" in requested:
                try:
                    rhr = client.get_rhr_day(date)
                    if isinstance(rhr, dict):
                        rhr_values = rhr.get("allMetrics") or {}
                        if isinstance(rhr_values, dict):
                            metrics_list = rhr_values.get("metricsMap", {}).get("WELLNESS_RESTING_HEART_RATE", [])
                            if metrics_list and isinstance(metrics_list, list):
                                day_data["resting_heart_rate"] = metrics_list[0].get("value")
                            else:
                                day_data["resting_heart_rate"] = None
                        else:
                            day_data["resting_heart_rate"] = None
                    else:
                        day_data["resting_heart_rate"] = None
                except Exception as exc:
                    day_data["resting_heart_rate"] = None
                    day_warnings.append(f"RHR: {exc}")

            if "stress" in requested:
                try:
                    stress = client.get_all_day_stress(date)
                    if isinstance(stress, dict):
                        day_data["stress"] = {
                            "overall_level": stress.get("overallStressLevel"),
                            "rest_stress_duration": stress.get("restStressDuration"),
                            "activity_stress_duration": stress.get("activityStressDuration"),
                            "low_stress_duration": stress.get("lowStressDuration"),
                            "medium_stress_duration": stress.get("mediumStressDuration"),
                            "high_stress_duration": stress.get("highStressDuration"),
                        }
                    else:
                        day_data["stress"] = None
                except Exception as exc:
                    day_data["stress"] = None
                    day_warnings.append(f"Stress: {exc}")

            if "bb" in requested:
                try:
                    bb = client.get_body_battery(date)
                    if isinstance(bb, list) and bb:
                        item = bb[0] if isinstance(bb[0], dict) else {}
                        day_data["body_battery"] = {
                            "charged": item.get("charged"),
                            "drained": item.get("drained"),
                            "start_level": item.get("startTimestampGMT"),
                            "end_level": item.get("endTimestampGMT"),
                        }
                    elif isinstance(bb, dict):
                        day_data["body_battery"] = bb
                    else:
                        # Fallback to user_summary
                        try:
                            daily = client.get_user_summary(date)
                            day_data["body_battery"] = {
                                "highest": daily.get("bodyBatteryHighestValue"),
                                "lowest": daily.get("bodyBatteryLowestValue"),
                                "most_recent": daily.get("bodyBatteryMostRecentValue"),
                            }
                        except Exception:
                            day_data["body_battery"] = None
                except Exception as exc:
                    day_data["body_battery"] = None
                    day_warnings.append(f"Body Battery: {exc}")

            if "spo2" in requested:
                try:
                    spo2 = client.get_spo2_data(date)
                    if isinstance(spo2, dict):
                        day_data["spo2"] = {
                            "average": spo2.get("averageSpO2"),
                            "lowest": spo2.get("lowestSpO2"),
                            "latest": spo2.get("latestSpO2"),
                        }
                    else:
                        day_data["spo2"] = None
                except Exception as exc:
                    day_data["spo2"] = None
                    day_warnings.append(f"SpO2: {exc}")

            if "respiration" in requested:
                try:
                    resp_data = client.get_respiration_data(date)
                    if isinstance(resp_data, dict):
                        day_data["respiration"] = {
                            "avg_waking": resp_data.get("avgWakingRespirationValue"),
                            "avg_sleeping": resp_data.get("avgSleepRespirationValue"),
                            "highest": resp_data.get("highestRespirationValue"),
                            "lowest": resp_data.get("lowestRespirationValue"),
                        }
                    else:
                        day_data["respiration"] = None
                except Exception as exc:
                    day_data["respiration"] = None
                    day_warnings.append(f"Respiration: {exc}")

            if day_warnings:
                warnings.extend([f"{date} - {w}" for w in day_warnings])

            records.append(day_data)

        # Summary statistics
        summary_stats = {}
        if "rhr" in requested:
            rhr_vals = [r["resting_heart_rate"] for r in records if r.get("resting_heart_rate") is not None]
            if rhr_vals:
                summary_stats["resting_heart_rate"] = {
                    "avg": safe_round(sum(rhr_vals) / len(rhr_vals)),
                    "min": min(rhr_vals),
                    "max": max(rhr_vals),
                }

        if "hrv" in requested:
            hrv_vals = [
                r["hrv"]["last_night_avg"]
                for r in records
                if r.get("hrv") and isinstance(r["hrv"], dict) and r["hrv"].get("last_night_avg") is not None
            ]
            if hrv_vals:
                summary_stats["hrv_last_night_avg"] = {
                    "avg": safe_round(sum(hrv_vals) / len(hrv_vals)),
                    "min": safe_round(min(hrv_vals)),
                    "max": safe_round(max(hrv_vals)),
                }

        if "stress" in requested:
            stress_vals = [
                r["stress"]["overall_level"]
                for r in records
                if r.get("stress") and isinstance(r["stress"], dict) and r["stress"].get("overall_level") is not None
            ]
            if stress_vals:
                summary_stats["stress_overall"] = {
                    "avg": safe_round(sum(stress_vals) / len(stress_vals)),
                    "min": min(stress_vals),
                    "max": max(stress_vals),
                }

        resp = {
            "status": "success",
            "command": "health",
            "date_range": f"{start_str} ~ {end_str}",
            "metrics": sorted(requested),
            "data": records,
            "summary": summary_stats if summary_stats else None,
        }
        if warnings:
            resp["warnings"] = warnings
        return resp
    except Exception as exc:
        return {"status": "error", "command": "health", "message": str(exc)}


def cmd_export(args):
    client, err = get_client()
    if err:
        return {"status": "error", "command": "export", "message": err}

    activity_id = args.activity_id
    fmt = args.format
    output_dir = args.output

    fmt_map = {
        "fit": "ORIGINAL",
        "gpx": "GPX",
        "tcx": "TCX",
        "csv": "CSV",
    }

    try:
        dl_fmt = Garmin.ActivityDownloadFormat[fmt_map[fmt]]
        data = client.download_activity(activity_id, dl_fmt=dl_fmt)

        if not data:
            return {"status": "error", "command": "export", "message": f"活动 {activity_id} 导出数据为空"}

        os.makedirs(output_dir, exist_ok=True)

        if fmt == "fit":
            # FIT comes as a zip
            zip_path = os.path.join(output_dir, f"{activity_id}.zip")
            with open(zip_path, "wb") as f:
                f.write(data)

            # Extract FIT file from zip
            fit_path = None
            try:
                with zipfile.ZipFile(zip_path, "r") as zf:
                    fit_files = [n for n in zf.namelist() if n.lower().endswith(".fit")]
                    if fit_files:
                        zf.extract(fit_files[0], output_dir)
                        fit_path = os.path.join(output_dir, fit_files[0])
                os.remove(zip_path)
            except zipfile.BadZipFile:
                # Maybe it's already a FIT file, not a zip
                fit_path = os.path.join(output_dir, f"{activity_id}.fit")
                os.rename(zip_path, fit_path)

            file_path = fit_path or zip_path
        else:
            ext = fmt
            file_path = os.path.join(output_dir, f"{activity_id}.{ext}")
            with open(file_path, "wb") as f:
                f.write(data)

        file_size = os.path.getsize(file_path)
        return {
            "status": "success",
            "command": "export",
            "data": {
                "activity_id": activity_id,
                "format": fmt,
                "file_path": os.path.abspath(file_path),
                "size_bytes": file_size,
            },
        }
    except Exception as exc:
        return {"status": "error", "command": "export", "message": str(exc)}


# ── CLI Entry Point ───────────────────────────────────────────────────


def add_date_range_args(parser, default_days=7):
    parser.add_argument("--start", type=str, default=None, help="起始日期 YYYY-MM-DD")
    parser.add_argument("--end", type=str, default=None, help="结束日期 YYYY-MM-DD")
    parser.add_argument("--days", type=int, default=default_days, help=f"最近天数 (默认 {default_days})")


def main():
    parser = argparse.ArgumentParser(description="Garmin Connect CN (佳明中国) CLI")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # login
    p_login = subparsers.add_parser("login", help="登录佳明中国账号")
    p_login.add_argument("email", help="邮箱")
    p_login.add_argument("password", help="密码")

    # status
    subparsers.add_parser("status", help="检查登录状态")

    # summary
    p_summary = subparsers.add_parser("summary", help="每日综合健康摘要")
    p_summary.add_argument("--date", type=str, default=None, help="指定日期 YYYY-MM-DD (默认今天)")

    # activities
    p_activities = subparsers.add_parser("activities", help="查询活动列表")
    add_date_range_args(p_activities)
    p_activities.add_argument("--type", type=str, default=None, help="活动类型 (running, cycling, swimming, etc.)")

    # detail
    p_detail = subparsers.add_parser("detail", help="活动详细数据")
    p_detail.add_argument("activity_id", help="活动ID")

    # run
    p_run = subparsers.add_parser("run", help="跑步专项分析")
    p_run.add_argument("activity_id", nargs="?", default=None, help="活动ID (默认最近一次跑步)")

    # sleep
    p_sleep = subparsers.add_parser("sleep", help="睡眠数据查询")
    add_date_range_args(p_sleep)

    # health
    p_health = subparsers.add_parser("health", help="健康指标查询")
    add_date_range_args(p_health)
    p_health.add_argument("--metrics", type=str, default=None, help="指标列表，逗号分隔: hrv,rhr,stress,bb,spo2,respiration (默认全部)")

    # export
    p_export = subparsers.add_parser("export", help="导出活动数据文件")
    p_export.add_argument("activity_id", help="活动ID")
    p_export.add_argument("--format", choices=["fit", "gpx", "tcx", "csv"], default="fit", help="导出格式 (默认 fit)")
    p_export.add_argument("--output", type=str, default=".", help="输出目录 (默认当前目录)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if Garmin is None:
        output_json({"status": "error", "message": "garminconnect 未安装。请确保通过 uv 运行此脚本。"})
        sys.exit(1)

    cmd_map = {
        "login": cmd_login,
        "status": cmd_status,
        "summary": cmd_summary,
        "activities": cmd_activities,
        "detail": cmd_detail,
        "run": cmd_run,
        "sleep": cmd_sleep,
        "health": cmd_health,
        "export": cmd_export,
    }

    handler = cmd_map.get(args.command)
    if handler:
        result = handler(args)
    else:
        result = {"status": "error", "message": f"未知命令: {args.command}"}

    output_json(result)


if __name__ == "__main__":
    main()
