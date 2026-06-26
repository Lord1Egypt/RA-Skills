#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List, Tuple

MAIN_GROUP_Q = {
    "H": 1, "He": 2, "Li": 3, "Be": 4, "B": 3, "C": 4, "N": 5, "O": 6, "F": 7, "Ne": 8,
    "Na": 9, "Mg": 10, "Al": 3, "Si": 4, "P": 5, "S": 6, "Cl": 7, "Ar": 8,
    "K": 9, "Ca": 10, "Br": 7, "I": 7,
}


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_text(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.rstrip() + "\n")


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_xyz(path: str) -> List[Dict[str, Any]]:
    lines = [line.rstrip() for line in read_text(path).splitlines() if line.strip()]
    if len(lines) < 3:
        raise ValueError("XYZ file is too short")
    n_atoms = int(lines[0])
    atoms = []
    for idx, line in enumerate(lines[2:2+n_atoms], start=1):
        parts = line.split()
        if len(parts) < 4:
            raise ValueError(f"Invalid XYZ atom line {idx}: {line}")
        atoms.append({
            "element": parts[0].capitalize(),
            "x": float(parts[1]),
            "y": float(parts[2]),
            "z": float(parts[3]),
        })
    if len(atoms) != n_atoms:
        raise ValueError("XYZ atom count mismatch")
    return atoms


def parse_simple_cell_from_cif(path: str) -> Dict[str, Any]:
    text = read_text(path)
    values = {}
    for key in ["_cell_length_a", "_cell_length_b", "_cell_length_c", "_cell_angle_alpha", "_cell_angle_beta", "_cell_angle_gamma"]:
        for line in text.splitlines():
            if line.strip().startswith(key):
                values[key] = float(line.split()[1])
                break
    needed = ["_cell_length_a", "_cell_length_b", "_cell_length_c", "_cell_angle_alpha", "_cell_angle_beta", "_cell_angle_gamma"]
    if not all(k in values for k in needed):
        raise ValueError("CIF parser could not extract a complete cell")
    return {
        "a": values["_cell_length_a"],
        "b": values["_cell_length_b"],
        "c": values["_cell_length_c"],
        "alpha": values["_cell_angle_alpha"],
        "beta": values["_cell_angle_beta"],
        "gamma": values["_cell_angle_gamma"],
    }


def unique_elements(atoms: List[Dict[str, Any]]) -> List[str]:
    seen = OrderedDict()
    for atom in atoms:
        seen[atom["element"]] = True
    return list(seen.keys())


def potential_for(element: str, xc: str) -> str:
    if xc.upper() != "PBE":
        return f"GTH-{xc.upper()}"
    q = MAIN_GROUP_Q.get(element)
    return f"GTH-PBE-q{q}" if q else "GTH-PBE"


def basis_for(element: str, basis_family: str) -> str:
    return basis_family


def bbox(atoms: List[Dict[str, Any]]) -> Tuple[float, float, float, float, float, float]:
    xs = [a["x"] for a in atoms]
    ys = [a["y"] for a in atoms]
    zs = [a["z"] for a in atoms]
    return min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)


def infer_lengths_from_atoms(atoms: List[Dict[str, Any]], padding: float) -> Tuple[float, float, float]:
    xmin, xmax, ymin, ymax, zmin, zmax = bbox(atoms)
    return (
        round(max(15.0, (xmax - xmin) + 2 * padding), 4),
        round(max(15.0, (ymax - ymin) + 2 * padding), 4),
        round(max(15.0, (zmax - zmin) + 2 * padding), 4),
    )


def format_coord_lines(atoms: List[Dict[str, Any]]) -> str:
    return "\n".join(f"    {a['element']:<2} {a['x']:>14.8f} {a['y']:>14.8f} {a['z']:>14.8f}" for a in atoms)


def format_kind_blocks(elements: List[str], basis_family: str, xc: str) -> str:
    chunks = []
    for e in elements:
        chunks.append(
            "\n".join([
                f"    &KIND {e}",
                f"      BASIS_SET {basis_for(e, basis_family)}",
                f"      POTENTIAL {potential_for(e, xc)}",
                "    &END KIND",
            ])
        )
    return "\n".join(chunks)


def periodic_poisson(periodicity: str) -> str:
    if periodicity == "NONE":
        return "  &POISSON\n    PERIODIC NONE\n    PSOLVER MT\n  &END POISSON"
    return ""


def scf_block(job: Dict[str, Any]) -> str:
    lines = [
        "    &SCF",
        f"      EPS_SCF {job['eps_scf']:.1e}",
        f"      MAX_SCF {job['max_scf']}",
        "      SCF_GUESS ATOMIC",
    ]
    if job["scf_mode"] == "OT":
        lines += [
            "      &OT",
            "        PRECONDITIONER FULL_ALL",
            "        MINIMIZER DIIS",
            "      &END OT",
        ]
    else:
        lines += [
            "      &DIAGONALIZATION ON",
            "      &MIXING",
            "        METHOD BROYDEN_MIXING",
            "        ALPHA 0.2",
            "        NBROYDEN 8",
            "      &END MIXING",
            "      &SMEAR ON",
            "        METHOD FERMI_DIRAC",
            "        ELECTRONIC_TEMPERATURE [K] 300",
            "      &END SMEAR",
        ]
    lines.append("    &END SCF")
    return "\n".join(lines)


def motion_block(job: Dict[str, Any]) -> str:
    task = job["task_type"]
    if task == "geometry_optimization":
        return "\n".join([
            "&MOTION",
            "  &GEO_OPT",
            f"    OPTIMIZER {job['optimizer']}",
            "    MAX_ITER 200",
            "  &END GEO_OPT",
            "&END MOTION",
        ])
    if task == "cell_optimization":
        return "\n".join([
            "&MOTION",
            "  &CELL_OPT",
            "    TYPE DIRECT_CELL_OPT",
            "    MAX_ITER 200",
            "  &END CELL_OPT",
            "&END MOTION",
        ])
    if task == "md":
        md = job["md"]
        return "\n".join([
            "&MOTION",
            "  &MD",
            f"    ENSEMBLE {md['ensemble']}",
            f"    STEPS {md['steps']}",
            f"    TIMESTEP {md['timestep_fs']}",
            f"    TEMPERATURE [K] {md['temperature_k']}",
            "  &END MD",
            "&END MOTION",
        ])
    if task == "vibrational_analysis":
        return "\n".join([
            "&VIBRATIONAL_ANALYSIS",
            "  DX 0.01",
            "&END VIBRATIONAL_ANALYSIS",
        ])
    return ""


def dft_d3_block(job: Dict[str, Any]) -> str:
    if not job.get("dispersion"):
        return ""
    return "\n".join([
        "    &VDW_POTENTIAL",
        "      POTENTIAL_TYPE PAIR_POTENTIAL",
        "      &PAIR_POTENTIAL",
        "        TYPE DFTD3(BJ)",
        "        PARAMETER_FILE_NAME dftd3.dat",
        f"        REFERENCE_FUNCTIONAL {job['xc_functional'].upper()}",
        "      &END PAIR_POTENTIAL",
        "    &END VDW_POTENTIAL",
    ])


def kpoints_block(job: Dict[str, Any]) -> str:
    if job["periodicity"] == "NONE":
        return ""
    grid = " ".join(str(x) for x in job["kpoints_grid"])
    return f"    &KPOINTS\n      SCHEME MONKHORST-PACK {grid}\n    &END KPOINTS"


def cell_block(job: Dict[str, Any], structure_path: str, atoms: List[Dict[str, Any]] | None) -> str:
    fmt = job.get("structure_format")
    if job["periodicity"] == "NONE":
        if not atoms:
            raise ValueError("Non-periodic automatic cell construction requires coordinate atoms")
        a, b, c = infer_lengths_from_atoms(atoms, float(job.get("vacuum_padding_ang", 10.0)))
        return "\n".join([
            "    &CELL",
            f"      A {a} 0.0 0.0",
            f"      B 0.0 {b} 0.0",
            f"      C 0.0 0.0 {c}",
            "      PERIODIC NONE",
            "    &END CELL",
        ])
    if fmt == "cif":
        cell = parse_simple_cell_from_cif(structure_path)
        return "\n".join([
            "    &CELL",
            f"      ABC {cell['a']} {cell['b']} {cell['c']}",
            f"      ALPHA_BETA_GAMMA {cell['alpha']} {cell['beta']} {cell['gamma']}",
            f"      PERIODIC {job['periodicity']}",
            "    &END CELL",
        ])
    return "\n".join([
        "    &CELL",
        f"      PERIODIC {job['periodicity']}",
        "    &END CELL",
    ])


def coord_or_topology_block(job: Dict[str, Any], structure_path: str, atoms: List[Dict[str, Any]] | None) -> str:
    if atoms:
        return "\n".join([
            "    &COORD",
            format_coord_lines(atoms),
            "    &END COORD",
        ])
    return "\n".join([
        "    &TOPOLOGY",
        f"      COORD_FILE_NAME {Path(structure_path).name}",
        f"      COORD_FILE_FORMAT {job.get('structure_format', 'UNKNOWN').upper()}",
        "    &END TOPOLOGY",
    ])


def render(job: Dict[str, Any], structure_path: str) -> str:
    fmt = (job.get("structure_format") or os.path.splitext(structure_path)[1].lstrip(".")).lower()
    atoms = parse_xyz(structure_path) if fmt == "xyz" else None
    project_name = Path(job.get("structure_file") or structure_path).stem or "cp2k_job"

    if atoms:
        kinds_block = format_kind_blocks(unique_elements(atoms), job['basis_family'], job['xc_functional'])
    else:
        kinds_block = ""
        notes = job.setdefault("notes", [])
        review = job.setdefault("review_required", [])
        warning = f"Deterministic KIND generation was skipped because structure format '{fmt or 'unknown'}' is not parsed into explicit elements by the renderer"
        if warning not in notes:
            notes.append(warning)
        if "renderer_needs_external_kind_resolution" not in review:
            review.append("renderer_needs_external_kind_resolution")

    sections = [
        "&GLOBAL",
        f"  PROJECT {project_name}",
        f"  RUN_TYPE {job['run_type']}",
        "  PRINT_LEVEL MEDIUM",
        "&END GLOBAL",
        "",
        "&FORCE_EVAL",
        "  METHOD QS",
        "  &DFT",
        f"    BASIS_SET_FILE_NAME BASIS_MOLOPT",
        f"    POTENTIAL_FILE_NAME GTH_POTENTIALS",
        f"    CHARGE {job['charge']}",
        f"    MULTIPLICITY {job['multiplicity']}",
    ]
    if job.get("uks"):
        sections.append("    UKS TRUE")
    sections += [
        periodic_poisson(job['periodicity']),
        "    &QS",
        "      METHOD GPW",
        "    &END QS",
        scf_block(job),
        "    &MGRID",
        f"      CUTOFF {job['cutoff']}",
        f"      REL_CUTOFF {job['rel_cutoff']}",
        "    &END MGRID",
        "    &XC",
        "      &XC_FUNCTIONAL",
        f"        &{job['xc_functional'].upper()}\n        &END {job['xc_functional'].upper()}",
        "      &END XC_FUNCTIONAL",
        dft_d3_block(job),
        "    &END XC",
        kpoints_block(job),
        "  &END DFT",
        "  &SUBSYS",
        cell_block(job, structure_path, atoms),
        coord_or_topology_block(job, structure_path, atoms),
        kinds_block,
        "  &END SUBSYS",
        "&END FORCE_EVAL",
        motion_block(job),
    ]
    return "\n".join(s for s in sections if s != "") + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Render a CP2K input draft from a normalized job spec")
    p.add_argument("job_spec_json")
    p.add_argument("structure_file")
    p.add_argument("-o", "--output", default="job.inp")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    try:
        job = load_json(args.job_spec_json)
        rendered = render(job, args.structure_file)
        write_text(args.output, rendered)
    except Exception as e:
        print(f"Error while rendering CP2K input: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"CP2K input written to: {args.output}")


if __name__ == "__main__":
    main()
