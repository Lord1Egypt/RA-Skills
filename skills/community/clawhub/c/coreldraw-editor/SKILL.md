---
name: "coreldraw-editor"
description: "Inspect, edit, and export CorelDRAW CDR files via COM automation."
---

# CorelDRAW Editor

Use this skill to work with `.cdr` files through CorelDRAW itself. Prefer CorelDRAW COM automation over raw parsing because CDR is proprietary and version-sensitive.

## Requirements

- Windows with CorelDRAW installed and registered for automation, usually `CorelDRAW.Application` or `CorelDRAW.Application.<version>`.
- Python 3.9+.
- `pywin32`. If missing and local package installation is acceptable, run `py -3 -m pip install --user pywin32`.
- Optional: ImageMagick for contact sheets and alpha/size verification.

## Safety Rules

- Inspect first. Never edit blind.
- Preserve originals by default. For any edit that changes a document, create or open a copy and save to an explicit output path.
- Treat delete, ungroup, flatten/rasterize, font substitution, color conversion, and overwriting existing files as potentially destructive. Only do them when the user clearly asked or after making a copy.
- Close CorelDRAW in `finally` blocks with `doc.Close()` and `app.Quit()`.
- Report assumptions, especially when objects are unnamed or selected by coordinates/indexes.

## Core Workflow

1. Confirm the `.cdr` path and output destination.
2. Inspect structure:
   - `scripts/coreldraw_editor.py inspect input.cdr --json metadata.json`
   - Review pages, layers, shape indexes, names, types, positions, and sizes.
3. Make a page preview when objects are unnamed:
   - `scripts/coreldraw_editor.py preview input.cdr preview.png --page 1 --dpi 300`
4. Decide object selectors:
   - Use one-based shape indexes from inspection.
   - Use ranges such as `7-20` for clusters.
   - Use comma/range specs such as `2,5,8-10` for non-contiguous selections.
   - Use layer names or indexes when the document has multiple printable layers.
5. For exports, export selections or full top-level objects:
   - `scripts/coreldraw_editor.py export input.cdr outdir --item logo.png:3 --format png`
   - `scripts/coreldraw_editor.py export input.cdr outdir --item tree.png:7-20 --transparent --manifest out.csv`
6. For document edits, use copy-first plans:
   - `scripts/coreldraw_editor.py apply-plan input.cdr edited.cdr --op '{"op":"rename","shapes":"4","name":"logo-primary"}'`
   - `scripts/coreldraw_editor.py apply-plan input.cdr edited.cdr --plan edits.json`
7. Validate by reopening or inspecting the edited copy, and by exporting a preview/contact sheet when visual correctness matters.

## Supported Script Operations

The bundled script intentionally supports conservative operations that map cleanly to CorelDRAW's COM API:

- `rename`: set shape names.
- `move`: move selected shapes by `dx`, `dy` in document units.
- `set-position`: set selected shapes to `x`, `y`.
- `resize`: set selected shapes to `width`, `height`.
- `rotate`: rotate selected shapes by `angle` degrees.
- `duplicate`: duplicate selected shapes with optional `dx`, `dy` offset.
- `delete`: delete selected shapes from the edited copy.
- `group`: group selected shapes.
- `ungroup`: ungroup selected shapes.
- `layer-visible`: set layer visibility.
- `layer-printable`: set layer printability.
- `save-copy`: save an output `.cdr` copy without further edits.

For more specialized tasks such as precise fill/outline replacement, font substitution, text replacement, PowerClip edits, lens/effect edits, or import placement, first inspect the generated Corel COM wrapper under Python's `win32com.client.gencache` folder and script against the exact installed CorelDRAW version. Use page previews before and after.

## Validation

- For PNG exports, verify transparency and dimensions with ImageMagick when available:
  - `magick identify -format "%f %[channels] %[pixel:p{0,0}] %wx%h\n" *.png`
- For many exports, create a contact sheet:
  - `magick montage *.png -thumbnail 180x180 -set label "%t" contact_sheet.png`
- For edited CDR output, re-run `inspect` on the edited copy and export a preview before reporting success.

## Practical Notes

- `CorelDRAW.Application.<version>` is more deterministic than the version-independent ProgID when multiple Corel versions exist.
- Shape indexes are document/order dependent. Re-inspect after operations that add/delete/group/ungroup shapes.
- Exporting a selection usually crops to the selection bounds. Complex effects, lenses, transparencies, missing fonts, and linked assets may render differently depending on export format.
- If generic tools cannot decode CDR, that is normal; continue with CorelDRAW automation.
