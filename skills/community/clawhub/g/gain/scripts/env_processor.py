"""
Environmental feature engineering pipeline.
Converts daily weather data into 53-dim season-aggregated features,
then normalizes using historical location data.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

TBASE = 10.0

AGG_PLAN = {
    "Tmax":     ["mean", "max", "min", "std"],
    "Tmin":     ["mean", "max", "min", "std"],
    "DTR":      ["mean", "max", "std"],
    "TSR":      ["mean"],
    "MMR":      ["mean"],
    "GDD":      ["sum", "mean", "max"],
    "dGDD":     ["sum", "mean"],
    "RH":       ["mean", "min", "max", "std"],
    "PR":       ["sum", "mean", "max"],
    "PRDTR":    ["mean"],
    "DL_hours": ["mean", "max", "min"],
    "APAR":     ["sum", "mean"],
    "UVA":      ["sum", "mean"],
    "UVB":      ["sum", "mean"],
    "PTT":      ["sum", "mean"],
    "dPTT":     ["sum", "mean"],
    "PTR":      ["mean"],
    "PTD1":     ["sum", "mean"],
    "PTD2":     ["mean"],
    "PS_kPa":   ["mean"],
    "WS2M_mps": ["mean", "max"],
    "WD":       ["mean"],
    "SW":       ["mean", "min", "max"],
    "SM":       ["mean", "min", "max"],
}


def compute_derived_features(df, latitude):
    """Compute all derived features from raw daily weather data."""
    df = df.copy()
    df.replace(-999, np.nan, inplace=True)

    phi = np.radians(latitude)
    df["declination"] = np.radians(23.45) * np.sin(2 * np.pi * (df["DOY"] - 81) / 365)
    cos_arg = -np.tan(phi) * np.tan(df["declination"])
    cos_arg = cos_arg.clip(-1, 1)
    df["omega_s"] = np.arccos(cos_arg)
    df["DL_hours"] = 24 / np.pi * df["omega_s"]

    df["Tmax"] = df["T2M_MAX"]
    df["Tmin"] = df["T2M_MIN"]
    df["RH"]   = df["RH2M"]
    df["PR"]   = df["PRECTOTCORR"]
    df["PS_kPa"]   = df["PS"]
    df["WS2M_mps"] = df["WS2M"]
    df["WD"]   = df["WD2M"]
    df["SW"]   = df["GWETROOT"]
    df["SM"]   = df["GWETPROF"]
    df["APAR"] = df["ALLSKY_SFC_PAR_TOT"]
    df["UVA"]  = df["ALLSKY_SFC_UVA"]
    df["UVB"]  = df["ALLSKY_SFC_UVB"]

    df["DTR"]  = df["Tmax"] - df["Tmin"]
    df["TSR"]  = df["Tmax"] ** 2 - df["Tmin"] ** 2
    df["MMR"]  = df["Tmin"] / df["Tmax"]
    avgT = (df["Tmax"] + df["Tmin"]) / 2.0
    df["GDD"]  = (avgT - TBASE).clip(lower=0)
    df["dGDD"] = df["GDD"].diff().abs()

    df["PTT"]  = df["GDD"] * df["DL_hours"]
    df["dPTT"] = df["PTT"].diff().abs()
    df["PTR"]  = df["GDD"] / df["DL_hours"].replace(0, np.nan)
    df["PTD1"] = df["DTR"] * df["DL_hours"]
    df["PTD2"] = df["DTR"] / df["DL_hours"].replace(0, np.nan)
    df["PRDTR"] = df["PR"] / df["DTR"].replace(0, np.nan)

    for c in ["MMR", "PTR", "PTD2", "PRDTR"]:
        df.loc[~np.isfinite(df[c]), c] = np.nan

    return df


def aggregate_season(df_derived):
    """Aggregate daily derived features into 53-dim season vector."""
    out = {}
    for col, funcs in AGG_PLAN.items():
        if col not in df_derived.columns:
            continue
        s = df_derived[col]
        for fn in funcs:
            if fn == "sum":    val = s.sum(min_count=1)
            elif fn == "mean": val = s.mean()
            elif fn == "max":  val = s.max()
            elif fn == "min":  val = s.min()
            elif fn == "std":  val = s.std(ddof=0)
            else: continue
            out[f"SEASON_{col}_{fn}"] = val
    return pd.DataFrame([out])


def normalize_with_history(season_df, history_csv_path):
    """
    Normalize season features by fitting StandardScaler on the new location's
    data combined with 7 historical locations (same approach as training).
    Returns the normalized 53-dim feature vector for the new location.
    """
    history = pd.read_csv(history_csv_path)
    season_df_labeled = season_df.copy()
    season_df_labeled.insert(0, "label", "pre")

    combined = pd.concat([season_df_labeled, history], axis=0, ignore_index=True)
    col_names = list(season_df.columns)

    scaler = StandardScaler()
    scaled = scaler.fit_transform(combined.iloc[:, 1:])
    scaled_df = pd.DataFrame(scaled, columns=col_names)

    return scaled_df.iloc[[0]]


def process_env_data(daily_df, latitude, history_csv_path):
    """
    Full pipeline: daily raw data -> derived features -> season aggregation -> normalization.
    Returns normalized 53-dim season feature vector as DataFrame.
    """
    derived = compute_derived_features(daily_df, latitude)
    keep_cols = [c for c in derived.columns if c not in ["YEAR", "DOY", "DATE",
                 "T2M_MAX", "T2M_MIN", "RH2M", "PRECTOTCORR", "PS", "WS2M",
                 "WD2M", "GWETROOT", "GWETPROF", "ALLSKY_SFC_PAR_TOT",
                 "ALLSKY_SFC_UVA", "ALLSKY_SFC_UVB", "declination", "omega_s"]]
    derived_clean = derived[keep_cols]
    season = aggregate_season(derived_clean)
    normalized = normalize_with_history(season, history_csv_path)
    return normalized
