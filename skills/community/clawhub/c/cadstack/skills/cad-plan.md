# CAD Plan Skill

Plan complex multi-step CAD operations before execution.

## Role
You are a CAD architect. Plan and design complex CAD operations before generating and executing scripts.

## When to Use
- Multi-step operations with dependencies
- Complex assemblies
- Parametric designs
- Operations requiring multiple features

## Workflow

1. **Analyze Request**: Break down the user's request into discrete steps
2. **Identify Dependencies**: Determine which operations depend on others
3. **Plan Sequence**: Order operations correctly
4. **Validate Plan**: Check for geometric feasibility
5. **Present Plan**: Show the user the planned steps
6. **Execute**: Generate and run scripts for each step

## Planning Template

```markdown
## CAD Operation Plan

### Objective
[Clear description of what we're building]

### Parameters
- Dimension 1: [value] [unit]
- Dimension 2: [value] [unit]
- ...

### Steps

1. **Create Base Feature**
   - Type: [Box/Cylinder/Sketch/etc.]
   - Parameters: [...]
   - Result: Base solid

2. **Add Feature**
   - Type: [Extrude/Cut/Fillet/etc.]
   - Parameters: [...]
   - Dependencies: [Step 1]

3. **Boolean Operation**
   - Type: [Fuse/Cut/Intersect]
   - Bodies: [Body A, Body B]
   - Dependencies: [Steps 1, 2]

4. **Apply Modifications**
   - Type: [Fillet/Chamfer]
   - Edges: [description]
   - Radius/Distance: [value]

5. **Export**
   - Format: [STEP/STL/OBJ]
   - Filename: [name]

### Validation
- [ ] All dimensions positive
- [ ] No self-intersection
- [ ] Features manufacturable
- [ ] Dependencies satisfied
```

## Example

```
User: "Create a mounting bracket: 100x60x5mm base plate with
       four 8mm mounting holes at corners, 2mm chamfers"

## CAD Operation Plan

### Objective
Rectangular mounting bracket with corner holes and chamfers.

### Parameters
- Base: 100 x 60 x 5 mm
- Hole diameter: 8 mm
- Hole offset from edge: 10 mm
- Chamfer: 2 mm

### Steps

1. **Create Base Plate**
   - Type: Box
   - Dimensions: 100 x 60 x 5 mm
   - Result: Base solid

2. **Create Mounting Holes** (x4)
   - Type: Cylinder (for cutting)
   - Diameter: 8 mm
   - Height: 5 mm (through)
   - Positions:
     - Hole 1: (10, 10, 0)
     - Hole 2: (90, 10, 0)
     - Hole 3: (10, 50, 0)
     - Hole 4: (90, 50, 0)

3. **Cut Holes from Base**
   - Type: Boolean Cut (x4)
   - Target: Base plate
   - Tools: Mounting holes
   - Dependencies: Steps 1, 2

4. **Apply Edge Chamfers**
   - Type: Chamfer
   - Edges: All top/bottom edges
   - Distance: 2 mm
   - Dependencies: Step 3

5. **Export**
   - Format: STEP
   - Filename: mounting_bracket.step

### Validation
- [x] All dimensions positive
- [x] Holes within bounds (10mm offset from 100x60 edges)
- [x] Chamfer smaller than material thickness
- [x] Dependencies satisfied
```

## Decision Points

When planning, identify decision points where user input is needed:

- **Dimension choices**: If dimensions are ambiguous
- **Feature priority**: Order of operations when multiple valid sequences exist
- **Export format**: If not specified, default to STEP

## Validation Rules

1. **Geometric Feasibility**
   - ✓ Positive dimensions
   - ✓ Holes within material bounds
   - ✓ Fillet radius less than edge length
   - ✓ Chamfer less than material thickness

2. **Manufacturability**
   - ✓ Wall thickness adequate
   - ✓ Draft angles for molding (if applicable)
   - ✓ No impossible geometry (e.g., internal corners)

3. **Dependencies**
   - ✓ Base features created before modifications
   - ✓ Boolean operations have valid operands
   - ✓ Export happens after all geometry complete

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| ✗ InvalidDimension | Negative or zero dimension | → Fix dimension value |
| ✗ FeatureOpFailed | Fillet/chamfer too large | → Reduce radius/distance |
| ✗ BooleanOpFailed | Geometry doesn't intersect | → Check object positions |
| ⚠ AmbiguousFeature | Multiple valid interpretations | → Ask user for clarification |
| ✗ DependencyNotMet | Referenced object not created | → Check step order |

### Plan Validation Output

```
✓ Plan validated — 5 steps, 0 issues
   Dependencies: satisfied
   Geometry: feasible

⚠ Plan validated — 5 steps, 2 warnings
   ⚠ Fillet radius may be too large for edge length
      → Reduce from 5mm to 3mm or skip fillet
   ⚠ Hole position near edge
      → Verify hole offset is sufficient

✗ Plan validation failed — 3 issues
   ✗ Negative dimension: width = -10mm
   ✗ Hole position outside bounds: (200, 50) on 100x60 plate
   ✗ Circular dependency: Step 3 depends on Step 4
```
