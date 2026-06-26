#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from copy import deepcopy
from typing import Any, Dict, List, Optional

TASK_KEYWORDS = {
    "geometry_optimization": ["optimize", "optimise", "optimization", "optimisation", "relax", "geo_opt", "几何优化", "结构优化", "弛豫"],
    "cell_optimization": ["cell opt", "cell_opt", "lattice", "晶格", "晶胞优化", "晶格优化"],
    "single_point": ["single point", "single-point", "energy", "单点", "单点能"],
    "md": ["md", "molecular dynamics", "动力学", "温度", "nvt", "nve", "npt"],
    "vibrational_analysis": ["frequency", "frequencies", "vibration", "vibrational", "normal mode", "振动", "频率"],
}

RUN_TYPE_MAP = {
    "geometry_optimization": "GEO_OPT",
    "cell_optimization": "CELL_OPT",
    "single_point": "ENERGY",
    "md": "MD",
    "vibrational_analysis": "VIBRATIONAL_ANALYSIS",
    "unknown": "ENERGY",
}

MAIN_GROUP_Q = {
    "H": 1, "He": 2, "Li": 3, "Be": 4, "B": 3, "C": 4, "N": 5, "O": 6, "F": 7, "Ne": 8,
    "Na": 9, "Mg": 10, "Al": 3, "Si": 4, "P": 5, "S": 6, "Cl": 7, "Ar": 8,
    "K": 9, "Ca": 10, "Br": 7, "I": 7,
}

TRANSITION_METALS = {
    "Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn",
    "Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd",
    "Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg",
}


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(data: Dict[str, Any], path: Optional[str] = None) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    else:
        print(text)


def get_ext(filename: Optional[str]) -> str:
    return os.path.splitext(filename or "")[1].lower().lstrip(".")


def ensure_list(value: Any) -> List[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def default_job_spec() -> Dict[str, Any]:
    return {
        "task_type": "unknown",
        "run_type": "ENERGY",
        "system_type": "unknown",
        "structure_file": None,
        "structure_format": None,
        "periodicity": "unknown",
        "charge": 0,
        "multiplicity": 1,
        "uks": False,
        "priority": "balanced",
        "xc_functional": "PBE",
        "basis_family": "DZVP-MOLOPT-SR-GTH",
        "potential_family": "GTH-PBE",
        "scf_mode": "OT",
        "kpoints_scheme": "GAMMA",
        "kpoints_grid": [1, 1, 1],
        "dispersion": False,
        "cell_handling": "auto",
        "cell_vectors": None,
        "vacuum_padding_ang": 10.0,
        "cutoff": 500,
        "rel_cutoff": 60,
        "eps_scf": 1e-6,
        "max_scf": 100,
        "optimizer": "BFGS",
        "md": {
            "ensemble": None,
            "temperature_k": None,
            "timestep_fs": None,
            "steps": None,
        },
        "hardware": {
            "type": "unknown",
            "cores": None,
            "memory_gb": None,
        },
        "notes": [],
        "defaults_applied": [],
        "review_required": [],
    }


def infer_task_type(raw: Dict[str, Any], defaults: List[str], notes: List[str]) -> str:
    explicit = raw.get("task_type")
    if isinstance(explicit, str) and explicit:
        task = explicit.strip().lower()
        aliases = {
            "geo_opt": "geometry_optimization",
            "geometry optimization": "geometry_optimization",
            "cell_opt": "cell_optimization",
            "cell optimization": "cell_optimization",
            "energy": "single_point",
        }
        return aliases.get(task, task)

    text = " ".join(str(raw.get(k, "")) for k in ["request", "prompt", "description", "task", "user_text"]).lower()
    for task, keywords in TASK_KEYWORDS.items():
        if any(k in text for k in keywords):
            defaults.append(f"Inferred task_type={task} from natural-language request")
            return task

    defaults.append("Defaulted task_type=single_point because the request did not clearly specify a workflow")
    return "single_point"


def infer_system_type(raw: Dict[str, Any], structure_file: Optional[str], defaults: List[str], review: List[str]) -> str:
    explicit = raw.get("system_type")
    if isinstance(explicit, str) and explicit.strip():
        return explicit.strip().lower()

    ext = get_ext(structure_file)
    if ext in {"xyz", "pdb", "mol", "sdf"}:
        defaults.append(f"Inferred system_type=molecule from .{ext} structure file")
        return "molecule"
    if ext in {"cif", "cell", "poscar", "vasp"}:
        defaults.append(f"Inferred system_type=crystal from .{ext} structure file")
        return "crystal"

    text = " ".join(str(raw.get(k, "")) for k in ["request", "prompt", "description", "task", "user_text"]).lower()
    if any(k in text for k in ["surface", "slab", "adsorption", "monolayer", "2d"]):
        defaults.append("Inferred system_type=surface from natural-language request")
        return "surface"
    if any(k in text for k in ["crystal", "bulk", "solid", "晶体", "材料"]):
        defaults.append("Inferred system_type=crystal from natural-language request")
        review.append("confirm_periodic_structure")
        return "crystal"

    defaults.append("Defaulted system_type=molecule because no periodic cues were found")
    return "molecule"


def infer_periodicity(system_type: str, structure_format: Optional[str], defaults: List[str], review: List[str]) -> str:
    if system_type == "molecule":
        defaults.append("Set periodicity=NONE for molecular treatment")
        return "NONE"
    if system_type == "surface":
        defaults.append("Set periodicity=XY for slab/2D treatment")
        return "XY"
    if system_type == "crystal":
        defaults.append("Set periodicity=XYZ for bulk periodic treatment")
        if structure_format == "xyz":
            review.append("xyz_used_for_periodic_system")
        return "XYZ"
    review.append("periodicity_uncertain")
    return "unknown"


def infer_priority(raw: Dict[str, Any], defaults: List[str]) -> str:
    explicit = raw.get("priority")
    if explicit in {"fast", "balanced", "high"}:
        return explicit
    text = " ".join(str(raw.get(k, "")) for k in ["request", "prompt", "description", "task", "user_text"]).lower()
    if any(k in text for k in ["fast", "quick", "screen", "粗算", "快一点"]):
        defaults.append("Inferred priority=fast from user wording")
        return "fast"
    if any(k in text for k in ["accurate", "tight", "publication", "高精度", "更精确"]):
        defaults.append("Inferred priority=high from user wording")
        return "high"
    defaults.append("Applied priority=balanced by default")
    return "balanced"


def apply_priority(job: Dict[str, Any]) -> None:
    p = job["priority"]
    if p == "fast":
        job.update({"cutoff": 400, "rel_cutoff": 40, "eps_scf": 1e-5, "max_scf": 80})
    elif p == "high":
        job.update({"cutoff": 700, "rel_cutoff": 80, "eps_scf": 1e-7, "max_scf": 150, "basis_family": "TZVP-MOLOPT-SR-GTH"})
    else:
        job.update({"cutoff": 500, "rel_cutoff": 60, "eps_scf": 1e-6, "max_scf": 100})


def infer_xc(raw: Dict[str, Any], defaults: List[str]) -> str:
    explicit = raw.get("xc_functional")
    if isinstance(explicit, str) and explicit.strip():
        return explicit.strip().upper()
    defaults.append("Defaulted xc_functional=PBE")
    return "PBE"


def infer_spin(job: Dict[str, Any], raw: Dict[str, Any], defaults: List[str], review: List[str], notes: List[str]) -> None:
    charge = raw.get("charge")
    multiplicity = raw.get("multiplicity")
    if isinstance(charge, int):
        job["charge"] = charge
    else:
        defaults.append("Defaulted charge=0")

    if isinstance(multiplicity, int) and multiplicity >= 1:
        job["multiplicity"] = multiplicity
    else:
        text = " ".join(str(raw.get(k, "")) for k in ["request", "prompt", "description", "task", "user_text"]).lower()
        if any(k in text for k in ["radical", "triplet", "doublet", "magnetic", "spin", "open-shell"]):
            review.append("spin_state_uncertain")
            notes.append("Open-shell cues were detected but multiplicity was not explicitly provided")
        defaults.append("Defaulted multiplicity=1")

    job["uks"] = bool(job["multiplicity"] > 1)
    if job["uks"]:
        defaults.append("Enabled UKS because multiplicity > 1")


def infer_dispersion(job: Dict[str, Any], raw: Dict[str, Any], defaults: List[str], review: List[str]) -> None:
    explicit = raw.get("dispersion")
    if isinstance(explicit, bool):
        job["dispersion"] = explicit
        return
    text = " ".join(str(raw.get(k, "")) for k in ["request", "prompt", "description", "task", "user_text"]).lower()
    if any(k in text for k in ["adsorption", "physisorption", "vdw", "van der waals", "layered", "molecular crystal", "interface"]):
        job["dispersion"] = True
        defaults.append("Enabled dispersion by heuristic because the request suggests vdW-sensitive physics")
        review.append("dispersion_heuristic")


def infer_scf_and_kpoints(job: Dict[str, Any], raw: Dict[str, Any], defaults: List[str], review: List[str]) -> None:
    text = " ".join(str(raw.get(k, "")) for k in ["request", "prompt", "description", "task", "user_text"]).lower()
    if job["periodicity"] == "NONE":
        job["scf_mode"] = "OT"
        job["kpoints_scheme"] = "GAMMA"
        job["kpoints_grid"] = [1, 1, 1]
        job["cell_handling"] = "auto_vacuum_box"
        return

    metallic_cue = any(k in text for k in ["metal", "metallic", "ni", "fe", "co", "cu", "pt", "au", "pd"])
    if metallic_cue:
        job["scf_mode"] = "DIAGONALIZATION"
        defaults.append("Selected diagonalization SCF because metallic cues were detected")
    else:
        job["scf_mode"] = "DIAGONALIZATION"
        defaults.append("Selected diagonalization SCF for periodic treatment")

    if job["periodicity"] == "XYZ":
        job["kpoints_scheme"] = "MONKHORST_PACK"
        job["kpoints_grid"] = [4, 4, 4]
    elif job["periodicity"] == "XY":
        job["kpoints_scheme"] = "MONKHORST_PACK"
        job["kpoints_grid"] = [6, 6, 1]
    review.append("kpoints_are_heuristic")
    job["cell_handling"] = "use_input_cell"


def infer_basis_and_potential(job: Dict[str, Any], raw: Dict[str, Any], defaults: List[str], review: List[str]) -> None:
    if isinstance(raw.get("basis_family"), str) and raw["basis_family"].strip():
        job["basis_family"] = raw["basis_family"].strip()
    if isinstance(raw.get("potential_family"), str) and raw["potential_family"].strip():
        job["potential_family"] = raw["potential_family"].strip()
    if job["priority"] == "high" and raw.get("basis_family") is None:
        defaults.append("Promoted basis_family to TZVP-MOLOPT-SR-GTH for high-priority mode")

    elements = [e.capitalize() for e in ensure_list(raw.get("elements")) if isinstance(e, str)]
    if any(e in TRANSITION_METALS for e in elements):
        review.append("transition_metal_library_resolution")
        defaults.append("Kept potential_family as GTH-PBE placeholder for transition-metal library resolution")


def infer_md(job: Dict[str, Any], raw: Dict[str, Any], defaults: List[str]) -> None:
    if job["task_type"] != "md":
        return
    md = deepcopy(job["md"])
    raw_md = raw.get("md") if isinstance(raw.get("md"), dict) else {}
    text = " ".join(str(raw.get(k, "")) for k in ["request", "prompt", "description", "task", "user_text"]).lower()
    md["ensemble"] = raw_md.get("ensemble") or ("NVT" if "nve" not in text and "npt" not in text else ("NVE" if "nve" in text else "NPT_F"))
    md["temperature_k"] = raw_md.get("temperature_k") or 300
    md["steps"] = raw_md.get("steps") or 5000
    md["timestep_fs"] = raw_md.get("timestep_fs") or 0.5
    defaults.append("Applied short-test MD defaults for ensemble/temperature/steps/timestep where missing")
    job["md"] = md


def normalize_request(raw: Dict[str, Any]) -> Dict[str, Any]:
    job = default_job_spec()
    defaults = ensure_list(raw.get("defaults_applied"))
    notes = ensure_list(raw.get("notes"))
    review = ensure_list(raw.get("review_required"))

    structure_file = raw.get("structure_file")
    job["structure_file"] = structure_file
    job["structure_format"] = get_ext(structure_file) or None

    job["task_type"] = infer_task_type(raw, defaults, notes)
    job["run_type"] = RUN_TYPE_MAP.get(job["task_type"], "ENERGY")
    job["system_type"] = infer_system_type(raw, structure_file, defaults, review)
    job["periodicity"] = raw.get("periodicity") or infer_periodicity(job["system_type"], job["structure_format"], defaults, review)
    job["priority"] = infer_priority(raw, defaults)
    job["xc_functional"] = infer_xc(raw, defaults)
    apply_priority(job)
    infer_spin(job, raw, defaults, review, notes)
    infer_dispersion(job, raw, defaults, review)
    infer_scf_and_kpoints(job, raw, defaults, review)
    infer_basis_and_potential(job, raw, defaults, review)
    infer_md(job, raw, defaults)

    if isinstance(raw.get("vacuum_padding_ang"), (int, float)):
        job["vacuum_padding_ang"] = float(raw["vacuum_padding_ang"])
    if isinstance(raw.get("hardware"), dict):
        job["hardware"].update({k: raw["hardware"].get(k) for k in ["type", "cores", "memory_gb"] if k in raw["hardware"]})

    if job["task_type"] == "cell_optimization" and job["system_type"] == "molecule":
        review.append("cell_optimization_on_molecule")
        notes.append("CELL_OPT is unusual for an isolated molecule")
    if job["task_type"] == "vibrational_analysis":
        defaults.append("Tight vibrational workflows should start from a well-optimized stationary structure")
    if job["structure_file"] is None:
        review.append("missing_structure_file")
        notes.append("No structure file was provided; deterministic rendering needs a structure file")

    job["notes"] = notes
    job["defaults_applied"] = defaults
    job["review_required"] = sorted(set(review))
    return job


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Normalize a raw CP2K request JSON into the standard job spec")
    p.add_argument("input_json")
    p.add_argument("-o", "--output", default=None)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    try:
        raw = load_json(args.input_json)
        normalized = normalize_request(raw)
    except FileNotFoundError:
        print(f"Error: file not found: {args.input_json}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    dump_json(normalized, args.output)


if __name__ == "__main__":
    main()
