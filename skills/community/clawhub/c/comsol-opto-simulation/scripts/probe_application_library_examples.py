#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe useful official COMSOL Application Library examples.

The default mode is offline discovery: it locates local .mph examples and
matching Help documents without starting COMSOL or consuming a license.

Use --export-java only when a COMSOL license is available. It loads each
example through mph and saves an exported Model Java file for API inspection.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
VENDOR_SITE = SKILL_DIR / "vendor" / "site-packages"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
if VENDOR_SITE.exists() and str(VENDOR_SITE) not in sys.path:
    sys.path.insert(0, str(VENDOR_SITE))

from discover_comsol_environment import discover  # noqa: E402


@dataclass(frozen=True)
class ExampleSpec:
    key: str
    category: str
    reason: str
    doc_package: str
    mph_names: tuple[str, ...]
    learning_targets: tuple[str, ...]


TARGET_EXAMPLES = (
    ExampleSpec(
        key="gaas_pin_photodiode",
        category="photodetector",
        reason="Closest official photodiode template for Semiconductor + optical generation workflows.",
        doc_package="com.comsol.help.models.semicond.gaas_pin_photodiode",
        mph_names=("gaas_pin_photodiode.mph",),
        learning_targets=(
            "Optical transitions in Semiconductor",
            "Illuminated and dark current comparison",
            "Photodiode postprocessing quantities",
        ),
    ),
    ExampleSpec(
        key="si_solar_cell_1d",
        category="photovoltaic",
        reason="Useful 1D illuminated junction template for generation-current balance and EQE thinking.",
        doc_package="com.comsol.help.models.semicond.si_solar_cell_1d",
        mph_names=("si_solar_cell_1d.mph", "si_solar_cell_1d_basic.mph"),
        learning_targets=(
            "1D absorber transport baseline",
            "Illumination sweep setup",
            "Photocurrent and recombination diagnostics",
        ),
    ),
    ExampleSpec(
        key="reverse_bias_leakage_current",
        category="dark current",
        reason="Directly relevant to detector reverse-bias leakage and detectivity limits.",
        doc_package="com.comsol.help.models.semicond.reverse_bias_leakage_current",
        mph_names=("reverse_bias_leakage_current.mph",),
        learning_targets=(
            "Reverse-bias continuation",
            "Generation-recombination leakage",
            "Breakdown/leakage solver controls",
        ),
    ),
    ExampleSpec(
        key="heterojunction_1d",
        category="heterojunction",
        reason="Band offset and heterointerface reference for configured multi-material transport models.",
        doc_package="com.comsol.help.models.semicond.heterojunction_1d",
        mph_names=("heterojunction_1d.mph",),
        learning_targets=(
            "Electron affinity and band-gap offsets",
            "Interface continuity checks",
            "Equilibrium band diagram validation",
        ),
    ),
    ExampleSpec(
        key="heterojunction_tunneling",
        category="heterojunction",
        reason="Reference for interface transport barriers and tunneling-like leakage paths.",
        doc_package="com.comsol.help.models.semicond.heterojunction_tunneling",
        mph_names=("heterojunction_tunneling.mph",),
        learning_targets=(
            "Interface transport diagnostics",
            "Barrier-limited current",
            "Field-enhanced leakage interpretation",
        ),
    ),
    ExampleSpec(
        key="schottky_contact",
        category="contact",
        reason="Contact barrier template for configured electrode or boundary-condition checks.",
        doc_package="com.comsol.help.models.semicond.schottky_contact",
        mph_names=("schottky_contact.mph",),
        learning_targets=(
            "Metal contact barrier setup",
            "Contact-limited dark current",
            "Work-function sensitivity",
        ),
    ),
    ExampleSpec(
        key="nanowire_traps",
        category="trap states",
        reason="Trap-state workflow reference for configured interface and defect-density studies.",
        doc_package="com.comsol.help.models.semicond.nanowire_traps",
        mph_names=("nanowire_traps.mph",),
        learning_targets=(
            "Trap density parameterization",
            "Hysteresis or transient trap checks",
            "SRH recombination sensitivity",
        ),
    ),
)


def find_first(base: Path, names: Iterable[str]) -> Path | None:
    if not base.exists():
        return None
    wanted = {name.lower() for name in names}
    for path in base.rglob("*"):
        if path.is_file() and path.name.lower() in wanted:
            return path
    return None


def doc_files(doc_root: Path, package: str) -> dict[str, str | None]:
    folder = doc_root / package
    if not folder.exists():
        return {"folder": None, "html": None, "pdf": None}
    html = next(folder.glob("*.html"), None)
    pdf = next(folder.glob("*.pdf"), None)
    return {
        "folder": str(folder),
        "html": str(html) if html else None,
        "pdf": str(pdf) if pdf else None,
    }


def export_java(mph_path: Path, output_dir: Path, cores: int) -> dict[str, object]:
    import mph

    output_dir.mkdir(parents=True, exist_ok=True)
    client = mph.start(cores=cores)
    model = client.load(str(mph_path))
    java_path = output_dir / f"{mph_path.stem}.java"
    model.save(java_path, format="Java")
    info = {
        "status": "ok",
        "java": str(java_path),
        "model_name": model.name(),
        "used_products": model.modules(),
    }
    try:
        client.remove(model)
    except Exception:
        pass
    return info


def probe(args: argparse.Namespace) -> dict[str, object]:
    env = discover(args.root)
    result: dict[str, object] = {
        "environment_status": env.get("status"),
        "install_root": env.get("install_root"),
        "examples": [],
    }
    if env.get("status") != "found":
        return result

    install_root = Path(str(env["install_root"]))
    app_root = install_root / "applications"
    doc_root = Path(str(env["doc_root"]))
    export_dir = args.output_dir or (SKILL_DIR / "output" / "application_library_java")

    for spec in TARGET_EXAMPLES:
        mph_path = find_first(app_root, spec.mph_names)
        docs = doc_files(doc_root, spec.doc_package)
        entry: dict[str, object] = {
            "key": spec.key,
            "category": spec.category,
            "reason": spec.reason,
            "learning_targets": list(spec.learning_targets),
            "mph": str(mph_path) if mph_path else None,
            "docs": docs,
            "status": "found" if mph_path or docs["folder"] else "missing",
        }
        if args.export_java and mph_path:
            try:
                entry["java_export"] = export_java(mph_path, export_dir, args.cores)
            except Exception as exc:
                entry["java_export"] = {"status": "error", "message": str(exc)}
        result["examples"].append(entry)

    found = sum(1 for item in result["examples"] if item["status"] == "found")
    result["summary"] = {
        "found": found,
        "total": len(TARGET_EXAMPLES),
        "java_exported": bool(args.export_java),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, help="Override COMSOL installation root.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON.")
    parser.add_argument("--export-java", action="store_true", help="Load found .mph files and export Model Java.")
    parser.add_argument("--output-dir", type=Path, help="Directory for exported Java files.")
    parser.add_argument("--cores", type=int, default=2, help="COMSOL cores for mph.start when exporting Java.")
    args = parser.parse_args()

    result = probe(args)
    print(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False))
    found = result.get("summary", {}).get("found", 0)
    return 0 if found else 1


if __name__ == "__main__":
    raise SystemExit(main())


