# Changelog

All notable changes to `eplan-drawing-parser` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-20

### Added
- **Unified entry point** `scripts/parse_eplan.py`:
  - Parse any EPLAN/CAD vector PDF into per-page components + wire counts
  - Reference-designator classification (QF/FU/SPD/KM/X/..., PLC modules, AGH/CHA)
  - Annotated preview PNG overlay (`--preview`)
  - Console summary report
  - JSON output (default `<name>.json`)
- **Low-level extractor** `scripts/extract_geom.py`:
  - Vector wire geometry extraction (per-line start/end coordinates)
  - Text + coordinate extraction (model numbers, designators, values)
  - Wire-endpoint ↔ component-terminal matching for topology reconstruction
- **Domain knowledge** `knowledge/eplan_symbols.md`:
  - EPLAN reference-designator prefix → component-type mapping
  - Designator numbering conventions
  - Wire gauge/color conventions (main power vs signal)
- **Examples & docs**: `examples/README.md`, `README.md` (EN/中文), this file.

### Fixed
- Reference designators with leading prefix symbols (`-FU1001`, `\QF201`) are now
  correctly recognized by stripping leading `-\\/ .~` characters.

### Known limitations (v1.0.0)
- Requires **vector** PDF (text layer + vector lines). Scanned/image PDFs out of scope.
- Layout/assembly-drawing pages (component silhouettes) produce inflated wire counts
  (e.g. a parts-layout page may show ~100k line objects), but text designators are
  still extracted accurately.
- Cross-page connections (`至AGHxx` / `TO AGHxx`) require multi-page association
  (planned in v1.1.0).

## [Unreleased]

### Added (v1.1.0)
- **BOM cross-check** `scripts/check_bom.py`:
  - Cross-check EPLAN vector PDF vs Excel bill of materials (UL证书汇总)
  - Reference-designator (位号), model-number (型号), and quantity (数量) verification
  - Missing UL-file-number (UL档案号) detection with 型号↔供应商↔UL mapping check
  - Auto strip EPLAN leading `-` from designators; auto-detect `UL` sheet
  - Export colored xlsx with「位号核对 / 无UL档案号」sheets
- **Dependency**: added `openpyxl` (Excel read/write)
- SKILL.md: added BOM cross-check section + trigger keywords

## [1.0.0] - 2026-08-20
