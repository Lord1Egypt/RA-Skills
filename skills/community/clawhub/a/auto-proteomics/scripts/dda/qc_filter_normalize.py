#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description='QC, filter, and normalize protein abundance matrix')
    p.add_argument('--matrix', required=True)
    p.add_argument('--metadata', required=True)
    p.add_argument('--group-a', required=True)
    p.add_argument('--group-b', required=True)
    p.add_argument('--min-replicates', type=int, default=2)
    p.add_argument('--min-valid-values', type=int, default=2)
    p.add_argument('--missingness-threshold', type=float, default=0.7)
    p.add_argument('--pseudocount', type=float, default=1.0)
    p.add_argument('--output-filtered', required=True)
    p.add_argument('--output-log2norm', required=True)
    p.add_argument('--qc-dir', required=True)
    return p.parse_args()


def to_float(value: str) -> float | None:
    if value in ('', '0', None):
        return None
    try:
        return float(value)
    except Exception:
        return None


def median(values: list[float]) -> float | None:
    vals = sorted(v for v in values if v is not None)
    if not vals:
        return None
    n = len(vals)
    mid = n // 2
    if n % 2:
        return vals[mid]
    return (vals[mid - 1] + vals[mid]) / 2.0


def main() -> int:
    args = parse_args()
    metadata = []
    with open(args.metadata, 'r', encoding='utf-8', newline='') as fh:
        for row in csv.DictReader(fh, delimiter='\t'):
            if row.get('condition') in (args.group_a, args.group_b):
                metadata.append(row)
    if not metadata:
        raise SystemExit('No samples found for requested groups')
    samples = [row['sample_id'] for row in metadata]
    group_map = {row['sample_id']: row['condition'] for row in metadata}
    group_a_samples = [s for s in samples if group_map.get(s) == args.group_a]
    group_b_samples = [s for s in samples if group_map.get(s) == args.group_b]
    if not group_a_samples or not group_b_samples:
        raise SystemExit('Both comparison groups must have at least one sample')

    sample_missing = {s: 0 for s in samples}
    total_rows = 0
    filtered_rows = []
    all_missing = []
    with open(args.matrix, 'r', encoding='utf-8', newline='') as fh:
        for row in csv.DictReader(fh, delimiter='\t'):
            total_rows += 1
            values = {s: to_float(row.get(s, '')) for s in samples}
            miss_fraction = sum(v is None for v in values.values()) / max(1, len(samples))
            all_missing.append({'protein_id': row['protein_id'], 'missing_fraction': miss_fraction})
            for s, v in values.items():
                if v is None:
                    sample_missing[s] += 1
            enough_a = sum(values[s] is not None for s in group_a_samples) >= min(args.min_valid_values, len(group_a_samples))
            enough_b = sum(values[s] is not None for s in group_b_samples) >= min(args.min_valid_values, len(group_b_samples))
            if miss_fraction <= args.missingness_threshold and (enough_a or enough_b):
                filtered_rows.append({'protein_id': row['protein_id'], **values})

    log2_rows = []
    sample_medians = {}
    for s in samples:
        vals = [math.log2(r[s] + args.pseudocount) for r in filtered_rows if r[s] is not None]
        sample_medians[s] = median(vals)
    valid_medians = [v for v in sample_medians.values() if v is not None]
    global_median = median(valid_medians) if valid_medians else 0.0

    for row in filtered_rows:
        out = {'protein_id': row['protein_id']}
        for s in samples:
            if row[s] is None:
                out[s] = ''
            else:
                value = math.log2(row[s] + args.pseudocount)
                med = sample_medians[s] if sample_medians[s] is not None else global_median
                out[s] = value - med + global_median
        log2_rows.append(out)

    qc_dir = Path(args.qc_dir)
    qc_dir.mkdir(parents=True, exist_ok=True)
    with open(qc_dir / 'missingness_by_sample.tsv', 'w', encoding='utf-8', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=['sample_id', 'missing_fraction'], delimiter='\t')
        writer.writeheader()
        for s in samples:
            writer.writerow({'sample_id': s, 'missing_fraction': sample_missing[s] / max(1, total_rows)})
    with open(qc_dir / 'missingness_by_protein.tsv', 'w', encoding='utf-8', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=['protein_id', 'missing_fraction'], delimiter='\t')
        writer.writeheader()
        writer.writerows(all_missing)
    with open(qc_dir / 'sample_summary.tsv', 'w', encoding='utf-8', newline='') as fh:
        fields = ['sample_id', 'condition', 'replicate', 'median_log2_abundance']
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter='\t')
        writer.writeheader()
        for row in metadata:
            writer.writerow({
                'sample_id': row['sample_id'],
                'condition': row['condition'],
                'replicate': row.get('replicate', ''),
                'median_log2_abundance': sample_medians.get(row['sample_id'], ''),
            })

    fields = ['protein_id'] + samples
    Path(args.output_filtered).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output_filtered, 'w', encoding='utf-8', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter='\t')
        writer.writeheader()
        for row in filtered_rows:
            writer.writerow({k: ('' if v is None else v) for k, v in row.items()})
    with open(args.output_log2norm, 'w', encoding='utf-8', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter='\t')
        writer.writeheader()
        writer.writerows(log2_rows)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
