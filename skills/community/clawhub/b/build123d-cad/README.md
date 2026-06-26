# build123d-cad

OpenClaw skill for parametric 3D CAD via [build123d](https://github.com/gumyr/build123d). Generates STEP, STL, SVG from Python scripts using the `exec` tool.

## Scripts

| Script | Description |
|--------|-------------|
| `cad_generate.py` | Execute build123d script → export STEP/STL/SVG |
| `cad_measure.py` | Execute build123d script → bounding box, volume, surface area, center of mass |
| `cad_section.py` | Generate 2D cross-section SVG at a given plane + offset |
| `cad_validate.py` | Interference detection, clearance analysis, swept-volume collision checks |
| `cad_api.py` | Print build123d API cheatsheet (no build123d dependency needed) |

## Install

```bash
# clone into OpenClaw workspace skills
git clone https://github.com/xintlabs/build123d-cad.git ~/.openclaw/workspace/skills/build123d-cad

# create venv with Python 3.12 (build123d requires <=3.12 for OpenCascade wheels)
cd ~/.openclaw/workspace/skills/build123d-cad
uv venv --python 3.12
uv pip install build123d
```

That's it. OpenClaw auto-discovers the `SKILL.md` on next session. No config changes needed.

The agent calls scripts via the `exec` tool using the venv Python at `{baseDir}/.venv/bin/python`. Exported files go to `~/.openclaw/workspace/cad-output/`.

> **Note:** build123d requires Python ≤3.12 for OpenCascade wheels. Your system Python doesn't matter — scripts run in their own venv.

## Usage

Once installed, talk to your OpenClaw agent via Telegram (or any connected channel):

```
You:   Design a projector mount bracket for Puttreal. 60mm wide, 
       M4 mounting holes, 15° tilt angle. Export as STEP.

Agent: [runs cad_api.py to check available primitives]
       [runs cad_generate.py with the script]
       ✅ Exported to ~/.openclaw/workspace/cad-output/projector_mount.step
       Bounding box: 60 × 45 × 32 mm, 4 mounting holes, filleted edges.
```

```
You:   Measure the volume and check a cross-section at Z=15mm.

Agent: [runs cad_measure.py]
       Volume: 12,450 mm³, surface area: 8,230 mm², 14 faces, 36 edges.
       [runs cad_section.py --plane XY --offset 15]
       ✅ Section SVG at ~/.openclaw/workspace/cad-output/section_XY_15.0.svg
```

```
You:   What build123d primitives can I use?

Agent: [runs cad_api.py]
       Box, Cylinder, Sphere, Cone, Torus, Wedge...
       [returns full cheatsheet]
```

## Script format

All scripts expect a `--script` argument with valid build123d Python. The final solid must be assigned to `result`:

```python
from build123d import *

with BuildPart() as result:
    Box(100, 60, 40)
    fillet(result.edges().filter_by(Axis.Z), radius=5)
    with Locations((0, 0, 40)):
        CounterBoreHole(radius=5, counter_bore_radius=8, counter_bore_depth=3, depth=40)
```

## Environment

| Variable | Default | Description |
|----------|---------|-------------|
| `CAD_WORKSPACE` | `~/.openclaw/workspace/cad-output` | Directory for exported files |

## Test

```bash
cd ~/.openclaw/workspace/skills/build123d-cad
.venv/bin/python -m pytest tests/ -v
```
