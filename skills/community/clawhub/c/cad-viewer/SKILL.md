---
name: cad-viewer
description: "This skill should be used when the user wants to read, analyze, or work with CAD DWG/DXF drawing files. Trigger phrases include: DWG, DXF, CAD drawing, drawing analysis, layer, block, entity, screenshot, distance calculation, drawing audit, electrical diagram, distribution box, single-line diagram, or any mention of .dwg/.dxf files. This skill provides comprehensive CAD drawing analysis capabilities including reading file metadata, listing layers and entities, analyzing block definitions, calculating distances between entities, capturing screenshots of specific regions or entities, and auditing drawing compliance."
---

# CAD DWG/DXF Drawing Analysis Tool

## Purpose

Provide professional-grade DWG/DXF drawing file reading and analysis capabilities. This skill enables structured data extraction from CAD drawings, spatial analysis between entities, visual capture of drawing regions, and standards compliance auditing.

## ⚠️ Security Notice

**Before using this skill, please review the following:**

This skill does **NOT** automatically install any packages or run any setup scripts. If dependencies are missing, it will output a clear error message with manual installation instructions. To set up the environment, the user must explicitly run the setup command:

```bash
# Assisted setup (requires explicit --confirm flag)
python3 {SKILL_DIR}/scripts/cad_tools.py setup --confirm
```

The full setup process (when explicitly confirmed) will:
- Install Python packages (`ezdxf`, `matplotlib`)
- Install system packages (`xvfb`, `libGL`) via `sudo`
- Download and install **ODA File Converter** from `opendesign.com`
- Download and install **QCAD dwg2bmp** from `qcad.org`

**All downloads are from official sources**, but the skill requires network access and elevated permissions.

## Prerequisites

- **Python 3.8+** (system installed)
- **Python packages**: `ezdxf` and `matplotlib` must be installed before use
- **root/sudo permissions** (only if you choose to run automatic setup)
- **x86_64 Linux system**

## Setup Options

### Option A: Manual Setup (Recommended for security-conscious users)

Install dependencies yourself before using the skill:

```bash
# 1. Install Python packages
pip3 install ezdxf matplotlib

# 2. Install system packages (Ubuntu/Debian)
sudo apt-get install xvfb libgl1-mesa-glx libglu1-mesa

# 3. Download and install ODA File Converter manually from:
# https://www.opendesign.com/guestfiles/oda_file_converter

# 4. Download and extract QCAD dwg2bmp manually from:
# https://qcad.org/en/download
# Then set: export QCAD_DWG2BMP_PATH=/path/to/qcad/dwg2bmp
```

### Option B: Assisted Setup (Requires confirmation)

Run the setup script with explicit confirmation:

```bash
# Run setup with interactive confirmation
python3 {SKILL_DIR}/scripts/cad_tools.py setup --confirm

# Or manually specify packages you have already downloaded
python3 {SKILL_DIR}/scripts/cad_tools.py setup --oda-rpm /path/to/ODAFileConverter_xxx.rpm --qcad-tar /path/to/qcad-xxx-trial-linux-x86_64.tar.gz
```

**What setup does (with your confirmation):**
1. Installs Python dependencies (`ezdxf`, `matplotlib`) - **required**
2. Installs `xvfb` virtual display - **optional but recommended**
3. Downloads and installs **ODA File Converter** from `opendesign.com` - **required for DWG support**
4. Downloads and installs **QCAD dwg2bmp** from `qcad.org` - **optional, for high-quality screenshots**

ODA Download: https://www.opendesign.com/guestfiles/oda_file_converter (free registration required)
QCAD Download: https://qcad.org/en/download (Professional Trial)

### Check Environment Status

```bash
python3 {SKILL_DIR}/scripts/cad_tools.py check-env
```

Outputs JSON-formatted dependency status, including whether each component is installed, its path, and repair commands if missing.

**When to use**: Run `check-env` to diagnose issues when any command fails.

## Core Tool

All operations use a single CLI tool located at:

```
scripts/cad_tools.py
```

Usage pattern:

```bash
python3 {SKILL_DIR}/scripts/cad_tools.py COMMAND DWG_FILE [OPTIONS]
```

All commands output structured **JSON** to stdout, making the results directly parseable.

## Available Commands

### 1. `info` — Get Drawing Basic Information

Read file version, units, entity count summary, and metadata.

```bash
python3 {SKILL_DIR}/scripts/cad_tools.py info /path/to/drawing.dwg
```

Output includes: DXF version, drawing units, layer count, block count, entity type breakdown.

**When to use**: As the first step when analyzing any new DWG file. Always start with `info` to understand the drawing's scope.

### 2. `layers` — List All Layers

List all layer definitions with color, linetype, and state (on/off/locked/frozen).

```bash
python3 {SKILL_DIR}/scripts/cad_tools.py layers /path/to/drawing.dwg --count-entities --sort-by name
```

Options:
- `--count-entities`: Count entities on each layer (slower but informative)
- `--sort-by name|color`: Sort layers by name or color

**When to use**: To understand the drawing's organizational structure and identify which layers contain relevant content.

### 3. `entities` — List Model Space Entities

List entities with optional type and layer filtering.

```bash
python3 {SKILL_DIR}/scripts/cad_tools.py entities /path/to/drawing.dwg --type INSERT --layer "EC.SingleLine" --limit 20
```

Options:
- `--type`: Filter by entity type (INSERT, LINE, CIRCLE, TEXT, MTEXT, LWPOLYLINE, ARC, etc.)
- `--layer`: Filter by layer name (exact match)
- `--limit`: Maximum number of results

**When to use**: To inspect specific types of entities or explore a particular layer's contents.

### 4. `blocks` — List Block Definitions

List all block definitions (templates) with their internal entity composition.

```bash
python3 {SKILL_DIR}/scripts/cad_tools.py blocks /path/to/drawing.dwg --name-filter "breaker"
```

Options:
- `--name-filter`: Filter blocks by name (case-insensitive substring match)

**When to use**: To catalog available equipment types and standard components in the drawing.

### 5. `inserts` — List Block Reference Instances

List block reference instances (placed equipment/components) in model space.

```bash
python3 {SKILL_DIR}/scripts/cad_tools.py inserts /path/to/drawing.dwg --name-filter "10KV" --analyze-layers --limit 50
```

Options:
- `--name-filter`: Filter by block name
- `--analyze-layers`: Show internal layer distribution of each block
- `--limit`: Maximum results

**When to use**: To find specific equipment instances, their positions, and verify their layer assignments.

### 6. `texts` — Extract Text Content

Extract all text content (TEXT, MTEXT, and block attributes).

```bash
python3 {SKILL_DIR}/scripts/cad_tools.py texts /path/to/drawing.dwg --keyword "distribution" --limit 30
```

Options:
- `--keyword`: Filter by keyword (case-insensitive)
- `--limit`: Maximum results

**When to use**: To find labels, annotations, equipment names, or any textual information in the drawing.

### 7. `layer-content` — Extract Layer Entity Details

Get all entities on a specific layer with full details.

```bash
python3 {SKILL_DIR}/scripts/cad_tools.py layer-content /path/to/drawing.dwg "EC.SingleLine" --limit 20
```

**When to use**: To deeply inspect the contents of a particular professional layer.

### 8. `spaces` — View Space Layout System

List all spaces (model space, paper space, block definitions).

```bash
python3 {SKILL_DIR}/scripts/cad_tools.py spaces /path/to/drawing.dwg --detail
```

Options:
- `--detail`: Include viewport information for paper spaces

**When to use**: To understand the drawing's overall structure and printing layout.

### 9. `distance` — Calculate Distance Between Points/Entities

Calculate 2D and 3D distances between two entities or coordinates.

```bash
# By block names
python3 {SKILL_DIR}/scripts/cad_tools.py distance /path/to/drawing.dwg --entity1 "10KV.GenSet.01IncomingHV" --entity2 "10KV.RouteA-01Incoming.BreakerHV"

# By coordinates
python3 {SKILL_DIR}/scripts/cad_tools.py distance /path/to/drawing.dwg --coord1 "100,200" --coord2 "500,600"

# Mixed: entity + coordinate
python3 {SKILL_DIR}/scripts/cad_tools.py distance /path/to/drawing.dwg --entity1 "10KV.GenSet.01IncomingHV" --coord2 "500,600"
```

Output includes: 2D distance, 3D distance, delta X/Y/Z, and unit.

**When to use**: To verify clearance requirements, check equipment spacing, or measure distances between specific points.

### 10. `screenshot` — Entity/Region Screenshot

Capture a visual image of a specific entity, layer, or region.

```bash
# Screenshot centered on a specific block
python3 {SKILL_DIR}/scripts/cad_tools.py screenshot /path/to/drawing.dwg --block-name "10KV.GenSet.01IncomingHV" --radius 5000 -o /path/to/output.png

# Screenshot of an entire layer's bounding box
python3 {SKILL_DIR}/scripts/cad_tools.py screenshot /path/to/drawing.dwg --layer-name "EC.SingleLine" -o /path/to/layer_view.png

# Screenshot of a custom region (x, y, width, height)
python3 {SKILL_DIR}/scripts/cad_tools.py screenshot /path/to/drawing.dwg --region "-2580000,1020000,60000,40000" -o /path/to/region.png

# Full drawing screenshot
python3 {SKILL_DIR}/scripts/cad_tools.py screenshot /path/to/drawing.dwg -o /path/to/full.png
```

Options:
- `--block-name`: Center on a named block instance
- `--handle`: Center on entity by handle
- `--layer-name`: Capture the bounding box of all entities on a layer
- `--region "x,y,w,h"`: Specify exact capture region
- `--radius`: Expansion radius around entity center (default: 5000)
- `--output / -o`: Output file path (supports .png, .pdf, .svg)
- `--pixel-size`: Image resolution (default: 3000)
- `--background`: Background color (default: black)
- `--qcad-path`: Path to QCAD dwg2bmp tool

**When to use**: To visually inspect equipment, verify spatial arrangements, or generate images for reports and multimodal AI analysis.

### 11. `audit` — Drawing Compliance Audit

Run automated compliance checks on the drawing.

```bash
python3 {SKILL_DIR}/scripts/cad_tools.py audit /path/to/drawing.dwg
```

Checks performed:
- **Zero-layer violations**: INSERT entities on default layer 0
- **Block layer mixing**: Blocks with non-standard internal layer assignments
- **Empty layers**: Layers with no entities (potentially redundant)
- **DEFPOINTS entities**: Non-printing entities on DEFPOINTS layer

Output: Issue list with severity (error/warning/info), rule name, and details.

**When to use**: Before submitting drawings for review, or when auditing received drawings for compliance.

### 12. `search` — Search Entities by Keyword

Search entities by keyword across block names, text content, and layer names.

```bash
python3 {SKILL_DIR}/scripts/cad_tools.py search /path/to/drawing.dwg "transformer" --limit 20
```

**When to use**: To quickly locate specific equipment, annotations, or components by name.

### 13. `export-pdf` — Export to PDF

Convert the drawing to a vector PDF file.

```bash
python3 {SKILL_DIR}/scripts/cad_tools.py export-pdf /path/to/drawing.dwg -o /path/to/output.pdf --background "#FFFFFF"
```

**When to use**: To generate a portable visual representation of the drawing.

## Recommended Workflow

When analyzing a new DWG file, follow this order:

0. **Review past learnings** → Check `.learning/` for relevant experience (see [Self-Learning Mechanism](#self-learning-mechanism))
1. **`info`** → Understand file basics (version, units, entity count)
2. **`layers`** → See the organizational structure
3. **`inserts`** or **`entities`** → Find specific equipment/components
4. **`texts`** → Extract textual annotations
5. **`distance`** → Measure spatial relationships
6. **`screenshot`** → Capture visuals for detailed inspection
7. **`audit`** → Check compliance

## CAD Domain Knowledge

For detailed understanding of DWG file structure, entity types, layer conventions, and CAD coordinate systems, refer to:

```
references/cad_knowledge.md
```

This reference covers: DWG file hierarchy, entity type catalog, unit systems, layer naming conventions for data center drawings, and common audit rules.

## Output Format

All commands produce JSON output to stdout. Error messages go to stderr. Exit code 0 indicates success, non-zero indicates failure.

Example output structure (for `info` command):

```json
{
  "file": "/absolute/path/to/drawing.dwg",
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

## Error Handling

- If a file does not exist, the tool exits with a descriptive error message
- If required Python packages are missing, **the tool outputs clear installation instructions** and exits
- If ODA/QCAD are not available, the tool provides manual setup instructions
- If QCAD is not available for screenshots, the tool automatically falls back to matplotlib rendering
- All errors are written to stderr in JSON format for programmatic consumption
- **No packages are installed automatically** — all installation requires explicit user action

## Notes

- The `{SKILL_DIR}` placeholder refers to the directory containing this SKILL.md file
- **First run may take 1-3 minutes** as the tool automatically installs all dependencies
- After first setup, a marker file is created at `assets/.setup_done` to skip future setup
- To re-run setup (e.g. after system update), delete `assets/.setup_done` and run any command
- DWG files require ODA File Converter for reading; DXF files can be read directly
- Screenshot quality is best with QCAD dwg2bmp; matplotlib is a reasonable fallback
- Large drawings may take several seconds to load — this is normal for complex engineering files
- Coordinate values in CAD drawings can be very large (millions); this is normal for real-world projects

## Self-Learning Mechanism

This skill supports a self-learning mechanism that records user preferences, error resolutions, and best practices discovered during usage. These records are stored in a `.learning/` directory within the user's project and are **automatically referenced in subsequent sessions** to provide more accurate and personalized assistance.

### ⚡ Core Principle

**Unless the user explicitly requests to skip past experience (e.g., "don't refer to previous learnings", "start fresh"), the agent MUST review `.learning/` files at the beginning of every task and apply relevant knowledge throughout the session.**

### 📏 Capacity Limits & Eviction

To prevent records from growing indefinitely and losing their effectiveness, strict limits are enforced:

| File | Max Entries | Eviction Trigger |
|------|-------------|------------------|
| `LEARNINGS.md` | **50** | When adding a new entry would exceed 50 |
| `ERRORS.md` | **30** | When adding a new entry would exceed 30 |

**Counting method**: Count the number of `## [` heading lines in the file to determine the current entry count.

**Eviction strategy** — when the limit is reached, before adding a new entry, remove the lowest-value entry using this priority order:

1. **Status = `resolved`** entries are evicted first (already addressed, least future value)
2. **Status = `wont_fix`** entries are evicted next
3. Among candidates with the same status, evict the one with the **oldest `Logged` date**
4. Among candidates with the same status and date, evict the one with the **lowest priority** (`low` < `medium` < `high` < `critical`)

**Important rules**:
- `pending` and `in_progress` entries are never evicted automatically — if all entries are pending/in_progress and the limit is reached, the agent should ask the user which entry to remove or resolve
- When evicting, remove the entire entry block (from `## [` to the next `---`)
- User preference entries (`user_preference` category) have eviction protection — they are only evicted when no other candidates remain, because preferences are persistently valuable

**Quick count check** (the agent should do this before adding a new entry):
```bash
grep -c "^## \[" .learning/LEARNINGS.md
grep -c "^## \[" .learning/ERRORS.md
```

### First-Use Initialization

Before logging anything, ensure the `.learning/` directory and files exist in the **user's project root** (NOT in the skill directory). If any are missing, create them:

```bash
mkdir -p .learning
[ -f .learning/LEARNINGS.md ] || cp {SKILL_DIR}/assets/LEARNINGS.md .learning/LEARNINGS.md
[ -f .learning/ERRORS.md ] || cp {SKILL_DIR}/assets/ERRORS.md .learning/ERRORS.md
```

Never overwrite existing files. This is a no-op if `.learning/` is already initialized.

### When to Review Learnings (Start of Session)

At the start of every CAD analysis task, **before executing any commands**:

1. Check if `.learning/` directory exists in the project root
2. If it exists, read `.learning/LEARNINGS.md` and `.learning/ERRORS.md`
3. Identify entries relevant to the current task (by file type, command, layer names, error patterns, etc.)
4. Apply relevant learnings proactively — for example:
   - If a user preference for screenshot background color was recorded, use it automatically
   - If a known error with certain DWG versions was logged, warn the user or apply the fix preemptively
   - If a best practice for specific layer analysis was discovered, follow it

### When to Log

| Situation | Action |
|-----------|--------|
| Command fails or produces unexpected output | Log to `.learning/ERRORS.md` |
| User corrects the agent's approach | Log to `.learning/LEARNINGS.md` with category `correction` |
| User specifies a preference (e.g., output format, default options) | Log to `.learning/LEARNINGS.md` with category `user_preference` |
| A non-obvious solution is discovered | Log to `.learning/LEARNINGS.md` with category `insight` |
| Agent's knowledge about CAD was incorrect or outdated | Log to `.learning/LEARNINGS.md` with category `knowledge_gap` |
| A better workflow or approach is found | Log to `.learning/LEARNINGS.md` with category `best_practice` |

### Learning Entry Format

Append to `.learning/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending

### Summary
One-line description of what was learned

### Details
Full context: what happened, what was wrong, what's correct

### Suggested Action
Specific fix or improvement to apply in future sessions

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.dwg
- Tags: tag1, tag2
- See Also: LRN-YYYYMMDD-XXX (if related to existing entry)

---
```

### Error Entry Format

Append to `.learning/ERRORS.md`:

```markdown
## [ERR-YYYYMMDD-XXX] command_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending

### Summary
Brief description of what failed

### Error
```
Actual error message or output
```

### Context
- Command/operation attempted
- Input file and parameters used
- Environment details if relevant

### Resolution
How the error was resolved (fill in once fixed)

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.dwg
- See Also: ERR-YYYYMMDD-XXX (if recurring)

---
```

### ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (learning), `ERR` (error)
- YYYYMMDD: Current date
- XXX: Sequential number (e.g., `001`, `002`)

Examples: `LRN-20260408-001`, `ERR-20260408-001`

### Resolving Entries

When an issue is fixed or a learning is confirmed, update the entry:

1. Change `**Status**: pending` → `**Status**: resolved`
2. For errors, fill in the `### Resolution` section

### Privacy & Safety

- Do NOT log secrets, tokens, private keys, or sensitive environment variables
- Prefer short summaries over full command output
- Do NOT log full file contents — reference file paths instead
- The `.learning/` directory is local to the project and is NOT committed to version control by default

### Gitignore Recommendation

Add to the project's `.gitignore`:

```gitignore
.learning/
```

### Quick Reference for Agent Behavior

```
┌──────────────────────────────────────────────────────────┐
│                   Agent Task Start                        │
│                                                          │
│  1. Does .learning/ exist?                               │
│     ├─ YES → Read LEARNINGS.md & ERRORS.md              │
│     │        Apply relevant past experience               │
│     └─ NO  → Initialize .learning/ directory             │
│                                                          │
│  2. Execute the user's CAD analysis task                 │
│     └─ Apply past learnings throughout                   │
│                                                          │
│  3. During execution, did any of these occur?            │
│     ├─ Error encountered → Log to ERRORS.md              │
│     ├─ User correction → Log to LEARNINGS.md             │
│     ├─ User preference → Log to LEARNINGS.md             │
│     ├─ New insight → Log to LEARNINGS.md                 │
│     └─ Nothing notable → No logging needed               │
│                                                          │
│  4. Before writing a new entry:                          │
│     ├─ Count existing entries (grep -c "^## \[" file)    │
│     ├─ At limit? → Evict lowest-value entry first        │
│     │   (resolved > wont_fix > oldest > lowest priority) │
│     └─ Under limit? → Append directly                    │
│                                                          │
│  5. Task complete                                        │
└──────────────────────────────────────────────────────────┘
```
