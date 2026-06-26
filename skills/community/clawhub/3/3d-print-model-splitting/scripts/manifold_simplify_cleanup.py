#!/usr/bin/env python3
"""Clean tiny Manifold Boolean self-touch artifacts via manifold3d.simplify.

Use after clearance cutting instead of MeshFix. Keep tolerances small enough not to
remove intentional allowance geometry.
"""
import argparse
import json
import os

import numpy as np


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input-dir', required=True)
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--default-tolerance-mm', type=float, default=0.001)
    ap.add_argument('--override', action='append', default=[], help='filename.stl=tolerance_mm')
    ap.add_argument('--prefix-digits-only', action='store_true')
    return ap.parse_args()


def parse_overrides(items):
    out = {}
    for item in items:
        if '=' not in item:
            raise SystemExit(f'Bad --override {item!r}; expected filename.stl=tolerance')
        name, value = item.split('=', 1)
        out[name] = float(value)
    return out


def stats(mesh):
    edges = np.sort(mesh.edges.reshape((-1, 2)), axis=1)
    if len(edges) == 0:
        b = g = n = 0
    else:
        dt = np.dtype([('a', edges.dtype), ('b', edges.dtype)])
        v = edges.view(dt).reshape(-1)
        _, cnt = np.unique(v, return_counts=True)
        b = int((cnt == 1).sum())
        g = int((cnt > 2).sum())
        n = int((cnt != 2).sum())
    return {
        'verts': int(len(mesh.vertices)),
        'faces': int(len(mesh.faces)),
        'boundary_edges': b,
        'edges_more_than_2_faces': g,
        'non_2_face_edges': n,
        'watertight': bool(mesh.is_watertight),
        'winding_consistent': bool(mesh.is_winding_consistent),
        'volume': float(mesh.volume) if mesh.is_volume else None,
    }


def clean(mesh, tolerance):
    import manifold3d as mf
    import trimesh
    mesh = mesh.copy()
    mesh.remove_unreferenced_vertices()
    if mesh.volume < 0:
        mesh.invert()
    mani = mf.Manifold(mesh=mf.Mesh(vert_properties=np.array(mesh.vertices, dtype=np.float32), tri_verts=np.array(mesh.faces, dtype=np.uint32)))
    if tolerance > 0:
        mani = mani.simplify(tolerance)
    out = mani.to_mesh()
    result = trimesh.Trimesh(vertices=out.vert_properties, faces=out.tri_verts, process=True)
    if result.volume < 0:
        result.invert()
    return result


def main():
    args = parse_args()
    import trimesh
    overrides = parse_overrides(args.override)
    os.makedirs(args.outdir, exist_ok=True)
    parts_dir = os.path.join(args.outdir, 'simplified_parts')
    os.makedirs(parts_dir, exist_ok=True)

    files = sorted(f for f in os.listdir(args.input_dir) if f.lower().endswith('.stl'))
    if args.prefix_digits_only:
        files = [f for f in files if len(f) >= 2 and f[:2].isdigit()]
    if not files:
        raise SystemExit('No STL files found')

    report = []
    meshes = []
    for fn in files:
        tol = overrides.get(fn, args.default_tolerance_mm)
        mesh = trimesh.load(os.path.join(args.input_dir, fn), force='mesh', process=True)
        before = stats(mesh)
        cleaned = clean(mesh, tol)
        after = stats(cleaned)
        out = os.path.join(parts_dir, fn)
        cleaned.export(out)
        meshes.append(cleaned)
        report.append({'file': fn, 'tolerance_mm': tol, 'before': before, 'after': after, 'output': out})

    combined = trimesh.util.concatenate(meshes)
    combined_path = os.path.join(args.outdir, 'assembled_simplified_multi_shell.stl')
    combined.export(combined_path)
    data = {
        'input_dir': args.input_dir,
        'outdir': args.outdir,
        'default_tolerance_mm': args.default_tolerance_mm,
        'overrides': overrides,
        'method': 'manifold3d simplify cleanup; no MeshFix fill',
        'parts': report,
        'combined': {'stl': combined_path, 'stats': stats(combined)},
    }
    with open(os.path.join(args.outdir, 'manifold_simplify_cleanup_report.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
