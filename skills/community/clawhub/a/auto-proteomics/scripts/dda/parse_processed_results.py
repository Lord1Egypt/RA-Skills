#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

META_COLUMNS = [
    'Protein IDs', 'Majority protein IDs', 'Protein names', 'Gene names',
    'Fasta headers', 'Potential contaminant', 'Reverse', 'Only identified by site'
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description='Standardize MaxQuant processed proteinGroups results')
    p.add_argument('--protein-groups', required=True)
    p.add_argument('--summary', required=True)
    p.add_argument('--parameters')
    p.add_argument('--output', required=True)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    with open(args.protein_groups, 'r', encoding='utf-8', newline='') as fh:
        reader = csv.DictReader(fh, delimiter='\t')
        fieldnames = reader.fieldnames or []
        quant_cols = [c for c in fieldnames if c.startswith('LFQ intensity ') or c.startswith('Intensity ')]
        if not quant_cols:
            raise SystemExit('No LFQ intensity or Intensity columns found in proteinGroups.txt')
        keep = [c for c in META_COLUMNS if c in fieldnames] + quant_cols
        out_fields = []
        rename = {
            'Protein IDs': 'protein_id',
            'Majority protein IDs': 'majority_protein_id',
            'Protein names': 'protein_name',
            'Gene names': 'gene_name',
            'Fasta headers': 'description',
            'Potential contaminant': 'is_contaminant',
            'Reverse': 'is_reverse',
            'Only identified by site': 'only_site',
        }
        for field in keep:
            out_fields.append(rename.get(field, field))
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, 'w', encoding='utf-8', newline='') as out_fh:
            writer = csv.DictWriter(out_fh, fieldnames=out_fields, delimiter='\t')
            writer.writeheader()
            for row in reader:
                writer.writerow({rename.get(k, k): row.get(k, '') for k in keep})
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
