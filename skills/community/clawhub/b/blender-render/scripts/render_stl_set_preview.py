#!/usr/bin/env python3
"""Render deterministic Workbench previews for one or more STL/OBJ/PLY files.

Run with Blender, for example:
  blender --background --python render_stl_set_preview.py -- \
    --input /path/to/parts_dir --output-dir /path/to/preview --prefix model --explode 0.35
"""
import argparse
import hashlib
import os
import sys
from pathlib import Path

import bpy
from mathutils import Vector

SUPPORTED = {".stl", ".obj", ".ply"}
PALETTE = [
    (1.00, 0.10, 0.05, 1.0),
    (0.10, 0.45, 1.00, 1.0),
    (0.55, 0.18, 0.95, 1.0),
    (0.15, 0.90, 0.20, 1.0),
    (1.00, 0.82, 0.00, 1.0),
    (1.00, 0.55, 0.20, 1.0),
    (0.00, 0.85, 0.95, 1.0),
    (0.95, 0.30, 0.60, 1.0),
]


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--input", action="append", required=True, help="File or directory. May be repeated.")
    p.add_argument("--output-dir", required=True)
    p.add_argument("--prefix", default="preview")
    p.add_argument("--views", default="front,iso", help="Comma list: front,iso,top,side")
    p.add_argument("--explode", type=float, default=0.0, help="0 disables; 0.25-0.5 is usually enough.")
    p.add_argument("--resolution", type=int, default=1400)
    p.add_argument("--preserve-materials", action="store_true", help="Keep imported OBJ/PLY/FBX-style materials instead of assigning stable preview colors.")
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    return p.parse_args(argv)


def collect_inputs(inputs):
    files = []
    for raw in inputs:
        path = Path(raw).expanduser()
        if path.is_dir():
            files.extend(sorted(p for p in path.iterdir() if p.suffix.lower() in SUPPORTED))
        elif path.is_file() and path.suffix.lower() in SUPPORTED:
            files.append(path)
        else:
            print(f"skip unsupported/missing input: {path}", file=sys.stderr)
    # Keep deterministic unique paths.
    return sorted(dict.fromkeys(str(p.resolve()) for p in files))


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def import_model(filepath):
    before = set(bpy.data.objects)
    suffix = Path(filepath).suffix.lower()
    if suffix == ".stl":
        bpy.ops.wm.stl_import(filepath=filepath)
    elif suffix == ".obj":
        if hasattr(bpy.ops.wm, "obj_import"):
            bpy.ops.wm.obj_import(filepath=filepath)
        else:
            bpy.ops.import_scene.obj(filepath=filepath)
    elif suffix == ".ply":
        if hasattr(bpy.ops.wm, "ply_import"):
            bpy.ops.wm.ply_import(filepath=filepath)
        else:
            bpy.ops.import_mesh.ply(filepath=filepath)
    else:
        raise ValueError(f"unsupported file format: {filepath}")
    new_objs = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
    if not new_objs:
        raise RuntimeError(f"no mesh objects imported from {filepath}")
    return new_objs


def stable_color(name, idx):
    digest = hashlib.sha1(name.encode("utf-8")).digest()[0]
    return PALETTE[(digest + idx) % len(PALETTE)]


def assign_material(obj, color):
    mat = bpy.data.materials.new(f"{obj.name}_mat")
    mat.diffuse_color = color
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def sync_material_viewport_colors(obj):
    """Make imported node material colors visible in Workbench MATERIAL mode."""
    for mat in obj.data.materials:
        if not mat:
            continue
        try:
            node_tree = getattr(mat, "node_tree", None)
            if node_tree:
                for node in node_tree.nodes:
                    if node.bl_idname == "ShaderNodeBsdfPrincipled" and "Base Color" in node.inputs:
                        mat.diffuse_color = tuple(node.inputs["Base Color"].default_value)
                        break
        except Exception:
            pass


def bounds(objects):
    mins = Vector((float("inf"), float("inf"), float("inf")))
    maxs = Vector((float("-inf"), float("-inf"), float("-inf")))
    found = False
    for obj in objects:
        if obj.type != "MESH":
            continue
        for corner in obj.bound_box:
            world = obj.matrix_world @ Vector(corner)
            mins.x = min(mins.x, world.x)
            mins.y = min(mins.y, world.y)
            mins.z = min(mins.z, world.z)
            maxs.x = max(maxs.x, world.x)
            maxs.y = max(maxs.y, world.y)
            maxs.z = max(maxs.z, world.z)
            found = True
    if not found:
        raise RuntimeError("no mesh bounds found")
    return mins, maxs, (mins + maxs) * 0.5, maxs - mins


def make_preview_objects(objects, explode):
    if explode <= 0 or len(objects) <= 1:
        return objects
    _, _, _, dims = bounds(objects)
    step = max(dims.x, dims.y, dims.z, 1.0) * explode
    center_index = (len(objects) - 1) / 2.0
    copies = []
    for idx, obj in enumerate(objects):
        cp = obj.copy()
        cp.data = obj.data.copy()
        cp.name = f"preview_{obj.name}"
        bpy.context.collection.objects.link(cp)
        cp.location.x += (idx - center_index) * step
        obj.hide_viewport = True
        obj.hide_render = True
        copies.append(cp)
    return copies


def setup_workbench(resolution):
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.display.shading.light = "STUDIO"
    scene.display.shading.color_type = "MATERIAL"
    scene.display.shading.show_cavity = True
    scene.display.shading.show_object_outline = True
    scene.world.color = (0.04, 0.045, 0.052)
    scene.render.resolution_x = resolution
    scene.render.resolution_y = resolution
    scene.render.image_settings.file_format = "PNG"


def setup_camera():
    cam_data = bpy.data.cameras.new("Camera")
    cam = bpy.data.objects.new("Camera", cam_data)
    bpy.context.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    cam.data.type = "ORTHO"
    return cam


def look_at(obj, target):
    direction = Vector(target) - obj.location
    obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def render_views(cam, objects, outdir, prefix, view_names):
    _, _, center, dims = bounds(objects)
    radius = max(dims.x, dims.y, dims.z, 1.0)
    views = {
        "front": (Vector((center.x, center.y - radius * 3.0, center.z)), max(dims.x, dims.z) * 1.30),
        "side": (Vector((center.x + radius * 3.0, center.y, center.z)), max(dims.y, dims.z) * 1.30),
        "top": (Vector((center.x, center.y, center.z + radius * 3.0)), max(dims.x, dims.y) * 1.30),
        "iso": (Vector((center.x + radius * 2.0, center.y - radius * 2.4, center.z + radius * 1.5)), radius * 1.65),
    }
    scene = bpy.context.scene
    for name in view_names:
        name = name.strip().lower()
        if name not in views:
            print(f"skip unknown view: {name}", file=sys.stderr)
            continue
        loc, ortho_scale = views[name]
        cam.location = loc
        look_at(cam, center)
        cam.data.ortho_scale = max(ortho_scale, 1.0)
        scene.render.filepath = str(Path(outdir) / f"{prefix}-{name}.png")
        bpy.ops.render.render(write_still=True)
        print(scene.render.filepath)


def main():
    args = parse_args()
    files = collect_inputs(args.input)
    if not files:
        raise SystemExit("no supported model files found")
    os.makedirs(args.output_dir, exist_ok=True)
    clear_scene()
    objects = []
    for idx, filepath in enumerate(files):
        imported = import_model(filepath)
        for sub_idx, obj in enumerate(imported):
            base = Path(filepath).stem
            obj.name = base if len(imported) == 1 else f"{base}_{sub_idx + 1}"
            if args.preserve_materials and obj.data.materials:
                sync_material_viewport_colors(obj)
            else:
                assign_material(obj, stable_color(obj.name, idx + sub_idx))
            objects.append(obj)
    preview_objects = make_preview_objects(objects, args.explode)
    setup_workbench(args.resolution)
    cam = setup_camera()
    render_views(cam, preview_objects, args.output_dir, args.prefix, args.views.split(","))
    mins, maxs, _, dims = bounds(preview_objects)
    print(f"input_count={len(files)} object_count={len(objects)} preview_count={len(preview_objects)}")
    print(f"bbox_min={mins.x:.4f},{mins.y:.4f},{mins.z:.4f}")
    print(f"bbox_max={maxs.x:.4f},{maxs.y:.4f},{maxs.z:.4f}")
    print(f"dims={dims.x:.4f},{dims.y:.4f},{dims.z:.4f}")


if __name__ == "__main__":
    main()
