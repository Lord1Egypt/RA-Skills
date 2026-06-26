---
name: driver-card-tachograph
description: Parses EU Digital Tachograph driver card files (.ddd) and imports data into SQLite. Use when working with driver card data, tachograph records, or digital tachograph files for: (1) Parsing .ddd files to JSON, (2) Importing tachograph data into SQLite, (3) Exporting driving activities to CSV, (4) Analyzing driver hours, violations, or vehicle usage
---

# driver-card-tachograph

Parses EU Digital Tachograph driver card files (.ddd) and imports data into a SQLite database.

## Description

Processes EU Digital Tachograph files (.ddd):

- **.ddd files:** Binary driver card dumps
- **Parser:** `dddparser` (EU certified)
- **Database:** SQLite with 13 tables

### Certificates

See [references/certificates.md](references/certificates.md) for details on EU JRC public keys and signature verification.

## Commands

| Command | Description |
|---------|-------------|
| `./scripts/process.sh` | Full workflow (recommended) |
| `./bin/dddparser -card -format -input <file.ddd> -output <file.json>` | .ddd → JSON |
| `./scripts/import.py <file.json>` | JSON → SQLite |
| `./scripts/export.py` | SQLite → CSV |

## Directory Structure

```
driver-card-tachograph/
├── SKILL.md
├── bin/dddparser          # Parser
├── scripts/
│   ├── import.py
│   ├── export.py
│   └── process.sh
├── references/
│   ├── build.md           # Build guide
│   └── certificates.md    # Certificate details
└── data/                  # Runtime
```

## Requirements

- **Go 1.21+** – to build the parser
- **Python 3** – standard library (sqlite3, json, csv)

### Build dddparser

See [references/build.md](references/build.md) for the build guide.

### .ddd Files

- **Location:** `data/inbox/`
- **Extension:** `.ddd` (case-insensitive)
- **Min size:** 1KB

## Workflow

```bash
./scripts/process.sh
```

1. Take .ddd from `inbox/`
2. Parse to JSON (`parsed/`)
3. Import to SQLite (`json/` → DB)
4. Archive to `archive/`