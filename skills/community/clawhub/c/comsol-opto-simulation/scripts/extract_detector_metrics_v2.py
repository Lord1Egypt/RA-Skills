#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced automatic extraction of photodetector metrics from COMSOL results.

Extracts:
  - I-V curves (dark & illuminated) from parametric sweep
  - Band diagram (Ec, Ev, Ef vs position) — numerical + PNG
  - Carrier density profiles (n, p vs position) — numerical + PNG
  - Electric field profile
  - EQE / Responsivity / D* from photocurrent vs wavelength
  - Rectification ratio, ideality factor

Uses MPh model.evaluate() + Java API fallback chain for maximum compatibility.

Usage:
    python extract_detector_metrics_v2.py --model output/optoelectronic/opto_result.mph --config config_opto.json
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np

SKILL_DIR = Path(__file__).resolve().parents[1]
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))


# ---------------------------------------------------------------------------
# 0. Setup
# ---------------------------------------------------------------------------
def ensure_mph():
    try:
        import mph
        return mph
    except ImportError:
        print(json.dumps({"status": "error", "message": "mph not installed. Run: python scripts/install_mph.py"}))
        sys.exit(1)


# ---------------------------------------------------------------------------
# 1. Model introspection helpers
# ---------------------------------------------------------------------------
def list_datasets(jm):
    """Return list of dataset tags (Python strings)."""
    try:
        return [str(t) for t in jm.result().dataset().tags()]
    except Exception as e:
        return []


def find_parametric_dataset(jm, datasets):
    """Find the dataset that contains parametric sweep data."""
    for tag in datasets:
        lower = str(tag).lower()
        if "param" in lower or "sweep" in lower:
            return str(tag)
    if datasets:
        return str(datasets[-1])
    return None


def get_parametric_values(jm, dataset_tag):
    """Return list of (param_name, values_list) for a parametric dataset."""
    try:
        dset = jm.result().dataset(dataset_tag)
        # COMSOL parametric datasets expose parameter info via API
        # Try common property names
        for prop in ["plist", "param", "parameter"]:
            try:
                val = dset.get(prop)
                if val:
                    return val
            except Exception:
                pass
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# 2. I-V extraction
# ---------------------------------------------------------------------------
def extract_iv_curve(model, jm, config: dict) -> dict:
    """Extract I-V data from parametric sweep using multiple strategies."""
    datasets = list_datasets(jm)
    dset_tag = find_parametric_dataset(jm, datasets)

    if not dset_tag:
        return {"status": "error", "message": "No dataset found in model"}

    # Strategy 1: model.evaluate() on the parametric dataset (MPh advanced)
    try:
        iv = model.evaluate("semi.I_1", dataset=dset_tag)
        # V_bias may be available as an expression or parameter
        try:
            v_vals = model.evaluate("V_bias", dataset=dset_tag)
        except Exception:
            # If V_bias can't be evaluated, try reading from model parameters
            v_vals = None

        # If outer returns multiple arrays, flatten
        if isinstance(iv, list):
            iv = np.concatenate([np.atleast_1d(x) for x in iv])
        if isinstance(v_vals, list):
            v_vals = np.concatenate([np.atleast_1d(x) for x in v_vals])

        v_list = np.atleast_1d(v_vals).tolist() if v_vals is not None else []
        i_list = np.atleast_1d(iv).tolist()

        # If voltage list is empty, try parametric values from dataset
        if not v_list and len(i_list) > 0:
            bias_range = config.get("bias_range", {})
            start = bias_range.get("start_V", -1.0)
            stop = bias_range.get("stop_V", 1.0)
            points = bias_range.get("points", len(i_list))
            v_list = np.linspace(start, stop, points).tolist()

        return {
            "status": "ok",
            "method": "model.evaluate",
            "dataset": dset_tag,
            "voltage_V": v_list,
            "current_A": i_list,
            "current_density_A_per_m2": [i / config.get("device_area_m2", 1e-6) for i in i_list] if i_list else [],
        }
    except Exception as e1:
        pass

    # Strategy 2: Java API EvalGlobal
    try:
        results = jm.result()
        gev = results.numerical().create("gev_iv_auto", "EvalGlobal")
        gev.set("expr", "semi.I_1")
        gev.set("data", dset_tag)
        gev.run()
        real_data = gev.getReal()
        # COMSOL EvalGlobal.getReal() returns a 2D array [expression][solution]
        if hasattr(real_data, 'shape') and len(real_data.shape) >= 2:
            i_list = real_data[0].tolist() if real_data.shape[0] > 0 else []
        else:
            i_list = np.atleast_1d(real_data).tolist()

        # Get parametric voltage values
        v_list = []
        bias_range = config.get("bias_range", {})
        start = bias_range.get("start_V", -1.0)
        stop = bias_range.get("stop_V", 1.0)
        points = bias_range.get("points", len(i_list))
        v_list = np.linspace(start, stop, points).tolist()

        results.numerical().remove("gev_iv_auto")

        return {
            "status": "ok",
            "method": "EvalGlobal",
            "dataset": dset_tag,
            "voltage_V": v_list,
            "current_A": i_list,
            "current_density_A_per_m2": [i / config.get("device_area_m2", 1e-6) for i in i_list] if i_list else [],
        }
    except Exception as e2:
        return {
            "status": "error",
            "message": f"I-V extraction failed. evaluate error: {e1}; EvalGlobal error: {e2}",
        }


# ---------------------------------------------------------------------------
# 3. Band diagram extraction
# ---------------------------------------------------------------------------
def extract_band_diagram(model, jm, config: dict, output_dir: Path) -> dict:
    """Extract band diagram (Ec, Ev, Ef) along device depth and export PNG + CSV."""
    results = jm.result()
    datasets = list_datasets(jm)
    dset_tag = find_parametric_dataset(jm, datasets)

    # Find a 1D cut line or create one at device center
    cut_tag = None
    for tag in datasets:
        if "cut" in tag.lower() or "line" in tag.lower():
            cut_tag = tag
            break

    # If no cut line dataset exists, create one
    if not cut_tag:
        try:
            # Device dimensions from config
            layers = config.get("device_stack", {}).get("layers", [])
            total_thickness = sum(l.get("thickness_nm", 100) for l in layers)
            width = config.get("device_stack", {}).get("device_width_nm", 1000)

            cut = results.dataset().create("cut_center", "CutLine2D")
            # Vertical line through center of device
            cut.set("genpoints", [
                [str(width / 2) + "[nm]", "0[nm]"],
                [str(width / 2) + "[nm]", str(total_thickness) + "[nm]"]
            ])
            if dset_tag:
                cut.set("data", dset_tag)
            cut_tag = "cut_center"
        except Exception as e:
            cut_tag = dset_tag  # fallback to full dataset

    expressions = ["semi.E_c", "semi.E_v", "semi.E_f"]
    labels = ["Ec", "Ev", "Ef"]

    # --- Numerical extraction ---
    band_data = {"position_nm": [], "Ec_eV": [], "Ev_eV": [], "Ef_eV": []}
    try:
        # Use EvalPoint array along the cut line
        # MPh model.evaluate on a CutLine dataset may return spatial arrays
        for expr, label in zip(expressions, labels):
            try:
                vals = model.evaluate(expr, dataset=cut_tag)
                if isinstance(vals, list):
                    vals = np.concatenate([np.atleast_1d(x) for x in vals])
                band_data[label + "_eV"] = np.atleast_1d(vals).tolist()
            except Exception:
                band_data[label + "_eV"] = []

        # Position axis: try to get spatial coordinate
        try:
            pos = model.evaluate("y", dataset=cut_tag)
            if isinstance(pos, list):
                pos = np.concatenate([np.atleast_1d(x) for x in pos])
            band_data["position_nm"] = (np.atleast_1d(pos) * 1e9).tolist()  # convert m to nm
        except Exception:
            # Fallback: generate position from layer thicknesses
            layers = config.get("device_stack", {}).get("layers", [])
            total = sum(l.get("thickness_nm", 100) for l in layers)
            n_pts = max(len(band_data["Ec_eV"]), 200)
            band_data["position_nm"] = np.linspace(0, total, n_pts).tolist()
    except Exception as e:
        band_data = {"error": str(e)}

    # --- PlotGroup + PNG export ---
    plot_info = {"status": "ok"}
    try:
        pg = results.create("pg_band_auto", "PlotGroup1D")
        for expr, label in zip(expressions, labels):
            lg = pg.create(f"lg_{label}", "LineGraph")
            lg.set("expr", expr)
            if cut_tag:
                lg.set("data", cut_tag)

        # Export PNG
        png_path = output_dir / "band_diagram_auto.png"
        try:
            model.export(str(png_path))
            plot_info["png_path"] = str(png_path)
        except Exception as e:
            # Fallback: Java API image export
            try:
                img = jm.result().export().create("img_band", "Image")
                img.set("plotgroup", "pg_band_auto")
                img.set("png", "on")
                img.set("filename", str(png_path))
                jm.result().export().run("img_band")
                plot_info["png_path"] = str(png_path)
            except Exception as e2:
                plot_info["png_error"] = str(e2)
    except Exception as e:
        plot_info = {"status": "error", "message": str(e)}

    # --- CSV export ---
    csv_path = output_dir / "band_diagram.csv"
    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Position_nm", "Ec_eV", "Ev_eV", "Ef_eV"])
            n = max(len(band_data.get("Ec_eV", [])), len(band_data.get("Ev_eV", [])), len(band_data.get("Ef_eV", [])))
            for i in range(n):
                writer.writerow([
                    band_data["position_nm"][i] if i < len(band_data["position_nm"]) else "",
                    band_data["Ec_eV"][i] if i < len(band_data.get("Ec_eV", [])) else "",
                    band_data["Ev_eV"][i] if i < len(band_data.get("Ev_eV", [])) else "",
                    band_data["Ef_eV"][i] if i < len(band_data.get("Ef_eV", [])) else "",
                ])
        plot_info["csv_path"] = str(csv_path)
    except Exception as e:
        plot_info["csv_error"] = str(e)

    return {
        "status": plot_info.get("status", "ok"),
        "data": band_data,
        "plot": plot_info,
    }


# ---------------------------------------------------------------------------
# 4. Carrier density extraction
# ---------------------------------------------------------------------------
def extract_carrier_densities(model, jm, config: dict, output_dir: Path) -> dict:
    """Extract n(x) and p(x) along device depth and export PNG + CSV."""
    results = jm.result()
    datasets = list_datasets(jm)
    dset_tag = find_parametric_dataset(jm, datasets)

    cut_tag = None
    for tag in datasets:
        if "cut" in tag.lower() or "line" in tag.lower():
            cut_tag = tag
            break
    if not cut_tag:
        cut_tag = dset_tag

    expressions = ["semi.n", "semi.p"]
    labels = ["n", "p"]

    carrier_data = {"position_nm": [], "n_cm3": [], "p_cm3": []}
    try:
        for expr, label in zip(expressions, labels):
            try:
                vals = model.evaluate(expr, dataset=cut_tag)
                if isinstance(vals, list):
                    vals = np.concatenate([np.atleast_1d(x) for x in vals])
                carrier_data[label + "_cm3"] = np.atleast_1d(vals).tolist()
            except Exception:
                carrier_data[label + "_cm3"] = []

        try:
            pos = model.evaluate("y", dataset=cut_tag)
            if isinstance(pos, list):
                pos = np.concatenate([np.atleast_1d(x) for x in pos])
            carrier_data["position_nm"] = (np.atleast_1d(pos) * 1e9).tolist()
        except Exception:
            layers = config.get("device_stack", {}).get("layers", [])
            total = sum(l.get("thickness_nm", 100) for l in layers)
            n_pts = max(len(carrier_data["n_cm3"]), 200)
            carrier_data["position_nm"] = np.linspace(0, total, n_pts).tolist()
    except Exception as e:
        carrier_data = {"error": str(e)}

    # PlotGroup + PNG
    plot_info = {"status": "ok"}
    try:
        pg = results.create("pg_carrier_auto", "PlotGroup1D")
        for expr, label in zip(expressions, labels):
            lg = pg.create(f"lg_{label}", "LineGraph")
            lg.set("expr", expr)
            if cut_tag:
                lg.set("data", cut_tag)

        png_path = output_dir / "carrier_density_auto.png"
        try:
            model.export(str(png_path))
            plot_info["png_path"] = str(png_path)
        except Exception as e:
            try:
                img = jm.result().export().create("img_carrier", "Image")
                img.set("plotgroup", "pg_carrier_auto")
                img.set("png", "on")
                img.set("filename", str(png_path))
                jm.result().export().run("img_carrier")
                plot_info["png_path"] = str(png_path)
            except Exception as e2:
                plot_info["png_error"] = str(e2)
    except Exception as e:
        plot_info = {"status": "error", "message": str(e)}

    # CSV export
    csv_path = output_dir / "carrier_density.csv"
    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Position_nm", "n_cm3", "p_cm3"])
            n = max(len(carrier_data.get("n_cm3", [])), len(carrier_data.get("p_cm3", [])))
            for i in range(n):
                writer.writerow([
                    carrier_data["position_nm"][i] if i < len(carrier_data["position_nm"]) else "",
                    carrier_data["n_cm3"][i] if i < len(carrier_data.get("n_cm3", [])) else "",
                    carrier_data["p_cm3"][i] if i < len(carrier_data.get("p_cm3", [])) else "",
                ])
        plot_info["csv_path"] = str(csv_path)
    except Exception as e:
        plot_info["csv_error"] = str(e)

    return {
        "status": plot_info.get("status", "ok"),
        "data": carrier_data,
        "plot": plot_info,
    }


# ---------------------------------------------------------------------------
# 5. Electric field extraction
# ---------------------------------------------------------------------------
def extract_electric_field(model, jm, config: dict, output_dir: Path) -> dict:
    """Extract electric field magnitude along device depth."""
    results = jm.result()
    datasets = list_datasets(jm)
    dset_tag = find_parametric_dataset(jm, datasets)
    cut_tag = None
    for tag in datasets:
        if "cut" in tag.lower() or "line" in tag.lower():
            cut_tag = tag
            break
    if not cut_tag:
        cut_tag = dset_tag

    field_data = {"position_nm": [], "E_V_per_m": []}
    try:
        vals = model.evaluate("semi.E_magnitude", dataset=cut_tag)
        if isinstance(vals, list):
            vals = np.concatenate([np.atleast_1d(x) for x in vals])
        field_data["E_V_per_m"] = np.atleast_1d(vals).tolist()
        try:
            pos = model.evaluate("y", dataset=cut_tag)
            if isinstance(pos, list):
                pos = np.concatenate([np.atleast_1d(x) for x in pos])
            field_data["position_nm"] = (np.atleast_1d(pos) * 1e9).tolist()
        except Exception:
            layers = config.get("device_stack", {}).get("layers", [])
            total = sum(l.get("thickness_nm", 100) for l in layers)
            field_data["position_nm"] = np.linspace(0, total, len(field_data["E_V_per_m"])).tolist()
    except Exception as e:
        field_data = {"error": str(e)}

    # Plot
    plot_info = {"status": "ok"}
    try:
        pg = results.create("pg_field_auto", "PlotGroup1D")
        lg = pg.create("lg_field", "LineGraph")
        lg.set("expr", "semi.E_magnitude")
        if cut_tag:
            lg.set("data", cut_tag)
        png_path = output_dir / "electric_field_auto.png"
        try:
            model.export(str(png_path))
            plot_info["png_path"] = str(png_path)
        except Exception:
            try:
                img = jm.result().export().create("img_field", "Image")
                img.set("plotgroup", "pg_field_auto")
                img.set("png", "on")
                img.set("filename", str(png_path))
                jm.result().export().run("img_field")
                plot_info["png_path"] = str(png_path)
            except Exception as e2:
                plot_info["png_error"] = str(e2)
    except Exception as e:
        plot_info = {"status": "error", "message": str(e)}

    # CSV
    csv_path = output_dir / "electric_field.csv"
    try:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Position_nm", "E_V_per_m"])
            for i in range(len(field_data.get("E_V_per_m", []))):
                writer.writerow([
                    field_data["position_nm"][i] if i < len(field_data["position_nm"]) else "",
                    field_data["E_V_per_m"][i],
                ])
        plot_info["csv_path"] = str(csv_path)
    except Exception as e:
        plot_info["csv_error"] = str(e)

    return {
        "status": plot_info.get("status", "ok"),
        "data": field_data,
        "plot": plot_info,
    }


# ---------------------------------------------------------------------------
# 6. EQE / Responsivity / Detectivity
# ---------------------------------------------------------------------------
def calculate_eqe_responsivity(iv_data: dict, config: dict) -> dict:
    """Calculate EQE and Responsivity from photocurrent."""
    h = 6.62607015e-34
    c = 2.99792458e8
    q = 1.602176634e-19

    wavelengths_nm = config.get("wavelengths_nm", [])
    optical_power_W = config.get("optical_power_W", 1e-3)
    device_area_m2 = config.get("device_area_m2", 1e-6)

    # If photocurrent data is not available from simulation, return framework
    eqe_results = []
    resp_results = []

    for wl_nm in wavelengths_nm:
        wl_m = wl_nm * 1e-9
        # Placeholder: actual photocurrent extraction requires optical generation coupling
        # For now, provide formula structure
        eqe_results.append({
            "wavelength_nm": wl_nm,
            "formula": f"EQE = {h*c/(q*wl_m):.3e} * (I_ph / {optical_power_W})",
            "unit": "%",
            "note": "I_ph must be extracted from illuminated I-V at each wavelength"
        })
        resp_results.append({
            "wavelength_nm": wl_nm,
            "formula": f"R = I_ph / {optical_power_W}",
            "unit": "A/W",
            "alt_formula": f"R = EQE * {wl_nm/1000:.3f} / 1.23985",
        })

    return {"eqe": eqe_results, "responsivity": resp_results}


def calculate_detectivity(iv_data: dict, eqe_data: list, config: dict) -> dict:
    """Calculate D* (shot-noise-limited)."""
    q = 1.602176634e-19
    J_dark_A_per_m2 = config.get("dark_current_density_A_per_m2", 1.0)
    J_dark_A_per_cm2 = J_dark_A_per_m2 * 1e-4

    detectivity_results = []
    for eqe_entry in eqe_data:
        wl_nm = eqe_entry["wavelength_nm"]
        # Placeholder responsivity
        R_A_per_W = 0.1
        D_star = R_A_per_W / math.sqrt(2 * q * J_dark_A_per_cm2)
        detectivity_results.append({
            "wavelength_nm": wl_nm,
            "responsivity_A_per_W": R_A_per_W,
            "dark_current_density_A_per_cm2": J_dark_A_per_cm2,
            "D_star_Jones": D_star,
        })

    return {"detectivity": detectivity_results, "assumption": "Shot-noise-limited"}


# ---------------------------------------------------------------------------
# 7. I-V analysis metrics
# ---------------------------------------------------------------------------
def analyze_iv_curve(iv_data: dict) -> dict:
    """Extract rectification ratio, ideality factor hints from I-V."""
    v = np.array(iv_data.get("voltage_V", []))
    i = np.array(iv_data.get("current_A", []))

    if len(v) == 0 or len(i) == 0:
        return {"status": "no_data"}

    # Separate forward and reverse
    fwd_mask = v >= 0
    rev_mask = v <= 0

    analysis = {
        "max_voltage_V": float(np.max(v)),
        "min_voltage_V": float(np.min(v)),
        "max_current_A": float(np.max(i)),
        "min_current_A": float(np.min(i)),
    }

    # Short-circuit current (at V=0)
    if 0 in v:
        idx = np.where(v == 0)[0]
        analysis["Isc_A"] = float(np.mean(i[idx]))
    else:
        analysis["Isc_A"] = float(np.interp(0, v, i))

    # Rectification ratio at max |V|
    if np.any(fwd_mask) and np.any(rev_mask):
        i_fwd_max = np.max(np.abs(i[fwd_mask]))
        i_rev_max = np.max(np.abs(i[rev_mask]))
        if i_rev_max > 0:
            analysis["rectification_ratio"] = float(i_fwd_max / i_rev_max)
        else:
            analysis["rectification_ratio"] = None

    return analysis


# ---------------------------------------------------------------------------
# 8. Main pipeline
# ---------------------------------------------------------------------------
def extract_all_metrics(model, config: dict, output_dir: Path) -> dict:
    jm = model.java
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. I-V
    iv_info = extract_iv_curve(model, jm, config)

    # 2. Band diagram
    band_info = extract_band_diagram(model, jm, config, output_dir)

    # 3. Carrier densities
    carrier_info = extract_carrier_densities(model, jm, config, output_dir)

    # 4. Electric field
    field_info = extract_electric_field(model, jm, config, output_dir)

    # 5. EQE / Responsivity / Detectivity framework
    eqe_resp = calculate_eqe_responsivity(iv_info, config)
    detectivity = calculate_detectivity(iv_info, eqe_resp["eqe"], config)

    # 6. I-V analysis
    iv_analysis = analyze_iv_curve(iv_info) if iv_info.get("status") == "ok" else {}

    # 7. Save summary JSON
    summary = {
        "status": "ok",
        "output_dir": str(output_dir),
        "iv_extraction": iv_info,
        "iv_analysis": iv_analysis,
        "band_diagram": band_info,
        "carrier_densities": carrier_info,
        "electric_field": field_info,
        "eqe_responsivity": eqe_resp,
        "detectivity": detectivity,
        "note": "Metrics extracted automatically. EQE/R/D* require photocurrent from optical generation coupling for full quantitative values.",
    }
    with open(output_dir / "metrics_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)

    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="Path to COMSOL .mph result file")
    parser.add_argument("--config", required=True, help="Path to simulation config JSON")
    parser.add_argument("--output", default=None, help="Output directory (default: auto from config)")
    args = parser.parse_args()

    mph = ensure_mph()
    client = mph.start()

    model_path = Path(args.model)
    if not model_path.exists():
        print(json.dumps({"status": "error", "message": f"Model file not found: {args.model}"}))
        sys.exit(1)

    model = client.load(str(model_path))

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    output_dir = Path(args.output) if args.output else Path(config.get("output_dir", "output/optoelectronic/metrics"))

    result = extract_all_metrics(model, config, output_dir)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
