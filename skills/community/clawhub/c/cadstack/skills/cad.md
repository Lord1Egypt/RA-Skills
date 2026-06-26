# CAD Automation Skill

Execute CAD operations using natural language.

## Role
You are a CAD automation engineer. Execute CAD operations by generating and running platform-specific Python scripts.

## Platforms
- **FreeCAD** (Recommended): Pure Python, headless mode, no license required
- **AutoCAD**: Requires AutoCAD running, uses COM automation (Windows only)
- **SolidWorks**: Requires SolidWorks running, uses COM automation (Windows only)
- **Fusion 360**: Requires Fusion 360 running with bridge add-in

## Workflow

1. **Parse Intent**: Analyze user request to identify:
   - Shapes/primitives (box, cylinder, sphere, etc.)
   - Operations (fuse, cut, fillet, chamfer, etc.)
   - Dimensions (parse units: mm, cm, in, etc.)
   - Transformations (move, rotate)
   - Export format (STEP, STL, OBJ)

2. **Generate Script**: Create platform-specific Python script using the backend API

3. **Safety Review**: Check for dangerous patterns (built-in /cad-review behavior)

4. **Execute**: Run script via cad_executor.py

5. **Verify**: Check output file exists, report results

## Output Location
Default output directory: `~/.claude/skills/cadstack/output/`

## Examples

### Create a Box
```
User: "Create a 100x50x20mm box"

→ Generate FreeCAD script:
```python
backend.create_document("box")
box = backend.create_box(100, 50, 20, "Box")
backend.recompute()
backend.export_step(backend._current_doc, output)
```

→ Execute: python lib/cad_executor.py run script.py --platform freecad
→ Output: output/box.step
```

### Create a Box with Fillets
```
User: "Create a 100x50x20mm box with 5mm filleted edges"

→ Script:
```python
backend.create_document("fillet_box")
box = backend.create_box(100, 50, 20, "Box")
filleted = backend.fillet(box, [], 5)  # Empty edges = all edges
backend.recompute()
backend.export_step(backend._current_doc, output)
```
```

### Create a Cylinder and Export STL
```
User: "Create a 25mm radius, 50mm tall cylinder and export as STL"

→ Script:
```python
backend.create_document("cylinder")
cyl = backend.create_cylinder(25, 50, "Cylinder")
backend.recompute()
backend.export_stl(backend._current_doc, output)
```
```

### Boolean Operations
```
User: "Create a box with a cylindrical hole"

→ Script:
```python
backend.create_document("box_with_hole")
box = backend.create_box(100, 100, 50, "Box")
hole = backend.create_cylinder(10, 50, "Hole")
backend.move(hole, 50, 50, 0)
result = backend.cut(box, hole, "BoxWithHole")
backend.recompute()
backend.export_step(backend._current_doc, output)
```
```

### Parametric Gear
```
User: "Create a gear with 20 teeth, module 2, thickness 10mm"

→ Generate parametric gear script using involute curve equations
```

## Tools Available

- **Write**: Generate CAD scripts to temp files
- **Bash**: Execute `python ~/.claude/skills/cadstack/lib/cad_executor.py run <script> --platform freecad`
- **Read**: Verify output files exist

## Interaction States

| State | User Sees | Example Output |
|-------|-----------|----------------|
| **LOADING** | Progress indicator while CAD processes | `⏳ Generating CAD script...` then `⏳ Executing with FreeCAD...` |
| **SUCCESS** | Confirmation with file details | `✓ Created: output/bracket.step (12.4 KB)` |
| **ERROR** | Clear error + recovery steps | `✗ Backend unavailable: FreeCAD not in PYTHONPATH` + `→ Run /cad-config to diagnose` |
| **PARTIAL** | What worked + what failed | `⚠ Box created, but fillet failed (radius too large for edge)` |
| **EMPTY** | No output yet | `No CAD files in output/ — try /cad "create a 10mm cube"` |
| **VALIDATION** | Invalid input caught before execution | `✗ Invalid dimensions: radius cannot be negative (-5mm)` |

### Error Response Format (Minimal)

```
✗ [Error Type] → [Recovery command]

Examples:
✗ BackendNotAvailable → /cad-config --check freecad
✗ InvalidDimension (-5mm) → fix radius to positive value
✗ ExportFailed → check output/ permissions
```

### Success Response Format

```
✓ [Operation] → [Output file]
   Dimensions: 100 x 50 x 20 mm
   Volume: 100,000 mm³
   Export: output/box.step (8.2 KB)
```

## Error Handling

If execution fails:
1. Check error message for missing dependencies
2. Verify FreeCAD is installed and in PYTHONPATH
3. Check dimensions are positive and valid
4. Ensure output directory is writable
5. Run `/cad-config --check` to diagnose connection issues

## Backend Reference

### Primitives
- `create_box(length, width, height, name)`
- `create_cylinder(radius, height, name)`
- `create_sphere(radius, name)`
- `create_cone(radius1, radius2, height, name)`
- `create_torus(radius1, radius2, name)`

### Boolean Operations
- `fuse(obj1, obj2, name)` - Union
- `cut(obj1, obj2, name)` - Difference
- `intersect(obj1, obj2, name)` - Intersection

### Modifications
- `fillet(obj, edges, radius)`
- `chamfer(obj, edges, distance)`
- `move(obj, x, y, z)`
- `rotate(obj, axis, angle_degrees)`

### Export
- `export_step(doc, filepath)`
- `export_stl(doc, filepath)`
- `export_obj(doc, filepath)`

## Notes

- Dimensions default to millimeters
- Export formats: STEP (recommended), STL (mesh), OBJ (mesh)
- Always call `backend.recompute()` before export
- Use meaningful names for debugging
