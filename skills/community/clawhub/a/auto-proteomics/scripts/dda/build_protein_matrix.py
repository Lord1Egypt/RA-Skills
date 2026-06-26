#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description='Build standardized protein abundance matrix from proteinGroups and summary')
    p.add_argument('--standardized', required=True)
    p.add_argument('--summary', required=True)
    p.add_argument('--output-matrix', required=True)
    p.add_argument('--output-metadata', required=True)
    return p.parse_args()


def clean_sample_name(column: str) -> str:
    for prefix in ('LFQ intensity ', 'Intensity '):
        if column.startswith(prefix):
            return column[len(prefix):]
    return column


def main() -> int:
    args = parse_args()
    with open(args.standardized, 'r', encoding='utf-8', newline='') as fh:
        reader = csv.DictReader(fh, delimiter='\t')
        fields = reader.fieldnames or []
        quant_cols = [c for c in fields if c.startswith('LFQ intensity ') or c.startswith('Intensity ')]
        if not quant_cols:
            raise SystemExit('No quantitative columns found in standardized table')
        sample_names = [clean_sample_name(c) for c in quant_cols]
        rows = []
        for row in reader:
            if row.get('is_contaminant') == '+' or row.get('is_reverse') == '+' or row.get('only_site') == '+':
                continue
            out = {'protein_id': row.get('protein_id', '')}
            for qcol, sample in zip(quant_cols, sample_names):
                out[sample] = row.get(qcol, '')
            rows.append(out)

    metadata_rows = []
    with open(args.summary, 'r', encoding='utf-8', newline='') as fh:
        reader = csv.DictReader(fh, delimiter='\t')
        counts = {}
        for row in reader:
            sample_id = str(row.get('Raw file', '')).strip()
            condition = str(row.get('Experiment', '')).strip() or sample_id
            if sample_id and sample_id in sample_names:
                counts[condition] = counts.get(condition, 0) + 1
                metadata_rows.append({
                    'sample_id': sample_id,
                    'condition': condition,
                    'replicate': counts[condition],
                    'enzyme': row.get('Enzyme', ''),
                    'variable_modifications': row.get('Variable modifications', ''),
                    'fixed_modifications': row.get('Fixed modifications', ''),
                })
    if not metadata_rows:
        counts = {}
        for sample in sample_names:
            counts[sample] = counts.get(sample, 0) + 1
            metadata_rows.append({'sample_id': sample, 'condition': sample, 'replicate': counts[sample]})

    valid_samples = {row['sample_id'] for row in metadata_rows}
    trimmed_rows = []
    for row in rows:
        trimmed = {'protein_id': row['protein_id']}
        for sample in sample_names:
            if sample in valid_samples:
                trimmed[sample] = row.get(sample, '')
        trimmed_rows.append(trimmed)

    Path(args.output_matrix).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output_matrix, 'w', encoding='utf-8', newline='') as fh:
        fields = ['protein_id'] + [s for s in sample_names if s in valid_samples]
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter='\t')
        writer.writeheader()
        writer.writerows(trimmed_rows)

    Path(args.output_metadata).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output_metadata, 'w', encoding='utf-8', newline='') as fh:
        fields = list(metadata_rows[0].keys()) if metadata_rows else ['sample_id', 'condition', 'replicate']
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter='\t')
        writer.writeheader()
        writer.writerows(metadata_rows)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
