---
name: bjd
description: Convert a column of observation times in a CSV or FITS table to BJD_TDB (barycentric Julian date, TDB). The input format (jd, mjd or iso) and time scale (utc, tt, tai or tdb) must be stated explicitly — the tool refuses to guess either. Use when asked to convert times to BJD or BJD_TDB, correct observation times to the solar-system barycentre, or prepare exoplanet transit timing tables. Not for cross-matching catalogues from different epochs (use epochmatch), deciding which targets are observable tonight (use tonight), or auditing FITS headers (use fitslog).
license: MIT
compatibility: Requires Python 3.10+ and Astropy 6+. Installing needs network access to GitHub; the tool itself runs fully offline (built-in ephemeris, network downloads disabled).
---

# bjd

## What this tool does

bjd batch-converts one time column in a CSV or FITS table to BJD_TDB and
writes the table back with a `bjd_tdb` column appended, plus a printed
summary showing how large the correction was. It refuses to run unless the
input format and time scale are stated explicitly: a wrong assumption does
not crash, it silently shifts every time by seconds to over a minute.

## Install

```bash
pip install git+https://github.com/RakTikoo/bjd
```

This provides the `bjd` command. Verify an install any time with
`bjd check`, which recomputes a built-in reference case and prints PASS
when the computed BJD_TDB matches the expected value.

## Run

```bash
bjd convert times.csv --time-col jd_utc --format jd --scale utc --ra 84.291188 --dec -20.273999 --site "-24.6272,-70.4042,2635" --out times_bjd.csv
```

- `--time-col` names the column holding the observation times.
- `--format` is `jd`, `mjd` or `iso` — required, never guessed. A trailing
  `Z` on ISO strings is refused; state the scale instead.
- `--scale` is `utc`, `tt`, `tai` or `tdb` — required, never guessed.
- `--ra`, `--dec` are the target coordinates in degrees (ICRS); there is
  no default, because the correction is a projection onto the target
  direction.
- `--site` is the observatory as `"lat,lon,height_m"` — latitude first.
  Named observatories are not accepted; give coordinates.
- All input columns are carried through. Output format follows the
  `--out` suffix (`.csv` or `.fits`); without `--out` the output is
  `<input-name>_bjd.csv` next to the input.

## Reading the results

Exit code `0` means the conversion ran. The summary prints the time-column
mapping (`jd_utc (jd, UTC) -> bjd_tdb (BJD_TDB)`), the target, the site as
parsed, and the median shift applied with its min/max — that shift
includes the scale offset (TDB−UTC is about 69 s in recent years) plus the
light-travel term (at most about 500 s). Read the site line and the shift
before trusting the output: both are printed so a wrong assumption is
visible.

Exit code `2` means the tool refused or failed — a missing `--format` or
`--scale`, a missing column, a malformed site, an unreadable file. The
error is one clean explanation, never a traceback, and no converted
output should be used.

## Limits

- Built-in ephemeris precision: the light-travel time is accurate to well
  under 0.1 s. For sub-second transit timing for publication, cross-check
  critical epochs against a JPL-ephemeris tool such as barycorrpy.
- One target and one site per run; a mixed-target table needs one run per
  target.
- Mid-exposure times are your responsibility: the tool converts the times
  it is given, so add half the exposure first if the column holds
  exposure-start times.
- No relativistic (Shapiro) delay and no proper-motion correction of the
  target.
- The sub-0.1 s precision claim covers roughly 1900–2100; outside that
  range the tool still converts but prints a warning.
- A swapped `--site` that stays in range cannot be caught: if both
  numbers are plausible as latitude or longitude, the conversion succeeds
  with the wrong site and a plausible-looking correction. Only
  out-of-range swaps are refused — check the printed site line.
