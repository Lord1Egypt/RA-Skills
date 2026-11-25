---
name: fitslog
description: Turn a folder tree of telescope FITS files into one night-log CSV with header keywords normalised across instruments (EXPTIME/EXPOSURE/EXPT, OBJECT/TARGET/OBJNAME and more), plus an audit flagging corrupt files, missing fields, duplicated keywords and headers with no WCS. Use when asked to build a night log, catalogue or inventory a folder of FITS files, summarise an observing night, or check FITS headers for problems. Not for rendering FITS files as contact-sheet images (use fitspeek), converting observation times to BJD_TDB (use bjd), or cross-matching catalogues (use epochmatch).
license: MIT
compatibility: Requires Python 3.10+ and Astropy. Installing needs network access to GitHub; the tool itself runs fully offline and reads headers only.
---

# fitslog

## What this tool does

fitslog scans a folder tree of FITS files — headers only, image data is
never loaded — and writes one night-log CSV with the same columns for
every file, normalising the keyword spellings different instruments use
for the same thing. A second, optional audit CSV flags the problem
files: corrupt files, missing fields, duplicated keywords, no WCS.

## Install

```bash
pip install git+https://github.com/RakTikoo/fitslog
```

This provides the `fitslog` command.

## Run

```bash
fitslog scan /data/night1 --out nightlog.csv --audit audit.csv
```

- The scan recurses all subfolders. Files ending in `.fits`, `.fit` or
  `.fts` (any case) are scanned, including compressed forms (`.fits.gz`,
  `.bz2`, `.xz`, fpack `.fits.fz`).
- `--audit` is optional; the printed summary and flagged-file list appear either way.
- One row per file appears in the night log — including corrupt files,
  which get a mostly-empty row and an audit entry. A corrupt file never
  stops the scan.

## Reading the results

The night log's columns are `file, folder, date_obs, object, filter,
exptime_s, instrument, telescope, ra_deg, dec_deg, airmass, observer,
image_type`. `folder` is relative to the folder scanned. `date_obs` is
copied as written in the header (not re-formatted); RA/Dec come out as
decimal degrees, with sexagesimal strings converted.

Exit code `0` means the scan completed — it does **not** mean the files
were clean. The verdict is in the printed summary (`Files scanned`,
`Rows written`, `Flagged files`, top flags, then the flagged-file list)
and in the audit CSV, which has one row per flag with a `detail` column.
The flags are: `unreadable` (not openable as FITS at all), `missing_object`,
`missing_date`, `missing_exptime`, `duplicate_keyword` (detail names the
keyword; the first value is the one logged), `no_wcs`, and
`invalid_coordinate` (that axis is left empty in the log, never filled
with raw text).

Exit code `2` means the scan itself failed — for example the path is not
a directory. The error is printed as one clean line and no output should
be trusted.

## Limits

- Headers only: fitslog cannot tell you a frame is clouded out or out of
  focus. A file whose data section is corrupt but whose header is intact
  scans cleanly; only files unopenable as FITS are flagged `unreadable`.
- Values are not range-checked: a negative exposure time or an
  out-of-range coordinate is logged as written. Only unparseable
  coordinates are flagged.
- `date_obs` is not normalised beyond choosing between the two spellings;
  two instruments can still write different date formats.
- One row per file, from one header (the primary header, or the first
  extension header carrying a recognised keyword if the primary carries
  none). Per-extension logging of multi-extension mosaics is out of scope.
- The alias table covers common spellings, not every observatory. A
  missing spelling shows up as empty columns, made visible by the
  missing-field flags rather than silently.
- WCS detection is a presence check (CD, PC or CDELT keywords), not a
  validity check — a header can carry WCS keywords that are still wrong.
