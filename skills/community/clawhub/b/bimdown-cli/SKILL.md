---
name: bimdown
version: 1.4.1
description: A bridge between AI and building data. Read & create BIM exactly like writing code. Execute architectural design, or just model your own house!
metadata:
  {
    "openclaw": {
      "emoji": "🏛️",
      "requires": {
        "bins": ["bimdown"],
        "install": { "npm": "bimdown-cli" }
      },
      "optionalEnv": ["BIMCLAW_API"],
      "network": {
        "publish": {
          "endpoint": "https://bim-claw.com/api/shares/publish",
          "method": "POST",
          "description": "Optional sharing step. Uploads project CSV/SVG/GLB files as a zip to BimClaw and returns a public share URL. Anonymous (no account or token required). The agent MUST ask the user for explicit permission before the first publish of any given project.",
          "override": "Set BIMCLAW_API to point at a different backend (self-hosted)."
        }
      }
    }
  }
---

# BimDown Agent Skill & Schema Rules

> **Your Mission:** A bridge between AI agents and building data. Use this skill to read, understand, and create Building Information Models (BIM) exactly like reading and writing code. It enables you to execute architectural design, model from drawings, perform quantity surveying, and conduct model reviews. Of course, just modeling your own house is also very interesting and fully supported.


## Setup / Prerequisites

This skill **REQUIRES** the `bimdown` binary (provided by the `bimdown-cli` npm package). All workflow steps below invoke it directly — without it, the skill cannot function.

1. **Check first**: Run `which bimdown` (or `bimdown --version`). If it exists, skip the install step.
2. **If missing**: Install via npm — but you **MUST explicitly ask the user for permission** before running `npm install -g` autonomously. This writes to global npm paths and executes arbitrary package scripts, so it is a privileged action.

```bash
npm install -g bimdown-cli
```

The CLI is fully offline except for the optional `bimdown publish` step (see the Publishing section below for details on what that uploads and where).

You are an AI Coder operating within a BimDown project environment.
BimDown is an open-source, AI-native building data format using CSV for semantics and SVG for geometry.

## Core Architecture & Base Concepts

- **Global Unit is METERS**: All coordinates, widths, and structural attributes in CSV/SVG MUST strictly use METERS. BimDown simulates real-world dimensions.
- **Computed Fields are READ-ONLY**: Any field marked with `computed: true` (or listed in `virtual_fields`) is automatically calculated by the CLI. **DO NOT** write these fields to CSV files. You can retrieve their values using `bimdown query`.
- **Dual Nature**: Properties live in `{name}.csv`. 2D geometry lives in a sibling `{name}.svg` file. The `id` fields across both must match perfectly.
- **SVG-derived virtual columns**: When you write geometry in SVG, the CLI automatically computes these fields for `bimdown query` — do NOT write them to CSV:
  - Line elements (wall, beam, pipe, etc.): `length`, `start_x`, `start_y`, `end_x`, `end_y`
  - Polygon elements (slab, roof, etc.): `area`, `perimeter`
  - All elements: `level_id` (inferred from folder name, e.g. `lv-1/` → `lv-1`)
- **Concrete Example of CSV+SVG Linked State**:
  > `lv-1/wall.csv` (note: NO `level_id` column — it is auto-inferred):
  > `id,thickness,material`
  > `w-1,0.2,concrete`
  >
  > `lv-1/wall.svg`:
  > `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -10 10 10"> <g transform="scale(1,-1)"> <path id="w-1" d="M 0 0 L 10 0" stroke-width="0.2" /> </g> </svg>`
  >
  > After this, `bimdown query . "SELECT id, length, level_id FROM wall"` returns `w-1, 10.0, lv-1` — both `length` and `level_id` are computed automatically.

## Project Directory Structure

```
project/
  project_metadata.json        # project root marker (format version, name, units)
  global/                      # global-only files — MUST be here, NOT in lv-N/
    grid.csv
    level.csv
    mesh.csv
  lv-1/                        # per-level files
    wall.csv + wall.svg        # elements with geometry have paired CSV+SVG
    door.csv                   # hosted elements are CSV-only (parametric position on host wall)
    space.csv                  # spaces: CSV seed point + space.svg boundary (computed by build)
    ...
  lv-2/
    ...
```

**Key rules**:
- `level.csv`, `grid.csv`, `mesh.csv` MUST live in `global/`, never in `lv-N/` directories
- Per-level elements (wall, door, slab, space, etc.) go in `lv-N/` directories
- The folder name (e.g. `lv-1`) becomes the element's `level_id` — do NOT write `level_id` to CSV

## Recommended Workflow for Creating/Modifying Buildings

1. **Plan spatial layout first**: Before writing any files, reason through the spatial relationships — wall positions, room adjacencies, door/window placements. Sketch coordinates mentally or on paper.
2. **Write SVG geometry first**: Create the `.svg` files (walls, slabs, columns) with correct coordinates. Geometry determines everything else.
3. **Write CSV attributes second**: Create the `.csv` files with element properties (material, thickness, etc.). Remember: do NOT include computed fields like `level_id`, `length`, `area`.
4. **Render and visually verify**: Run `bimdown render <dir> -o render.png` and **view the PNG image** to confirm the layout is correct. Check that walls connect properly, rooms are enclosed, and doors/windows are in the right positions. **Save render outputs and any other non-BimDown files OUTSIDE the project directory** — the project directory must only contain BimDown CSV/SVG files, otherwise `build` will reject them.
5. **Build**: Run `bimdown build <dir>` to validate schema, check geometry, and compute space boundaries (generates `space.svg` from seed points).
6. **Iterate**: If the render or build shows problems, fix the SVG geometry and re-render until the layout looks right.
7. **Publish** (optional, network step): Run `bimdown publish <dir>` to upload the project to BimClaw and get a shareable 3D preview URL. See the **Publishing & Data Upload** section below for what is uploaded, where, and the consent requirement.

## Reference SOPs

**STOP — before writing a single file, you MUST read the matching reference SOP below.** These are not optional background material; they are the authoritative step-by-step procedures for the task.

- **If you need to DESIGN a building** (any request that starts from a brief, requirements, program, or "design me a ..."): **YOU MUST READ** [`references/building-design.md`](./references/building-design.md) — the full design-to-BIM workflow from massing through MEP.
- **If you need to MODEL from existing plans** (floor plan images, sketches, known dimensions, or an existing building to replicate): **YOU MUST READ** [`references/bim-modeling.md`](./references/bim-modeling.md) — element creation order, dependencies, and best practices.

Do not guess the workflow from memory. Do not start writing CSV/SVG before the relevant SOP has been read in full.

## CLI Tools & Best Practices

1. **`bimdown query <dir> <sql> --json`**: Runs DuckDB SQL across all tables, including SVG-derived virtual columns.
   - **Example**: `bimdown query ./proj "SELECT id, length FROM wall WHERE length > 5.0" --json`
2. **`bimdown render <dir> [-l level] [-o output.png] [-w width]`**: Renders a level into a PNG blueprint image (default 2048px wide). Use `.svg` extension for SVG output. **Always render after modifying geometry and view the PNG to visually verify the result.**
   - **Color legend** (memorize this so you can interpret your own renders):
     - **Walls**: dark navy `#1a1a2e` (structural walls are slate `#4a4e69`)
     - **Columns**: dark solid fill (structural columns slightly lighter)
     - **Slabs**: light grey translucent
     - **Spaces / rooms**: blue translucent with room name label
     - **Stairs**: orange
     - **Beams**: purple
     - **DOORS**: **bold red `#e63946`** lines cutting across the host wall — clearly visible
     - **WINDOWS**: **bold teal `#2a9d8f`** lines cutting across the host wall — clearly visible
     - **MEP** — ducts: cyan, pipes: light blue, cable tray: green, conduit: teal, equipment: red fill, terminals: orange fill
   - If a door or window is missing from the render, it usually means its `host_id` or `position` is wrong — check the CSV before blaming the renderer.
3. **`bimdown build <dir>`**: Validates the project, checks geometry (wall connectivity, hosted element bounds), and computes space boundaries (generates `space.svg`). **Run this EVERY TIME after modifying CSV or SVG files!** Also available as `bimdown validate` (alias).
4. **`bimdown schema [table]`**: Prints the full schema for any element type. Use this to look up fields before creating elements.
5. **`bimdown diff <dirA> <dirB>`**: Emits a `+`, `-`, `~` structural difference between project snapshots.
6. **`bimdown init <dir>`**: Creates a new empty BimDown project with the correct directory structure.
7. **`bimdown publish <dir> [--expires 7d] [--api <url>]`**: Publishes the project to BimClaw (default endpoint `https://bim-claw.com/api/shares/publish`) and returns a shareable 3D preview URL. Anonymous — no account or token is required. See the **Publishing & Data Upload** section below for the full security contract before running this.
8. **`bimdown info <dir>`**: Prints project summary (levels, element counts).
9. **`bimdown resolve-topology <dir>`**: Auto-detects coincident endpoints for MEP curves, generates `mep_nodes`, and fills connectivity fields.
10. **`bimdown merge <dirs...> -o <output>`**: Merges multiple project directories into one, resolving ID conflicts.
11. **`bimdown sync <dir>`**: Hydrates into DuckDB and dehydrates back out to CSV/SVG, applying computed defaults.
12. **Downloading a shared project**: If the user provides a share link like `https://bim-claw.com/s/<token>`, append `/download` to get the zip: `curl -L https://bim-claw.com/s/<token>/download -o project.zip && unzip project.zip -d project/`

## Publishing & Data Upload

`bimdown publish` is the **only** network-using command in this skill. Everything else runs fully offline on local files. Before running it, be explicit with the user about the following:

- **Destination**: `https://bim-claw.com/api/shares/publish` by default. Override with `--api <url>` or the `BIMCLAW_API` environment variable to point at a self-hosted backend.
- **What is uploaded**: the entire project directory, zipped — every CSV, every SVG, any `mesh/*.glb` files, and `project_metadata.json`. Filenames, geometry, room names, and any materials/notes you put in CSV columns all leave the device.
- **Authentication**: **none**. The upload is anonymous; no account, API key, or token is used or stored. The server returns a random share token (e.g. `https://bim-claw.com/s/abc123`). Anyone with that link can view and download the project until it expires (default 7 days, configurable via `--expires`).
- **Consent requirement** (HARD RULE): Before the **first** publish of any given project in a session, **you MUST ask the user for explicit permission** and wait for their confirmation. Do not publish autonomously. Once confirmed for that project, further re-publishes within the same conversation are fine.
- **Sensitivity check**: If the project contains anything the user might consider confidential — client names, specific addresses, unpublished designs, stamped construction docs — call this out in the consent question so the user can make an informed decision.

## Critical File & Geometry Rules

- **ID format**:
  - **Grid and Level** allow any string after prefix: level: `lv-` + any string (e.g. `lv-1`, `lv-A`, `lv-B2`); grid: `gr-` + any string (e.g. `gr-1`, `gr-A`, `gr-B2`)
  - **All other elements** use `{prefix}-{number}` (digits only): wall → `w-{n}`, column → `c-{n}`, slab → `sl-{n}`, space → `sp-{n}`, door → `d-{n}`, window → `wn-{n}`, ...
  - **Always run `bimdown build` to confirm your IDs are compliant.**
- **SVG Coordinate Y-Flip**: All geometry inside `.svg` files **MUST** be wrapped in a Y-axis flip group: `<g transform="scale(1,-1)"> ... </g>`. This is just a fixed boilerplate — you do NOT need to do any coordinate conversion. Use normal Cartesian coordinates (X = right, Y = up) directly inside the group.
- **CSV vs Computed Fields**: Only write fields that are NOT marked as computed. Specifically, `level_id`, `length`, `area`, `start_x/y`, `end_x/y`, `perimeter`, `volume`, `bbox_*` are all auto-computed — never write them to CSV.
- **Vertical positioning** (walls, columns, and other vertical elements):
  - `level_id`: auto-inferred from folder name — do NOT write to CSV
  - `base_offset`: vertical offset in meters from the element's level. Default 0. Usually leave empty.
  - `top_level_id`: the level where the element's top is constrained. **Leave empty** to default to the next level above. Only set this if the element spans to a non-adjacent level.
  - `top_offset`: vertical offset in meters from the top level. Default 0. Usually leave empty.
  - `height`: auto-computed from level elevations and offsets — do NOT write to CSV.
  - **For most single-story walls**: leave `top_level_id`, `top_offset`, and `base_offset` all empty — the CLI will compute the correct height from level elevations.

## Generation Tips

### Typical Values (meters)
| Element | Field | Typical Range |
|---------|-------|--------------|
| Wall (partition) | thickness | 0.1 – 0.15 |
| Wall (exterior) | thickness | 0.2 – 0.3 |
| Wall (structural) | thickness | 0.3 – 0.6 |
| Door (single) | width × height | 0.9 × 2.1 |
| Door (double) | width × height | 1.8 × 2.1 |
| Window | width × height | 1.2–1.8 × 1.5 |
| Window | base_offset (sill height) | 0.9 (standard), 0.0 (floor-to-ceiling) |
| Column | size_x × size_y | 0.3–0.6 × 0.3–0.6 |
| Slab | thickness | 0.15 – 0.25 |
| Level spacing | elevation diff | 3.0 – 4.0 |

### Room Boundary Connectivity
Rooms are enclosed by **walls, curtain walls, columns, and room separators**. For the boundary to close properly:
- Line element endpoints (walls, curtain walls, room separators) must meet exactly at shared coordinates
- Example: w-1 ends at (10,0) → w-2 must start at (10,0) for an L-junction
- The CLI `build` command warns about unconnected endpoints and computes space boundaries from closed loops

### Door/Window Placement Rules

**Recommended: use `host_x, host_y`** instead of `position`. Just write the 2D coordinate of the opening center — `bimdown build` will auto-resolve the nearest wall and compute `position` for you.

```csv
id,host_x,host_y,width,height,operation,material
d-1,5.0,3.0,0.9,2.1,single,wood
```

After `bimdown build`, the CSV is rewritten with `host_id` and `position` replacing `host_x/host_y`. You can also provide `host_id` alongside `host_x/host_y` to force a specific wall.

**Alternative: manual `position`** = distance in meters from wall **start point** (the M coordinate in SVG path) to the opening **center**.

**Validation rules** (apply to both methods):
- Must satisfy: `position - width/2 >= 0` AND `position + width/2 <= wall_length`
- Multiple openings on the same wall must not overlap
- The CLI `build` command warns about out-of-bounds and overlapping placements

### SVG File Template
Always use this structure for SVG files:
```xml
<svg xmlns="http://www.w3.org/2000/svg">
  <g transform="scale(1,-1)">
    <!-- elements here, using normal Cartesian coordinates (X=right, Y=up) -->
  </g>
</svg>
```

## Base Schema Reference

All elements inherit from `element`:
- **Write to CSV**: `id` (required), `number`, `base_offset` (default 0), `mesh_file`
- **Query-only** (computed, never write): `level_id`, `created_at`, `updated_at`, `volume`, `bbox_min_x`, `bbox_min_y`, `bbox_min_z`, `bbox_max_x`, `bbox_max_y`, `bbox_max_z`

**Geometry bases** — these fields are query-only (derived from SVG, never write to CSV):
- `line_element` (wall, beam, etc.): `start_x`, `start_y`, `end_x`, `end_y`, `length`
- `point_element` (column, equipment, etc.): `x`, `y`, `rotation`
- `polygon_element` (slab, roof, etc.): `points`, `area`, `perimeter`

**Hosted elements** (`hosted_element`): Use `host_x`/`host_y` (recommended) or `host_id` + `position`. See Door/Window Placement Rules above.

**Vertical span** (`vertical_span`): Write `top_level_id`, `top_offset` — see Vertical Positioning rules above. Query-only: `height`.

**Material enum** (`materialized`): concrete, steel, wood, clt, glass, aluminum, brick, stone, gypsum, insulation, copper, pvc, ceramic, fiber_cement, composite

## Core Schema Topologies (Concrete Tables)

Below is a curated whitelist of the **most commonly used** core architectural elements. 

> **IMPORTANT**: The complete list of available elements in this project is:
> `beam`, `brace`, `cable_tray`, `ceiling`, `column`, `conduit`, `curtain_wall`, `door`, `duct`, `equipment`, `foundation`, `grid`, `level`, `mep_node`, `mesh`, `opening`, `pipe`, `railing`, `ramp`, `roof`, `room_separator`, `slab`, `space`, `stair`, `structure_column`, `structure_slab`, `structure_wall`, `terminal`, `wall`, `window`
> 
> If the user asks you to modify or generate elements not listed below, **RUN** `bimdown schema <table_name>` to fetch their requirements!

### Table: `door` (Prefix: `d`)
- **Geometry**: CSV only. Use `host_x, host_y` or `host_id` + `position` to place on a wall.
```yaml
id_prefix: d
name: door
bases:
  - hosted_element
  - materialized
host_type: wall

fields:
  - name: width
    type: float
    required: true

  - name: height
    type: float

  - name: operation
    type: enum
    values:
      - single_swing
      - double_swing
      - sliding
      - folding
      - revolving

  - name: hinge_position
    type: enum
    values:
      - start
      - end

  - name: swing_side
    type: enum
    values:
      - left
      - right

```

### Table: `grid` (Prefix: `gr`)
- **Geometry**: CSV only
```yaml
id_prefix: gr
name: grid

fields:
  - name: id
    type: string
    required: true

  - name: number
    type: string
    required: true

  - name: start_x
    type: float
    required: true

  - name: start_y
    type: float
    required: true

  - name: end_x
    type: float
    required: true

  - name: end_y
    type: float
    required: true
```

### Table: `level` (Prefix: `lv`)
- **Geometry**: CSV only
```yaml
id_prefix: lv
name: level

fields:
  - name: id
    type: string
    required: true

  - name: number
    type: string
    required: true

  - name: name
    type: string

  - name: elevation
    type: float
    required: true
```

### Table: `space` (Prefix: `sp`)
- **Geometry**: SVG required
```yaml
id_prefix: sp
name: space
bases:
  - element

fields:
  - name: x
    type: float
    required: true
    description: Seed point X coordinate (room interior point)

  - name: y
    type: float
    required: true
    description: Seed point Y coordinate (room interior point)

  - name: name
    type: string

  - name: boundary_points
    type: string
    computed: true
    description: Space boundary polygon vertices (computed by build from surrounding walls)

  - name: area
    type: float
    computed: true
    description: Space area in square meters (computed from boundary polygon)

```

### Table: `wall` (Prefix: `w`)
- **Geometry**: SVG required
- **IMPORTANT**: A wall MUST be one complete straight line (start to end). Do NOT split a wall into segments for doors/windows. Doors and windows attach to the wall via the `position` parameter on the host wall.
```yaml
id_prefix: w
name: wall
bases:
  - line_element
  - vertical_span
  - materialized

fields:
  - name: thickness
    type: float
    required: true
    description: Wall thickness in meters. SVG stroke-width should match but CSV is source of truth.

```

### Table: `window` (Prefix: `wn`)
- **Geometry**: CSV only. Use `host_x, host_y` or `host_id` + `position`. Always set `base_offset` (sill height, typically 0.9m).
```yaml
id_prefix: wn
name: window
bases:
  - hosted_element
  - materialized
host_type: wall

fields:
  - name: width
    type: float
    required: true

  - name: height
    type: float

```

## Additional Resources

If you need more detailed information about the BimDown format, or if you need the conversion tool to round-trip data between Autodesk Revit and BimDown, please refer to the official GitHub repository:
**[https://github.com/NovaShang/BimDown](https://github.com/NovaShang/BimDown)**
