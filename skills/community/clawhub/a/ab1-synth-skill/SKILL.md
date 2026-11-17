---
name: ab1-synth-skill
description: Generate a synthetic Sanger .ab1 chromatogram from a reference FASTA (ASV/consensus) plus raw FASTQ reads, with realistic peak spacing/height/width, baseline noise and minor peaks, and a Chromas-compatible ABIF container. Use when a user asks to turn an ASV, OTU, consensus or FASTA sequence into an .ab1/ABIF/峰图 file, or asks to visualize amplicon reads as a Sanger trace.
---

# AB1 Synth Skill

Builds an `.ab1` file that opens in Chromas, FinchTV, SnapGene and Biopython.
Input is a reference sequence (e.g. one ASV from `asv_rep.fasta`) plus the
trimmed reads that support it; read variation and base qualities shape the
peaks.

**This is a simulated trace, not instrument data.** FASTQ contains no
fluorescence channels, so the chromatogram is reconstructed. Say so when the
result will be used as evidence.

## Quick start

```bash
python scripts/make_ab1.py \
  --fasta asv_rep.fasta --id ASV1 \
  --fastq trim.L9.fq.gz \
  --out ASV1.ab1
```

Optional: `--sample NAME`, `--seed N`, `--kmer 17`, `--open` (launch Chromas
on Windows), or omit `--fastq` for a reference-only trace.

## Pipeline

1. `load_target` — pick the FASTA record (`--id`, else first record).
2. `map_reads` — unique k-mer seeds vote for an offset; reads are accepted when
   they overlap at least half the reference and stay under the mismatch rate.
   Per-position base counts and Phred sums are accumulated.
3. `build_trace` — one peak per base with base-dependent spacing bias, jitter,
   quality-scaled height, asymmetric width, minor peaks from allele fractions,
   spectral pull-up, baseline drift, noise and a few dye bumps.
4. `write_abif` — ABIF container (see rules below).
5. `validate` — re-read with Biopython, compare base calls and channel lengths.

## ABIF rules that actually matter

- The file header is **34 bytes**: `ABIF` + version + `tdir` + number + element
  type + element size + element count + data size + data offset + **4-byte
  handle**. A 30-byte header makes Chromas report
  "not a recognised file type or the data is corrupted".
- Start payload at 128 and keep every data offset and the directory offset
  4-byte aligned.
- Sort directory entries by tag name, then tag number.
- Channel order is `FWO_1 = GATC`; `DATA1..4` are the raw channels in that
  order, `DATA9..12` the processed ones. Chromas displays `DATA1..4`.
- `PLOC2` must point at the real peak apexes, one entry per base.
- `PCON1/2` as element type 2 keeps Biopython happy (`abi` parser decodes it).
- `SMPL1` is a pString (type 18): a length byte followed by the name.

## Notes

- Reads often cover only part of the amplicon (e.g. ASV1 is 344 bp but reads
  start at base 31). Uncovered positions fall back to the reference sequence
  with default quality.
- If Chromas still refuses a file, compare its header/directory against a
  known-good `.ab1` (`struct.unpack(">H4sI2H3I4x", data[4:34])`).
- Requires Biopython. Python 3.9+.
