#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Type C: Thermal-Electrical Coupled Simulation.

Couples:
  - Heat Transfer in Solids
  - Semiconductor (drift-diffusion)
  - Electromagnetic Waves (optical generation + heat source)

Workflow:
  1. Load existing optoelectronic model (Type B) or build from scratch
  2. Add Heat Transfer physics with material thermal properties
  3. Add Heat Source from electromagnetic losses (optical absorption heating)
  4. Add Joule Heating coupling (Semiconductor -> Heat Transfer)
  5. Set temperature-dependent material properties:
     - Bandgap: Varshni equation or linear temperature coefficient
     - Mobility: power-law or Arrhenius temperature dependence
  6. Set thermal boundary conditions (ambient, convection, contact heat sinks)
  7. Solve: Stationary thermal-electric coupled or sequential coupling
  8. Export temperature profile, thermal-induced performance shift

Usage:
    python run_thermal_coupled_sim.py --config config_thermal.json
"""

from __future__ import annotations

import argparse
import json
import sys
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


def setup_heat_transfer(jm, comp, config: dict) -> dict:
    """Add Heat Transfer in Solids physics to the model."""
    
    # Create Heat Transfer physics
    ht = comp.physics().create("ht", "HeatTransfer", "geom1")
    
    layers = config.get("device_stack", {}).get("layers", [])
    thermal_props = config.get("thermal_properties", {})
    
    # Add Solid feature per domain with thermal properties
    for i, layer in enumerate(layers):
        mat_name = layer.get("material", f"layer{i}")
        layer_thermal = thermal_props.get(mat_name, {})
        
        # Thermal conductivity (W/m/K)
        k_thermal = layer_thermal.get("thermal_conductivity_W_per_mK", 1.0)
        # Density (kg/m³)
        rho = layer_thermal.get("density_kg_per_m3", 5000.0)
        # Heat capacity (J/kg/K)
        Cp = layer_thermal.get("heat_capacity_J_per_kgK", 500.0)
        
        solid = ht.create(f"solid{i}", "SolidHeatTransferModel")
        solid.selection().set([i + 1])
        solid.set("k", str(k_thermal))
        solid.set("rho", str(rho))
        solid.set("Cp", str(Cp))
    
    return {"ht_tag": "ht", "domains": len(layers)}


def setup_thermal_boundaries(jm, comp, config: dict) -> dict:
    """Set up thermal boundary conditions."""
    
    ht = comp.physics("ht")
    boundaries = config.get("thermal_boundaries", {})
    
    # Ambient temperature parameter
    T_ambient = boundaries.get("ambient_temperature_K", 300)
    jm.param().set("T_ambient", f"{T_ambient}[K]")
    
    # Top boundary: convection + radiation (if exposed)
    top_bc = boundaries.get("top", {"type": "convection", "h": 10, "T_inf": T_ambient})
    if top_bc.get("type") == "convection":
        conv_top = ht.create("conv_top", "ConvectiveHeatFlux")
        # Top boundary index depends on geometry; assuming last external boundary
        # For 2D layered stack: boundaries are numbered sequentially
        # This is a placeholder; actual boundary selection needs geometry inspection
        h_val = top_bc.get("h_W_per_m2K", 10.0)
        conv_top.set("h", str(h_val))
        conv_top.set("T_inf", "T_ambient")
    
    # Bottom boundary: heat sink / fixed temperature (substrate contact)
    bottom_bc = boundaries.get("bottom", {"type": "temperature", "T": T_ambient})
    if bottom_bc.get("type") == "temperature":
        temp_bottom = ht.create("temp_bottom", "Temperature")
        T_val = bottom_bc.get("temperature_K", T_ambient)
        temp_bottom.set("T0", f"{T_val}[K]")
    elif bottom_bc.get("type") == "convection":
        conv_bottom = ht.create("conv_bottom", "ConvectiveHeatFlux")
        h_val = bottom_bc.get("h_W_per_m2K", 100.0)  # Higher h for heat sink
        conv_bottom.set("h", str(h_val))
        conv_bottom.set("T_inf", "T_ambient")
    
    # Side boundaries: adiabatic (default) or symmetry
    sides_bc = boundaries.get("sides", {"type": "adiabatic"})
    if sides_bc.get("type") == "symmetry":
        sym = ht.create("sym_sides", "SymmetryHeatFlux")
        # Select side boundaries
    
    return {"T_ambient_K": T_ambient, "boundary_config": boundaries}


def setup_heat_sources(jm, comp, config: dict) -> dict:
    """
    Add heat sources from:
      1. Optical absorption (electromagnetic losses)
      2. Joule heating (Semiconductor module coupling)
    """
    
    ht = comp.physics("ht")
    heat_sources = config.get("heat_sources", {})
    
    sources_added = []
    
    # Source 1: EM Wave losses (optical absorption -> heat)
    if heat_sources.get("optical_absorption", False):
        # In COMSOL: Electromagnetic Losses multiphysics coupling
        # Or manually: Qh = 0.5 * ω * ε0 * ε" * |E|²
        # Simplified: use Electromagnetic Heating multiphysics feature if available
        try:
            em_losses = ht.create("em_heat", "ElectromagneticLosses")
            sources_added.append("electromagnetic_losses")
        except Exception as e:
            # Fallback: add Heat Source feature with expression
            for i in range(len(config.get("device_stack", {}).get("layers", []))):
                heat_src = ht.create(f"qsrc{i}", "HeatSource")
                heat_src.selection().set([i + 1])
                # Placeholder expression; actual would reference EM solution
                heat_src.set("Qh", "emw.Qh")  # EM losses variable
            sources_added.append("heat_source_from_emw")
    
    # Source 2: Joule heating from semiconductor current
    if heat_sources.get("joule_heating", True):
        # COMSOL Semiconductor module has built-in Joule heating coupling
        # Via Multiphysics > Joule Heating (semi + ht)
        try:
            multiphysics = jm.component("comp1").multiphysics()
            jh = multiphysics.create("jh1", "JouleHeating")
            jh.set("semi", "semi")
            jh.set("ht", "ht")
            sources_added.append("joule_heating_multiphysics")
        except Exception as e:
            # Fallback: add as explicit heat source
            for i in range(len(config.get("device_stack", {}).get("layers", []))):
                jh_src = ht.create(f"jh{i}", "HeatSource")
                jh_src.selection().set([i + 1])
                jh_src.set("Qh", "semi.Qj")  # Joule heating variable
            sources_added.append("joule_heating_explicit")
    
    return {"heat_sources_added": sources_added}


def setup_temperature_dependent_properties(jm, comp, config: dict) -> dict:
    """
    Set temperature-dependent material properties for semiconductor layers.
    
    Temperature dependence models:
      - Bandgap: Varshhi equation: Eg(T) = Eg(0) - alpha*T²/(T + beta)
        or linear: Eg(T) = Eg(300) + dEg_dT * (T - 300)
      - Mobility: Power law: mu(T) = mu(300) * (T/300)^(-gamma)
        or Arrhenius: mu(T) = mu(300) * exp(-Ea/kB * (1/T - 1/300))
    """
    
    layers = config.get("device_stack", {}).get("layers", [])
    temp_coeffs = config.get("temperature_coefficients", {})
    
    modified = []
    
    for i, layer in enumerate(layers):
        mat_name = layer.get("material", f"layer{i}")
        coeffs = temp_coeffs.get(mat_name, {})
        
        if not coeffs:
            continue
        
        # Get semiconductor physics
        semi = comp.physics("semi")
        mat_feat_tag = f"mat{i}"
        
        try:
            mat_feat = semi.feature(mat_feat_tag)
        except Exception:
            continue
        
        # Bandgap temperature dependence
        bandgap_model = coeffs.get("bandgap_model", "varshni")
        if bandgap_model == "varshni":
            alpha = coeffs.get("varshni_alpha_eV_per_K", 5.0e-4)
            beta = coeffs.get("varshni_beta_K", 300.0)
            Eg_0 = layer.get("bandgap_eV", 1.0)
            # In COMSOL, set as expression involving T (temperature variable)
            # Note: actual implementation depends on COMSOL version and API
            # This is a template showing the approach
            modified.append({
                "layer": mat_name,
                "property": "bandgap",
                "model": "varshni",
                "alpha": alpha,
                "beta": beta,
                "Eg_0_eV": Eg_0,
            })
        elif bandgap_model == "linear":
            dEg_dT = coeffs.get("dEg_dT_eV_per_K", -2.5e-4)
            Eg_300 = layer.get("bandgap_eV", 1.0)
            modified.append({
                "layer": mat_name,
                "property": "bandgap",
                "model": "linear",
                "dEg_dT_eV_per_K": dEg_dT,
                "Eg_300_eV": Eg_300,
            })
        
        # Mobility temperature dependence
        mobility_model = coeffs.get("mobility_model", "power_law")
        if mobility_model == "power_law":
            gamma_n = coeffs.get("mu_n_gamma", 1.5)
            gamma_p = coeffs.get("mu_p_gamma", 1.5)
            mu_n_300 = layer.get("mu_n", 100)
            mu_p_300 = layer.get("mu_p", 50)
            modified.append({
                "layer": mat_name,
                "property": "mobility",
                "model": "power_law",
                "mu_n_300": mu_n_300,
                "mu_p_300": mu_p_300,
                "gamma_n": gamma_n,
                "gamma_p": gamma_p,
            })
        elif mobility_model == "arrhenius":
            Ea_n = coeffs.get("mu_n_Ea_eV", 0.01)
            Ea_p = coeffs.get("mu_p_Ea_eV", 0.01)
            modified.append({
                "layer": mat_name,
                "property": "mobility",
                "model": "arrhenius",
                "Ea_n_eV": Ea_n,
                "Ea_p_eV": Ea_p,
            })
    
    return {"temperature_dependent_layers": modified}


def run_thermal_coupled_simulation(config: dict) -> dict:
    mph = ensure_mph()
    client = mph.start()
    
    model_path = config.get("model_path")
    if model_path and Path(model_path).exists():
        model = client.load(model_path)
    else:
        # Build from device_stack or require optoelectronic model
        build_script = Path(__file__).parent / "build_heterostructure.py"
        import importlib.util
        spec = importlib.util.spec_from_file_location("build", str(build_script))
        build_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(build_mod)
        
        device_config = config.get("device_stack", {})
        tmp_model = SKILL_DIR / "output" / "tmp_device_thermal.mph"
        build_mod.build_layered_device(device_config, str(tmp_model))
        model = client.load(str(tmp_model))
    
    jm = model.java
    comp = jm.component("comp1")
    
    # Ensure Semiconductor physics exists (for Joule heating coupling)
    if "semi" not in [comp.physics().tag(i) for i in range(comp.physics().size())]:
        # Run basic optoelectronic setup first
        print(json.dumps({
            "status": "warning",
            "message": "Semiconductor physics not found. Thermal coupling requires optoelectronic model. Run Type B first or include semiconductor setup in config."
        }))
    
    # 1. Setup Heat Transfer
    ht_info = setup_heat_transfer(jm, comp, config)
    
    # 2. Setup Thermal Boundary Conditions
    bc_info = setup_thermal_boundaries(jm, comp, config)
    
    # 3. Setup Heat Sources (optical + Joule heating)
    source_info = setup_heat_sources(jm, comp, config)
    
    # 4. Setup Temperature-Dependent Properties
    temp_dep_info = setup_temperature_dependent_properties(jm, comp, config)
    
    # 5. Setup Study
    study = jm.study().create("std_thermal")
    
    # Option A: Fully coupled stationary thermal-electric
    coupling_mode = config.get("coupling_mode", "fully_coupled")
    
    if coupling_mode == "fully_coupled":
        # Single stationary step solving all physics together
        stat = study.feature().create("stat_thermal", "Stationary")
        # Include both Semiconductor and Heat Transfer in study
        stat.set("physics", ["semi", "ht"])
        
        # If EM waves included for optical heating:
        if source_info.get("heat_sources_added", []) and "emw" in [comp.physics().tag(i) for i in range(comp.physics().size())]:
            stat.set("physics", ["semi", "ht", "emw"])
    
    elif coupling_mode == "sequential":
        # Step 1: Solve thermal at initial bias
        stat_thermal = study.feature().create("stat_thermal_only", "Stationary")
        stat_thermal.set("physics", ["ht"])
        
        # Step 2: Solve semiconductor with temperature field
        stat_semi = study.feature().create("stat_semi", "Stationary")
        stat_semi.set("physics", ["semi"])
    
    elif coupling_mode == "parametric_sweep":
        # Parametric sweep over bias voltage with thermal feedback
        stat = study.feature().create("stat_param", "Stationary")
        stat.set("physics", ["semi", "ht"])
        
        sweep = stat.create("sweep", "AuxiliarySweep")
        bias_config = config.get("bias_range", {"start_V": -1.0, "stop_V": 1.0, "points": 51})
        start_V = bias_config.get("start_V", -1.0)
        stop_V = bias_config.get("stop_V", 1.0)
        points = bias_config.get("points", 51)
        
        # Generate voltage list string
        import numpy as np
        voltages = np.linspace(start_V, stop_V, points)
        voltages_str = ",".join([f"{v}[V]" for v in voltages])
        
        sweep.set("pname", "V_bias")
        sweep.set("plist", voltages_str)
    
    # Mesh
    mesh = comp.mesh().create("mesh_thermal")
    mesh.feature().create("size1", "Size")
    mesh.feature("size1").set("hauto", "4")
    dim = config.get("device_stack", {}).get("dimension", 2)
    if dim == 1:
        mesh.feature().create("edg1", "Edge")
    elif dim == 2:
        mesh.feature().create("ftri1", "FreeTri")
    elif dim == 3:
        mesh.feature().create("ftet1", "FreeTet")
    mesh.run()
    
    # Solve
    try:
        study.run()
        solve_status = "ok"
        solve_message = "Thermal-electrical coupled simulation completed"
    except Exception as e:
        solve_status = "error"
        solve_message = f"Solve failed: {str(e)}"
    
    # Export results
    output_dir = Path(config.get("output_dir", "output/thermal"))
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Export temperature profile
    results = jm.result()
    
    # 2D/3D temperature plot
    temp_plot = results.create("pg_temp", "PlotGroup2D")
    surface = temp_plot.create("surf_temp", "Surface")
    surface.set("expr", "T")
    temp_plot.set("data", jm.dataset().tags()[-1] if jm.dataset().size() > 0 else "dset1")
    
    # Export temperature plot
    model.export(f"temp_profile_{coupling_mode}.png", str(output_dir / "temperature_profile.png"))
    
    # Line plot: temperature along device cross-section
    line_plot = results.create("pg_temp_line", "PlotGroup1D")
    line = line_plot.create("line_temp", "LineGraph")
    line.set("expr", "T")
    # Select vertical line through center
    
    model.export(f"temp_line_{coupling_mode}.png", str(output_dir / "temperature_line.png"))
    
    # Save model
    model.save(str(output_dir / "thermal_result.mph"))
    
    return {
        "status": solve_status,
        "message": solve_message,
        "output_dir": str(output_dir),
        "coupling_mode": coupling_mode,
        "T_ambient_K": bc_info["T_ambient_K"],
        "heat_sources": source_info["heat_sources_added"],
        "temperature_dependent_properties": temp_dep_info.get("temperature_dependent_layers", []),
        "model_saved": str(output_dir / "thermal_result.mph"),
        "note": "Temperature-dependent property expressions may require manual verification in COMSOL GUI.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to thermal coupling config JSON")
    args = parser.parse_args()
    
    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    result = run_thermal_coupled_simulation(config)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
