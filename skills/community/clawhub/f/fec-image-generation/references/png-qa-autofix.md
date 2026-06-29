# PNG QA And Autofix

## Loop

1. Export PNG from the editable source or image workflow.
2. Inspect the PNG visually.
3. Run `png-qa.mjs` with a manifest when available.
4. Convert each issue into source, prompt, or layout changes.
5. Repeat for 2 rounds by default, up to 5 when the user asks for more repair attempts.

## Issue mapping

| Issue | Repair |
| ----- | ------ |
| `blank-image` | Check export target, renderer errors, hidden layers, transparent fill, or failed image generation. |
| `edge-clipping` | Add canvas padding, expand SVG viewBox, reduce subject scale, or export a larger frame. |
| `box-overlap` | Increase spacing, reflow to grid/layers, split clusters, or shorten labels. |
| `box-out-of-bounds` | Move the node inside canvas or increase canvas dimensions. |
| `label-overflow` | Wrap text, widen the box, reduce copy, or increase font/container size together. |
| `connector-through-label` | Add waypoints around boxes, move labels, or use orthogonal routing. |
| `connector-stacking` | Offset parallel connectors or replace repeated lines with a labeled grouped path. |
| `manifest-canvas-mismatch` | Regenerate the manifest from final export dimensions. |

## Manifest quality

The helper can only reason about overlaps and connectors when the manifest coordinates match the exported PNG. If the manifest is stale, repair the manifest first, then rerun QA.

## Reporting

Report the number of QA rounds and the final issue list. If issues remain because the source renderer cannot expose layout coordinates, say which checks were image-only and which require manual visual review.
