#!/usr/bin/env python3
"""Fast all-pairs STL interference check using trimesh Boolean backends."""
import argparse
import itertools
import json
import os

import trimesh


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input-dir', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--engine', default='manifold')
    ap.add_argument('--prefix-digits-only', action='store_true')
    ap.add_argument('--volume-warn-mm3', type=float, default=0.5)
    ap.add_argument('--volume-big-mm3', type=float, default=5.0)
    return ap.parse_args()


def load(indir, filename):
    mesh = trimesh.load(os.path.join(indir, filename), force='mesh', process=True)
    mesh.remove_unreferenced_vertices()
    if mesh.volume < 0:
        mesh.invert()
    return mesh


def main():
    args = parse_args()
    files = sorted(f for f in os.listdir(args.input_dir) if f.lower().endswith('.stl'))
    if args.prefix_digits_only:
        files = [f for f in files if len(f) >= 2 and f[:2].isdigit()]
    if len(files) < 2:
        raise SystemExit('Need at least two STL files')

    meshes = {os.path.splitext(f)[0]: load(args.input_dir, f) for f in files}
    rows = []
    for a, b in itertools.combinations(meshes, 2):
        ma, mb = meshes[a], meshes[b]
        amin, amax = ma.bounds
        bmin, bmax = mb.bounds
        if ((amax < bmin).any() or (bmax < amin).any()):
            rows.append({'pair': [a, b], 'status': 'bbox_no_overlap', 'volume_mm3': 0.0})
            continue
        try:
            inter = trimesh.boolean.intersection([ma, mb], engine=args.engine, check_volume=False)
            if inter is None or len(inter.faces) == 0:
                vol = 0.0
                faces = 0
                verts = 0
            else:
                inter.process(validate=True)
                vol = abs(float(inter.volume))
                faces = len(inter.faces)
                verts = len(inter.vertices)
            rows.append({'pair': [a, b], 'status': 'ok', 'volume_mm3': vol, 'faces': faces, 'verts': verts})
        except Exception as e:
            rows.append({'pair': [a, b], 'status': 'error', 'error': repr(e)})

    data = {
        'input_dir': args.input_dir,
        'pairs': rows,
        'volume_warn_mm3': args.volume_warn_mm3,
        'volume_big_mm3': args.volume_big_mm3,
    }
    os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
