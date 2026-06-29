---
name: cx
description: "Semantic code navigation with `cx` CLI. Use when you need to understand code structure before reading files, find symbol definitions, trace references before refactoring, or explore large codebases efficiently. Triggers: 'cx overview', 'cx symbols', 'cx definition', 'cx references', 'code structure', 'find function', 'where is X defined', 'who calls X', 'semantic navigation'."
metadata:
  openclaw:
    emoji: 🧭
    requires:
      bins: [cx]
---

# cx — Semantic Code Navigation

Use `cx` to navigate code semantically **before** reading full files. This saves tokens and focuses attention on relevant code.

## Escalation Hierarchy

**Always follow this order**: overview → symbols → definition / references → read

| Goal | Command | Token Cost |
|------|---------|------------|
| Understand file structure | `cx overview <file>` | ~200 tokens |
| Find symbols across project | `cx symbols [--kind K] [--name GLOB]` | ~300 tokens |
| Read specific function/type | `cx definition --name <name>` | ~500 tokens |
| Find all usages of symbol | `cx references --name <name>` | ~200 tokens |
| Full file context (last resort) | `read <file>` | ~2000+ tokens |

## Quick Reference

```bash
# File structure (all symbols + signatures)
cx overview PATH

# Symbol search across project
cx symbols [--kind K] [--name GLOB] [--file PATH]

# Symbol body (function/type definition)
cx definition --name NAME [--from PATH] [--kind K] [--max-lines N]

# Symbol usages (call sites, references)
cx references --name NAME [--file PATH]

# Language management
cx lang list                    # Show installed grammars
cx lang add LANG [LANG...]      # Install grammars (rust, typescript, python, go, etc.)

# Cache management
cx cache path                   # Show cache location
cx cache clean                  # Delete cached index
```

**Short aliases**: `cx o`, `cx s`, `cx d`, `cx r`

**Symbol kinds**: `fn`, `method`, `struct`, `enum`, `trait`, `type`, `const`, `class`, `interface`, `module`, `event`

## When to Use cx vs Read

### ✅ Use cx when:
- **Before reading a file**: run `cx overview` first to understand structure
- **Before editing a function**: use `cx definition --name X` to capture exact text
- **Before refactoring**: use `cx references --name X` to understand impact
- **Exploring a codebase**: use `cx symbols` first, then narrow with `cx definition`
- **After context compression**: re-orient with `cx overview`

### ❌ Don't use cx when:
- File is **not a supported language** (cx only supports: Rust, TypeScript, Python, Go, C, C++, Java, Ruby, Lua, Zig, Bash, Solidity, Elixir)
- You need **full file context** (imports, comments, non-code content)
- File is **Markdown, YAML, JSON** — cx returns `unsupported file type`
- You need to **edit the file** — cx is read-only navigation

## 🔴 CHECKPOINT: Before Running cx

**STOP and verify**:
1. Target file is a **supported programming language** (not .md, .yaml, .json)
2. You're in a **git repository** (cx uses git root as project root)
3. Required **language grammar is installed** (`cx lang list` to check)

## Failure Modes & Recovery

### Error: `cx: unsupported file type: .md`
**Cause**: cx only parses source code, not markup/config files
**Fix**: Use `read` tool directly for .md/.yaml/.json files

### Error: `cx: database locked, waiting...`
**Cause**: Another cx process holds the index lock
**Fix**:
1. Wait 2-3 seconds and retry
2. If persistent: `cx cache clean` to reset
3. Last resort: kill stale cx processes

### Error: `cx: file not in index: <path>`
**Cause**: File not yet indexed (new file or outside project root)
**Fix**: Ensure file is within git root; cx auto-indexes on first query

### Error: `cx: missing grammar for <language>`
**Cause**: Language grammar not installed
**Fix**: `cx lang add <language>` (e.g., `cx lang add rust typescript`)

### Error: `cx: symbol not found: <name>`
**Cause**: Symbol doesn't exist or name is misspelled
**Fix**:
1. Try `cx symbols --name "*partial*"` with glob pattern
2. Check `cx overview <file>` to see available symbols
3. Verify spelling and case sensitivity

## Anti-Patterns (Don't Do This)

| ❌ Wrong | ✅ Right | Why |
|----------|----------|-----|
| `cx overview README.md` | `read README.md` | cx doesn't parse Markdown |
| `cx definition --name main` without context | `cx definition --name main --from src/app.py` | Ambiguous names need `--from` disambiguation |
| Reading full file before checking structure | `cx overview file.py` → then targeted `cx definition` | Saves 80%+ tokens |
| `cx symbols` with exact name | `cx symbols --name "*handler*"` | Use glob patterns for discovery |
| Ignoring `cx lang list` errors | Install missing grammars first | cx silently skips unsupported files |
| Using cx for YAML/JSON config | Use `read` or `grep` | cx only parses source code |

## Workflow Examples

### Example 1: Understand a new codebase
```bash
# Step 1: Find all functions
cx symbols --kind fn

# Step 2: Look at entry point
cx definition --name main --from src/main.py

# Step 3: Trace dependencies
cx references --name main
```

### Example 2: Safe refactoring
```bash
# Step 1: Find all usages before renaming
cx references --name old_function_name

# Step 2: Read the definition
cx definition --name old_function_name

# Step 3: Now edit with confidence
```

### Example 3: Debug a call chain
```bash
# Step 1: Find the error function
cx symbols --name "*error*" --kind fn

# Step 2: Get its definition
cx definition --name handle_error --from src/errors.py

# Step 3: Find who calls it
cx references --name handle_error
```

## 📚 Reference Documents

| Document | Purpose |
|----------|--------|
| `references/decision-tree.md` | Visual decision tree for when/how to use cx |
| `references/output-examples.md` | Real output samples from each command |

## Output Format Reference

See `references/output-examples.md` for real output samples from each command. Key points:
- Default format: **TOON** (compact, line-based)
- Use `--json` flag for machine-parseable JSON
- Line numbers are 1-indexed
- File paths are relative to git root

## Installation

Install from crates.io package **cx-cli**:

```bash
cargo install cx-cli
```

If `cx` reports a missing grammar:

```bash
cx lang add rust typescript python go
```

## 🛑 STOP: Limitations

- **Read-only**: cx cannot modify files, only navigate
- **Language support**: Limited to installed grammars (13 languages)
- **No markup parsing**: .md, .yaml, .json, .toml are unsupported
- **Git-dependent**: Uses git root as project boundary
- **Index latency**: New files may need a moment to appear in index

## 🔴 CHECKPOINT: Common Pitfalls

**Before running any cx command, verify:**

1. **File type check**: Is it a supported language? (not .md/.yaml/.json)
2. **Git root**: Are you in a git repository?
3. **Grammar installed**: Run `cx lang list` to verify language support
4. **Symbol name**: Use glob patterns (`*partial*`) for discovery, not exact names

**If command fails:**
- Check error message against "Failure Modes & Recovery" section
- Try `--json` flag for machine-parseable output
- Fall back to `read` tool if cx doesn't support the file type
