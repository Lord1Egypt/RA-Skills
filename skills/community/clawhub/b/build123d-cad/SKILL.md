---
name: build123d-cad
description: "Parametric 3D CAD via build123d. Generate STEP, STL, SVG from Python scripts. Use when the user asks to design, model, create, or export 3D parts, enclosures, mounts, brackets, or mechanical components."
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["python3"]},"emoji":"🔧"}}
---

# build123d CAD

Parametric 3D CAD via [build123d](https://build123d.readthedocs.io). This skill provides Python scripts for generating and measuring 3D solids. Run them with the `exec` tool.

## Setup (first time only)

```bash
cd {baseDir}
uv venv --python 3.12
uv pip install build123d
```

## Commands

All scripts use the venv Python at `{baseDir}/.venv/bin/python`. All output JSON to stdout.

### Generate — export STEP/STL/SVG

```bash
{baseDir}/.venv/bin/python {baseDir}/scripts/cad_generate.py \
  --script 'from build123d import *
with BuildPart() as result:
    Box(100, 60, 40)' \
  --format step \
  --filename my_box
```

Output: `{ "success": true, "artifact_path": "...", "format": "step", "file_size_bytes": N, "bounding_box_mm": {...} }`

### Measure — dimensions, volume, mass

```bash
{baseDir}/.venv/bin/python {baseDir}/scripts/cad_measure.py \
  --script 'from build123d import *
with BuildPart() as result:
    Cylinder(10, 50)'
```

Output: `{ "success": true, "bounding_box_mm": {...}, "volume_mm3": N, "surface_area_mm2": N, "center_of_mass_mm": {...}, "face_count": N, "edge_count": N }`

### Section — 2D cross-section SVG

```bash
{baseDir}/.venv/bin/python {baseDir}/scripts/cad_section.py \
  --script '...' \
  --plane XY \
  --offset 5.0
```

Output: `{ "success": true, "artifact_path": "...", "plane": "XY", "offset_mm": 5.0 }`

### API Reference — build123d cheatsheet

```bash
{baseDir}/.venv/bin/python {baseDir}/scripts/cad_api.py
```

Output: JSON with primitives, operations, selectors, export functions. Call this first if you need to learn what's available.

### Validate — interference, clearance, swept-volume collision

Check an assembly of multiple parts for interference, minimum clearance, and moving-part collisions.

```bash
{baseDir}/.venv/bin/python {baseDir}/scripts/cad_validate.py \
  --script '...' \
  --mode full \
  --min-clearance 1.0
```

Modes: `static` (Boolean intersection between all pairs), `clearance` (bounding box gap), `sweep` (rotate moving parts through angular range, check collisions), `full` (all three, default).

The script must define `parts = {"name": solid, ...}` dict. Optionally define `sweeps` list for moving parts:

```python
from build123d import *

with BuildPart() as enclosure:
    Box(100, 80, 50)
    offset(amount=-3, openings=enclosure.faces().sort_by(Axis.Z)[-1:])

with BuildPart() as pcb:
    with Locations((0, 0, 5)):
        Box(60, 40, 2)

with BuildPart() as servo_arm:
    with Locations((30, 0, 25)):
        Box(5, 20, 3)

parts = {
    "enclosure": enclosure.part,
    "pcb": pcb.part,
    "servo_arm": servo_arm.part,
}

sweeps = [
    {
        "name": "servo_arm",
        "axis_origin": (30, 0, 25),
        "axis_direction": (0, 1, 0),
        "angle_start": -45,
        "angle_end": 45,
        "angle_step": 5,
    },
]
```

Output: `{ "verdict": "PASS|WARN|FAIL", "static_interference": {...}, "clearance": {...}, "swept_volume": {...} }`

- **PASS** — no interference, clearance OK
- **WARN** — clearance below threshold but no hard collision
- **FAIL** — parts intersect or moving parts collide during sweep

Swept volumes are exported to `~/.openclaw/workspace/cad-output/swept_<name>.step` for visualization.

## Script Format

All single-part scripts must assign the final solid to `result` via a `BuildPart` context:

```python
from build123d import *

with BuildPart() as result:
    Box(100, 60, 40)
    fillet(result.edges().filter_by(Axis.Z), radius=5)
    with Locations((0, 0, 40)):
        CounterBoreHole(radius=5, counter_bore_radius=8, counter_bore_depth=3, depth=40)
```

For validation scripts, define `parts` dict (and optionally `sweeps` list) instead of `result`.

All dimensions in millimeters. Exported files go to `~/.openclaw/workspace/cad-output/`.

## Workflow

1. If unsure about build123d API, run `cad_api.py` first for the cheatsheet.
2. Write a parameterized script (no magic numbers).
3. Run `cad_measure.py` to verify dimensions before exporting.
4. **For multi-part assemblies: run `cad_validate.py --mode full` before exporting.** Fix any FAIL/WARN before proceeding.
5. Run `cad_generate.py` with the desired format (step for CAD, stl for 3D printing).
6. For clearance visualization, run `cad_section.py` at relevant planes.
7. Report artifact paths and validation verdict.

## Design Rules

- Parameterize all dimensions for reusability.
- Add fillets to stress concentrations (min 1mm for plastic, 0.5mm for metal).
- Include mounting features (bosses, standoffs, screw posts) where applicable.
- Specify material and process assumptions in comments.
- Output both the script and the exported file.
