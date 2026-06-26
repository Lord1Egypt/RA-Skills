"""
Simulate environmental stress by modifying daily weather data.
Supports: high_temp, low_temp, drought, flood, low_light.
"""
import numpy as np
import pandas as pd


STRESS_TYPES = {
    "high_temp": "高温胁迫: 增加日最高/最低温度",
    "low_temp":  "低温胁迫: 降低日最高/最低温度",
    "drought":   "干旱胁迫: 减少降水量和土壤水分",
    "flood":     "涝害胁迫: 大幅增加降水量",
    "low_light": "寡照胁迫: 降低光合有效辐射",
}

DEFAULT_PARAMS = {
    "high_temp": {"delta_tmax": 3.0, "delta_tmin": 2.0},
    "low_temp":  {"delta_tmax": -3.0, "delta_tmin": -2.0},
    "drought":   {"precip_factor": 0.1, "soil_factor": 0.5},
    "flood":     {"precip_factor": 3.0},
    "low_light": {"par_factor": 0.4, "uv_factor": 0.5},
}


def apply_stress(daily_df, stress_type, params=None):
    """
    Apply environmental stress to daily weather data.
    Returns modified DataFrame (copy).
    """
    if stress_type not in STRESS_TYPES:
        raise ValueError(f"Unknown stress type: {stress_type}. "
                         f"Supported: {list(STRESS_TYPES.keys())}")

    df = daily_df.copy()
    p = {**DEFAULT_PARAMS[stress_type], **(params or {})}

    if stress_type == "high_temp":
        df["T2M_MAX"] = df["T2M_MAX"] + p["delta_tmax"]
        df["T2M_MIN"] = df["T2M_MIN"] + p["delta_tmin"]

    elif stress_type == "low_temp":
        df["T2M_MAX"] = df["T2M_MAX"] + p["delta_tmax"]
        df["T2M_MIN"] = df["T2M_MIN"] + p["delta_tmin"]

    elif stress_type == "drought":
        df["PRECTOTCORR"] = df["PRECTOTCORR"] * p["precip_factor"]
        df["GWETROOT"] = df["GWETROOT"] * p.get("soil_factor", 0.5)
        df["GWETPROF"] = df["GWETPROF"] * p.get("soil_factor", 0.5)

    elif stress_type == "flood":
        df["PRECTOTCORR"] = df["PRECTOTCORR"] * p["precip_factor"]
        df["GWETROOT"] = np.minimum(df["GWETROOT"] * 1.3, 1.0)
        df["GWETPROF"] = np.minimum(df["GWETPROF"] * 1.3, 1.0)

    elif stress_type == "low_light":
        df["ALLSKY_SFC_PAR_TOT"] = df["ALLSKY_SFC_PAR_TOT"] * p["par_factor"]
        df["ALLSKY_SFC_UVA"] = df["ALLSKY_SFC_UVA"] * p.get("uv_factor", 0.5)
        df["ALLSKY_SFC_UVB"] = df["ALLSKY_SFC_UVB"] * p.get("uv_factor", 0.5)

    return df
