#!/usr/bin/env python3
"""
abs_query.py — ABS SDMX REST query engine

Fetches data from the ABS Data API and formats it as value + citation,
table, CSV, JSON, or (optionally) a chart.

Usage:
    abs_query.py <dataflow_id> [KEY] [options]
    abs_query.py --preset <preset_name> [options]
    abs_query.py --list-presets
    abs_query.py --describe-preset <name>
    abs_query.py --summary latest --preset <name>
    abs_query.py --report macro-snapshot

Arguments:
    dataflow_id    ABS dataflow ID  (e.g. CPI, LF, WPI)
    KEY            SDMX dimension key, dot-separated (e.g. 1.10003.10.Q)
                   Use "all" or omit for all data (server may apply defaults)

Options:
    --version VER            Dataflow version (default: auto-detect from catalog)
    --start-period P         Start period  e.g. 2020-Q1 or 2020-01
    --end-period P           End period
    --latest                 Fetch only the latest observation
    --format FMT             Output format: text (default), csv, json, table
    --chart                  Plot a line chart (requires matplotlib)
    --citation-style S       Citation style: inline (default) or analyst
    --out FILE               Write output to FILE instead of stdout
    --flat-view              Use AllDimensions format (wide/flat response; may return large datasets)
    --preset NAME            Use a named preset query from presets.json
    --list-presets           List all available preset queries and exit
    --describe-preset NAME   Show full description for a preset and exit
    --summary latest         Show latest value with change context (works with --preset)
    --report macro-snapshot  Build a compact macro economic snapshot from presets

Examples:
    abs_query.py CPI 1.10003.10.Q --latest
    abs_query.py LF 1.3.15.M --start-period 2020-01 --format table
    abs_query.py WPI 1... --latest --format csv
    abs_query.py ANA_AGG --latest --format json
    abs_query.py ANA_AGG --latest --format table --citation-style analyst

    # Using presets (quick queries for common indicators)
    abs_query.py --preset cpi-all-groups --format table
    abs_query.py --preset unemployment-rate --latest
    abs_query.py --preset gdp-annual-change --chart
    abs_query.py --list-presets
    abs_query.py --describe-preset cpi-annual-change

    # Summary mode (latest + context)
    abs_query.py --preset cpi-annual-change --summary latest
    abs_query.py --preset unemployment-rate --summary latest

    # Report mode (macro snapshot)
    abs_query.py --report macro-snapshot
"""

import csv
import io
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

BASE_URL = "https://data.api.abs.gov.au/rest"
CACHE_DIR = Path(os.environ.get("ABS_CACHE_DIR", Path.home() / ".cache" / "abs-data-api"))
SKILL_DIR = Path(__file__).parent.parent  # skills/abs-data-api/
PRESETS_FILE = SKILL_DIR / "presets.json"

# Threshold: warn when query returns more observations than this (heuristic for "too broad")
BROAD_QUERY_THRESHOLD = 100

# Presets used for macro-snapshot report (in display order)
MACRO_SNAPSHOT_PRESETS = [
    ("cpi-annual-change", "Inflation (CPI)"),
    ("gdp-annual-change", "GDP Growth"),
    ("unemployment-rate", "Unemployment Rate"),
    ("wage-annual-change", "Wage Growth (WPI)"),
    ("participation-rate", "Participation Rate"),
    ("population-national", "Population (ERP)"),
    ("trade-balance", "Goods Trade Balance"),
    ("household-spending-change", "Household Spending"),
]


# ---------------------------------------------------------------------------
# Period rendering helpers
# ---------------------------------------------------------------------------

MONTH_NAMES = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]

QUARTER_MONTH = {
    "Q1": "March quarter",
    "Q2": "June quarter",
    "Q3": "September quarter",
    "Q4": "December quarter",
}


def _render_period(period: str) -> str:
    """Convert raw ABS period code to human-readable string.

    Examples:
        2026-01   -> January 2026
        2025-Q4   -> December quarter 2025
        2025-Q1   -> March quarter 2025
        2025      -> 2025
        2025-W01  -> Week 1, 2025
    """
    if not period:
        return period
    # Monthly: YYYY-MM
    m = re.match(r"^(\d{4})-(\d{2})$", period)
    if m:
        year, month = int(m.group(1)), int(m.group(2))
        if 1 <= month <= 12:
            return f"{MONTH_NAMES[month]} {year}"
        return period
    # Quarterly: YYYY-QN
    m = re.match(r"^(\d{4})-(Q[1-4])$", period)
    if m:
        year, q = m.group(1), m.group(2)
        label = QUARTER_MONTH.get(q, q)
        return f"{label} {year}"
    # Annual: YYYY
    m = re.match(r"^(\d{4})$", period)
    if m:
        return period
    return period


def _render_period_range(periods: list) -> str:
    """Render a range of periods cleanly."""
    if not periods:
        return ""
    unique = sorted(set(periods))
    if len(unique) == 1:
        return _render_period(unique[0])
    return f"{_render_period(unique[0])} to {_render_period(unique[-1])}"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _request(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:500]
        raise RuntimeError(f"HTTP {e.code} for {url}\n{body}") from e


def _get_version(dataflow_id: str) -> str:
    """Look up version from local catalog or generated metadata, default 1.0.0."""
    # Try generated metadata first
    from pathlib import Path as _Path
    meta_file = CACHE_DIR / "metadata.generated.json"
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text())
            if dataflow_id in meta:
                v = meta[dataflow_id].get("version")
                if v:
                    return v
        except Exception:
            pass
    catalog_file = CACHE_DIR / "catalog.json"
    if catalog_file.exists():
        try:
            catalog = json.loads(catalog_file.read_text())
            if dataflow_id in catalog:
                return catalog[dataflow_id].get("version", "1.0.0")
        except Exception:
            pass
    return "1.0.0"


def _build_data_url(dataflow_id: str, version: str, key: str,
                    start_period: str = None, end_period: str = None,
                    latest: bool = False, flat_view: bool = False) -> str:
    """Construct SDMX REST data URL."""
    if not key or key.lower() in ("all", ""):
        key = "all"
    url = f"{BASE_URL}/data/ABS,{dataflow_id},{version}/{key}"
    params = []

    if flat_view or (latest and flat_view):
        params.append("dimensionAtObservation=AllDimensions")
    else:
        params.append("dimensionAtObservation=TIME_PERIOD")

    if latest:
        params.append("lastNObservations=1")
    if start_period:
        params.append(f"startPeriod={start_period}")
    if end_period:
        params.append(f"endPeriod={end_period}")
    if params:
        url += "?" + "&".join(params)
    return url


def _parse_response(data: dict) -> tuple:
    """
    Parse SDMX-JSON response (handles both series-level and AllDimensions formats).
    Returns (dimensions, observations) where:
      dimensions  : list of {"id", "name", "values": [{"id","name"},...]}
      observations: list of {"dims": [...codes], "value": float|None, "period": str}
    """
    structure = data.get("structure") or data.get("data", {}).get("structure", {})
    if not structure:
        raise RuntimeError("No 'structure' key in response")

    all_dims_meta = structure.get("dimensions", {})
    datasets = data.get("dataSets") or data.get("data", {}).get("dataSets", [])
    if not datasets:
        raise RuntimeError("No 'dataSets' in response")
    dataset = datasets[0]

    def build_dim_list(dims_list):
        return [
            {
                "id": d.get("id", ""),
                "name": d.get("name", ""),
                "values": [{"id": v.get("id", ""), "name": v.get("name", "")}
                           for v in d.get("values", [])],
            }
            for d in dims_list
        ]

    observations = []

    # Format 1: AllDimensions — all dims encoded in observation key
    if "observations" in dataset:
        dims_meta = all_dims_meta.get("observation", [])
        dimensions = build_dim_list(dims_meta)
        for key_str, obs_vals in dataset["observations"].items():
            indices = [int(i) for i in key_str.split(":")]
            dim_codes = []
            period = ""
            for i, dim in enumerate(dimensions):
                idx = indices[i] if i < len(indices) else 0
                vals = dim["values"]
                code = vals[idx]["id"] if idx < len(vals) else str(idx)
                if dim["id"] == "TIME_PERIOD":
                    period = code
                dim_codes.append(code)
            value = obs_vals[0] if obs_vals else None
            observations.append({"dims": dim_codes, "value": value, "period": period})

    # Format 2: Series-level
    elif "series" in dataset:
        series_dims_meta = all_dims_meta.get("series", [])
        obs_dims_meta = all_dims_meta.get("observation", [])
        dimensions = build_dim_list(series_dims_meta) + build_dim_list(obs_dims_meta)

        for series_key_str, series_data in dataset["series"].items():
            series_indices = [int(i) for i in series_key_str.split(":")]
            series_codes = []
            for i, dim in enumerate(build_dim_list(series_dims_meta)):
                idx = series_indices[i] if i < len(series_indices) else 0
                vals = dim["values"]
                series_codes.append(vals[idx]["id"] if idx < len(vals) else str(idx))

            for obs_key_str, obs_vals in series_data.get("observations", {}).items():
                obs_idx = int(obs_key_str)
                period = ""
                obs_codes = []
                for j, dim in enumerate(build_dim_list(obs_dims_meta)):
                    if dim["id"] == "TIME_PERIOD":
                        vals = dim["values"]
                        code = vals[obs_idx]["id"] if obs_idx < len(vals) else str(obs_idx)
                        period = code
                        obs_codes.append(code)
                    else:
                        obs_codes.append(str(obs_idx))

                value = obs_vals[0] if obs_vals else None
                observations.append({
                    "dims": series_codes + obs_codes,
                    "value": value,
                    "period": period,
                })
    else:
        raise RuntimeError("Dataset has neither 'observations' nor 'series' key")

    observations.sort(key=lambda o: o.get("period", ""))
    return dimensions, observations


def _dataset_name(dataflow_id: str) -> str | None:
    """Look up human-readable dataset name. Prefers structured metadata over markdown."""
    # Try generated metadata first
    meta_file = CACHE_DIR / "metadata.generated.json"
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text())
            item = meta.get(dataflow_id, {})
            name = item.get("name")
            if name and name != dataflow_id:
                # Strip trailing "(ID)" suffix if present
                suffix = f" ({dataflow_id})"
                if name.endswith(suffix):
                    name = name[:-len(suffix)]
                return name
        except Exception:
            pass

    # Fall back to catalog
    catalog_file = CACHE_DIR / "catalog.json"
    if catalog_file.exists():
        try:
            catalog = json.loads(catalog_file.read_text())
            item = catalog.get(dataflow_id)
            if isinstance(item, dict):
                name = item.get("name") or item.get("description")
                if isinstance(name, str):
                    suffix = f" ({dataflow_id})"
                    if name.endswith(suffix):
                        name = name[:-len(suffix)]
                    return name
        except Exception:
            pass
    return None


def _catalogue_number(dataflow_id: str) -> str | None:
    """Look up the ABS catalogue number. Prefers structured metadata."""
    # Try generated metadata
    meta_file = CACHE_DIR / "metadata.generated.json"
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text())
            cat = meta.get(dataflow_id, {}).get("cat_no")
            if cat:
                return cat
        except Exception:
            pass

    # Fall back to markdown catalog (for datasets not in presets)
    catalog_md = SKILL_DIR / "references" / "dataset-catalog.md"
    if not catalog_md.exists():
        return None
    needle = f"`{dataflow_id}`"
    try:
        for line in catalog_md.read_text().splitlines():
            if needle in line and line.strip().startswith("|"):
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 5 and parts[1] == needle:
                    return parts[4]
    except Exception:
        pass
    return None


def _period_label(observations: list) -> str | None:
    """Return a human-readable period label for single values or compact ranges."""
    periods = [o.get("period") for o in observations if o.get("period")]
    if not periods:
        return None
    return _render_period_range(periods)


def _citation(dataflow_id: str, version: str, observations: list | None = None) -> str:
    dataset_name = _dataset_name(dataflow_id)
    cat_no = _catalogue_number(dataflow_id)
    period = _period_label(observations or [])

    dataset_label = dataset_name or dataflow_id
    details = []
    if cat_no:
        details.append(f"Cat. {cat_no}")
    details.append(f"dataset `{dataflow_id}`")
    details.append(f"v{version}")
    details_str = "; ".join(details)

    parts = [
        f"Source: Australian Bureau of Statistics, *{dataset_label}* ({details_str})"
    ]
    if period:
        parts.append(period)
    parts.append(f"Retrieved via ABS Data API: {BASE_URL}/data/ABS,{dataflow_id},{version}/")
    return ". ".join(parts) + "."


def _load_presets() -> dict:
    """Load presets.json from the skill directory."""
    if PRESETS_FILE.exists():
        try:
            return json.loads(PRESETS_FILE.read_text())
        except Exception as e:
            print(f"Warning: could not load presets.json: {e}", file=sys.stderr)
    return {}


def _list_presets() -> str:
    """Return formatted list of available presets."""
    presets = _load_presets()
    if not presets:
        return "No presets found. Expected: " + str(PRESETS_FILE)
    lines = ["Available presets:\n"]
    for name, p in presets.items():
        lines.append(f"  {name}")
        lines.append(f"    Dataflow: {p['dataflow']}  Key: {p.get('key', 'all')}")
        lines.append(f"    {p.get('description', '')}")
        if p.get("note"):
            lines.append(f"    Note: {p['note']}")
        lines.append("")
    lines.append(f"Usage: abs_query.py --preset <name> [--latest] [--format text|csv|table|json] [--chart]")
    lines.append(f"       abs_query.py --describe-preset <name>")
    return "\n".join(lines)


def _describe_preset(preset_name: str) -> str:
    """Return full description of a preset."""
    presets = _load_presets()
    if preset_name not in presets:
        available = ", ".join(presets.keys()) if presets else "(none found)"
        return f"Error: unknown preset '{preset_name}'. Available: {available}"
    p = presets[preset_name]
    lines = [
        f"Preset: {preset_name}",
        f"{'─' * (len(preset_name) + 9)}",
        f"Description:     {p.get('description', '(none)')}",
        f"Dataflow:        {p.get('dataflow', '?')}",
        f"Key:             {p.get('key', 'all')}",
        f"What it measures: {p.get('what_it_measures', p.get('note', '(see note)'))}",
        f"When to use:     {p.get('when_to_use', '(see description)')}",
    ]
    if p.get("note"):
        lines.append(f"Technical note:  {p['note']}")
    lines.append("")
    lines.append(f"Example usage:")
    lines.append(f"  abs_query.py --preset {preset_name} --latest --format table")
    lines.append(f"  abs_query.py --preset {preset_name} --summary latest")
    return "\n".join(lines)


def _broad_query_warning(count: int, dataflow_id: str) -> str:
    """Return a warning string when the observation count is suspiciously high."""
    return (
        f"\n⚠️  WARNING: Query returned {count:,} observations — this may be broader than intended.\n"
        f"   Use a more specific dimension key to filter the data.\n"
        f"   Tip: check the dimension structure first:\n"
        f"     python3 scripts/abs_cache.py structure {dataflow_id}\n"
        f"   Then narrow the key, e.g. abs_query.py {dataflow_id} 1.10001.10.50.M --latest\n"
    )


# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------

def _label_for(dim: dict, value: str) -> str:
    """Return a friendly label for a dimension value when available."""
    for item in dim.get("values", []):
        if item.get("id") == value:
            return item.get("name") or value
    return value


def _friendly_obs_dims(dimensions: list, obs: dict) -> list:
    cells = []
    for i, d in enumerate(dimensions):
        val = obs["dims"][i] if i < len(obs["dims"]) else "?"
        cells.append(_label_for(d, val))
    return cells


def _analyst_footnote(dataflow_id: str, version: str, observations: list) -> str:
    dataset_name = _dataset_name(dataflow_id) or dataflow_id
    cat_no = _catalogue_number(dataflow_id)
    period = _period_label(observations) or "latest available period"
    details = [f"dataset `{dataflow_id}`", f"v{version}"]
    if cat_no:
        details.insert(0, f"Cat. {cat_no}")
    return f"Sources\n- Australian Bureau of Statistics, *{dataset_name}* ({'; '.join(details)}), {period}, via ABS Data API"


def fmt_text(dimensions: list, observations: list, dataflow_id: str, version: str, citation_style: str = "inline") -> str:
    lines = []
    time_idx = next((i for i, d in enumerate(dimensions) if d["id"] == "TIME_PERIOD"), len(dimensions) - 1)

    for obs in observations[-50:]:
        parts = []
        for i, d in enumerate(dimensions):
            if d["id"] == "TIME_PERIOD":
                continue
            val = obs["dims"][i] if i < len(obs["dims"]) else "?"
            label = _label_for(d, val)
            parts.append(f"{d['id']}={label}")
        period = obs.get("period", obs["dims"][time_idx] if time_idx < len(obs["dims"]) else "?")
        period_display = _render_period(period)
        value = obs["value"]
        value_str = f"{value:,.3f}" if isinstance(value, (int, float)) else str(value)
        dim_str = "  ".join(parts) if parts else ""
        lines.append(f"{period_display}  {value_str}  {dim_str}")

    if len(observations) > 50:
        lines.append(f"... ({len(observations)} total observations; showing last 50)")

    lines.append("")
    lines.append(_analyst_footnote(dataflow_id, version, observations) if citation_style == "analyst" else _citation(dataflow_id, version, observations))
    return "\n".join(lines)


def fmt_csv(dimensions: list, observations: list, dataflow_id: str, version: str) -> str:
    output = io.StringIO()
    headers = [d["id"] for d in dimensions] + ["value"]
    writer = csv.writer(output)
    writer.writerow(headers)
    for obs in observations:
        row = obs["dims"] + [obs["value"]]
        writer.writerow(row)
    writer.writerow([])
    writer.writerow(["# " + _citation(dataflow_id, version, observations)])
    return output.getvalue()


def fmt_json(dimensions: list, observations: list, dataflow_id: str, version: str) -> str:
    """JSON output with raw codes AND friendly *_label fields for each dimension."""
    dim_ids = [d["id"] for d in dimensions]
    obs_list = []
    for obs in observations:
        row = {}
        for i, d in enumerate(dimensions):
            raw_val = obs["dims"][i] if i < len(obs["dims"]) else None
            row[d["id"]] = raw_val
            # Add label field for non-TIME_PERIOD dimensions
            if d["id"] != "TIME_PERIOD":
                row[d["id"] + "_label"] = _label_for(d, raw_val) if raw_val is not None else None
            else:
                row["TIME_PERIOD_rendered"] = _render_period(raw_val) if raw_val else None
        row["value"] = obs["value"]
        obs_list.append(row)

    result = {
        "dataflow": dataflow_id,
        "version": version,
        "dimensions": dim_ids,
        "observations": obs_list,
        "citation": _citation(dataflow_id, version, observations),
    }
    return json.dumps(result, indent=2)


def fmt_table(dimensions: list, observations: list, dataflow_id: str, version: str, citation_style: str = "inline") -> str:
    """Markdown-style table with friendly dimension labels and rendered periods."""
    headers = [d["id"] for d in dimensions] + ["VALUE"]
    rendered_rows = []
    for obs in observations:
        friendly = []
        for i, d in enumerate(dimensions):
            val = obs["dims"][i] if i < len(obs["dims"]) else "?"
            if d["id"] == "TIME_PERIOD":
                friendly.append(_render_period(val))
            else:
                friendly.append(_label_for(d, val))
        value = obs["value"]
        value = f"{value:,.3f}" if isinstance(value, (int, float)) else str(value)
        rendered_rows.append(friendly + [value])

    col_widths = [max(len(h), 8) for h in headers]
    for row in rendered_rows:
        for i, v in enumerate(row):
            if len(str(v)) > col_widths[i]:
                col_widths[i] = len(str(v))

    def row_str(cells):
        return "| " + " | ".join(str(c).ljust(col_widths[i]) for i, c in enumerate(cells)) + " |"

    lines = [
        row_str(headers),
        "| " + " | ".join("-" * col_widths[i] for i in range(len(headers))) + " |",
    ]
    for row in rendered_rows:
        lines.append(row_str(row))
    lines.append("")
    lines.append(_analyst_footnote(dataflow_id, version, observations) if citation_style == "analyst" else _citation(dataflow_id, version, observations))
    return "\n".join(lines)


def fmt_chart(dimensions: list, observations: list, dataflow_id: str, version: str,
              out_file: str = None, dataset_name: str = None) -> str:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return "[Chart skipped: matplotlib not installed. Run: pip install matplotlib]\n" + \
               fmt_text(dimensions, observations, dataflow_id, version)

    time_idx = next((i for i, d in enumerate(dimensions) if d["id"] == "TIME_PERIOD"), len(dimensions) - 1)
    periods = [obs["dims"][time_idx] if time_idx < len(obs["dims"]) else "" for obs in observations]
    values = [obs["value"] for obs in observations]

    pairs = [(p, v) for p, v in zip(periods, values) if isinstance(v, (int, float))]
    if not pairs:
        return "[Chart skipped: no numeric values]\n" + fmt_text(dimensions, observations, dataflow_id, version)

    x_labels = [p for p, _ in pairs]
    y_values = [v for _, v in pairs]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(range(len(y_values)), y_values, marker="o", markersize=3, linewidth=1.5)

    # Use dataset name in title if available
    title = dataset_name or _dataset_name(dataflow_id) or dataflow_id
    ax.set_title(title, fontsize=13, fontweight="bold")

    # Subtitle with source and period
    if periods:
        period_range = _render_period_range(periods)
        subtitle = f"ABS {dataflow_id} v{version} | {period_range}"
        ax.set_xlabel(subtitle, fontsize=8, color="gray")
    ax.set_ylabel("Value")

    # Annotate latest point
    if y_values:
        last_x = len(y_values) - 1
        last_y = y_values[-1]
        ax.annotate(
            f"{last_y:,.2f}",
            xy=(last_x, last_y),
            xytext=(last_x - max(1, len(y_values) // 10), last_y),
            fontsize=8,
            color="navy",
            arrowprops=dict(arrowstyle="->", color="navy", lw=0.8),
        )

    # Show every Nth label
    n = max(1, len(x_labels) // 20)
    ax.set_xticks(range(0, len(x_labels), n))
    rendered_labels = [_render_period(lbl) for lbl in x_labels[::n]]
    ax.set_xticklabels(rendered_labels, rotation=45, ha="right", fontsize=7)

    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    # Friendly filename
    if out_file:
        chart_path = out_file.replace(".txt", ".png") if out_file.endswith(".txt") else out_file + ".png"
    else:
        safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", dataflow_id.lower())
        chart_path = f"/tmp/abs_{safe_name}.png"

    plt.savefig(chart_path, dpi=120)
    plt.close()
    return f"Chart saved: {chart_path}\n\n" + _citation(dataflow_id, version, observations)


def _uses_percentage_point_change(label: str = "", preset_name: str = "", dataflow_id: str = "") -> bool:
    """Return True for rates/growth measures that should use percentage-point deltas, not relative % change."""
    text = " ".join([label or "", preset_name or "", dataflow_id or ""]).lower()
    markers = [
        "rate",
        "growth",
        "inflation",
        "annual change",
        "annual-change",
        "percentage change",
        "percentage-change",
        "participation",
        "underemployment",
        "unemployment",
    ]
    return any(m in text for m in markers)


def fmt_summary(dimensions: list, observations: list, dataflow_id: str, version: str,
                preset_name: str = None) -> str:
    """
    'Latest plus context' summary mode.
    Shows latest value, previous value, absolute/percent change, and a short textual summary.
    """
    if not observations:
        return "No observations to summarise."

    # Get last two numeric observations
    numeric_obs = [o for o in observations if isinstance(o.get("value"), (int, float))]
    if not numeric_obs:
        return "No numeric observations to summarise."

    latest = numeric_obs[-1]
    previous = numeric_obs[-2] if len(numeric_obs) >= 2 else None

    latest_period = _render_period(latest.get("period", ""))
    latest_val = latest["value"]

    dataset_name = _dataset_name(dataflow_id) or dataflow_id
    pp_mode = _uses_percentage_point_change(dataset_name, preset_name or "", dataflow_id)

    lines = []
    lines.append(f"{'─' * 50}")
    lines.append(f"  {dataset_name}")
    if preset_name:
        lines.append(f"  Preset: {preset_name}")
    lines.append(f"{'─' * 50}")
    lines.append(f"  Latest:   {latest_val:,.3f}  ({latest_period})")

    if previous is not None:
        prev_period = _render_period(previous.get("period", ""))
        prev_val = previous["value"]
        lines.append(f"  Previous: {prev_val:,.3f}  ({prev_period})")

        abs_change = latest_val - prev_val
        if pp_mode:
            change_str = f"{abs_change:+,.3f} percentage points"
        elif prev_val != 0:
            pct_change = (abs_change / abs(prev_val)) * 100
            change_str = f"{abs_change:+,.3f}  ({pct_change:+.2f}%)"
        else:
            change_str = f"{abs_change:+,.3f}"
        lines.append(f"  Change:   {change_str}")

        # Short textual summary
        direction = "up" if abs_change > 0 else ("down" if abs_change < 0 else "unchanged")
        if abs_change != 0:
            if pp_mode:
                summary_text = (
                    f"{dataset_name} was {latest_val:,.2f} in {latest_period}, "
                    f"{direction} from {prev_val:,.2f} in {prev_period}, a change of {abs_change:+.2f} percentage points."
                )
            else:
                summary_text = (
                    f"{dataset_name} was {latest_val:,.2f} in {latest_period}, "
                    f"{direction} from {prev_val:,.2f} in {prev_period}."
                )
        else:
            summary_text = (
                f"{dataset_name} was {latest_val:,.2f} in {latest_period}, unchanged from {prev_period}."
            )
        lines.append("")
        lines.append(f"  Summary: {summary_text}")
    else:
        lines.append("")
        lines.append(f"  Summary: {dataset_name} was {latest_val:,.2f} in {latest_period}.")

    lines.append("")
    lines.append("  " + _citation(dataflow_id, version, [latest]))
    return "\n".join(lines)


def _run_macro_snapshot() -> str:
    """Build a compact macro economic snapshot from presets."""
    presets = _load_presets()
    lines = []
    lines.append("=" * 62)
    lines.append("  AUSTRALIAN MACRO SNAPSHOT")
    lines.append("  Source: ABS Data API | Generated by abs-data-api skill")
    lines.append("=" * 62)
    lines.append("")

    sources = []
    errors = []

    for preset_name, display_label in MACRO_SNAPSHOT_PRESETS:
        if preset_name not in presets:
            errors.append(f"  {display_label:30s}  [preset not found: {preset_name}]")
            continue

        preset = presets[preset_name]
        dataflow_id = preset["dataflow"]
        key = preset.get("key", "all")

        try:
            version = _get_version(dataflow_id)
            url = _build_data_url(dataflow_id, version, key, latest=False)
            # Fetch last 2 observations for change context
            url_2 = _build_data_url(dataflow_id, version, key, latest=False)
            url_2 = url_2 + ("&" if "?" in url_2 else "?") + "lastNObservations=2"
            raw = _request(url_2)
            dimensions, observations = _parse_response(raw)

            if not observations:
                errors.append(f"  {display_label:30s}  [no data]")
                continue

            numeric_obs = [o for o in observations if isinstance(o.get("value"), (int, float))]
            if not numeric_obs:
                errors.append(f"  {display_label:30s}  [no numeric data]")
                continue

            latest = numeric_obs[-1]
            val = latest["value"]
            period_raw = latest.get("period", "")
            period_display = _render_period(period_raw)

            change_str = ""
            if len(numeric_obs) >= 2:
                prev_val = numeric_obs[-2]["value"]
                if isinstance(prev_val, (int, float)):
                    chg = val - prev_val
                    arrow = "▲" if chg > 0 else ("▼" if chg < 0 else "→")
                    if _uses_percentage_point_change(display_label, preset_name, dataflow_id):
                        change_str = f"  {arrow} {chg:+.2f}pp"
                    elif prev_val != 0:
                        pct = (chg / abs(prev_val)) * 100
                        change_str = f"  {arrow} {pct:+.2f}%"
                    else:
                        change_str = f"  {arrow} {chg:+.2f}"

            lines.append(f"  {display_label:30s}  {val:>10,.2f}  ({period_display}){change_str}")

            # Collect source
            dataset_name = _dataset_name(dataflow_id) or dataflow_id
            cat_no = _catalogue_number(dataflow_id)
            src = f"ABS, *{dataset_name}*"
            if cat_no:
                src += f" (Cat. {cat_no})"
            sources.append(src)

        except Exception as e:
            errors.append(f"  {display_label:30s}  [error: {e}]")

    if errors:
        lines.append("")
        lines.append("  Note: the following presets could not be fetched:")
        lines.extend(errors)

    if sources:
        lines.append("")
        lines.append("─" * 62)
        lines.append("Sources")
        for s in sources:
            lines.append(f"  - {s}, via ABS Data API")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main query function
# ---------------------------------------------------------------------------

def query(dataflow_id: str, key: str = "all", version: str = None,
          start_period: str = None, end_period: str = None,
          latest: bool = False, fmt: str = "text",
          chart: bool = False, out_file: str = None,
          flat_view: bool = False, citation_style: str = "inline",
          summary_mode: str = None, preset_name: str = None) -> str:
    if not version:
        version = _get_version(dataflow_id)

    url = _build_data_url(dataflow_id, version, key, start_period, end_period, latest, flat_view)
    print(f"Fetching: {url}", file=sys.stderr)
    raw = _request(url)
    dimensions, observations = _parse_response(raw)

    if not observations:
        return f"No observations returned.\nURL: {url}\n{_citation(dataflow_id, version, observations)}"

    # Broad query warning
    if len(observations) > BROAD_QUERY_THRESHOLD:
        warning = _broad_query_warning(len(observations), dataflow_id)
        sys.stderr.write(warning)

    # Summary mode
    if summary_mode == "latest":
        return fmt_summary(dimensions, observations, dataflow_id, version, preset_name=preset_name)

    dataset_name = _dataset_name(dataflow_id)

    if chart:
        result = fmt_chart(dimensions, observations, dataflow_id, version, out_file, dataset_name=dataset_name)
    elif fmt == "csv":
        result = fmt_csv(dimensions, observations, dataflow_id, version)
    elif fmt == "json":
        result = fmt_json(dimensions, observations, dataflow_id, version)
    elif fmt == "table":
        result = fmt_table(dimensions, observations, dataflow_id, version, citation_style=citation_style)
    else:
        result = fmt_text(dimensions, observations, dataflow_id, version, citation_style=citation_style)

    return result


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    # --list-presets
    if "--list-presets" in args:
        print(_list_presets())
        sys.exit(0)

    # --describe-preset <name>
    if "--describe-preset" in args:
        idx = args.index("--describe-preset")
        if idx + 1 < len(args):
            name = args[idx + 1]
        else:
            print("Error: --describe-preset requires a preset name", file=sys.stderr)
            sys.exit(1)
        print(_describe_preset(name))
        sys.exit(0)

    # --report macro-snapshot
    if "--report" in args:
        idx = args.index("--report")
        report_name = args[idx + 1] if idx + 1 < len(args) else "macro-snapshot"
        if report_name == "macro-snapshot":
            print(_run_macro_snapshot())
        else:
            print(f"Unknown report: {report_name}. Available: macro-snapshot", file=sys.stderr)
            sys.exit(1)
        sys.exit(0)

    # Parse --preset
    preset_name = None
    preset_dataflow = None
    preset_key = None
    if "--preset" in args:
        idx = args.index("--preset")
        if idx + 1 < len(args):
            preset_name = args[idx + 1]
            args = args[:idx] + args[idx + 2:]
        else:
            print("Error: --preset requires a preset name. Use --list-presets to see options.", file=sys.stderr)
            sys.exit(1)

        presets = _load_presets()
        if preset_name not in presets:
            available = ", ".join(presets.keys()) if presets else "(none found)"
            print(f"Error: unknown preset '{preset_name}'. Available: {available}", file=sys.stderr)
            sys.exit(1)
        preset = presets[preset_name]
        preset_dataflow = preset["dataflow"]
        preset_key = preset.get("key", "all")
        print(f"Using preset '{preset_name}': {preset.get('description', '')}", file=sys.stderr)

    # Positional arg: dataflow_id
    if not preset_name:
        if not args:
            print("Error: dataflow_id required. Usage: abs_query.py <ID> [KEY] [options]", file=sys.stderr)
            sys.exit(1)
        dataflow_id = args[0]
        args = args[1:]
    else:
        dataflow_id = preset_dataflow
        if args and not args[0].startswith("--"):
            args = args[1:]

    key = preset_key if preset_name else "all"
    version = None
    start_period = None
    end_period = None
    latest = False
    fmt = "text"
    chart = False
    out_file = None
    flat_view = False
    citation_style = "inline"
    summary_mode = None

    i = 0
    while i < len(args):
        a = args[i]
        if a == "--version" and i + 1 < len(args):
            version = args[i + 1]; i += 2
        elif a == "--start-period" and i + 1 < len(args):
            start_period = args[i + 1]; i += 2
        elif a == "--end-period" and i + 1 < len(args):
            end_period = args[i + 1]; i += 2
        elif a == "--latest":
            latest = True; i += 1
        elif a == "--format" and i + 1 < len(args):
            fmt = args[i + 1]; i += 2
        elif a == "--chart":
            chart = True; i += 1
        elif a == "--out" and i + 1 < len(args):
            out_file = args[i + 1]; i += 2
        elif a == "--flat-view":
            flat_view = True; i += 1
        elif a == "--citation-style" and i + 1 < len(args):
            citation_style = args[i + 1]; i += 2
        elif a == "--summary" and i + 1 < len(args):
            summary_mode = args[i + 1]; i += 2
        elif not a.startswith("--"):
            if not preset_name:
                key = a
            i += 1
        else:
            print(f"Unknown option: {a}", file=sys.stderr)
            i += 1

    try:
        result = query(
            dataflow_id, key=key, version=version,
            start_period=start_period, end_period=end_period,
            latest=latest, fmt=fmt, chart=chart, out_file=out_file,
            flat_view=flat_view, citation_style=citation_style,
            summary_mode=summary_mode, preset_name=preset_name,
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if out_file and not chart:
        Path(out_file).write_text(result)
        print(f"Output written to {out_file}")
    else:
        print(result)


if __name__ == "__main__":
    main()
