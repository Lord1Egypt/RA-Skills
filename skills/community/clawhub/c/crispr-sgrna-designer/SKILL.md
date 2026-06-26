---
name: crispr-sgrna-designer
description: Professional-grade CRISPR sgRNA design for viral and microbial genomes, with specialized logic for extreme-GC templates (e.g., Herpesviruses). Use when needing to design high-efficiency, low-off-target sgRNAs for (1) Gene knockouts, (2) Site-specific insertions/tagging, or (3) Precise genome editing. Includes PAM scanning, position-weight scoring (Rule Set 2 style), and synonymous mutation strategy for donor template design. Designed by ZJU PhD @ Bio-chat.
---

# CRISPR sgRNA Designer (Bio-chat Series)

This skill provides a rigorous workflow for designing and scoring CRISPR/Cas9 sgRNAs, specifically optimized for high-GC viral genomes where standard tools often struggle.

## Key Capabilities

1. **Precision PAM Scanning**: Automated scanning of target regions for SpCas9 (NGG) and alternative PAMs.
2. **GC-Weighted Scoring**: Specialized weighting for high-GC templates (65-80% GC) to ensure thermodynamic stability of the R-loop.
3. **Positional Analysis**: Calculates cut sites relative to functional features (ATG start codons, stop codons, or exon junctions).
4. **Off-target Defense**: Rapid genomic indexing to ensure seed-region (12bp) uniqueness in small viral/microbial genomes.
5. **Donor Template Strategy**: Automatically suggests synonymous mutations to prevent re-cutting of integrated donor sequences.

## Workflow

1. **Target Identification**: Provide a genomic region or gene name (e.g., PRV UL15 N-terminus).
2. **Sequence Extraction**: Automatically pulls the latest reference sequences via NCBI E-utils.
3. **sgRNA Generation**: Runs a sliding window scan for NGG PAMs within the target window.
4. **On-target Scoring**:
   - **Position Weighting**: Rewards specific nucleotides in the seed region.
   - **GC Penalty/Reward**: Optimizes for the high-GC context of viruses like PRV.
5. **Result Ranking**: Provides a ranked list of sgRNAs with comprehensive scoring (0-100) and experimental recommendations.

## Technical Standards

- **Scoring Model**: Modified Rule Set 2 logic adapted for extreme sequence contexts.
- **Seed Region**: Strict 12bp specificity check.
- **PAM Requirement**: 5'-NGG-3' (Standard SpCas9).

*Designed by ZJU PhD @ Bio-chat Community*
