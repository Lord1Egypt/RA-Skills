---
name: blender-3d-modeling
description: "Blender 3D Modeling: Blender 3D suite running headless in the cloud. Use when an agent needs blender 3d modeling, render turntable videos of 3d models for game asset previews, create multi angle product shots from 3d models for e commerce, convert 3d files between formats like glb to blend, glb to fbx, cancel task, task id, check printability through AgentPMT-hosted remote tool calls. Discovery terms: blender 3d modeling, render turntable videos of 3d models for game asset previews."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/blender-3d-modeling
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/blender-3d-modeling"}}
---
# Blender 3D Modeling

## Freshness
Last updated: `2026-06-24`.

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

#### Printability QA

`check_printability` and `fix_printability` use Blender's `object_print3d_utils` addon to surface the geometric problems an FFF/FDM printer slicer cannot recover from.

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
- `slice_preview.png` — a Blender-rendered image showing the model resting on a printbed-sized plane in roughly PrusaSlicer's default 3D-view orientation, with print-time / filament / layer / profile-name lines overlaid in the bottom-right corner. This is a wayfinding visual, not a hero render.
- `metadata` — the parsed time / filament / layer-count fields lifted directly out of the slicer's gcode comment block.

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

---

##### render_views

Render the model from multiple preset camera angles and return individual images. Returns a task_id immediately.

**Required fields:**
- `file_url` or `file_id`

**Optional fields:**
- `views` (array of strings) — front, back, left, right, top, bottom, 3quarter. Default: front, back, left, right, top, 3quarter.
- `resolution`, `samples`, `background_color`, `lighting_preset` — same as render_turntable
- `camera_distance`, `camera_lens_mm`, `fit_margin`, `decimate_ratio` — same as render_turntable

---

##### render_custom

Render with a custom camera position, target, and field of view. Returns a task_id immediately.

**Required fields:**
- `file_url` or `file_id`

**Optional fields:**
- `camera_position` (array [x, y, z], default [3, -3, 2.5])
- `look_at` (array [x, y, z], default [0, 0, 0])
- `fov` (float, 10-120, default 50)
- `resolution`, `samples`, `background_color`, `lighting_preset`

---

##### convert_format

Convert a 3D model between file formats. Runs **synchronously**.

**Required fields:**
- `file_url` or `file_id`
- `output_format` (string) — blend, glb, fbx, obj, stl, dae, ply

**Optional fields:**
- `apply_transforms` (boolean, default true) — ignored for `blend` output.

If the queue is full, returns HTTP 429 with `error_code: "GPU_RENDER_QUEUE_FULL"` and a `Retry-After` header.

---

##### check_printability

Run a structured 3D-printability analysis using `object_print3d_utils`. Read-only — no upload, no mesh mutation.

**Required:** `file_url` or `file_id`.

**Optional:** `checks` (subset of solid/intersect/degenerate/distort/thick/overhang), `thickness_min_mm`, `overhang_angle_deg`, `distort_angle_deg`.

---

##### fix_printability

Light-touch repair using the addon's clean operators. Preserves fine surface detail. Use `voxel_remesh` for structurally-broken inputs.

**Required:** `file_url` or `file_id`, `output_format` (`stl`, `glb`, `obj`, `ply`).

**Optional:** `auto_fix_non_manifold` (default true), `auto_fix_distorted` (default true), `checks`, `thickness_min_mm`, `overhang_angle_deg`, `distort_angle_deg`.

---

##### voxel_remesh

Rebuild a model into a watertight manifold via OpenVDB voxel remesh. The right tool for structurally-broken inputs. Output is guaranteed manifold; surface detail smaller than the voxel size is smoothed away.

**Required:** `file_url` or `file_id`, `output_format` (`stl`, `glb`, `obj`, `ply`).

**Optional:** `voxel_size` (float, 0.01–100.0; omit to auto-scale to ~1.3% of the longest bounding-box dimension).

Pre-flight rejects requests whose grid cell count exceeds 5,000,000 with `error_code: "BLENDER_VOXEL_GRID_TOO_LARGE"` — the error message includes the minimum-safe `voxel_size` for the input.

---

##### slice_for_printing

Slice a model with PrusaSlicer's headless CLI against a bundled printer profile. Returns the gcode, a Blender-rendered "model on the printbed" preview PNG, and parsed metadata.

**Required:** `file_url` or `file_id`.

**Optional:** `printer_profile` (default `prusa_mk4_pla_020`), `layer_height_mm`, `infill_density_pct`, `support_material`.

---

##### run_script

Execute a custom Blender Python script. Returns a task_id immediately.

**Required:** `script` (string).

**Optional:** `file_url` or `file_id` (sets MODEL_PATH), `output_type` (image/video/model/all, default image), `script_timeout_seconds` (600-1800).

**Available in the script:** `bpy`, `MODEL_PATH`, `OUTPUT_DIR`. Save output files to `OUTPUT_DIR` for automatic upload.

Script payloads are limited to 64 KiB; oversize requests fail with `error_code: "BLENDER_RUN_SCRIPT_TOO_LARGE"`.

---

##### get_task

Check the status of a render task and retrieve download links when complete.

**Required:** `task_id`.

Non-terminal responses include `queue_position` (0 when running, 1+ when queued), `queue_eta_seconds` (best-guess wait), and `queue_stats` (running/queued/capacity counters). All three are omitted on terminal records.

**Response when processing:**
```json
{"action": "get_task", "task_id": "...", "status": "processing", "progress": 45, "queue_position": 0, "queue_eta_seconds": 60, "queue_stats": {"queue_total_running": 1, "queue_total_queued": 2, "queue_total_capacity": 50}}
```

**Response when failed (cancelled):**
```json
{"action": "get_task", "task_id": "...", "status": "failed", "error": "Task canceled by caller.", "error_code": "GPU_RENDER_TASK_CANCELED"}
```

**Response when failed (container restart):**
```json
{"action": "get_task", "task_id": "...", "status": "failed", "error": "Container restarted before this task could complete.", "error_code": "GPU_RENDER_CONTAINER_RESTARTED"}
```

---

##### cancel_task

Cancel a queued or running task. Idempotent.

**Required:** `task_id`.

**Response (success):**
```json
{"action": "cancel_task", "task_id": "...", "cancel_outcome": "queued_or_running_canceled"}
```

The task itself transitions to `status: "failed"` with `error_code: "GPU_RENDER_TASK_CANCELED"` once the SIGTERM grace window closes (≤30 seconds for a running render, immediate for a queued one). Poll `get_task` to confirm the terminal state.

---

##### list_tasks

List all render tasks for the current user, most recent first.

**Optional:** `limit` (1-100, default 20).

#### Lighting Presets

| Preset | Description | Best For |
|--------|-------------|----------|
| studio | 3-point lighting (key, fill, rim). Neutral white. | Product shots, portfolio |
| product | Large soft overhead with bottom fill. | E-commerce, catalogs |
| outdoor | Sun lamp with ambient sky fill. | Architectural, outdoor |
| dramatic | Single hard spotlight from the side. | Character models, cinematic |

#### Notes

- Models are automatically centered and scaled for consistent framing across render actions.
- Blender runs with Python auto-execution disabled when loading files.
- Turntable videos are rendered as PNG frames then stitched to H.264 MP4 via ffmpeg.
- Cycles is the default render engine; runs on GPU when available, falls back to CPU automatically.
- The `object_print3d_utils` addon is enabled at runtime for `check_printability` / `fix_printability`.
- `voxel_remesh` uses Blender's OpenVDB-backed voxel remesher.
- `slice_for_printing` ships PrusaSlicer 2.x with one bundled MK4 PLA profile.
- Output files are stored for 7 days via signed URLs.
- Each Blender subprocess runs under an auto-scaled timeout — floor 10 minutes (600s), capped at 30 minutes (1800s).
- The render queue is strict-FIFO with capacity 50; a full queue returns HTTP 429 with `error_code: "GPU_RENDER_QUEUE_FULL"` and a `Retry-After` header.
- Per-subprocess memory cap is 12 GiB; per-container backstop is 14 GiB.

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
- `check_printability` (action slug: `check-printability`): Run a structured 3D-printability analysis using Blender's object_print3d_utils addon. Read-only — no upload, no mesh mutation. Returns a task_id immediately. Price: `25` credits. Parameters: `checks`, `distort_angle_deg`, `file_id`, `file_url`, `overhang_angle_deg`, `thickness_min_mm`.
- `convert_format` (action slug: `convert-format`): Convert a 3D model between file formats. Runs synchronously through the queue; if the queue is full, returns 429 with error_code GPU_RENDER_QUEUE_FULL. Price: `25` credits. Parameters: `apply_transforms`, `file_id`, `file_url`, `output_format`.
- `fix_printability` (action slug: `fix-printability`): Light-touch repair using Blender's object_print3d_utils clean operators. For mostly-clean inputs (CAD exports, few stray non-manifolds). Use voxel_remesh for structurally-broken inputs. Price: `25` credits. Parameters: `auto_fix_distorted`, `auto_fix_non_manifold`, `checks`, `distort_angle_deg`, `file_id`, `file_url`, `output_format`, `overhang_angle_deg`, plus 1 more.
- `get_task` (action slug: `get-task`): Check the status of a render task and retrieve download links when complete. Non-terminal responses include queue_position (0 when running, 1+ when queued), queue_eta_seconds, and queue_stats {queue_total_running, queue_total_queued, queue_total_capacity}. Caller-driven failures (GPU_RENDER_QUEUE_FULL, BLENDER_VOXEL_GRID_TOO_LARGE, BLENDER_RUN_SCRIPT_TOO_LARGE, GPU_RENDER_TASK_CANCELED, BLENDER_SLICER_PROFILE_INVALID) report at warning severity and are safe to retry with corrected inputs; subprocess / memory / timeout failures (GPU_RENDER_BLENDER_NONZERO_EXIT, GPU_RENDER_BLENDER_TIMEOUT, BLENDER_SUBPROCESS_MEMORY_LIMIT, GPU_RENDER_CONTAINER_RESTARTED, GPU_RENDER_UNEXPECTED_ERROR) report at error severity — retry once but escalate if it recurs. Price: `25` credits. Parameters: `task_id`.
- `list_tasks` (action slug: `list-tasks`): List render tasks for the current user, most recent first. Price: `25` credits. Parameters: `limit`.
- `render_custom` (action slug: `render-custom`): Render with a custom camera position. Returns a task_id immediately. Joins the strict-FIFO render queue. Price: `25` credits. Parameters: `background_color`, `camera_position`, `decimate_ratio`, `file_id`, `file_url`, `fov`, `lighting_preset`, `look_at`, plus 2 more.
- `render_turntable` (action slug: `render-turntable`): Generate a spinning turntable video of a 3D model. Returns a task_id immediately; use get_task to check progress and retrieve the output. Joins the strict-FIFO render queue (capacity 50); if the queue is full, returns a 429 with error_code GPU_RENDER_QUEUE_FULL and a Retry-After header. Price: `25` credits. Parameters: `background_color`, `camera_distance`, `camera_lens_mm`, `decimate_ratio`, `duration_seconds`, `elevation`, `file_id`, `file_url`, plus 5 more.
- `render_views` (action slug: `render-views`): Render preset camera angles. Returns a task_id immediately. Joins the strict-FIFO render queue. Price: `25` credits. Parameters: `background_color`, `camera_distance`, `camera_lens_mm`, `decimate_ratio`, `file_id`, `file_url`, `fit_margin`, `lighting_preset`, plus 3 more.
- `run_script` (action slug: `run-script`): Execute a custom Blender Python script. Returns a task_id immediately. Script payload limited to 65,536 bytes — oversize requests fail with error_code BLENDER_RUN_SCRIPT_TOO_LARGE. Price: `25` credits. Parameters: `file_id`, `file_url`, `output_type`, `script`, `script_timeout_seconds`.
- `slice_for_printing` (action slug: `slice-for-printing`): Slice a 3D model with PrusaSlicer and return G-code, parsed metadata, and a Blender-rendered printbed preview PNG. Returns a task_id immediately. Price: `25` credits. Parameters: `file_id`, `file_url`, `infill_density_pct`, `layer_height_mm`, `printer_profile`, `support_material`.
- `voxel_remesh` (action slug: `voxel-remesh`): Rebuild a model into a watertight manifold via OpenVDB voxel remesh. The right tool for structurally-broken inputs. Output is guaranteed manifold; surface detail smaller than the voxel size is smoothed away. Pre-flight rejects requests whose grid cell count exceeds 5,000,000 with error_code BLENDER_VOXEL_GRID_TOO_LARGE — the response message includes the minimum-safe voxel_size for the input, and the report context exposes bbox_x/y/z, voxel_size, cells, max_cells, and min_safe_voxel_size for runbooks. Price: `25` credits. Parameters: `file_id`, `file_url`, `output_format`, `voxel_size`.

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
