# cad-viewer — CAD DWG/DXF Drawing Analysis Skill

Professional-grade CAD drawing reading and analysis tool, designed to run as an AI Agent Skill. Through 13 CLI subcommands, AI Agents can structurally read, query, analyze, and visualize AutoCAD DWG/DXF format engineering drawings.

## Feature Overview

| Capability | Description |
|------------|-------------|
| Drawing Info Extraction | Version, units, layer/block/entity statistics |
| Layer & Entity Query | Filter by type, layer, full-text search support |
| Text Content Extraction | TEXT, MTEXT, block attributes |
| Spatial Distance Calculation | Entity-to-entity, coordinate-to-coordinate distances |
| Screenshot Visualization | Generate PNG/PDF/SVG by block name/layer/region |
| Compliance Audit | Zero-layer violations, empty layers, DEFPOINTS checks |
| PDF Export | Export drawings to vector PDF |
| Automated Environment Setup | One-command setup with explicit confirmation (`setup --confirm`) |

All commands output structured **JSON** for direct AI Agent parsing.

---

## System Requirements

- **OS**: Linux x86_64 (Ubuntu/Debian/RHEL/CentOS supported)
- **Python**: 3.8+ (system installed, other deps auto-installed)
- **Permissions**: root or sudo (required for installing system packages on first setup)

> macOS / Windows not supported (ODA File Converter and QCAD are Linux x86_64 only)

---

## Quick Start

### Install as CodeBuddy Code Skill

Execute in CodeBuddy Code:

```
/install cad-viewer
```

After installation, the skill auto-triggers when DWG/DXF/CAD drawings are mentioned in conversation.

### Manual Usage

```bash
# Check and auto-configure environment (run on first use)
python3 scripts/cad_tools.py check-env

# View drawing basic information
python3 scripts/cad_tools.py info /path/to/drawing.dwg

# List all layers
python3 scripts/cad_tools.py layers /path/to/drawing.dwg --count-entities

# Extract text content
python3 scripts/cad_tools.py texts /path/to/drawing.dwg --keyword "distribution"
```

> **First run**: If Python dependencies (`ezdxf`, `matplotlib`) are not installed, the tool will display an error with installation instructions. Please install them manually or run `python3 scripts/cad_tools.py setup --confirm` to set up the full environment.

---

## External Dependencies

This skill's core functionality (DXF reading, calculations, search) only requires pure Python libraries with no additional installation needed.
The following two external tools are **optional**, enhancing DWG support and screenshot quality respectively:

### ODA File Converter — Required for DWG Reading

**Purpose**: AutoCAD `.dwg` format is a proprietary binary format. ODA File Converter is needed to convert it to readable DXF format. Not needed if only using `.dxf` files.

**How to obtain** (free, registration required):

1. Visit [https://www.opendesign.com/guestfiles/oda_file_converter](https://www.opendesign.com/guestfiles/oda_file_converter)
2. Register a free account (Open Design Alliance account)
3. Download the appropriate Linux version:
   - Debian/Ubuntu: download `.deb` package
   - RHEL/CentOS: download `.rpm` package

**Automatic Installation** (recommended):

`setup.sh` attempts to automatically download and install from ODA official servers:

```bash
bash scripts/setup.sh
```

**Manual Installation** (when network restricted):

```bash
# Specify local RPM package
bash scripts/setup.sh --oda-rpm /path/to/ODAFileConverter_QT6_lnxX64_8.3dll_25.3.rpm

# Specify local DEB package (same parameter, auto-detects format)
bash scripts/setup.sh --oda-rpm /path/to/ODAFileConverter_QT6_lnxX64_8.3dll_25.3.deb
```

**Skip Installation** (DXF files only):

```bash
bash scripts/setup.sh --skip-oda
```

---

### QCAD dwg2bmp — Optional for High-Quality Screenshots

**Purpose**: The `screenshot` command uses QCAD's `dwg2bmp` tool by default to render drawing screenshots with quality close to native CAD software display. If not installed, the screenshot function automatically falls back to `matplotlib` rendering (simpler line styles).

**How to obtain**:

1. Visit [https://qcad.org/en/download](https://qcad.org/en/download)
2. Download **QCAD Professional Trial** — Linux 64-bit (`.tar.gz` format)
3. The Trial version includes the complete `dwg2bmp` command-line tool for free use

**Automatic Installation** (recommended):

```bash
bash scripts/setup.sh
```

`setup.sh` attempts to download multiple versions of QCAD in sequence, extracting to the `assets/qcad/` directory.

**Manual Installation** (when network restricted):

```bash
bash scripts/setup.sh --qcad-tar /path/to/qcad-3.32.6-trial-linux-x86_64.tar.gz
```

**Skip Installation** (accept matplotlib screenshot quality):

```bash
bash scripts/setup.sh --skip-qcad
```

---

### Check Environment Status

When any command errors, first run environment check:

```bash
python3 scripts/cad_tools.py check-env
```

Example output:

```json
{
  "python": { "ok": true, "version": "3.10.12" },
  "ezdxf": { "ok": true, "version": "1.4.3" },
  "matplotlib": { "ok": true, "version": "3.10.8" },
  "xvfb": { "ok": true, "path": "/usr/bin/xvfb-run" },
  "oda": { "ok": true, "path": "/usr/local/bin/ODAFileConverter" },
  "qcad": { "ok": false, "fix": "bash setup.sh --qcad-tar /path/to/qcad.tar.gz" }
}
```

---

## Command Reference

All commands follow this format:

```bash
python3 scripts/cad_tools.py <command> <file_path> [options]
```

### info — Drawing Basic Information

```bash
python3 scripts/cad_tools.py info drawing.dwg
```

Outputs DXF version, units, layer count, block count, entity type statistics. **Recommended as the first step when analyzing any DWG file.**

---

### layers — List Layers

```bash
python3 scripts/cad_tools.py layers drawing.dwg [--count-entities] [--sort-by name|color]
```

Lists all layers' colors, linetypes, and states (on/off/locked/frozen).

---

### entities — List Entities

```bash
python3 scripts/cad_tools.py entities drawing.dwg [--type INSERT] [--layer "EC.SingleLine"] [--limit 20]
```

Lists entities in model space, supports filtering by type and layer.

Common entity types: `INSERT`, `LINE`, `CIRCLE`, `ARC`, `TEXT`, `MTEXT`, `LWPOLYLINE`

---

### blocks — List Block Definitions

```bash
python3 scripts/cad_tools.py blocks drawing.dwg [--name-filter "breaker"]
```

Lists all block definitions (templates), showing internal entity composition.

---

### inserts — List Block Instances

```bash
python3 scripts/cad_tools.py inserts drawing.dwg [--name-filter "10KV"] [--analyze-layers] [--limit 50]
```

Lists block reference instances (equipment, components) in model space. `--analyze-layers` shows each block's internal layer distribution.

---

### texts — Extract Text

```bash
python3 scripts/cad_tools.py texts drawing.dwg [--keyword "distribution"] [--limit 30]
```

Extracts all TEXT, MTEXT, and block attribute texts, supports keyword filtering.

---

### layer-content — Layer Details

```bash
python3 scripts/cad_tools.py layer-content drawing.dwg "EC.SingleLine" [--limit 20]
```

Gets full details of all entities on a specified layer.

---

### spaces — Space Layout

```bash
python3 scripts/cad_tools.py spaces drawing.dwg [--detail]
```

Lists model space, paper layouts, block definitions, and other space structures.

---

### distance — Calculate Distance

```bash
# By block names
python3 scripts/cad_tools.py distance drawing.dwg --entity1 "EquipmentA" --entity2 "EquipmentB"

# By coordinates
python3 scripts/cad_tools.py distance drawing.dwg --coord1 "100,200" --coord2 "500,600"

# Mixed (entity + coordinate)
python3 scripts/cad_tools.py distance drawing.dwg --entity1 "EquipmentA" --coord2 "500,600"
```

Outputs 2D/3D distance and delta values for each axis.

---

### screenshot — Screenshot

```bash
# Screenshot centered on specified block
python3 scripts/cad_tools.py screenshot drawing.dwg --block-name "EquipmentA" --radius 5000 -o output.png

# Screenshot entire layer bounding box
python3 scripts/cad_tools.py screenshot drawing.dwg --layer-name "EC.SingleLine" -o layer.png

# Custom region (x, y, width, height)
python3 scripts/cad_tools.py screenshot drawing.dwg --region "100000,200000,50000,30000" -o region.png

# Full drawing
python3 scripts/cad_tools.py screenshot drawing.dwg -o full.png
```

Options: `--pixel-size 3000` (resolution), `--background black` (background color), `--qcad-path` (specify QCAD path)

---

### audit — Compliance Audit

```bash
python3 scripts/cad_tools.py audit drawing.dwg
```

Performs the following compliance checks:
- Zero-layer violations (INSERT entities on default layer 0)
- Block layer mixing (blocks referencing layers not belonging to themselves)
- Empty layers (layers with no entities)
- DEFPOINTS anomalies (entities that should not be printed)

---

### search — Keyword Search

```bash
python3 scripts/cad_tools.py search drawing.dwg "transformer" [--limit 20]
```

Searches for keywords in block names, text content, and layer names.

---

### export-pdf — Export to PDF

```bash
python3 scripts/cad_tools.py export-pdf drawing.dwg -o output.pdf [--background "#FFFFFF"]
```

Exports the drawing to a vector PDF file.

---

## Recommended Workflow

When analyzing a new DWG file, follow this order for progressive deepening:

```
1. info          → Understand drawing scale, version, units
2. layers        → Understand organizational structure
3. inserts       → Locate main equipment and components
4. texts         → Extract labels and parameter information
5. distance      → Verify critical spacing
6. screenshot    → Obtain visual evidence
7. audit         → Generate compliance report
```

---

## Output Format

All commands output **JSON** to **stdout**, errors to **stderr**, exit code 0 indicates success.

Example `info` command output:

```json
{
  "file": "/path/to/drawing.dwg",
  "dxf_version": "AC1032",
  "unit": "Millimeters",
  "unit_code": 4,
  "total_layers": 45,
  "total_blocks": 120,
  "modelspace_entity_count": 343,
  "entity_type_summary": {
    "INSERT": 36,
    "LINE": 58,
    "LWPOLYLINE": 6,
    "TEXT": 15,
    "MTEXT": 228
  }
}
```

---

## Troubleshooting

**Permission errors on first run**

setup.sh requires root permissions to install system packages. Please run as root or via sudo.

**ODA automatic download fails**

ODA official download links may change with version updates. Please download manually and specify path:

```bash
bash scripts/setup.sh --oda-rpm /path/to/ODAFileConverter_xxx.rpm
```

**QCAD automatic download fails**

```bash
bash scripts/setup.sh --qcad-tar /path/to/qcad-xxx-trial-linux-x86_64.tar.gz
```

**Reset environment configuration**

Delete the marker file to re-run full installation on next execution:

```bash
rm assets/.setup_done
```

**Poor screenshot quality**

Indicates QCAD not installed, currently using matplotlib rendering. Screenshot quality will significantly improve after installing QCAD:

```bash
python3 scripts/cad_tools.py check-env  # View fix command in qcad field
```

**DWG read errors**

Verify ODA File Converter is correctly installed:

```bash
ODAFileConverter --help  # Should produce output
python3 scripts/cad_tools.py check-env  # Check oda field status
```

---

## File Structure

```
cad-viewer/
├── README.md                # This document
├── SKILL.md                 # Skill metadata and AI usage guide
├── scripts/
│   ├── cad_tools.py         # Core CLI tool (13 subcommands)
│   └── setup.sh             # One-click environment setup script
├── references/
│   └── cad_knowledge.md     # CAD domain knowledge reference
└── assets/                  # Auto-generated at runtime
    ├── .setup_done          # Installation completion marker
    ├── oda_wrapper.sh       # ODA virtual display wrapper
    └── qcad/                # QCAD tools directory
```

---

## License

- This tool code (`cad_tools.py`, `setup.sh`): MIT License
- **ODA File Converter**: Provided by Open Design Alliance, subject to their [End User License Agreement](https://www.opendesign.com/legal-notices)
- **QCAD**: QCAD Professional Trial subject to [QCAD License Agreement](https://www.qcad.org/en/qcad-documentation/qcad-license-agreement), not for commercial screenshot production use

---

## Related Links

- [CodeBuddy Code](https://cnb.cool/codebuddy/codebuddy-code) — AI Programming Assistant
- [ezdxf Documentation](https://ezdxf.readthedocs.io/) — DXF/DWG Python Library
- [ODA File Converter Download](https://www.opendesign.com/guestfiles/oda_file_converter)
- [QCAD Download](https://qcad.org/en/download)
