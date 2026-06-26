#!/usr/bin/env python3
"""
Rice phenotype prediction CLI.
Predicts 10 agronomic traits using genotype (VAE) and/or environmental data.
base_dir is auto-detected from script location (one level up from scripts/).

Usage examples:
  python predict.py --lat 30.5 --lon 114.3 --sample sample1
  python predict.py --lat 25.0 --lon 102.7 --sample sample1 --mode gene
  python predict.py --lat 30.5 --lon 114.3 --sample sample1 --stress high_temp
  python predict.py --lat 30.5 --lon 114.3 --genotype_file my_vae.csv
  python predict.py --lat 30.5 --lon 114.3 --sample sample1 --device cpu
"""
import argparse
import json
import os
import sys
import warnings

import numpy as np
import pandas as pd
import torch

warnings.filterwarnings("ignore")

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_BASE_DIR = os.path.dirname(_SCRIPT_DIR)
sys.path.insert(0, _SCRIPT_DIR)

from model_def import GeneMMOE, EnvMMOE
from grid_manager import find_nearest_location
from env_data_fetcher import get_env_data
from env_processor import process_env_data
from stress_simulator import apply_stress, STRESS_TYPES

LABEL_COLS = ["HD", "PH", "PL", "TN", "GP", "SSR", "TGW", "GL", "GW", "Y"]
TRAIT_INFO = {
    "HD":  {"name": "抽穗期",     "name_en": "Heading Date",         "unit": "days"},
    "PH":  {"name": "株高",       "name_en": "Plant Height",         "unit": "cm"},
    "PL":  {"name": "穗长",       "name_en": "Panicle Length",       "unit": "cm"},
    "TN":  {"name": "分蘖数",     "name_en": "Tiller Number",        "unit": "count"},
    "GP":  {"name": "每穗粒数",   "name_en": "Grains Per Panicle",   "unit": "count"},
    "SSR": {"name": "结实率",     "name_en": "Seed Setting Rate",    "unit": "%"},
    "TGW": {"name": "千粒重",     "name_en": "Thousand Grain Weight", "unit": "g"},
    "GL":  {"name": "粒长",       "name_en": "Grain Length",         "unit": "mm"},
    "GW":  {"name": "粒宽",       "name_en": "Grain Width",          "unit": "mm"},
    "Y":   {"name": "产量",       "name_en": "Yield",                "unit": "kg/ha"},
}

ENV_TRAIT_CODES = ["hd", "ph", "gl", "gw", "ssr", "pl", "gp", "tn", "tgw", "y"]


def load_genotype(base_dir, sample_id=None, genotype_file=None):
    """Load genotype features. Returns (DataFrame with 1024 cols, list of sample IDs)."""
    if genotype_file:
        df = pd.read_csv(genotype_file, index_col=0)
        return df, list(df.index.astype(str))

    vae_path = os.path.join(base_dir, "data", "vae_features.csv")
    all_data = pd.read_csv(vae_path, index_col=0)

    if sample_id:
        samples = [s.strip() for s in sample_id.split(",")]
        matched = all_data.loc[all_data.index.isin(samples)]
        if matched.empty:
            all_ids = list(all_data.index[:10])
            raise ValueError(
                f"Sample(s) {samples} not found. Available (first 10): {all_ids}"
            )
        return matched, list(matched.index.astype(str))

    return all_data, list(all_data.index.astype(str))


def predict_gene(base_dir, genotype_df, location_code, device):
    """
    Genotype-only prediction: 1 location model -> 10 traits.
    Returns dict {trait: value} for each sample.
    """
    model_path = os.path.join(base_dir, "data", "models_gene", f"{location_code}.pt")
    if not os.path.exists(model_path):
        return None

    ckpt = torch.load(model_path, map_location=device, weights_only=False)
    input_dim = len(genotype_df.columns)
    model = GeneMMOE(input_dim=input_dim, task_num=len(LABEL_COLS)).to(device)
    model.load_state_dict(ckpt["model_state"])
    model.eval()

    x_scaler = ckpt["x_scaler"]
    y_scalers = ckpt["y_scalers"]

    X = x_scaler.transform(genotype_df).astype(np.float32)
    X = np.nan_to_num(X)
    X_tensor = torch.tensor(X, dtype=torch.float32).to(device)

    with torch.no_grad():
        outs = model(X_tensor)
        preds = torch.stack(outs, dim=1).cpu().numpy()

    for t in range(len(LABEL_COLS)):
        preds[:, t:t+1] = y_scalers[t].inverse_transform(preds[:, t:t+1])

    results = {}
    for i in range(preds.shape[0]):
        sample_result = {}
        for t, label in enumerate(LABEL_COLS):
            sample_result[label] = round(float(preds[i, t]), 3)
        results[genotype_df.index[i]] = sample_result
    return results


def predict_env(base_dir, genotype_df, env_features_normalized, device, traits=None):
    """
    Environment+genotype prediction: 10 trait-specific models.
    Each model predicts 1 trait for all samples.
    """
    if traits is None:
        traits = ENV_TRAIT_CODES

    n_samples = len(genotype_df)
    env_repeated = pd.concat([env_features_normalized] * n_samples, ignore_index=True)
    pre_data = pd.concat([
        genotype_df.reset_index(drop=True),
        env_repeated.reset_index(drop=True)
    ], axis=1)

    trait_to_label = {
        "hd": "HD", "ph": "PH", "gl": "GL", "gw": "GW", "ssr": "SSR",
        "pl": "PL", "gp": "GP", "tn": "TN", "tgw": "TGW", "y": "Y"
    }

    all_preds = {}
    input_dim = pre_data.shape[1]

    for trait_code in traits:
        model_path = os.path.join(base_dir, "data", "models_env", f"{trait_code}.pt")
        if not os.path.exists(model_path):
            continue

        ckpt = torch.load(model_path, map_location=device, weights_only=False)
        model = EnvMMOE(input_dim=input_dim, task_num=1).to(device)
        model.load_state_dict(ckpt["model_state"])
        model.eval()

        x_scaler = ckpt["x_scaler"]
        y_scalers = ckpt["y_scalers"]

        X = x_scaler.transform(pre_data).astype(np.float32)
        X = np.nan_to_num(X)
        X_tensor = torch.tensor(X, dtype=torch.float32).to(device)

        with torch.no_grad():
            outs = model(X_tensor)
            preds = outs[0].cpu().numpy().reshape(-1, 1)

        preds_inv = y_scalers[0].inverse_transform(preds).ravel()
        label = trait_to_label[trait_code]
        all_preds[label] = preds_inv

    results = {}
    for i, idx in enumerate(genotype_df.index):
        sample_result = {}
        for label, vals in all_preds.items():
            sample_result[label] = round(float(vals[i]), 3)
        results[str(idx)] = sample_result
    return results


def main():
    parser = argparse.ArgumentParser(description="Rice phenotype prediction")
    parser.add_argument("--base_dir", default=None,
                        help="Path to rice_prediction directory (auto-detected if omitted)")
    parser.add_argument("--lat", type=float, required=True, help="Latitude")
    parser.add_argument("--lon", type=float, required=True, help="Longitude")
    parser.add_argument("--sample", type=str, default=None,
                        help="Sample ID(s) from built-in data, comma-separated")
    parser.add_argument("--genotype_file", type=str, default=None,
                        help="Path to custom VAE-encoded genotype CSV (1024 dims, index=sample_id)")
    parser.add_argument("--mode", choices=["gene", "env", "full"], default="full",
                        help="Prediction mode: gene-only, env-only, or full (both)")
    parser.add_argument("--trait", type=str, default="all",
                        help="Trait(s) to predict: 'all' or comma-separated codes (HD,PH,...)")
    parser.add_argument("--stress", type=str, default=None,
                        help="Stress type: high_temp, low_temp, drought, flood, low_light")
    parser.add_argument("--stress_delta", type=float, default=None,
                        help="Temperature stress delta (overrides default)")
    parser.add_argument("--year", type=int, default=2024, help="Year for environmental data")
    parser.add_argument("--device", type=str, default="auto",
                        help="Device: 'auto' (cuda:0 if available, else cpu), 'cpu', or 'cuda:0'")
    parser.add_argument("--output", choices=["json", "table"], default="json")
    args = parser.parse_args()

    if args.base_dir is None:
        args.base_dir = _DEFAULT_BASE_DIR

    if args.device == "auto":
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(args.device)

    genotype_df, sample_ids = load_genotype(
        args.base_dir, sample_id=args.sample, genotype_file=args.genotype_file
    )

    loc, dist_km = find_nearest_location(args.lat, args.lon, args.base_dir)

    requested_traits = None
    if args.trait != "all":
        requested_traits = [t.strip().lower() for t in args.trait.split(",")]

    result = {
        "location": {
            "input_lat": args.lat, "input_lon": args.lon,
            "nearest_station": loc["name"], "station_code": loc["code"],
            "station_lat": loc["lat"], "station_lon": loc["lon"],
            "distance_km": dist_km
        },
        "samples": sample_ids,
        "device": str(device),
    }

    # --- Genotype-only prediction ---
    if args.mode in ("gene", "full"):
        gene_results = predict_gene(args.base_dir, genotype_df, loc["code"], device)
        if gene_results:
            if requested_traits:
                trait_upper = [t.upper() for t in requested_traits]
                gene_results = {
                    sid: {k: v for k, v in preds.items() if k in trait_upper}
                    for sid, preds in gene_results.items()
                }
            result["genotype_prediction"] = gene_results

    # --- Environment prediction ---
    if args.mode in ("env", "full"):
        history_path = os.path.join(args.base_dir, "data", "season_history.csv")
        daily_df = get_env_data(
            args.base_dir, loc["lat"], loc["lon"],
            loc["season_start_doy"], loc["season_end_doy"],
            year=args.year, nearest_code=loc["code"]
        )

        env_norm = process_env_data(daily_df, args.lat, history_path)

        env_traits = requested_traits if requested_traits else ENV_TRAIT_CODES
        env_results = predict_env(args.base_dir, genotype_df, env_norm, device, env_traits)
        result["environment_prediction"] = env_results

        # --- Stress prediction ---
        if args.stress:
            stress_params = None
            if args.stress_delta is not None and args.stress in ("high_temp", "low_temp"):
                sign = 1 if args.stress == "high_temp" else -1
                stress_params = {
                    "delta_tmax": sign * abs(args.stress_delta),
                    "delta_tmin": sign * abs(args.stress_delta) * 0.67
                }

            stressed_df = apply_stress(daily_df, args.stress, stress_params)
            env_norm_stressed = process_env_data(stressed_df, args.lat, history_path)
            stress_results = predict_env(
                args.base_dir, genotype_df, env_norm_stressed, device, env_traits
            )
            result["stress_prediction"] = {
                "stress_type": args.stress,
                "stress_description": STRESS_TYPES[args.stress],
                "predictions": stress_results,
            }

    # --- Add trait metadata ---
    result["trait_info"] = {
        k: v for k, v in TRAIT_INFO.items()
        if not requested_traits or k.lower() in (requested_traits or []) or k in [t.upper() for t in (requested_traits or [])]
    }

    if args.output == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        _print_table(result)


def _print_table(result):
    """Print results as a readable table."""
    print(f"\n{'='*60}")
    loc = result["location"]
    print(f"Location: {loc['nearest_station']} ({loc['station_code']})")
    print(f"  Input: ({loc['input_lat']}, {loc['input_lon']})")
    print(f"  Station: ({loc['station_lat']}, {loc['station_lon']}), {loc['distance_km']} km away")
    print(f"Samples: {', '.join(result['samples'][:5])}"
          + (f" ... +{len(result['samples'])-5} more" if len(result['samples']) > 5 else ""))

    for pred_type in ["genotype_prediction", "environment_prediction"]:
        if pred_type not in result:
            continue
        label = "Genotype-only" if "genotype" in pred_type else "Genotype+Environment"
        print(f"\n--- {label} ---")
        preds = result[pred_type]
        first_sample = list(preds.keys())[0]
        traits = list(preds[first_sample].keys())
        header = f"{'Sample':<12}" + "".join(f"{t:>10}" for t in traits)
        print(header)
        print("-" * len(header))
        for sid in list(preds.keys())[:10]:
            row = f"{sid:<12}" + "".join(f"{preds[sid][t]:>10.2f}" for t in traits)
            print(row)

    if "stress_prediction" in result:
        sp = result["stress_prediction"]
        print(f"\n--- Stress: {sp['stress_description']} ---")
        preds = sp["predictions"]
        first_sample = list(preds.keys())[0]
        traits = list(preds[first_sample].keys())
        header = f"{'Sample':<12}" + "".join(f"{t:>10}" for t in traits)
        print(header)
        print("-" * len(header))
        for sid in list(preds.keys())[:10]:
            row = f"{sid:<12}" + "".join(f"{preds[sid][t]:>10.2f}" for t in traits)
            print(row)
    print(f"\n{'='*60}")


if __name__ == "__main__":
    main()
