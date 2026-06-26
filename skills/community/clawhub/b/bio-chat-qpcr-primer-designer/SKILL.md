---
name: rtqpcr-primer-design
description: Advanced RT-qPCR primer and probe design with specialized support for cross-species homology mapping (e.g., Human to Vero cells) and high-GC virus optimization. Use when needing to design high-specificity qPCR assays for: (1) Standard Human/Mouse/Monkey transcripts, (2) Predicted transcripts (XM_) lacking exon data via homology mapping, (3) High-GC viral templates (e.g., PRV), or (4) SYBR Green and TaqMan probe-based assays. Designed by ZJU PhD.
---

# RT-qPCR Primer Design (Bio-chat Series)

This skill provides a professional-grade workflow for designing high-specificity RT-qPCR primers and probes, optimized for complex biological samples.

## Key Capabilities

1. **Homology-based Junction Mapping**: Automatically maps exon-exon junctions from a well-annotated ortholog (e.g., Human NM_) to a predicted target transcript (e.g., Vero XM_) to ensure gDNA-safe design even when annotations are missing.
2. **High-GC Template Optimization**: Specialized algorithms for templates with >70% GC content (e.g., Pseudorabies virus), automatically adjusting primer length and Tm weight to ensure specificity.
3. **SYBR & TaqMan Support**: Designs optimized primer pairs for SYBR Green and triplex/probe sets for TaqMan assays with precise Tm matching.

## Workflow

1. **Target Identification**: Provide a NCBI Accession (NM_/XM_) or a local FASTA sequence.
2. **Homology Mapping (Optional)**: For predicted monkey transcripts, provide a Human ortholog Accession to activate "Hardcore Mode" for exon junction mapping.
3. **Automated Design**: Execute `scripts/design_qpcr_assay.py` with specific parameters:
   - `--target`: Target accession
   - `--homolog`: Human ortholog for mapping
   - `--offtarget`: Accession for 3' specificity check
4. **Validation**: Review the top-scoring primer/probe sets based on Tm, GC, 3' quality, and secondary structure.

## Technical Standards

- **Tm Calculation**: Nearest-Neighbor (NN) model.
- **gDNA Defense**: Primers must span or flank exon-exon junctions.
- **3' Quality**: Strict control of 3' GC-clamp and mismatch prevention.

*Designed by ZJU PhD @ Bio-chat Community*
