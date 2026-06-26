# pyright: reportMissingImports=false
import argparse
import json
import math
import os
import sys
from datetime import datetime

import bpy  # type: ignore
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

import compat  # type: ignore  # noqa: E402


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _log(fp, msg: str) -> None:
    fp.write(msg.rstrip() + "\n")
    fp.flush()


def _mm_to_m(v_mm: float) -> float:
    return float(v_mm) / 1000.0


def _set_scene_units_mm() -> None:
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    # 1 Blender unit = 1m; scale_length=0.001 => mm display.
    scene.unit_settings.scale_length = 0.001
    scene.unit_settings.length_unit = "MILLIMETERS"


def _cleanup_default_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    # Remove unused data blocks (best effort)
    for datablock in (
        bpy.data.meshes,
        bpy.data.materials,
        bpy.data.lights,
        bpy.data.cameras,
    ):
        for b in list(datablock):
            if b.users == 0:
                datablock.remove(b)


def _make_pbr_placeholder_material(
    name: str, base_color_rgba, roughness: float, metallic: float
):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    for n in list(nodes):
        nodes.remove(n)

    out = nodes.new(type="ShaderNodeOutputMaterial")
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = tuple(base_color_rgba)
    bsdf.inputs["Roughness"].default_value = float(roughness)
    bsdf.inputs["Metallic"].default_value = float(metallic)
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def _apply_transform(obj, loc_mm, rot_deg):
    if loc_mm is not None:
        obj.location = (
            _mm_to_m(loc_mm[0]),
            _mm_to_m(loc_mm[1]),
            _mm_to_m(loc_mm[2]),
        )
    if rot_deg is not None:
        obj.rotation_euler = (
            math.radians(rot_deg[0]),
            math.radians(rot_deg[1]),
            math.radians(rot_deg[2]),
        )


def _add_box(name: str, params_mm: dict):
    w = _mm_to_m(params_mm.get("width", 100))
    d = _mm_to_m(params_mm.get("depth", 60))
    h = _mm_to_m(params_mm.get("height", 40))
    bevel_r = _mm_to_m(params_mm.get("bevel_radius", 0))

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (w / 2.0, d / 2.0, h / 2.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    if bevel_r > 0:
        mod = obj.modifiers.new(name="BEVEL", type="BEVEL")
        mod.width = bevel_r
        mod.segments = int(params_mm.get("bevel_segments", 3))
        mod.limit_method = "ANGLE"
        bpy.ops.object.modifier_apply(modifier=mod.name)

    return obj


def _add_cylinder(name: str, params_mm: dict):
    r = _mm_to_m(params_mm.get("radius", 35))
    h = _mm_to_m(params_mm.get("height", 120))
    verts = int(params_mm.get("vertices", 64))
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=verts,
        radius=r,
        depth=h,
        location=(0, 0, h / 2.0),
    )
    obj = bpy.context.active_object
    obj.name = name
    return obj


def _add_bottle_like(name: str, params_mm: dict):
    # MVP bottle-ish: main cylinder + neck cylinder + simple bevels.
    height = float(params_mm.get("height", 240))
    diameter = float(params_mm.get("diameter", 70))
    neck_height = float(params_mm.get("neck_height", 35))
    neck_diameter = float(params_mm.get("neck_diameter", 32))
    base_bevel = float(params_mm.get("base_bevel_radius", 0))
    top_bevel = float(params_mm.get("top_bevel_radius", 0))

    body_h_mm = max(1.0, height - neck_height)
    body = _add_cylinder(
        name=name + "__body",
        params_mm={
            "radius": diameter / 2.0,
            "height": body_h_mm,
            "vertices": int(params_mm.get("vertices", 96)),
        },
    )
    body.location = (0, 0, _mm_to_m(body_h_mm) / 2.0)

    neck = _add_cylinder(
        name=name + "__neck",
        params_mm={
            "radius": neck_diameter / 2.0,
            "height": neck_height,
            "vertices": int(params_mm.get("vertices", 96)),
        },
    )
    neck.location = (0, 0, _mm_to_m(body_h_mm) + _mm_to_m(neck_height) / 2.0)

    # Join parts into one mesh for MVP export simplicity.
    bpy.ops.object.select_all(action="DESELECT")
    body.select_set(True)
    neck.select_set(True)
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.join()
    obj = bpy.context.active_object
    obj.name = name

    # Bevel (best effort)
    bevel_r = _mm_to_m(max(base_bevel, top_bevel))
    if bevel_r > 0:
        mod = obj.modifiers.new(name="BEVEL", type="BEVEL")
        mod.width = bevel_r
        mod.segments = int(params_mm.get("bevel_segments", 3))
        mod.limit_method = "ANGLE"
        bpy.ops.object.modifier_apply(modifier=mod.name)

    # Smooth shading for nicer previews.
    for poly in obj.data.polygons:
        poly.use_smooth = True
    compat.enable_auto_smooth_best_effort(obj, angle_deg=30.0)
    return obj


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    parser.add_argument("--out_blend", required=True)
    parser.add_argument("--log", default="run-log.txt")
    argv = sys.argv
    if "--" in argv:
        idx = argv.index("--")
        argv = argv[idx + 1:]  # type: ignore[index]
    else:
        argv = []
    args = parser.parse_args(argv)

    _ensure_dir(os.path.dirname(args.out_blend) or ".")
    _ensure_dir(os.path.dirname(args.log) or ".")

    with open(args.log, "a", encoding="utf-8") as lf:
        _log(lf, f"[build] {datetime.utcnow().isoformat()}Z")
        _log(lf, f"[build] blender={compat.blender_version_string()}")
        _log(lf, f"[build] spec={args.spec}")
        _log(lf, f"[build] out_blend={args.out_blend}")

        with open(args.spec, "r", encoding="utf-8") as f:
            spec = json.load(f)

        _set_scene_units_mm()
        _cleanup_default_scene()

        # Materials
        mats = {}
        for m in spec.get("asset", {}).get("materials", []) or []:
            if m.get("type") != "pbr_placeholder":
                continue
            mats[m["name"]] = _make_pbr_placeholder_material(
                name=m["name"],
                base_color_rgba=m.get("base_color_rgba", [0.8, 0.8, 0.8, 1.0]),
                roughness=m.get("roughness", 0.5),
                metallic=m.get("metallic", 0.0),
            )

        # Collection root
        asset_name = spec.get("asset", {}).get("name", "asset")
        col = bpy.data.collections.new("ASSET__" + asset_name)
        bpy.context.scene.collection.children.link(col)

        # Components
        for c in spec.get("asset", {}).get("components", []):
            cname = c.get("name", "MESH__part")
            prim = c.get("primitive")
            params_mm = c.get("params_mm") or {}

            if prim == "box":
                obj = _add_box(cname, params_mm)
            elif prim == "cylinder":
                obj = _add_cylinder(cname, params_mm)
            elif prim == "bottle_like":
                obj = _add_bottle_like(cname, params_mm)
            else:
                _log(
                    lf,
                    f"[build][warn] unsupported primitive={prim} for "
                    f"component={cname}, skipping",
                )
                continue

            # Apply material (best effort)
            mat_name = c.get("material")
            if mat_name and mat_name in mats:
                if obj.data.materials:
                    obj.data.materials[0] = mats[mat_name]
                else:
                    obj.data.materials.append(mats[mat_name])

            # Transform
            tr = c.get("transform") or {}
            _apply_transform(
                obj,
                tr.get("location_mm"),
                tr.get("rotation_deg"),
            )

            # Link to asset collection
            if obj.name in bpy.context.scene.collection.objects:
                bpy.context.scene.collection.objects.unlink(obj)
            col.objects.link(obj)

        # Save .blend
        bpy.ops.wm.save_as_mainfile(filepath=args.out_blend)
        _log(lf, "[build] ok")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
