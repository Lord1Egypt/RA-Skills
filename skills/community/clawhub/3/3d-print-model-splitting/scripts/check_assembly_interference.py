#!/usr/bin/env python3
import itertools
import os
import sys


def parse_args():
    if '--' not in sys.argv:
        if '-h' in sys.argv or '--help' in sys.argv:
            print('Usage: blender --background --python check_assembly_interference.py -- --input-dir dir --outdir out')
            raise SystemExit(0)
        raise SystemExit('Usage: blender --background --python check_assembly_interference.py -- --input-dir dir --outdir out')
    args = sys.argv[sys.argv.index('--')+1:]
    opts = {}
    i = 0
    while i < len(args):
        if args[i].startswith('--'):
            k = args[i][2:]
            if i+1 < len(args) and not args[i+1].startswith('--'):
                opts[k] = args[i+1]
                i += 2
            else:
                opts[k] = True
                i += 1
        else:
            i += 1
    return opts


def import_stl(path):
    before = set(bpy.data.objects)
    bpy.ops.wm.stl_import(filepath=path)
    new = [o for o in bpy.data.objects if o not in before and o.type == 'MESH']
    if not new:
        raise RuntimeError(f'No mesh imported: {path}')
    obj = new[0]
    obj.name = os.path.splitext(os.path.basename(path))[0]
    return obj


def bbox(obj):
    pts = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return mn, mx, mx-mn


def bbox_overlap(a, b, eps=1e-6):
    amin, amax, _ = bbox(a)
    bmin, bmax, _ = bbox(b)
    return all((amin[i] <= bmax[i] + eps and bmin[i] <= amax[i] + eps) for i in range(3))


def dup(obj, name):
    cp = obj.copy()
    cp.data = obj.data.copy()
    cp.name = name
    bpy.context.collection.objects.link(cp)
    return cp


def mesh_volume_abs(obj):
    # bpy Mesh has volume only through bmesh; use signed tetra volume.
    mesh = obj.data
    mesh.calc_loop_triangles()
    vol = 0.0
    mw = obj.matrix_world
    for tri in mesh.loop_triangles:
        p0, p1, p2 = [mw @ mesh.vertices[i].co for i in tri.vertices]
        vol += p0.dot(p1.cross(p2)) / 6.0
    return abs(vol)


def main():
    opts = parse_args()
    global bpy, Vector
    import bpy
    from mathutils import Vector
    indir = opts['input-dir']
    outdir = opts['outdir']
    os.makedirs(outdir, exist_ok=True)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    files = sorted([os.path.join(indir, f) for f in os.listdir(indir) if f.lower().endswith('.stl')])
    objs = [import_stl(f) for f in files]
    for obj in objs:
        obj.hide_render = True

    # classify thresholds in mm^3 because current files are scaled to mm.
    # Tiny boolean fragments below this are usually coplanar/numerical noise.
    volume_warn = 0.5
    volume_big = 5.0
    reports = []
    reports.append(f'input_dir={indir}')
    reports.append(f'outdir={outdir}')
    reports.append('method=assembled-position pairwise Boolean INTERSECT; dimensions are in mm for current scaled STL set')
    reports.append(f'volume_warn_mm3={volume_warn}')
    reports.append(f'volume_big_mm3={volume_big}')

    intersections = []
    for a, b in itertools.combinations(objs, 2):
        if not bbox_overlap(a, b):
            reports.append(f'PAIR {a.name} || {b.name}: bbox_no_overlap')
            continue
        ia = dup(a, 'INTERSECT__' + a.name + '__AND__' + b.name)
        ib = dup(b, 'CUTTER__' + b.name)
        mod = ia.modifiers.new('intersection', 'BOOLEAN')
        mod.operation = 'INTERSECT'
        mod.object = ib
        try:
            mod.solver = 'EXACT'
        except Exception:
            pass
        bpy.context.view_layer.objects.active = ia
        ia.select_set(True)
        status = 'ok'
        err = ''
        try:
            bpy.ops.object.modifier_apply(modifier=mod.name)
        except Exception as e:
            status = 'boolean_failed'
            err = str(e)
        ia.select_set(False)
        ib.hide_viewport = True
        ib.hide_render = True
        faces = len(ia.data.polygons) if status == 'ok' else -1
        verts = len(ia.data.vertices) if status == 'ok' else -1
        vol = mesh_volume_abs(ia) if status == 'ok' and faces else 0.0
        if status == 'ok' and faces:
            mn, mx, dims = bbox(ia)
            # keep visible only if nontrivial
            if vol >= volume_warn or faces >= 50:
                intersections.append(ia)
                ia.hide_render = False
                ia.hide_viewport = False
            else:
                ia.hide_render = True
                ia.hide_viewport = True
            severity = 'BIG_INTERFERENCE' if vol >= volume_big else ('small_or_coplanar' if vol >= volume_warn or faces else 'none')
            reports.append(f'PAIR {a.name} || {b.name}: status={status}; severity={severity}; faces={faces}; verts={verts}; volume_mm3={vol:.6f}; bbox_min=({mn.x:.3f},{mn.y:.3f},{mn.z:.3f}); bbox_max=({mx.x:.3f},{mx.y:.3f},{mx.z:.3f}); dims=({dims.x:.3f},{dims.y:.3f},{dims.z:.3f})')
        else:
            reports.append(f'PAIR {a.name} || {b.name}: status={status}; error={err}')

    # Render an intersection overview if any nontrivial intersections exist.
    if intersections:
        mat = bpy.data.materials.new('INTERFERENCE_RED')
        mat.diffuse_color = (1, 0, 0, 1)
        for o in intersections:
            o.data.materials.clear(); o.data.materials.append(mat)
        # Show original parts faintly-ish with colors (Workbench no transparency; use gray and render intersections separately visible)
        for o in objs:
            o.hide_render = False; o.hide_viewport = False
            m = bpy.data.materials.new(o.name + '_gray')
            m.diffuse_color = (0.55, 0.55, 0.55, 1)
            o.data.materials.clear(); o.data.materials.append(m)
        all_show = objs + intersections
        pts = []
        for o in all_show:
            for c in o.bound_box:
                pts.append(o.matrix_world @ Vector(c))
        center = Vector((sum(p.x for p in pts)/len(pts), sum(p.y for p in pts)/len(pts), sum(p.z for p in pts)/len(pts)))
        mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
        mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
        dims = mx - mn
        r = max(dims) or 1
        scene = bpy.context.scene
        scene.render.engine = 'BLENDER_WORKBENCH'
        scene.display.shading.light = 'STUDIO'
        scene.display.shading.color_type = 'MATERIAL'
        scene.display.shading.show_cavity = True
        scene.display.shading.show_object_outline = True
        scene.world.color = (0.04, 0.045, 0.052)
        scene.render.resolution_x = 1400
        scene.render.resolution_y = 1400
        scene.render.image_settings.file_format = 'PNG'
        light_data = bpy.data.lights.new('Light', 'AREA')
        light = bpy.data.objects.new('Light', light_data); bpy.context.collection.objects.link(light)
        light.location = (center.x+r, center.y-r*1.5, center.z+r*1.3); light.data.energy = 500; light.data.size = r
        cam_data = bpy.data.cameras.new('Camera')
        cam = bpy.data.objects.new('Camera', cam_data); bpy.context.collection.objects.link(cam)
        scene.camera = cam; cam.data.type = 'ORTHO'
        def look_at(obj, target):
            d = target - obj.location
            obj.rotation_euler = d.to_track_quat('-Z','Y').to_euler()
        for name, loc in {
            'interference_front': (center.x, center.y-r*3, center.z),
            'interference_iso': (center.x+r*2, center.y-r*2.4, center.z+r*1.5),
        }.items():
            cam.location = Vector(loc); look_at(cam, center)
            cam.data.ortho_scale = max(dims.x, dims.z) * 1.25 if name.endswith('front') else max(dims) * 1.45
            scene.render.filepath = os.path.join(outdir, name + '.png')
            bpy.ops.render.render(write_still=True)
    else:
        reports.append('no_nontrivial_intersection_objects_for_preview=true')

    blend = os.path.join(outdir, 'assembly_interference_check.blend')
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    reports.append(f'blend={blend}')
    path = os.path.join(outdir, 'assembly_interference_report.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(reports) + '\n')
    print(open(path, encoding='utf-8').read())

if __name__ == '__main__':
    main()
