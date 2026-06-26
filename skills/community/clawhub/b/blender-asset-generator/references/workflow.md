## Workflow (Blender 4.2+ including 5.x, Cloud Windows + Local)

### 1) Normalize Input -> Spec

Create a `spec.json` with:
- Identity: `asset_name`, `use_case`, `category`
- Scale: `units` (default `mm`) + at least one anchor dimension if available
- Structure: components list (each has primitive type + params)
- Materials: simple PBR placeholders
- Outputs: export formats + preview renders

If user provides reference images:
- Vision-assisted mode: extract a draft structure card and dimension hypotheses, then ask for confirmation of at least one anchor.
- No-vision mode: follow `references/degradation-strategy.md` to ask minimal clarifications, then proceed.

### 2) Generate/Update Scripts

Always produce scripts with a stable CLI:
- `scripts/build.py -- --spec <path> --out_blend <path> --log <path>`
- `scripts/render.py -- --blend <path> --out_dir <dir> --log <path>`
- `scripts/export.py -- --blend <path> --out_glb <path> [--out_fbx <path>] --log <path>`

Scripts should:
- Set units explicitly
- Build geometry deterministically
- Name objects consistently (`ASSET__<name>`, `MESH__...`, `MAT__...`)
- Write logs and exit non-zero on failure (best effort inside Blender)

### 3) Provide Run Instructions

Provide both:
- Cloud PC (Windows): paths under a fixed workspace (e.g. `C:\work\<project>`)
- Local: Windows + macOS examples

Prefer non-UI Blender execution:
- Windows: `blender.exe -b --python scripts\build.py -- --spec spec.json ...`
- macOS: `/Applications/Blender.app/Contents/MacOS/Blender -b --python ...`

### 4) Verify + Iterate

Minimum verification:
- At least 2 preview renders exist (`front`, `3q`)
- GLB opens in a viewer
- Scale sanity: bounding box matches spec anchor within tolerance
- No obvious shading issues (normals / autosmooth)

### 5) Final Evaluation

Use a simple rubric:
- Correctness: geometry matches text/spec; scale plausible
- Deliverability: GLB export success; renders exist; logs are complete
- Usability: clean naming; components separated; editable parameters in spec
