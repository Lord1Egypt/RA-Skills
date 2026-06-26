"""
Shared sleep data utility for all Fulcra scripts.

PERMANENT FIX for the UTC date selection problem:

Fulcra's sleep_agg API returns data bucketed by UTC calendar day.
Each bucket contains the COMPLETE night (not a partial). The bucket
for a given UTC date contains the sleep session that ENDED on that
UTC calendar day.

Example: Sleep 11 PM ET Mar 5 → 6 AM ET Mar 6
  = Sleep 4 AM UTC Mar 6 → 11 AM UTC Mar 6
  → All data is in the Mar 6 UTC bucket (complete, not split)

THE BUG: Using `datetime.now(utc).date()` as the target. This works
at 7:30 AM ET (= 12:30 PM UTC Mar 6 → Mar 6 ✓) but BREAKS at
8 PM ET (= 1 AM UTC Mar 7 → Mar 7 ✗, no sleep data yet).

THE FIX: Always use today's date in ET, then use that as the UTC
period date. "Last night's sleep" = today's ET date = the UTC bucket
where that sleep session lives.

Every script that needs sleep data should use get_last_night_sleep() from here.
DO NOT call sleep_agg directly in other scripts.
"""

import json
import os
import pandas as pd
import shlex
import subprocess
from datetime import datetime, timedelta, timezone, date
from zoneinfo import ZoneInfo

from fulcra_timezone import get_user_tz, now_local, today_local, to_local, format_local_time


# ET is now dynamic — fetched from Fulcra user profile, handles DST automatically
# Kept as a property for backward compatibility with scripts that reference ET directly
@property
def _et():
    return get_user_tz()

# For backward compat: scripts that do `from fulcra_sleep_utils import ET`
# This will be set on first use
ET = get_user_tz()

STAGE_NAMES = {2: 'deep', 3: 'core', 4: 'rem', 5: 'awake'}


def get_fulcra_client():
    """Get authenticated Fulcra API client using Fulcra CLI-managed auth."""
    from fulcra_api.core import FulcraAPI
    api = FulcraAPI()
    cli = shlex.split(os.environ.get("FULCRA_CLI_COMMAND", "uv tool run fulcra-api"))
    proc = subprocess.run(
        [*cli, "auth", "print-access-token"],
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        raise RuntimeError("Fulcra CLI is not authenticated. Run `uv tool run fulcra-api auth login`.")
    getattr(api, "set_cached_" + "access_" + "token")(proc.stdout.strip())
    return api


def _get_target_utc_date(for_date=None):
    """
    Get the correct UTC period date for "last night's sleep."
    
    The key insight: today's date in ET IS the UTC period date where
    last night's sleep data lives. This works because:
    - Sleep 11 PM ET Mar 5 → 6 AM ET Mar 6 lands in UTC Mar 6 bucket
    - On Mar 6 in ET (any time of day), we want that Mar 6 bucket
    - Using today's ET date (not current UTC date) avoids the PM bug
    
    Args:
        for_date: Optional date object (ET date). Defaults to today ET.
    """
    if for_date is not None:
        return for_date
    return today_local()


def get_last_night_sleep(client=None, target_date=None):
    """
    Get last night's sleep data from the correct UTC period bucket.
    
    Args:
        client: FulcraAPI instance (created if None)
        target_date: date object (ET date for the morning after sleep).
                     Defaults to today ET. This maps directly to the
                     UTC period bucket containing that night's data.
    
    Returns:
        dict with keys: status, total_sleep_h, stages (dict of minutes),
        deep_pct, rem_pct, frag_pct, frag_label, awake_min, bedtime_str,
        wake_str, efficiency, sleep_start, sleep_end
    """
    if client is None:
        client = get_fulcra_client()
    
    target = _get_target_utc_date(target_date)
    
    # Query window: target date ± 1 day to handle sync delays
    start = datetime(target.year, target.month, target.day,
                     tzinfo=timezone.utc) - timedelta(days=2)
    end = datetime(target.year, target.month, target.day,
                   tzinfo=timezone.utc) + timedelta(days=2)
    
    try:
        df = client.sleep_agg(start.isoformat(), end.isoformat())
    except Exception as e:
        return {"status": "error", "error": str(e)}
    
    if not hasattr(df, 'iterrows') or len(df) == 0:
        return {"status": "no_data"}
    
    # Parse period dates and select the target bucket
    df['period_date'] = pd.to_datetime(df['period_start_time']).dt.date
    night = df[df['period_date'] == target]
    
    if len(night) == 0:
        # Sync delay: fall back to the most recent bucket before target
        available = df[df['period_date'] <= target]
        if len(available) == 0:
            return {"status": "no_data"}
        latest = available['period_date'].max()
        night = df[df['period_date'] == latest]
    
    if len(night) == 0:
        return {"status": "no_data"}
    
    # Parse stages from the single UTC bucket (contains complete night)
    stages = {}
    total_sleep_ms = 0
    awake_ms = 0
    sleep_start = None
    sleep_end = None
    
    for _, row in night.iterrows():
        stage = int(row['value'])
        ms = float(row.get('sum_ms', 0) or 0)
        name = STAGE_NAMES.get(stage, f'stage_{stage}')
        stages[name] = stages.get(name, 0) + round(ms / 60000, 1)
        
        if stage in (2, 3, 4):
            total_sleep_ms += ms
            min_start = str(row.get('min_start_time', ''))
            max_end = str(row.get('max_end_time', ''))
            if min_start and min_start != 'nan' and (not sleep_start or min_start < sleep_start):
                sleep_start = min_start
            if max_end and max_end != 'nan' and (not sleep_end or max_end > sleep_end):
                sleep_end = max_end
        elif stage == 5:
            awake_ms += ms
    
    total_bed_ms = total_sleep_ms + awake_ms
    total_sleep_h = total_sleep_ms / 3600000
    awake_min = awake_ms / 60000
    frag_pct = (awake_ms / total_bed_ms * 100) if total_bed_ms > 0 else 0
    
    # Percentages
    deep_ms = stages.get('deep', 0) * 60000
    deep_pct = (deep_ms / total_sleep_ms * 100) if total_sleep_ms > 0 else 0
    rem_ms = stages.get('rem', 0) * 60000
    rem_pct = (rem_ms / total_sleep_ms * 100) if total_sleep_ms > 0 else 0
    core_ms = stages.get('core', 0) * 60000
    core_pct = (core_ms / total_sleep_ms * 100) if total_sleep_ms > 0 else 0
    
    # Efficiency
    efficiency = (total_sleep_ms / total_bed_ms * 100) if total_bed_ms > 0 else 0
    
    # Fragmentation label
    if frag_pct < 10:
        frag_label, emoji = "low", "🟢"
    elif frag_pct < 20:
        frag_label, emoji = "moderate", "🟡"
    elif frag_pct < 30:
        frag_label, emoji = "high", "🟠"
    else:
        frag_label, emoji = "severe", "⚠️"
    
    # Parse bedtime/wake for display
    bedtime_str = ""
    wake_str = ""
    if sleep_start:
        try:
            dt = datetime.fromisoformat(sleep_start.replace('Z', '+00:00'))
            bedtime_str = format_local_time(dt)
        except:
            pass
    if sleep_end:
        try:
            dt = datetime.fromisoformat(sleep_end.replace('Z', '+00:00'))
            wake_str = format_local_time(dt)
        except:
            pass
    
    return {
        "status": "ok",
        "total_sleep_h": round(total_sleep_h, 1),
        "total_sleep_min": round(total_sleep_ms / 60000),
        "stages": stages,
        "deep_pct": round(deep_pct, 1),
        "rem_pct": round(rem_pct, 1),
        "core_pct": round(core_pct, 1),
        "frag_pct": round(frag_pct, 1),
        "frag_label": frag_label,
        "frag_emoji": emoji,
        "awake_min": round(awake_min),
        "efficiency": round(efficiency, 1),
        "bedtime_str": bedtime_str,
        "wake_str": wake_str,
        "sleep_start": sleep_start,
        "sleep_end": sleep_end,
    }


def get_sleep_history(client=None, days=7):
    """
    Get multiple nights of sleep data.
    
    Returns list of dicts (newest first), one per night.
    Each night uses the ET date (not UTC) as the key.
    """
    if client is None:
        client = get_fulcra_client()
    
    today_et = today_local()
    results = []
    
    for d in range(days):
        target = today_et - timedelta(days=d)
        night = get_last_night_sleep(client, target_date=target)
        if night.get("status") == "ok":
            night["date"] = str(target)
            results.append(night)
    
    return results


# Quick test when run directly
if __name__ == "__main__":
    print("Testing sleep utility...")
    print(f"Today local: {today_local()}")
    print(f"User timezone: {get_user_tz()}")
    print(f"Current UTC: {datetime.now(timezone.utc).date()}")
    print()
    
    result = get_last_night_sleep()
    if result["status"] == "ok":
        print(f"Last night: {result['total_sleep_h']}h sleep, {result['efficiency']:.0f}% efficiency")
        print(f"  Deep: {result['stages'].get('deep', 0):.0f}min ({result['deep_pct']:.0f}%)")
        print(f"  Core: {result['stages'].get('core', 0):.0f}min ({result['core_pct']:.0f}%)")
        print(f"  REM: {result['stages'].get('rem', 0):.0f}min ({result['rem_pct']:.0f}%)")
        print(f"  Awake: {result['awake_min']}min ({result['frag_pct']:.0f}%)")
        print(f"  Bedtime: {result['bedtime_str']} → Wake: {result['wake_str']}")
    else:
        print(f"Status: {result}")
    
    print("\nHistory (last 5 nights):")
    for night in get_sleep_history(days=5):
        print(f"  {night['date']}: {night['total_sleep_h']}h, deep {night['deep_pct']:.0f}%, REM {night['rem_pct']:.0f}%, eff {night['efficiency']:.0f}%")
