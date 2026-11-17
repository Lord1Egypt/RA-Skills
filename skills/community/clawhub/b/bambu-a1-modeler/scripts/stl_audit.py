#!/usr/bin/env python3
"""Audit basic geometry properties of binary or ASCII STL files without dependencies."""

from __future__ import annotations

import argparse
import json
import math
import re
import struct
import sys
from collections import Counter
from pathlib import Path

Vec = tuple[float, float, float]
Tri = tuple[Vec, Vec, Vec]


def parse_stl(path: Path) -> list[Tri]:
    data = path.read_bytes()
    if len(data) >= 84:
        count = struct.unpack_from("<I", data, 80)[0]
        if 84 + 50 * count == len(data):
            out: list[Tri] = []
            pos = 84
            for _ in range(count):
                vals = struct.unpack_from("<12fH", data, pos)
                out.append(((vals[3], vals[4], vals[5]),
                            (vals[6], vals[7], vals[8]),
                            (vals[9], vals[10], vals[11])))
                pos += 50
            return out

    text = data.decode("utf-8", errors="ignore")
    verts = [
        tuple(map(float, m))
        for m in re.findall(
            r"\bvertex\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)",
            text,
            flags=re.IGNORECASE,
        )
    ]
    if not verts or len(verts) % 3:
        raise ValueError("arquivo não parece ser STL binário nem ASCII válido")
    return [(verts[i], verts[i + 1], verts[i + 2]) for i in range(0, len(verts), 3)]


def sub(a: Vec, b: Vec) -> Vec:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross(a: Vec, b: Vec) -> Vec:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def dot(a: Vec, b: Vec) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def q(v: Vec, places: int = 6) -> Vec:
    return tuple(round(x, places) for x in v)  # type: ignore[return-value]


def audit(tris: list[Tri]) -> dict:
    if not tris:
        raise ValueError("STL sem triângulos")

    coords = [v for tri in tris for v in tri]
    mins = [min(v[i] for v in coords) for i in range(3)]
    maxs = [max(v[i] for v in coords) for i in range(3)]
    dims = [maxs[i] - mins[i] for i in range(3)]

    area = 0.0
    signed_volume = 0.0
    degenerate = 0
    edges: Counter[tuple[Vec, Vec]] = Counter()

    for a, b, c in tris:
        normal = cross(sub(b, a), sub(c, a))
        twice_area = math.sqrt(dot(normal, normal))
        if twice_area <= 1e-12:
            degenerate += 1
        area += 0.5 * twice_area
        signed_volume += dot(a, cross(b, c)) / 6.0
        qa, qb, qc = q(a), q(b), q(c)
        for u, v in ((qa, qb), (qb, qc), (qc, qa)):
            edges[tuple(sorted((u, v)))] += 1

    boundary = sum(1 for n in edges.values() if n == 1)
    nonmanifold = sum(1 for n in edges.values() if n > 2)
    warnings: list[str] = []
    if any(d > 256.0 + 1e-6 for d in dims):
        warnings.append("caixa envolvente excede 256 mm em pelo menos um eixo")
    if abs(mins[2]) > 0.01:
        warnings.append(f"base fora de Z=0 (Z mínimo {mins[2]:.3f} mm)")
    if degenerate:
        warnings.append(f"{degenerate} triângulo(s) degenerado(s)")
    if boundary:
        warnings.append(f"{boundary} aresta(s) de contorno: malha possivelmente aberta")
    if nonmanifold:
        warnings.append(f"{nonmanifold} aresta(s) não-manifold")
    if abs(signed_volume) <= 1e-9:
        warnings.append("volume assinado próximo de zero; verifique orientação/fechamento")

    return {
        "triangles": len(tris),
        "bbox_min_mm": [round(x, 6) for x in mins],
        "bbox_max_mm": [round(x, 6) for x in maxs],
        "dimensions_mm": [round(x, 6) for x in dims],
        "surface_area_mm2": round(area, 6),
        "signed_volume_mm3": round(signed_volume, 6),
        "absolute_volume_mm3": round(abs(signed_volume), 6),
        "boundary_edges": boundary,
        "nonmanifold_edges": nonmanifold,
        "degenerate_triangles": degenerate,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stl", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        result = audit(parse_stl(args.stl))
    except (OSError, ValueError, struct.error) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Arquivo: {args.stl}")
        print("Dimensões (X×Y×Z): " + " × ".join(f"{x:.3f}" for x in result["dimensions_mm"]) + " mm")
        print(f"Triângulos: {result['triangles']}")
        print(f"Volume absoluto: {result['absolute_volume_mm3']:.3f} mm³")
        print(f"Bordas abertas: {result['boundary_edges']}")
        print(f"Arestas não-manifold: {result['nonmanifold_edges']}")
        print(f"Triângulos degenerados: {result['degenerate_triangles']}")
        if result["warnings"]:
            print("Alertas:")
            for warning in result["warnings"]:
                print(f"- {warning}")
        else:
            print("Sem alertas geométricos básicos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
