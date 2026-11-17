#!/usr/bin/env python3
"""
Fetch health data from Garmin Connect.
Outputs JSON to stdout for parsing by the agent.
"""

import json
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Import auth helper
sys.path.insert(0, str(Path(__file__).parent))
from garmin_auth import get_client

try:
    from garminconnect import Garmin
except ImportError:
    print('{"error": "garminconnect not installed. Run: pip3 install garminconnect"}', file=sys.stderr)
    sys.exit(1)


def get_date_range(days=None, start=None, end=None):
    """Calculate date range for queries."""
    if start and end:
        return start, end
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days or 7)
    
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


def _loc_ms(ms):
    """Epoch ms -> local 'YYYY-MM-DD HH:MM:SS' (system TZ, Europe/Helsinki)."""
    if not ms:
        return None
    try:
        return datetime.fromtimestamp(ms / 1000).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return None


def fetch_sleep(client, days=7, start=None, end=None):
    """Fetch sleep data."""
    start_date, end_date = get_date_range(days, start, end)
    
    try:
        sleep_data = []
        current = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            try:
                data = client.get_sleep_data(date_str)
                if data:
                    # Sleep data is nested inside dailySleepDTO
                    sleep_dto = data.get("dailySleepDTO", {})
                    if sleep_dto:
                        sleep_data.append({
                            "date": date_str,
                            "sleep_time_seconds": sleep_dto.get("sleepTimeSeconds"),
                            "deep_sleep_seconds": sleep_dto.get("deepSleepSeconds"),
                            "light_sleep_seconds": sleep_dto.get("lightSleepSeconds"),
                            "rem_sleep_seconds": sleep_dto.get("remSleepSeconds"),
                            "awake_seconds": sleep_dto.get("awakeSleepSeconds"),
                            "sleep_score": sleep_dto.get("sleepScores", {}).get("overall", {}).get("value"),
                            "restless_periods": data.get("restlessMomentsCount"),  # This is on root
                            # Epoch ms, local-shifted. NOTE: the telemetry key is
                            # avgHeartRate, not averageHeartRate (the latter is
                            # always None in this payload).
                            "sleep_start_ms": sleep_dto.get("sleepStartTimestampLocal"),
                            "sleep_end_ms": sleep_dto.get("sleepEndTimestampLocal"),
                            # Local wall-clock strings. These are the keys the
                            # heartbeat writes to garmin.sleep, so they MUST be
                            # present or the hourly path contributes no timing.
                            "sleep_start": _loc_ms(sleep_dto.get("sleepStartTimestampLocal")),
                            "sleep_end": _loc_ms(sleep_dto.get("sleepEndTimestampLocal")),
                            "avg_hr": sleep_dto.get("avgHeartRate"),
                            "avg_sleep_stress": sleep_dto.get("avgSleepStress"),
                            "avg_hrv": data.get("avgOvernightHrv"),  # This is on root
                            "avg_respiration": sleep_dto.get("averageRespirationValue"),
                            "high_respiration": sleep_dto.get("highestRespirationValue"),
                            "low_respiration": sleep_dto.get("lowestRespirationValue"),
                            "avg_spo2": sleep_dto.get("averageSpO2Value"),
                            "low_spo2": sleep_dto.get("lowestSpO2Value"),
                            "sleep_window_confirmed": sleep_dto.get("sleepWindowConfirmed"),
                            "sleep_from_device": sleep_dto.get("sleepFromDevice"),
                        })
            except Exception as e:
                print(f"⚠️  No sleep data for {date_str}: {e}", file=sys.stderr)
            
            current += timedelta(days=1)
        
        return {"sleep": sleep_data, "start": start_date, "end": end_date}
    
    except Exception as e:
        return {"error": str(e)}


def fetch_hrv(client, days=7, start=None, end=None):
    """Fetch HRV data."""
    start_date, end_date = get_date_range(days, start, end)
    
    try:
        hrv_data = []
        current = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            try:
                data = client.get_hrv_data(date_str)
                if data and "hrvSummary" in data:
                    summary = data["hrvSummary"]
                    hrv_data.append({
                        "date": date_str,
                        "last_night_avg": summary.get("lastNightAvg"),
                        "last_night_5min_high": summary.get("lastNight5MinHigh"),
                        "last_night_5min_low": summary.get("lastNight5MinLow"),
                        "weekly_avg": summary.get("weeklyAvg"),
                        "baseline_balanced_low": summary.get("baselineBalancedLow"),
                        "baseline_balanced_high": summary.get("baselineBalancedHigh"),
                        "status": summary.get("status")
                    })
            except Exception:
                pass
            
            current += timedelta(days=1)
        
        return {"hrv": hrv_data, "start": start_date, "end": end_date}
    
    except Exception as e:
        return {"error": str(e)}


def fetch_body_battery(client, days=7, start=None, end=None):
    """Fetch Body Battery data (Garmin's recovery metric)."""
    start_date, end_date = get_date_range(days, start, end)
    
    try:
        bb_data = []
        current = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            try:
                data = client.get_body_battery(date_str)
                if data and len(data) > 0:
                    day_data = data[0]
                    charged = day_data.get("charged")
                    drained = day_data.get("drained")
                    
                    # Parse bodyBatteryValuesArray to get highest/lowest
                    values_array = day_data.get("bodyBatteryValuesArray", [])
                    values = [v[1] for v in values_array if len(v) > 1]  # Extract values from [timestamp, value] pairs
                    
                    highest = max(values) if values else None
                    lowest = min(values) if values else None
                    
                    bb_data.append({
                        "date": date_str,
                        "charged": charged,
                        "drained": drained,
                        "highest": highest,
                        "lowest": lowest
                    })
            except Exception:
                pass
            
            current += timedelta(days=1)
        
        return {"body_battery": bb_data, "start": start_date, "end": end_date}
    
    except Exception as e:
        return {"error": str(e)}


def fetch_heart_rate(client, days=7, start=None, end=None):
    """Fetch heart rate data."""
    start_date, end_date = get_date_range(days, start, end)
    
    try:
        hr_data = []
        current = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            try:
                data = client.get_heart_rates(date_str)
                if data:
                    hr_data.append({
                        "date": date_str,
                        "resting_hr": data.get("restingHeartRate"),
                        "max_hr": data.get("maxHeartRate"),
                        "min_hr": data.get("minHeartRate")
                    })
            except Exception:
                pass
            
            current += timedelta(days=1)
        
        return {"heart_rate": hr_data, "start": start_date, "end": end_date}
    
    except Exception as e:
        return {"error": str(e)}


def fetch_activities(client, days=7, start=None, end=None):
    """Fetch activities/workouts."""
    start_date, end_date = get_date_range(days, start, end)
    
    try:
        # Garmin API uses offset-based pagination
        activities = client.get_activities_by_date(start_date, end_date, activitytype="")
        
        activity_list = []
        for activity in activities:
            activity_list.append({
                "activity_id": activity.get("activityId"),
                "date": activity.get("startTimeLocal", "").split(" ")[0],
                "activity_type": activity.get("activityType", {}).get("typeKey"),
                "activity_name": activity.get("activityName"),
                "duration_seconds": activity.get("duration"),
                "distance_meters": activity.get("distance"),
                "calories": activity.get("calories"),
                "avg_hr": activity.get("averageHR"),
                "max_hr": activity.get("maxHR"),
                "elevation_gain": activity.get("elevationGain"),
                "avg_speed": activity.get("averageSpeed")
            })
        
        return {"activities": activity_list, "start": start_date, "end": end_date, "count": len(activity_list)}
    
    except Exception as e:
        return {"error": str(e)}


def fetch_activity_splits(client, activity_id):
    """Fetch lap/split data for a specific activity (per-lap HR, speed, distance, etc.)."""
    try:
        splits = client.get_activity_splits(activity_id)
        lap_dtos = splits.get("lapDTOs", [])
        
        lap_list = []
        for lap in lap_dtos:
            lap_list.append({
                "lap_index": lap.get("lapIndex"),
                "start_time_gmt": lap.get("startTimeGMT"),
                "distance_meters": lap.get("distance"),
                "duration_seconds": lap.get("duration"),
                "moving_duration": lap.get("movingDuration"),
                "average_speed": lap.get("averageSpeed"),
                "average_moving_speed": lap.get("averageMovingSpeed"),
                "max_speed": lap.get("maxSpeed"),
                "avg_hr": lap.get("averageHR"),
                "max_hr": lap.get("maxHR"),
                "calories": lap.get("calories"),
                "elevation_gain": lap.get("elevationGain"),
                "elevation_loss": lap.get("elevationLoss"),
                "max_elevation": lap.get("maxElevation"),
                "min_elevation": lap.get("minElevation"),
                "average_run_cadence": lap.get("averageRunCadence"),
                "max_run_cadence": lap.get("maxRunCadence"),
                "average_power": lap.get("averagePower"),
                "max_power": lap.get("maxPower"),
                "normalized_power": lap.get("normalizedPower"),
                "intensity_type": lap.get("intensityType"),
            })
        
        return {"activity_id": activity_id, "laps": lap_list, "lap_count": len(lap_list)}
    
    except Exception as e:
        return {"error": str(e), "activity_id": activity_id}


def fetch_activity_detail(client, activity_id, metrics=None, sample_interval=1):
    """Fetch per-second time-series data for a specific activity.
    
    Args:
        client: Garmin client instance
        activity_id: Activity ID
        metrics: Comma-separated list of metric keys to include (default: all).
                 Common keys: directHeartRate, directSpeed, sumDistance, directElevation,
                 directPower, directRunCadence, directTimestamp
        sample_interval: Output every N-th data point (default: 1 = every second).
                         Use 10 for every 10 seconds, 30 for every 30 seconds, etc.
    """
    try:
        details = client.get_activity_details(activity_id)
        
        # Build metric key -> index mapping
        metric_descriptors = details.get("metricDescriptors", [])
        key_to_idx = {}
        for i, md in enumerate(metric_descriptors):
            key_to_idx[md.get("key")] = i
        
        detail_data = details.get("activityDetailMetrics", [])
        
        # Determine which metrics to extract
        if metrics:
            requested_keys = [k.strip() for k in metrics.split(",")]
        else:
            requested_keys = list(key_to_idx.keys())
        
        # Build index mapping for requested keys only
        selected = [(k, key_to_idx[k]) for k in requested_keys if k in key_to_idx]
        
        # Extract time-series data
        time_series = []
        for i, dp in enumerate(detail_data):
            if i % sample_interval != 0:
                continue
            m = dp.get("metrics", [])
            point = {}
            for key, idx in selected:
                point[key] = m[idx] if idx < len(m) else None
            time_series.append(point)
        
        return {
            "activity_id": activity_id,
            "total_data_points": len(detail_data),
            "sample_interval": sample_interval,
            "sampled_points": len(time_series),
            "available_metrics": list(key_to_idx.keys()),
            "selected_metrics": [k for k, _ in selected],
            "time_series": time_series
        }
    
    except Exception as e:
        return {"error": str(e), "activity_id": activity_id}


def fetch_stress(client, days=7, start=None, end=None):
    """Fetch stress levels."""
    start_date, end_date = get_date_range(days, start, end)
    
    try:
        stress_data = []
        current = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            try:
                data = client.get_stress_data(date_str)
                if data:
                    stress_data.append({
                        "date": date_str,
                        "avg_stress": data.get("avgStressLevel"),
                        "max_stress": data.get("maxStressLevel"),
                        "rest_stress": data.get("restStressLevel"),
                        "activity_stress": data.get("activityStressLevel"),
                        "low_stress_duration": data.get("lowStressDuration"),
                        "medium_stress_duration": data.get("mediumStressDuration"),
                        "high_stress_duration": data.get("highStressDuration")
                    })
            except Exception:
                pass
            
            current += timedelta(days=1)
        
        return {"stress": stress_data, "start": start_date, "end": end_date}
    
    except Exception as e:
        return {"error": str(e)}


def fetch_summary(client, days=7, start=None, end=None):
    """Fetch combined summary with key metrics."""
    start_date, end_date = get_date_range(days, start, end)
    
    try:
        # Fetch multiple data types
        sleep = fetch_sleep(client, days, start, end).get("sleep", [])
        hrv = fetch_hrv(client, days, start, end).get("hrv", [])
        bb = fetch_body_battery(client, days, start, end).get("body_battery", [])
        hr = fetch_heart_rate(client, days, start, end).get("heart_rate", [])
        activities = fetch_activities(client, days, start, end).get("activities", [])

        # VO2max (live value from Garmin Connect)
        vo2max = None
        try:
            mm = client.get_max_metrics(end_date)
            if mm and isinstance(mm, list) and mm:
                vo2max = mm[0].get("generic", {}).get("vo2MaxPreciseValue")
        except Exception:
            pass

        # Calculate averages (handle None values)
        sleep_times = [s.get("sleep_time_seconds") for s in sleep if s.get("sleep_time_seconds")]
        avg_sleep_hours = (sum(sleep_times) / len(sleep_times) / 3600) if sleep_times else 0
        
        sleep_scores = [s.get("sleep_score") for s in sleep if s.get("sleep_score") is not None]
        avg_sleep_score = (sum(sleep_scores) / len(sleep_scores)) if sleep_scores else 0
        
        hrv_values = [h.get("last_night_avg") for h in hrv if h.get("last_night_avg") is not None]
        avg_hrv = (sum(hrv_values) / len(hrv_values)) if hrv_values else 0
        
        rhr_values = [h.get("resting_hr") for h in hr if h.get("resting_hr") is not None]
        avg_rhr = (sum(rhr_values) / len(rhr_values)) if rhr_values else 0
        
        bb_charged_values = [b.get("charged") for b in bb if b.get("charged") is not None]
        avg_bb_charged = (sum(bb_charged_values) / len(bb_charged_values)) if bb_charged_values else 0
        
        return {
            "summary": {
                "period": f"{start_date} to {end_date}",
                "days": days,
                "avg_sleep_hours": round(avg_sleep_hours, 1),
                "avg_sleep_score": round(avg_sleep_score, 1),
                "avg_hrv_ms": round(avg_hrv, 1),
                "avg_resting_hr": round(avg_rhr, 1),
                "avg_body_battery_charged": round(avg_bb_charged, 1),
                "total_activities": len(activities),
                "total_calories": sum(a.get("calories", 0) for a in activities if a.get("calories"))
            },
            "sleep": sleep,
            "hrv": hrv,
            "body_battery": bb,
            "heart_rate": hr,
            "activities": activities,
            "vo2max": vo2max
        }
    
    except Exception as e:
        return {"error": str(e)}


def fetch_profile(client):
    """Fetch user profile."""
    try:
        profile = client.get_full_name()
        stats = client.get_user_summary(datetime.now().strftime("%Y-%m-%d"))
        
        return {
            "profile": {
                "name": profile,
                "display_name": stats.get("displayName"),
                "email": stats.get("email")
            }
        }
    
    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Fetch Garmin health data")
    parser.add_argument("metric", choices=[
        "sleep", "hrv", "body_battery", "heart_rate", "activities",
        "stress", "summary", "profile", "activity_splits", "activity_detail"
    ], help="Type of data to fetch")
    parser.add_argument("--days", type=int, default=7, help="Number of days to fetch (default: 7)")
    parser.add_argument("--start", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", help="End date (YYYY-MM-DD)")
    parser.add_argument("--activity-id", type=int, help="Activity ID (required for activity_splits/activity_detail)")
    parser.add_argument("--metrics", help="Comma-separated metric keys for activity_detail (default: all). "
                       "Common: directHeartRate,directSpeed,sumDistance,directElevation,directPower,directRunCadence")
    parser.add_argument("--sample-interval", type=int, default=1,
                       help="Sample every N-th data point for activity_detail (default: 1 = every second)")
    
    args = parser.parse_args()
    
    # Get authenticated client
    client = get_client()
    if not client:
        print('{"error": "Not authenticated. Run: python3 scripts/garmin_auth.py login --email YOUR_EMAIL --password YOUR_PASSWORD"}')
        sys.exit(1)
    
    # Fetch requested data
    if args.metric == "sleep":
        result = fetch_sleep(client, args.days, args.start, args.end)
    elif args.metric == "hrv":
        result = fetch_hrv(client, args.days, args.start, args.end)
    elif args.metric == "body_battery":
        result = fetch_body_battery(client, args.days, args.start, args.end)
    elif args.metric == "heart_rate":
        result = fetch_heart_rate(client, args.days, args.start, args.end)
    elif args.metric == "activities":
        result = fetch_activities(client, args.days, args.start, args.end)
    elif args.metric == "stress":
        result = fetch_stress(client, args.days, args.start, args.end)
    elif args.metric == "summary":
        result = fetch_summary(client, args.days, args.start, args.end)
    elif args.metric == "profile":
        result = fetch_profile(client)
    elif args.metric == "activity_splits":
        if not args.activity_id:
            print('{"error": "--activity-id is required for activity_splits. Use activities to find IDs."}')
            sys.exit(1)
        result = fetch_activity_splits(client, args.activity_id)
    elif args.metric == "activity_detail":
        if not args.activity_id:
            print('{"error": "--activity-id is required for activity_detail. Use activities to find IDs."}')
            sys.exit(1)
        result = fetch_activity_detail(client, args.activity_id, args.metrics, args.sample_interval)
    
    # Output JSON
    print(json.dumps(result, indent=2))

    # An error dict is a failure, not data. Exit non-zero so a caller (agent or
    # shell) can tell "no data / auth failed" apart from a successful empty result.
    if isinstance(result, dict) and result.get("error"):
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
