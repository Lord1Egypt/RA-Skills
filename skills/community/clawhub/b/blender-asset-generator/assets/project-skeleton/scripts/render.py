# pyright: reportMissingImports=false
import argparse
import os
import sys
from datetime import datetime
from typing import Any

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


def _setup_world_and_lights() -> None:
    scene = bpy.context.scene
    compat.set_render_engine_best_effort()

    # Simple light gray background.
    if bpy.data.worlds.get("WORLD__mvp") is None:
        world = bpy.data.worlds.new("WORLD__mvp")
    else:
        world = bpy.data.worlds["WORLD__mvp"]
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (0.9, 0.9, 0.92, 1.0)
        bg.inputs[1].default_value = 1.0
    scene.world = world

    # Remove existing lights to keep deterministic.
    for obj in list(bpy.data.objects):
        if obj.type == "LIGHT":
            bpy.data.objects.remove(obj, do_unlink=True)

    def add_light(name: str, loc, energy: float):
        light_data = bpy.data.lights.new(name=name, type="AREA")
        light_data.energy = energy
        light_obj = bpy.data.objects.new(name, light_data)
        light_obj.location = loc
        bpy.context.scene.collection.objects.link(light_obj)
        return light_obj

    add_light("LIGHT__key", (1.2, -1.2, 1.5), 800.0)
    add_light("LIGHT__fill", (-1.4, -0.6, 1.0), 350.0)
    add_light("LIGHT__rim", (-1.2, 1.4, 1.6), 450.0)


def _ensure_camera() -> Any:
    cam = bpy.data.objects.get("CAM__mvp")
    if cam and cam.type == "CAMERA":
        bpy.context.scene.camera = cam
        return cam

    cam_data = bpy.data.cameras.new("CAM__mvp")
    cam = bpy.data.objects.new("CAM__mvp", cam_data)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera = cam
    return cam


def _frame_asset_and_place_camera(cam_obj, view: str) -> None:
    # Frame based on all mesh bounds.
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if not meshes:
        return

    min_x = float("inf")
    min_y = float("inf")
    min_z = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")
    max_z = float("-inf")

    for o in meshes:
        mw = o.matrix_world
        for v in o.data.vertices:
            p = mw @ v.co
            min_x = min(min_x, p.x)
            min_y = min(min_y, p.y)
            min_z = min(min_z, p.z)
            max_x = max(max_x, p.x)
            max_y = max(max_y, p.y)
            max_z = max(max_z, p.z)

    cx = (float(min_x) + float(max_x)) / 2.0
    cy = (float(min_y) + float(max_y)) / 2.0
    cz = (float(min_z) + float(max_z)) / 2.0
    size = max(
        float(max_x) - float(min_x),
        float(max_y) - float(min_y),
        float(max_z) - float(min_z),
    )
    dist = max(0.6, size * 2.2)

    if view == "front":
        cam_obj.location = (cx, cy - dist, cz + size * 0.35)
    else:
        cam_obj.location = (cx + dist * 0.8, cy - dist * 0.8, cz + size * 0.5)

    # Look at center (robust across Blender versions).
    compat.look_at(cam_obj, (cx, cy, cz))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blend", required=True)
    parser.add_argument("--out_dir", required=True)
    parser.add_argument("--log", default="run-log.txt")
    argv = sys.argv
    if "--" in argv:
        idx = argv.index("--")
        argv = argv[idx + 1:]  # type: ignore[index]
    else:
        argv = []
    args = parser.parse_args(argv)

    _ensure_dir(args.out_dir)
    _ensure_dir(os.path.dirname(args.log) or ".")

    with open(args.log, "a", encoding="utf-8") as lf:
        _log(lf, f"[render] {datetime.utcnow().isoformat()}Z")
        _log(lf, f"[render] blend={args.blend}")
        _log(lf, f"[render] out_dir={args.out_dir}")

        bpy.ops.wm.open_mainfile(filepath=args.blend)
        _setup_world_and_lights()
        cam = _ensure_camera()

        scene = bpy.context.scene
        # Avoid clipping for small/large scenes.
        scene.camera.data.clip_start = 0.001
        scene.camera.data.clip_end = 1000.0
        scene.render.resolution_x = 1024
        scene.render.resolution_y = 1024
        scene.render.image_settings.file_format = "PNG"

        view_pairs = (
            ("front", "front.png"),
            ("three_quarter", "three_quarter.png"),
        )
        for view_name, fname in view_pairs:
            _frame_asset_and_place_camera(cam, view=view_name)
            out_path = os.path.join(args.out_dir, fname)
            scene.render.filepath = out_path
            bpy.ops.render.render(write_still=True)
            _log(lf, f"[render] wrote={out_path}")

        _log(lf, "[render] ok")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
