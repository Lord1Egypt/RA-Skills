## Presets (MVP Defaults)

### Units

- Default units: `mm`
- Default scale anchor (if user provides none): category-based

### Category Defaults (Only when user refuses dimensions)

- `bottle-ish`: height 240mm, diameter 70mm
- `lunch-box`: width 190mm, depth 120mm, height 70mm
- `hanger`: width 420mm, thickness 10mm
- `simple-prop`: largest dimension 200mm

All defaults must be marked as low-confidence in `open_questions`.

### Render Preset (MVP)

- Output: PNG
- Resolution: 1024x1024
- Views:
  - `front` (orthographic-ish or mild perspective)
  - `three_quarter` (45 degrees)
- Background: light gray
- Lighting: simple 3-point

### Export Preset (MVP)

- GLB: required, apply transforms
- FBX: optional

