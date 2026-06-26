#!/usr/bin/env python3
"""Repair STL parts with pymeshfix before clearance work.

Use this only before intentional clearance cavities are cut.
"""
import argparse
import json
import os

import numpy as np


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input-dir', required=True)
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--pattern-prefix-digits', action='store_true', help='Only process STL files whose names start with two digits')
    group = ap.add_mutually_exclusive_group()
    group.add_argument('--join-components', dest='join_components', action='store_true', default=True)
    group.add_argument('--no-join-components', dest='join_components', action='store_false')
    return ap.parse_args()


def stats(mesh):
    e = np.sort(mesh.edges.reshape((-1, 2)), axis=1)
    if len(e) == 0:
        return {'verts': len(mesh.vertices), 'faces': len(mesh.faces), 'boundary_edges': 0, 'edges_more_than_2_faces': 0, 'non_2_face_edges': 0, 'watertight': False}
    dt = np.dtype([('a', e.dtype), ('b', e.dtype)])
    v = e.view(dt).reshape(-1)
    _, c = np.unique(v, return_counts=True)
    return {
        'verts': int(len(mesh.vertices)),
        'faces': int(len(mesh.faces)),
        'boundary_edges': int((c == 1).sum()),
        'edges_more_than_2_faces': int((c > 2).sum()),
        'non_2_face_edges': int((c != 2).sum()),
        'watertight': bool(mesh.is_watertight),
        'winding_consistent': bool(mesh.is_winding_consistent),
        'volume': float(mesh.volume) if mesh.is_volume else None,
    }


def combine_meshes(meshes):
    import trimesh
    verts = []
    faces = []
    off = 0
    for m in meshes:
        verts.append(np.asarray(m.vertices))
        faces.append(np.asarray(m.faces) + off)
        off += len(m.vertices)
    if not verts:
        return None
    return trimesh.Trimesh(vertices=np.vstack(verts), faces=np.vstack(faces), process=False)


def export_obj(meshes, names, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write('# repaired STL parts as separate OBJ objects\n')
        off = 1
        for name, mesh in zip(names, meshes):
            f.write(f'o {name}\n')
            for v in mesh.vertices:
                f.write(f'v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n')
            for face in mesh.faces:
                f.write('f ' + ' '.join(str(int(i) + off) for i in face) + '\n')
            off += len(mesh.vertices)


def main():
    args = parse_args()
    import pymeshfix
    import trimesh
    os.makedirs(args.outdir, exist_ok=True)
    parts_dir = os.path.join(args.outdir, 'meshfixed_parts')
    os.makedirs(parts_dir, exist_ok=True)

    files = sorted(f for f in os.listdir(args.input_dir) if f.lower().endswith('.stl'))
    if args.pattern_prefix_digits:
        files = [f for f in files if len(f) >= 2 and f[:2].isdigit()]
    if not files:
        raise SystemExit('No STL files found')

    report = {'input_dir': args.input_dir, 'outdir': args.outdir, 'warning': 'Use MeshFix before clearance only; do not use it to repair intentional clearance cavities.', 'parts': []}
    repaired = []
    names = []

    for fn in files:
        src = os.path.join(args.input_dir, fn)
        mesh = trimesh.load(src, force='mesh', process=True)
        before = stats(mesh)
        mf = pymeshfix.MeshFix(mesh.vertices, mesh.faces)
        mf.repair(verbose=False, joincomp=args.join_components, remove_smallest_components=False)
        fixed = trimesh.Trimesh(vertices=mf.v, faces=mf.f, process=True)
        fixed.remove_unreferenced_vertices()
        after = stats(fixed)
        out = os.path.join(parts_dir, fn)
        fixed.export(out)
        repaired.append(fixed)
        names.append(os.path.splitext(fn)[0])
        report['parts'].append({'file': fn, 'before': before, 'after': after, 'output': out})

    combined = combine_meshes(repaired)
    if combined is not None:
        combined_path = os.path.join(args.outdir, 'assembled_meshfixed_multi_shell.stl')
        combined.export(combined_path)
        obj_path = os.path.join(args.outdir, 'assembled_meshfixed_separate_objects.obj')
        export_obj(repaired, names, obj_path)
        report['combined'] = {'stl': combined_path, 'obj': obj_path, 'stats': stats(combined)}

    report_path = os.path.join(args.outdir, 'meshfix_repair_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
