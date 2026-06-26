---
name: blender-asset-generator
description: Generates ecommerce/game/teaching 3D assets via Blender scripts (Blender 4.2+ including 5.x). Supports cloud Windows and local machines; reference-image guided workflow with graceful degradation when vision is unavailable.
---

# Blender Asset Generator (Blender 4.2+ / 5.x)

This Skill generates a reproducible asset project that can be executed in:
- Cloud PC (Windows) as the primary runtime
- Local computer (Windows or macOS) as an alternative runtime

The Skill outputs:
- A structured spec (`spec.json`) describing the asset
- Executable Blender Python scripts (`scripts/*.py`) using `bpy`
- Run scripts for Windows/macOS
- Export artifacts: `GLB` (required), `FBX` (optional), `USDC` (optional), plus preview renders

## Quick Start

1. Choose a mode:
   - `Text-only Mode` (no image or no vision): fast and deterministic
   - `Vision-assisted Mode` (reference images + multimodal model): extract structure/dimensions from images, then confirm with user

2. Provide input:
   - Required: object name + use case (`ecommerce` / `game` / `teaching`) + desired output formats (`GLB` required, `FBX` optional)
   - Optional: target size (at least one anchor dimension), poly budget, material style, reference images

3. The Skill will:
   - Normalize input into `spec.json`
   - Generate `scripts/build.py`, `scripts/render.py`, `scripts/export.py` (or update them)
   - Provide `Cloud (Windows)` and `Local (Windows/macOS)` run commands
   - Generate a QA checklist and a final evaluation

## Input Template

```text
Blender Version: 4.2+ (supports 4.2 and 5.x)
Primary Runtime: Cloud PC (Windows)
Output Priority: GLB required; FBX optional
USD: USDC optional (via file extension)

Use Case: ecommerce | game | teaching
Asset Name:
Asset Category: (e.g., bottle / lunch box / hanger / simple prop / teaching diagram)

Text Description (required):
- What it is:
- Key parts/components:
- Material style (optional): plastic/metal/glass/wood/fabric
- Target realism: low/medium/high

Dimensions (recommended):
- Provide at least ONE anchor dimension, e.g. height=240mm
- If unknown: provide category-typical size OR accept default size

Constraints (optional):
- Poly budget (triangles):
- UV: required | optional | no
- Texture placeholders: yes | no
- Naming convention: (optional)

Reference Images (optional):
- Attach images (front/side/top) if available
- If images are provided, say whether there is a scale reference in the image:
  - e.g. A4 paper / coin / ruler / hand / known product standard size
```

## References

Read these as needed:
- Workflow: `references/workflow.md`
- Ecommerce reference-image template: `references/ecommerce-reference-guided-template.md`
- Degradation strategy (no vision available): `references/degradation-strategy.md`
- QA checklist: `references/qa-checklist.md`
- Presets (common defaults): `references/presets.md`

## Output Contract

Always output in this structure:
1. `Project Package`
   - File tree (what to create/update)
   - `spec.json` (final)
2. `Run Instructions`
   - Cloud PC (Windows) command(s)
   - Local (Windows) command(s)
   - Local (macOS) command(s)
3. `Expected Artifacts`
   - `scene.blend`
   - `exports/*.glb` (required)
   - `exports/*.fbx` (optional)
   - `renders/*.png` (required: at least 2 views)
   - `run-log.txt` (required)
4. `QA + Evaluation`
   - Checklist results
   - Verdict: `Achieved | Partially Achieved | Not Achieved`
   - Top fixes

## Behavior Rules

- Determinism: prefer parametric geometry and explicit settings; avoid random seeds unless user asks.
- Evidence: do not invent certifications/performance claims; in 3D context, do not assume hidden dimensions from a single photo.
- Reference images:
  - If a multimodal model is available, extract a *draft* structure card and dimension hypotheses, then ask for confirmation of at least one anchor dimension.
  - If vision is NOT available, never block the workflow. Use `Text-only Mode` + ask for a minimal clarification form (see `references/degradation-strategy.md`).
- Units: default to millimeters in the spec; enforce unit conversion in scripts.
- Exports: always export GLB; export FBX only when requested.

## Assets (Project Skeleton)

Use the project skeleton to generate a runnable folder:
- `assets/project-skeleton/spec.schema.json`
- `assets/project-skeleton/spec.example.json`
- `assets/project-skeleton/scripts/build.py`
- `assets/project-skeleton/scripts/render.py`
- `assets/project-skeleton/scripts/export.py`
- `assets/project-skeleton/run_local_windows.ps1`
- `assets/project-skeleton/run_local_macos.sh`
- `assets/project-skeleton/run_cloud_windows.ps1`
