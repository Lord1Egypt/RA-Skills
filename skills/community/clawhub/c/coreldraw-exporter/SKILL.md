---
name: "coreldraw-exporter"
description: "Inspect and export objects from CorelDRAW CDR files via COM automation."
---

# CorelDRAW Exporter

Use this skill to inspect `.cdr` files and export specific CorelDRAW content through the installed CorelDRAW application instead of attempting to parse the proprietary CDR format directly.

## Requirements

- Windows with CorelDRAW installed and registered for automation, usually `CorelDRAW.Application` or `CorelDRAW.Application.<version>`.
- Python 3.9+.
- `pywin32` available in the Python environment. If it is missing and the user allows local package installation, run `py -3 -m pip install --user pywin32`.
- Optional: ImageMagick for contact sheets and post-export trimming/compositing.

## Safety

- Preserve the source `.cdr`; export derived files only unless the user explicitly asks for edits.
- Do not overwrite existing exports unless the user requested it or you are writing to a fresh output folder. Prefer a manifest so exports are traceable.
- For public/shareable output, avoid embedding local machine paths, private usernames, or proprietary project notes in the skill or exported metadata.
- CorelDRAW may open a GUI window during automation. Close it with `app.Quit()` in `finally` blocks.

## Workflow

1. Confirm the input `.cdr` exists and choose an output directory.
2. Inspect the document before exporting:
   - Run `scripts/coreldraw_export.py inspect <input.cdr> --json <metadata.json>`.
   - Review pages, layers, top-level shape indexes, names, types, positions, and dimensions.
   - Export a page preview if object names are missing: `scripts/coreldraw_export.py preview <input.cdr> <preview.png> --page 1 --dpi 300`.
3. Decide export specs:
   - Use one-based shape indexes from inspection.
   - Use ranges for multi-shape clusters, e.g. `7-20`.
   - Use comma lists for non-contiguous clusters, e.g. `2,5,8-10`.
   - Prefer semantic filenames from visual/content context, e.g. `birch_summer_01.png`, `logo_primary.svg`.
4. Export selected content:
   - Single objects: `scripts/coreldraw_export.py export <input.cdr> <outdir> --item tree_01.png:4`.
   - Multi-object clusters: `scripts/coreldraw_export.py export <input.cdr> <outdir> --item tree_cluster.png:7-20`.
   - Multiple outputs: pass `--item` repeatedly.
   - Full layer/page fallback: use `--all-top-level` or `preview` when exact object grouping is unclear.
5. Validate the result:
   - Check file count and byte sizes.
   - For PNGs, verify alpha with ImageMagick if available: `magick identify -format "%f %[channels] %[pixel:p{0,0}] %wx%h\n" <files>`.
   - Create a contact sheet when many assets were exported: `magick montage <files> -thumbnail 180x180 -set label "%t" <contact_sheet.png>`.
6. Report what was exported, where, naming assumptions, and any ambiguous objects skipped.

## Notes

- CorelDRAW shape `Type` values are numeric in COM output; use them mainly for filtering/recon, not as the only semantic signal.
- Many CDRs have unnamed objects. In that case, use visual page previews plus coordinates and object ordering.
- Exporting a selection usually crops to the selected object/range bounds. Complex effects, lenses, transparencies, or fonts may rasterize or render differently depending on the export format.
- If generic converters such as ImageMagick, Inkscape, or LibreOffice fail on CDR, keep using CorelDRAW COM. It is the most reliable path when CorelDRAW is installed.
