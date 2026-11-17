# engineering-drawing-prep

[![Hermes Skill](https://img.shields.io/badge/Hermes-Skill-blue)]()
[![Version](https://img.shields.io/badge/version-0.1.0-green)]()

> Automated pre-design document preparation for engineering projects. Standardize client DWGs, audit deliverables, extract data tables, and generate RFIs — before you open Civil 3D or Revit.

---

## Problem

Every engineering project starts the same way: the client dumps a messy folder of DWGs, PDFs, Excel schedules, Word specs, and SHX fonts. The design team spends 2–3 days just sorting out what was actually sent, fixing broken references, unifying layers, and drafting RFIs for missing data.

This skill automates that grind.

## Capabilities

| Capability | Description |
|------------|-------------|
| **Intake Audit** | Inventory every file, strip macOS noise (`._*`, `.DS_Store`, `.dwl`), compute SHA-256 hashes, and flag unreadable or corrupted DWGs. |
| **Drawing Standardization** | Enforce unified layers, fonts, title blocks, and plot settings across all AutoCAD files, exporting standardized WIP DWGs and PDFs. |
| **Quality Audit** | Check file openability, external references, proxy objects, missing fonts, layout integrity, and visual anomalies — producing a structured QA report. |
| **Data Extraction** | Parse Excel/Word room lists, equipment schedules, lighting tables, and MEP specs into structured design interface registers. |
| **RFI Generation** | Identify missing surveys, CRS datums, control points, elevation benchmarks, and broken cross-references, then draft formal Request for Information documents. |
| **Traceable Archive** | Generate SHA-256 hashes, version manifests, and issue logs for every processed file — so you can prove "this is exactly what the client gave us" three months later. |

## Limitations (Honest)

This skill prepares the ground. It does **not** replace the designer or engineer.

- Does not create Civil 3D terrain, road, or drainage models.
- Does not author Revit/IFC models or perform clash detection.
- Does not perform load calculations, pipe sizing, or equipment selection.
- Does not produce statutory permit drawings or sealed construction documents.

## Quick Start

```bash
# 1. Place client deliverables in ./clientgiven/
mkdir -p clientgiven
# cp -r /path/to/client/deliverables/* clientgiven/

# 2. Run intake audit
bash scripts/01_intake_audit.sh ./clientgiven/

# 3. Standardize drawings
bash scripts/02_standardize.sh ./clientgiven/ ./output/wip/

# 4. Generate tables and RFI
python scripts/03_tabulate_and_rfi.py ./clientgiven/ ./output/
```

## Directory Structure

```
.
├── clientgiven/          # Raw client deliverables (read-only)
├── output/
│   ├── wip/              # Standardized DWGs + PDFs
│   ├── reports/          # QA audit reports
│   ├── tables/           # Extracted CSV/Excel registers
│   └── rfi/              # Generated RFI documents
├── scripts/              # Automation scripts
├── schemas/              # JSON schemas for registers and manifests
├── templates/            # Standard layer/font/title-block templates
└── references/           # Industry standards and field lessons
```

## Requirements

- **AutoCAD 2020+** (for Core Console batch processing)
- **Python 3.10+**
- `ezdxf` or `pyautocad` (optional, for non-AutoCAD environments)

## Industries

- EPC contracting (oil & gas, energy, infrastructure)
- Architecture and design institutes
- MEP installation and consulting
- Petrochemical and power generation
- International engineering (multi-standard, multi-language projects)

## License

MIT
