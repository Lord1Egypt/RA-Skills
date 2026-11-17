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
| `box-overlap` | Increase spacing, reflow to grid/layers, split clusters, or wrap complete labels. |
| `box-out-of-bounds` | Move the node inside canvas or increase canvas dimensions. |
| `label-overflow` | Wrap text, widen the box, preserve complete copy, and increase font/container size together. |
| `connector-through-label` | Add waypoints around boxes, move labels, or use orthogonal routing. |
| `connector-stacking` | Offset parallel connectors or replace repeated lines with a labeled grouped path. |
| `manifest-canvas-mismatch` | Regenerate the manifest from final export dimensions. |

## Manifest quality

The helper can only reason about overlaps and connectors when the manifest coordinates match the exported PNG. If the manifest is stale, repair the manifest first, then rerun QA.

## Reporting

Report the number of QA rounds and the final issue list. If issues remain because the source renderer cannot expose layout coordinates, say which checks were image-only and which require manual visual review.


## Quality delivery contract

Prefer local Mermaid for standard sequence/workflow diagrams, reuse fec-drawio-studio for manually editable architecture, and optionally use Graphviz for dense topology. Fall back to compatible JSON/HTML if local tools are missing, without automatic installation/downloads. Preview, standalone SVG and PNG share source theme styles; export with `--theme light|dark`. PNG export waits for fonts and measures text; use `--manifest source.layout.json --output-manifest image.actual.json` for scaled pixel coordinates. QA must read the actual manifest, not reuse estimated coordinates unchanged for a 2x PNG.

The extended manifest retains canvas/boxes/connectors and adds coordinateSpace, scale, measurement, groups, labels and issues. Group containment is not node overlap. New checks include node-text-overflow, label-content-loss, label-out-of-bounds, edge-label-collision, text-overlap and degenerate-connector. Legacy manifests retain estimated checks. Diagnose constrained explicit sizes/waypoints without dropping text, changing relationships or silently moving coordinates. Increasing export resolution cannot fix source overflow. Visually review the final PNG and record tool availability/version, theme, scale, repair rounds and remaining defects; report partial acceptance when unresolved.
