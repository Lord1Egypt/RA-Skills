# Profile Tuning

Use the default profile first. Only tune it after checking one annotated sample.

## Fields

- `search_roi_norm`
  Limit the search window to the part of the frame where the hook is expected.
  Expand it if the hook is missed. Shrink it if bright clutter causes false positives.

- `bright_threshold`
  Raise these values if sun glare causes false detections.
  Lower them slightly if the hook body is dim.

- `filters.min_area` / `filters.max_area`
  Increase `min_area` if tiny bright fragments are being chosen.
  Increase `max_area` if the hook appears larger in another camera feed.

- `filters.min_aspect` / `filters.max_aspect`
  The hook is a tall component. Tighten these limits if wide bright blobs are being selected.

- `reference_component_bbox_norm`
  This is the reference bbox shape used for scoring. Update it if the accepted hook bbox is consistently different for a new camera.

- `polygon_points_in_bbox_norm`
  These are the normalized polygon points that define the strict outline.
  Edit only the side that is wrong. Leave the opposite side unchanged when refining.

## Recommended Tuning Loop

1. Run one sample image with `-WriteDebugRoi`.
2. Check `debug-roi/` and `manifest.json`.
3. Adjust one profile field at a time.
4. Re-run the same sample.
5. Batch the full directory only after the sample is stable.
