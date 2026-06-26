# 2D pygcadwin workflow

Use this reference when converting a prose OpenClaw/gcadclaw request into executable 2D GstarCAD automation.

## Brief

Create `brief.md` before drawing. Include:

- requested object or mechanism
- units and dimensions
- inferred assumptions
- layers and colors
- entities to create or modify
- dimensions, labels, tables, and annotations
- required views; default to top, front, and right-side views for normal part designs
- `.dwg` and feedback artifact paths
- validation targets

## Implementation pattern

Install `pygcadwin` from PyPI before running drawing code:

```powershell
pip install pygcadwin
```

Preferred script shape:

```python
from pathlib import Path

from pygcadwin import Gcad

out_dir = Path("gcadclaw_runs/example")
out_dir.mkdir(parents=True, exist_ok=True)

cad = Gcad(create_if_missing=True, visible=True)
try:
    ctx = cad.context
    ctx.ensure_layer("CLAW-OUTLINE", color=1)
    ctx.ensure_layer("CLAW-DIM", color=3)

    # Calculate first; then create geometry.
    jaw_length = 80.0
    jaw_width = 18.0
    pivot_radius = 6.0

    ctx.create_rect((0, -jaw_width / 2), (jaw_length, jaw_width / 2), layer="CLAW-OUTLINE")
    ctx.create_circle((0, 0), pivot_radius, layer="CLAW-OUTLINE")
    ctx.create_dimension((0, -jaw_width / 2), (0, jaw_width / 2), (-10, 0), text="18", layer="CLAW-DIM")
    ctx.zoom_extents()
    ctx.view.snapshot().save(out_dir / "review.png")
    cad.document.save_as(out_dir / "drawing.dwg")
finally:
    cad.close()
```

## Action logging

Write `actions.jsonl` while executing. Each row should include:

- step name
- operation/tool name
- arguments or source file path
- status
- handles or output paths when available
- error text for failed attempts

## Entity evidence

Use `scripts/capture_feedback.py` or direct `iter_layout_entities` calls to write before/after JSON. Include object name, handle, layer, color, linetype, lineweight, and common geometric fields when available.

## Screenshot evidence

Always call `ctx.zoom_extents()` or an explicitly scoped view operation before screenshot capture. Persist a PNG with `ctx.view.snapshot().save(path)` or the `snapshot` tool. Confirm the image is not a uniform black/white repaint failure before accepting it. The screenshot is part of the completion contract, not a presentation extra.
