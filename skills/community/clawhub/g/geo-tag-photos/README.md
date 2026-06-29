# geo-tag-photos

> Recover lost GPS metadata for JPG photos by recognizing landmarks via
> vision, then writing GPS coordinates back into EXIF.

This is a [ClawHub](https://clawhub.app) Claude skill, mirrored on GitHub.
Use it when you have a directory of JPGs whose GPS got stripped by
backups / phone exports / cloud sync, and the photos contain recognizable
landmarks.

## Use only on your own photos

This skill infers location from visual content. Do not use it to track
people, surveil others, or de-anonymize photos that were intentionally
stripped of location data. Inferred coordinates are best-guess estimates
and **must not** be used for legal, forensic, or evidentiary purposes.

## Install

```bash
git clone https://github.com/ucsdzehualiu/my_openclaw_skill.git
cd my_openclaw_skill/geo-tag-photos
pip install -r requirements.txt
```

Or via ClawHub CLI:

```bash
clawhub install geo-tag-photos
```

## Quickstart

The skill drives Claude through a 5-phase workflow. From a Claude Code
session in a folder containing JPG photos:

```
> use geo-tag-photos to add GPS to my photos in ~/photos
```

Claude will:

1. Scan the directory.
2. Look at each photo and propose `landmark / city / country / confidence`.
3. Geocode the inferences via Nominatim.
4. Build a `report.csv`. **It will pause here and ask you to review.**
5. After your confirmation, write GPS into EXIF (with mandatory backup).

## What it can do

- Recognize global public landmarks (Eiffel Tower, Sydney Opera House, Taj
  Mahal, etc.)
- City- / landmark-level GPS precision
- Process JPG / JPEG (HEIC / PNG / TIFF / RAW: convert first)

## What it cannot do

- Identify ordinary streets, residences, interiors, plain portraits, generic
  nature
- Provide street- or building-level precision
- Modify any EXIF field other than the four we explicitly write
  (`GPSLatitude`, `GPSLongitude`, `ImageDescription`, `UserComment`)

## Safety: dry-run by default

The `write` subcommand is dry-run by default. Real writes require **both**
`--write` **and** `--backup-dir`. The script refuses if:

- `--backup-dir` is missing
- the backup directory is non-empty
- the backup directory is inside the source directory
- more than 500 photos would be written in one go
- the photo isn't a JPG

After every successful write, the script reads the GPS back and reports any
roundtrip mismatches.

## Privacy

The script sends only text (`landmark, city, country`) to Nominatim. **It
never uploads photos.** The AI vision step happens inside your Claude
session; whether photos leave the machine in that step is governed by your
Claude setup, not by this skill.

## Manual CLI

If you want to drive the script outside a Claude session:

```bash
# 1. Scan
python scripts/photo_geolocator.py scan --dir ~/photos --out exif_status.csv

# 2. Build ai_results.json yourself (or by hand-editing — schema in SKILL.md)

# 3. Geocode
python scripts/photo_geolocator.py geocode \
  --input ai_results.json --out geocoded.csv

# 4. Build report
python scripts/photo_geolocator.py report \
  --dir ~/photos --geocoded geocoded.csv --out report.csv

# 5. Dry-run
python scripts/photo_geolocator.py write --dir ~/photos --csv report.csv

# 6. Real write (after reviewing report)
python scripts/photo_geolocator.py write --dir ~/photos --csv report.csv \
  --write --backup-dir ~/photos.bak

# Cache maintenance
python scripts/photo_geolocator.py cache --show
python scripts/photo_geolocator.py cache --clear
```

## Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

End-to-end test on real public landmark photos:

```bash
python e2e/fetch_landmarks.py        # downloads 8 public-domain landmarks
# follow e2e/README.md for the rest
```

## License

MIT — see `LICENSE`.
