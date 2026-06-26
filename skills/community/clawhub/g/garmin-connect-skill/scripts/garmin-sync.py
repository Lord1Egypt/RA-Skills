#!/usr/bin/env python3
# Author: SQ
"""
Garmin Connect Data Sync
Syncs all fitness data using saved credentials
Supports both global (garmin.com) and China (garmin.cn) regions
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    from garminconnect import Garmin
except ImportError:
    print("❌ Dependencies not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

def load_credentials():
    """Load saved Garmin credentials"""
    import base64
    
    session_file = Path.home() / ".garth" / "session.json"
    
    if not session_file.exists():
        print(f"❌ No credentials found at {session_file}")
        print("\nRun: python3 garmin-auth.py <email> <password> [--cn]")
        return None
    
    try:
        with open(session_file, 'r') as f:
            creds = json.load(f)
        
        # Decrypt password
        if 'password_encrypted' in creds:
            creds['password'] = base64.b64decode(creds['password_encrypted']).decode()
        
        return creds
    except Exception as e:
        print(f"❌ Failed to load credentials: {e}")
        return None

def get_garmin_client():
    """Initialize Garmin client with saved credentials"""
    creds = load_credentials()
    if not creds:
        return None
    
    try:
        # Initialize with saved credentials
        garmin = Garmin(
            creds['email'],
            creds['password'],
            is_cn=creds.get('is_cn', False)
        )
        garmin.login()
        return garmin
    except Exception as e:
        print(f"❌ Failed to connect to Garmin: {e}")
        return None

def get_daily_summary(garmin_client, date_str):
    """Get daily summary: steps, HR, calories, active minutes, and more"""

    data = {
        'steps': 0,
        'heart_rate_resting': 0,
        'heart_rate_min': 0,
        'heart_rate_max': 0,
        'calories': 0,
        'calories_active': 0,
        'calories_bmr': 0,
        'active_minutes': 0,
        'distance_km': 0,
        'floors_ascended': 0,
        'floors_descended': 0,
        'intensity_minutes': 0,
        'moderate_intensity_minutes': 0,
        'vigorous_intensity_minutes': 0,
    }

    try:
        summary = garmin_client.get_user_summary(date_str)

        data['steps'] = summary.get('totalSteps', 0)
        data['heart_rate_resting'] = summary.get('restingHeartRate', 0)
        data['calories'] = summary.get('totalKilocalories', 0)
        data['active_minutes'] = summary.get('totalIntensityMinutes', 0)
        data['distance_km'] = round(summary.get('totalDistance', 0) / 1000, 2)

    except Exception as e:
        print(f"⚠️  Daily summary error: {e}", file=sys.stderr)

    # Get more detailed stats from get_stats
    try:
        stats = garmin_client.get_stats(date_str)

        data['heart_rate_min'] = stats.get('minHeartRate', 0)
        data['heart_rate_max'] = stats.get('maxHeartRate', 0)
        data['calories_active'] = stats.get('activeKilocalories', 0)
        data['calories_bmr'] = stats.get('bmrKilocalories', 0)
        data['floors_ascended'] = stats.get('floorsAscended', 0)
        data['floors_descended'] = stats.get('floorsDescended', 0)
        data['intensity_minutes'] = stats.get('moderateIntensityMinutes', 0) + stats.get('vigorousIntensityMinutes', 0)
        data['moderate_intensity_minutes'] = stats.get('moderateIntensityMinutes', 0)
        data['vigorous_intensity_minutes'] = stats.get('vigorousIntensityMinutes', 0)

    except Exception as e:
        print(f"⚠️  Stats error: {e}", file=sys.stderr)

    return data

def get_sleep_data(garmin_client, date_str):
    """Get sleep data: duration, quality, deep/REM sleep, naps

    Smart merge: If nap duration >= 3 hours and in late-night window (22:00-10:00),
    automatically promote to main sleep (for users who sleep late).
    """

    data = {
        'duration_hours': 0,
        'duration_minutes': 0,
        'quality_percent': 0,
        'deep_sleep_hours': 0,
        'rem_sleep_hours': 0,
        'light_sleep_hours': 0,
        'awake_minutes': 0,
        'nap_count': 0,
        'nap_total_minutes': 0,
        'nap_details': [],
        'sleep_source': 'none',  # 'main', 'promoted_nap', 'none'
    }

    try:
        sleep = garmin_client.get_sleep_data(date_str)

        if sleep and 'dailySleepDTO' in sleep:
            s = sleep['dailySleepDTO']

            # Safe division: handle None values
            def safe_div(value, divisor, default=0):
                if value is None:
                    return default
                try:
                    return round(value / divisor, 1)
                except (TypeError, ZeroDivisionError):
                    return default

            # Main sleep data
            duration_sec = s.get('sleepTimeSeconds') or 0

            # Check if we should promote a nap to main sleep
            nap_to_promote = None
            if duration_sec == 0 and 'dailyNapDTOS' in s and s['dailyNapDTOS']:
                # No main sleep, check if any nap qualifies for promotion
                for nap in s['dailyNapDTOS']:
                    nap_sec = nap.get('napTimeSec', 0)
                    nap_min = round(nap_sec / 60, 0)

                    # Check duration: >= 3 hours (180 minutes)
                    if nap_min < 180:
                        continue

                    # Check time window: sleep starts between 22:00-10:00 local time
                    from datetime import datetime, timedelta
                    start_gmt = nap.get('napStartTimestampGMT', '')
                    if start_gmt:
                        start_dt = datetime.fromisoformat(start_gmt.replace('Z', '+00:00'))
                        start_local = start_dt + timedelta(hours=8)
                        start_hour = start_local.hour

                        # Late-night window: 22:00 - 10:00 (next day)
                        if start_hour >= 22 or start_hour < 10:
                            nap_to_promote = nap
                            break  # Promote the first qualifying nap

            if nap_to_promote:
                # Promote nap to main sleep
                nap_sec = nap_to_promote.get('napTimeSec', 0)
                data['duration_hours'] = safe_div(nap_sec, 3600)
                data['duration_minutes'] = safe_div(nap_sec, 60)
                # Nap data doesn't include quality scores, set defaults
                data['quality_percent'] = 70  # Default: fair
                data['sleep_score'] = 70
                data['sleep_source'] = 'promoted_nap'
                print(f"💤 Nap promoted to main sleep: {data['duration_hours']}h", file=sys.stderr)
            else:
                # Use main sleep data (even if zero)
                data['duration_hours'] = safe_div(duration_sec, 3600)
                data['duration_minutes'] = safe_div(duration_sec, 60)
                data['quality_percent'] = s.get('sleepQualityPercentage') or 0
                data['sleep_score'] = s.get('sleepQualityPercentage') or 0
                data['deep_sleep_hours'] = safe_div(s.get('deepSleepSeconds'), 3600)
                data['rem_sleep_hours'] = safe_div(s.get('remSleepSeconds'), 3600)
                data['light_sleep_hours'] = safe_div(s.get('lightSleepSeconds'), 3600)
                data['awake_minutes'] = safe_div(s.get('awakeTimeSeconds'), 60)

                if duration_sec > 0:
                    data['sleep_source'] = 'main'

            # Nap data (小睡数据) - always collect for reference
            if 'dailyNapDTOS' in s and s['dailyNapDTOS']:
                data['nap_count'] = len(s['dailyNapDTOS'])
                for nap in s['dailyNapDTOS']:
                    nap_sec = nap.get('napTimeSec', 0)
                    nap_min = round(nap_sec / 60, 0)
                    data['nap_total_minutes'] += nap_min

                    # Convert UTC to local time (GMT+8 for China)
                    from datetime import datetime, timedelta
                    start_gmt = nap.get('napStartTimestampGMT', '')
                    end_gmt = nap.get('napEndTimestampGMT', '')

                    if start_gmt and end_gmt:
                        start_dt = datetime.fromisoformat(start_gmt.replace('Z', '+00:00'))
                        end_dt = datetime.fromisoformat(end_gmt.replace('Z', '+00:00'))
                        start_local = start_dt + timedelta(hours=8)
                        end_local = end_dt + timedelta(hours=8)

                        data['nap_details'].append({
                            'duration_minutes': nap_min,
                            'start_time': start_local.strftime('%H:%M'),
                            'end_time': end_local.strftime('%H:%M'),
                        })

    except Exception as e:
        print(f"⚠️  Sleep data error: {e}", file=sys.stderr)

    return data

def get_workouts(garmin_client):
    """Get recent workouts with correct timestamps"""

    workouts = []

    try:
        activities = garmin_client.get_activities(0, 20)  # Last 20 workouts

        for activity in activities[:10]:  # Return last 10
            # 获取startTimeGMT并转换为时间戳
            start_time_gmt = activity.get('startTimeGMT', None)
            timestamp = 0
            date_str = ''

            if start_time_gmt:
                try:
                    # startTimeGMT是ISO 8601格式字符串，如 "2026-03-12 12:46:47"
                    dt = datetime.fromisoformat(start_time_gmt.replace('Z', '+00:00'))
                    timestamp = int(dt.timestamp())
                    date_str = dt.strftime('%Y-%m-%d')
                except Exception as e:
                    print(f"⚠️  Failed to parse startTimeGMT: {e}", file=sys.stderr)

            workout = {
                'type': activity.get('activityType', 'Unknown'),
                'name': activity.get('activityName', 'Unnamed'),
                'distance_km': round(activity.get('distance', 0) / 1000, 2),
                'duration_minutes': round(activity.get('duration', 0) / 60, 0),
                'calories': activity.get('calories', 0),
                'heart_rate_avg': activity.get('avgHeartRate', 0),
                'heart_rate_max': activity.get('maxHeartRate', 0),
                'timestamp': timestamp,  # 正确的Unix时间戳
                'date': date_str,  # 日期字符串 (YYYY-MM-DD)
            }
            workouts.append(workout)

    except Exception as e:
        print(f"⚠️  Workouts error: {e}", file=sys.stderr)

    return workouts


def get_vo2_max(garmin_client, date_str):
    """Get VO2 Max data (checks today and yesterday)"""

    data = {
        'vo2_max': 0,
        'vo2_max_precise': 0,
        'fitness_age': None,
        'date': None,
    }

    try:
        from datetime import timedelta

        # Try today first
        max_metrics = garmin_client.get_max_metrics(date_str)

        # If no data today, try yesterday
        if not max_metrics or len(max_metrics) == 0:
            yesterday = (datetime.strptime(date_str, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
            max_metrics = garmin_client.get_max_metrics(yesterday)
            if max_metrics and len(max_metrics) > 0:
                data['date'] = yesterday

        if max_metrics and len(max_metrics) > 0:
            generic = max_metrics[0].get('generic', {})
            data['vo2_max'] = generic.get('vo2MaxValue', 0)
            data['vo2_max_precise'] = generic.get('vo2MaxPreciseValue', 0)
            data['fitness_age'] = generic.get('fitnessAge')
            if not data['date']:
                data['date'] = date_str

    except Exception as e:
        print(f"⚠️  VO2 Max error: {e}", file=sys.stderr)

    return data


def get_body_battery(garmin_client, date_str):
    """Get body battery data"""

    data = {
        'charged': 0,
        'drained': 0,
        'highest': 0,
        'lowest': 0,
        'current': 0,
        'most_recent': 0,  # 实时值（来自时序数据最新值）
    }

    try:
        # 使用 get_body_battery() API 获取时序数据
        bb_data = garmin_client.get_body_battery(date_str)

        if bb_data and isinstance(bb_data, list) and len(bb_data) > 0:
            day_data = bb_data[0]

            data['charged'] = day_data.get('charged', 0)
            data['drained'] = day_data.get('drained', 0)

            # 从时序数组获取最高、最低、当前值
            values_array = day_data.get('bodyBatteryValuesArray', [])
            if values_array:
                battery_values = [v[1] for v in values_array if isinstance(v, list) and len(v) >= 2 and v[1] is not None]
                if battery_values:
                    data['highest'] = max(battery_values)
                    data['lowest'] = min(battery_values)
                    # 最后一个值是实时值
                    data['current'] = battery_values[-1]
                    data['most_recent'] = battery_values[-1]
                else:
                    # 如果时序为空，回退到旧方法
                    stats = garmin_client.get_stats(date_str)
                    data['highest'] = stats.get('bodyBatteryHighestValue', 0)
                    data['lowest'] = stats.get('bodyBatteryLowestValue', 0)
                    data['current'] = stats.get('bodyBatteryHighestValue', 0) - data['drained'] + data['charged']
                    data['most_recent'] = data['current']
            else:
                # 没有时序数据，使用 get_stats()
                stats = garmin_client.get_stats(date_str)
                data['highest'] = stats.get('bodyBatteryHighestValue', 0)
                data['lowest'] = stats.get('bodyBatteryLowestValue', 0)
                data['current'] = data['highest'] - data['drained'] + data['charged']
                data['most_recent'] = data['current']
        else:
            # API返回格式异常，回退到 get_stats()
            stats = garmin_client.get_stats(date_str)
            data['charged'] = stats.get('bodyBatteryChargedValue', 0)
            data['drained'] = stats.get('bodyBatteryDrainedValue', 0)
            data['highest'] = stats.get('bodyBatteryHighestValue', 0)
            data['lowest'] = stats.get('bodyBatteryLowestValue', 0)
            data['current'] = data['highest'] - data['drained'] + data['charged']
            data['most_recent'] = data['current']

    except Exception as e:
        print(f"⚠️  Body battery error: {e}", file=sys.stderr)
        # 出错时回退到 get_stats()
        try:
            stats = garmin_client.get_stats(date_str)
            data['charged'] = stats.get('bodyBatteryChargedValue', 0)
            data['drained'] = stats.get('bodyBatteryDrainedValue', 0)
            data['highest'] = stats.get('bodyBatteryHighestValue', 0)
            data['lowest'] = stats.get('bodyBatteryLowestValue', 0)
            data['current'] = data['highest'] - data['drained'] + data['charged']
            data['most_recent'] = data['current']
        except:
            pass

    return data


def get_stress_data(garmin_client, date_str):
    """Get stress data"""

    data = {
        'average': 0,
        'max': 0,
        'stress_percentage': 0,
        'rest_percentage': 0,
        'activity_percentage': 0,
        'low_stress_percentage': 0,
        'medium_stress_percentage': 0,
        'high_stress_percentage': 0,
    }

    try:
        stats = garmin_client.get_stats(date_str)

        data['average'] = stats.get('averageStressLevel', 0)
        data['max'] = stats.get('maxStressLevel', 0)
        data['stress_percentage'] = stats.get('stressPercentage', 0)
        data['rest_percentage'] = stats.get('restStressPercentage', 0)
        data['activity_percentage'] = stats.get('activityStressPercentage', 0)
        data['low_stress_percentage'] = stats.get('lowStressPercentage', 0)
        data['medium_stress_percentage'] = stats.get('mediumStressPercentage', 0)
        data['high_stress_percentage'] = stats.get('highStressPercentage', 0)

    except Exception as e:
        print(f"⚠️  Stress data error: {e}", file=sys.stderr)

    return data


def get_hrv_data(garmin_client, date_str):
    """Get Heart Rate Variability data"""

    data = {
        'hrv_last_night': 0,
        'hrv_weekly_avg': 0,
    }

    try:
        hrv = garmin_client.get_hrv_data(date_str)

        if hrv and len(hrv) > 0:
            # Get the most recent HRV reading
            data['hrv_last_night'] = hrv[0].get('hrvValue', 0) if isinstance(hrv[0], dict) else 0

        # Weekly average might need separate call
        # For now, just store nightly HRV

    except Exception as e:
        print(f"⚠️  HRV error: {e}", file=sys.stderr)

    return data


def get_fitness_age(garmin_client, date_str):
    """Get Fitness Age data"""

    data = {
        'chronological_age': 0,
        'fitness_age': 0,
        'achievable_fitness_age': 0,
        'priority_area': None,
    }

    try:
        fit_age = garmin_client.get_fitnessage_data(date_str)

        if fit_age:
            data['chronological_age'] = fit_age.get('chronologicalAge', 0)
            data['fitness_age'] = round(fit_age.get('fitnessAge', 0), 1)
            data['achievable_fitness_age'] = round(fit_age.get('achievableFitnessAge', 0), 1)

            # Find the priority area (lowest priority value = highest priority)
            components = fit_age.get('components', {})
            if components:
                best_priority = 999
                best_area = None
                for area_name, area_data in components.items():
                    if isinstance(area_data, dict) and 'priority' in area_data:
                        priority = area_data['priority']
                        if priority < best_priority:
                            best_priority = priority
                            best_area = area_name
                data['priority_area'] = best_area

    except Exception as e:
        print(f"⚠️  Fitness age error: {e}", file=sys.stderr)

    return data


def get_respiration_data(garmin_client, date_str):
    """Get respiration data"""

    data = {
        'avg_respiration': 0,
        'highest_respiration': 0,
        'lowest_respiration': 0,
        'sleep_respiration': 0,
    }

    try:
        resp = garmin_client.get_respiration_data(date_str)

        if resp:
            data['avg_respiration'] = resp.get('avgRespirationValue', 0)
            data['highest_respiration'] = resp.get('highestRespirationValue', 0)
            data['lowest_respiration'] = resp.get('lowestRespirationValue', 0)
            data['sleep_respiration'] = resp.get('sleepRespirationValue', 0)

    except Exception as e:
        print(f"⚠️  Respiration error: {e}", file=sys.stderr)

    return data


def get_lactate_threshold(garmin_client):
    """Get lactate threshold (functional threshold power) data"""

    data = {
        'ftp_watts': 0,
        'power_to_weight': 0,
        'threshold_heart_rate': 0,
        'threshold_speed': 0,
    }

    try:
        lt = garmin_client.get_lactate_threshold()

        if lt and 'power' in lt:
            power = lt['power']
            data['ftp_watts'] = power.get('functionalThresholdPower', 0)
            data['power_to_weight'] = power.get('powerToWeight', 0)

        if lt and 'speed_and_heart_rate' in lt:
            shr = lt['speed_and_heart_rate']
            data['threshold_heart_rate'] = shr.get('heartRate', 0)
            # Speed in m/s, convert to min/km for running
            speed_ms = float(shr.get('speed') or 0)
            if speed_ms and speed_ms > 0:
                # m/s to min/km = 1000 / (speed_ms * 60)
                data['threshold_speed'] = round(1000 / (speed_ms * 60), 2)

    except Exception as e:
        print(f"⚠️  Lactate threshold error: {e}", file=sys.stderr)

    return data

def sync_all(output_file=None):
    """Sync all Garmin data including all available health metrics"""

    garmin_client = get_garmin_client()
    if not garmin_client:
        return None

    from datetime import timedelta, timezone

    # 获取北京时间（UTC+8）
    beijing_tz = timezone(timedelta(hours=8))
    now_beijing = datetime.now(beijing_tz)
    hour = now_beijing.hour

    # 智能日期选择：如果现在是0-5点，视为前一天
    if hour < 5:
        target_date = (now_beijing - timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        target_date = now_beijing.strftime("%Y-%m-%d")

    # 先获取运动记录（用于推断实际数据日期）
    workouts = get_workouts(garmin_client)

    # 根据最新运动记录的日期推断实际数据日期
    actual_date = target_date  # 默认使用目标日期

    if workouts and len(workouts) > 0:
        # 找到最新的有日期的运动记录
        for workout in workouts:
            if 'date' in workout and workout['date']:
                workout_date = workout['date']
                # 如果运动日期与目标日期相差不超过1天，使用运动日期
                workout_dt = datetime.strptime(workout_date, '%Y-%m-%d')
                target_dt = datetime.strptime(target_date, '%Y-%m-%d')
                diff = abs((workout_dt - target_dt).days)

                if diff <= 1:
                    actual_date = workout_date
                    break

    # 获取实际日期的数据
    summary = get_daily_summary(garmin_client, actual_date)

    # 获取其他健康数据（先获取，保证在 all_data 之前定义）
    bb = get_body_battery(garmin_client, actual_date)
    stress = get_stress_data(garmin_client, actual_date)
    vo2 = get_vo2_max(garmin_client, actual_date)
    fa = get_fitness_age(garmin_client, actual_date)

    # Collect all data - field names must match garmin_db_reader.py / sync_all.py expectations
    all_data = {
        'timestamp': datetime.now().isoformat(),
        'date': actual_date,  # 使用运动记录的实际日期
        'summary': {
            'steps': summary.get('steps', 0),
            'heart_rate_resting': summary.get('heart_rate_resting', 0),
            'heart_rate_min': summary.get('heart_rate_min', 0),
            'heart_rate_max': summary.get('heart_rate_max', 0),
            'calories': summary.get('calories', 0),
            'calories_active': summary.get('calories_active', 0),
            'calories_bmr': summary.get('calories_bmr', 0),
            'active_minutes': summary.get('active_minutes', 0),
            'distance_km': summary.get('distance_km', 0),
            'floors_ascended': summary.get('floors_ascended', 0),
            'floors_descended': summary.get('floors_descended', 0),
            'intensity_minutes': summary.get('intensity_minutes', 0),
            'moderate_intensity_minutes': summary.get('moderate_intensity_minutes', 0),
            'vigorous_intensity_minutes': summary.get('vigorous_intensity_minutes', 0),
            # Extended fields needed by report scripts
            'body_battery_current': bb.get('most_recent') or bb.get('current', 0),
            'body_battery_highest': bb.get('highest', 0),
            'body_battery_lowest': bb.get('lowest', 0),
            'stress_average': stress.get('average', 0),
            'vo2_max': vo2.get('vo2_max', 0),
            'fitness_age': fa.get('fitness_age', 0),
        },
        'sleep': get_sleep_data(garmin_client, actual_date),
        'workouts': workouts,
        'vo2_max': vo2,
        'body_battery': bb,
        'stress': stress,
        'hrv': get_hrv_data(garmin_client, actual_date),
        'fitness_age': fa,
        'respiration': get_respiration_data(garmin_client, actual_date),
        'lactate_threshold': get_lactate_threshold(garmin_client),
    }

    # Save to file if specified
    if output_file:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(all_data, f, indent=2)

    # Print JSON to stdout
    print(json.dumps(all_data, indent=2))

    return all_data

if __name__ == "__main__":
    
    # Default cache file
    cache_file = os.path.expanduser('~/.clawdbot/.garmin-cache.json')
    
    # Use custom path if provided
    if len(sys.argv) > 1:
        cache_file = sys.argv[1]
    
    sync_all(cache_file)
