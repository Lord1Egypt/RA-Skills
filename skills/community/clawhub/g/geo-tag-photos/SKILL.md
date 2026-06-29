---
name: geo-tag-photos
description: >
  Recover lost GPS metadata for JPG photos by recognizing landmarks via vision
  and writing GPS coordinates back into EXIF. Default dry-run; explicit --write
  with --backup-dir is required to modify files. Global coverage via Nominatim
  (OpenStreetMap), no API keys.
version: 1.0.1
author: ucsdzehualiu
license: MIT
trigger_keywords:
  - geo-tag-photos
  - photo geolocation
  - 照片定位
  - 推断拍摄地点
  - EXIF GPS 写入
  - geotag photos
  - recover photo location
---

# geo-tag-photos

Recover GPS metadata for JPG photos. The model identifies landmarks visually,
the script geocodes those landmarks via Nominatim (OpenStreetMap) and writes
the coordinates back into EXIF.

## Use only on your own photos

This skill infers location from visual content. **Do not** use it to track
other people, surveil private individuals, or de-anonymize photos that were
intentionally stripped of location data. Inferred coordinates are best-guess
estimates and **must not** be used for legal, forensic, evidentiary, or
law-enforcement purposes.

## What it can and cannot do

| Can | Cannot |
|---|---|
| Identify global public landmarks (Eiffel, Opera House, Taj Mahal …) | Identify ordinary streets, residences, interiors, plain portraits, generic nature |
| Reach city- / landmark-level precision | Provide street- or building-level precision |
| Process JPG / JPEG | Process HEIC / PNG / TIFF / RAW (convert first) |
| Write GPS + ImageDescription + UserComment | Modify any other EXIF field |
| Handle a few hundred photos at a time | Reliably batch thousands (rate limits + cache hit-rate degrade) |

## Setup

```bash
cd <skill-folder>
pip install -r requirements.txt
```

The script will refuse to run if any of `piexif`, `Pillow`, `requests` is
missing.

## Workflow (5 phases)

You must walk the user through these phases in order. Each phase has a clear
output the user can inspect.

### Phase 1: scan

Identify which photos already have GPS (skip them) and which need inference.

```bash
python scripts/photo_geolocator.py scan --dir <photos> --out exif_status.csv
```

Read the CSV: any row with `note=NO_GPS` is a candidate for inference.
Anything with `note=NOT_JPG` must be skipped (or converted by the user first).

### Phase 2: AI vision (you do this directly)

For every JPG with `NO_GPS`, use the `Read` tool to view the image and extract:

- `landmark` — the landmark name (e.g. "Eiffel Tower"). If no recognizable
  landmark, leave empty.
- `city` — best-guess city, or empty.
- `country` — best-guess country, or empty.
- `confidence` — `high` / `medium` / `low`. Be honest. `low` rows will be
  skipped on write by default.
- `evidence` — short text: visual cues you used (architecture style, signage
  language, flags, geography).

Aggregate into a JSON file `ai_results.json`:

```json
[
  {"filename": "p1.jpg", "landmark": "Eiffel Tower", "city": "Paris",
   "country": "France", "confidence": "high", "evidence": "Iron lattice tower visible"},
  {"filename": "p2.jpg", "landmark": "", "city": "", "country": "",
   "confidence": "low", "evidence": "interior, no landmarks"}
]
```

Photos with no recognizable landmark: set `confidence: low` and empty
strings. The pipeline will skip them on write.

### Phase 3: geocode

```bash
python scripts/photo_geolocator.py geocode --input ai_results.json --out geocoded.csv
```

This calls Nominatim (rate-limited to 1 req / 1.1 s) and caches results
locally. Failures are recorded in the CSV — they do not stop the run.

### Phase 4: report

```bash
python scripts/photo_geolocator.py report \
  --dir <photos> --geocoded geocoded.csv --out report.csv
```

The report shows every photo and what action will be taken: `WRITE`,
`SKIP_HAS_GPS`, `SKIP_NOT_JPG`, `SKIP_LOW_CONFIDENCE`, `SKIP_NO_GEOCODE`,
`SKIP_AI_UNKNOWN`.

**Show the report path to the user. Tell them to review it. Wait for explicit
confirmation before phase 5.**

### Phase 5: write (only after user confirms)

First, dry-run to print the planned changes (no files modified):

```bash
python scripts/photo_geolocator.py write --dir <photos> --csv report.csv
```

Then, after user confirmation, the real write:

```bash
python scripts/photo_geolocator.py write --dir <photos> --csv report.csv \
  --write --backup-dir <photos>.bak
```

`--backup-dir` is mandatory and the script refuses if it's non-empty or
inside the source directory. Maximum 500 photos per invocation.

After writing, run `scan` again and compare to the report. The script also
verifies internally and reports any roundtrip mismatches.

## Hard limits enforced by the script

- JPG-only — non-JPG files are listed in scan but never written
- `--write` without `--backup-dir` → exit code 2
- Backup dir must be empty or non-existent → exit code 2
- Backup dir cannot be inside source dir → exit code 2
- Maximum 500 photos per `write` invocation → exit code 2
- `confidence: low` rows skipped unless `--include-low`
- Photos that already have GPS skipped unless `--overwrite-existing` (with
  warning)

## Privacy

The script sends only text (`landmark, city, country`) to Nominatim.
**Photos never leave your machine via the script.** The AI vision step
happens inside your Claude session; whether the photos leave the machine for
that step is governed by your Claude setup, not by this skill.

## Troubleshooting

- **Geocoding returns wrong coordinates.** Nominatim is fuzzy with ambiguous
  names (e.g. "Springfield"). Refine the AI step: include city + country
  with the landmark.
- **Cache holds bad entries.** `python scripts/photo_geolocator.py cache --clear`
- **`exif_io.EXIFError: not a JPG`.** Convert your HEIC / PNG / TIFF / RAW to
  JPG first (e.g. `magick mogrify -format jpg *.heic`).
- **Many photos report SKIP_AI_UNKNOWN.** Phase 2 didn't emit entries for
  every photo — re-run vision for the missing ones.
