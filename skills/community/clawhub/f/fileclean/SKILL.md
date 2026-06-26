# FileClean

Cleans filename clutter by removing date timestamps, hashes, UUIDs, and excessive symbols, transforming messy filenames like `report_20230101_a1b2c3d.pdf` into clean, readable ones like `Report.pdf`.

## Usage

Preview changes:
```bash
python fileclean.py ~/Downloads ~/Documents --skip-ext pdf jpg
```

Apply changes:
```bash
python fileclean.py myfile.txt --rename
```

## Price

$2.75
