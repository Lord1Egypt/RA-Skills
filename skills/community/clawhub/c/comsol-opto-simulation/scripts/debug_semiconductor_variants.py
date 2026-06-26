#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Try minimal Semiconductor study variants and report DOF counts.

This is a diagnostic script, not a production simulation entry point.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

import mph


def dof_from_message(message: str) -> int | None:
    match = re.search(r"自由度数：(\d+)", message)
    if match:
        return int(match.group(1))
    match = re.search(r"degrees of freedom:\s*(\d+)", message, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def try_set(feature, key: str, value: str, log: list[str]) -> None:
    try:
        feature.set(key, value)
        log.append(f"{key}={value}")
    except Exception as exc:
        log.append(f"{key} failed: {str(exc).splitlines()[0]}")


def build_model(client, name: str, variant: dict):
    model = client.create(name)
    jm = model.java
    comp = jm.component().create("comp1", True)
    geom = comp.geom().create("geom1", 2)

    rect_p = geom.feature().create("rect_p", "Rectangle")
    rect_p.set("size", ["500[nm]", "500[nm]"])
    rect_p.set("pos", ["0[nm]", "0[nm]"])
    rect_n = geom.feature().create("rect_n", "Rectangle")
    rect_n.set("size", ["500[nm]", "500[nm]"])
    rect_n.set("pos", ["500[nm]", "0[nm]"])
    geom.run()

    semi = comp.physics().create("semi", "Semiconductor", "geom1")
    if variant.get("semi_all"):
        semi.selection().all()

    log: list[str] = []
    for tag, domain, donor, acceptor in [
        ("mat_p", 1, "0[1/cm^3]", "1e16[1/cm^3]"),
        ("mat_n", 2, "1e16[1/cm^3]", "0[1/cm^3]"),
    ]:
        mat = semi.create(tag, "SemiconductorMaterialModel")
        mat.selection().set([domain])
        for key, value in [
            ("Eg0", "1.12[eV]"),
            ("chi0", "4.05[eV]"),
            ("mun", "1000[cm^2/(V*s)]"),
            ("mup", "500[cm^2/(V*s)]"),
            ("Nc", "2.8e19[1/cm^3]"),
            ("Nv", "1.04e19[1/cm^3]"),
            ("epsilonr", "11.7"),
        ]:
            if variant.get("userdef_material_values"):
                try_set(mat, f"{key}_mat", "userdef", log)
            try_set(mat, key, value, log)
        if variant.get("model_input_doping"):
            try_set(mat, "minput_numberdensitydonor_src", "userdef", log)
            try_set(mat, "minput_numberdensitydonor", donor, log)
            try_set(mat, "minput_numberdensityacceptor_src", "userdef", log)
            try_set(mat, "minput_numberdensityacceptor", acceptor, log)

        if variant.get("analytic_doping"):
            adm = semi.create(f"adm_{tag}", "AnalyticDopingModel")
            adm.selection().set([domain])
            try_set(adm, "FeatureType", "Doping", log)
            try_set(adm, "impurityType", "donor" if donor != "0[1/cm^3]" else "acceptor", log)
            try_set(adm, "NDc", donor, log)
            try_set(adm, "NAc", acceptor, log)

    anode = semi.create("anode", "MetalContact")
    anode.selection().set([1])
    anode.set("V0", "0[V]")
    anode.set("ContactType", "ohmic")
    cathode = semi.create("cathode", "MetalContact")
    cathode.selection().set([7])
    cathode.set("V0", "0.1[V]")
    cathode.set("ContactType", "ohmic")

    mesh = comp.mesh().create("mesh1")
    size = mesh.feature().create("size1", "Size")
    size.set("hauto", "4")
    if variant.get("free_tri"):
        mesh.feature().create("ftri1", "FreeTri")
    mesh.run()

    study = jm.study().create("std1")
    try:
        stat = study.feature().create("stat1", variant.get("study_type", "Stationary"))
    except Exception as exc:
        log.append(f"study type {variant.get('study_type')} failed: {str(exc).splitlines()[0]}")
        stat = study.feature().create("stat1", "Stationary")
    if variant.get("activate"):
        try:
            stat.activate("semi", True)
            log.append("activate(semi)=True")
        except Exception as exc:
            log.append(f"activate failed: {str(exc).splitlines()[0]}")

    return model, log


def main() -> None:
    client = mph.start()
    variants = [
        {"name": "baseline"},
        {"name": "semi_all", "semi_all": True},
        {"name": "free_tri", "semi_all": True, "free_tri": True},
        {"name": "activated", "activate": True},
        {"name": "all_activated", "semi_all": True, "activate": True},
        {"name": "doped_all_activated", "semi_all": True, "activate": True, "model_input_doping": True},
        {"name": "analytic_doping", "semi_all": True, "activate": True, "analytic_doping": True},
        {"name": "analytic_and_model_input", "semi_all": True, "activate": True, "model_input_doping": True, "analytic_doping": True},
        {"name": "full_fixed", "semi_all": True, "activate": True, "model_input_doping": True, "analytic_doping": True, "free_tri": True},
        {"name": "full_fixed_userdef", "semi_all": True, "activate": True, "model_input_doping": True, "analytic_doping": True, "free_tri": True, "userdef_material_values": True},
        {"name": "semi_equilibrium", "semi_all": True, "activate": True, "model_input_doping": True, "study_type": "SemiconductorEquilibrium"},
        {"name": "semiconductor_stationary", "semi_all": True, "activate": True, "model_input_doping": True, "study_type": "SemiconductorStationary"},
        {"name": "semi_stationary", "semi_all": True, "activate": True, "model_input_doping": True, "study_type": "SemiStationary"},
    ]
    results = []
    for variant in variants:
        name = variant["name"]
        model, log = build_model(client, f"debug_{name}", variant)
        jm = model.java
        entry = {"variant": name, "setup_log": log[-12:]}
        try:
            model.build()
            model.solve()
            msg = str(jm.sol("sol1").feature("s1").getString("message"))
            entry["dof"] = dof_from_message(msg)
            entry["solver_message"] = msg[-600:]
        except Exception as exc:
            entry["error"] = str(exc)
        for expr in ["V", "semi.Nd", "semi.Na", "semi.normJ"]:
            try:
                data = model.evaluate(expr)
                entry.setdefault("eval", {})[expr] = str(data.shape) if hasattr(data, "shape") else str(data)[:80]
            except Exception as exc:
                entry.setdefault("eval_errors", {})[expr] = str(exc).splitlines()[0]
        results.append(entry)
        model.clear()
    print(json.dumps({"status": "debug_semiconductor_variants", "results": results}, indent=2, ensure_ascii=False))
    client.disconnect()


if __name__ == "__main__":
    main()
