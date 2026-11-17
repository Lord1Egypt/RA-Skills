---
name: engineering-drawing-prep
description: Automated pre-design document preparation for engineering projects. Standardize client DWGs, audit deliverables, extract data tables, and generate RFIs before real design begins.
version: 0.1.0
author: MCLYang <gy86@cornell.edu>
tags:
  - engineering
  - cad
  - autocad
  - dwg
  - pdf
  - standardization
  - audit
  - rfi
  - epc
  - mep
  - infrastructure
  - document-management
---

# engineering-drawing-prep

> Automated pre-design document preparation for engineering projects. Standardize client DWGs, audit deliverables, extract data tables, and generate RFIs — before you open Civil 3D or Revit.

## What It Does

| Stage | Input | Output |
|-------|-------|--------|
| Intake | Raw client folder (DWG, PDF, XLSX, DOCX, SHX) | Inventory manifest + SHA-256 hashes |
| Standardization | Heterogeneous DWGs with mismatched layers/fonts/title blocks | Unified WIP DWGs + PDFs |
| Audit | Unvetted CAD files | QA report: proxy objects, missing refs, font issues, layout errors |
| Tabulation | Scattered Excel/Word schedules | Structured room, equipment, lighting, and MEP interface registers |
| RFI | Identified gaps (missing survey, CRS, benchmarks, broken refs) | Formal Request for Information documents |
| Archive | All processed files | Versioned, hashed, traceable WIP package |

## What It Does NOT Do

- Does not create Civil 3D terrain, road, or drainage models.
- Does not author Revit/IFC models or perform clash detection.
- Does not perform load calculations, pipe sizing, or equipment selection.
- Does not produce statutory permit drawings or sealed construction documents.

## Quick Start

```bash
# Place client deliverables in ./clientgiven/
# Run the intake audit
bash scripts/01_intake_audit.sh ./clientgiven/

# Standardize drawings
bash scripts/02_standardize.sh ./clientgiven/ ./output/wip/

# Generate tables and RFI
python scripts/03_tabulate_and_rfi.py ./clientgiven/ ./output/
```

## Requirements

- AutoCAD 2020+ (for Core Console batch processing)
- Python 3.10+
- ezdxf / pyautocad (optional, for non-AutoCAD environments)

## Project Structure

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

## License

MIT
