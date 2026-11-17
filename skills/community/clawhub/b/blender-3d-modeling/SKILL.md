---
name: blender-3d-modeling
description: "Blender 3D Modeling: Blender 3D suite running headless in the cloud. Use when an agent needs blender 3d modeling, render turntable videos of 3d models for game asset previews, create multi angle product shots from 3d models for e commerce, convert 3d files between formats like glb to blend, glb to fbx, cancel task, task id, check printability through AgentPMT-hosted remote tool calls. Discovery terms: blender 3d modeling, render turntable videos of 3d models for game asset previews."
version: 1.0.1
homepage: https://www.agentpmt.com/marketplace/blender-3d-modeling
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/blender-3d-modeling"}}
---
# Blender 3D Modeling

## Freshness
Last updated: `2026-09-11`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Full access to Blender, the industry-standard open-source 3D creation suite, running headless in the cloud. Render stunning images and turntable videos from any 3D model, convert between file formats (BLEND, GLB, FBX, OBJ, STL, DAE, PLY), set up professional studio lighting, and run custom Blender Python scripts — all without installing anything locally. Upload your 3D models and get back production-quality renders, spinning animations, processed assets, and Blender project files. Choose from four lighting presets (studio, product, outdoor, dramatic), render from multiple camera angles at once, or position the camera exactly where you want it. Perfect for game development asset previews, product visualization, architectural walkthroughs, e-commerce 3D photography, 3D printing prep, portfolio showcases, and creative projects of any kind.

## Product Instructions
### Blender 3D Modeling

Full access to Blender, the industry-standard 3D creation suite, running headless in the cloud. Render images and videos from 3D models, convert between file formats, and run custom Blender Python scripts.

#### How It Works

Render actions (`render_turntable`, `render_views`, `render_custom`, `run_script`, `check_printability`, `fix_printability`, `voxel_remesh`, `slice_for_printing`) run **asynchronously**. They return immediately with a `task_id` and `status: "processing"`. The render runs in the background. Use `get_task` to check progress and retrieve download links when complete.

`convert_format` runs **synchronously** and returns the converted file immediately (typically under 5 seconds).

The GPU runs one render at a time. When you submit while another job is in flight, your request joins a strict-FIFO queue and `get_task` returns three additional fields so you can plan around the wait:

- `queue_position` — `0` while running, otherwise the 1-based slot in line.
- `queue_eta_seconds` — best-guess seconds until the job is dequeued.
- `queue_stats` — `{queue_total_running, queue_total_queued, queue_total_capacity}`.

A submitted task that you no longer need can be cancelled with `cancel_task`. Cancellation works whether the task is still queued or actively rendering — see the action's docs for the contract.

#### Quick Start For Agents

Use this decision flow when choosing an action:

1. Need a spinning preview video of an existing model: call `render_turntable`.
2. Need front/top/side/3quarter still images of an existing model: call `render_views`.
3. Need one specific camera angle: call `render_custom`.
4. Need to change model file format, including exporting a native `.blend` file: call `convert_format`.
5. Need to know if a model is 3D-printable: call `check_printability`.
6. Need a light-touch cleaned export of a *mostly-clean* model (CAD output, hand-modeled mesh with a few stray non-manifolds): call `fix_printability`.
7. Need to repair a *structurally-broken* organic model (3D-modeled / sculpted shapes with overlapping geometry, photogrammetry exports, self-intersecting Boolean unions, inverted-normal regions, dense multi-shell tessellation): call `voxel_remesh`.
8. Need to slice a model and get print time / filament estimates: call `slice_for_printing`.
9. Need to create or modify geometry/materials/lighting with Blender Python, render custom media, or save several files: call `run_script`.
10. Need the result from an async action: call `get_task` with the returned `task_id`.
11. Need recent work history: call `list_tasks`.
12. Need to abort a queued or running task: call `cancel_task` with the `task_id`.

For any action that accepts a model, provide exactly one model source:
- `file_id` when the model is already in AgentPMT file storage.
- `file_url` when the model is available at a public HTTPS URL.

Do not invent file IDs. If the user only has a local path, first upload it through the platform file manager or ask the user to provide an accessible file URL.

#### Async Task Pattern

`render_turntable`, `render_views`, `render_custom`, `run_script`, `check_printability`, `fix_printability`, `voxel_remesh`, and `slice_for_printing` return a task immediately. Always follow this pattern:

1. Call the async action.
2. Save the returned `task_id`.
3. Poll `get_task` until `status` is `completed` or `failed`.
4. When completed, read the returned `outputs` array and give the user the `signed_url`, `file_id`, `filename`, and `size_bytes`.
5. If still processing, wait and poll again. Do not assume failure just because the first response has no file links.

`convert_format` is the exception: it returns the converted file directly in the first response. If the queue is full it returns HTTP 429 with `error_code: "GPU_RENDER_QUEUE_FULL"` and a `Retry-After` hint; back off and retry.

You may abort a task you submitted with `cancel_task` (queued or running). The task transitions to `status: "failed"` with `error_code: "GPU_RENDER_TASK_CANCELED"` once the SIGTERM grace window closes (≤30 seconds for a running render, immediate for a queued one).

#### Queue and Capacity

- The GPU serves one render at a time. Submissions queue strictly in arrival order — there is **no per-budget reordering** or fair-share. Visibility (`queue_position`, `queue_eta_seconds`) is the fairness mechanism.
- Maximum queue depth is **50**. A submission past that limit returns HTTP 429 with body `{"success": false, "output": {"error": "...", "error_code": "GPU_RENDER_QUEUE_FULL"}}` and a `Retry-After` header. Wait the suggested interval and retry.
- Container restarts: if a job was processing when the container restarted, `get_task` returns `status: "failed"` with `error_code: "GPU_RENDER_CONTAINER_RESTARTED"`. Resubmit the request.

#### Memory Limits

Each render runs under a kernel-enforced memory cap and an additional container-level backstop:

- Per-subprocess: **12 GiB**. A render that allocates beyond this fails fast with `error_code: "BLENDER_SUBPROCESS_MEMORY_LIMIT"`.
- Per-container: **14 GiB hard cap** (catastrophic backstop only — the per-subprocess cap fires first).
- `voxel_remesh` rejects requests whose grid cell count exceeds **5,000,000** with `error_code: "BLENDER_VOXEL_GRID_TOO_LARGE"`. The error message includes the minimum-safe `voxel_size`. For a 150 mm bbox the minimum-safe value is ≈ 0.31 mm; smaller voxels make the grid blow up cubically.
- `run_script` rejects payloads larger than **64 KiB** with `error_code: "BLENDER_RUN_SCRIPT_TOO_LARGE"`. Reach for `convert_format` or `render_views` if the script is just orchestrating a few API calls.

#### Input And Output Rules

Supported model inputs for standard render/convert actions are BLEND, GLB, GLTF, FBX, OBJ, STL, DAE, and PLY.

Supported `convert_format` outputs are `blend`, `glb`, `fbx`, `obj`, `stl`, `dae`, and `ply`.

`fix_printability` re-exports the cleaned mesh and supports a smaller subset (`stl`, `glb`, `obj`, `ply`) — formats designed for 3D-printing pipelines.

`slice_for_printing` accepts the same model inputs as the renderers and returns a `.gcode` file plus a Blender-rendered "model on the printbed" preview PNG with the print-time and filament numbers overlaid.

Every model-taking action accepts `source_units` (see "Units") to declare the unit basis of the input file when it cannot be inferred.

For `run_script`, any files saved directly inside `OUTPUT_DIR` are uploaded automatically. Use `output_type` to tell the tool what files to return:
- `image` returns image outputs such as `.png`, `.jpg`, `.jpeg`, and `.webp`.
- `video` returns video outputs such as `.mp4`, `.mov`, and `.webm`.
- `model` returns model outputs such as `.blend`, `.glb`, `.gltf`, `.fbx`, `.obj`, `.stl`, `.dae`, `.ply`, and `.usdz`.
- `all` returns every regular file written to `OUTPUT_DIR`.

If `output_type` does not match the files your script writes, the task can complete with skipped files. For example, set `output_type: "model"` when saving a `.blend` file and `output_type: "video"` when writing an `.mp4`.

Blender project files are returned as generic binary downloads for broad client compatibility. They still use the `.blend` filename extension.

#### Render Quality And Framing

The standard render actions automatically center and scale models for consistent framing. Leave `camera_distance` unset unless the user explicitly asks for a manual distance.

Use these defaults for reliable results:
- Product-style previews: `lighting_preset: "product"`, `background_color: "ffffff"`, `fit_margin: 1.35` to `1.6`, `camera_lens_mm: 28` to `35`.
- General studio previews: `lighting_preset: "studio"`, default background, default framing.
- Fast draft previews: out-of-the-box defaults are tuned for this — `resolution: "720p"`, `samples: 8`, with 12-24 turntable frames for a quick spin.
- Higher quality stills: opt in with `resolution: "1080p"` or `2k` and `samples: 32` to `128`. Hero marketing renders may use `samples: 128+`.

For turntables, slower and smoother videos use more frames and longer duration. A useful default is 24 frames over 6 seconds for a quick review, or 72-96 frames over 6-8 seconds for smoother presentation.

The service renders with Cycles on an NVIDIA L4 GPU in production (Cloud Run); local dev falls back to CPU when no GPU is attached. Very large `samples` × `resolution` × `frames` combinations will still hit the per-action timeout cap even on GPU; choose the fast defaults for previews and only opt in to higher quality when the output justifies the wait. For very heavy STL imports, `decimate_ratio` lowers polygon count before rendering and is the right control to reach for instead of dropping resolution.

#### Units

Every action that takes a model normalizes it to real-world size before doing anything else, using one rule set:

- `source_units` (optional on every model-taking action): `auto` (default), `mm`, `cm`, `m`, `in`, or `native`.
- `auto` means: an STL whose header declares a unit (Onshape writes `Units = meters`) is read in that unit; otherwise STL / OBJ / PLY are read as **millimetres** (the 3D-printing convention PrusaSlicer also assumes) and glTF / GLB / FBX / DAE / BLEND are read as their own native units.
- Set `source_units` explicitly when a mesh was written in another unit without saying so (for example `source_units: "m"` for a metre-valued STL with a blank header).
- All reported sizes are real-world: `model_stats.bounding_box_mm`, `volume_mm3`, `voxel_size`, `bbox_before`, `metadata.max_layer_z_mm` are millimetres regardless of what the file declared.
- STL / OBJ / PLY outputs from `fix_printability`, `voxel_remesh` and `convert_format` are always written in millimetres, so they round-trip through `check_printability` and `slice_for_printing` at the same size. glTF / GLB / FBX / DAE / BLEND are written native.
- Responses include a `units` block (`source_units_requested`, `source_units_resolved`, `import_scale_to_meters`, `stl_header_units`, plus `export_units` / `slicer_scale` where relevant) so you can confirm the basis that was applied.

#### Printability QA

`check_printability` and `fix_printability` use Blender's `object_print3d_utils` addon to surface the geometric problems an FFF/FDM printer slicer cannot recover from. The model is normalized to real-world units first (see "Units"), so `thickness_min_mm` and the degenerate-face threshold (`0.01 mm²`, faces smaller than a 0.4 mm nozzle can resolve) mean the same thing for a mm-valued and a metre-valued file.

The single contract for `summary.is_printable`:

> A model is printable iff it has no non-manifold edges, no non-manifold vertices, no self-intersecting faces, and no degenerate faces or edges.

Distorted faces, thin walls (below `thickness_min_mm`), and steep overhangs (above `overhang_angle_deg`) are all reported as `warning_count` rather than blockers — they are slicer-tunable and printer-dependent (an SLA printer can print steeper overhangs than an FDM printer; supports usually rescue most overhangs anyway).

##### Choosing between `fix_printability` and `voxel_remesh`

Both repair actions produce a printable export. They use different techniques and have different trade-offs — pick based on the *severity* of the input's issues:

- **`fix_printability`** runs Blender's lightweight clean operators (clean-non-manifold, clean-distorted). Preserves fine surface detail. The right tool when `check_printability` reports a small number of issues (dozens to a few hundred), typically from CAD exports or hand-modeled meshes with a few stray non-manifolds. If the input is structurally broken, this action's clean operators can actually make the metrics worse.
- **`voxel_remesh`** rebuilds the entire mesh from a uniform voxel grid via OpenVDB. Guaranteed manifold output. Loses sub-voxel surface detail (smooths fine grooves, embossed text smaller than the voxel size). The right tool for organic 3D-modeled / sculpted shapes, photogrammetry exports, self-intersecting Boolean unions, inverted-normal regions, and dense multi-shell tessellation problems. Typically the only thing that fixes Meshy / sculpting / photogrammetry output. The auto-scaled voxel size keeps tentacle-class silhouette features intact on a normal-sized print.

A reasonable default workflow: call `check_printability` first; if `summary.issue_count` is in the dozens or low hundreds, try `fix_printability`. If it's in the thousands, go straight to `voxel_remesh`.

#### Slicing

`slice_for_printing` ships one bundled printer profile, `prusa_mk4_pla_020`, an Original Prusa MK4 with the 0.4mm nozzle, Generic PLA filament, and the 0.20mm QUALITY print profile (250 × 210 mm bed, 0.2mm layers, 15% infill, no supports). The override fields (`layer_height_mm`, `infill_density_pct`, `support_material`) apply on top of that profile per call. The action returns:

- `model.gcode` — the actual G-code that a printer can stream from.
- `slice_preview.png` — a Blender-rendered image showing the model resting on a printbed-sized plane in roughly PrusaSlicer's default 3D-view orientation, with print-time / filament / layer / profile-name lines overlaid in the bottom-right corner. This is a wayfinding visual, not a hero render. The model and the bed share one unit basis (see "Units"), so the model appears at true size on the bed.
- `metadata` — the parsed time / filament fields from the slicer's gcode comment block, plus `total_layers` and `max_layer_z_mm` counted from the per-layer `;LAYER_CHANGE` / `;Z:` markers when the slicer omits a summary line.
- `units` — the unit basis applied to the input and the `--scale` (if any) passed to the slicer.

#### Security And Script Safety

Blender starts with Python auto-execution disabled when loading files, including user-provided `.blend` inputs.

`run_script` executes the script in Blender, so keep scripts scoped to the requested task. Save only intended outputs into `OUTPUT_DIR`. Do not assume application source files, credentials, or other task working directories are available.

#### Actions

##### render_turntable

Generate a spinning turntable video of a 3D model with professional lighting. Returns a task_id immediately.

**Required fields:**
- `file_url` or `file_id` — the 3D model (BLEND, GLB, FBX, OBJ, STL, DAE, PLY)

**Optional fields:**
- `frames` (int, 12-120, default 72) — number of animation frames
- `duration_seconds` (float, 1-30, default 6) — video length in seconds
- `resolution` (string, default "720p") — 720p, 1080p, 2k, 4k, or custom WxH. Raise to 1080p or higher for hero output; the default is tuned for fast previews.
- `samples` (int, 1-512, default 8) — render quality (higher = better but slower). Raise to 32-64 for hero stills, 128+ for marketing renders.
- `background_color` (hex string without #, default "1a1a1a") — background color
- `lighting_preset` (string, default "studio") — studio, product, outdoor, dramatic
- `elevation` (float, -45 to 90, default 25) — camera elevation angle in degrees
- `camera_distance` (float, optional) — explicit camera distance; omit for automatic full-object framing
- `camera_lens_mm` (float, 10-120, default 35) — focal length in mm; lower is wider
- `fit_margin` (float, 1-3, default 1.25) — auto-framing padding; higher leaves more space around the model
- `decimate_ratio` (float, 0.05-1.0, optional) — polygon-reduction ratio applied before rendering. 0.5 keeps half the faces, 0.2 keeps a fifth, omit (or 1.0) for full fidelity. Use for very heavy STL imports of organic / 3D-print geometry where preview-quality renders are acceptable.

**Example — basic turntable:**
```json
{"action": "render_turntable", "file_url": "https://example.com/model.glb"}
```

**Example — slow smooth spin at high quality:**
```json
{"action": "render_turntable", "file_url": "https://example.com/model.glb", "frames": 96, "duration_seconds": 8, "resolution": "1080p", "samples": 48, "lighting_preset": "product"}
```

**Example — wider framing:**
```json
{"action": "render_turntable", "file_id": "abc-123-def", "fit_margin": 1.6, "camera_lens_mm": 28}
```

**Example — quick low-res preview:**
```json
{"action": "render_turntable", "file_id": "abc-123-def", "frames": 12, "duration_seconds": 2, "resolution": "720p", "samples": 16}
```

**Example — dramatic lighting with low camera:**
```json
{"action": "render_turntable", "file_url": "https://example.com/character.glb", "lighting_preset": "dramatic", "elevation": 10, "background_color": "000000"}
```

---

##### render_views

Render the model from multiple preset camera angles and return individual images. Returns a task_id immediately.

**Required fields:**
- `file_url` or `file_id`

**Optional fields:**
- `views` (array of strings) — front, back, left, right, top, bottom, 3quarter. Default: front, back, left, right, top, 3quarter.
- `resolution`, `samples`, `background_color`, `lighting_preset` — same as render_turntable
- `camera_distance` (float, optional) — explicit camera distance; omit for automatic full-object framing
- `camera_lens_mm` (float, 10-120, default 35) — focal length in mm; lower is wider
- `fit_margin` (float, 1-3, default 1.25) — auto-framing padding; higher leaves more space around the model
- `decimate_ratio` (float, 0.05-1.0, optional) — polygon-reduction ratio applied before rendering. Same semantics as render_turntable.

**Example — all default views:**
```json
{"action": "render_views", "file_url": "https://example.com/model.glb"}
```

**Example — specific views with product lighting:**
```json
{"action": "render_views", "file_url": "https://example.com/model.glb", "views": ["front", "3quarter", "top"], "lighting_preset": "product", "background_color": "ffffff"}
```

**Example — using a stored file:**
```json
{"action": "render_views", "file_id": "abc-123-def", "views": ["front", "back"], "resolution": "2k"}
```

**Example — wider product views:**
```json
{"action": "render_views", "file_id": "abc-123-def", "views": ["front", "3quarter"], "lighting_preset": "product", "background_color": "ffffff", "fit_margin": 1.45, "camera_lens_mm": 30}
```

---

##### render_custom

Render with a custom camera position, target, and field of view. Returns a task_id immediately.

**Required fields:**
- `file_url` or `file_id`

**Optional fields:**
- `camera_position` (array [x, y, z], default [3, -3, 2.5]) — camera world position
- `look_at` (array [x, y, z], default [0, 0, 0]) — point the camera looks at
- `fov` (float, 10-120, default 50) — focal length in mm (lower = wider angle)
- `resolution`, `samples`, `background_color`, `lighting_preset`

**Example — close-up from the front:**
```json
{"action": "render_custom", "file_url": "https://example.com/model.glb", "camera_position": [0, -3, 1], "look_at": [0, 0, 0.5], "fov": 35}
```

**Example — bird's eye view:**
```json
{"action": "render_custom", "file_url": "https://example.com/building.glb", "camera_position": [0, 0, 8], "look_at": [0, 0, 0], "fov": 50, "lighting_preset": "outdoor"}
```

**Example — dramatic side angle:**
```json
{"action": "render_custom", "file_url": "https://example.com/model.glb", "camera_position": [6, -1, 2], "lighting_preset": "dramatic", "background_color": "0a0a0a"}
```

---

##### convert_format

Convert a 3D model between file formats using Blender's importers and exporters. Runs **synchronously** (returns result immediately).

**Required fields:**
- `file_url` or `file_id` — the source 3D model
- `output_format` (string) — target format: blend, glb, fbx, obj, stl, dae, ply

**Optional fields:**
- `apply_transforms` (boolean, default true) — apply location, rotation, and scale transforms before interchange-format export. Ignored for `blend` output so editable Blender scene transforms are preserved.
- `source_units` (string, default `auto`) — unit basis of the input; see "Units". STL / OBJ / PLY outputs are written in millimetres, glTF / GLB / FBX / DAE / BLEND natively (glTF is metres by spec). The response includes a `units` block.

**Example — FBX to GLB for web:**
```json
{"action": "convert_format", "file_url": "https://example.com/model.fbx", "output_format": "glb"}
```

**Example — GLB to STL for 3D printing:**
```json
{"action": "convert_format", "file_id": "abc-123-def", "output_format": "stl"}
```

**Example — OBJ to FBX for Unity:**
```json
{"action": "convert_format", "file_url": "https://example.com/model.obj", "output_format": "fbx"}
```

**Example — GLB to Blender project file:**
```json
{"action": "convert_format", "file_id": "abc-123-def", "output_format": "blend"}
```
Blender project files are returned as generic binary downloads for broad client compatibility.

**Typical time:** Under 5 seconds for most models.

---

##### check_printability

Run a structured 3D-printability analysis on a model using Blender's bundled `object_print3d_utils` addon. Read-only — no upload, no mesh mutation. Returns a task_id immediately.

**Required fields:**
- `file_url` or `file_id` — the 3D model

**Optional fields:**
- `checks` (array of strings, default all six) — subset of `solid`, `intersect`, `degenerate`, `distort`, `thick`, `overhang`
- `thickness_min_mm` (float, 0.05-10.0, default 0.5) — wall-thickness threshold
- `overhang_angle_deg` (float, 10-89, default 45.0) — overhang threshold
- `distort_angle_deg` (float, 5-89, default 45.0) — face-distortion threshold
- `source_units` (string, default `auto`) — unit basis of the file; see "Units"

**Response shape (in `outputs[0]`):** `type: "printability_report"`, `summary.is_printable` (bool), `summary.issue_count`, `summary.warning_count`, `results.{solid,intersect,degenerate,distort,thick,overhang}` per-check counts, `thresholds` (including `degenerate_threshold_mm2`), a `units` block, and a `model_stats` block with vertex/face/edge counts and `bounding_box_mm` / `volume_mm3` in real-world millimetres. `is_printable` is `true` only when the mesh is manifold, non-self-intersecting, and free of degenerate geometry (faces of 0.01 mm² or less) — distorted faces, thin walls, and steep overhangs register as warnings, not blockers. Sanity-check `model_stats.bounding_box_mm` against the size you expect; if it is off by 1000x, pass `source_units` explicitly.

**Example — full default check:**
```json
{"action": "check_printability", "file_url": "https://example.com/model.glb"}
```

**Example — custom thickness threshold:**
```json
{"action": "check_printability", "file_id": "abc-123-def", "thickness_min_mm": 1.2}
```

**Example — only the manifold + intersect checks:**
```json
{"action": "check_printability", "file_url": "https://example.com/model.glb", "checks": ["solid", "intersect"]}
```

---

##### fix_printability

Run the same checks, then attempt the addon's auto-clean operators and re-export the cleaned mesh in the requested format. Returns a task_id immediately.

**Required fields:**
- `file_url` or `file_id`
- `output_format` (string) — `stl`, `glb`, `obj`, or `ply`

**Optional fields:**
- `auto_fix_non_manifold` (boolean, default true) — run `print3d_clean_non_manifold`
- `auto_fix_distorted` (boolean, default true) — run `print3d_clean_distorted`
- `checks`, `thickness_min_mm`, `overhang_angle_deg`, `distort_angle_deg`, `source_units` — same as `check_printability`

**Response shape (in `outputs[0]`):** all the fields of `check_printability` PLUS `before` and `after` blocks with the per-check results, a `fixes_applied` array (e.g. `["non_manifold", "distorted"]`), a `model_stats` block split into `before`/`after`, and the standard upload fields `signed_url`, `file_id`, `filename`, `size_bytes` for the cleaned export. STL / OBJ / PLY exports are written in millimetres (`units.export_units`), so a 73 mm part stays 73 mm when re-checked or sliced.

**Example — fix and export STL:**
```json
{"action": "fix_printability", "file_url": "https://example.com/model.glb", "output_format": "stl"}
```

**Example — only run the manifold cleanup, skip distorted:**
```json
{"action": "fix_printability", "file_id": "abc-123-def", "output_format": "stl", "auto_fix_distorted": false}
```

**Example — tighter thin-wall threshold for fine-detail prints:**
```json
{"action": "fix_printability", "file_url": "https://example.com/figurine.glb", "output_format": "stl", "thickness_min_mm": 0.8}
```

---

##### voxel_remesh

Rebuild a model into a watertight manifold via OpenVDB voxel remesh. Returns a task_id immediately.

The right tool for inputs that are structurally broken — meshes the lightweight `fix_printability` operators cannot rescue:

- 3D-modeled / sculpted organic shapes with overlapping geometry (tentacles, character models, organic planters)
- Photogrammetry exports with shell artifacts
- Self-intersecting Boolean union output from sloppy CAD
- Inverted-normal regions
- Dense multi-shell tessellation problems on heavily-decimated meshes

The output is **guaranteed manifold** (no non-manifold edges or self-intersections, normals consistently pointed outward). The trade-off is that surface detail smaller than the voxel size gets smoothed away.

**Required fields:**
- `file_url` or `file_id`
- `output_format` (string) — `stl`, `glb`, `obj`, or `ply`

**Optional fields:**
- `voxel_size` (float, 0.01–100.0) — explicit voxel size in **millimetres** (the model is normalized to real-world units first; see "Units"). Smaller values preserve more detail at the cost of compute time. Omit to auto-scale to ~1.3% of the longest bounding-box dimension with a 0.5 mm floor, which works well for most print-scale models.
- `source_units` (string, default `auto`) — unit basis of the file; see "Units"

**Response shape (in `outputs[0]`):** `type: "voxel_remesh_report"`, `voxel_size` (mm, `voxel_size_units: "mm"`), `voxel_size_source: "auto"|"override"`, `bbox_before` (3-tuple, mm), `before` and `after` blocks with manifold metrics (`vertices`, `faces`, `edges`, `non_manifold_edges`, `non_manifold_verts`, `bad_contiguous_edges`), `is_manifold_after` (bool), and the standard upload fields `signed_url`, `file_id`, `filename`, `size_bytes` for the remeshed export (STL / OBJ / PLY written in millimetres).

**Example — repair an organic 3D-modeled mesh:**
```json
{"action": "voxel_remesh", "file_url": "https://example.com/sculpt.glb", "output_format": "stl"}
```

**Example — finer detail for a small jewelry-class model:**
```json
{"action": "voxel_remesh", "file_id": "abc-123-def", "output_format": "stl", "voxel_size": 0.3}
```

**Example — coarser remesh for a large statue (faster, smaller output):**
```json
{"action": "voxel_remesh", "file_url": "https://example.com/statue.glb", "output_format": "glb", "voxel_size": 5.0}
```

---

##### slice_for_printing

Slice a model with PrusaSlicer's headless CLI against a bundled printer profile (default: `prusa_mk4_pla_020`, an Original Prusa MK4 with 0.4mm nozzle, Generic PLA, 0.20 mm QUALITY). Returns the gcode, a Blender-rendered "model on the printbed" preview PNG with the print-time and filament numbers overlaid in the corner, and parsed metadata. Returns a task_id immediately.

**Required fields:**
- `file_url` or `file_id`

**Optional fields:**
- `printer_profile` (string, default `prusa_mk4_pla_020`) — bundled profile name (lowercase letters, digits, underscores)
- `layer_height_mm` (float, 0.05-0.6) — override the slicer's layer height; omit to use the profile's value
- `infill_density_pct` (int, 0-100) — override infill density percent
- `support_material` (boolean) — override the support-material toggle
- `source_units` (string, default `auto`) — unit basis of the file; see "Units". A metre-valued STL is rescaled for the slicer automatically when its header says so, or when you pass `source_units: "m"`.

**Response shape (in `outputs[0]`):** `type: "slice_result"`, `printer_profile`, `bed_dimensions_mm`, `units` (`source_units_resolved`, `slicer_scale`, ...), `metadata.{estimated_print_time_seconds,estimated_print_time_formatted,filament_used_mm,filament_used_g,filament_used_cm3,filament_cost,total_layers,max_layer_z_mm}`, `gcode.{signed_url,file_id,filename,size_bytes}` for `model.gcode`, and `preview.{signed_url,file_id,filename,size_bytes}` for `slice_preview.png` (the printbed preview with the metadata overlay). `total_layers` / `max_layer_z_mm` are counted from the gcode's per-layer markers, so they are populated even when the slicer writes no summary line.

**Example — default slice:**
```json
{"action": "slice_for_printing", "file_url": "https://example.com/model.glb"}
```

**Example — finer 0.10 mm layers:**
```json
{"action": "slice_for_printing", "file_id": "abc-123-def", "layer_height_mm": 0.10}
```

**Example — force supports off and 30% infill:**
```json
{"action": "slice_for_printing", "file_url": "https://example.com/model.glb", "support_material": false, "infill_density_pct": 30}
```

---

##### run_script

Execute a custom Blender Python script on a model for advanced operations. Returns a task_id immediately.

**Required fields:**
- `script` (string) — Blender Python code to execute

**Optional fields:**
- `file_url` or `file_id` — model to load before running the script (optional; the script can create from scratch)
- `output_type` (string) — image, video, model, all. Hint for what the script produces. Use `model` for `.blend`, `.glb`, `.fbx`, `.obj`, `.stl`, `.dae`, `.ply`, and `.usdz` outputs.
- `script_timeout_seconds` (int, 600-1800, optional) — override the per-subprocess timeout for this run. The default is auto-scaled based on the rendered resolution and samples. Use this only when a script genuinely needs more than the default budget; it cannot exceed the service maximum (1800s).

**Available variables in the script:**
- `bpy` — the full Blender Python API
- `MODEL_PATH` — filesystem path to the downloaded model (empty string if no model provided)
- `OUTPUT_DIR` — directory to save output files. All files saved here are automatically uploaded and returned in the task outputs.

**Example — render with Cycles ray-tracing:**
```json
{
  "action": "run_script",
  "file_url": "https://example.com/model.glb",
  "script": "import bpy, os\nbpy.ops.import_scene.gltf(filepath=MODEL_PATH)\nbpy.context.scene.render.engine = 'CYCLES'\nbpy.context.scene.cycles.samples = 128\nbpy.context.scene.render.resolution_x = 1920\nbpy.context.scene.render.resolution_y = 1080\ncam = bpy.data.cameras.new('Cam')\ncam_obj = bpy.data.objects.new('Cam', cam)\nbpy.context.scene.collection.objects.link(cam_obj)\nbpy.context.scene.camera = cam_obj\ncam_obj.location = (4, -4, 3)\ntrack = cam_obj.constraints.new('TRACK_TO')\nempty = bpy.data.objects.new('T', None)\nempty.location = (0, 0, 0)\nbpy.context.scene.collection.objects.link(empty)\ntrack.target = empty\ntrack.track_axis = 'TRACK_NEGATIVE_Z'\ntrack.up_axis = 'UP_Y'\nlight = bpy.data.lights.new('Sun', 'SUN')\nlight.energy = 5\nlight_obj = bpy.data.objects.new('Sun', light)\nlight_obj.rotation_euler = (0.8, 0, 0.5)\nbpy.context.scene.collection.objects.link(light_obj)\nbpy.context.scene.render.filepath = os.path.join(OUTPUT_DIR, 'render.png')\nbpy.ops.render.render(write_still=True)"
}
```

**Example — get model statistics:**
```json
{
  "action": "run_script",
  "file_url": "https://example.com/model.glb",
  "script": "import bpy, os, json\nbpy.ops.import_scene.gltf(filepath=MODEL_PATH)\nmeshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']\nstats = {'meshes': len(meshes), 'total_vertices': sum(len(m.data.vertices) for m in meshes), 'total_faces': sum(len(m.data.polygons) for m in meshes)}\nwith open(os.path.join(OUTPUT_DIR, 'stats.json'), 'w') as f:\n    json.dump(stats, f, indent=2)"
}
```

**Example — apply a subdivision modifier and re-export:**
```json
{
  "action": "run_script",
  "file_url": "https://example.com/lowpoly.glb",
  "script": "import bpy, os\nbpy.ops.import_scene.gltf(filepath=MODEL_PATH)\nfor obj in bpy.context.scene.objects:\n    if obj.type == 'MESH':\n        mod = obj.modifiers.new('Subdiv', 'SUBSURF')\n        mod.levels = 2\nbpy.ops.export_scene.gltf(filepath=os.path.join(OUTPUT_DIR, 'subdivided.glb'), export_format='GLB')"
}
```

**Example — save the processed scene as a Blender file:**
```json
{
  "action": "run_script",
  "file_url": "https://example.com/model.glb",
  "output_type": "model",
  "script": "import bpy, os\nbpy.ops.import_scene.gltf(filepath=MODEL_PATH)\nbpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUTPUT_DIR, 'scene.blend'))"
}
```

---

##### get_task

Check the status of a render task and retrieve download links when complete.

**Required fields:**
- `task_id` (string) — the task ID returned from any async render action

**Example:**
```json
{"action": "get_task", "task_id": "849b4c79-2c2e-4886-bd40-1c01a8a2bd1d"}
```

**Response when processing:**
```json
{"action": "get_task", "task_id": "849b4c79...", "status": "processing", "progress": 25, "stage": "running_checks", "date_updated": "2026-09-11T14:02:11+00:00", "queue_position": 0, "queue_eta_seconds": 60, "queue_stats": {"queue_total_running": 1, "queue_total_queued": 2, "queue_total_capacity": 50}}
```

`queue_position` is `0` when the task is running, `N` when it is the Nth slot from the front of the queue. `queue_eta_seconds` is the best-guess wait until the task is dequeued (always `0` for a running task). `queue_stats` summarizes the current queue state. All three fields are omitted on terminal records.

`progress` is **coarse**: it advances only at stage boundaries (queued → started → downloading_model → running_checks / slicing / rendering → uploading), not continuously, so it can sit at one value for the whole Blender or slicer run. Key off `status` for completion, `stage` for what the worker is doing, and `date_updated` as a heartbeat; a task whose `date_updated` is more than a few minutes old with no `stage` change is the one to `cancel_task`. Never treat a flat `progress` alone as "hung".

**Response when completed:**
```json
{"action": "get_task", "task_id": "849b4c79...", "status": "completed", "progress": 100, "outputs": [{"type": "video", "signed_url": "https://...", "file_id": "...", "size_bytes": 426703}]}
```

**Response when failed:**
```json
{"action": "get_task", "task_id": "849b4c79...", "status": "failed", "error": "Blender exited with code 1."}
```

The `error` field contains a sanitized message — `"Blender timed out after Ns."`, `"Blender exited with code N."`, `"ffmpeg timed out after Ns."`, or a validation message — where `N` reflects the auto-scaled per-action timeout in effect, not a fixed wall.

---

##### cancel_task

Cancel a queued or running task. Idempotent: cancelling an already-terminal task returns an error explaining that.

**Required fields:**
- `task_id` (string) — the task ID returned from any async render action.

**Example — cancel a queued task:**
```json
{"action": "cancel_task", "task_id": "849b4c79-2c2e-4886-bd40-1c01a8a2bd1d"}
```

**Response (success):**
```json
{"action": "cancel_task", "task_id": "849b4c79...", "cancel_outcome": "queued_or_running_canceled"}
```

The task itself transitions to `status: "failed"` with `error_code: "GPU_RENDER_TASK_CANCELED"` once the SIGTERM grace window closes (≤30 seconds for a running render, immediate for a queued one). Poll `get_task` to confirm the terminal state.

**Cancel a running task:**
```json
{"action": "cancel_task", "task_id": "1b4f2acc-ff15-4b86-9d6d-2bd1c3a1b1d1"}
```

The semantics are identical — cancellation does not block awaiting subprocess termination; the response returns immediately and the task moves to terminal state asynchronously.

---

##### list_tasks

List all render tasks for the current user, most recent first.

**Optional fields:**
- `limit` (int, 1-100, default 20) — maximum tasks to return

**Example:**
```json
{"action": "list_tasks", "limit": 10}
```

**Response:**
```json
{"action": "list_tasks", "count": 3, "tasks": [{"task_id": "...", "action": "render_turntable", "status": "completed", "progress": 100, "outputs": [...]}, {"task_id": "...", "action": "render_views", "status": "processing", "progress": 45}]}
```

---

#### Recommended Workflows

##### Basic render workflow
1. Call `render_turntable` or `render_views` with your model URL — get a `task_id`
2. Wait 1-5 minutes depending on complexity
3. Call `get_task` with the `task_id`
4. If `status` is `"completed"`, the `outputs` array has download links
5. If `status` is still `"processing"`, check `progress` and wait a bit longer

##### Multiple renders at once
Submit multiple render requests — they run in parallel:
```json
{"action": "render_turntable", "file_url": "https://...", "lighting_preset": "studio"}
{"action": "render_views", "file_url": "https://...", "views": ["front", "3quarter"]}
```
Then use `list_tasks` to see all of them at once, or `get_task` on each individually.

##### Generate a 3D model and render it
1. Use the 3D Modeling Agent to create a model from text or image
2. Take the GLB download URL from the completed task
3. Pass it to `render_turntable` or `render_views` to get professional renders
4. Use `convert_format` to export to FBX for Unity or STL for 3D printing

---

#### Lighting Presets

| Preset | Description | Best For |
|--------|-------------|----------|
| studio | 3-point lighting (key, fill, rim). Neutral white, soft shadows. | Product shots, portfolio renders, general purpose |
| product | Large soft overhead light with bottom fill. Clean, even illumination. | E-commerce product photography, catalogs |
| outdoor | Sun lamp with ambient sky fill. Natural daylight feel. | Architectural models, outdoor scenes |
| dramatic | Single hard spotlight from the side. Deep shadows, dark background. | Character models, cinematic presentations, game assets |

#### Supported Formats

| Direction | Formats |
|-----------|---------|
| Import | BLEND, GLB, GLTF, FBX, OBJ, STL, DAE, PLY |
| Export (convert_format) | BLEND, GLB, FBX, OBJ, STL, DAE, PLY |
| Export (fix_printability / voxel_remesh) | STL, GLB, OBJ, PLY |
| Slicer output | G-code (`.gcode`) + printbed preview PNG |

#### Notes

- Models are automatically centered and scaled for consistent framing across all render actions.
- Unit handling is uniform across actions (see "Units"): imports are normalized to real-world size, unit-less mesh formats default to millimetres, and STL / OBJ / PLY outputs are written in millimetres.
- Blender runs with Python auto-execution disabled when loading files, including user-provided `.blend` inputs.
- Turntable videos are rendered as individual PNG frames then stitched to H.264 MP4 via ffmpeg.
- Cycles is the default render engine and runs on GPU when available, falling back to CPU automatically when no GPU is attached. Use `run_script` with `bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'` only if you need EEVEE specifically.
- Output files are stored for 7 days via signed URLs.
- Each Blender subprocess runs under an auto-scaled timeout — floor 10 minutes (600s) for trivial work, scaling with frames × resolution × samples × view count, capped at 30 minutes (1800s). Very large requests (high samples, 4K resolution, many frames or views) hit the cap and may time out; choose the fast defaults for previews and only opt in to higher quality when the output justifies the wait.
- The `run_script` action gives full access to the Blender Python API. Save output files to `OUTPUT_DIR` and they are automatically uploaded.

## When To Use
- Use this skill for `Blender 3D Modeling` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: blender 3d modeling, render turntable videos of 3d models for game asset previews, create multi angle product shots from 3d models for e commerce, convert 3d files between formats like glb to blend, glb to fbx, cancel task, task id, check printability.
- Supported action names: `cancel_task`, `check_printability`, `convert_format`, `fix_printability`, `get_task`, `list_tasks`, `render_custom`, `render_turntable`, `render_views`, `run_script`, `slice_for_printing`, `voxel_remesh`.

## Use Cases
- Render turntable videos of 3D models for game asset previews
- Create multi-angle product shots from 3D models for e-commerce
- Convert 3D files between formats like GLB to BLEND
- GLB to FBX
- or OBJ to STL
- Save procedurally generated scenes as Blender .blend files
- Generate professional renders with studio lighting for portfolios
- Preview 3D-printed models from every angle before printing
- Render architectural models with custom camera positions
- Create spinning animations of characters or props for social media
- Apply dramatic lighting to 3D models for cinematic presentations
- Run custom Blender Python scripts for advanced 3D processing
- Render 3D models generated by AI tools like Meshy with proper textures and lighting
- Convert game assets between Unity FBX and web GLB formats
- Generate thumbnail images of 3D models for catalogs and marketplaces

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `12`.
x402 availability: not enabled for this product.

- `cancel_task` (action slug: `cancel-task`): Cancel a queued or running render task. Idempotent: cancelling an already-terminal task returns an error explaining that. Queued tasks transition immediately; running tasks transition once the SIGTERM grace window closes (≤30s). The task ends with status='failed' and error_code='GPU_RENDER_TASK_CANCELED'. Poll get_task to confirm the terminal state. Price: `25` credits. Parameters: `task_id`.
- `check_printability` (action slug: `check-printability`): Run a structured 3D-printability analysis using Blender's object_print3d_utils addon. Read-only — no upload, no mesh mutation. Returns a task_id immediately. Price: `25` credits. Parameters: `checks`, `distort_angle_deg`, `file_id`, `file_url`, `overhang_angle_deg`, `source_units`, `thickness_min_mm`.
- `convert_format` (action slug: `convert-format`): Convert a 3D model between file formats. Runs synchronously through the queue; if the queue is full, returns 429 with error_code GPU_RENDER_QUEUE_FULL. Price: `25` credits. Parameters: `apply_transforms`, `file_id`, `file_url`, `output_format`, `source_units`.
- `fix_printability` (action slug: `fix-printability`): Light-touch repair using Blender's object_print3d_utils clean operators. For mostly-clean inputs (CAD exports, few stray non-manifolds). Use voxel_remesh for structurally-broken inputs. Price: `25` credits. Parameters: `auto_fix_distorted`, `auto_fix_non_manifold`, `checks`, `distort_angle_deg`, `file_id`, `file_url`, `output_format`, `overhang_angle_deg`, plus 2 more.
- `get_task` (action slug: `get-task`): Check the status of a render task and retrieve download links when complete. Non-terminal responses include stage (what the worker is doing: queued, started, downloading_model, running_checks, slicing, rendering_preview, uploading_...) and date_updated as a heartbeat; progress is coarse and only advances at stage boundaries, so key off status and stage rather than a flat progress value. They also include queue_position (0 when running, 1+ when queued), queue_eta_seconds, and queue_stats {queue_total_running, queue_total_queued, queue_total_capacity}. Caller-driven failures (GPU_RENDER_QUEUE_FULL, BLENDER_VOXEL_GRID_TOO_LARGE, BLENDER_RUN_SCRIPT_TOO_LARGE, GPU_RENDER_TASK_CANCELED, BLENDER_SLICER_PROFILE_INVALID) report at warning severity and are safe to retry with corrected inputs; subprocess / memory / timeout failures (GPU_RENDER_BLENDER_NONZERO_EXIT, GPU_RENDER_BLENDER_TIMEOUT, BLENDER_SUBPROCESS_MEMORY_LIMIT, GPU_RENDER_CONTAINER_RESTARTED, GPU_RENDER_UNEXPECTED_ERROR) report at error severity — retry once but escalate if it recurs. Price: `25` credits. Parameters: `task_id`.
- `list_tasks` (action slug: `list-tasks`): List render tasks for the current user, most recent first. Price: `25` credits. Parameters: `limit`.
- `render_custom` (action slug: `render-custom`): Render with a custom camera position. Returns a task_id immediately. Joins the strict-FIFO render queue. Price: `25` credits. Parameters: `background_color`, `camera_position`, `decimate_ratio`, `file_id`, `file_url`, `fov`, `lighting_preset`, `look_at`, plus 3 more.
- `render_turntable` (action slug: `render-turntable`): Generate a spinning turntable video of a 3D model. Returns a task_id immediately; use get_task to check progress and retrieve the output. Joins the strict-FIFO render queue (capacity 50); if the queue is full, returns a 429 with error_code GPU_RENDER_QUEUE_FULL and a Retry-After header. Price: `25` credits. Parameters: `background_color`, `camera_distance`, `camera_lens_mm`, `decimate_ratio`, `duration_seconds`, `elevation`, `file_id`, `file_url`, plus 6 more.
- `render_views` (action slug: `render-views`): Render preset camera angles. Returns a task_id immediately. Joins the strict-FIFO render queue. Price: `25` credits. Parameters: `background_color`, `camera_distance`, `camera_lens_mm`, `decimate_ratio`, `file_id`, `file_url`, `fit_margin`, `lighting_preset`, plus 4 more.
- `run_script` (action slug: `run-script`): Execute a custom Blender Python script. Returns a task_id immediately. Script payload limited to 65,536 bytes — oversize requests fail with error_code BLENDER_RUN_SCRIPT_TOO_LARGE. Price: `25` credits. Parameters: `file_id`, `file_url`, `output_type`, `script`, `script_timeout_seconds`, `source_units`.
- `slice_for_printing` (action slug: `slice-for-printing`): Slice a 3D model with PrusaSlicer and return G-code, parsed metadata, and a Blender-rendered printbed preview PNG. Returns a task_id immediately. Price: `25` credits. Parameters: `file_id`, `file_url`, `infill_density_pct`, `layer_height_mm`, `printer_profile`, `source_units`, `support_material`.
- `voxel_remesh` (action slug: `voxel-remesh`): Rebuild a model into a watertight manifold via OpenVDB voxel remesh. The right tool for structurally-broken inputs. Output is guaranteed manifold; surface detail smaller than the voxel size is smoothed away. Pre-flight rejects requests whose grid cell count exceeds 5,000,000 with error_code BLENDER_VOXEL_GRID_TOO_LARGE — the response message includes the minimum-safe voxel_size for the input, and the report context exposes bbox_x/y/z, voxel_size, cells, max_cells, and min_safe_voxel_size for runbooks. Price: `25` credits. Parameters: `file_id`, `file_url`, `output_format`, `source_units`, `voxel_size`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "blender-3d-modeling"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "blender-3d-modeling"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "blender-3d-modeling"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "blender-3d-modeling"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "blender-3d-modeling"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "blender-3d-modeling"
  }
}
```

## Call This Tool
Product slug: `blender-3d-modeling`

Marketplace page: https://www.agentpmt.com/marketplace/blender-3d-modeling

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Blender-3D-Modeling",
    "arguments": {
      "action": "cancel_task",
      "task_id": "example task id"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "blender-3d-modeling",
  "parameters": {
    "action": "cancel_task",
    "task_id": "example task id"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `cancel_task` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/blender-3d-modeling
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
