---
name: editorconfig-linter
description: Validate .editorconfig syntax and check source files for EditorConfig compliance.
version: 1.0.0
---

# EditorConfig Linter

Validate .editorconfig files and check source files for compliance.

## Commands

### Validate .editorconfig syntax
```bash
python3 scripts/editorconfig-linter.py validate .editorconfig
```

### Check files against .editorconfig rules
```bash
python3 scripts/editorconfig-linter.py check src/
python3 scripts/editorconfig-linter.py check src/ --editorconfig .editorconfig
```

### Show effective config for a file
```bash
python3 scripts/editorconfig-linter.py show src/main.py
```

### Fix violations automatically
```bash
python3 scripts/editorconfig-linter.py fix src/
```

## Options

- `--editorconfig PATH` — Path to .editorconfig (default: auto-discover)
- `--format text|json|markdown` — Output format (default: text)
- `--strict` — Exit 1 on any violation (CI mode)
- `--exclude PATTERN` — Glob pattern to exclude (repeatable)
- `--max-files N` — Max files to check (default: 1000)

## What It Checks

### .editorconfig Syntax
- Invalid property names
- Invalid property values (indent_style must be tab/space, etc.)
- Duplicate sections
- Unreachable sections (shadowed by earlier glob)
- Missing root = true
- Invalid glob patterns

### File Compliance (9 rules)
- `indent_style` — tabs vs spaces
- `indent_size` — number of spaces per indent
- `end_of_line` — lf, crlf, cr
- `charset` — utf-8, utf-8-bom, latin1, utf-16be, utf-16le
- `trim_trailing_whitespace` — trailing whitespace check
- `insert_final_newline` — file ends with newline
- `max_line_length` — line length limit
- `tab_width` — tab display width
- Mixed indentation detection

## Exit Codes
- 0: No violations
- 1: Violations found (or --strict)
- 2: Invalid arguments or .editorconfig errors
