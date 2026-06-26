# CADStack Design System

> This document defines the design standards for all CADStack skills. All skill files should follow these conventions for consistent user experience.

## Output Format Standards

### Status Icons

| Icon | Meaning | Usage |
|------|---------|-------|
| ✓ | Success | Operation completed successfully |
| ✗ | Error | Operation failed (requires user action) |
| ⚠ | Warning | Completed with caveats |
| ⏳ | Loading | Operation in progress |
| ○ | Empty | No items/results |
| ℹ | Info | Informational note |

### Terminal Output Blocks

```
╭─────────────────────────────────────────╮
│ [Title]                                 │
├─────────────────────────────────────────┤
│ Content here...                         │
╰─────────────────────────────────────────╯
```

Use Rich console tables for structured data.

### Section Headers

```markdown
## [SECTION NAME]

Brief description (optional).

### Subsection

Content...
```

Standard sections for all skills:
1. Role
2. Workflow
3. Examples
4. Error Handling
5. Reference (if applicable)

## Report Templates

### Success Report

```
✓ [Operation] → [Result]
   [Key details in 1-2 lines]

Example:
✓ Created: output/bracket.step (12.4 KB)
   Dimensions: 100 × 50 × 5 mm | Volume: 25,000 mm³
```

### Error Report

```
✗ [Error Type] → [Recovery command]

Example:
✗ BackendNotAvailable → /cad-config --check freecad
```

### Warning Report

```
⚠ [Issue description]
   → [Optional action]

Example:
⚠ Fillet skipped on 2 edges (radius too large)
   → Reduce fillet radius to 3mm or increase edge length
```

### QA Report Structure

```markdown
## CAD QA Report

### Summary
- **File**: [filename]
- **Format**: [STEP/STL/OBJ]
- **Status**: PASS / FAIL
- **Issues**: [count]

### Dimension Check
| Dimension | Expected | Actual | Status |
|-----------|----------|--------|--------|
| Length    | 100 mm   | 100.0  | ✓      |

### Geometry Check
- ✓ Manifold (watertight)
- ✓ No self-intersections
- ✓ Correct face normals
```

### Review Report Structure

```markdown
## Script Review

### Summary
- **Status**: PASS / WARN / FAIL
- **Issues Found**: [count]
- **Lines Reviewed**: [count]

### Issues
#### CRITICAL (Must Fix)
1. [Line X] [Issue] → [Fix]

#### WARNINGS (Should Review)
1. [Line X] [Issue] → [Suggestion]

### Security Check
- ✓ No system commands
- ✓ No dynamic code execution
- ✓ No file operations outside output directory
```

## Terminology

| Term | Definition |
|------|------------|
| Backend | CAD platform (FreeCAD, AutoCAD, etc.) |
| Primitive | Basic shape (box, cylinder, sphere) |
| Boolean | Combine operations (fuse, cut, intersect) |
| Feature | Modification (fillet, chamfer, hole) |
| Export | Save to file format (STEP, STL, OBJ) |
| Manifold | Watertight geometry (no holes in surface) |

## Units Convention

- Default: millimeters (mm)
- Always include units in user-facing text
- Accept: mm, cm, m, in, inches, ft, feet
- Internal: convert everything to mm

## Error Categories

| Category | Icon | Recovery |
|----------|------|----------|
| BackendNotAvailable | ✗ | /cad-config --check [platform] |
| InvalidDimension | ✗ | Fix dimension value |
| ExportFailed | ✗ | Check output/ permissions |
| ValidationWarning | ⚠ | Review or accept |
| GeometryError | ✗ | Fix CAD script |

## File Naming

### Output Files
- Pattern: `{part_name}.{format}`
- Example: `bracket.step`, `gear.stl`
- Default location: `~/.claude/skills/cadstack/output/`

### Template Files
- Pattern: `{platform}/{part_type}.py`
- Example: `freecad/basic_box.py`, `cadquery/gear.py`

## Color Codes (for Rich output)

| Element | Color | Rich Code |
|---------|-------|-----------|
| Success | Green | `green` |
| Error | Red | `red` |
| Warning | Yellow | `yellow` |
| Info | Blue | `blue` |
| Muted | Dim | `dim` |
| Highlight | Cyan | `cyan` |

## Accessibility

- Always include text equivalents for icons (✓ = "Success")
- Use high contrast for terminal output
- Provide alternative instructions when Rich formatting unavailable
- Error messages should be actionable, not just descriptive

### Text Equivalents for Icons

When screen readers or plain-text terminals are detected, replace:

| Icon | Text Equivalent |
|------|-----------------|
| ✓ | [OK] |
| ✗ | [FAIL] |
| ⚠ | [WARN] |
| ⏳ | [WORKING] |
| ○ | [EMPTY] |
| ℹ | [INFO] |

### Color-Blind Considerations

Never rely solely on color to convey meaning:
- ✓ Use icons AND color
- ✓ Use text labels for critical status
- ✓ Test with `NO_COLOR=1` environment variable

### Terminal Width

Assume 80-char minimum width. Wrap long lines:
```
✓ Created: output/very_long_filename_that_exceeds...
   (truncated, full path: ~/.claude/skills/cadstack/...)
```
