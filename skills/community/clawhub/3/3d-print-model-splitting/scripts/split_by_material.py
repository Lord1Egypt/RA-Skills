#!/usr/bin/env python3
"""Split a Blender mesh into STL files by material names.

Run with Blender:
  blender --background --python scripts/split_by_material.py -- \
    --input annotation/annotation.blend \
    --outdir versions/v02-split-baseline/outputs \
    --part PART_01_HAT=01_hat \
    --part PART_02_HEAD=02_head
"""
import argparse
import json
import os
import struct
import sys
from collections import Counter, defaultdict, deque



def parse_args():
    if '--' not in sys.argv:
        if '-h' in sys.argv or '--help' in sys.argv:
            print('Usage: blender --background --python split_by_material.py -- --input in.blend --outdir out --part MAT=slug [--part ...]')
            raise SystemExit(0)
        raise SystemExit('Usage: blender --background --python split_by_material.py -- --input in.blend --outdir out --part MAT=slug [--part ...]')
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--source-object', default='')
    ap.add_argument('--part', action='append', required=True, help='MATERIAL_NAME=output_slug')
    ap.add_argument('--tiny-island-max-faces', type=int, default=60)
    ap.add_argument('--allow-open-boundary', action='store_true', help='Do not fail when capping leaves boundary edges; report them instead')
    return ap.parse_args(sys.argv[sys.argv.index('--') + 1:])


def parse_parts(specs):
    out = []
    for spec in specs:
        if '=' not in spec:
            raise SystemExit(f'Bad --part spec {spec!r}; expected MATERIAL=slug')
        mat, slug = spec.split('=', 1)
        out.append((mat, slug))
    return out


def find_source(name=''):
    meshes = [o for o in bpy.data.objects if o.type == 'MESH' and len(o.data.polygons) > 0]
    if not meshes:
        raise SystemExit('No mesh object found')
    if name:
        obj = bpy.data.objects.get(name)
        if not obj or obj.type != 'MESH':
            raise SystemExit(f'Source mesh not found: {name}')
        return obj
    for o in meshes:
        if o.name.startswith('MARKUP_SOURCE'):
            return o
    return max(meshes, key=lambda o: len(o.data.polygons))


def build_neighbors(mesh):
    neighbors = [[] for _ in mesh.polygons]
    edge_faces = defaultdict(list)
    for p in mesh.polygons:
        for e in p.edge_keys:
            edge_faces[e].append(p.index)
    for fs in edge_faces.values():
        for i, a in enumerate(fs):
            for b in fs[i + 1:]:
                neighbors[a].append(b)
                neighbors[b].append(a)
    return neighbors


def cleanup_tiny_material_islands(mesh, mat_by_face, valid_indices, neighbors, max_faces):
    n = len(mesh.polygons)
    seen = bytearray(n)
    changes = []
    for start in range(n):
        if seen[start]:
            continue
        mat = mat_by_face[start]
        q = deque([start])
        seen[start] = 1
        comp = []
        adjacent = []
        while q:
            f = q.popleft()
            comp.append(f)
            for nb in neighbors[f]:
                if mat_by_face[nb] == mat:
                    if not seen[nb]:
                        seen[nb] = 1
                        q.append(nb)
                else:
                    adjacent.append(mat_by_face[nb])
        if len(comp) <= max_faces and adjacent:
            target, target_count = Counter(adjacent).most_common(1)[0]
            if target in valid_indices and target_count >= max(3, len(adjacent) * 0.65):
                for f in comp:
                    mat_by_face[f] = target
                changes.append({'from': mat, 'to': target, 'faces': len(comp)})
    return changes


def create_mesh_from_faces(src_obj, face_indices, name):
    src_mesh = src_obj.data
    verts = []
    vmap = {}
    faces = []
    for fi in face_indices:
        poly = src_mesh.polygons[fi]
        face = []
        for vi in poly.vertices:
            if vi not in vmap:
                vmap[vi] = len(verts)
                verts.append(tuple(src_obj.matrix_world @ src_mesh.vertices[vi].co))
            face.append(vmap[vi])
        faces.append(face)
    mesh = bpy.data.meshes.new(name + '_mesh')
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj


def cap_mesh(obj):
    import bmesh
    mesh = obj.data
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table(); bm.faces.ensure_lookup_table()
    boundary_edges = [e for e in bm.edges if len(e.link_faces) == 1]
    before = len(bm.faces)
    cap_faces = 0
    if boundary_edges:
        res = bmesh.ops.holes_fill(bm, edges=boundary_edges, sides=0)
        cap_faces += sum(1 for item in res.get('geom', []) if isinstance(item, bmesh.types.BMFace))
        bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table(); bm.faces.ensure_lookup_table()

    # Some sculpt split boundaries are not filled by holes_fill (for example when
    # a selected surface already occupies the loop). Fallback to a conservative
    # fan cap for any remaining boundary components so raw open shells are not
    # exported as a baseline by accident.
    residual_edges = [e for e in bm.edges if len(e.link_faces) == 1]
    if residual_edges:
        edge_set = set(residual_edges)
        vertex_edges = {}
        for edge in residual_edges:
            for vert in edge.verts:
                vertex_edges.setdefault(vert, []).append(edge)
        components = []
        while edge_set:
            stack = [edge_set.pop()]
            comp = []
            while stack:
                edge = stack.pop()
                comp.append(edge)
                for vert in edge.verts:
                    for next_edge in vertex_edges.get(vert, []):
                        if next_edge in edge_set:
                            edge_set.remove(next_edge)
                            stack.append(next_edge)
            components.append(comp)

        for comp in components:
            verts = list({vert for edge in comp for vert in edge.verts})
            if len(verts) < 3:
                continue
            center = verts[0].co.copy()
            center.zero()
            for vert in verts:
                center += vert.co
            center /= len(verts)
            center_vert = bm.verts.new(center)
            bm.verts.ensure_lookup_table()
            for edge in comp:
                try:
                    bm.faces.new((edge.verts[0], edge.verts[1], center_vert))
                    cap_faces += 1
                except ValueError:
                    try:
                        bm.faces.new((edge.verts[1], edge.verts[0], center_vert))
                        cap_faces += 1
                    except ValueError:
                        pass

    bm.faces.ensure_lookup_table()
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.edges.ensure_lookup_table()
    boundary_after = len([e for e in bm.edges if len(e.link_faces) == 1])
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    return {
        'boundary_edges_before': len(boundary_edges),
        'boundary_edges_after': boundary_after,
        'cap_faces_created': cap_faces,
        'faces_before': before,
        'faces_after': len(mesh.polygons),
        'capped_ok': boundary_after == 0,
    }


def export_binary_stl(obj, path):
    mesh = obj.data
    mesh.calc_loop_triangles()
    header = (f'split STL {obj.name}'.encode('utf-8')[:80]).ljust(80, b' ')
    with open(path, 'wb') as f:
        f.write(header)
        f.write(struct.pack('<I', len(mesh.loop_triangles)))
        for tri in mesh.loop_triangles:
            pts = [obj.matrix_world @ mesh.vertices[i].co for i in tri.vertices]
            n = (pts[1] - pts[0]).cross(pts[2] - pts[0])
            if n.length:
                n.normalize()
            f.write(struct.pack('<3f', n.x, n.y, n.z))
            for p in pts:
                f.write(struct.pack('<3f', p.x, p.y, p.z))
            f.write(struct.pack('<H', 0))


def main():
    args = parse_args()
    global bpy, Vector
    import bpy
    from mathutils import Vector
    parts = parse_parts(args.part)
    os.makedirs(args.outdir, exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=args.input)
    src = find_source(args.source_object)
    mat_names = [m.name if m else '<None>' for m in src.data.materials]
    mat_index_by_name = {name: i for i, name in enumerate(mat_names)}

    missing = [mat for mat, _ in parts if mat not in mat_index_by_name]
    if missing:
        raise SystemExit(f'Missing material(s): {missing}; available={mat_names}')

    valid = {mat_index_by_name[mat] for mat, _ in parts}
    mat_by_face = [p.material_index for p in src.data.polygons]
    changes = cleanup_tiny_material_islands(src.data, mat_by_face, valid, build_neighbors(src.data), args.tiny_island_max_faces)
    for poly, mi in zip(src.data.polygons, mat_by_face):
        poly.material_index = mi

    report = {
        'input': args.input,
        'source_object': src.name,
        'total_faces': len(src.data.polygons),
        'cleanup_changes': changes,
        'parts': [],
    }

    for mat, slug in parts:
        mi = mat_index_by_name[mat]
        faces = [i for i, cur in enumerate(mat_by_face) if cur == mi]
        obj = create_mesh_from_faces(src, faces, slug)
        cap = cap_mesh(obj)
        if cap['boundary_edges_after'] and not args.allow_open_boundary:
            raise SystemExit(
                f'Capping left {cap["boundary_edges_after"]} boundary edges for {slug}. '
                'Do not export this as a split baseline; repair the cap or rerun with '
                '--allow-open-boundary only for diagnostic previews.'
            )
        stl = os.path.join(args.outdir, slug + '.stl')
        export_binary_stl(obj, stl)
        report['parts'].append({'material': mat, 'slug': slug, 'source_faces': len(faces), 'cap': cap, 'stl': stl})

    processed = os.path.join(args.outdir, 'split_processed.blend')
    bpy.ops.wm.save_as_mainfile(filepath=processed)
    report['processed_blend'] = processed
    report_path = os.path.join(args.outdir, 'split_by_material_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
