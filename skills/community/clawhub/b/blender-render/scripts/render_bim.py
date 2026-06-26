#!/usr/bin/env python3
"""Render a robust Workbench snapshot for BIM/Revit-style FBX files."""
import argparse
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--resolution-x", type=int, default=1920)
    p.add_argument("--resolution-y", type=int, default=1080)
    return p.parse_args(argv)


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def import_fbx(filepath):
    if not Path(filepath).is_file():
        raise SystemExit(f"FBX file not found: {filepath}")
    before = set(bpy.data.objects)
    try:
        bpy.ops.import_scene.fbx(filepath=filepath)
    except Exception as exc:
        raise SystemExit(f"Failed to import FBX: {exc}") from exc
    new_meshes = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
    if not new_meshes:
        raise SystemExit(f"FBX imported but no mesh objects were found: {filepath}")
    return new_meshes


def force_visibility():
    for obj in bpy.context.scene.objects:
        obj.hide_viewport = False
        obj.hide_render = False


def get_mesh_bounds(mesh_objects):
    mins = Vector((float("inf"), float("inf"), float("inf")))
    maxs = Vector((float("-inf"), float("-inf"), float("-inf")))
    found = False
    for obj in mesh_objects:
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
        raise SystemExit("No mesh bounds found after FBX import")
    center = (mins + maxs) * 0.5
    size = (maxs - mins).length or 10.0
    return center, size


def setup_camera(center, size):
    bpy.ops.object.camera_add(location=(center.x + size, center.y - size, center.z + size * 0.5))
    cam = bpy.context.object
    bpy.context.scene.camera = cam
    direction = center - cam.location
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    cam.data.clip_end = max(1000.0, size * 10)
    cam.data.clip_start = min(0.1, max(size * 0.001, 0.001))
    return cam


def render_workbench(output_path, resolution_x, resolution_y):
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.display.shading.light = "MATCAP"
    scene.display.shading.color_type = "OBJECT"
    scene.display.shading.show_cavity = True
    scene.display.shading.cavity_type = "BOTH"
    scene.render.resolution_x = resolution_x
    scene.render.resolution_y = resolution_y
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)
    print(output_path)


def main():
    args = parse_args()
    clear_scene()
    meshes = import_fbx(args.input)
    force_visibility()
    center, size = get_mesh_bounds(meshes)
    setup_camera(center, size)
    render_workbench(args.output, args.resolution_x, args.resolution_y)


if __name__ == "__main__":
    main()
