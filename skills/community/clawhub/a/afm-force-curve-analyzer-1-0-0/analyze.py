#!/usr/bin/env python3
"""
AFM Force Curve Analyzer v1.0.0
AFM nanoindentation & force spectroscopy data analyzer for electrocatalysis.
Author: Labclaw 🦎 | 2026-04-17
"""

import argparse, sys, json, warnings, textwrap
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import integrate
from scipy.optimize import curve_fit, leastsq
from scipy.signal import savgol_filter
from lmfit import Model

# ─── Constants ────────────────────────────────────────────────────────────
PI = np.pi
KB = 1.380649e-23  # Boltzmann constant J/K
NAV = 6.022e23      # Avogadro number mol⁻¹
NU_SAMPLE_DEFAULT = 0.3   # Poisson ratio for NiOOH/Ni hydroxide
NU_TIP = 0.17             # Poisson ratio for SiN tip
E_TIP_SIN = 97e9         # Young's modulus of SiN tip (Pa)
ARCTAN_ANGLE_CONE = 15 * PI / 180  # default cone half-angle for AFM tip

# ─── Reference Database ──────────────────────────────────────────────────────
REFERENCE_MODULUS = {
    "NiOOH":          180e9,
    "γ-NiOOH":       120e9,
    "β-NiOOH":       200e9,
    "Ni(OH)₂":        50e9,
    "FeOOH":          80e9,
    "IrO₂":          350e9,
    "RuO₂":          300e9,
    "TiO₂":          230e9,
    "LiCoO₂":        200e9,
    "Si":            130e9,
    "Pt":             78e9,
    "Au":             79e9,
    "graphene":     1000e9,
    "CaCO₃":          30e9,
    "MXene":         300e9,
}

# ─── Models ─────────────────────────────────────────────────────────────────

def sneddon_cone(F, E_r, alpha, nu):
    """Indentation depth δ from force F for conical indenter (Sneddon)."""
    return np.sqrt(2 * F * (1 - nu**2) / (PI * E_r * np.tan(alpha)))

def hertz_spherical(F, R, E_r):
    """Indentation depth δ from force F for spherical contact (Hertz)."""
    return (F * R / E_r) ** (1/3)

def jkr_adhesion(F, E_r, R, w):
    """JKR model adhesion force from work of adhesion w."""
    return 1.5 * PI * R * w

def dmt_adhesion(F, E_r, R, w):
    """DMT model adhesion force from work of adhesion w."""
    return 2 * PI * R * w

def sneddon_extract_modulus(force_arr, depth_arr, alpha=ARCTAN_ANGLE_CONE,
                             nu=NU_SAMPLE_DEFAULT):
    """
    Extract Young's modulus via Sneddon cone model.
    F = (π/2) E tanα (1-ν²)⁻¹ δ²
    Linear fit of F vs δ² → slope → E
    """
    # Take approach portion only (positive slope)
    mask = depth_arr > 0
    F = force_arr[mask]
    d = depth_arr[mask]
    if len(F) < 5:
        return np.nan, np.nan, np.nan, np.nan, np.nan
    # Polynomial fit for baseline subtraction
    idx_sort = np.argsort(d)
    F_sorted = F[idx_sort]
    d_sorted = d[idx_sort]
    # Use upper 60% for linear fit (exclude noise floor)
    n_use = int(0.6 * len(F_sorted))
    if n_use < 3:
        n_use = max(3, len(F_sorted) // 2)
    d_fit = d_sorted[-n_use:]
    F_fit = F_sorted[-n_use:]
    # Fit F = A * d² (quadratic through origin)
    poly_coeffs = np.polyfit(d_fit, F_fit, 2, cov=False)
    A = poly_coeffs[0]  # quadratic coefficient (F = A*δ²)
    # Sneddon: F = (π/2) * E_r * tanα / (1-ν²) * δ²
    E_r = 2 * A * (1 - nu**2) / (PI * np.tan(alpha))
    # Convert to sample modulus (E_r = [(1-νs²)/Es + (1-νt²)/Et]⁻¹)
    # For hard tip: Es ≈ E_r
    delta_fitted_arr = np.sqrt(F_fit / A) if A > 0 else np.nan
    # R² of the quadratic fit
    F_pred = A * d_fit**2
    ss_res = np.sum((F_fit - F_pred)**2)
    ss_tot = np.sum((F_fit - np.mean(F_fit))**2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    if isinstance(delta_fitted_arr, np.ndarray) and len(delta_fitted_arr) > 0:
        d_fit_last = delta_fitted_arr[-1]
    elif np.isfinite(delta_fitted_arr):
        d_fit_last = delta_fitted_arr
    else:
        d_fit_last = np.nan
    return E_r, A, r2, d_fit_last, np.nan

def extract_adhesion(force_arr, distance_arr):
    """Extract adhesion force (minimum force) and pull-off work."""
    # Pull-off region: negative force (adhesive)
    mask = force_arr < 0
    if not np.any(mask):
        return np.nan, np.nan
    F_ad = np.min(force_arr[mask])   # most negative = max adhesion
    idx_ad = np.argmin(force_arr)
    # Pull-off work: integral of F over distance during pull-off
    d_arr = distance_arr[idx_ad:]
    F_arr = force_arr[idx_ad:]
    # Find where contact re-establishes (sign change)
    zero_crossings = np.where(np.diff(np.sign(F_arr)))[0]
    if len(zero_crossings) > 0:
        zc_idx = zero_crossings[0]
        d_work = d_arr[:zc_idx+1] - d_arr[0]
        F_work = F_arr[:zc_idx+1]
    else:
        d_work = d_arr - d_arr[0]
        F_work = F_arr
    work = np.trapz(np.abs(F_work), d_work) if len(d_work) > 1 else np.nan
    return abs(F_ad), work

def baseline_subtract(force_arr, distance_arr, method='polynomial'):
    """Subtract baseline from force curve."""
    # Identify non-contact region (far distance, near zero force)
    mask_contact = distance_arr < np.percentile(distance_arr, 80)
    d_contact = distance_arr[mask_contact]
    f_contact = force_arr[mask_contact]
    if len(d_contact) < 5:
        return force_arr
    # Polynomial baseline on approach portion
    popt = np.polyfit(d_contact, f_contact, 2)
    baseline = np.polyval(popt, distance_arr)
    return force_arr - baseline

# ─── Format Parsers ─────────────────────────────────────────────────────────

def parse_asylum_csv(path):
    """Parse Asylum Research (MFP-3D) CSV force curve."""
    with open(path, 'r') as f:
        lines = f.readlines()
    # Find header row
    header_idx = 0
    for i, line in enumerate(lines):
        if any(kw in line.lower() for kw in ['force', 'deflection', 'z', 'distance']):
            header_idx = i
            break
    # Try tab/comma/semicolon delimiter
    delim = ',' if ',' in lines[header_idx] else '\t' if '\t' in lines[header_idx] else ';'
    df = pd.read_csv(path, skiprows=header_idx, delim_whitespace=True if lines[header_idx].startswith(' ') else False,
                     on_bad_lines='skip')
    df.columns = [c.strip() for c in df.columns]
    # Identify columns
    z_col = next((c for c in df.columns if 'z' in c.lower() or 'height' in c.lower()), None)
    f_col = next((c for c in df.columns if 'force' in c.lower() or 'deflection' in c.lower()), None)
    if z_col is None or f_col is None:
        # Fall back to first two columns
        z_col, f_col = df.columns[0], df.columns[1]
    z = pd.to_numeric(df[z_col], errors='coerce').dropna().values
    f = pd.to_numeric(df[f_col], errors='coerce').dropna().values
    min_len = min(len(z), len(f))
    return z[:min_len], f[:min_len]

def parse_bruker_txt(path):
    """Parse Bruker Nanoscope force curve TXT."""
    with open(path, 'r') as f:
        lines = f.readlines()
    data_start = 0
    for i, line in enumerate(lines):
        if line.strip().replace('.','').replace('-','').isdigit():
            data_start = i
            break
    data = pd.read_csv(path, skiprows=data_start, header=None)
    # Typically: Deflection [m], Height [m], Time [s]
    z = data.iloc[:, 1].values
    f = data.iloc[:, 0].values
    return z, f

def parse_jpk_txt(path):
    """Parse JPK Instruments force curve TXT."""
    with open(path, 'r') as f:
        lines = f.readlines()
    header = {}
    for i, line in enumerate(lines):
        if '=' in line:
            key, val = line.split('=', 1)
            header[key.strip()] = val.strip()
    df = pd.read_csv(path, skiprows=len(header)+2, header=None)
    # JPK: force [N] vs piezo [m]
    f = df.iloc[:, 0].values
    z = df.iloc[:, 1].values
    return z, f

def parse_nanonis_sxm(path):
    """Parse Nanonis SXM AFM image/map file."""
    with open(path, 'rb') as f:
        content = f.read()
    # Simple parser: extract numeric data between markers
    data = np.frombuffer(content, dtype=float, count=-1)
    # Return raw data for grid reconstruction
    return data

def parse_force_map_csv(path):
    """Parse CSV force map grid: each row is a force curve."""
    df = pd.read_csv(path)
    # Expect columns: Distance, Force, or grid format
    cols = df.columns.tolist()
    return df

def auto_parse(path):
    """Auto-detect format and parse."""
    suffixes = {'.csv': 'csv', '.txt': 'txt', '.xlsx': 'xlsx', '.xls': 'xls', '.sxm': 'sxm', '.nwi': 'nwi'}
    ext = Path(path).suffix.lower()
    if ext in ['.csv', '.txt']:
        # Try to auto-detect format
        try:
            with open(path, 'r') as f:
                first = f.read(500)
            if 'asylum' in first.lower() or 'mfp' in first.lower():
                return parse_asylum_csv(path)
            elif 'bruker' in first.lower() or 'nanoscope' in first.lower():
                return parse_bruker_txt(path)
            elif 'jpk' in first.lower():
                return parse_jpk_txt(path)
            else:
                # Generic CSV
                df = pd.read_csv(path)
                z = df.iloc[:, 0].values
                f = df.iloc[:, 1].values
                return z, f
        except Exception:
            df = pd.read_csv(path)
            z = df.iloc[:, 0].values
            f = df.iloc[:, 1].values
            return z, f
    elif ext in ['.xlsx', '.xls']:
        df = pd.read_excel(path, header=None)
        z = df.iloc[:, 0].values
        f = df.iloc[:, 1].values
        return z, f
    elif ext == '.sxm':
        return parse_nanonis_sxm(path)
    return None, None

# ─── Main Analyzer ───────────────────────────────────────────────────────────

def analyze_single_curve(z, f, indenter='conical', tip_radius=None,
                         nu=NU_SAMPLE_DEFAULT, alpha=ARCTAN_ANGLE_CONE,
                         save_path=None):
    """Analyze a single force curve."""
    # Convert to SI (assume nN/nm → N/m if needed; scale if values are tiny)
    # Detect units from magnitude
    if np.nanmax(np.abs(f)) < 1e-6:  # probably in nN
        f = f * 1e-9  # nN → N
    if np.nanmax(np.abs(z)) < 1e-6:  # probably in nm
        z = z * 1e-9  # nm → m
    # Baseline subtraction
    f_bs = baseline_subtract(f, z)
    # Extract modulus
    if indenter == 'conical':
        E_r, A, r2, max_disp, _ = sneddon_extract_modulus(f_bs, z, alpha=alpha, nu=nu)
        E_s = E_r  # approximate sample modulus
    elif indenter == 'spherical':
        if tip_radius is None:
            tip_radius = 20e-9  # default 20nm
        E_r = None
        E_s = E_r
        A = None
        r2 = None
        max_disp = None
    else:
        E_r = E_s = A = r2 = max_disp = np.nan
    # Adhesion
    F_ad, W_ad = extract_adhesion(f_bs, z)
    # Stiffness (contact slope)
    mask_contact = z > np.percentile(z, 60)
    if np.sum(mask_contact) > 3:
        slope = np.polyfit(z[mask_contact], f_bs[mask_contact], 1)[0]
    else:
        slope = np.nan
    result = {
        'modulus_E_r_Pa': E_r,
        'modulus_E_sample_Pa': E_s,
        'fit_R2': r2,
        'adhesion_force_N': F_ad,
        'pull_off_work_J': W_ad,
        'contact_slope_N_m': slope,
        'max_indentation_m': max_disp,
        'indenter_type': indenter,
        'tip_radius_m': tip_radius,
        'poisson_ratio': nu,
    }
    return result, z, f_bs

def build_dashboard(curve_data, results, labels, out_path, title="AFM Force Curve Analysis"):
    """Build multi-panel PNG dashboard.
    curve_data: list of (z, f) tuples for plotting
    results: list of result dicts for statistics
    """
    n = len(curve_data)
    n_cols = min(3, n)
    n_rows = (n + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(4*n_cols, 3.5*n_rows))
    fig.suptitle(title, fontsize=14, fontweight='bold')
    if n == 1:
        axes = np.array([axes])
    axes = np.array(axes).flatten()
    # Panel 1: Force curves overlay
    ax = axes[0]
    colors = plt.cm.tab10(np.linspace(0, 1, n))
    for i, ((z, f), label, color) in enumerate(zip(curve_data, labels, colors)):
        if len(z) == 0:
            continue
        if np.nanmax(np.abs(f)) < 1e-9:
            f_disp = f * 1e9  # N → nN
            z_disp = z * 1e9  # m → nm
            unit_f, unit_z = 'nN', 'nm'
        else:
            f_disp = f * 1e6  # N → μN
            z_disp = z * 1e6  # m → μm
            unit_f, unit_z = 'μN', 'μm'
        ax.plot(z_disp, f_disp, color=color, label=label, lw=1.5, alpha=0.8)
    ax.set_xlabel(f'Indentation ({unit_z})')
    ax.set_ylabel(f'Force ({unit_f})')
    ax.set_title('Force-Distance Curves')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    # Panel 2: Statistics bar chart
    if n >= 1 and len(axes) > 1:
        ax2 = axes[1]
        E_vals = [r.get('modulus_E_r_Pa', np.nan) for r in results]
        E_GPa = [v/1e9 if not np.isnan(v) else 0 for v in E_vals]
        bars = ax2.bar(labels, E_GPa, color=colors[:n], alpha=0.8, edgecolor='black')
        ax2.set_ylabel('Modulus E (GPa)')
        ax2.set_title("Young's Modulus Comparison")
        ax2.tick_params(axis='x', rotation=30)
        for bar, val in zip(bars, E_GPa):
            if val > 0:
                ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                        f'{val:.1f}', ha='center', va='bottom', fontsize=8)
    # Panel 3: Adhesion forces
    if n >= 1 and len(axes) > 2:
        ax3 = axes[2]
        F_ad_vals = [r.get('adhesion_force_N', np.nan) for r in results]
        F_ad_nN = [v*1e9 if not np.isnan(v) else 0 for v in F_ad_vals]
        bars3 = ax3.bar(labels, F_ad_nN, color=colors[:n], alpha=0.8, edgecolor='black')
        ax3.set_ylabel('Adhesion Force (nN)')
        ax3.set_title('Adhesion Force Comparison')
        ax3.tick_params(axis='x', rotation=30)
        for bar, val in zip(bars3, F_ad_nN):
            if val > 0:
                ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                        f'{val:.1f}', ha='center', va='bottom', fontsize=8)
    # Remaining panels: summary table placeholder
    for idx in range(min(3, n*3), len(axes)):
        axes[idx].axis('off')
    plt.tight_layout()
    png_path = Path(out_path) if out_path else Path.cwd() / 'afm_force_dashboard.png'
    plt.savefig(png_path, dpi=150, bbox_inches='tight')
    plt.close()
    return str(png_path)

def generate_markdown_report(results, labels, summary_stats, out_path):
    """Generate Markdown summary report."""
    lines = [
        "# AFM Force Curve Analysis Report",
        f"**Generated:** 2026-04-17 by Labclaw 🦎",
        "",
        "## Summary Statistics",
        f"| Sample | Modulus E (GPa) | Adhesion (nN) | Pull-off Work (pN·nm) | R² Fit |",
        f"|--------|----------------|---------------|----------------------|--------|",
    ]
    for r, lbl in zip(results, labels):
        E_GPa = r.get('modulus_E_r_Pa', np.nan) / 1e9 if not np.isnan(r.get('modulus_E_r_Pa', np.nan)) else 0
        F_nN = r.get('adhesion_force_N', np.nan) * 1e9 if not np.isnan(r.get('adhesion_force_N', np.nan)) else 0
        W_pN = r.get('pull_off_work_J', np.nan) * 1e12 if not np.isnan(r.get('pull_off_work_J', np.nan)) else 0
        r2 = r.get('fit_R2', np.nan)
        lines.append(f"| {lbl} | {E_GPa:.2f} | {F_nN:.2f} | {W_pN:.2f} | {r2:.4f} |")
    lines += ["", "## Overall Statistics", ""]
    if summary_stats:
        for k, v in summary_stats.items():
            lines.append(f"- **{k}:** {v}")
    lines += [
        "",
        "## Sneddon Cone Model",
        "For a conical indenter with half-angle α:",
        "$$F = \\frac{\\pi}{2} E_r \\tan\\alpha \\cdot \\delta^2$",
        "where $E_r$ is the reduced modulus and δ is indentation depth.",
        "",
        "## Reference Modulus Database",
        "| Material | E (GPa) |",
        "|----------|---------|",
    ]
    for mat, val in REFERENCE_MODULUS.items():
        lines.append(f"| {mat} | {val/1e9:.1f} |")
    lines += ["", "*Report generated by AFM Force Curve Analyzer v1.0.0*"]
    report_path = Path(out_path) if out_path else Path.cwd() / 'afm_force_report.md'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text('\n'.join(lines))
    return str(report_path)

# ─── CLI ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='AFM Force Curve Analyzer v1.0.0')
    parser.add_argument('--input', '-i', required=True, help='Input force curve file(s), comma-separated')
    parser.add_argument('--labels', '-l', default=None, help='Labels for each file, comma-separated')
    parser.add_argument('--indenter', default='conical', choices=['conical','spherical','pyramid'],
                        help='Indenter geometry (default: conical)')
    parser.add_argument('--tip-radius', type=float, default=20e-9,
                        help='Tip radius in m (default: 20e-9 = 20nm)')
    parser.add_argument('--poisson', '-ν', type=float, default=NU_SAMPLE_DEFAULT,
                        help='Poisson ratio of sample (default: 0.3 for NiOOH)')
    parser.add_argument('--alpha', type=float, default=15.0,
                        help='Cone half-angle in degrees (default: 15°)')
    parser.add_argument('--output', '-o', default='./afm_force_output',
                        help='Output directory')
    parser.add_argument('--format', default='png,csv,json,md',
                        help='Output formats (comma-separated)')
    parser.add_argument('--ref-database', action='store_true',
                        help='Print reference modulus database and exit')
    args = parser.parse_args()

    if args.ref_database:
        print("=== Reference Modulus Database ===")
        for mat, val in sorted(REFERENCE_MODULUS.items(), key=lambda x: -x[1]):
            print(f"  {mat:12s}: {val/1e9:7.1f} GPa")
        return

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    alpha_rad = args.alpha * PI / 180

    input_files = [f.strip() for f in args.input.split(',')]
    if args.labels:
        labels = [l.strip() for l in args.labels.split(',')]
        if len(labels) < len(input_files):
            labels += [f'Sample{i+1}' for i in range(len(labels), len(input_files))]
    else:
        labels = [Path(f).stem for f in input_files]

    results, zf_pairs = [], []
    for fpath in input_files:
        z, F = auto_parse(fpath)
        if z is None or len(z) == 0:
            warnings.warn(f"Could not parse: {fpath}")
            continue
        res, z_sub, f_sub = analyze_single_curve(z, F, indenter=args.indenter,
                                                   tip_radius=args.tip_radius,
                                                   nu=args.poisson, alpha=alpha_rad)
        results.append(res)
        zf_pairs.append((z_sub, f_sub))

    if not results:
        print("No valid data parsed. Exiting.")
        sys.exit(1)

    # Summary statistics
    E_vals = np.array([r['modulus_E_r_Pa'] for r in results])
    F_vals = np.array([r['adhesion_force_N'] for r in results])
    summary = {
        'Mean Modulus (GPa)': f"{np.nanmean(E_vals)/1e9:.2f} ± {np.nanstd(E_vals)/1e9:.2f}",
        'Mean Adhesion (nN)': f"{np.nanmean(F_vals)*1e9:.2f} ± {np.nanstd(F_vals)*1e9:.2f}",
        'N_curves': len(results),
        'Indenter': args.indenter,
        'Tip radius (nm)': f"{args.tip_radius*1e9:.1f}",
        'Poisson ratio': args.poisson,
        'Cone half-angle (°)': args.alpha,
    }

    outputs = []
    fmts = [f.strip() for f in args.format.split(',')]
    for fmt in fmts:
        if fmt == 'png':
            p = build_dashboard(zf_pairs, results, labels, out_dir / 'afm_force_dashboard.png',
                                title='AFM Force Curve Analysis Dashboard')
            outputs.append(p)
        elif fmt == 'csv':
            df = pd.DataFrame(results)
            # Add labels
            df.insert(0, 'sample', labels[:len(df)])
            csv_path = out_dir / 'afm_force_results.csv'
            df.to_csv(csv_path, index=False)
            outputs.append(str(csv_path))
        elif fmt == 'json':
            json_path = out_dir / 'afm_force_results.json'
            with open(json_path, 'w') as jf:
                json.dump({'summary': summary, 'results': results, 'labels': labels}, jf,
                          indent=2, default=str)
            outputs.append(str(json_path))
        elif fmt == 'md':
            p = generate_markdown_report(results, labels, summary, out_dir / 'afm_force_report.md')
            outputs.append(p)

    print(f"\n✅ AFM Force Curve Analysis Complete")
    print(f"   Curves analyzed: {len(results)}")
    print(f"   Output directory: {out_dir}")
    for o in outputs:
        print(f"   → {o}")

if __name__ == '__main__':
    main()
