#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a user-configured layered structure from scratch in COMSOL.

The layer order, layer roles, materials, and geometry must come from the
user's project configuration or an explicit JSON config.

Usage:
    python build_heterostructure.py --config device_stack.json --output output/model.mph

Output:
    - output/model.mph          : COMSOL model file
    - output/model.mapping.json : Domain/boundary selection mapping
"""

from __future__ import annotations

import argparse
import json
import sys
import os
from pathlib import Path

# Ensure vendor is on path
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


def _extract_geometry_mapping(jm, geom, dim: int, layer_tags: list[dict]) -> dict:
    """
    Extract domain / boundary indices from built geometry.

    Strategy:
      1. Try COMSOL Java API to read actual object indices.
      2. If API unavailable (mph not running), fallback to theoretically
         expected indices based on layer creation order.

    Returns mapping dict with keys:
      - domains:    {layer_name: domain_index, ...}
      - boundaries: {boundary_name: [indices], ...}
      - interfaces: [{between: [nameA, nameB], boundary_indices: [...]}, ...]
      - contacts:   {top: index, bottom: index}
    """
    n_layers = len(layer_tags)
    mapping = {
        "domains": {},
        "boundaries": {},
        "interfaces": [],
        "contacts": {},
        "source": "",
        "note": "",
    }

    # -- Attempt 1: COMSOL live read --------------------------------
    try:
        domains_live = {}
        # After geom.run(), objects exist and can be queried via geom.object(tag)
        # COMSOL Java API: geom.object(tag).getDomainNames() returns domain indices
        for i, lt in enumerate(layer_tags):
            tag = lt["tag"]
            domain_idx = None
            try:
                obj = geom.object(tag)
                domains = obj.getDomainNames()
                if domains and len(domains) > 0:
                    domain_idx = int(domains[0])
            except Exception:
                pass

            if domain_idx is None:
                # Fallback: create explicit selection from object
                try:
                    sel_name = f"sel_{tag}"
                    sel = geom.selection().create(sel_name, "Explicit")
                    sel.set(tag)
                    entities = list(sel.entities())
                    if entities:
                        domain_idx = int(entities[0])
                        # Clean up temporary selection
                        geom.selection().remove(sel_name)
                except Exception:
                    pass

            if domain_idx is None:
                domain_idx = i + 1

            domains_live[lt["name"]] = domain_idx

        top_layer = layer_tags[-1]
        bottom_layer = layer_tags[0]

        contacts_live = {
            "top": {
                "layer": top_layer["name"],
                "edge": "top",
                "selection_tag": "sel_top",
                "note": "Top boundary of entire stack (y = total_thickness)",
            },
            "bottom": {
                "layer": bottom_layer["name"],
                "edge": "bottom",
                "selection_tag": "sel_bottom",
                "note": "Bottom boundary of entire stack (y = 0)",
            },
        }
        
        boundaries_live = {
            "sides": {
                "selection_tag": "sel_sides",
                "note": "Side boundaries (left and right edges)",
            }
        }

        interfaces_live = []
        for i in range(n_layers - 1):
            upper = layer_tags[i]
            lower = layer_tags[i + 1]
            interfaces_live.append({
                "between": [upper["name"], lower["name"]],
                "upper_layer": upper["name"],
                "lower_layer": lower["name"],
                "upper_domain": domains_live.get(upper["name"]),
                "lower_domain": domains_live.get(lower["name"]),
                "expected_tag": f"interface_{upper['name']}_{lower['name']}",
                "note": "Shared boundary between adjacent layers",
            })

        mapping["domains"] = domains_live
        mapping["contacts"] = contacts_live
        mapping["interfaces"] = interfaces_live
        mapping["boundaries"] = boundaries_live
        mapping["source"] = "live_comsol_api"
        mapping["note"] = "Domain indices read from COMSOL geometry. Boundary selections use Box-based explicit selections (sel_top, sel_bottom, sel_sides)."

    except Exception as e:
        # -- Attempt 2: Theoretical fallback -------------------------------
        domains_fallback = {}
        for i, lt in enumerate(layer_tags):
            domains_fallback[lt["name"]] = i + 1

        top_layer_fb = layer_tags[-1]
        bottom_layer_fb = layer_tags[0]

        contacts_fallback = {
            "top": {
                "layer": top_layer_fb["name"],
                "edge": "top",
                "selection_tag": "sel_top",
                "note": "Top boundary of entire stack",
            },
            "bottom": {
                "layer": bottom_layer_fb["name"],
                "edge": "bottom",
                "selection_tag": "sel_bottom",
                "note": "Bottom boundary of entire stack",
            },
        }

        boundaries_fallback = {
            "sides": {
                "selection_tag": "sel_sides",
                "note": "Side boundaries (left and right edges)",
            }
        }

        interfaces_fallback = []
        for i in range(n_layers - 1):
            upper = layer_tags[i]
            lower = layer_tags[i + 1]
            interfaces_fallback.append({
                "between": [upper["name"], lower["name"]],
                "upper_layer": upper["name"],
                "lower_layer": lower["name"],
                "upper_domain": i + 1,
                "lower_domain": i + 2,
                "expected_tag": f"interface_{upper['name']}_{lower['name']}",
                "note": "Shared boundary between adjacent layers",
            })

        mapping["domains"] = domains_fallback
        mapping["contacts"] = contacts_fallback
        mapping["interfaces"] = interfaces_fallback
        mapping["boundaries"] = boundaries_fallback
        mapping["source"] = "theoretical_fallback"
        mapping["note"] = f"COMSOL live read failed ({type(e).__name__}: {str(e)}). Domain indices are theoretical (creation order, 1-based). Boundary selections use Box-based explicit selections."

    return mapping


def build_layered_device(config: dict, output_path: str) -> dict:
    """Build device layers from scratch using MPh.

    Additionally, creates a geometry-to-physics mapping file
    (mapping.json) that records:
      - domain index for each layer
      - top/bottom/external boundary indices
      - interface boundaries between adjacent layers

    This mapping is consumed by simulation scripts to avoid
    hard-coded selection indices.
    """
    mph = ensure_mph()
    client = mph.start()

    model_name = config.get("name", "heterojunction_photodetector")
    model = client.create(model_name)
    jm = model.java

    # Create component and 1D/2D/3D geometry
    dim = config.get("dimension", 2)  # Default 2D cross-section
    comp = jm.component().create("comp1", True)
    geom = comp.geom().create("geom1", dim)

    # Build layers from bottom (back electrode) to top (front electrode)
    # For 2D: rectangle strips stacked vertically
    layers = config.get("layers", [])
    y_offset = 0.0
    layer_tags = []

    for i, layer in enumerate(layers):
        tag = f"layer{i}"
        thickness = layer["thickness_nm"]
        width = layer.get("width_nm", config.get("device_width_nm", 1000))

        if dim == 2:
            rect = geom.feature().create(tag, "Rectangle")
            rect.set("size", [f"{width}[nm]", f"{thickness}[nm]"])
            rect.set("pos", ["0[nm]", f"{y_offset}[nm]"])
        elif dim == 3:
            depth = layer.get("depth_nm", config.get("device_depth_nm", 1000))
            block = geom.feature().create(tag, "Block")
            block.set("size", [f"{width}[nm]", f"{thickness}[nm]", f"{depth}[nm]"])
            block.set("pos", ["0[nm]", f"{y_offset}[nm]", "0[nm]"])

        layer_tags.append({
            "name": layer["name"],
            "tag": tag,
            "thickness_nm": thickness,
            "y_bottom_nm": y_offset,
            "y_top_nm": y_offset + thickness,
            "material": layer.get("material", ""),
        })
        y_offset += thickness

    # Build geometry
    # Form Union is automatically created as 'fin' when geometry is initialized
    # We just need to set its action to 'union' to merge all layers
    fin = geom.feature('fin')
    fin.set('action', 'union')
    
    geom.run()
    
    # Create explicit boundary selections using Box selection at component level
    width = config.get("device_width_nm", 1000)
    total_thickness = y_offset
    
    from jpype import JInt
    
    # Select top boundary (y near total_thickness)
    sel_top = comp.selection().create('sel_top', 'Box')
    sel_top.set('xmin', '0[nm]')
    sel_top.set('xmax', f'{width}[nm]')
    sel_top.set('ymin', f'{total_thickness-1}[nm]')
    sel_top.set('ymax', f'{total_thickness+1}[nm]')
    sel_top.set('condition', 'inside')
    sel_top.set('entitydim', JInt(1))
    
    # Select bottom boundary (y near 0)
    sel_bottom = comp.selection().create('sel_bottom', 'Box')
    sel_bottom.set('xmin', '0[nm]')
    sel_bottom.set('xmax', f'{width}[nm]')
    sel_bottom.set('ymin', '-1[nm]')
    sel_bottom.set('ymax', '1[nm]')
    sel_bottom.set('condition', 'inside')
    sel_bottom.set('entitydim', JInt(1))
    
    # Select side boundaries (x near 0 and x near width)
    sel_sides = comp.selection().create('sel_sides', 'Box')
    sel_sides.set('xmin', '-1[nm]')
    sel_sides.set('xmax', f'{width+1}[nm]')
    sel_sides.set('ymin', '-1[nm]')
    sel_sides.set('ymax', f'{total_thickness+1}[nm]')
    sel_sides.set('condition', 'inside')
    sel_sides.set('entitydim', JInt(1))

    # -- Extract domain / boundary mapping -----------------------------
    mapping = _extract_geometry_mapping(jm, geom, dim, layer_tags)

    # Save mapping alongside the model
    mapping_path = Path(output_path).with_suffix(".mapping.json")
    with open(mapping_path, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

    # Save model
    model.save(output_path)

    return {
        "status": "ok",
        "model_name": model_name,
        "output_path": output_path,
        "total_thickness_nm": y_offset,
        "layers": layer_tags,
        "dimension": dim,
        "mapping": mapping,
        "mapping_path": str(mapping_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to device stack JSON config")
    parser.add_argument("--output", default="output/heterostructure.mph", help="Output .mph file path")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Extract device_stack if present (config_opto.json format)
    device_config = config.get("device_stack", config)

    # Ensure output dir exists
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    result = build_layered_device(device_config, str(out))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()


