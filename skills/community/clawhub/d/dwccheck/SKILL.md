---
name: dwccheck
description: Check a Darwin Core occurrence file (CSV or TSV) locally before uploading it to GBIF, using GBIF's own flag names. Use when asked to validate a Darwin Core or GBIF occurrence dataset, pre-check an occurrence file before upload, or find what GBIF would flag — for example "check this occurrence file before I upload to GBIF", "what would GBIF flag in this dataset", or "validate my Darwin Core CSV". Checks required terms, controlled vocabularies, dates, coordinates, duplicate occurrenceIDs, and country versus countryCode agreement — the subset of GBIF's checks that can be decided from the file alone. Not for ham-radio ADIF logs (that is adifcheck) or iCalendar (.ics) files (that is icslint).
license: MIT
compatibility: Requires Python 3.10+. No dependencies (standard library only) and runs fully offline; network is needed only to install.
---

# dwccheck

## What this tool does

dwccheck runs the file-decidable subset of GBIF's occurrence checks on a single Darwin Core CSV or TSV file, locally: required and recommended terms present, headers spelled as real Darwin Core terms, controlled vocabularies, date sanity and format, coordinate sanity, duplicate occurrenceIDs, and whether `country` and `countryCode` agree. Every per-record finding is reported under the same flag GBIF itself would use (for example `COORDINATE_INVALID`, `ZERO_COORDINATE`, `BASIS_OF_RECORD_INVALID`, `COUNTRY_MISMATCH`), with the row and term, so the file can be fixed before the real GBIF validator ever sees it. It only reads the file; it never uploads or changes anything.

## Install

```bash
pip install git+https://github.com/RakTikoo/dwccheck
```

This provides the `dwccheck` command.

## Run

Check one occurrence file:

```bash
dwccheck check occurrences.csv
```

The same findings in machine-readable form come from `--format json` or `--format csv` (one finding per object or row: row, flag, severity, term, value, message). A `.txt` input has its delimiter sniffed from its first line. To see every flag the tool can emit, with GBIF's definition of each:

```bash
dwccheck flags
```

## Reading the results

Findings print one per line: `row N: FLAG [term] — message` for record problems, or `file: FLAG [term] — message` for file-level problems. Row numbers are line numbers in the file (the header is row 1). The run ends with `summary: E error(s), W warning(s)` and a verdict line. Flags starting `DWCCHECK_` are this tool's own file-level codes (missing column, duplicate ID, unknown header) — GBIF has no per-record flag for those, and the names keep the two sets apart. The exit code is the verdict:

- `0` — no errors. The verdict line reads `result: PASS — no errors found.`, or `result: PASS — no errors (warnings above).` when warnings are listed; warnings are worth fixing but do not fail the run.
- `1` — errors found: `result: FAIL — fix the errors before uploading to GBIF.`
- `2` — the file cannot be checked at all (missing, empty, unreadable). File problems fail with clean one-line errors, never tracebacks.

## Limits

- No border or gazetteer checks: coordinates are never compared against any map, coastline or country boundary, so GBIF's `COUNTRY_COORDINATE_MISMATCH` and its negated-coordinate flags are not produced. Swapped coordinates are only flagged for the one signature decidable from the file alone (latitude outside ±90 that becomes valid when the pair is swapped); an in-range swapped pair cannot be told from a genuine record and is not claimed.
- No taxon matching: whether `scientificName` matches GBIF's taxonomic backbone needs GBIF's server. Offline, a name is only checked for being present.
- The bundled ISO country table answers one question only — do `country` and `countryCode` in the same row name the same country? An unusual but legitimate country-name spelling can still be flagged `COUNTRY_INVALID`; the code column is what GBIF keys on.
- One file, not an archive: Darwin Core Archives (zip with `meta.xml`) and multi-file datasets are not unpacked in this version.
- Footprint geometry is not judged: `footprintWKT` is checked for being interpretable WKT, but whether it contains the record's coordinates (`FOOTPRINT_WKT_MISMATCH`) is not attempted. Geological-context terms and DNA-sequence terms are not checked. Terms with no GBIF occurrence flag (for example `sex`, `lifeStage`) are not vocabulary-checked rather than checked under an invented flag, and a coordinate uncertainty of exactly 0 is not flagged.
