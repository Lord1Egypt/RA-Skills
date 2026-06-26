#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description='Two-group differential protein analysis')
    p.add_argument('--matrix', required=True)
    p.add_argument('--metadata', required=True)
    p.add_argument('--group-a', required=True)
    p.add_argument('--group-b', required=True)
    p.add_argument('--output-all', required=True)
    p.add_argument('--output-significant', required=True)
    return p.parse_args()


def to_float(value: str) -> float | None:
    if value in ('', None):
        return None
    try:
        return float(value)
    except Exception:
        return None


def mean(values: list[float]) -> float | None:
    vals = [v for v in values if v is not None]
    if not vals:
        return None
    return sum(vals) / len(vals)


def variance(values: list[float], avg: float) -> float | None:
    vals = [v for v in values if v is not None]
    if len(vals) < 2:
        return None
    return sum((v - avg) ** 2 for v in vals) / (len(vals) - 1)


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def approx_p_value(a: list[float], b: list[float]) -> float | None:
    a = [v for v in a if v is not None]
    b = [v for v in b if v is not None]
    if len(a) < 2 or len(b) < 2:
        return None
    mean_a = mean(a)
    mean_b = mean(b)
    var_a = variance(a, mean_a)
    var_b = variance(b, mean_b)
    if var_a is None or var_b is None:
        return None
    denom = math.sqrt(var_a / len(a) + var_b / len(b))
    if denom == 0:
        return 1.0
    z = abs((mean_b - mean_a) / denom)
    return max(0.0, min(1.0, 2 * (1 - normal_cdf(z))))


def bh_adjust(rows: list[dict[str, object]]) -> None:
    indexed = []
    for i, row in enumerate(rows):
        p = row['p_value']
        indexed.append((i, 1.0 if p in (None, '') else float(p)))
    indexed.sort(key=lambda x: x[1])
    n = len(indexed)
    adjusted = [1.0] * n
    cumulative = 1.0
    for j in range(n - 1, -1, -1):
        idx, p = indexed[j]
        rank = j + 1
        cumulative = min(cumulative, p * n / rank)
        adjusted[j] = cumulative
    for (j, (idx, _)) in enumerate(indexed):
        rows[idx]['adj_p_value'] = adjusted[j]


def main() -> int:
    args = parse_args()
    with open(args.metadata, 'r', encoding='utf-8', newline='') as fh:
        metadata = list(csv.DictReader(fh, delimiter='\t'))
    group_map = {row['sample_id']: row['condition'] for row in metadata}
    with open(args.matrix, 'r', encoding='utf-8', newline='') as fh:
        reader = csv.DictReader(fh, delimiter='\t')
        fields = reader.fieldnames or []
        group_a_samples = [c for c in fields if group_map.get(c) == args.group_a]
        group_b_samples = [c for c in fields if group_map.get(c) == args.group_b]
        if not group_a_samples or not group_b_samples:
            raise SystemExit('Both comparison groups must have at least one sample')
        rows = []
        for row in reader:
            a = [to_float(row.get(s, '')) for s in group_a_samples]
            b = [to_float(row.get(s, '')) for s in group_b_samples]
            mean_a = mean(a)
            mean_b = mean(b)
            log2fc = '' if mean_a is None or mean_b is None else mean_b - mean_a
            pval = approx_p_value(a, b)
            rows.append({
                'protein_id': row['protein_id'],
                'mean_group_a': '' if mean_a is None else mean_a,
                'mean_group_b': '' if mean_b is None else mean_b,
                'log2fc': log2fc,
                'p_value': '' if pval is None else pval,
            })
    bh_adjust(rows)
    for row in rows:
        row['direction'] = 'ns'
        if row['adj_p_value'] < 0.05 and row['log2fc'] != '':
            if row['log2fc'] > 1.0:
                row['direction'] = 'up'
            elif row['log2fc'] < -1.0:
                row['direction'] = 'down'
    Path(args.output_all).parent.mkdir(parents=True, exist_ok=True)
    fields = ['protein_id', 'mean_group_a', 'mean_group_b', 'log2fc', 'p_value', 'adj_p_value', 'direction']
    with open(args.output_all, 'w', encoding='utf-8', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)
    with open(args.output_significant, 'w', encoding='utf-8', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter='\t')
        writer.writeheader()
        writer.writerows([r for r in rows if r['direction'] != 'ns'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
