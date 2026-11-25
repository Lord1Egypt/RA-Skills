# Excalidraw scene format (condensed)

Reference for hand-authoring or debugging `.excalidraw` JSON. The bundled
`scripts/make_notes.py` emits all of this correctly — read this when you
need to extend or debug the generator.

## Scene envelope

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": { "viewBackgroundColor": "#ffffff", "gridSize": null },
  "files": {}
}
```

## Common element fields (all types)

`id, type, x, y, width, height, angle, strokeColor, backgroundColor,
fillStyle, strokeWidth, strokeStyle, roughness, opacity, groupIds,
frameId, roundness, seed, version, versionNonce, isDeleted,
boundElements, updated, link, locked`

- `id` unique in the scene; `seed` differs per element; `version` /
  `versionNonce` start at 1.
- `backgroundColor` is `"transparent"` unless filled.
- `roundness`: `{"type": 3}` for rounded rectangles; `null` for text/line.
- `frame` elements carry a `name`; children reference them via `frameId`.

## Type-specific additions

| type | extra fields |
|------|--------------|
| `text` | `fontSize, fontFamily, text, textAlign, verticalAlign, containerId, originalText, lineHeight` |
| `line` / `arrow` | `points, lastCommittedPoint, startBinding, endBinding, startArrowhead, endArrowhead` |
| `rectangle` / `ellipse` | none beyond common (plus `roundness`) |

For lines/arrows, `points` are relative to the element origin:
`[[0,0],[dx,dy]]`; `width`/`height` = `abs(dx)`/`abs(dy)`. Set
`endArrowhead: "arrow"` to draw a head.

## Text rules that bite

- Excalidraw does **not** wrap or clip text; set `width`/`height` yourself
  from the wrapped line count (`height = lines * fontSize * 1.25`).
- Glyph estimate for wrapping: ~0.5em/char for Virgil (family 1),
  ~0.6em for Cascadia mono (family 3).
- `originalText` should equal `text`.
- Font families: 1 = hand-drawn (Virgil), 2 = Helvetica, 3 = Cascadia mono.

## Verification

1. Parse the JSON; assert every element has the common fields above.
2. Same-column overlap check: for text elements sharing (near-equal) `x`,
   assert `a.y + a.height <= b.y` or vice versa.
3. Render the HTML preview and screenshot it — catches overflow the
   overlap check misses. `make_notes.save()` runs checks 1–2 automatically.
