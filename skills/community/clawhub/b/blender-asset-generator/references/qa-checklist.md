## QA Checklist (MVP)

### Build & Deliverability

- Blender version is 4.2 (or compatible 4.2.x)
- `run-log.txt` exists and includes spec path + output paths + errors if any
- `scene.blend` is created successfully
- `exports/<asset>.glb` exists and is non-empty
- If requested: `exports/<asset>.fbx` exists and is non-empty
- `renders/` includes at least:
  - `front.png`
  - `three_quarter.png`

### Scale & Geometry Sanity

- Scene units are set to mm (or converted correctly)
- The bounding box roughly matches the anchor dimension (+/- 5% for MVP)
- No obvious inverted normals; autosmooth enabled when needed
- Modifier stack is applied (or intentionally left editable) and documented

### Ecommerce Suitability

- Object origin is sensible (base-centered or world origin), documented in log
- Naming is clean:
  - `ASSET__<name>` top collection
  - `MESH__*` objects
  - `MAT__*` materials
- Simple materials are assigned (no missing textures in MVP)

### Export Settings

- GLB export uses `export_apply` (so transform is applied)
- Axes are consistent (document: Blender is Z-up; GLB usually Y-up in some viewers)
- For FBX (if enabled): document the axis settings used

