# RT-qPCR Primer Design Guidelines

## 1. Physicochemical Properties
- **Length**: 18-24 bp.
- **Tm**: 58-62 °C (Difference between F and R < 2 °C).
- **GC Content**: 45-60%.
- **3' End**: Avoid G/C clusters (more than 3 G or C in the last 5 bases) to prevent mispriming.
- **Self-Complementarity**: Avoid hairpins and primer-dimers (Delta G > -5 kcal/mol).

## 2. Specificity (The 3' Mismatch Rule)
To distinguish highly homologous genes (e.g., DDX3X vs DDX3Y):
- **Placement**: Place the 3' end of the primer exactly on a divergent nucleotide.
- **Taq Inhibition**: A mismatch at the last (3' terminal) or penultimate position significantly inhibits Taq polymerase extension on the unintended template.

## 3. Genomic DNA (gDNA) Prevention
- **Exon-Exon Junction**: Design primers that span the junction of two exons.
- **Intron Spanning**: Ensure the forward and reverse primers are in different exons, separated by a large intron (>1kb), so that any contaminating gDNA results in an amplicon too large for standard qPCR extension times.

## 4. TaqMan Probe Design (Advanced)
To design a high-quality fluorogenic probe (e.g., FAM-TAMRA):
- **Location**: The probe must sit between the Forward and Reverse primers.
- **Tm**: The probe Tm should be **8-10 °C higher** than the primer Tm (typically 68-70 °C) to ensure it binds before the primers extend.
- **Length**: Usually 13-30 bp.
- **Nucleotide Content**: 
    - No G at the 5' end (G acts as a quencher and reduces signal).
    - Avoid consecutive G runs (more than 3 Gs).
    - GC content should be 30-80%.
