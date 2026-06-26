#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Type B: Optoelectronic I-V and photocurrent simulation via Semiconductor + EM coupling.

Workflow:
  1. Load device geometry with materials (and mapping.json if available)
  2. Set up Semiconductor module (drift-diffusion) with full material properties
  3. Import optical generation rate from Type A (or compute inline)
  4. Set up Study: Stationary + Auxiliary sweep for I-V
  5. Solve for I-V at dark and under illumination
  6. Export I-V curves, EQE, band diagram, carrier distributions

Usage:
    python run_optoelectronic_sim.py --config config_opto.json
"""

from __future__ import annotations

import argparse
import copy
from datetime import datetime
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


def load_mapping(config: dict) -> dict | None:
    """Try to load geometry mapping from .mapping.json alongside the model."""
    model_path = config.get("model_path")
    if not model_path:
        return None
    mapping_path = Path(model_path).with_suffix(".mapping.json")
    if not mapping_path.exists():
        alt = Path(str(mapping_path) + ".mapping.json")
        if alt.exists():
            mapping_path = alt
        else:
            return None
    with open(mapping_path, "r", encoding="utf-8") as f:
        return json.load(f)


def set_userdef(feature, key: str, value: str) -> None:
    """Set a Semiconductor feature value and force COMSOL to use it."""
    mat_key = f"{key}_mat"
    try:
        feature.set(mat_key, "userdef")
    except Exception:
        pass
    feature.set(key, value)


def set_selection(feature, entity) -> None:
    if isinstance(entity, list):
        feature.selection().set([int(x) for x in entity])
    else:
        feature.selection().set([int(entity)])


def add_analytic_doping(semi, tag: str, domain_idx, dopant_type: str, concentration: float, setup_log: dict) -> None:
    """Add explicit Semiconductor analytic doping; material properties alone are not enough."""
    if concentration <= 0:
        return
    try:
        dop = semi.create(tag, "AnalyticDopingModel")
        set_selection(dop, domain_idx)
        dop.set("FeatureType", "Doping")
        dop.set("impurityType", dopant_type)
        if dopant_type == "donor":
            dop.set("NDc", f"{concentration}[1/cm^3]")
        else:
            dop.set("NAc", f"{concentration}[1/cm^3]")
        setup_log.setdefault("doping_models", []).append({
            "tag": tag,
            "domain": domain_idx,
            "type": dopant_type,
            "concentration_cm3": concentration,
        })
    except Exception as e:
        setup_log["errors"].append(f"{tag} analytic doping failed: {e}")


def should_apply_doping(layer: dict, config: dict) -> bool:
    role = layer.get("role", "").lower()
    if "absorber" in role:
        return True
    if "transport" in role or "buffer" in role:
        return bool(config.get("enable_transport_doping", False))
    if "electrode" in role:
        return bool(config.get("enable_electrode_doping", False))
    return bool(config.get("enable_other_layer_doping", False))


def semiconductor_device_config(config: dict) -> dict:
    device_config = copy.deepcopy(config.get("device_stack", {}))
    if config.get("exclude_electrode_domains", True):
        layers = device_config.get("layers", [])
        device_config["layers"] = [
            layer for layer in layers
            if "electrode" not in layer.get("role", "").lower()
        ]
    return device_config


def is_transport_or_intermediate_layer(layer: dict) -> bool:
    """Identify configurable non-absorber semiconductor layers by role, not by a fixed material stack."""
    role = layer.get("role", "").lower()
    if layer.get("active_transport_regularized"):
        return True
    return any(term in role for term in ("transport", "buffer", "intermediate", "functional"))


def absorber_core_config(config: dict) -> dict:
    """Keep only absorber layers for a numerically robust electrical core model."""
    fallback = copy.deepcopy(config)
    fallback["model_path"] = None
    fallback["output_dir"] = str(Path(config.get("output_dir", "output/optoelectronic")).with_name(
        Path(config.get("output_dir", "output/optoelectronic")).name + "_absorber_core"
    ))
    device_config = copy.deepcopy(config.get("device_stack", {}))
    device_config["layers"] = [
        layer for layer in device_config.get("layers", [])
        if "absorber" in layer.get("role", "").lower()
    ]
    fallback["device_stack"] = device_config
    fallback["electrical_model"] = "absorber_core"
    fallback["fallback_reason"] = (
        "The configured full stack is numerically stiff under bias; non-absorber transport, interface, "
        "or contact layers are treated as boundary/contact layers for this first I-V solve."
    )
    return fallback


def transport_passive_full_geometry_config(config: dict) -> dict:
    """Keep full non-electrode geometry, but solve drift-diffusion only in absorber domains."""
    fallback = copy.deepcopy(config)
    fallback["model_path"] = None
    fallback["output_dir"] = str(Path(config.get("output_dir", "output/optoelectronic")).with_name(
        Path(config.get("output_dir", "output/optoelectronic")).name + "_transport_passive"
    ))
    fallback["electrical_model"] = "transport_passive_full_geometry"
    fallback["semiconductor_active_roles"] = ["absorber"]
    fallback["selective_contact_at_active_stack"] = True
    fallback["fallback_reason"] = (
        "Configured transport/interface layers are retained in the geometry but treated as passive layers; "
        "drift-diffusion is solved only in layers whose role includes absorber."
    )
    return fallback


def active_transport_regularized_config(config: dict) -> dict:
    """Keep configured transport/intermediate layers active with regularized parameters and adaptive continuation."""
    fallback = copy.deepcopy(config)
    fallback["model_path"] = None
    fallback["output_dir"] = str(Path(config.get("output_dir", "output/optoelectronic")).with_name(
        Path(config.get("output_dir", "output/optoelectronic")).name + "_active_transport"
    ))
    fallback["electrical_model"] = "active_transport_regularized"
    fallback["enable_transport_doping"] = True
    fallback["fallback_to_transport_passive"] = False
    fallback["fallback_to_absorber_core"] = False
    fallback["solve_strategy"] = "adaptive_continuation"
    fallback["mesh_auto_size"] = fallback.get("mesh_auto_size", 3)
    fallback["continuation_initial_step_V"] = fallback.get("continuation_initial_step_V", 1e-4)
    fallback["continuation_step_V"] = fallback.get("continuation_step_V", 5e-4)
    fallback["continuation_step_switch_V"] = fallback.get("continuation_step_switch_V", 5e-3)
    target = float(fallback.get("active_transport_target_V", 0.05))
    fallback["bias_range"] = {"start_V": 0.0, "stop_V": target, "points": int(round(target / 5e-4)) + 1}
    for layer in fallback.get("device_stack", {}).get("layers", []):
        if is_transport_or_intermediate_layer(layer):
            layer["Na"] = 0
            layer["Nd"] = fallback.get("active_transport_Nd_cm3", layer.get("Nd", 1e15))
            layer["mu_n"] = fallback.get("active_transport_mu_n", layer.get("mu_n", 0.1))
            layer["mu_p"] = fallback.get("active_transport_mu_p", layer.get("mu_p", 0.001))
    fallback["fallback_reason"] = (
        "Configured transport/intermediate layers remain active Semiconductor domains; the fallback uses regularized "
        "carrier parameters, fine mesh, and adaptive voltage continuation to reduce high-field divergence."
    )
    return fallback


def should_try_absorber_core_fallback(config: dict, solve_status: str) -> bool:
    if not config.get("fallback_to_absorber_core", True):
        return False
    if config.get("electrical_model") == "absorber_core":
        return False
    if "bias sweep failed" not in solve_status and "0 V solved" not in solve_status:
        return False
    layers = config.get("device_stack", {}).get("layers", [])
    absorber_layers = [layer for layer in layers if "absorber" in layer.get("role", "").lower()]
    return 0 < len(absorber_layers) < len(layers)


def should_try_transport_passive_fallback(config: dict, solve_status: str) -> bool:
    if not config.get("fallback_to_transport_passive", True):
        return False
    if config.get("electrical_model") in {"transport_passive_full_geometry", "absorber_core"}:
        return False
    if "bias sweep failed" not in solve_status and "0 V solved" not in solve_status:
        return False
    layers = semiconductor_device_config(config).get("layers", [])
    has_absorber = any("absorber" in layer.get("role", "").lower() for layer in layers)
    has_transport = any(
        "transport" in layer.get("role", "").lower() or "buffer" in layer.get("role", "").lower()
        for layer in layers
    )
    return has_absorber and has_transport


def should_try_active_transport_fallback(config: dict, solve_status: str) -> bool:
    if not config.get("fallback_to_active_transport", False):
        return False
    if config.get("electrical_model") in {
        "active_transport_regularized",
        "transport_passive_full_geometry",
        "absorber_core",
    }:
        return False
    if "bias sweep failed" not in solve_status and "0 V solved" not in solve_status:
        return False
    layers = semiconductor_device_config(config).get("layers", [])
    has_absorber = any("absorber" in layer.get("role", "").lower() for layer in layers)
    has_transport = any(is_transport_or_intermediate_layer(layer) for layer in layers)
    return has_absorber and has_transport


def save_model_safely(model, target: Path) -> tuple[str, list[str]]:
    """Save model, falling back to a timestamped filename if COMSOL locks the target."""
    warnings = []
    try:
        model.save(str(target))
        return str(target), warnings
    except Exception as e:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fallback = target.with_name(f"{target.stem}_{timestamp}{target.suffix}")
        warnings.append(f"primary save failed for {target}: {e}")
        model.save(str(fallback))
        warnings.append(f"saved to fallback path {fallback}")
        return str(fallback), warnings


def layer_matches_active_roles(layer: dict, active_roles: list[str]) -> bool:
    role = layer.get("role", "").lower()
    return any(active_role.lower() in role for active_role in active_roles)


def create_horizontal_boundary_selection(comp, tag: str, y_nm: float, width_nm: float, tolerance_nm: float = 1.0) -> None:
    """Create a component Box selection for a horizontal boundary at y = y_nm."""
    from jpype import JInt

    sel = comp.selection().create(tag, "Box")
    sel.set("xmin", "0[nm]")
    sel.set("xmax", f"{width_nm}[nm]")
    sel.set("ymin", f"{y_nm - tolerance_nm}[nm]")
    sel.set("ymax", f"{y_nm + tolerance_nm}[nm]")
    sel.set("condition", "inside")
    sel.set("entitydim", JInt(1))


def safe_tag(text: str) -> str:
    import re
    return re.sub(r"[^0-9A-Za-z_]+", "_", text)


def try_set_feature(feature, key: str, value, log: list[dict]) -> None:
    try:
        feature.set(key, value)
        log.append({"set": key, "value": value})
    except Exception as e:
        log.append({"set_error": key, "value": value, "message": str(e)[:180]})


def layer_interface_y_nm(layers: list[dict], upper: str, lower: str) -> float | None:
    y_bottom = 0.0
    for i, layer in enumerate(layers[:-1]):
        y_top = y_bottom + float(layer.get("thickness_nm", 0.0))
        next_layer = layers[i + 1]
        if layer.get("name") == upper and next_layer.get("name") == lower:
            return y_top
        y_bottom = y_top
    return None


def apply_metal_contact_transport(contact, name: str, config: dict, setup_log: dict) -> None:
    """Apply Schottky/contact-resistance settings to a metal contact when requested."""
    contact_cfg = config.get("external_contact_transport", {}).get(name, {})
    if not contact_cfg:
        return

    log: list[dict] = []
    if "contact_type" in contact_cfg:
        try_set_feature(contact, "ContactType", contact_cfg["contact_type"], log)
    if contact_cfg.get("weak_constraints", True):
        try_set_feature(contact, "constraintOptions", "weakConstraints", log)
        try_set_feature(contact, "constraintMethod", "elemental", log)
    if "specify_using" in contact_cfg:
        try_set_feature(contact, "SpecifyUsing", contact_cfg["specify_using"], log)
    if "barrier_height_eV" in contact_cfg:
        try_set_feature(contact, "SpecifyBarrierHeight", "userdef", log)
        try_set_feature(contact, "Phi_B", f"{contact_cfg['barrier_height_eV']}[eV]", log)
    if "work_function_eV" in contact_cfg:
        try_set_feature(contact, "Phi", f"{contact_cfg['work_function_eV']}[eV]", log)
    if "rho_c_ohm_m2" in contact_cfg:
        try_set_feature(contact, "ContactResistance", "1", log)
        try_set_feature(contact, "rho_c", f"{contact_cfg['rho_c_ohm_m2']}[ohm*m^2]", log)
    if "extraElectronCurrent" in contact_cfg:
        try_set_feature(contact, "extraElectronCurrent", contact_cfg["extraElectronCurrent"], log)
    if "extraHoleCurrent" in contact_cfg:
        try_set_feature(contact, "extraHoleCurrent", contact_cfg["extraHoleCurrent"], log)
    setup_log.setdefault("external_contact_transport", []).append({"contact": name, "settings": log})


def apply_interface_transport_models(semi, comp, config: dict, mapping: dict | None, setup_log: dict) -> None:
    """Add calibrated heterointerface continuity/tunneling models on layer boundaries."""
    iface_cfg = config.get("interface_transport", {})
    if not iface_cfg.get("enabled", False):
        return

    layers = config.get("device_stack", {}).get("layers", [])
    width_nm = config.get("device_stack", {}).get("device_width_nm", 1000)
    default_cfg = iface_cfg.get("default", {})
    interfaces = iface_cfg.get("interfaces", [])

    if iface_cfg.get("use_default_continuity", False):
        settings_log: list[dict] = []
        try:
            cont = semi.feature("cont1")
            for key in [
                "constraintOptions",
                "constraintMethod",
                "HeteroModelSelection",
                "ContinuationType",
                "extraElectronCurrent",
                "extraHoleCurrent",
                "nJn_int",
                "nJp_int",
                "delta_nJn",
                "delta_nJp",
            ]:
                if key in default_cfg:
                    try_set_feature(cont, key, default_cfg[key], settings_log)
            setup_log.setdefault("interface_transport", []).append({
                "tag": "cont1",
                "model": iface_cfg.get("model", "global_calibrated_default_continuity"),
                "scope": "all_internal_semiconductor_interfaces",
                "settings": settings_log,
            })
        except Exception as e:
            setup_log.setdefault("errors", []).append(f"default continuity calibration failed: {e}")

        for interface in interfaces:
            between = interface.get("between", [])
            y_nm = layer_interface_y_nm(layers, between[0], between[1]) if len(between) == 2 else None
            setup_log.setdefault("interface_transport_calibration", []).append({
                "between": between,
                "y_nm": y_nm,
                "model": interface.get("model"),
                "rho_int_ohm_m2": interface.get("rho_int_ohm_m2"),
                "electron_barrier_eV": interface.get("electron_barrier_eV"),
                "hole_barrier_eV": interface.get("hole_barrier_eV"),
                "note": "calibration metadata; COMSOL default cont1 carries the active weak/WKB transport settings",
            })
        return

    if iface_cfg.get("deactivate_default_continuity", True):
        try:
            semi.feature("cont1").active(False)
            setup_log.setdefault("interface_transport", []).append({
                "tag": "cont1",
                "status": "deactivated_default_continuity",
            })
        except Exception as e:
            setup_log.setdefault("errors", []).append(f"default continuity deactivation failed: {e}")

    if not interfaces:
        interfaces = [
            {"between": [layers[i]["name"], layers[i + 1]["name"]]}
            for i in range(len(layers) - 1)
        ]

    for idx, interface in enumerate(interfaces):
        between = interface.get("between", [])
        if len(between) != 2:
            setup_log.setdefault("errors", []).append(f"interface entry {idx} has invalid between={between}")
            continue
        upper, lower = between
        y_nm = layer_interface_y_nm(layers, upper, lower)
        if y_nm is None:
            setup_log.setdefault("errors", []).append(f"interface {upper}/{lower} not found in adjacent layer stack")
            continue

        sel_tag = interface.get("selection_tag", f"sel_if_{safe_tag(upper)}_{safe_tag(lower)}")
        try:
            create_horizontal_boundary_selection(
                comp,
                sel_tag,
                y_nm,
                width_nm,
                float(interface.get("tolerance_nm", iface_cfg.get("selection_tolerance_nm", 1.0))),
            )
        except Exception as e:
            setup_log.setdefault("errors", []).append(f"interface selection {sel_tag} creation failed: {e}")
            continue

        tag = interface.get("tag", f"cont_if_{idx}_{safe_tag(upper)}_{safe_tag(lower)}")
        try:
            cont = semi.create(tag, "Continuity")
            cont.selection().named(sel_tag)
        except Exception as e:
            setup_log.setdefault("errors", []).append(f"interface continuity {tag} creation failed: {e}")
            continue

        merged = copy.deepcopy(default_cfg)
        merged.update(interface)
        settings_log: list[dict] = []
        for key in [
            "constraintOptions",
            "constraintMethod",
            "HeteroModelSelection",
            "ContinuationType",
            "extraElectronCurrent",
            "extraHoleCurrent",
            "nJn_int",
            "nJp_int",
            "delta_nJn",
            "delta_nJp",
        ]:
            if key in merged:
                try_set_feature(cont, key, merged[key], settings_log)

        setup_log.setdefault("interface_transport", []).append({
            "tag": tag,
            "between": [upper, lower],
            "selection": sel_tag,
            "y_nm": y_nm,
            "model": merged.get("model", "continuity_wkb_or_user_defined"),
            "rho_int_ohm_m2": merged.get("rho_int_ohm_m2"),
            "electron_barrier_eV": merged.get("electron_barrier_eV"),
            "hole_barrier_eV": merged.get("hole_barrier_eV"),
            "settings": settings_log,
        })


def apply_selective_semiconductor_domains(semi, comp, config: dict, mapping: dict | None, setup_log: dict) -> None:
    """Restrict Semiconductor physics to active layers and move contacts to active-stack edges."""
    active_roles = config.get("semiconductor_active_roles")
    if not active_roles:
        return

    layers = config.get("device_stack", {}).get("layers", [])
    width_nm = config.get("device_stack", {}).get("device_width_nm", 1000)
    active_domain_indices = []
    active_layer_indices = []
    y_bottom = 0.0
    layer_bounds = []
    for i, layer in enumerate(layers):
        thickness = float(layer.get("thickness_nm", 0.0))
        y_top = y_bottom + thickness
        domain_idx = None
        if mapping and "domains" in mapping:
            domain_idx = mapping["domains"].get(layer["name"])
        if domain_idx is None:
            domain_idx = i + 1
        layer_bounds.append((y_bottom, y_top, domain_idx))
        if layer_matches_active_roles(layer, active_roles):
            active_domain_indices.append(int(domain_idx))
            active_layer_indices.append(i)
        y_bottom = y_top

    if not active_domain_indices:
        setup_log.setdefault("errors", []).append(f"no active semiconductor domains matched roles {active_roles}")
        return

    try:
        semi.selection().set(active_domain_indices)
        setup_log["semi_domain_selection"] = active_domain_indices
    except Exception as e:
        setup_log.setdefault("errors", []).append(f"semi domain selection failed: {e}")

    for i, _layer in enumerate(layers):
        if i in active_layer_indices:
            continue
        for tag in (f"mat{i}", f"srh{i}", f"dop_donor{i}", f"dop_acceptor{i}"):
            try:
                semi.feature(tag).active(False)
                setup_log.setdefault("deactivated_features", []).append(tag)
            except Exception:
                pass

    if not config.get("selective_contact_at_active_stack", False):
        return

    first_active = active_layer_indices[0]
    last_active = active_layer_indices[-1]
    bottom_y = layer_bounds[first_active][0]
    top_y = layer_bounds[last_active][1]

    try:
        if first_active == 0:
            semi.feature("bottom_contact").selection().named("sel_bottom")
            setup_log["bottom_contact_selection"] = "sel_bottom"
        else:
            tag = "sel_active_bottom_contact"
            create_horizontal_boundary_selection(comp, tag, bottom_y, width_nm)
            semi.feature("bottom_contact").selection().named(tag)
            setup_log["bottom_contact_selection"] = tag
    except Exception as e:
        setup_log.setdefault("errors", []).append(f"active bottom contact selection failed: {e}")

    try:
        if last_active == len(layers) - 1:
            semi.feature("top_contact").selection().named("sel_top")
            setup_log["top_contact_selection"] = "sel_top"
        else:
            tag = "sel_active_top_contact"
            create_horizontal_boundary_selection(comp, tag, top_y, width_nm)
            semi.feature("top_contact").selection().named(tag)
            setup_log["top_contact_selection"] = tag
    except Exception as e:
        setup_log.setdefault("errors", []).append(f"active top contact selection failed: {e}")


def ensure_mesh_generator(mesh, dim: int, log: dict) -> None:
    """A Size node only controls element size; it does not generate a mesh."""
    try:
        if dim == 1:
            mesh.feature().create("edg1", "Edge")
            log.setdefault("mesh_features", []).append("Edge")
        elif dim == 2:
            mesh.feature().create("ftri1", "FreeTri")
            log.setdefault("mesh_features", []).append("FreeTri")
        elif dim == 3:
            mesh.feature().create("ftet1", "FreeTet")
            log.setdefault("mesh_features", []).append("FreeTet")
    except Exception as e:
        log.setdefault("mesh_errors", []).append(f"mesh generator creation failed: {e}")


def solver_dof(jm) -> int | None:
    import re
    try:
        message = str(jm.sol("sol1").feature("s1").getString("message"))
    except Exception:
        return None
    match = re.search(r"自由度数：(\d+)", message)
    if match:
        return int(match.group(1))
    match = re.search(r"degrees of freedom:\s*(\d+)", message, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def segmented_voltage_path(start_V: float, stop_V: float, points: int) -> list[float]:
    """Order requested voltages from 0 V outward to improve nonlinear continuation."""
    import numpy as np

    voltages = [float(v) for v in np.linspace(start_V, stop_V, points)]
    if not any(abs(v) < 1e-15 for v in voltages):
        voltages.append(0.0)
    unique = sorted(set(round(v, 12) for v in voltages), key=lambda v: (abs(v), v < 0, v))
    return [float(v) for v in unique]


def adaptive_voltage_path(start_V: float, stop_V: float, initial_step: float, coarse_step: float, switch_V: float) -> list[float]:
    """Build a conservative path that starts from 0 V and moves outward in small steps."""
    path = [0.0]

    def extend_to(target: float) -> None:
        sign = 1.0 if target >= 0 else -1.0
        current = 0.0
        while abs(current - target) > 1e-15:
            step = initial_step if abs(current) < abs(switch_V) else coarse_step
            next_value = current + sign * step
            if (sign > 0 and next_value > target) or (sign < 0 and next_value < target):
                next_value = target
            rounded = round(next_value, 12)
            if rounded not in path:
                path.append(rounded)
            current = next_value

    if stop_V >= 0:
        extend_to(stop_V)
    if start_V < 0:
        extend_to(start_V)
    return [float(v) for v in path]


def tune_fully_coupled_solver(jm) -> list[dict]:
    """Relax the generated Fully Coupled nonlinear solver for active ETL continuation."""
    log = []
    try:
        fc = jm.sol("sol1").feature("s1").feature("fc1")
    except Exception as e:
        return [{"tune_error": str(e)}]
    for key, value in [
        ("maxiter", "150"),
        ("dtech", "ddog"),
        ("minstep", "1e-9"),
        ("damp", "1"),
        ("ntolfact", "100"),
    ]:
        try:
            fc.set(key, value)
            log.append({"set": key, "value": value})
        except Exception as e:
            log.append({"set_error": key, "message": str(e)[:160]})
    return log


def run_adaptive_continuation(jm, study, start_V: float, stop_V: float, config: dict) -> dict:
    """Run active-transport continuation with small near-zero steps."""
    initial_step = float(config.get("continuation_initial_step_V", 1e-4))
    coarse_step = float(config.get("continuation_step_V", 5e-4))
    switch_V = float(config.get("continuation_step_switch_V", 5e-3))
    steps = []
    tune_log = []
    for index, voltage in enumerate(adaptive_voltage_path(start_V, stop_V, initial_step, coarse_step, switch_V)):
        jm.param().set("V_bias", f"{voltage}[V]")
        try:
            study.run()
            if index == 0:
                tune_log = tune_fully_coupled_solver(jm)
            steps.append({"V": voltage, "status": "ok", "dof": solver_dof(jm)})
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "failed_voltage_V": voltage,
                "dof": solver_dof(jm),
                "steps": steps,
                "solver_tuning": tune_log,
            }
    return {"status": "ok", "dof": solver_dof(jm), "steps": steps, "solver_tuning": tune_log}


def run_segmented_continuation(jm, study, start_V: float, stop_V: float, points: int) -> dict:
    """Fallback solver path: remove Parametric node and run requested bias points one by one."""
    log = []
    try:
        study.feature().remove("param1")
    except Exception:
        pass

    for voltage in segmented_voltage_path(start_V, stop_V, points):
        jm.param().set("V_bias", f"{voltage}[V]")
        try:
            study.run()
            log.append({"V": voltage, "status": "ok", "dof": solver_dof(jm)})
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "failed_voltage_V": voltage,
                "dof": solver_dof(jm),
                "steps": log,
            }

    return {"status": "ok", "dof": solver_dof(jm), "steps": log}


def setup_semiconductor_physics(jm, comp, config: dict, mapping: dict | None) -> dict:
    """
    Configure Semiconductor physics with full material properties.
    """
    semi = comp.physics().create("semi", "Semiconductor", "geom1")

    layers = config.get("device_stack", {}).get("layers", [])
    n_layers = len(layers)

    setup_log = {"material_models": [], "errors": []}

    # ----------------------------------------------------------------
    # 0. Create Materials per layer (electronaffinity, bandgap, doping, permittivity)
    # ----------------------------------------------------------------
    for i, layer in enumerate(layers):
        domain_idx = None
        if mapping and "domains" in mapping:
            domain_idx = mapping["domains"].get(layer["name"])
        if domain_idx is None:
            domain_idx = i + 1

        mat_tag = f"mat_layer{i}"
        try:
            mat = comp.material().create(mat_tag, "Common")
            set_selection(mat, domain_idx)
            pg = mat.propertyGroup("def")

            # Electron affinity (eV)
            chi = layer.get("electron_affinity_eV", 4.0)
            pg.set("electronaffinity", f"{chi}[eV]")

            # Bandgap (eV)
            Eg = layer.get("bandgap_eV", 1.0)
            pg.set("bandgap", f"{Eg}[eV]")

            # Relative permittivity
            eps_r = layer.get("epsilon_r", 10.0)
            pg.set("relpermittivity", str(eps_r))

            # Doping concentrations in material
            Nd = layer.get("Nd", 0.0)
            Na = layer.get("Na", 0.0)
            if Nd > 0:
                pg.set("donor_concentration", f"{Nd}[1/cm^3]")
            if Na > 0:
                pg.set("acceptor_concentration", f"{Na}[1/cm^3]")
        except Exception as e:
            setup_log["errors"].append(f"material {mat_tag} creation failed: {e}")

    # ----------------------------------------------------------------
    # 1. Semiconductor Material Model per layer
    # ----------------------------------------------------------------
    for i, layer in enumerate(layers):
        tag = f"mat{i}"
        mm = semi.create(tag, "SemiconductorMaterialModel")

        domain_idx = None
        if mapping and "domains" in mapping:
            domain_idx = mapping["domains"].get(layer["name"])
        if domain_idx is None:
            domain_idx = i + 1

        try:
            set_selection(mm, domain_idx)
        except Exception as e:
            setup_log["errors"].append(f"mat{i} selection failed: {e}")

        # Bandgap (eV)
        Eg = layer.get("bandgap_eV", 1.0)
        set_userdef(mm, "Eg0", f"{Eg}[eV]")

        # Electron affinity (eV) - COMSOL uses lowercase chi0
        chi = layer.get("electron_affinity_eV", 4.0)
        try:
            set_userdef(mm, "chi0", f"{chi}[eV]")
        except Exception:
            setup_log["errors"].append(f"mat{i} chi0 set failed")

        # Mobility
        mu_n = layer.get("mu_n", 100.0)
        mu_p = layer.get("mu_p", 100.0)
        set_userdef(mm, "mun", f"{mu_n}[cm^2/(V*s)]")
        set_userdef(mm, "mup", f"{mu_p}[cm^2/(V*s)]")

        # Effective density of states
        Nc = layer.get("Nc_cm3", 1e19)
        Nv = layer.get("Nv_cm3", 1e19)
        set_userdef(mm, "Nc", f"{Nc}[1/cm^3]")
        set_userdef(mm, "Nv", f"{Nv}[1/cm^3]")

        # Permittivity
        eps_r = layer.get("epsilon_r", 10.0)
        set_userdef(mm, "epsilonr", str(eps_r))

        Nd = layer.get("Nd", 0.0)
        Na = layer.get("Na", 0.0)
        layer["_Nd"] = Nd
        layer["_Na"] = Na
        if should_apply_doping(layer, config):
            add_analytic_doping(semi, f"dop_donor{i}", domain_idx, "donor", Nd, setup_log)
            add_analytic_doping(semi, f"dop_acceptor{i}", domain_idx, "acceptor", Na, setup_log)
        elif Nd > 0 or Na > 0:
            setup_log.setdefault("skipped_doping", []).append({
                "layer": layer["name"],
                "domain": domain_idx,
                "Nd_cm3": Nd,
                "Na_cm3": Na,
                "reason": "doping disabled for non-absorber layer by default",
            })
        try:
            mm.set("minput_numberdensitydonor_src", "userdef")
            mm.set("minput_numberdensitydonor", f"{Nd}[1/cm^3]")
            mm.set("minput_numberdensityacceptor_src", "userdef")
            mm.set("minput_numberdensityacceptor", f"{Na}[1/cm^3]")
        except Exception as e:
            setup_log["errors"].append(f"mat{i} model-input doping failed: {e}")

        setup_log["material_models"].append({
            "tag": tag,
            "layer": layer["name"],
            "domain": domain_idx,
            "Eg_eV": Eg,
            "Chi_eV": chi,
            "mu_n": mu_n,
            "mu_p": mu_p,
        })

    # ----------------------------------------------------------------
    # 2. Recombination: Trap-Assisted (SRH equivalent)
    # ----------------------------------------------------------------
    for i, layer in enumerate(layers):
        tau_n = layer.get("tau_n", 1e-9)
        tau_p = layer.get("tau_p", 1e-9)

        domain_idx = None
        if mapping and "domains" in mapping:
            domain_idx = mapping["domains"].get(layer["name"])
        if domain_idx is None:
            domain_idx = i + 1

        # Only add recombination for semiconductor layers (absorbers / transport)
        role = layer.get("role", "").lower()
        if "electrode" in role:
            continue  # Skip electrodes

        try:
            srh = semi.create(f"srh{i}", "TrapAssistedRecombination")
            set_selection(srh, domain_idx)
            set_userdef(srh, "taun", f"{tau_n}[s]")
            set_userdef(srh, "taup", f"{tau_p}[s]")
        except Exception as e:
            setup_log["errors"].append(f"srh{i} creation failed: {e}")

    # ----------------------------------------------------------------
    # 3. Metal Contacts (ohmic) - top and bottom
    # ----------------------------------------------------------------
    top_bc = None
    bottom_bc = None
    if mapping and "contacts" in mapping:
        top_bc = mapping["contacts"].get("top")
        bottom_bc = mapping["contacts"].get("bottom")

    top_contact = semi.create("top_contact", "MetalContact")
    top_contact.set("V0", "V_bias")
    top_contact.set("ContactType", "ohmic")
    apply_metal_contact_transport(top_contact, "top", config, setup_log)

    bottom_contact = semi.create("bottom_contact", "MetalContact")
    bottom_contact.set("V0", "0[V]")
    bottom_contact.set("ContactType", "ohmic")
    apply_metal_contact_transport(bottom_contact, "bottom", config, setup_log)

    # Apply boundary selections from mapping
    if mapping and "contacts" in mapping:
        top_info = mapping["contacts"].get("top", {})
        bottom_info = mapping["contacts"].get("bottom", {})
        boundaries_info = mapping.get("boundaries", {})
        
        # Apply top contact boundary selection
        top_sel_tag = top_info.get("selection_tag")
        if top_sel_tag:
            try:
                top_contact.selection().named(top_sel_tag)
                setup_log["top_contact_selection"] = top_sel_tag
            except Exception as e:
                setup_log["errors"].append(f"top_contact selection failed: {e}")
        
        # Apply bottom contact boundary selection
        bottom_sel_tag = bottom_info.get("selection_tag")
        if bottom_sel_tag:
            try:
                bottom_contact.selection().named(bottom_sel_tag)
                setup_log["bottom_contact_selection"] = bottom_sel_tag
            except Exception as e:
                setup_log["errors"].append(f"bottom_contact selection failed: {e}")
        
        # The Semiconductor interface already creates a default Insulation node.
        # The historical `sel_sides` Box selection also catches top/bottom
        # boundaries in this layered geometry, so adding another insulation
        # feature here can overlap the metal contacts and destabilize the solve.
        sides_sel_tag = boundaries_info.get("sides", {}).get("selection_tag")
        if sides_sel_tag:
            setup_log["insulation_selection"] = "default_insulation_only"
    else:
        setup_log["errors"].append("No mapping found for boundary selections; MetalContact may fail.")

    apply_interface_transport_models(semi, comp, config, mapping, setup_log)
    apply_selective_semiconductor_domains(semi, comp, config, mapping, setup_log)

    return {"physics_tag": "semi", "setup_log": setup_log}


def setup_optical_generation(jm, comp, config: dict) -> dict:
    """
    Add optical generation rate G_opt to the semiconductor model.
    """
    opt_gen = config.get("optical_generation", {})
    source = opt_gen.get("source", "analytic")

    if source == "from_optical_sim":
        file_path = opt_gen.get("file", "")
        if Path(file_path).exists():
            return {"status": "placeholder", "note": f"Import from {file_path} requires COMSOL solution coupling."}
        return {"status": "error", "message": f"Optical sim file not found: {file_path}"}

    elif source == "analytic":
        wavelength_nm = opt_gen.get("wavelength_nm", 550)
        intensity = opt_gen.get("intensity", "1000[W/m^2]")
        return {"status": "ok", "model": "beer_lambert", "wavelength_nm": wavelength_nm, "intensity": intensity}

    elif source == "uniform":
        G_val = opt_gen.get("G_uniform", 1e21)
        return {"status": "ok", "model": "uniform", "G": G_val}

    return {"status": "error", "message": f"Unknown optical_generation source: {source}"}


def setup_study_and_solve(jm, comp, config: dict) -> dict:
    """Create study, mesh, and solve."""
    output_dir = Path(config.get("output_dir", "output/optoelectronic"))
    output_dir.mkdir(parents=True, exist_ok=True)

    # --- Study ---
    study = jm.study().create("std1")
    stat = study.feature().create("stat1", "Stationary")

    # Bias sweep
    bias_cfg = config.get("bias_range", {})
    start_V = bias_cfg.get("start_V", -1.0)
    stop_V = bias_cfg.get("stop_V", 1.0)
    points = bias_cfg.get("points", 51)

    jm.param().set("V_bias", "0[V]")

    mesh_log = {"mesh_features": [], "mesh_errors": []}

    # --- Mesh ---
    mesh = comp.mesh().create("mesh1")
    layers = config.get("device_stack", {}).get("layers", [])
    all_hmax = config.get("mesh_hmax_nm_all_semiconductor")
    if all_hmax:
        size_all = mesh.feature().create("size_all", "Size")
        size_all.set("custom", "on")
        size_all.set("hmax", f"{all_hmax}[nm]")
        try:
            size_all.selection().geom("geom1", 2)
            size_all.selection().set(list(range(1, len(layers) + 1)))
        except Exception:
            pass
    else:
        semiconductor_domains = []
        for i, layer in enumerate(layers):
            role = layer.get("role", "").lower()
            if "absorber" in role or "active" in role:
                semiconductor_domains.append(i + 1)

        if semiconductor_domains:
            size_feat = mesh.feature().create("size1", "Size")
            size_feat.set("custom", "on")
            size_feat.set("hmax", "5[nm]")
            try:
                size_feat.selection().geom("geom1", 2)
                size_feat.selection().set(semiconductor_domains)
            except Exception:
                pass

        mesh.feature().create("size2", "Size")
        mesh.feature("size2").set("hauto", str(config.get("mesh_auto_size", 4)))
    dim = config.get("device_stack", {}).get("dimension", 2)
    ensure_mesh_generator(mesh, dim, mesh_log)
    mesh.run()

    if config.get("solve_strategy") == "adaptive_continuation":
        adaptive = run_adaptive_continuation(jm, study, start_V, stop_V, config)
        solve_status = "ok" if adaptive.get("status") == "ok" else f"error: adaptive continuation failed: {adaptive.get('message')}"
        return {
            "solve_status": solve_status,
            "output_dir": str(output_dir),
            "bias_points": len(adaptive.get("steps", [])),
            "dof": adaptive.get("dof"),
            "mesh_log": mesh_log,
            "solve_log": [{"stage": "adaptive_bias_continuation", **adaptive}],
        }

    # --- Solve: first build a stable 0 V solution, then optionally continue with bias sweep.
    solve_status = "unknown"
    solve_log = []
    dof = None
    try:
        study.run()
        dof = solver_dof(jm)
        if dof == 0:
            solve_status = "error: COMSOL generated 0 degrees of freedom; mesh/physics activation failed"
        else:
            solve_status = "ok"
            solve_log.append({"stage": "single_point_0V", "status": "ok", "dof": dof})
    except Exception as e:
        solve_status = f"error: {e}"
        dof = solver_dof(jm)
        solve_log.append({"stage": "single_point_0V", "status": "error", "message": str(e), "dof": dof})

    if solve_status == "ok" and points > 1:
        try:
            import numpy as np
            voltages = np.linspace(start_V, stop_V, points)
            voltages_str = ",".join([f"{v}[V]" for v in voltages])
            sweep = study.feature().create("param1", "Parametric")
            sweep.set("pname", "V_bias")
            sweep.set("plist", voltages_str)
            sweep.set("punit", "V")
            study.run()
            dof = solver_dof(jm)
            if dof == 0:
                solve_status = "partial: 0 V solved, but sweep generated 0 degrees of freedom"
            else:
                solve_status = "ok"
            solve_log.append({"stage": "bias_sweep", "status": solve_status, "points": points, "dof": dof})
        except Exception as e:
            solve_status = f"partial: 0 V solved, bias sweep failed: {e}"
            dof = solver_dof(jm)
            solve_log.append({"stage": "bias_sweep", "status": "error", "message": str(e), "points": points, "dof": dof})
            if config.get("enable_segmented_continuation", True):
                segmented = run_segmented_continuation(jm, study, start_V, stop_V, points)
                dof = segmented.get("dof", dof)
                solve_log.append({"stage": "segmented_bias_continuation", **segmented})
                if segmented.get("status") == "ok":
                    solve_status = "ok"
                else:
                    solve_status = (
                        "partial: 0 V solved, bias sweep and segmented continuation failed: "
                        f"{segmented.get('message')}"
                    )

    return {
        "solve_status": solve_status,
        "output_dir": str(output_dir),
        "bias_points": points,
        "dof": dof,
        "mesh_log": mesh_log,
        "solve_log": solve_log,
    }


def _run_optoelectronic_once(config: dict, run_label: str = "full_stack") -> dict:
    mph = ensure_mph()
    client = mph.start()

    sim_config = copy.deepcopy(config)
    model_path = config.get("model_path")
    if model_path and Path(model_path).exists():
        model = client.load(model_path)
    else:
        build_script = Path(__file__).parent / "build_heterostructure.py"
        import importlib.util
        spec = importlib.util.spec_from_file_location("build", str(build_script))
        build_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(build_mod)

        device_config = semiconductor_device_config(config)
        sim_config["device_stack"] = device_config
        tmp_stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        tmp_model = SKILL_DIR / "output" / f"tmp_opto_device_{run_label}_{tmp_stamp}.mph"
        build_mod.build_layered_device(device_config, str(tmp_model))
        model = client.load(str(tmp_model))
        model_path = str(tmp_model)

    jm = model.java
    comp = jm.component("comp1")

    # Load geometry mapping
    mapping = load_mapping({"model_path": model_path})

    # 1. Semiconductor physics
    semi_info = setup_semiconductor_physics(jm, comp, sim_config, mapping)

    # 2. Optical generation
    gen_info = setup_optical_generation(jm, comp, sim_config)

    # 3. Study, mesh, solve
    solve_info = setup_study_and_solve(jm, comp, sim_config)

    # 4. Results export
    output_dir = Path(solve_info["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save model with solution
    result_mph = output_dir / "opto_result.mph"
    saved_path, save_warnings = save_model_safely(model, result_mph)

    # Plot/export setup is intentionally deferred until a line/path dataset is
    # defined for the 2D stack; creating a placeholder export emits COMSOL noise.
    export_info = {
        "band_diagram": "skipped",
        "reason": "line/path dataset for band-edge export is not configured yet",
    }

    return {
        "status": solve_info["solve_status"],
        "run_label": run_label,
        "electrical_model": sim_config.get("electrical_model", "full_stack"),
        "output_dir": str(output_dir),
        "model_saved": saved_path,
        "save_warnings": save_warnings,
        "dof": solve_info.get("dof"),
        "mesh": solve_info.get("mesh_log"),
        "solve_log": solve_info.get("solve_log"),
        "mapping": mapping,
        "semiconductor_setup": semi_info["setup_log"],
        "optical_generation": gen_info,
        "exports": export_info,
        "note": "Full I-V extraction requires Global Evaluation setup with V_bias sweep.",
    }


def run_optoelectronic_simulation(config: dict) -> dict:
    result = _run_optoelectronic_once(config, "full_stack")
    full_stack_result = result
    if should_try_active_transport_fallback(config, result["status"]):
        active_cfg = active_transport_regularized_config(config)
        active_result = _run_optoelectronic_once(active_cfg, "active_transport_regularized")
        if active_result.get("status") == "ok":
            combined = copy.deepcopy(active_result)
            combined["status"] = "ok_with_active_transport_regularized"
            combined["full_stack_attempt"] = full_stack_result
            combined["fallback_reason"] = active_cfg["fallback_reason"]
            combined["note"] = (
                "Configured transport/intermediate layers are active Semiconductor domains in the solved model. "
                "The solved active-transport window is intentionally limited for numerical continuation; "
                "use transport-passive mode for wide scans until interface transport is calibrated."
            )
            return combined
        result = copy.deepcopy(active_result)
        result["full_stack_attempt"] = full_stack_result

    if not should_try_transport_passive_fallback(config, result["status"]):
        if not should_try_absorber_core_fallback(config, result["status"]):
            return result
    else:
        transport_cfg = transport_passive_full_geometry_config(config)
        transport_result = _run_optoelectronic_once(transport_cfg, "transport_passive_full_geometry")
        if transport_result.get("status") == "ok":
            combined = copy.deepcopy(transport_result)
            combined["status"] = "ok_with_transport_passive_full_geometry"
            combined["full_stack_attempt"] = result
            combined["fallback_reason"] = transport_cfg["fallback_reason"]
            combined["note"] = (
                "Full stack drift-diffusion was attempted first. The solved model keeps configured "
                "transport/intermediate layers in the geometry as passive layers and solves absorber layers electrically."
            )
            return combined

        result = copy.deepcopy(transport_result)
        result["full_stack_attempt"] = full_stack_result

    if not should_try_absorber_core_fallback(config, result["status"]):
        return result

    fallback_cfg = absorber_core_config(config)
    fallback_result = _run_optoelectronic_once(fallback_cfg, "absorber_core_fallback")
    combined = copy.deepcopy(fallback_result)
    if fallback_result.get("status") == "ok":
        combined["status"] = "ok_with_absorber_core_fallback"
    else:
        combined["status"] = f"partial: full stack and absorber-core fallback failed ({fallback_result.get('status')})"
    combined["previous_attempt"] = result
    combined["fallback_reason"] = fallback_cfg["fallback_reason"]
    combined["note"] = (
        "Full stack and transport-passive attempts were tried first. The reported solved model is the absorber-core "
        "fallback unless previous_attempt.status is ok."
    )
    return combined


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to optoelectronic simulation config JSON")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    result = run_optoelectronic_simulation(config)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()


