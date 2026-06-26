#!/usr/bin/env python3
"""Validate mesh objects embedded in a 3MF archive without unsafe extraction.

This parser validates direct mesh objects. It reports component/build usage as
warnings so callers know when validation may be incomplete.
"""
import argparse
import json
import os
import zipfile
import xml.etree.ElementTree as ET

import numpy as np
import trimesh

NS = '{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}'


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


def parse_model_bytes(data, model_file):
    root = ET.fromstring(data)
    rows = []
    warnings = []

    build = root.find(NS + 'build')
    if build is not None:
        for item in build.findall(NS + 'item'):
            transform = item.get('transform')
            if transform:
                warnings.append({
                    'model_file': model_file,
                    'kind': 'build_transform_unsupported',
                    'object_id': item.get('objectid'),
                    'transform': transform,
                    'message': 'Build transforms are reported but not applied by this validator.',
                })

    for obj in root.iter(NS + 'object'):
        components = obj.find(NS + 'components')
        if components is not None:
            warnings.append({
                'model_file': model_file,
                'kind': 'component_object_unsupported',
                'object_id': obj.get('id'),
                'name': obj.get('name'),
                'message': 'Component-based 3MF object found; direct mesh stats may be incomplete.',
            })

        mesh_el = obj.find(NS + 'mesh')
        if mesh_el is None:
            continue
        verts = []
        faces = []
        vs = mesh_el.find(NS + 'vertices')
        ts = mesh_el.find(NS + 'triangles')
        if vs is None or ts is None:
            warnings.append({
                'model_file': model_file,
                'kind': 'mesh_missing_vertices_or_triangles',
                'object_id': obj.get('id'),
                'name': obj.get('name'),
            })
            continue
        for v in vs.findall(NS + 'vertex'):
            verts.append([float(v.get('x')), float(v.get('y')), float(v.get('z'))])
        for t in ts.findall(NS + 'triangle'):
            faces.append([int(t.get('v1')), int(t.get('v2')), int(t.get('v3'))])
        mesh = trimesh.Trimesh(vertices=np.array(verts), faces=np.array(faces), process=True)
        rows.append({'object_id': obj.get('id'), 'name': obj.get('name'), 'model_file': model_file, 'stats': stats(mesh)})
    return rows, warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    out = {'input': args.input, 'objects': [], 'warnings': []}
    with zipfile.ZipFile(args.input) as zf:
        for info in zf.infolist():
            # Do not extract archive members. Read only model XML entries.
            normalized = info.filename.replace('\\', '/')
            if normalized.startswith('/') or '..' in normalized.split('/'):
                out['warnings'].append({'model_file': info.filename, 'kind': 'unsafe_zip_member_skipped'})
                continue
            if not normalized.endswith('.model'):
                continue
            rows, warnings = parse_model_bytes(zf.read(info), normalized)
            out['objects'].extend(rows)
            out['warnings'].extend(warnings)

    os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
