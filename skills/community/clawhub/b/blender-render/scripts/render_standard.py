#!/usr/bin/env python3
"""Render a simple Cycles beauty preview for one STL/OBJ/PLY model."""
import argparse
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True, help="Output prefix; view suffixes are appended.")
    p.add_argument("--resolution", type=int, default=1400)
    p.add_argument("--samples", type=int, default=64)
    p.add_argument("--device", choices=["cpu", "gpu", "auto"], default="auto")
    return p.parse_args(argv)


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def import_model(filepath):
    suffix = Path(filepath).suffix.lower()
    before = set(bpy.data.objects)
    if suffix == ".stl":
        if hasattr(bpy.ops.wm, "stl_import"):
            bpy.ops.wm.stl_import(filepath=filepath)
        else:
            bpy.ops.import_mesh.stl(filepath=filepath)
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
        raise ValueError("Unsupported file format. Use .stl, .obj, or .ply.")
    new_meshes = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
    if not new_meshes:
        raise RuntimeError(f"No mesh objects imported from {filepath}")
    return new_meshes


def setup_procedural_wood():
    mat = bpy.data.materials.new(name="WoodProcedural")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out_node = nodes.new(type="ShaderNodeOutputMaterial")
    out_node.location = (400, 0)
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf.location = (100, 0)
    noise = nodes.new(type="ShaderNodeTexNoise")
    noise.location = (-300, 0)
    noise.inputs["Scale"].default_value = 10.0
    noise.inputs["Detail"].default_value = 15.0
    noise.inputs["Distortion"].default_value = 1.0
    ramp = nodes.new(type="ShaderNodeValToRGB")
    ramp.location = (-100, 0)
    ramp.color_ramp.elements[0].position = 0.3
    ramp.color_ramp.elements[0].color = (0.45, 0.23, 0.08, 1.0)
    ramp.color_ramp.elements[1].position = 0.75
    ramp.color_ramp.elements[1].color = (0.95, 0.64, 0.28, 1.0)

    links.new(noise.outputs["Color"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    links.new(bsdf.outputs["BSDF"], out_node.inputs["Surface"])
    return mat


def get_scene_bounds():
    mins = Vector((float("inf"), float("inf"), float("inf")))
    maxs = Vector((float("-inf"), float("-inf"), float("-inf")))
    found = False
    for obj in bpy.context.scene.objects:
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
        raise RuntimeError("No mesh bounds found")
    center = (mins + maxs) * 0.5
    size = (maxs - mins).length or 1.0
    return center, size


def setup_lighting(center, size):
    dist = size * 1.5
    energy = max(size * size * 100, 250)
    lights = [
        ("Key", (center.x + dist, center.y - dist, center.z + dist), energy * 2.0, size * 0.5),
        ("Fill", (center.x - dist, center.y - dist, center.z + dist / 2), energy * 0.5, size * 0.8),
        ("Back", (center.x, center.y + dist * 1.2, center.z + dist), energy * 1.5, size),
    ]
    for name, loc, power, radius in lights:
        bpy.ops.object.light_add(type="AREA", location=loc)
        light = bpy.context.object
        light.name = name
        light.data.energy = power
        light.data.size = max(radius, 0.1)


def setup_camera():
    bpy.ops.object.camera_add()
    cam = bpy.context.object
    bpy.context.scene.camera = cam
    return cam


def point_camera(cam, target_pos):
    direction = target_pos - cam.location
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def setup_cycles(resolution, samples, device):
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = samples
    scene.render.resolution_x = resolution
    scene.render.resolution_y = int(resolution * 9 / 16)
    scene.render.image_settings.file_format = "PNG"
    if device == "cpu":
        scene.cycles.device = "CPU"
    elif device == "gpu":
        scene.cycles.device = "GPU"
    else:
        # Keep Blender's configured default; do not force unavailable GPU devices.
        pass


def render_views(cam, center, size, output_prefix):
    dist = max(size * 1.2, 1.0)
    views = {
        "front": (center.x, center.y - dist, center.z + size * 0.2),
        "side": (center.x + dist, center.y, center.z + size * 0.2),
        "top": (center.x + size * 0.1, center.y - size * 0.1, center.z + dist * 1.5),
    }
    for view_name, cam_pos in views.items():
        cam.location = Vector(cam_pos)
        point_camera(cam, center)
        bpy.context.scene.render.filepath = f"{output_prefix}_{view_name}.png"
        bpy.ops.render.render(write_still=True)
        print(bpy.context.scene.render.filepath)


def main():
    args = parse_args()
    clear_scene()
    objects = import_model(args.input)
    mat = setup_procedural_wood()
    for obj in objects:
        obj.data.materials.clear()
        obj.data.materials.append(mat)
    center, size = get_scene_bounds()
    setup_lighting(center, size)
    cam = setup_camera()
    setup_cycles(args.resolution, args.samples, args.device)
    render_views(cam, center, size, args.output)


if __name__ == "__main__":
    main()
