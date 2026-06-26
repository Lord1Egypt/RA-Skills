#!/usr/bin/env python3
"""Export workspace/bird.json observations to CSV (optional per-species summary)."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from bird_json_util import load_doc, workspace_bird_path  # noqa: E402

OBS_FIELDNAMES = [
    "time_utc",
    "species",
    "notes",
    "source",
    "image_path",
    "location_query",
    "ebird_region_code",
    "ebird_region_name",
    "ebird_region_name_cn",
    "ebird_country_code",
]

SUMMARY_FIELDNAMES = ["species", "count", "first_time_utc", "last_time_utc"]


def _region_tuple(doc: Dict[str, Any]) -> Tuple[str, str, str, str, str]:
    loc = (doc.get("location_query") or "").strip()
    cc = (doc.get("country_code") or "").strip()
    reg = doc.get("region")
    if not isinstance(reg, dict):
        return loc, "", "", "", cc
    code = (reg.get("code") or "").strip()
    name = (reg.get("name") or "").strip()
    name_cn = (reg.get("name_cn") or "").strip()
    return loc, code, name, name_cn, cc


def _obs_row(
    doc: Dict[str, Any],
    obs: Dict[str, Any],
) -> Dict[str, Any]:
    loc, rcode, rname, rname_cn, ccode = _region_tuple(doc)
    return {
        "time_utc": (obs.get("time_utc") or "").strip(),
        "species": (obs.get("species") or "").strip(),
        "notes": (obs.get("notes") or "").strip(),
        "source": (obs.get("source") or "").strip(),
        "image_path": obs.get("image_path") if obs.get("image_path") else "",
        "location_query": loc,
        "ebird_region_code": rcode,
        "ebird_region_name": rname,
        "ebird_region_name_cn": rname_cn,
        "ebird_country_code": ccode,
    }


def _open_csv_writer(
    path: Optional[Path],
    *,
    excel_bom: bool,
) -> Tuple[Any, Any]:
    if path is None:
        return sys.stdout, csv.writer(
            sys.stdout,
            lineterminator="\n",
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    f = path.open("w", encoding="utf-8-sig" if excel_bom else "utf-8", newline="")
    return f, csv.writer(f)


def write_observations_csv(
    doc: Dict[str, Any],
    out_path: Optional[Path],
    *,
    excel_bom: bool,
) -> None:
    observations = doc.get("observations") or []
    if not isinstance(observations, list):
        observations = []

    fh: Any
    writer: Any
    fh, writer = _open_csv_writer(out_path, excel_bom=excel_bom)
    close_fh = out_path is not None
    try:
        writer.writerow(OBS_FIELDNAMES)
        for raw in observations:
            if not isinstance(raw, dict):
                continue
            row = _obs_row(doc, raw)
            writer.writerow([row[k] for k in OBS_FIELDNAMES])
    finally:
        if close_fh and fh is not None:
            fh.close()


def write_summary_csv(
    doc: Dict[str, Any],
    out_path: Path,
    *,
    excel_bom: bool,
) -> None:
    observations = doc.get("observations") or []
    if not isinstance(observations, list):
        observations = []

    by_species: Dict[str, List[str]] = {}
    for raw in observations:
        if not isinstance(raw, dict):
            continue
        sp = (raw.get("species") or "").strip()
        if not sp:
            sp = "(empty)"
        t = (raw.get("time_utc") or "").strip()
        by_species.setdefault(sp, []).append(t)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if excel_bom else "utf-8"
    with out_path.open("w", encoding=encoding, newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(SUMMARY_FIELDNAMES)
        for species in sorted(by_species.keys()):
            times = [x for x in by_species[species] if x]
            times.sort()
            first = times[0] if times else ""
            last = times[-1] if times else ""
            w.writerow([species, len(by_species[species]), first, last])


def default_output_path(workspace: Path) -> Path:
    return workspace.resolve() / "workspace" / "bird_sightings_export.csv"


def default_summary_path(main_csv: Path) -> Path:
    return main_csv.with_name(main_csv.stem + "_by_species" + main_csv.suffix)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export bird.json observations to CSV for sharing (e.g. attach or paste).",
        epilog="When called by an agent: absolute path for this script, --workspace, and file outputs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd(),
        help="Absolute path to project root (contains workspace/bird.json)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="",
        help="Absolute CSV path, or '-' for stdout (default: <workspace>/workspace/bird_sightings_export.csv)",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Also write per-species counts (default path: <output_stem>_by_species.csv)",
    )
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=None,
        help="Absolute path for summary CSV (only with --summary)",
    )
    parser.add_argument(
        "--excel",
        action="store_true",
        help="UTF-8 BOM for Excel",
    )
    args = parser.parse_args()
    ws: Path = args.workspace

    bird_path = workspace_bird_path(ws)
    if not bird_path.is_file():
        print(f"error: missing {bird_path}", file=sys.stderr)
        return 2

    doc = load_doc(ws)
    out_arg = (args.output or "").strip()
    if out_arg == "-":
        if args.summary:
            print("error: --summary cannot be used with --output -", file=sys.stderr)
            return 3
        write_observations_csv(doc, None, excel_bom=False)
        print(bird_path, file=sys.stderr)
        return 0

    out_path = Path(out_arg) if out_arg else default_output_path(ws)
    if not out_path.is_absolute():
        out_path = (ws / out_path).resolve()

    write_observations_csv(doc, out_path, excel_bom=args.excel)
    print(str(out_path), file=sys.stderr)

    if args.summary:
        sum_path = args.summary_output
        if sum_path is None:
            sum_path = default_summary_path(out_path)
        elif not sum_path.is_absolute():
            sum_path = (ws / sum_path).resolve()
        write_summary_csv(doc, sum_path, excel_bom=args.excel)
        print(str(sum_path), file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
