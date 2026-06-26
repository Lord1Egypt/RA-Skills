# CAD Review Skill

Review generated CAD scripts for safety and correctness.

## Role
You are a safety reviewer for CAD automation scripts. Analyze scripts before execution to catch errors and security issues.

## What Gets Reviewed

### 1. Security Review
Check for dangerous patterns that could harm the system:

```python
# DANGEROUS - Should reject or warn
os.system("rm -rf /")
subprocess.call(["dangerous", "command"])
eval(user_input)
exec(untrusted_code)
__import__("os")

# SAFE - CAD operations only
backend.create_box(100, 50, 20)
backend.export_step(doc, output)
```

### 2. Syntax Review
Check for Python syntax errors:

```python
# ERROR - Missing parenthesis
backend.create_box(100, 50, 20

# ERROR - Undefined variable
backend.create_box(length, width, height)  # Variables not defined

# OK - Correct syntax
backend.create_box(100, 50, 20)
```

### 3. API Review
Check for correct API usage:

```python
# ERROR - Wrong parameter order
backend.create_box(20, 100, 50)  # Should be length, width, height

# ERROR - Missing required parameter
backend.create_cylinder(25)  # Missing height

# ERROR - Invalid operation
backend.create_cube(100)  # Should be create_box

# OK - Correct API usage
backend.create_box(length=100, width=50, height=20)
```

### 4. Geometric Review
Check for geometric validity:

```python
# WARNING - Negative dimension
backend.create_box(-100, 50, 20)  # Negative length

# WARNING - Zero dimension
backend.create_cylinder(0, 50)  # Zero radius

# WARNING - Unusual aspect ratio
backend.create_box(1000, 1, 1)  # Very thin, might cause issues

# OK - Valid geometry
backend.create_box(100, 50, 20)
```

### 5. Logic Review
Check for logical errors:

```python
# WARNING - Cut target not defined
result = backend.cut(undefined_box, hole)

# WARNING - Export before recompute
backend.export_step(doc, output)  # Without backend.recompute()

# WARNING - No document created
box = backend.create_box(100, 50, 20)  # No create_document call

# OK - Correct logic
backend.create_document("part")
box = backend.create_box(100, 50, 20)
backend.recompute()
backend.export_step(backend._current_doc, output)
```

## Review Output Format

```markdown
## Script Review

### Summary
- **Status**: PASS / WARN / FAIL
- **Issues Found**: [count]
- **Lines Reviewed**: [count]

### Issues

#### CRITICAL (Must Fix)
1. [Line X] [Issue description]
   - Code: `relevant code`
   - Fix: [How to fix]

#### WARNINGS (Should Review)
1. [Line X] [Warning description]
   - Code: `relevant code`
   - Suggestion: [Improvement]

#### SUGGESTIONS (Optional)
1. [Line X] [Suggestion]
   - Code: `relevant code`
   - Reason: [Why this helps]

### Security Check
- ✓ No system commands
- ✓ No dynamic code execution
- ✓ No file operations outside output directory
- ✓ No network operations

### Corrected Script
```python
# Provide corrected version if fixes were needed
```
```

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| ✗ SecurityViolation | Dangerous pattern detected | → Remove os/subprocess/eval calls |
| ✗ SyntaxError | Invalid Python syntax | → Fix syntax on indicated line |
| ✗ InvalidAPIUsage | Wrong method/parameters | → Check API documentation |
| ⚠ NegativeDimension | Negative value in geometry | → Use positive dimension |
| ⚠ ZeroDimension | Zero value in geometry | → Use non-zero dimension |
| ⚠ UndefinedVariable | Variable used before definition | → Define variable before use |
| ⚠ MissingRecompute | Export without recompute | → Add backend.recompute() |
| ⚠ MissingDocument | Operation without document | → Add backend.create_document() |

## Text Equivalents (Accessibility)

When screen readers or plain-text output is needed:

| Icon | Text |
|------|------|
| ✓ | [OK] |
| ✗ | [FAIL] |
| ⚠ | [WARN] |

## Review Process

1. **Read Script**: Parse the script content
2. **Run Validator**: Use CADScriptValidator for security check
3. **Manual Review**: Check API usage and logic
4. **Generate Report**: Create structured review output
5. **Fix Issues**: Either auto-fix or report to user

## Integration with /cad

The /cad skill has built-in safety review. Use /cad-review separately when:
- You want a more thorough review
- The script is complex and needs detailed analysis
- You're reviewing a script from an external source
- You want to audit existing CAD scripts

## Example Review

```python
# Script to review:
backend.create_document("bracket")
box = backend.create_box(100, 60, 5)
hole = backend.create_cylinder(4, 5)
backend.move(hole, 10, 10, 0)
result = backend.cut(box, hole, "BracketWithHole")
backend.export_step(backend._current_doc, output)
```

```markdown
## Script Review

### Summary
- **Status**: WARN
- **Issues Found**: 2
- **Lines Reviewed**: 6

### Issues

#### WARNINGS
1. [Line 6] Missing recompute before export
   - Code: `backend.export_step(backend._current_doc, output)`
   - Suggestion: Add `backend.recompute()` before export

2. [Line 4] Only one hole created
   - Note: User asked for "four holes" but script only creates one
   - Suggestion: Create and position all four holes

### Security Check
- ✓ No system commands
- ✓ No dynamic code execution
- ✓ No file operations outside output directory
- ✓ No network operations

### Corrected Script
```python
backend.create_document("bracket")
box = backend.create_box(100, 60, 5)

# Create four mounting holes
holes = []
for x, y in [(10, 10), (90, 10), (10, 50), (90, 50)]:
    hole = backend.create_cylinder(4, 5, f"Hole_{x}_{y}")
    backend.move(hole, x, y, 0)
    holes.append(hole)

# Cut all holes
result = box
for hole in holes:
    result = backend.cut(result, hole)

backend.recompute()
backend.export_step(backend._current_doc, output)
```
```
