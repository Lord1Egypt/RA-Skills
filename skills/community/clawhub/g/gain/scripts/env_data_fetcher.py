"""
Fetch daily environmental data from NASA POWER API or load from local cache.
Data format matches the rice prediction pipeline: 14 columns of daily weather.
"""
import os
import json
import time
import numpy as np
import pandas as pd

POWER_PARAMS = [
    "T2M_MAX", "T2M_MIN", "RH2M", "PRECTOTCORR", "PS",
    "WS2M", "WD2M", "GWETROOT", "GWETPROF",
    "ALLSKY_SFC_PAR_TOT", "ALLSKY_SFC_UVA", "ALLSKY_SFC_UVB"
]

CSV_COLUMNS = [
    "YEAR", "DOY", "ALLSKY_SFC_UVB", "ALLSKY_SFC_UVA", "ALLSKY_SFC_PAR_TOT",
    "RH2M", "WS2M", "PS", "GWETROOT", "GWETPROF",
    "WD2M", "PRECTOTCORR", "T2M_MAX", "T2M_MIN"
]


def _cache_path(base_dir, lat, lon, year):
    cache_dir = os.path.join(base_dir, "data", "env_cache")
    os.makedirs(cache_dir, exist_ok=True)
    return os.path.join(cache_dir, f"env_{lat:.2f}_{lon:.2f}_{year}.csv")


def fetch_from_nasa_power(lat, lon, start_doy, end_doy, year=2024):
    """Fetch daily data from NASA POWER API. Returns DataFrame."""
    try:
        import requests
    except ImportError:
        raise RuntimeError("requests library required: pip install requests")

    start_date = pd.Timestamp(year=year, month=1, day=1) + pd.Timedelta(days=start_doy - 1)
    end_date = pd.Timestamp(year=year, month=1, day=1) + pd.Timedelta(days=end_doy - 1)

    url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?parameters={','.join(POWER_PARAMS)}"
        f"&community=AG"
        f"&longitude={lon}&latitude={lat}"
        f"&start={start_date.strftime('%Y%m%d')}"
        f"&end={end_date.strftime('%Y%m%d')}"
        f"&format=JSON"
    )

    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    params = data["properties"]["parameter"]
    dates = sorted(params[POWER_PARAMS[0]].keys())

    rows = []
    for date_str in dates:
        dt = pd.Timestamp(date_str)
        row = {"YEAR": dt.year, "DOY": dt.day_of_year}
        for p in POWER_PARAMS:
            row[p] = params[p].get(date_str, np.nan)
        rows.append(row)

    df = pd.DataFrame(rows)
    df = df[CSV_COLUMNS]
    return df


def _find_any_cached_csv(base_dir):
    """Return path to any available CSV in env_cache (fallback)."""
    cache_dir = os.path.join(base_dir, "data", "env_cache")
    if os.path.isdir(cache_dir):
        for f in os.listdir(cache_dir):
            if f.endswith(".csv"):
                return os.path.join(cache_dir, f), f.replace(".csv", "")
    return None, None


def get_env_data(base_dir, lat, lon, season_start_doy, season_end_doy,
                 year=2024, nearest_code=None):
    """
    Get environmental data with cascading fallback:
    1. Exact lat/lon cache file
    2. Nearest station's built-in CSV
    3. NASA POWER API (with caching)
    4. Any available built-in CSV (last resort)
    """
    cache_file = _cache_path(base_dir, lat, lon, year)
    if os.path.exists(cache_file):
        return pd.read_csv(cache_file)

    if nearest_code:
        builtin = os.path.join(base_dir, "data", "env_cache", f"{nearest_code}.csv")
        if os.path.exists(builtin):
            return pd.read_csv(builtin)

    try:
        df = fetch_from_nasa_power(lat, lon, season_start_doy, season_end_doy, year)
        df.to_csv(cache_file, index=False)
        return df
    except Exception:
        pass

    fallback_path, fallback_name = _find_any_cached_csv(base_dir)
    if fallback_path:
        import sys
        print(f"[WARNING] No env data for ({lat}, {lon}), using fallback "
              f"station '{fallback_name}' data. For accurate results, ensure "
              f"internet access or place a CSV at {cache_file}",
              file=sys.stderr)
        return pd.read_csv(fallback_path)

    raise RuntimeError(
        f"Cannot get env data for ({lat}, {lon}). "
        f"Place a CSV file at {cache_file} or ensure internet access."
    )


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 6:
        print("Usage: python env_data_fetcher.py <base_dir> <lat> <lon> <start_doy> <end_doy> [year]")
        sys.exit(1)
    base = sys.argv[1]
    lat, lon = float(sys.argv[2]), float(sys.argv[3])
    s, e = int(sys.argv[4]), int(sys.argv[5])
    yr = int(sys.argv[6]) if len(sys.argv) > 6 else 2024
    df = get_env_data(base, lat, lon, s, e, yr)
    print(f"Loaded {len(df)} days of environmental data")
    print(df.head())
