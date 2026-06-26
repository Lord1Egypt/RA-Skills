---
name: crane-hook-annotation
description: Detect and tightly annotate tower-crane hook outlines in similar construction-site monitoring images. Use when Codex needs to batch-process `.png`, `.jpg`, or `.jpeg` images from a stable camera view, locate the hook from bright metal pixels inside a known search region, export annotated copies, and produce reusable coordinates or polygon metadata for follow-up QA.
---

# Crane Hook Annotation

Use this skill when the user has many similar site-monitoring images and wants the crane hook outlined with a strict polygon rather than a loose box.

## Workflow

1. Confirm the images are from a similar viewpoint.
2. Run [annotate-crane-hooks.ps1](./scripts/annotate-crane-hooks.ps1) on one sample image first.
3. Inspect the annotated output and the manifest JSON.
4. If the hook is consistently shifted, edit [default-monitoring-profile.json](./scripts/profiles/default-monitoring-profile.json).
5. Re-run the same script on the full directory once the sample looks right.

## Quick Start

Run a sample image:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\crane-hook-annotation\scripts\annotate-crane-hooks.ps1 `
  -InputPath .\sample-image.jpg `
  -OutputDir .\hook-batch-output `
  -WriteDebugRoi
```

Run a directory:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\crane-hook-annotation\scripts\annotate-crane-hooks.ps1 `
  -InputPath .\incoming-images `
  -OutputDir .\hook-batch-output `
  -Recurse
```

## Outputs

- `annotated/`: annotated images with the strict hook polygon and label
- `debug-roi/`: optional ROI crops for inspection
- `manifest.json`: one record per image with component bbox, polygon points, and status

## Tuning

Read [profile-tuning.md](./references/profile-tuning.md) when:

- the hook is detected but the outline is systematically shifted
- the hook search area is too narrow or too wide
- the user changes camera angle or image resolution
- a different site needs its own profile

Adjust these fields first:

- `search_roi_norm`
- `bright_threshold`
- `filters`
- `reference_component_bbox_norm`
- `polygon_points_in_bbox_norm`

## Notes

- The current default profile is calibrated from the accepted hook outline in this workspace.
- The script assumes a bright metal hook against a darker construction background.
- Batch execution is safest when images come from the same or a very similar camera setup.
