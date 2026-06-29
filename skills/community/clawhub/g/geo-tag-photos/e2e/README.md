# End-to-end test

This harness validates the full pipeline against 8 real public-domain
landmark photos.

## Setup

```bash
cd geo-tag-photos
pip install -r requirements.txt
python e2e/fetch_landmarks.py
```

That downloads 8 photos to `e2e/landmarks/` and strips their EXIF (so the
pipeline sees the same "GPS-lost" input a real user has).

`e2e/landmarks/` and `e2e/landmarks.bak/` are gitignored.

## Run the pipeline

```bash
# Phase 1: scan — all 8 should report NO_GPS
python scripts/photo_geolocator.py scan \
  --dir e2e/landmarks --out e2e/exif_status.csv

# Phase 2: AI vision — done in a Claude session.
# Build e2e/ai_results.json by hand or via Claude. Or: copy
# e2e/canonical_coords.json into ai_results.json and add confidence=high.

# Phase 3: geocode (real Nominatim call — be patient, ~10 s)
python scripts/photo_geolocator.py geocode \
  --input e2e/ai_results.json --out e2e/geocoded.csv

# Phase 4: report
python scripts/photo_geolocator.py report \
  --dir e2e/landmarks --geocoded e2e/geocoded.csv --out e2e/report.csv

# Phase 5a: dry-run
python scripts/photo_geolocator.py write \
  --dir e2e/landmarks --csv e2e/report.csv

# Phase 5b: real write (with backup)
python scripts/photo_geolocator.py write \
  --dir e2e/landmarks --csv e2e/report.csv \
  --write --backup-dir e2e/landmarks.bak
```

## Verify the result

```bash
python e2e/verify.py
```

Pass criteria: each of the 8 photos has GPS within 5 km of
`canonical_coords.json`, and `e2e/landmarks.bak/` contains 8 untagged copies.
