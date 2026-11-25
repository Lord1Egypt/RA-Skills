---
name: epochmatch
description: Cross-match two star catalogues measured at different epochs (CSV, VOTable or FITS tables), propagating positions to a common epoch with proper motions (pmra, pmdec) before matching, so stars that moved still match. Use when asked to cross-match, join or compare two catalogues from different years or epochs, match a catalogue against Gaia, or find counterparts for stars with proper motion. Not for barycentric time conversion (use bjd), FITS header audits (use fitslog), planning tonight's observing (use tonight), or FITS contact sheets (use fitspeek).
license: MIT
compatibility: Requires Python 3.10+ with Astropy, NumPy and SciPy. Installing needs network access to GitHub; the tool itself runs fully offline.
---

# epochmatch

## What this tool does

epochmatch cross-matches two star catalogues from different epochs. It moves
both catalogues to one shared epoch using their proper motions, then matches
by position, and reports which pairs matched, which did not, and which were
too close to call (ambiguous). It never guesses a match when several
candidates fall inside the radius.

## Install

```bash
pip install git+https://github.com/RakTikoo/epochmatch
```

This provides the `epochmatch` command.

## Run

```bash
epochmatch catalogue_a.csv catalogue_b.fits --epoch-a 2000.0 --epoch-b 2015.5 --to-epoch 2016.0 --radius 2.0 --out result
```

- Both `--epoch-a` and `--epoch-b` are required (decimal years). `--to-epoch`
  defaults to the later of the two epochs; `--radius` is in arcsec
  (default 2.0).
- Inputs can be CSV, VOTable or FITS tables, mixed freely.
- Columns are `ra`, `dec` in degrees and `pmra`, `pmdec` in mas/yr
  (pm_ra_cosdec convention). Rename them with `--ra-col`, `--dec-col`,
  `--pmra-col`, `--pmdec-col`; `--id-a` / `--id-b` name an ID column (default: the row number).
- `--propagated-columns` adds each side's propagated position at the common
  epoch to the matched output.

## Reading the results

The command prints a four-line summary (`Matched`, `Ambiguous`,
`Unmatched in A`, `Unmatched in B`) and writes four CSV files:

- `<out>_matched.csv` — one row per matched pair, with `sep_arcsec` at the
  common epoch plus both rows' coordinate and proper-motion columns.
- `<out>_unmatched_a.csv` / `<out>_unmatched_b.csv` — rows with no candidate.
- `<out>_ambiguous.csv` — one row per candidate pair, with a `reason` (for
  example `multiple_candidates_within_radius`). Ambiguous pairs are
  reported, never silently resolved: a non-empty file means those pairs
  still need a decision; they are not matches.

Exit code `0` means the run completed — read the summary counts, not just
the exit code, because a completed run can still have unmatched and
ambiguous rows. Exit code `2` means the run failed (missing file, missing
required flag, unreadable table): the error is printed as one clean line and no output should be trusted.

If a catalogue has no proper-motion columns, its positions are matched
as-is and a warning is printed. Rows with missing or non-finite coordinates
or proper motions are counted in a warning and reported as unmatched.

## Limits

- Directions only: propagation uses proper motions, not parallax or radial
  velocity; very nearby, very fast stars over long baselines would need a
  full space-motion treatment to be accurate.
- Units are fixed by convention: degrees and mas/yr, pm_ra_cosdec. There
  are no unit-conversion flags; convert columns first if they differ.
- Ambiguity is positional only — no probabilistic or magnitude-aware
  matching.
- Not built for billion-row surveys: matching is an in-memory KD-tree,
  comfortable for thousands to millions of rows, not a Gaia-scale join.
- In dense fields the ambiguous file grows quadratically (N×N candidate
  rows when N stars on each side share one radius).
- Output coordinate columns are the original catalogue values by default,
  not the propagated ones; separations are at the common epoch. For a
  catalogue without proper-motion columns, its proper-motion columns in
  the matched output are NaN, not a fabricated 0.0.
