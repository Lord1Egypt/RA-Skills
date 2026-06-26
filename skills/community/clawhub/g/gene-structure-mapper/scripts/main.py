#!/usr/bin/env python3
"""
Gene Structure Mapper
Visualize gene exon-intron structure using the Ensembl REST API.
Outputs publication-ready SVG, PNG, or PDF figures.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

from typing import Dict, List, Optional

import requests
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

ENSEMBL_BASE = "https://rest.ensembl.org"
CACHE_DIR = Path(".cache")

# Hardcoded TP53 GRCh38 demo data (no internet required)
DEMO_DATA = {
    "id": "ENSG00000141510",
    "display_name": "TP53",
    "start": 7661779,
    "end": 7687538,
    "strand": -1,
    "Transcript": [
        {
            "id": "ENST00000269305",
            "is_canonical": 1,
            "Exon": [
                {"start": 7687377, "end": 7687538, "id": "ENSE00001657961"},
                {"start": 7676594, "end": 7676622, "id": "ENSE00003625790"},
                {"start": 7674181, "end": 7674290, "id": "ENSE00003518480"},
                {"start": 7673535, "end": 7673608, "id": "ENSE00003723991"},
                {"start": 7670609, "end": 7670715, "id": "ENSE00003625794"},
                {"start": 7669609, "end": 7669690, "id": "ENSE00003518478"},
                {"start": 7668421, "end": 7668562, "id": "ENSE00003625796"},
                {"start": 7667117, "end": 7667290, "id": "ENSE00003518479"},
                {"start": 7665985, "end": 7666069, "id": "ENSE00003625798"},
                {"start": 7661779, "end": 7663209, "id": "ENSE00001596491"},
            ],
            "UTR": [
                {"start": 7687377, "end": 7687538, "object_type": "five_prime_UTR"},
                {"start": 7661779, "end": 7661972, "object_type": "three_prime_UTR"},
            ],
        }
    ],
}


def get_cache_path(gene: str) -> Path:
    CACHE_DIR.mkdir(exist_ok=True)
    return CACHE_DIR / f"{gene}_ensembl.json"


def fetch_gene_data(gene: str, species: str) -> Optional[dict]:
    """Fetch gene structure from Ensembl REST API with caching."""
    cache_path = get_cache_path(gene)
    if cache_path.exists():
        with open(cache_path) as f:
            return json.load(f)

    url = f"{ENSEMBL_BASE}/lookup/symbol/{species}/{gene}"
    params = {"expand": 1, "content-type": "application/json"}

    for attempt in range(2):
        try:
            resp = requests.get(url, params=params, timeout=15)
            if resp.status_code in (400, 404):
                print(
                    f"Error: Gene not found: {gene}. Check the gene symbol and try again.",
                    file=sys.stderr,
                )
                sys.exit(1)
            resp.raise_for_status()
            data = resp.json()
            with open(cache_path, "w") as f:
                json.dump(data, f)
            time.sleep(0.1)
            return data
        except requests.exceptions.Timeout:
            if attempt == 0:
                time.sleep(1)
                continue
            print(
                "Error: Ensembl API request timed out. Check your connection and try again.",
                file=sys.stderr,
            )
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f"Error: Ensembl API request failed: {e}", file=sys.stderr)
            sys.exit(1)


def fetch_uniprot_domains(gene_id: str) -> list:
    """Fetch UniProt domain annotations for a gene via Ensembl xrefs."""
    url = f"{ENSEMBL_BASE}/xrefs/id/{gene_id}"
    params = {"content-type": "application/json", "external_db": "Uniprot/SWISSPROT"}
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        xrefs = resp.json()
        time.sleep(0.1)
    except Exception:
        return []

    domains = []
    for xref in xrefs[:1]:  # use first UniProt accession
        acc = xref.get("primary_id", "")
        if not acc:
            continue
        try:
            up_url = f"https://www.ebi.ac.uk/proteins/api/features/{acc}"
            up_resp = requests.get(
                up_url,
                headers={"Accept": "application/json"},
                timeout=15,
            )
            up_resp.raise_for_status()
            features = up_resp.json().get("features", [])
            for feat in features:
                if feat.get("type") == "DOMAIN":
                    domains.append(
                        {
                            "description": feat.get("description", "Domain"),
                            "begin": int(feat["begin"]),
                            "end": int(feat["end"]),
                        }
                    )
            time.sleep(0.1)
        except Exception:
            pass
    return domains


def pick_canonical_transcript(gene_data: dict) -> Optional[dict]:
    transcripts = gene_data.get("Transcript", [])
    for t in transcripts:
        if t.get("is_canonical"):
            return t
    return transcripts[0] if transcripts else None


def draw_gene_structure(
    gene_data: dict,
    output_path: str,
    fmt: str,
    domains: Optional[List[dict]] = None,
    mutations: Optional[List[int]] = None,
) -> None:
    """Draw gene model: exons as boxes, introns as lines, UTRs as lighter boxes."""
    transcript = pick_canonical_transcript(gene_data)
    if transcript is None:
        print("Error: No transcript data found for this gene.", file=sys.stderr)
        sys.exit(1)

    exons = sorted(transcript.get("Exon", []), key=lambda e: e["start"])
    utrs = transcript.get("UTR", [])
    utr_ranges = [(u["start"], u["end"]) for u in utrs]

    gene_start = gene_data["start"]
    gene_end = gene_data["end"]
    gene_len = gene_end - gene_start or 1

    fig, ax = plt.subplots(figsize=(12, 3))
    ax.set_xlim(0, gene_len)
    ax.set_ylim(-1, 2)
    ax.axis("off")

    gene_name = gene_data.get("display_name", gene_data.get("id", "Gene"))
    ax.set_title(f"{gene_name} — Gene Structure (canonical transcript)", fontsize=13, pad=10)

    # Draw intron backbone
    ax.plot([0, gene_len], [0.5, 0.5], color="#555555", lw=1.5, zorder=1)

    def is_utr(start: int, end: int) -> bool:
        for us, ue in utr_ranges:
            if start >= us and end <= ue:
                return True
        return False

    # Draw exons
    for exon in exons:
        rel_start = exon["start"] - gene_start
        rel_end = exon["end"] - gene_start
        width = max(rel_end - rel_start, gene_len * 0.003)
        utr = is_utr(exon["start"], exon["end"])
        color = "#aec6e8" if utr else "#2166ac"
        rect = mpatches.FancyBboxPatch(
            (rel_start, 0.15),
            width,
            0.7,
            boxstyle="square,pad=0",
            facecolor=color,
            edgecolor="#1a4a7a",
            linewidth=0.8,
            zorder=2,
        )
        ax.add_patch(rect)

    # Draw domain overlays
    if domains:
        cds_len = sum(e["end"] - e["start"] for e in exons)
        aa_to_bp = cds_len / max(gene_data.get("length", cds_len), 1)
        domain_colors = plt.cm.Set2.colors
        for i, dom in enumerate(domains):
            dom_start_bp = dom["begin"] * 3 * aa_to_bp
            dom_end_bp = dom["end"] * 3 * aa_to_bp
            rect = mpatches.FancyBboxPatch(
                (dom_start_bp, 0.05),
                max(dom_end_bp - dom_start_bp, gene_len * 0.01),
                0.9,
                boxstyle="square,pad=0",
                facecolor=domain_colors[i % len(domain_colors)],
                edgecolor="black",
                linewidth=0.6,
                alpha=0.45,
                zorder=3,
            )
            ax.add_patch(rect)
            ax.text(
                (dom_start_bp + dom_end_bp) / 2,
                1.05,
                dom["description"],
                ha="center",
                va="bottom",
                fontsize=6,
                color="#333333",
            )

    # Draw mutation markers
    if mutations:
        cds_len = sum(e["end"] - e["start"] for e in exons)
        bp_per_aa = cds_len / max(gene_data.get("length", cds_len / 3), 1)
        for pos in mutations:
            x = pos * 3 * bp_per_aa
            ax.axvline(x=x, ymin=0.1, ymax=0.9, color="red", lw=1.5, zorder=4)
            ax.text(x, 1.0, str(pos), ha="center", va="bottom", fontsize=7, color="red")

    # Legend
    legend_handles = [
        mpatches.Patch(facecolor="#2166ac", edgecolor="#1a4a7a", label="Exon"),
        mpatches.Patch(facecolor="#aec6e8", edgecolor="#1a4a7a", label="UTR"),
    ]
    if domains:
        legend_handles.append(
            mpatches.Patch(facecolor="#8da0cb", alpha=0.5, label="Domain")
        )
    if mutations:
        legend_handles.append(
            mpatches.Patch(facecolor="red", label="Mutation")
        )
    ax.legend(handles=legend_handles, loc="lower right", fontsize=8, framealpha=0.7)

    # Genomic coordinate labels
    ax.text(0, -0.3, f"{gene_start:,}", ha="left", va="top", fontsize=7, color="#666666")
    ax.text(gene_len, -0.3, f"{gene_end:,}", ha="right", va="top", fontsize=7, color="#666666")
    ax.text(gene_len / 2, -0.3, "Genomic position (bp)", ha="center", va="top", fontsize=8)

    plt.tight_layout()
    plt.savefig(output_path, format=fmt, dpi=150, bbox_inches="tight")
    plt.close()
    print(output_path)


def parse_mutations(mutations_str: str) -> List[int]:
    """Parse comma-separated codon positions; exit 1 on non-numeric values."""
    positions = []
    for part in mutations_str.split(","):
        part = part.strip()
        if not part:
            continue
        if not part.isdigit():
            print(
                "Error: --mutations must be comma-separated integers (codon positions).",
                file=sys.stderr,
            )
            sys.exit(1)
        positions.append(int(part))
    return positions


def main():
    parser = argparse.ArgumentParser(
        description="Gene Structure Mapper — visualize gene exon-intron structure"
    )
    parser.add_argument("--gene", "-g", help="Gene symbol or Ensembl ID (e.g. TP53, BRCA1)")
    parser.add_argument(
        "--species", default="homo_sapiens", help="Species name (default: homo_sapiens)"
    )
    parser.add_argument(
        "--format",
        default="png",
        choices=["png", "svg", "pdf"],
        help="Output format (default: png)",
    )
    parser.add_argument(
        "--output", "-o", default=None, help="Output file path (default: <gene>_structure.<format>)"
    )
    parser.add_argument(
        "--domains", action="store_true", help="Fetch and overlay UniProt domain annotations"
    )
    parser.add_argument(
        "--mutations",
        default=None,
        metavar="POSITIONS",
        help="Comma-separated codon positions to mark (e.g. 248,273)",
    )
    parser.add_argument(
        "--demo", action="store_true", help="Use BRCA1/TP53 demo data — no internet required"
    )
    args = parser.parse_args()

    if not args.demo and not args.gene:
        parser.error("--gene is required unless --demo is used. Example: --gene TP53")

    # Resolve gene data
    if args.demo:
        gene_data = DEMO_DATA
        gene_label = "TP53"
    else:
        gene_label = args.gene
        gene_data = fetch_gene_data(args.gene, args.species)
        if gene_data is None:
            print(f"Error: Gene not found: {args.gene}. Check the gene symbol and try again.", file=sys.stderr)
            sys.exit(1)

    # Resolve output path
    fmt = args.format
    output_path = args.output or f"{gene_label}_structure.{fmt}"

    # Parse mutations
    mutations = None
    if args.mutations:
        mutations = parse_mutations(args.mutations)

    # Fetch domains
    domain_list = None
    if args.domains and not args.demo:
        domain_list = fetch_uniprot_domains(gene_data.get("id", ""))

    draw_gene_structure(gene_data, output_path, fmt, domains=domain_list, mutations=mutations)


if __name__ == "__main__":
    main()
