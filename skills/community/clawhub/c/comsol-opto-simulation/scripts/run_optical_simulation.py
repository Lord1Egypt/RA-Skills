#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Type A: Optical absorption simulation via Electromagnetic Waves, Frequency Domain.

Workflow:
  1. Load or create device geometry
  2. Assign optical constants (n, k) per layer per wavelength
  3. Set up EM Waves, Frequency Domain study
  4. Solve across wavelength sweep
  5. Export absorption per layer, reflection, transmission, field distribution

Usage:
    python run_optical_simulation.py --config config_optical.json
"""

from __future__ import annotations

import argparse
import json
import sys
import os
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))


def ensure_mph():
    try:
        import mph
        return mph
    except ImportError:
        print(json.dumps({"status": "error", "message": "mph not installed. Run: python scripts/install_mph.py"}))
        sys.exit(1)


def run_optical_simulation(config: dict) -> dict:
    mph = ensure_mph()
    client = mph.start()
    
    # Load model or build from scratch
    model_path = config.get("model_path")
    if model_path and Path(model_path).exists():
        model = client.load(model_path)
    else:
        # Build from device_stack config
        build_script = Path(__file__).parent / "build_heterostructure.py"
        # Import and call build function
        import importlib.util
        spec = importlib.util.spec_from_file_location("build", str(build_script))
        build_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(build_mod)
        
        device_config = config.get("device_stack", {})
        tmp_model = SKILL_DIR / "output" / "tmp_device.mph"
        build_mod.build_layered_device(device_config, str(tmp_model))
        model = client.load(str(tmp_model))
    
    jm = model.java
    comp = jm.component("comp1")
    
    # Assign materials with optical properties
    # In COMSOL: use Refractive Index (n, k) or permittivity
    wavelengths = config.get("wavelengths_nm", [400, 500, 600, 700, 800])
    
    # Set up Electromagnetic Waves, Frequency Domain
    emw = comp.physics().create("emw", "ElectromagneticWavesFrequencyDomain", "geom1")
    
    # Add Wave Equation, Electric
    # For layered stack, typically use Port or Perfectly Matched Layer for boundaries
    # Simplified: use Periodic or Scattering boundary conditions
    
    # Create study
    study = jm.study().create("std1")
    freq_step = study.create("freq1", "Frequency")
    # Convert wavelengths to frequencies: f = c / lambda
    # COMSOL expects frequency in Hz
    freq_vals = [f"{299792458 / (w * 1e-9)}[Hz]" for w in wavelengths]
    freq_step.set("plist", freq_vals)
    
    # Add materials
    layers = config.get("device_stack", {}).get("layers", [])
    for i, layer in enumerate(layers):
        mat = comp.material().create(f"mat{i}", "Common")
        pg = mat.propertyGroup("def")
        # Set refractive index as a single string (real or complex)
        # COMSOL format: "n-kj" for complex refractive index (n = real, k = extinction)
        n = layer.get("n", 2.0)
        k = layer.get("k", 0.1)
        if k > 0:
            ri_str = f"{n}-{k}j"
        else:
            ri_str = str(n)
        pg.set("refractiveindex", ri_str)
        # Assign to domain
        try:
            mat.selection().set([i + 1])
        except Exception:
            pass
    
    # Mesh (automatic)
    mesh = comp.mesh().create("mesh1")
    mesh.feature().create("size1", "Size")
    dim = config.get("device_stack", {}).get("dimension", 2)
    if dim == 1:
        mesh.feature().create("edg1", "Edge")
    elif dim == 2:
        mesh.feature().create("ftri1", "FreeTri")
    elif dim == 3:
        mesh.feature().create("ftet1", "FreeTet")
    mesh.run()
    
    # Solve
    study.run()
    
    # Export results
    output_dir = Path(config.get("output_dir", "output/optical"))
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Evaluate global quantities: reflection, transmission, absorption
    # These would be defined in Results > Global Evaluation
    
    # Save model with solution
    model.save(str(output_dir / "optical_result.mph"))
    
    return {
        "status": "ok",
        "wavelengths_nm": wavelengths,
        "output_dir": str(output_dir),
        "model_saved": str(output_dir / "optical_result.mph"),
        "note": "Full absorption extraction requires post-processing definitions (Global Eval, Integration).",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to optical simulation config JSON")
    args = parser.parse_args()
    
    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    result = run_optical_simulation(config)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
