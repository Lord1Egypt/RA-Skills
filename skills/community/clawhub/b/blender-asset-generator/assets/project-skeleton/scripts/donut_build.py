# pyright: reportMissingImports=false
import argparse
import math
import os
import random
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


def _clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def _make_material(name: str, base_color, roughness: float, metallic: float):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*base_color, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
    return mat


def _enable_auto_smooth(obj, angle_deg: float) -> None:
    # Blender 4.x: mesh.use_auto_smooth + mesh.auto_smooth_angle
    # Blender 5.x: this API may move; fall back to operator if present.
    mesh = getattr(obj, "data", None)
    if mesh is None:
        return

    if hasattr(mesh, "use_auto_smooth"):
        mesh.use_auto_smooth = True
        if hasattr(mesh, "auto_smooth_angle"):
            mesh.auto_smooth_angle = math.radians(angle_deg)
        return

    # Blender 4.1+ has an operator; keep as a compatibility fallback.
    if hasattr(bpy.ops.object, "shade_auto_smooth"):
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.shade_auto_smooth(angle=math.radians(angle_deg))


def _shade_smooth(obj) -> None:
    for poly in obj.data.polygons:
        poly.use_smooth = True
    compat.enable_auto_smooth_best_effort(obj, angle_deg=30.0)


def _add_sprinkles(target_obj, count: int, seed: int):
    # Deterministic sprinkles as small cylinders on the top half of the donut.
    random.seed(seed)

    sprinkles = []
    for i in range(count):
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=12,
            radius=0.01,
            depth=0.06,
            location=(0, 0, 0),
        )
        s = bpy.context.active_object
        s.name = f"MESH__sprinkle_{i:03d}"

        # Sample around torus: angle + small jitter.
        ang = random.random() * math.tau
        rad = 0.32 + random.uniform(-0.02, 0.02)
        x = math.cos(ang) * rad
        y = math.sin(ang) * rad
        z = 0.10 + random.uniform(-0.02, 0.03)
        s.location = (x, y, z)
        s.rotation_euler = (
            random.random() * math.tau,
            random.random() * math.tau,
            random.random() * math.tau,
        )
        sprinkles.append(s)

    # Parent to target for convenience.
    for s in sprinkles:
        s.parent = target_obj


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out_blend", default="donut.blend")
    parser.add_argument("--log", default="run-log.txt")
    parser.add_argument("--sprinkle_count", type=int, default=120)
    parser.add_argument("--seed", type=int, default=42)
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
        _log(lf, f"[donut_build] {datetime.utcnow().isoformat()}Z")
        _log(lf, f"[donut_build] blender={compat.blender_version_string()}")
        _log(lf, f"[donut_build] out_blend={args.out_blend}")

        _clear_scene()

        # Donut base (torus)
        bpy.ops.mesh.primitive_torus_add(
            major_radius=0.35,
            minor_radius=0.14,
            major_segments=64,
            minor_segments=32,
            location=(0, 0, 0),
        )
        donut = bpy.context.active_object
        donut.name = "MESH__donut"
        _shade_smooth(donut)

        # Icing: duplicate + shrinkwrap-ish effect via solidify + slight scale.
        bpy.ops.object.duplicate()
        icing = bpy.context.active_object
        icing.name = "MESH__icing"
        icing.scale = (1.01, 1.01, 1.01)
        bpy.ops.object.transform_apply(
            location=False,
            rotation=False,
            scale=True,
        )
        _shade_smooth(icing)

        solid = icing.modifiers.new(name="SOLIDIFY", type="SOLIDIFY")
        solid.thickness = 0.03
        bpy.ops.object.modifier_apply(modifier=solid.name)

        # Cut icing bottom half: boolean with a cube (keep top).
        bpy.ops.mesh.primitive_cube_add(size=3.0, location=(0, 0, -0.7))
        cutter = bpy.context.active_object
        cutter.name = "TMP__cutter"
        bool_mod = icing.modifiers.new(
            name="BOOLEAN",
            type="BOOLEAN",
        )
        bool_mod.operation = "DIFFERENCE"
        bool_mod.object = cutter
        bpy.context.view_layer.objects.active = icing
        bpy.ops.object.modifier_apply(modifier=bool_mod.name)
        bpy.data.objects.remove(cutter, do_unlink=True)

        # Materials (simple placeholders)
        mat_donut = _make_material("MAT__donut", (0.55, 0.33, 0.16), 0.7, 0.0)
        mat_icing = _make_material("MAT__icing", (0.95, 0.55, 0.75), 0.35, 0.0)
        donut.data.materials.append(mat_donut)
        icing.data.materials.append(mat_icing)

        # Sprinkles on icing
        _add_sprinkles(icing, count=args.sprinkle_count, seed=args.seed)
        sprinkle_mat = _make_material(
            "MAT__sprinkle",
            (0.2, 0.7, 0.9),
            0.4,
            0.0,
        )
        for obj in bpy.context.scene.objects:
            if not obj.name.startswith("MESH__sprinkle_"):
                continue
            obj.data.materials.append(sprinkle_mat)
            _shade_smooth(obj)

        # Save
        bpy.ops.wm.save_as_mainfile(filepath=args.out_blend)
        _log(lf, "[donut_build] ok")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
