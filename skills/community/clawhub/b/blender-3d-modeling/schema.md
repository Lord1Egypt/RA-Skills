# Blender 3D Modeling Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `blender-3d-modeling`

x402 availability: not enabled for this product.

## `cancel_task`

Action slug: `cancel-task`

Price: `25` credits

Cancel a queued or running render task. Idempotent: cancelling an already-terminal task returns an error explaining that. Queued tasks transition immediately; running tasks transition once the SIGTERM grace window closes (≤30s). The task ends with status='failed' and error_code='GPU_RENDER_TASK_CANCELED'. Poll get_task to confirm the terminal state.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `task_id` | `string` | yes | Task ID returned from a render action. |

Sample parameters:

```json
{
  "task_id": "example task id"
}
```

Generated JSON parameter schema:

```json
{
  "task_id": {
    "description": "Task ID returned from a render action.",
    "required": true,
    "type": "string"
  }
}
```

## `check_printability`

Action slug: `check-printability`

Price: `25` credits

Run a structured 3D-printability analysis using Blender's object_print3d_utils addon. Read-only — no upload, no mesh mutation. Returns a task_id immediately.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `checks` | `array` | no | Subset of checks to run. Default: all six. |
| `distort_angle_deg` | `number` | no | Face-distortion angle threshold in degrees. Default: 45. |
| `file_id` | `string` | no | AgentPMT file storage ID. |
| `file_url` | `string` | no | Public URL of the 3D model file. |
| `overhang_angle_deg` | `number` | no | Overhang angle threshold in degrees. Default: 45. |
| `thickness_min_mm` | `number` | no | Wall-thickness threshold in mm. Default: 0.5. |

Sample parameters:

```json
{
  "checks": [
    "solid"
  ],
  "distort_angle_deg": 5,
  "file_id": "example file id",
  "file_url": "https://example.com",
  "overhang_angle_deg": 10,
  "thickness_min_mm": 0.05
}
```

Generated JSON parameter schema:

```json
{
  "checks": {
    "description": "Subset of checks to run. Default: all six.",
    "items": {
      "enum": [
        "solid",
        "intersect",
        "degenerate",
        "distort",
        "thick",
        "overhang"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "distort_angle_deg": {
    "description": "Face-distortion angle threshold in degrees. Default: 45.",
    "maximum": 89,
    "minimum": 5,
    "required": false,
    "type": "number"
  },
  "file_id": {
    "description": "AgentPMT file storage ID.",
    "required": false,
    "type": "string"
  },
  "file_url": {
    "description": "Public URL of the 3D model file.",
    "required": false,
    "type": "string"
  },
  "overhang_angle_deg": {
    "description": "Overhang angle threshold in degrees. Default: 45.",
    "maximum": 89,
    "minimum": 10,
    "required": false,
    "type": "number"
  },
  "thickness_min_mm": {
    "description": "Wall-thickness threshold in mm. Default: 0.5.",
    "maximum": 10,
    "minimum": 0.05,
    "required": false,
    "type": "number"
  }
}
```

## `convert_format`

Action slug: `convert-format`

Price: `25` credits

Convert a 3D model between file formats. Runs synchronously through the queue; if the queue is full, returns 429 with error_code GPU_RENDER_QUEUE_FULL.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `apply_transforms` | `boolean` | no | Apply transforms before export. Default: true. |
| `file_id` | `string` | no | AgentPMT file storage ID for the source 3D model. |
| `file_url` | `string` | no | Public URL of the source 3D model. |
| `output_format` | `string` | yes | Target format. |

Sample parameters:

```json
{
  "apply_transforms": true,
  "file_id": "example file id",
  "file_url": "https://example.com",
  "output_format": "blend"
}
```

Generated JSON parameter schema:

```json
{
  "apply_transforms": {
    "description": "Apply transforms before export. Default: true.",
    "required": false,
    "type": "boolean"
  },
  "file_id": {
    "description": "AgentPMT file storage ID for the source 3D model.",
    "required": false,
    "type": "string"
  },
  "file_url": {
    "description": "Public URL of the source 3D model.",
    "required": false,
    "type": "string"
  },
  "output_format": {
    "description": "Target format.",
    "enum": [
      "blend",
      "glb",
      "fbx",
      "obj",
      "stl",
      "dae",
      "ply"
    ],
    "required": true,
    "type": "string"
  }
}
```

## `fix_printability`

Action slug: `fix-printability`

Price: `25` credits

Light-touch repair using Blender's object_print3d_utils clean operators. For mostly-clean inputs (CAD exports, few stray non-manifolds). Use voxel_remesh for structurally-broken inputs.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `auto_fix_distorted` | `boolean` | no | Run the addon's clean-distorted operator. Default: true. |
| `auto_fix_non_manifold` | `boolean` | no | Run the addon's clean-non-manifold operator. Default: true. |
| `checks` | `array` | no | Subset of checks to run. Default: all six. |
| `distort_angle_deg` | `number` | no | Face-distortion angle threshold in degrees. Default: 45. |
| `file_id` | `string` | no | AgentPMT file storage ID. |
| `file_url` | `string` | no | Public URL of the 3D model file. |
| `output_format` | `string` | yes | Target format for the cleaned export. |
| `overhang_angle_deg` | `number` | no | Overhang angle threshold in degrees. Default: 45. |
| `thickness_min_mm` | `number` | no | Wall-thickness threshold in mm. Default: 0.5. |

Sample parameters:

```json
{
  "auto_fix_distorted": true,
  "auto_fix_non_manifold": true,
  "checks": [
    "solid"
  ],
  "distort_angle_deg": 5,
  "file_id": "example file id",
  "file_url": "https://example.com",
  "output_format": "stl",
  "overhang_angle_deg": 10
}
```

Generated JSON parameter schema:

```json
{
  "auto_fix_distorted": {
    "description": "Run the addon's clean-distorted operator. Default: true.",
    "required": false,
    "type": "boolean"
  },
  "auto_fix_non_manifold": {
    "description": "Run the addon's clean-non-manifold operator. Default: true.",
    "required": false,
    "type": "boolean"
  },
  "checks": {
    "description": "Subset of checks to run. Default: all six.",
    "items": {
      "enum": [
        "solid",
        "intersect",
        "degenerate",
        "distort",
        "thick",
        "overhang"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "distort_angle_deg": {
    "description": "Face-distortion angle threshold in degrees. Default: 45.",
    "maximum": 89,
    "minimum": 5,
    "required": false,
    "type": "number"
  },
  "file_id": {
    "description": "AgentPMT file storage ID.",
    "required": false,
    "type": "string"
  },
  "file_url": {
    "description": "Public URL of the 3D model file.",
    "required": false,
    "type": "string"
  },
  "output_format": {
    "description": "Target format for the cleaned export.",
    "enum": [
      "stl",
      "glb",
      "obj",
      "ply"
    ],
    "required": true,
    "type": "string"
  },
  "overhang_angle_deg": {
    "description": "Overhang angle threshold in degrees. Default: 45.",
    "maximum": 89,
    "minimum": 10,
    "required": false,
    "type": "number"
  },
  "thickness_min_mm": {
    "description": "Wall-thickness threshold in mm. Default: 0.5.",
    "maximum": 10,
    "minimum": 0.05,
    "required": false,
    "type": "number"
  }
}
```

## `get_task`

Action slug: `get-task`

Price: `25` credits

Check the status of a render task and retrieve download links when complete. Non-terminal responses include queue_position (0 when running, 1+ when queued), queue_eta_seconds, and queue_stats {queue_total_running, queue_total_queued, queue_total_capacity}. Caller-driven failures (GPU_RENDER_QUEUE_FULL, BLENDER_VOXEL_GRID_TOO_LARGE, BLENDER_RUN_SCRIPT_TOO_LARGE, GPU_RENDER_TASK_CANCELED, BLENDER_SLICER_PROFILE_INVALID) report at warning severity and are safe to retry with corrected inputs; subprocess / memory / timeout failures (GPU_RENDER_BLENDER_NONZERO_EXIT, GPU_RENDER_BLENDER_TIMEOUT, BLENDER_SUBPROCESS_MEMORY_LIMIT, GPU_RENDER_CONTAINER_RESTARTED, GPU_RENDER_UNEXPECTED_ERROR) report at error severity — retry once but escalate if it recurs.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `task_id` | `string` | yes | Task ID returned from a render action. |

Sample parameters:

```json
{
  "task_id": "example task id"
}
```

Generated JSON parameter schema:

```json
{
  "task_id": {
    "description": "Task ID returned from a render action.",
    "required": true,
    "type": "string"
  }
}
```

## `list_tasks`

Action slug: `list-tasks`

Price: `25` credits

List render tasks for the current user, most recent first.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `limit` | `integer` | no | Maximum tasks to return (1-100). Default: 20. |

Sample parameters:

```json
{
  "limit": 1
}
```

Generated JSON parameter schema:

```json
{
  "limit": {
    "description": "Maximum tasks to return (1-100). Default: 20.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `render_custom`

Action slug: `render-custom`

Price: `25` credits

Render with a custom camera position. Returns a task_id immediately. Joins the strict-FIFO render queue.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `background_color` | `string` | no | Background hex color without #. |
| `camera_position` | `array` | no | Camera [x, y, z] position. Default: [3, -3, 2.5]. |
| `decimate_ratio` | `number` | no | Optional polygon-reduction ratio (0.05-1.0). |
| `file_id` | `string` | no | AgentPMT file storage ID. |
| `file_url` | `string` | no | Public URL of the 3D model file. |
| `fov` | `number` | no | Camera focal length in mm (10-120). Default: 50. |
| `lighting_preset` | `string` | no | Lighting style. |
| `look_at` | `array` | no | Camera look-at [x, y, z] target. Default: [0, 0, 0]. |
| `resolution` | `string` | no | Resolution preset or WxH. |
| `samples` | `integer` | no | Render samples. |

Sample parameters:

```json
{
  "background_color": "example background color",
  "camera_position": [
    1
  ],
  "decimate_ratio": 0.05,
  "file_id": "example file id",
  "file_url": "https://example.com",
  "fov": 10,
  "lighting_preset": "studio",
  "look_at": [
    1
  ]
}
```

Generated JSON parameter schema:

```json
{
  "background_color": {
    "description": "Background hex color without #.",
    "required": false,
    "type": "string"
  },
  "camera_position": {
    "description": "Camera [x, y, z] position. Default: [3, -3, 2.5].",
    "items": {
      "type": "number"
    },
    "required": false,
    "type": "array"
  },
  "decimate_ratio": {
    "description": "Optional polygon-reduction ratio (0.05-1.0).",
    "maximum": 1,
    "minimum": 0.05,
    "required": false,
    "type": "number"
  },
  "file_id": {
    "description": "AgentPMT file storage ID.",
    "required": false,
    "type": "string"
  },
  "file_url": {
    "description": "Public URL of the 3D model file.",
    "required": false,
    "type": "string"
  },
  "fov": {
    "description": "Camera focal length in mm (10-120). Default: 50.",
    "maximum": 120,
    "minimum": 10,
    "required": false,
    "type": "number"
  },
  "lighting_preset": {
    "description": "Lighting style.",
    "enum": [
      "studio",
      "product",
      "outdoor",
      "dramatic"
    ],
    "required": false,
    "type": "string"
  },
  "look_at": {
    "description": "Camera look-at [x, y, z] target. Default: [0, 0, 0].",
    "items": {
      "type": "number"
    },
    "required": false,
    "type": "array"
  },
  "resolution": {
    "description": "Resolution preset or WxH.",
    "required": false,
    "type": "string"
  },
  "samples": {
    "description": "Render samples.",
    "maximum": 512,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `render_turntable`

Action slug: `render-turntable`

Price: `25` credits

Generate a spinning turntable video of a 3D model. Returns a task_id immediately; use get_task to check progress and retrieve the output. Joins the strict-FIFO render queue (capacity 50); if the queue is full, returns a 429 with error_code GPU_RENDER_QUEUE_FULL and a Retry-After header.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `background_color` | `string` | no | Background hex color without #. Default: 1a1a1a. |
| `camera_distance` | `number` | no | Optional camera distance override. |
| `camera_lens_mm` | `number` | no | Camera focal length in mm (10-120). Default: 35. |
| `decimate_ratio` | `number` | no | Optional polygon-reduction ratio (0.05-1.0). |
| `duration_seconds` | `number` | no | Video duration in seconds (1-30). Default: 6. |
| `elevation` | `number` | no | Camera elevation degrees (-45 to 90). Default: 25. |
| `file_id` | `string` | no | AgentPMT file storage ID for the 3D model. |
| `file_url` | `string` | no | Public URL of the 3D model file (BLEND, GLB, GLTF, FBX, OBJ, STL, DAE, PLY). |
| `fit_margin` | `number` | no | Auto-framing padding multiplier (1-3). Default: 1.25. |
| `frames` | `integer` | no | Number of animation frames (12-120). Default: 72. |
| `lighting_preset` | `string` | no | Lighting style. |
| `resolution` | `string` | no | Resolution: 720p (default), 1080p, 2k, 4k, or WxH. |
| `samples` | `integer` | no | Render samples (1-512). Default: 8. |

Sample parameters:

```json
{
  "background_color": "example background color",
  "camera_distance": 0.1,
  "camera_lens_mm": 10,
  "decimate_ratio": 0.05,
  "duration_seconds": 1,
  "elevation": -45,
  "file_id": "example file id",
  "file_url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "background_color": {
    "description": "Background hex color without #. Default: 1a1a1a.",
    "required": false,
    "type": "string"
  },
  "camera_distance": {
    "description": "Optional camera distance override.",
    "maximum": 100,
    "minimum": 0.1,
    "required": false,
    "type": "number"
  },
  "camera_lens_mm": {
    "description": "Camera focal length in mm (10-120). Default: 35.",
    "maximum": 120,
    "minimum": 10,
    "required": false,
    "type": "number"
  },
  "decimate_ratio": {
    "description": "Optional polygon-reduction ratio (0.05-1.0).",
    "maximum": 1,
    "minimum": 0.05,
    "required": false,
    "type": "number"
  },
  "duration_seconds": {
    "description": "Video duration in seconds (1-30). Default: 6.",
    "maximum": 30,
    "minimum": 1,
    "required": false,
    "type": "number"
  },
  "elevation": {
    "description": "Camera elevation degrees (-45 to 90). Default: 25.",
    "maximum": 90,
    "minimum": -45,
    "required": false,
    "type": "number"
  },
  "file_id": {
    "description": "AgentPMT file storage ID for the 3D model.",
    "required": false,
    "type": "string"
  },
  "file_url": {
    "description": "Public URL of the 3D model file (BLEND, GLB, GLTF, FBX, OBJ, STL, DAE, PLY).",
    "required": false,
    "type": "string"
  },
  "fit_margin": {
    "description": "Auto-framing padding multiplier (1-3). Default: 1.25.",
    "maximum": 3,
    "minimum": 1,
    "required": false,
    "type": "number"
  },
  "frames": {
    "description": "Number of animation frames (12-120). Default: 72.",
    "maximum": 120,
    "minimum": 12,
    "required": false,
    "type": "integer"
  },
  "lighting_preset": {
    "description": "Lighting style.",
    "enum": [
      "studio",
      "product",
      "outdoor",
      "dramatic"
    ],
    "required": false,
    "type": "string"
  },
  "resolution": {
    "description": "Resolution: 720p (default), 1080p, 2k, 4k, or WxH.",
    "required": false,
    "type": "string"
  },
  "samples": {
    "description": "Render samples (1-512). Default: 8.",
    "maximum": 512,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `render_views`

Action slug: `render-views`

Price: `25` credits

Render preset camera angles. Returns a task_id immediately. Joins the strict-FIFO render queue.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `background_color` | `string` | no | Background hex color without #. Default: 1a1a1a. |
| `camera_distance` | `number` | no | Optional camera distance override. |
| `camera_lens_mm` | `number` | no | Camera focal length in mm (10-120). Default: 35. |
| `decimate_ratio` | `number` | no | Optional polygon-reduction ratio (0.05-1.0). |
| `file_id` | `string` | no | AgentPMT file storage ID. |
| `file_url` | `string` | no | Public URL of the 3D model file. |
| `fit_margin` | `number` | no | Auto-framing padding multiplier (1-3). Default: 1.25. |
| `lighting_preset` | `string` | no | Lighting style. |
| `resolution` | `string` | no | Resolution: 720p (default), 1080p, 2k, 4k, or WxH. |
| `samples` | `integer` | no | Render samples (1-512). Default: 8. |
| `views` | `array` | no | Views to render. Default: front, back, left, right, top, 3quarter. |

Sample parameters:

```json
{
  "background_color": "example background color",
  "camera_distance": 0.1,
  "camera_lens_mm": 10,
  "decimate_ratio": 0.05,
  "file_id": "example file id",
  "file_url": "https://example.com",
  "fit_margin": 1,
  "lighting_preset": "studio"
}
```

Generated JSON parameter schema:

```json
{
  "background_color": {
    "description": "Background hex color without #. Default: 1a1a1a.",
    "required": false,
    "type": "string"
  },
  "camera_distance": {
    "description": "Optional camera distance override.",
    "maximum": 100,
    "minimum": 0.1,
    "required": false,
    "type": "number"
  },
  "camera_lens_mm": {
    "description": "Camera focal length in mm (10-120). Default: 35.",
    "maximum": 120,
    "minimum": 10,
    "required": false,
    "type": "number"
  },
  "decimate_ratio": {
    "description": "Optional polygon-reduction ratio (0.05-1.0).",
    "maximum": 1,
    "minimum": 0.05,
    "required": false,
    "type": "number"
  },
  "file_id": {
    "description": "AgentPMT file storage ID.",
    "required": false,
    "type": "string"
  },
  "file_url": {
    "description": "Public URL of the 3D model file.",
    "required": false,
    "type": "string"
  },
  "fit_margin": {
    "description": "Auto-framing padding multiplier (1-3). Default: 1.25.",
    "maximum": 3,
    "minimum": 1,
    "required": false,
    "type": "number"
  },
  "lighting_preset": {
    "description": "Lighting style.",
    "enum": [
      "studio",
      "product",
      "outdoor",
      "dramatic"
    ],
    "required": false,
    "type": "string"
  },
  "resolution": {
    "description": "Resolution: 720p (default), 1080p, 2k, 4k, or WxH.",
    "required": false,
    "type": "string"
  },
  "samples": {
    "description": "Render samples (1-512). Default: 8.",
    "maximum": 512,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "views": {
    "description": "Views to render. Default: front, back, left, right, top, 3quarter.",
    "items": {
      "enum": [
        "front",
        "back",
        "left",
        "right",
        "top",
        "bottom",
        "3quarter"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  }
}
```

## `run_script`

Action slug: `run-script`

Price: `25` credits

Execute a custom Blender Python script. Returns a task_id immediately. Script payload limited to 65,536 bytes — oversize requests fail with error_code BLENDER_RUN_SCRIPT_TOO_LARGE.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | no | Optional AgentPMT file storage ID — exposed as MODEL_PATH. |
| `file_url` | `string` | no | Optional model URL — exposed as MODEL_PATH. |
| `output_type` | `string` | no | Expected output class. Default: image. |
| `script` | `string` | yes | Blender Python script (≤64 KiB). Has access to bpy, MODEL_PATH, OUTPUT_DIR. |
| `script_timeout_seconds` | `integer` | no | Override the per-subprocess timeout in seconds. |

Sample parameters:

```json
{
  "file_id": "example file id",
  "file_url": "https://example.com",
  "output_type": "image",
  "script": "example script",
  "script_timeout_seconds": 600
}
```

Generated JSON parameter schema:

```json
{
  "file_id": {
    "description": "Optional AgentPMT file storage ID — exposed as MODEL_PATH.",
    "required": false,
    "type": "string"
  },
  "file_url": {
    "description": "Optional model URL — exposed as MODEL_PATH.",
    "required": false,
    "type": "string"
  },
  "output_type": {
    "description": "Expected output class. Default: image.",
    "enum": [
      "image",
      "video",
      "model",
      "all"
    ],
    "required": false,
    "type": "string"
  },
  "script": {
    "description": "Blender Python script (≤64 KiB). Has access to bpy, MODEL_PATH, OUTPUT_DIR.",
    "required": true,
    "type": "string"
  },
  "script_timeout_seconds": {
    "description": "Override the per-subprocess timeout in seconds.",
    "maximum": 1800,
    "minimum": 600,
    "required": false,
    "type": "integer"
  }
}
```

## `slice_for_printing`

Action slug: `slice-for-printing`

Price: `25` credits

Slice a 3D model with PrusaSlicer and return G-code, parsed metadata, and a Blender-rendered printbed preview PNG. Returns a task_id immediately.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | no | AgentPMT file storage ID. |
| `file_url` | `string` | no | Public URL of the 3D model file. |
| `infill_density_pct` | `integer` | no | Override infill density percent (0-100). |
| `layer_height_mm` | `number` | no | Override the slicer's layer height in mm. |
| `printer_profile` | `string` | no | Bundled PrusaSlicer profile name. Default: prusa_mk4_pla_020. |
| `support_material` | `boolean` | no | Override the support-material toggle. |

Sample parameters:

```json
{
  "file_id": "example file id",
  "file_url": "https://example.com",
  "infill_density_pct": 0,
  "layer_height_mm": 0.05,
  "printer_profile": "example printer profile",
  "support_material": true
}
```

Generated JSON parameter schema:

```json
{
  "file_id": {
    "description": "AgentPMT file storage ID.",
    "required": false,
    "type": "string"
  },
  "file_url": {
    "description": "Public URL of the 3D model file.",
    "required": false,
    "type": "string"
  },
  "infill_density_pct": {
    "description": "Override infill density percent (0-100).",
    "maximum": 100,
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "layer_height_mm": {
    "description": "Override the slicer's layer height in mm.",
    "maximum": 0.6,
    "minimum": 0.05,
    "required": false,
    "type": "number"
  },
  "printer_profile": {
    "description": "Bundled PrusaSlicer profile name. Default: prusa_mk4_pla_020.",
    "pattern": "^[a-z0-9_]+$",
    "required": false,
    "type": "string"
  },
  "support_material": {
    "description": "Override the support-material toggle.",
    "required": false,
    "type": "boolean"
  }
}
```

## `voxel_remesh`

Action slug: `voxel-remesh`

Price: `25` credits

Rebuild a model into a watertight manifold via OpenVDB voxel remesh. The right tool for structurally-broken inputs. Output is guaranteed manifold; surface detail smaller than the voxel size is smoothed away. Pre-flight rejects requests whose grid cell count exceeds 5,000,000 with error_code BLENDER_VOXEL_GRID_TOO_LARGE — the response message includes the minimum-safe voxel_size for the input, and the report context exposes bbox_x/y/z, voxel_size, cells, max_cells, and min_safe_voxel_size for runbooks.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_id` | `string` | no | AgentPMT file storage ID. |
| `file_url` | `string` | no | Public URL of the 3D model file. |
| `output_format` | `string` | yes | Target format for the remeshed export. |
| `voxel_size` | `number` | no | Optional explicit voxel size in the same units as your model (typically mm). Smaller = finer detail and longer compute. Omit to auto-scale to ~1.3% of the longest bounding-box dimension. |

Sample parameters:

```json
{
  "file_id": "example file id",
  "file_url": "https://example.com",
  "output_format": "stl",
  "voxel_size": 0.01
}
```

Generated JSON parameter schema:

```json
{
  "file_id": {
    "description": "AgentPMT file storage ID.",
    "required": false,
    "type": "string"
  },
  "file_url": {
    "description": "Public URL of the 3D model file.",
    "required": false,
    "type": "string"
  },
  "output_format": {
    "description": "Target format for the remeshed export.",
    "enum": [
      "stl",
      "glb",
      "obj",
      "ply"
    ],
    "required": true,
    "type": "string"
  },
  "voxel_size": {
    "description": "Optional explicit voxel size in the same units as your model (typically mm). Smaller = finer detail and longer compute. Omit to auto-scale to ~1.3% of the longest bounding-box dimension.",
    "maximum": 100,
    "minimum": 0.01,
    "required": false,
    "type": "number"
  }
}
```
