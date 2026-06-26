---
name: blender-mcp
description: "Connect to and control Blender via the official Blender MCP Server. Covers 20+ built-in tools plus arbitrary bpy code execution. Compatible with Blender 5.1 and 5.2 LTS."
homepage: https://www.blender.org/lab/mcp-server/
author: taosiuman
version: 2.0.0
metadata:
  openclaw:
    requires:
      bins: ["blender", "mcporter"]
    install:
      - id: mcporter
        kind: node
        package: mcporter
        bins: ["mcporter"]
        label: "Install mcporter (npm)"
---

# Blender MCP Server Connection Skill

Connect to and control a running Blender instance via the official Blender MCP Server.

**Version support**: Blender 5.1+ and 5.2 LTS Beta (API compatibility notes included below)

---

## Architecture Overview

```
┌─────────────┐     TCP Socket      ┌──────────────────     MCP Protocol     ┌──────────────
│  LLM Client │ ◄─────────────────► │  MCP Server      │ ◄──────────────────► │   Blender    │
│  (OpenClaw) │    stdio / HTTP     │  (Python process) │    port 9876         │   (Addon)    │
└─────────────┘                     └──────────────────┘                      └──────────────
```

**Two-component architecture**:
1. **Blender Addon** — runs inside Blender, provides a TCP Socket Server (default `localhost:9876`)
2. **MCP Server** — standalone Python process that bridges the LLM client and the Blender Addon

---

## Installation

### 1. Install the Blender Addon

**Option A: From ZIP**
1. Download addon ZIP: `https://projects.blender.org/lab/blender_mcp/releases/download/v1.0.0/mcp-1.0.0.zip`
2. Blender → Edit → Preferences → Add-ons → Install from Disk
3. Enable the "Blender MCP" addon
4. Confirm Host/Port in addon settings (default `localhost:9876`)

**Option B: Drag & Drop**
- Drag the ZIP file into the Blender window (twice: first to add the Blender Lab repository, second to install the addon)

**Option C: From Source**
- Source code locations: `mcp/blmcp/` and `addon/blender_mcp_addon/`

### 2. Start the Blender MCP Server

```bash
# Install dependencies
cd path/to/blender_mcp
pip install mcp pyyaml starlette

# Start MCP Server (stdio mode)
python -m blmcp --transport stdio

# Or HTTP mode (default 127.0.0.1:8000)
python -m blmcp --transport http --host 127.0.0.1 --port 8000
```

### 3. Configure mcporter

```bash
# Add Blender MCP Server config
mcporter config add blender-mcp --transport stdio --command "python -m blmcp --transport stdio"

# Or use HTTP mode
mcporter config add blender-mcp --transport http --url "http://127.0.0.1:8000"

# Verify connection
mcporter list blender-mcp --schema
```

---

## Usage

### Method 1: Via mcporter (recommended)

```bash
# List all available tools
mcporter list blender-mcp --schema

# Call a specific tool
mcporter call blender-mcp.execute_blender_code code='import bpy; result = {"objects": [o.name for o in bpy.data.objects]}'

mcporter call blender-mcp.get_objects_summary
mcporter call blender-mcp.get_object_detail_summary object_name="Cube"

# Search API docs
mcporter call blender-mcp.search_api_docs query="bpy.ops.object.delete"

# Search user manual
mcporter call blender-mcp.search_manual_docs query="Geometry Nodes"

# Screenshot
mcporter call blender-mcp.get_screenshot_of_window_as_image

# Render viewport
mcporter call blender-mcp.render_viewport_to_path output_path="C:\\render.png"
```

### Method 2: Direct TCP Socket to Blender Addon (lightweight)

⚠️ **Warning**: This mode sends caller-supplied code directly to Blender with no guardrails. Review code before execution.

```python
import socket
import json

def send_to_blender(code: str, host="localhost", port=9876, timeout=30.0) -> dict:
    """Send Python code directly to Blender Addon for execution."""
    request = json.dumps({
        "type": "execute",
        "code": code,
        "strict_json": False,
    }) + "\0"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.sendall(request.encode("utf-8"))

        buf = bytearray()
        while True:
            chunk = sock.recv(65536)
            if not chunk:
                break
            buf.extend(chunk)
            if b"\0" in buf:
                break

    line, _, _ = buf.partition(b"\0")
    return json.loads(line.decode("utf-8"))

# Example: get all object names in the scene
response = send_to_blender(
    'import bpy\nresult = {"objects": [o.name for o in bpy.data.objects]}'
)
print(response)
# {"status": "ok", "result": {"objects": ["Cube", "Camera", "Light"]}}
```

### Method 3: Blender Background Mode (headless rendering / batch)

```bash
# Start Blender background MCP Server
blender --background myscene.blend --command blender_mcp --host localhost --port 9876

# Or execute code via CLI
blender --background myscene.blend --python-expr "
import bpy
# your code
result = {'count': len(bpy.data.objects)}
print('__BLMCP_RESULT__' + str(result))
"
```

---

## Built-in Tools (20 total)

### Core
| Tool | Description | Params |
|------|-------------|--------|
| `execute_blender_code` | Execute arbitrary Python code (full bpy access) | `code: str` |
| `execute_blender_code_for_cli` | Execute code in a background Blender process | `blend_file: str, code: str` |

### Scene Analysis
| Tool | Description | Params |
|------|-------------|--------|
| `get_objects_summary` | Get scene object hierarchy and basic info | none |
| `get_object_detail_summary` | Get detailed info for a specific object | `object_name: str` |
| `get_blendfile_summary_datablocks` | Analyze .blend file data-blocks | `blend_file: str` |
| `get_blendfile_summary_missing_files` | Check for missing external file references | `blend_file: str` |
| `get_blendfile_summary_of_linked_libraries` | List linked external libraries | `blend_file: str` |
| `get_blendfile_summary_path_info` | Analyze .blend file path information | `blend_file: str` |
| `get_blendfile_summary_usage_guess` | Guess the purpose of a .blend file | `blend_file: str` |

### Screenshots & Rendering
| Tool | Description | Params |
|------|-------------|--------|
| `get_screenshot_of_window_as_image` | Capture Blender window screenshot | none |
| `get_screenshot_of_area_as_image` | Capture specific area screenshot | `area_type: str` |
| `get_screenshot_of_window_as_json` | Get window layout as JSON description | none |
| `render_viewport_to_path` | Render viewport to file | `output_path: str` |
| `render_thumbnail_to_path` | Render thumbnail to file | `output_path: str` |

### Navigation
| Tool | Description | Params |
|------|-------------|--------|
| `jump_to_tab_by_name` | Jump to a named editor tab | `tab_name: str` |
| `jump_to_tab_by_space_type` | Jump to a space type | `space_type: str` |
| `jump_to_view3d_object_by_name` | Focus on an object in 3D View | `object_name: str` |
| `jump_to_view3d_object_data_by_name` | Focus on object data in 3D View | `data_name: str` |

### Documentation Search
| Tool | Description | Params |
|------|-------------|--------|
| `search_api_docs` | Search Blender Python API docs | `query: str` |
| `search_manual_docs` | Search Blender user manual | `query: str` |
| `get_python_api_docs` | Get Python API docs | `query: str` |

---

## Communication Protocol

### TCP Socket Protocol

**Request format** (null-byte delimited JSON):
```json
{"type": "execute", "code": "import bpy\nresult = {'key': 'value'}", "strict_json": false}\0
```

**Response format**:
```json
// Success
{"status": "ok", "result": {"key": "value"}, "stdout": "", "stderr": ""}\0

// Error
{"status": "error", "message": "Traceback...", "stdout": "", "stderr": ""}\0
```

### Code Execution Conventions

- Assign return value to the `result` variable (must be a dict)
- `strict_json=True`: strict JSON serialization; non-serializable values will error
- `strict_json=False`: uses `repr()` as fallback for non-JSON values
- Supports deferred responses: return a `check_is_finished` callable for long-running tasks

### Example: Get Object Info

```python
import bpy
obj = bpy.data.objects.get("Cube")
if obj:
    result = {
        "name": obj.name,
        "type": obj.type,
        "location": list(obj.location),
        "vertices": len(obj.data.vertices) if obj.type == "MESH" else 0,
    }
else:
    result = {"error": "Object not found"}
```

### Example: Create an Object

```python
import bpy
bpy.ops.mesh.primitive_torus_add(
    align='WORLD',
    location=(0, 0, 0),
    major_radius=1.0,
    minor_radius=0.3,
)
result = {"status": "created", "name": bpy.context.active_object.name}
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BLENDER_MCP_HOST` | `localhost` | Blender Addon host address |
| `BLENDER_MCP_PORT` | `9876` | Blender Addon port |
| `BLENDER_PATH` | `blender` | Path to Blender executable |

---

## Security Notes

⚠️ **Official security warning**: The MCP Server executes LLM-generated code with **no sandboxing**.

**Built-in weak sandbox** (`WeakSandboxForLLM`):
- Blocks `sys.exit()` calls
- Blocks dangerous operators: `wm.quit_blender`, `wm.read_factory_settings`, `wm.read_factory_userpref`, `wm.read_userpref`

### Security Best Practices

1. **Keep server local only** — Always use `localhost` / `127.0.0.1`; never bind to `0.0.0.0`
2. **Review code before execution** — Prefer scoped built-in tools over raw `execute_blender_code`
3. **Protect your projects** — Keep backups of important `.blend` files
4. **Verify external dependencies** — Download addon only from official Blender Lab sources

---

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `ConnectionRefusedError` | Blender not running or Addon not started | Start Blender, enable MCP Addon, click "Start Server" |
| `ConnectionError: Empty response` | Network timeout or Addon crashed | Check Blender console output, verify port |
| `result is not JSON-serializable` | Returned a Blender object | Use `strict_json=False` or manually convert to dict |
| `Blender executable not found` | Blender command not found | Set `BLENDER_PATH` environment variable |
| `Deferred responses not supported` | Background mode doesn't support deferred responses | Use synchronous code or switch to GUI mode |

---

## Blender 5.1 API Compatibility Notes

### Action Layered Structure (Breaking Change)

In Blender 5.1, `Action.fcurves` was removed. The new layered animation system uses:

```python
# ❌ Old (5.0 and earlier)
fcurves = action.fcurves

# ✅ Blender 5.1+
fcurves = action.layers[0].strips[0].channelbags[0].fcurves
```

### Brush API: `use_*` → `stroke_method` Enum

```python
# ❌ Old (5.0)
brush.use_airbrush = True

# ✅ 5.1+
brush.stroke_method = 'AIRBRUSH'  # Options: AIRBRUSH, SPACE, ANCHORED, LINE, CURVE, DRAG_DOT
```

### VSE Time Property Renames

| Old (5.0) | New (5.1) |
|-----------|-----------|
| `frame_final_duration` | `duration` |
| `frame_final_start` | `left_handle` |
| `frame_final_end` | `right_handle` |
| `frame_duration` | `content_duration` |

### Principled BSDF Input Renames

| Old (5.0) | New (5.1) |
|-----------|-----------|
| `inputs['Transmission']` | `inputs['Transmission Weight']` |
| `inputs['Emission']` | `inputs['Emission Color']` + `inputs['Emission Strength']` |

### Other 5.1 Changes
- `sculpt.sample_color` → `paint.sample_color`
- `bpy.app.cachedir` — new standard cache directory
- `bpy.app.handlers.exit_pre` — new exit handler
- Python 3.13 runtime

---

## Blender 5.2 LTS Compatibility Notes (Beta)

> Blender 5.2 LTS entered Beta on 2026-06-03. API is frozen; RC expected 2026-07-08, release 2026-07-14.

### 🔴 Breaking Changes (12 total — all Beta confirmed)

#### 1. Geometry Nodes Modifier API Rewrite

```python
# ❌ 5.1 and earlier
modifier["SocketName"] = 5.0
modifier["SocketName_use_attribute"] = True
modifier["SocketName_attribute_name"] = "some_input"

# ✅ 5.2+
modifier.properties.inputs.SocketName.value = 5.0
modifier.properties.inputs.SocketName.type = "ATTRIBUTE"
modifier.properties.inputs.SocketName.attribute_name = "some_input"
modifier.properties.outputs.SocketName.attribute_name = "some_output"

# ✅ Compatible pattern
import bpy
if bpy.app.version >= (5, 2, 0):
    val = modifier.properties.inputs.SocketName.value
else:
    val = modifier["SocketName"]
```

#### 2. Principled BSDF Node Renamed
- `Transmission` → `Transmission Weight`
- Already applies from 5.1; ensure plugin references match

#### 3. `paint.eraser_brush` API Removed
- No longer needs manual setting; last eraser brush auto-activates

#### 4. Automasking → MeshAutomaskingSettings (17 properties migrated)

```python
# ❌ Old
brush.use_automasking_topology = True
brush.automasking_cavity_factor = 0.5

# ✅ 5.2+
brush.mesh_automasking_settings.use_automasking_topology = True
brush.mesh_automasking_settings.cavity_factor = 0.5
```

All 17 properties: `use_automasking_topology`, `use_automasking_face_sets`, `use_automasking_boundary_edges`, `use_automasking_boundary_face_sets`, `use_automasking_cavity`, `use_automasking_cavity_inverted`, `use_automasking_start_normal`, `use_automasking_view_normal`, `automasking_boundary_edges_propagation_steps`, `automasking_cavity_factor`, `automasking_cavity_blur_steps`, `automasking_cavity_curve`, `automasking_cavity_curve_op`, `automasking_start_normal_limit`, `automasking_start_normal_falloff`, `automasking_view_normal_limit`, `automasking_view_normal_falloff`

#### 5. VSE `strip.use_linear_modifiers` Removed
#### 6. VSE `timecode files` Feature Removed
#### 7. `UILayout.template_palette` `color` Parameter Removed
#### 8. Compare / Random Value Node Socket Identifiers Changed
#### 9. Asset Library Index Shift — "All Libraries" and "Essentials" now occupy first two indices
#### 10. Evaluated Meshes Naming Change — Geo Nodes created meshes no longer share object's original mesh name
#### 11. Brush `use_*` → `stroke_method` (see 5.1 section above)
#### 12. VSE Time Property Renames (see 5.1 section above)

---

### 🟢 High-Value New APIs (5.2 LTS)

#### Python API
| API | Description |
|-----|-------------|
| `bpy.data.all_ids` | Single iterator over ALL data-blocks |
| `WindowManager.reports` | Read-only reports list with session-wide unique uid |
| `bpy.data.libraries.load()` input | Now exposes nested library paths |
| `Window.screenshot()` | Get window pixel data without saving to file |
| `gpu.init()` | Initialize GPU backend in `--background` mode |
| `mathutils` slice step | `vector[begin:end:step]` for Vector/Matrix/Color/Euler |
| Blender Arrays slice step | `image.pixels[begin:end:step]` — e.g., `pixels[3::4]` for alpha channel |
| `path_foreach` options | EXPAND_TOKENS, EXPAND_SEQUENCES, EXPAND_CACHES |
| Annotations API | `frame.strokes.new()`, `stroke.points.add(count, pressure, strength)`, `stroke.points.remove(index)`, `frame.strokes.remove(stroke)` |
| `UILayout.link` / `textbox` | Styled link buttons and multi-line text buttons |
| `imbuf` extended | Pixel-level image access, format conversion, buffer protocol |
| Node panel collapse | Programmatically open/close node panels from Python |
| Node Tool input values | Set Node Tool parameters programmatically in 5.2 |

#### Geometry Nodes
| Node / Feature | Description |
|----------------|-------------|
| **Physics (experimental)** | XPBD Solver, Cloth Dynamics modifier, Hair Dynamics, Effector system |
| **Mesh Bevel** | Long-awaited procedural bevel node |
| **Geometry Bundles** | Set/Get Geometry Bundle — attach arbitrary data (fields, closures) to geometry |
| **Lists data type** | New core type alongside single/field/grid — Length, Get, Filter, Sort |
| **Sample Sound Frequencies** | Audio-driven animation without keyframe baking |
| **PCA** | Principal Component Analysis for auto-alignment |
| **Transfer Attributes** | Transfer attributes between two geometries |
| **3D ↔ Screen Space** | Bundled transform nodes (3D to Screen, Screen to 3D, Project with Depth) |
| **Collection Children** | Recursive access to collection children as lists |
| **Empty Objects** | Geo Nodes modifiers on Empty objects |
| **Capture Attribute Selection** | Selection input for efficiency |
| **NURBS Order/Weight** | Set NURBS Order and Weight nodes |
| **Scene Frame default input** | Float/int sockets default to current frame |
| **Self-object default** | Object sockets can default to self-object |
| **Merge by Distance split** | Now: Merge Points + Cluster by Distance + Cluster by Connected |

#### Cycles
| Feature | Description |
|---------|-------------|
| **Texture Cache** | `.tx` files reduce memory 34-77% in texture-heavy scenes. Enable: Performance > Texture Cache + Auto Generate. CLI: `blender scene.blend --command maketx` |
| **Raycast Attributes** | Access attributes at intersection point (Cycles only) |
| **SSS Negative Anisotropy** | Principled/Subsurface BSDF: -1 to 1 range |
| **World Cast Shadows** | World can now cast shadows |
| **OSL GPU** | Texture cache improves OSL performance + adds GPU support |
| **Simplify Texture Resolution** | Percentage-based texture scaling (50%, 25%) |

#### EEVEE
| Feature | Description |
|---------|-------------|
| **Shader Raycast** | Screen-space raytracing node |
| **Light Path Intensity** | Global indirect light intensity control |
| **Texture pool -40%** | Vulkan: 406MB → 245MB |

#### Grease Pencil
| Feature | Description |
|---------|-------------|
| **Fill Tool Delaunay** | New Delaunay solver: precise geometry, auto gap detection, scale-independent, faster |
| **Draw Tool curves** | Bézier / Catmull-Rom / NURBS curve types |
| **Line Materials placement** | Count / Density / Radius modes with randomization |
| **`layer.layer_masks` API** | Add/remove layer masks via Python |

#### Video Sequencer
| Feature | Description |
|---------|-------------|
| **Compositor Effect Strip** | Use compositor node trees for VSE transitions/effects (0/1/2 inputs + fader) |
| **Compositor GPU acceleration** | In VSE modifiers |
| **`strip.connections`** | API to find connected strips |

#### Sculpt
| Feature | Description |
|---------|-------------|
| **Scene Project brush** | Displace vertices toward other objects (like Shrinkwrap) |
| **Add Primitive in Sculpt Mode** | Cube/Cone/Cylinder directly in sculpt |
| **Color Filter unified color** | Uses scene unified colors; Ctrl-X quick fill |
| **Dyntopo confirmation removed** | No more confirmation dialog when switching back to Sculpt |
| **Voxel Remesher attribute interpolation** | Smooth vertex/corner attribute interpolation |

#### Assets
| Feature | Description |
|---------|-------------|
| **Online Asset Library** | Browse and download from remote hosted libraries |
| **Asset Library index shift** | "All Libraries" and "Essentials" now at indices 0 and 1 |

#### Other
| Feature | Description |
|---------|-------------|
| **LoopTools built-in** | Circle/Space/Flatten now native — no addon needed |
| **Hydra 2.0 API** | OpenUSD provides abstraction layer |
| **Animation +125%** | Action evaluation 32.8→74.1 fps (4 threads) |
| **Gaussian Smooth F-Curve** | Non-destructive curve smoothing modifier |

---

## OpenClaw Integration

### Configure openclaw.json

```json
{
  "plugins": {
    "entries": {
      "mcp": {
        "servers": {
          "blender-mcp": {
            "command": "python",
            "args": ["-m", "blmcp", "--transport", "stdio"],
            "cwd": "path/to/blender_mcp",
            "env": {
              "BLENDER_MCP_HOST": "localhost",
              "BLENDER_MCP_PORT": "9876"
            }
          }
        }
      }
    }
  }
}
```

### Via mcporter CLI

```bash
# List tools
mcporter call blender-mcp.get_objects_summary

# Execute code
mcporter call blender-mcp.execute_blender_code code='import bpy; result = {"count": len(bpy.data.objects)}'
```

---

## Quick Start Checklist

- [ ] Blender 5.1+ installed
- [ ] MCP Addon installed and enabled
- [ ] MCP Server started (`python -m blmcp --transport stdio`)
- [ ] mcporter installed (`npm install -g mcporter`)
- [ ] Port 9876 available (default)
- [ ] `BLENDER_PATH` environment variable set (if needed)
