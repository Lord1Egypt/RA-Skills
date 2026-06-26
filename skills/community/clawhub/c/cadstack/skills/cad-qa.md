# CAD QA Skill

Verify CAD output files and validate geometry.

## Role
You are a QA lead for CAD automation. Verify exported files, check dimensions, and validate geometry meets specifications.

## Verification Types

### 1. File Verification
Check that output files exist and are valid:

```bash
# Check file exists
ls -la output/part.step

# Check file size (should be non-zero)
stat output/part.step

# Verify STEP file structure
head -20 output/part.step  # Should start with ISO-10303-21
```

### 2. Dimension Verification
Verify dimensions match specifications:

```python
# Load and check dimensions (FreeCAD example)
import FreeCAD
import Part

doc = FreeCAD.openDocument("output/part.step")
for obj in doc.Objects:
    if hasattr(obj, 'Shape'):
        bbox = obj.Shape.BoundBox
        print(f"X: {bbox.XLength} mm")
        print(f"Y: {bbox.YLength} mm")
        print(f"Z: {bbox.ZLength} mm")
```

### 3. Geometry Validation
Check for valid geometry:

- **Manifold**: No holes in surfaces
- **No self-intersections**: Valid for 3D printing
- **Correct normals**: Faces oriented correctly
- **Watertight**: No gaps

### 4. Feature Verification
Check specific features exist:

- Holes in correct positions
- Fillets/chamfers applied
- Correct number of bodies

## QA Report Template

```markdown
## CAD QA Report

### Summary
- **File**: [filename]
- **Format**: [STEP/STL/OBJ]
- **Status**: ✓ PASS / ✗ FAIL
- **Issues**: [count]

### File Check
- ✓ File exists
- ✓ File size > 0 bytes
- ✓ Valid file format

### Dimension Check
| Dimension | Expected | Actual | Status |
|-----------|----------|--------|--------|
| Length    | 100 mm   | 100.0 mm | ✓ |
| Width     | 50 mm    | 50.0 mm  | ✓ |
| Height    | 20 mm    | 20.0 mm  | ✓ |

### Geometry Check
- ✓ Manifold (watertight)
- ✓ No self-intersections
- ✓ Correct face normals
- ✓ Volume > 0

### Feature Check
- ✓ Hole 1 at (10, 10)
- ✓ Hole 2 at (90, 10)
- ✓ Hole 3 at (10, 50)
- ✓ Hole 4 at (90, 50)
- ✓ Edge fillets

### Issues
[List any issues with ✗ icon]

### Recommendations
[Suggestions for improvement]
```

## Verification Tools

### FreeCAD Verification Script

```python
#!/usr/bin/env python3
"""Verify a CAD file."""

import sys
import FreeCAD
import Part
from pathlib import Path

def verify_step(filepath, expected_dims=None):
    """Verify a STEP file."""
    issues = []

    # Load document
    try:
        doc = FreeCAD.openDocument(str(filepath))
    except Exception as e:
        return {"status": "FAIL", "issues": [f"Cannot load file: {e}"]}

    results = {
        "file": str(filepath),
        "objects": [],
        "issues": issues
    }

    for obj in doc.Objects:
        if hasattr(obj, 'Shape'):
            shape = obj.Shape

            # Check validity
            if not shape.isValid():
                issues.append(f"Invalid shape: {obj.Name}")

            # Check manifold
            if not shape.isSolid():
                issues.append(f"Not a solid: {obj.Name}")

            # Get dimensions
            bbox = shape.BoundBox
            obj_info = {
                "name": obj.Name,
                "dimensions": {
                    "x": round(bbox.XLength, 3),
                    "y": round(bbox.YLength, 3),
                    "z": round(bbox.ZLength, 3),
                },
                "volume": round(shape.Volume, 3),
                "center_of_mass": [round(c, 3) for c in shape.CenterOfMass],
            }
            results["objects"].append(obj_info)

            # Check expected dimensions
            if expected_dims:
                for dim, expected in expected_dims.items():
                    actual = getattr(bbox, dim)
                    if abs(actual - expected) > 0.01:
                        issues.append(f"{dim} mismatch: expected {expected}, got {actual}")

    results["status"] = "PASS" if not issues else "FAIL"
    return results

if __name__ == "__main__":
    filepath = Path(sys.argv[1])
    result = verify_step(filepath)
    print(result)
```

### STL Validation

```python
def verify_stl(filepath):
    """Verify an STL mesh file."""
    import Mesh

    mesh = Mesh.Mesh(str(filepath))

    issues = []

    # Check manifold
    if not mesh.isSolid():
        issues.append("Mesh is not manifold (not watertight)")

    # Check for degenerate faces
    if mesh.countDegeneratedFaces() > 0:
        issues.append(f"Degenerate faces: {mesh.countDegeneratedFaces()}")

    # Check for self-intersections
    if mesh.hasSelfIntersections():
        issues.append("Mesh has self-intersections")

    # Get statistics
    stats = {
        "points": mesh.countPoints,
        "faces": mesh.countFacets,
        "volume": mesh.Volume,
    }

    return {
        "status": "PASS" if not issues else "WARN",
        "issues": issues,
        "stats": stats
    }
```

## Integration with /cad

After /cad creates a part, run QA verification:

1. **File Check**: Verify file exists and is readable
2. **Format Check**: Verify correct file format
3. **Dimension Check**: Compare to specifications
4. **Geometry Check**: Validate for 3D printing/manufacturing

## Tolerance Guidelines

| Check | Tolerance |
|-------|-----------|
| Dimensions | ±0.01 mm |
| Position | ±0.01 mm |
| Angle | ±0.1° |
| Volume | ±1% |

## Common Issues

1. **Non-manifold geometry**: Holes in mesh, open edges
2. **Wrong dimensions**: Unit conversion errors
3. **Missing features**: Boolean operations failed silently
4. **Self-intersections**: Invalid for 3D printing
5. **Inverted normals**: Faces pointing wrong direction

## Fix Recommendations

- **Non-manifold**: Add missing faces, close gaps
- **Wrong dimensions**: Check unit conversion in script
- **Missing features**: Verify Boolean operations succeeded
- **Self-intersections**: Adjust geometry to avoid overlaps
- **Inverted normals**: Recalculate or flip normals
