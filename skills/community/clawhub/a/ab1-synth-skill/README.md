# ab1-synth-skill

Turn a reference sequence (ASV / OTU / consensus FASTA) plus its supporting
reads into a **synthetic Sanger `.ab1` chromatogram** that opens in Chromas,
FinchTV, SnapGene and Biopython.

FASTQ files contain no fluorescence channels, so the trace is reconstructed:
read variation supplies minor peaks, Phred scores drive peak heights, and peak
spacing/width/baseline are modelled to look like a real electropherogram.
**The result is simulated data, not instrument output.**

## Requirements

- Python 3.9+
- Biopython (`pip install biopython`)

## Usage

```bash
python scripts/make_ab1.py \
  --fasta asv_rep.fasta \
  --id ASV1 \
  --fastq trim.L9.fq.gz \
  --out ASV1.ab1
```

| Option | Meaning |
| --- | --- |
| `--fasta` | reference FASTA |
| `--id` | sequence id to use (default: first record) |
| `--fastq` | reads for peak variation (FASTQ/FASTA, `.gz` supported); optional |
| `--out` | output `.ab1` |
| `--sample` | `SMPL1` sample name |
| `--seed` | random seed for reproducible traces |
| `--open` | open the result in Chromas on Windows |

Output is validated by re-reading it with Biopython: base calls must match the
reference and all eight trace channels must have equal length.

## How it works

1. Unique 17-mers from the reference vote for a read offset; reads must cover at
   least half the reference and stay below a 4% mismatch rate.
2. Per-position base counts and quality sums are accumulated.
3. Peaks are drawn with base-dependent spacing and height, asymmetric Gaussian
   shape, spectral pull-up, baseline drift, noise and a few dye bumps.
4. A valid ABIF container is written.

## ABIF gotchas

- Header is **34 bytes** (it includes a 4-byte handle). A 30-byte header makes
  Chromas report *"not a recognised file type or the data is corrupted"*.
- Payload starts at 128; every data offset and the directory offset must be
  4-byte aligned.
- Directory entries are sorted by tag name, then number.
- `FWO_1 = GATC` defines the channel order of `DATA1..4`.

