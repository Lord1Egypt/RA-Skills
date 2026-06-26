#!/usr/bin/env python3
"""Prepare a Blender file for human material-face STL annotation.

Run with Blender:
  blender --background --python scripts/prepare_annotation_file.py -- \
    --input source/input.stl \
    --output annotation/annotation.blend \
    --part PART_01_HAT:1,0,0,1 \
    --part PART_02_HEAD:1,0.7,0.5,1
"""
import argparse
import os
import sys


def parse_args():
    if '--' not in sys.argv:
        if '-h' in sys.argv or '--help' in sys.argv:
            print('Usage: blender --background --python prepare_annotation_file.py -- --input in.stl --output out.blend --part NAME:R,G,B,A [--part ...]')
            raise SystemExit(0)
        raise SystemExit('Usage: blender --background --python prepare_annotation_file.py -- --input in.stl --output out.blend --part NAME:R,G,B,A [--part ...]')
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--object-name', default='MARKUP_SOURCE')
    ap.add_argument('--base-material', default='BASE_UNASSIGNED')
    ap.add_argument('--check-material', default='CHECK_UNCERTAIN')
    ap.add_argument('--part', action='append', default=[], help='Material name or NAME:R,G,B,A')
    return ap.parse_args(sys.argv[sys.argv.index('--') + 1:])


def parse_part(spec, idx):
    if ':' not in spec:
        return spec, default_color(idx)
    name, raw = spec.split(':', 1)
    vals = [float(x) for x in raw.split(',')]
    if len(vals) == 3:
        vals.append(1.0)
    if len(vals) != 4:
        raise SystemExit(f'Bad --part color spec: {spec}')
    return name, tuple(vals)


def default_color(i):
    palette = [
        (1.0, 0.05, 0.02, 1.0),
        (1.0, 0.72, 0.48, 1.0),
        (0.10, 0.45, 1.0, 1.0),
        (0.0, 0.85, 0.95, 1.0),
        (0.55, 0.18, 0.95, 1.0),
        (0.15, 0.90, 0.20, 1.0),
        (1.0, 0.82, 0.0, 1.0),
    ]
    return palette[i % len(palette)]


def new_mat(name, color):
    m = bpy.data.materials.new(name)
    m.diffuse_color = color
    return m


def add_camera_and_light(obj):
    bbox = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    mins = [min(v[i] for v in bbox) for i in range(3)]
    maxs = [max(v[i] for v in bbox) for i in range(3)]
    center = Vector([(mins[i] + maxs[i]) / 2 for i in range(3)])
    dims = [maxs[i] - mins[i] for i in range(3)]
    r = max(dims) or 1.0
    bpy.ops.object.light_add(type='AREA', location=(center.x + r, center.y - r * 1.5, center.z + r * 1.5))
    bpy.context.object.name = 'Preview Light'
    bpy.context.object.data.energy = 450
    bpy.context.object.data.size = r
    bpy.ops.object.camera_add(location=(center.x + r * 1.7, center.y - r * 2.2, center.z + r * 1.2))
    cam = bpy.context.object
    direction = center - cam.location
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    cam.data.type = 'ORTHO'
    cam.data.ortho_scale = r * 1.3
    bpy.context.scene.camera = cam


def main():
    args = parse_args()
    global bpy, Vector
    import bpy
    from mathutils import Vector
    if not args.part:
        raise SystemExit('Provide at least one --part material name')

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    bpy.ops.wm.stl_import(filepath=args.input)

    meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    if not meshes:
        raise SystemExit('No mesh imported')
    if len(meshes) > 1:
        bpy.ops.object.select_all(action='DESELECT')
        for o in meshes:
            o.select_set(True)
        bpy.context.view_layer.objects.active = meshes[0]
        bpy.ops.object.join()

    obj = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]
    obj.name = args.object_name
    obj.data.name = args.object_name + '_MESH'

    obj.data.materials.append(new_mat(args.base_material, (0.55, 0.55, 0.55, 1.0)))
    for i, spec in enumerate(args.part):
        name, color = parse_part(spec, i)
        obj.data.materials.append(new_mat(name, color))
    obj.data.materials.append(new_mat(args.check_material, (1.0, 1.0, 0.05, 1.0)))

    for p in obj.data.polygons:
        p.material_index = 0

    add_camera_and_light(obj)

    note = bpy.data.texts.new('README_annotation_instructions')
    part_names = '\n'.join(f'- {parse_part(spec, i)[0]}' for i, spec in enumerate(args.part))
    note.write(f'''Material-face annotation instructions\n\nObject: {args.object_name}\n\nPart materials:\n{part_names}\n\nSteps:\n1. Select the source mesh.\n2. Tab into Edit Mode.\n3. Press 3 for Face Select.\n4. Select faces for one part.\n5. Choose the corresponding PART material and click Assign.\n6. Use {args.check_material} for uncertain boundary faces if needed.\n7. Save the .blend.\n\nDo not use Texture Paint; this workflow needs per-face material assignment.\n''')

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=args.output)
    print(args.output)


if __name__ == '__main__':
    main()
