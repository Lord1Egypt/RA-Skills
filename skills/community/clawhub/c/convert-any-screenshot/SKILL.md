---
name: convert-any-screenshot
description: >
  Use when (1) Convert any UI screenshot into a clean React or HTML/CSS implementation prompt. 
license: MIT
metadata:
  version: "1.0"
  category: design
  author: wangjipeng
  sources:
    - https://github.com/MiniMax-AI/skills
---
## Core Position

This skill transforms **input data from one format into a target format**, preserving structure and fidelity. It is NOT a simple copy-paste — it handles formatting, schema mapping, and edge cases.

Key responsibilities:
- Parse the input format (JSON/CSV/code/etc.) and validate structure before transforming
- Apply formatting rules specific to the target format (indentation, escaping, etc.)
- Handle edge cases: missing fields, unusual characters, nested structures
- Provide a clear mapping summary so the user understands how input maps to output

## Modes

### `/convert-any-screenshot --pretty`
**Formatted output.** Applies proper indentation, spacing, and style conventions.

### `/convert-any-screenshot --strict`
**Strict mode.** Fails on any deviation from expected structure rather than guessing.

## Execution Steps

1. **Parse input** — Read and parse the input; detect format (JSON/CSV/XML/code/etc.)
   - If parsing fails, report: "Failed to parse input as [format] — error at line [N]: [detail]"
2. **Validate structure** — Check required fields/columns are present
   - If missing required field `X`, stop and report: "Missing required field: [X]"
3. **Transform** — Convert input to target format, applying format-specific rules
   - Preserve all data — do not silently drop fields
   - Apply proper escaping for special characters (quotes, newlines, etc.)
4. **Validate output** — Run the target format parser on the result to confirm it's valid
   - If output is invalid, revert to previous version and report what went wrong
5. **Deliver** — Return the converted output with a brief mapping summary

## Mandatory Rules

### Do not

- Do not silently drop fields or data — if a field cannot be mapped, report it
- Do not guess at missing data — if a field is absent, leave it null/empty and flag it
- Do not apply formatting that destroys the semantic meaning of the data
- Do not produce output that fails the target format validator
- Do not convert binary data as if it were text — detect and handle binary separately

### Do

- Report the complete field mapping: `[source] -> [target]` for every field
- Validate input and output formats before and after transformation
- Preserve character encoding (UTF-8) throughout the conversion process
- Handle large inputs in chunks if needed to avoid memory exhaustion
- Log conversion statistics: fields mapped, fields dropped, warnings issued

## Quality Bar

| Criterion | Minimum | Ideal |
|-----------|---------|-------|
| Data fidelity | Zero data loss — all fields mapped | Full semantic equivalence, not just structural |
| Format validity | Output passes target parser | Output passes strict schema validation |
| Edge case handling | Handles missing/null/empty gracefully | Documents every edge case decision |
| Escaping correctness | Proper escaping for target format | Round-trip: convert back to source equals original |
| Performance | Completes within 2x manual time | Streaming output for large inputs |

A good output passes the target format parser without errors and preserves all semantic content.

## Good vs. Bad Examples

| Scenario | Bad | Good |
|---------|-----|------|
| Missing field | Omits field from output silently | Reports "Field [X] absent — output null, flagged as warning" |
| Special characters | Only escapes visible chars | Escapes all special chars per target format spec |
| Large input | Loads entire file into memory | Streams in chunks, reports progress at 25/50/75% |
| Output validation | Skips validation | Runs target parser on output, confirms valid before returning |
| Format error | Returns raw output with error text appended | Returns nothing, reports "Output invalid: [parser error] at [location]" |
