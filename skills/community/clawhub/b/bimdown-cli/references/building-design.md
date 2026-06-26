# Building Design SOP

> From user brief to complete BimDown BIM model. Follow phases in order; render + build after each.

## Phase 0: Prerequisites

Run `bimdown init <dir>`. Gather from user (ask if missing): building type, total GFA, floor count, site constraints, functional requirements.

## Phase 1: Programming & Massing

**Floor heights** (m): Office 3.6–4.0 | Residential 2.8–3.0 | Commercial 4.5–5.0 | Hotel 3.2–3.6 | Healthcare 3.9–4.2 | Basement 3.6–4.2 | Ground floor lobby 4.5–6.0

**Footprint**: `GFA / above-ground floors = footprint area`. Verify it fits the site.

**Shape**: Rectangle (default), L/U/H-shape for daylight or site. Keep workspace-to-exterior-wall ≤ 8m (office) for daylight.

**Entrance**: Main entrance faces primary road. Service entrance on opposite side.

**Create `global/level.csv`**: elevation cumulative from 0, basements negative.

**Checkpoint**: floor count × floor area ≈ GFA (±10%), `bimdown build` passes.

## Phase 2: Space Programming

**Office room standards**:
- Open office 6–8 m²/person | Small meeting 12–15 m² | Medium meeting 25–35 m² | Large meeting 50–80 m²
- Executive office 15–25 m² | Restroom (M/F) 25–35 m²/floor | Pantry 10–20 m² | IT room 15–25 m²
- Storage 10–15 m² | Electrical 6–10 m² | Janitor 4–6 m² | Lobby 30–80 m² (GF only)

**Residential**: Living 20–35 m² | Master bed 12–18 m² | Secondary bed 9–12 m² | Kitchen 5–8 m² | Bath 3–6 m²

**Area balance**: usable + circulation (18–25%) + walls (5–8%) ≈ gross floor area (±15%).

**Checkpoint**: complete room list per floor, no missing essentials (restrooms, mechanical, egress).

## Phase 3: Vertical Circulation

**Stairs**: ≥ 2 for multi-story. Max evacuation distance ≤ 40m, dead-end ≤ 20m. Footprint ~6.0 × 2.8m. Width ≥ 1.2m (commercial). Tread 0.26–0.28m, riser 0.15–0.175m. Place at opposite building ends.

**Elevators**: ~1 per 3,000–5,000 m² GFA. Shaft 2.1 × 2.4m (standard), 2.4 × 2.4m (accessible). Group near center.

**Core**: Combine stairs + elevators + restrooms + shafts. Central core (towers), side core (slab buildings). Core = 15–20% of floor area. Use regular `wall` elements for enclosures.

**Checkpoint**: max point-to-stair ≤ 40m, ≥ 2 stairs, core 15–20%.

## Phase 4: Horizontal Circulation & Room Connectivity

**Corridor widths** (m): Main 1.8 | Secondary 1.4 | Residential 1.2 | Dead-end 1.4 (max 20m) | Hospital 2.4

**Layout**: Central corridor (double-loaded, depth > 12m) or single-loaded (depth ≤ 8m, premium).

**Define room connectivity BEFORE drawing walls.** Write out the connectivity graph for each floor — every room must trace back to a stair/elevator through doors. Example for an office floor:

```
Stair 1 ─┬─ Corridor ─┬─ Open Office
Stair 2 ─┘            ├─ Meeting Room 1
Elevator ──────────────┤
                       ├─ Meeting Room 2
                       ├─ Pantry
                       ├─ Restroom M
                       ├─ Restroom F
                       ├─ Storage
                       └─ Electrical Room
```

Example for a hotel floor:
```
Stair 1 ─┬─ Corridor ─┬─ Room 201 ── Bathroom 201
Stair 2 ─┘            ├─ Room 202 ── Bathroom 202
Elevator ──────────────┤
                       ├─ Room 203 ── Bathroom 203
                       └─ Housekeeping
```

Each `──` connection means a door is needed on the wall between those two spaces. Use this graph when placing doors in Phase 5.3 to ensure no room is left disconnected.

**Assign coordinates**: Work on grid lines. Tile rooms along corridor with no gaps/overlaps.

**Checkpoint**: connectivity graph covers every room, corridor widths meet minimums, dead-ends ≤ 20m.

## Phase 5: Architecture Drawing

**Render after each subsection. Fix before moving on.**

### 5.1 Grid
Create `global/grid.csv`. X-grids (vertical): `start_x = end_x`, numbered 1,2,3. Y-grids (horizontal): `start_y = end_y`, lettered A,B,C. Spacing: 6/7.2/8/9m. Extend 2–5m beyond building.

### 5.2 Walls
Exterior first (0.2–0.3m, concrete/brick), then interior partitions (0.1–0.15m, gypsum), core walls (0.2m, concrete). One wall = one straight line, never split for doors. Endpoints must align exactly.

### 5.3 Doors & Windows
**Doors**: single 0.9×2.1m, double 1.8×2.1m, entrance 1.8–2.4×2.4–3.0m, fire 0.9–1.0×2.1m.

**Windows**: standard 1.2–1.8×1.5m `base_offset=0.9`, floor-to-ceiling 1.5–3.0×2.4m `base_offset=0.0`, high strip 1.2–2.4×0.6m `base_offset=1.8`. **Always set `base_offset`** (sill height) — omitting it puts windows at floor level.

**Recommended**: use `host_x, host_y` (2D coordinate of the opening center) instead of `position` — `bimdown build` auto-finds the wall and computes position. Validate: `position ± width/2` within wall length, no overlaps.

**Connectivity check**: Place doors according to the connectivity graph from Phase 4. Every `──` connection in the graph = one door on the wall between those spaces. After placing all doors, verify every room traces back to a stair/elevator.

### 5.4 Slabs
Polygon matching exterior wall outline. `function`: floor or roof. Thickness 0.15–0.25m. Account for stair/elevator shaft openings.

### 5.5 Spaces
Seed point (x, y) inside each enclosed room. `bimdown build` computes boundary. Point must be clearly inside walls, not on or near them.

### 5.6 Roof
Top floor only. `roof_type`: flat/gable/hip/shed/mansard. `slope` in degrees.

### 5.7 Multi-Floor
Complete typical floor (usually lv-2) → validate → copy to other lv-N dirs → adjust non-standard floors (GF lobby, top mechanical, basement parking). IDs are level-scoped.

**Checkpoint**: build zero warnings, every floor renders correctly, all connectivity graph connections have corresponding doors, all spaces have computed boundaries, slabs cover full footprint.

## Phase 6: Structural Design

**Columns** (`structure_column`): At grid intersections. Sizes: residential 0.3–0.4m, office 0.5–0.6m, tall 0.6–0.8m. SVG `<rect>` x,y = corner (not center).

**Beams**: Primary along grid (rect 0.3×0.6m), secondary perpendicular at 2–3m (rect 0.2×0.4m). `start_z`/`end_z` = offset from level (0 or negative).

**Structure slabs**: If needed separately from architectural slabs.

**Foundations** (lowest level): SVG geometry determines type — `<rect>`/`<circle>` = isolated, `<path>` = strip, `<polygon>` = raft.

**Checkpoint**: column at every grid intersection, beams connect columns, foundations under all columns.

## Phase 7: HVAC

**System selection**: Small office → VRF/split | Medium → AHU+FCU | Large → central plant+VAV | Residential → split/VRF

**system_type codes**: SA (Supply Air), RA (Return Air), EA (Exhaust Air), OA (Outdoor Air), CHWS/CHWR (Chilled Water Supply/Return), HWS/HWR (Hot Water Supply/Return)

**Equipment**: ahu in mechanical room (3.0×1.5m), fcu per zone (1.0×0.4m), chiller/boiler in basement

**Ducts**: Main along corridor ceiling (rect 0.6×0.4m), branches to rooms (0.3×0.2m). `start_z`/`end_z` ≈ floor_height − 0.3 to 0.5.

**Terminals**: Every occupied room: ≥ 1 `supply_air_diffuser` (SA) + 1 `return_air_grille` (RA). Spacing 3–4m in large rooms.

**Topology**: Align duct endpoints with equipment/terminal coordinates. Run `bimdown resolve-topology`.

**Checkpoint**: every room has supply+return, ducts connect AHU→rooms, resolve-topology succeeds.

## Phase 8: Plumbing

**system_type codes**: DW (Domestic Water), HW (Hot Water), SW (Sanitary Waste), RW (Rain Water), FP (Fire Protection)

**Pipes**: Risers in shafts, branches to restrooms/pantries. Supply DN15–50 (0.015–0.05m), drain DN50–100 (0.05–0.1m). Waste pipes need slope (`start_z` ≠ `end_z`).

**Terminals**: `plumbing_fixture` per restroom/pantry, `sprinkler_head` on 3×3m grid (FP).

**Checkpoint**: restrooms/pantries have pipes, sprinkler coverage (if FP), resolve-topology succeeds.

## Phase 9: Electrical

**system_type codes**: POWER, LIGHTING, FIRE_ALARM, DATA

**Equipment**: transformer (basement, 1/building), panelboard (per floor in electrical closet)

**Distribution**: cable_tray from shaft along corridor (rect 0.3×0.1m), conduit branches to rooms (round 0.025m)

**Terminals**: light_fixture (2.5–3m grid), power_outlet (1–2/wall), data_outlet (1/workstation), fire_alarm_device (1/room+corridors)

**Checkpoint**: every floor has panelboard, every room has lights+outlets, fire alarm coverage, resolve-topology succeeds.

## Phase 10: Final Delivery

1. `bimdown build` — zero warnings
2. `bimdown info` — element counts reasonable
3. `bimdown render` every floor — visually verify
4. `bimdown publish` — provide 3D preview URL
5. Summary to user: floors, GFA, room schedule, systems, preview link

## Iteration Protocol

After every major step: **Create → Render → Build → Fix → Repeat**. Never skip render — visual verification catches errors validation cannot.
