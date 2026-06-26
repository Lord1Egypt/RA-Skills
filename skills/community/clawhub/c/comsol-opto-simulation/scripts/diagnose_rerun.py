#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Full diagnostic + rerun of optoelectronic simulation.
Checks model, fixes issues, runs study, exports results.
"""
import sys, json, os
from pathlib import Path

# Ensure vendor/mph on path
SKILL_DIR = Path(__file__).resolve().parents[1]
VENDOR_DIR = SKILL_DIR / "vendor" / "site-packages"
if str(VENDOR_DIR) not in sys.path:
    sys.path.insert(0, str(VENDOR_DIR))

# Also ensure mph from comsol-opto-simulation vendor
OPTO_DIR = Path(__file__).resolve().parents[1]
OPTO_VENDOR = OPTO_DIR / "vendor" / "site-packages"
if str(OPTO_VENDOR) not in sys.path:
    sys.path.insert(0, str(OPTO_VENDOR))

def ensure_mph():
    try:
        import mph
        return mph
    except ImportError as e:
        print(json.dumps({"status": "error", "message": f"mph not found: {e}"}))
        sys.exit(1)

def diagnose_and_rerun(config_path: str):
    mph = ensure_mph()
    client = mph.start()

    # Load config
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    model_path = config.get("model_path", str(OPTO_DIR / "opto_result.mph"))
    log = {"steps": [], "errors": []}

    # Step 1: Load or build model
    if Path(model_path).exists():
        log["steps"].append("load_existing_model")
        model = client.load(model_path)
    else:
        log["steps"].append("model_not_found")
        print(json.dumps({"status": "error", "message": f"Model not found: {model_path}", "log": log}))
        return

    jm = model.java
    comp = jm.component("comp1")
    geom = comp.geom("geom1")
    semi = comp.physics("semi")

    # Step 2: Check geometry has FormUnion
    try:
        fin = geom.feature("fin")
        action = str(fin.getString("action"))
        log["steps"].append({"check": "form_union", "action": action})
        if action != "union":
            fin.set("action", "union")
            geom.run()
            log["steps"].append("fixed_form_union_to_union")
    except Exception as e:
        log["errors"].append(f"form_union check failed: {e}")

    # Step 3: Check MetalContact boundary selections
    for contact_tag in ["top_contact", "bottom_contact"]:
        try:
            contact = semi.feature(contact_tag)
            sel_type = "unknown"
            try:
                sel = contact.selection()
                sel_type = str(type(sel).__name__)
                entities = list(sel.entities())
                log["steps"].append({"check": f"contact_{contact_tag}", "selection_type": sel_type, "entities": entities})
            except Exception as e2:
                log["steps"].append({"check": f"contact_{contact_tag}", "selection_type": sel_type, "error": str(e2)})
        except Exception as e:
            log["errors"].append(f"contact {contact_tag} check failed: {e}")

    # Step 4: Check study
    try:
        studies = list(jm.study())
        log["steps"].append({"studies": studies})
        if not studies:
            log["errors"].append("No studies found")
    except Exception as e:
        log["errors"].append(f"study check failed: {e}")

    # Step 5: Check solution datasets
    try:
        if hasattr(jm, 'result') and jm.result():
            datasets = list(jm.result().dataset())
            log["steps"].append({"result_datasets": [str(d) for d in datasets]})
        else:
            log["steps"].append({"result_datasets": "none"})
    except Exception as e:
        log["errors"].append(f"dataset check failed: {e}")

    # Step 6: Try to run study if exists but no solution
    if studies:
        study_tag = studies[0]
        try:
            log["steps"].append({"action": "run_study", "study": study_tag})
            jm.study(study_tag).run()
            log["steps"].append({"action": "run_study_complete", "study": study_tag})
        except Exception as e:
            log["errors"].append(f"study run failed: {e}")

    # Step 7: Save
    try:
        model.save(model_path)
        log["steps"].append("model_saved")
    except Exception as e:
        log["errors"].append(f"save failed: {e}")

    print(json.dumps({"status": "ok", "model_path": model_path, "log": log}, indent=2, ensure_ascii=False))
    model.clear()
    client.disconnect()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(OPTO_DIR / "config_opto.json"))
    args = parser.parse_args()
    diagnose_and_rerun(args.config)


