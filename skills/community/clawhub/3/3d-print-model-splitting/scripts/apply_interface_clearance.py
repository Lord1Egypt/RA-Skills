#!/usr/bin/env python3
"""Apply interface clearance by subtracting expanded neighboring STL parts.

Example:
  python scripts/apply_interface_clearance.py \
    --input-dir parts \
    --outdir clearance_parts \
    --part hat_head=01_hat_head.stl \
    --part body=02_body.stl \
    --interface body:hat_head \
    --clearance-mm 0.5

Each --interface TARGET:CUTTER means:
  TARGET = TARGET - expand(CUTTER, clearance_mm)
"""
import argparse
import json
import os

import numpy as np
import trimesh


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input-dir', required=True)
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--part', action='append', required=True, help='key=filename.stl')
    ap.add_argument('--interface', action='append', required=True, help='target_key:cutter_key')
    ap.add_argument('--clearance-mm', type=float, default=0.5)
    ap.add_argument('--engine', default='manifold')
    return ap.parse_args()


def parse_key_value(items, flag):
    out = {}
    for item in items:
        if '=' not in item:
            raise SystemExit(f'Bad {flag} {item!r}; expected key=value')
        k, v = item.split('=', 1)
        out[k] = v
    return out


def parse_interfaces(items):
    out = []
    for item in items:
        if ':' not in item:
            raise SystemExit(f'Bad --interface {item!r}; expected target:cutter')
        target, cutter = item.split(':', 1)
        out.append((target, cutter))
    return out


def stats(mesh):
    e = np.sort(mesh.edges.reshape((-1, 2)), axis=1)
    if len(e) == 0:
        b = g = n = 0
    else:
        dt = np.dtype([('a', e.dtype), ('b', e.dtype)])
        v = e.view(dt).reshape(-1)
        _, c = np.unique(v, return_counts=True)
        b = int((c == 1).sum())
        g = int((c > 2).sum())
        n = int((c != 2).sum())
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


def orient(mesh):
    mesh = mesh.copy()
    mesh.remove_unreferenced_vertices()
    if mesh.volume < 0:
        mesh.invert()
    return mesh


def expand(mesh, clearance):
    cp = orient(mesh)
    cp.vertices = cp.vertices + cp.vertex_normals * clearance
    return orient(cp)


def boolean_difference(target, cutter, engine):
    result = trimesh.boolean.difference([target, cutter], engine=engine, check_volume=False)
    if isinstance(result, list):
        result = trimesh.util.concatenate(result)
    if result is None or len(result.faces) == 0:
        raise RuntimeError('Boolean difference returned empty result')
    return orient(result)


def main():
    args = parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    part_files = parse_key_value(args.part, '--part')
    interfaces = parse_interfaces(args.interface)

    missing = sorted({k for pair in interfaces for k in pair if k not in part_files})
    if missing:
        raise SystemExit(f'Interface references unknown part key(s): {missing}')

    parts = {}
    for key, filename in part_files.items():
        path = os.path.join(args.input_dir, filename)
        parts[key] = orient(trimesh.load(path, force='mesh', process=True))

    report = {
        'input_dir': args.input_dir,
        'outdir': args.outdir,
        'clearance_mm': args.clearance_mm,
        'engine': args.engine,
        'parts': part_files,
        'interfaces': interfaces,
        'initial_stats': {k: stats(v) for k, v in parts.items()},
        'steps': [],
    }

    for target_key, cutter_key in interfaces:
        before = stats(parts[target_key])
        cutter = expand(parts[cutter_key], args.clearance_mm)
        parts[target_key] = boolean_difference(parts[target_key], cutter, args.engine)
        report['steps'].append({
            'target': target_key,
            'cutter': cutter_key,
            'before': before,
            'expanded_cutter': stats(cutter),
            'after': stats(parts[target_key]),
        })

    output_files = {}
    for key, filename in part_files.items():
        out = os.path.join(args.outdir, filename)
        parts[key].export(out)
        output_files[key] = out

    combined = trimesh.util.concatenate([parts[k] for k in part_files])
    combined_path = os.path.join(args.outdir, 'assembled_clearance_multi_shell.stl')
    combined.export(combined_path)

    report['outputs'] = output_files
    report['combined'] = {'stl': combined_path, 'stats': stats(combined)}
    report['final_stats'] = {k: stats(v) for k, v in parts.items()}

    report_path = os.path.join(args.outdir, 'apply_interface_clearance_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
