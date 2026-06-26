---
name: blender-render
description: Automate Blender headless previews for STL/OBJ/FBX/BIM and multi-part 3D-print models. Use for local-path model import, Workbench orthographic previews, stable part colors, exploded views, contact sheets, simple Cycles beauty renders, and BIM fallback snapshots without opening the Blender UI.
---

# Blender Headless Rendering Workflow

Use this skill when the user needs quick, reliable images from local 3D assets: STL/OBJ/PLY print models, multi-part model folders, or BIM/Revit FBX exports. For actual 3D-print splitting, clearance, 3MF validation, or assembly-fit debugging, use a dedicated 3D-print workflow instead; this skill only produces previews/renders.

## Current operating assumptions

- Prefer **Workbench + orthographic camera** for technical previews. It is fast, stable in headless mode, and shows geometry/part colors clearly.
- Use **Cycles** only when the user specifically wants a nicer beauty render; it is slower and more sensitive to GPU/render settings.
- Do not assume a fixed Blender version like `5.0.1`. Use the installed Blender that works on the host, ideally current stable/LTS.
- Do not install or upgrade Blender without explicit user permission.
- Render previews are **not validation**. A pretty preview does not prove watertightness, printability, or physical assembly fit.

## Blender executable

Resolve Blender in this order:

```bash
${BLENDER_BIN:-$(command -v blender || echo /Applications/Blender.app/Contents/MacOS/Blender)}
```

If that path fails, try `command -v blender`. If Blender is missing, ask before installing.

## Workflow 1: multi-part STL/OBJ preview for print handoff

This is the preferred workflow for technical handoff previews: deterministic colors, orthographic front/iso views, optional exploded layout, and a contact sheet for chat/slicer review.

```bash
BLENDER_BIN="${BLENDER_BIN:-/Applications/Blender.app/Contents/MacOS/Blender}"
"$BLENDER_BIN" --background \
  --python scripts/render_stl_set_preview.py -- \
  --input /path/to/final_parts_dir \
  --output-dir /path/to/preview \
  --prefix model-preview \
  --explode 0.35
```

If the source format carries useful imported materials (for example OBJ+MTL), add `--preserve-materials`. For plain STL handoff previews, leave it off so the script assigns stable high-contrast colors. Contact sheets require Pillow (`python3 -m pip install pillow`) if it is not already available.

Then optionally create a labeled contact sheet:

```bash
python3 scripts/make_contact_sheet.py \
  --output /path/to/preview/model-preview-contact-sheet.png \
  --image /path/to/preview/model-preview-front.png --label 正面预览 \
  --image /path/to/preview/model-preview-iso.png --label 透视预览
```

Quality checks:

- Parts are visibly separated or clearly color-coded.
- Orthographic front view is not clipped.
- Iso view shows the important interfaces.
- File names and labels make the preview understandable outside this chat.

## Workflow 2: standard single-mesh beauty render

For STL/OBJ models where the goal is a nicer preview with procedural material and lighting:

```bash
BLENDER_BIN="${BLENDER_BIN:-/Applications/Blender.app/Contents/MacOS/Blender}"
"$BLENDER_BIN" --background \
  --python scripts/render_standard.py -- \
  --input /path/to/model.stl \
  --output /path/to/output_prefix \
  --device auto \
  --samples 64 \
  --resolution 1400
```

This emits `*_front.png`, `*_side.png`, and `*_top.png`. Use `--device cpu` for portable smoke tests; use `--device gpu` only when GPU rendering is configured.

## Workflow 3: BIM/Revit FBX fallback snapshot

BIM FBX often imports with hierarchy/material problems and may appear black in Cycles/Eevee. Use Workbench and force visibility:

```bash
BLENDER_BIN="${BLENDER_BIN:-/Applications/Blender.app/Contents/MacOS/Blender}"
"$BLENDER_BIN" --background \
  --python scripts/render_bim.py -- \
  --input /path/to/structure.fbx \
  --output /path/to/structure-preview.png
```

## Recent lessons to preserve

- **Workbench first.** For geometry review, Workbench/MATCAP or Workbench/STUDIO is more useful than photorealistic rendering.
- **Orthographic cameras beat perspective** for judging part layout and dimensions.
- **Stable colors matter.** Assign deterministic material colors per object/file for STL handoff screenshots; preserve imported materials only when the source format actually carries meaningful material data.
- **Exploded copies are previews only.** Keep source objects hidden or untouched; render duplicated preview objects with offsets.
- **Large files should stay local.** If chat upload is unreliable for large FBX/STL/3MF files, ask for a local absolute path copied from the OS file manager.
- **Do not confuse render with validation.** For print/slicer handoff, pair previews with geometry/3MF validation reports from the relevant workflow.

## Script maintenance smoke test

After editing bundled scripts, at least run:

```bash
python3 -m py_compile scripts/*.py
```

A real Blender render smoke test is better, but only run it when Blender is available and the user permits access to the chosen local model paths.
