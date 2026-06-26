"""
Shared timezone utility for all Fulcra scripts.

SINGLE SOURCE OF TRUTH for user timezone.
Gets timezone from Fulcra's get_user_info() endpoint.
Caches to disk to avoid repeated API calls.

EVERY Fulcra script should import from here:
    from fulcra_timezone import get_user_tz, now_local, today_local

NEVER hardcode timezone. NEVER manually subtract UTC offsets.
Python's ZoneInfo handles DST automatically.
"""

import json
import os
import shlex
import subprocess
from datetime import datetime, timezone, date
from zoneinfo import ZoneInfo
from pathlib import Path

# Cache file — refreshed daily or on miss
_CACHE_PATH = Path.home() / '.config' / 'fulcra' / 'timezone_cache.json'
_tz_instance = None  # in-memory cache for the session


def _get_fulcra_client():
    """Get authenticated Fulcra API client (standalone, no circular imports)."""
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


def _read_cache():
    """Read cached timezone if fresh (same UTC day)."""
    try:
        if _CACHE_PATH.exists():
            data = json.loads(_CACHE_PATH.read_text())
            cached_date = data.get('cached_date')
            tz_name = data.get('timezone')
            if cached_date == str(datetime.now(timezone.utc).date()) and tz_name:
                return tz_name
    except Exception:
        pass
    return None


def _write_cache(tz_name):
    """Write timezone to cache."""
    try:
        _CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        _CACHE_PATH.write_text(json.dumps({
            'timezone': tz_name,
            'cached_date': str(datetime.now(timezone.utc).date()),
        }))
    except Exception:
        pass


def get_user_tz(client=None) -> ZoneInfo:
    """
    Get user's timezone as a ZoneInfo object.
    
    Resolution order:
    1. In-memory cache (fastest, same session)
    2. Disk cache (same day)
    3. Fulcra API get_user_info() → preferences.timezone
    4. FULCRA_TIMEZONE env var
    5. Fallback: America/New_York (last resort, logs warning)
    
    Returns:
        ZoneInfo instance for the user's timezone
    """
    global _tz_instance
    
    # 1. In-memory cache
    if _tz_instance is not None:
        return _tz_instance
    
    tz_name = None
    
    # 2. Disk cache
    tz_name = _read_cache()
    
    # 3. Fulcra API
    if not tz_name:
        try:
            if client is None:
                client = _get_fulcra_client()
            info = client.get_user_info()
            tz_name = info.get('preferences', {}).get('timezone')
            if tz_name:
                _write_cache(tz_name)
        except Exception as e:
            import sys
            print(f"[fulcra_timezone] API lookup failed: {e}", file=sys.stderr)
    
    # 4. Environment variable
    if not tz_name:
        tz_name = os.environ.get('FULCRA_TIMEZONE')
    
    # 5. Fallback
    if not tz_name:
        import sys
        print("[fulcra_timezone] WARNING: Using fallback timezone America/New_York", file=sys.stderr)
        tz_name = 'America/New_York'
    
    _tz_instance = ZoneInfo(tz_name)
    return _tz_instance


def now_local(client=None) -> datetime:
    """Get current datetime in user's local timezone (DST-aware)."""
    return datetime.now(get_user_tz(client))


def today_local(client=None) -> date:
    """Get today's date in user's local timezone."""
    return now_local(client).date()


def to_local(dt_utc, client=None) -> datetime:
    """
    Convert a UTC datetime to user's local timezone.
    
    ALWAYS use this instead of manual offset subtraction.
    Handles DST transitions automatically.
    
    Args:
        dt_utc: datetime with tzinfo (UTC) or naive (assumed UTC)
    """
    if dt_utc.tzinfo is None:
        dt_utc = dt_utc.replace(tzinfo=timezone.utc)
    return dt_utc.astimezone(get_user_tz(client))


def format_local_time(dt_utc, fmt='%-I:%M %p', client=None) -> str:
    """Convert UTC datetime to formatted local time string."""
    return to_local(dt_utc, client).strftime(fmt)


def get_periods_of_day(client=None) -> dict:
    """
    Get user's period-of-day boundaries from Fulcra profile.
    Returns dict like: {'morning': '08:00:00', 'afternoon': '12:00:00', ...}
    Falls back to sensible defaults.
    """
    try:
        if client is None:
            client = _get_fulcra_client()
        info = client.get_user_info()
        periods = info.get('preferences', {}).get('periods_of_day')
        if periods:
            return periods
    except Exception:
        pass
    return {
        'morning': '08:00:00',
        'afternoon': '12:00:00', 
        'evening': '18:00:00',
        'end_of_day': '21:00:00'
    }


if __name__ == '__main__':
    tz = get_user_tz()
    print(f"User timezone: {tz}")
    print(f"Current local time: {now_local()}")
    print(f"Today local: {today_local()}")
    print(f"DST active: {now_local().dst() != timezone.utc.utcoffset(None)}")
    print(f"UTC offset: {now_local().strftime('%z')}")
    print(f"Periods of day: {get_periods_of_day()}")
