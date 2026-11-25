---
name: fitspeek
description: Turn FITS image files into contact-sheet PNGs — a grid of thumbnails stamped with filename, OBJECT, DATE-OBS, filter and exposure time, with a north/east compass where the WCS carries a CD or PC matrix, plus an index.csv mapping every thumbnail back to its source file. Use when asked to preview or triage a night's FITS images, make contact sheets or thumbnails from FITS files, or eyeball a pile of frames at a glance. Not for building a night-log CSV from FITS headers (use fitslog), planning an observing night (use tonight), or converting observation times to BJD_TDB (use bjd).
license: MIT
compatibility: Requires Python 3.10+ with Astropy, NumPy and Matplotlib. Installing needs network access to GitHub; the tool itself runs fully offline.
---

# fitspeek

## What this tool does

fitspeek renders a pile of FITS image files into contact-sheet PNGs:
grids of thumbnails, each stamped with its filename and key header info,
so a night's images can be triaged at a glance instead of opened one by
one. An `index.csv` maps every collected file to its sheet and tile, or
records that it was skipped and why.

## Install

```bash
pip install git+https://github.com/RakTikoo/fitspeek
```

This provides the `fitspeek` command.

## Run

```bash
fitspeek make /data/night1 --out sheets/ --cols 3
fitspeek make frame001.fits frame002.fits --out sheets/ --cols 2
```

- Inputs can be folders (all FITS files directly inside are used),
  individual files, or a mix. Folder inputs are not recursive.
- Each sheet holds `--cols` × `--cols` thumbnails, written as
  `sheet_001.png`, `sheet_002.png`, … into the `--out` folder
  (default `sheets/`).
- The first HDU holding image data is the one rendered; cubes are
  median-combined across all planes into a single image first. Every
  thumbnail uses a ZScale stretch (with a percentile fallback) and gets
  a north/east compass when the header carries a CD or PC matrix.

## Reading the results

Exit code `0` means the command ran — it does **not** mean every file
was rendered. Judge the run by the printed summary: a `skipped:` line
per skipped file with its reason, then `Rendered: N`, `Skipped: M`
(with a reason breakdown), and how many sheets were written. Files with
no image data, zero-size images, all-NaN images and corrupt files are
skipped with a reason; one bad file never stops the batch. A nonexistent
input path is noted ("does not exist, ignoring") and also does not stop
the batch — a run can exit 0 having rendered nothing, so always check
the counts.

`index.csv` in the output folder is the durable record: one row per
collected FITS file with `source_file, sheet, tile, status, reason`,
where `status` is `rendered` or `skipped`. Non-FITS files inside a
folder argument are not collected and do not appear.

Exit code `2` is a usage error (for example no inputs given); nothing
was rendered.

## Limits

- Folder inputs are not recursive — subfolders are not scanned.
- The stamp reads `OBJECT`, `DATE-OBS`, `FILTER`, `EXPTIME` only,
  spelled exactly that way; instrument variants (such as `FILTER1` or
  `EXPOSURE`) are not normalised.
- The compass needs a CD or PC matrix; a header with only
  `CDELT`/`CROTA` gets no compass.
- Sheets are for triage, not measurement: thumbnails are stretched for
  visibility, not photometrically faithful.
- Large images are rendered in memory as-is; there is no downsampling
  step before the stretch.
- `--cols` has no upper bound; very large values produce very large,
  slow sheets.
