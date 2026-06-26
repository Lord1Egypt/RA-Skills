#!/usr/bin/env python3
"""
Bubble Plot Generator for Gene Expression Data
Reads a TSV/CSV expression matrix and generates bubble (dot) plots.
Each plot: x = cancerType, y = cellType, color = scaled avg expression, size = % positive cells.
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import argparse


# ── Column auto-detection ──────────────────────────────────────────────

METADATA_KEYWORDS = {
    'cell_type': ['majorcluster', 'cell_type', 'celltype', 'cell type', 'cluster',
                  'cell_annot', 'cellannot', 'cell_annotation', 'celllabel', 'cell_label'],
    'tissue':    ['tissue', 'class', 'condition', 'sample_type', 'group', 'source'],
    'cancer_type': ['cancertype', 'cancer_type', 'cancer type', 'cancer', 'disease',
                    'tumor_type', 'tumortype', 'project', 'dataset'],
}

TISSUE_NORMALIZE = {
    'adjacent': 'normal',
    'normal': 'normal',
    'healthy': 'normal',
    'control': 'normal',
    'para': 'normal',
    'tumor': 'tumor',
    'cancer': 'tumor',
}


def detect_columns(df):
    """Auto-detect cell_type, tissue, cancer_type columns. Returns dict."""
    cols_lower = {c.lower().strip(): c for c in df.columns}
    result = {}
    for role, keywords in METADATA_KEYWORDS.items():
        for kw in keywords:
            if kw in cols_lower:
                result[role] = cols_lower[kw]
                break
    return result


def detect_gene_columns(df, meta_cols):
    """All numeric columns that are NOT metadata = gene columns."""
    meta_set = set(meta_cols.values())
    genes = []
    for col in df.columns:
        if col in meta_set:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            genes.append(col)
    return genes


# ── Plotting ───────────────────────────────────────────────────────────

def plot_bubble(data, gene_col, gene_name, cell_col, cancer_col, tissue_label=""):
    """Create one bubble plot."""
    grouped = data.groupby([cancer_col, cell_col])[gene_col].agg(
        Total='count',
        Positive=lambda x: (x > 0).sum(),
        AvgExpr='mean'
    ).reset_index()

    grouped['PctExpr'] = grouped['Positive'] / grouped['Total'] * 100

    max_expr = grouped['AvgExpr'].max()
    if max_expr == 0:
        max_expr = 1
    grouped['AvgExpr_Scaled'] = grouped['AvgExpr'] / max_expr

    cancer_types = sorted(grouped[cancer_col].unique())
    cell_types = sorted(grouped[cell_col].unique())

    x_map = {ct: i for i, ct in enumerate(cancer_types)}
    y_map = {ct: i for i, ct in enumerate(cell_types)}

    grouped['x'] = grouped[cancer_col].map(x_map)
    grouped['y'] = grouped[cell_col].map(y_map)

    fig, ax = plt.subplots(figsize=(max(10, len(cancer_types) * 0.5),
                                    max(5, len(cell_types) * 0.45)))

    scatter = ax.scatter(
        grouped['x'], grouped['y'],
        c=grouped['AvgExpr_Scaled'],
        s=grouped['PctExpr'] * 8,
        cmap=plt.cm.RdBu_r,
        vmin=0, vmax=1,
        edgecolors='gray', linewidths=0.3, alpha=0.9
    )

    cbar = plt.colorbar(scatter, ax=ax, shrink=0.8, pad=0.02)
    cbar.set_label(f'Scaled avg {gene_name} expression', fontsize=9)

    # Size legend
    pct_vals = [10, 25, 50, 75]
    handles = [plt.scatter([], [], s=pv * 8, c='gray', alpha=0.6,
                           edgecolors='gray', linewidths=0.3) for pv in pct_vals]
    ax.legend(handles, [f'{pv}%' for pv in pct_vals],
              title=f'{gene_name}+ cell fraction',
              loc='upper left', bbox_to_anchor=(1.15, 0.5),
              frameon=True, fontsize=8, title_fontsize=9, labelspacing=1.2)

    ax.set_xticks(range(len(cancer_types)))
    ax.set_xticklabels(cancer_types, rotation=45, ha='right', fontsize=8)
    ax.set_yticks(range(len(cell_types)))
    ax.set_yticklabels(cell_types, fontsize=9)
    ax.set_xlabel(cancer_col, fontsize=10, fontweight='bold')
    ax.set_ylabel(cell_col, fontsize=10, fontweight='bold')

    title = f'{gene_name}'
    if tissue_label:
        title += f' - {tissue_label}'
    ax.set_title(title, fontsize=12, fontweight='bold')

    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.5)

    ax.grid(False)
    fig.tight_layout()
    return fig


# ── Main ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Bubble plot generator for gene expression data')
    parser.add_argument('input', help='Input TSV or CSV file')
    parser.add_argument('--genes', '-g', nargs='+', default=None,
                        help='Gene names to plot (default: auto-detect all numeric non-metadata columns)')
    parser.add_argument('--tissue-col', default=None, help='Override tissue column name')
    parser.add_argument('--cell-col', default=None, help='Override cell type column name')
    parser.add_argument('--cancer-col', default=None, help='Override cancer type column name')
    parser.add_argument('--split-tissue', action='store_true', default=True,
                        help='Split plots by tissue type (default: True)')
    parser.add_argument('--no-split-tissue', dest='split_tissue', action='store_false')
    parser.add_argument('--outdir', '-o', default='bubble_plots', help='Output directory')
    parser.add_argument('--dpi', type=int, default=300, help='PNG DPI')
    parser.add_argument('--width', type=float, default=10, help='Figure width in inches')
    parser.add_argument('--height', type=float, default=7, help='Figure height in inches')
    args = parser.parse_args()

    # Read data
    print(f"Reading {args.input} ...")
    sep = '\t' if args.input.endswith('.tsv') else ','
    df = pd.read_csv(args.input, sep=sep)
    # If first column looks like row names (unnamed), drop it
    if df.columns[0].startswith('Unnamed') or df.columns[0] == '':
        df = pd.read_csv(args.input, sep=sep, index_col=0)
    print(f"  {df.shape[0]:,} rows, {df.shape[1]} columns")

    # Detect columns
    meta = detect_columns(df)
    print(f"  Detected metadata: {meta}")

    # Apply overrides
    if args.cell_col:
        meta['cell_type'] = args.cell_col
    if args.tissue_col:
        meta['tissue'] = args.tissue_col
    if args.cancer_col:
        meta['cancer_type'] = args.cancer_col

    # Validate required columns
    if 'cell_type' not in meta:
        print("ERROR: Cannot detect cell type column. Use --cell-col to specify.")
        print(f"  Available columns: {list(df.columns)}")
        sys.exit(1)
    if 'cancer_type' not in meta:
        print("ERROR: Cannot detect cancer type column. Use --cancer-col to specify.")
        print(f"  Available columns: {list(df.columns)}")
        sys.exit(1)

    # Detect gene columns
    if args.genes:
        gene_cols = args.genes
        missing = [g for g in gene_cols if g not in df.columns]
        if missing:
            print(f"ERROR: Gene columns not found: {missing}")
            print(f"  Available: {[c for c in df.columns if c not in meta.values()]}")
            sys.exit(1)
    else:
        gene_cols = detect_gene_columns(df, meta)
        print(f"  Auto-detected {len(gene_cols)} gene columns")

    if not gene_cols:
        print("ERROR: No gene columns found.")
        sys.exit(1)

    # Normalize tissue values
    if 'tissue' in meta:
        tcol = meta['tissue']
        df[tcol] = df[tcol].astype(str).str.lower().map(
            lambda v: TISSUE_NORMALIZE.get(v, v)
        )
        tissue_values = sorted(df[tcol].unique())
    else:
        tissue_values = ['all']
        df['_all'] = 'all'
        meta['tissue'] = '_all'

    tcol = meta['tissue']
    cell_col = meta['cell_type']
    cancer_col = meta['cancer_type']

    # Output
    os.makedirs(args.outdir, exist_ok=True)
    files_written = []

    for gene in gene_cols:
        for tissue_val in tissue_values:
            label = tissue_val if tissue_val != 'all' else ''
            print(f"  Plotting {gene}{' - ' + label if label else ''} ...")

            data_sub = df[df[tcol] == tissue_val].copy()
            if len(data_sub) == 0:
                print(f"    No data, skipping")
                continue

            fig = plot_bubble(data_sub, gene, gene, cell_col, cancer_col, label)

            base = f"{gene}_dotplot"
            if label:
                base += f"_{label}"

            png_path = os.path.join(args.outdir, f"{base}.png")
            pdf_path = os.path.join(args.outdir, f"{base}.pdf")

            fig.savefig(png_path, dpi=args.dpi, bbox_inches='tight', facecolor='white')
            fig.savefig(pdf_path, bbox_inches='tight', facecolor='white')
            plt.close(fig)
            files_written.extend([png_path, pdf_path])

    # Summary
    print(f"\nDone! {len(files_written)} files in {args.outdir}/")
    for f in sorted(files_written):
        print(f"  {f} ({os.path.getsize(f) / 1024:.1f} KB)")


if __name__ == '__main__':
    main()
