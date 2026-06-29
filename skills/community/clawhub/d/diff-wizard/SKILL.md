---
name: diff-wizard
display_name: Diff Wizard / 文本对比精灵
description: "Smart text comparison tool with format-aware diffing, AI explanation, and 3-way merge. Covers structured JSON, YAML, CSV, code, and plain text."
metadata:
  category: Developer Tools
  priority: P1
  languages: en, zh-CN
  model: deepseek
  tags:
    - diff
    - compare
    - merge
    - text-processing
    - developer-tools
---

# Diff Wizard (diff-wizard)

Smart text comparison beyond traditional `diff` / `git diff`. Detects semantic differences in JSON, YAML, CSV, code, and plain text with format-aware comparison strategies, AI-powered natural-language explanations, and 3-way merge conflict resolution.

## Quick Start

```bash
clawhub run diff-wizard --help           # Show usage
clawhub run diff-wizard a.json b.json    # Compare two files
clawhub run diff-wizard --paste           # Paste content to compare
clawhub run diff-wizard --merge base ours theirs  # 3-way merge
clawhub run diff-wizard ./dir-a/ ./dir-b/         # Compare directories
```

## First-Success Path

```
Step 1: Install → clawhub install diff-wizard
Step 2: Run → clawhub run diff-wizard file-v1.json file-v2.json
Step 3: See diff → Color-coded terminal output with AI explanation (<10 seconds)
Step 4: Explore → Try --paste mode for clipboard-based comparison
```

## Features

| Feature | Description |
|---------|-------------|
| **Format-aware diffing** | Auto-detect JSON, YAML, CSV, TOML, code, text, XML/HTML — applies optimal comparison strategy per format |
| **Structured comparison** | Field-level diff for JSON/YAML, row/column for CSV, semantic diff for code, DOM for XML |
| **Terminal color output** | 🟢 green (added), 🔴 red (deleted), 🟡 yellow (modified) with side-by-side or unified format |
| **AI explanation** | LLM-powered natural-language explanation of complex diffs, configurable language (zh-CN/en-US) |
| **3-way merge** | `base` + `ours` + `theirs` merge with conflict markers, AI merge suggestions per conflict |
| **Directory diff** | Recursive directory comparison with aggregate stats and per-file diff reports |
| **Multiple output formats** | Terminal, unified diff, markdown, HTML, JSON |
| **Security first** | Local-only processing, sensitive file detection, credential redaction, path traversal protection |

## Input Modes

### File Comparison
```bash
clawhub run diff-wizard config-v1.json config-v2.json
clawhub run diff-wizard --ignore-whitespace old.js new.js
clawhub run diff-wizard --output markdown --context-lines 5 a.yaml b.yaml
```

### Paste Mode (interactive)
```bash
clawhub run diff-wizard --paste
```

### Directory Comparison
```bash
clawhub run diff-wizard ./env/dev/ ./env/staging/ --exclude "node_modules,.git,*.log"
clawhub run diff-wizard ./config-v1/ ./config-v2/ --recursive --sort
```

### 3-Way Merge
```bash
clawhub run diff-wizard --merge base.json ours.json theirs.json
clawhub run diff-wizard --merge --auto-resolve --output merged.ts base.ts ours.ts theirs.ts
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--format` | auto | Force format: json, yaml, csv, toml, xml, code, text |
| `--output` | terminal | Output: terminal, unified, side-by-side, markdown, html, json |
| `--context-lines` | 3 | Context lines around diffs (0-99) |
| `--ignore-whitespace` | false | Ignore whitespace-only changes |
| `--ignore-case` | false | Ignore case differences |
| `--ignore-comments` | false | Ignore comment changes |
| `--sort-keys` | false | Sort JSON/YAML keys before comparison |
| `--ai-explain` | true | Enable/disable AI explanation |
| `--ai-language` | auto | AI explanation language: zh-CN, en-US |
| `--detail-level` | normal | Diff granularity: summary, normal, detailed |
| `--color` | true | Terminal color output |
| `--no-color` | false | Disable color output |
| `--exclude` | — | Exclude patterns (comma-separated, for dir mode) |
| `--max-depth` | 99 | Max directory recursion depth |
| `--auto-resolve` | false | Auto-resolve non-conflicting 3-way merges |
| `--strategy` | manual | Conflict strategy: ours, theirs, manual |

## Error Codes

| Code | Scenario | Handling |
|------|----------|----------|
| E001 | File not found | Show nearest match via Levenshtein |
| E002 | File exceeds size limit | Show file size + max_file_size_mb setting |
| E003 | Permission denied | Show permission error + fix suggestion |
| E004 | Empty input | Show error + usage example |
| E005 | Format detection failure | Fallback to plain text + warning |
| E006 | Parse error | Show precise location (line:col) + error reason |
| E007 | AI explanation failure | Skip AI, still return diff |
| E008 | 3-way merge conflict overflow | List conflicts + AI suggestions |
| E009 | Directory scan read failure | Skip file + annotate in report |
| E010 | CSV parse failure | Fallback to plain text diff |
| E011 | Encoding detection failure | Try UTF-8 / GBK / UTF-16 fallback |

## Sample Prompts

### 1. Quick file comparison
```bash
clawhub run diff-wizard before.json after.json
```
**Expected output:**
```
📄 Comparing before.json ↔ after.json  (format: json)

🔴 removed: "deprecated_field"
🟢 added:   "new_feature_enabled": true
🟡 changed: "version": "1.0.0" → "2.0.0"
🟡 changed: "timeout_ms": 5000 → 30000

📊 Summary: 1 removed, 1 added, 2 changed
💡 AI: "Version bumped from 1.0 to 2.0, deprecated_field removed,
       new_feature_enabled added, timeout increased 6x."
```

### 2. Paste mode
```bash
clawhub run diff-wizard --paste
```
**Expected output:**
```
📋 Paste Mode — paste the first text block, press Enter, then Ctrl+D
[Paste content A...]
📋 Now paste the second text block, press Enter, then Ctrl+D
[Paste content B...]

🔴 removed: line 3
🟢 added:   line 7
🟡 changed: line 5 "old" → "new"
📊 3 differences found
```

### 3. 3-way merge with AI suggestions
```bash
clawhub run diff-wizard --merge base.ts ours.ts theirs.ts --ai-explain
```
**Expected output:**
```
🔀 3-Way Merge: base ← ours + theirs

✅ Auto-resolved (2): type User struct, import statement
⚠️  Conflicts (1):
  [ours]   name: string = "Alice"
  [theirs] username: string = "Bob"
  💡 AI suggests: "Prefer 'name' and merge both values with configurable default"

📄 Merged written to: merged.ts
```

### 4. Directory batch comparison
```bash
clawhub run diff-wizard ./env/dev/ ./env/staging/ --exclude "node_modules,.git,*.log"
```
**Expected output:**
```
📁 Comparing ./env/dev/ ↔ ./env/staging/ (recursive)

🔴 Only in dev/:    local-overrides.yaml
🟢 Only in staging/: production-secrets.yaml
🟡 Modified: config.yaml (12 changes)
🟡 Modified: docker-compose.yaml (3 changes)
✅ Unchanged: 47 files

📊 Summary: 2 added, 1 removed, 2 modified, 47 unchanged
```

### 5. CSV data diff
```bash
clawhub run diff-wizard --format csv --output terminal prices-q1.csv prices-q2.csv
```
**Expected output:**
```
📊 Comparing prices-q1.csv ↔ prices-q2.csv  (format: csv, 142 rows)

🟢 Added rows (3):
  | SKU-109 | Widget Pro | $29.99 |
  | SKU-110 | Widget Max | $49.99 |
  | SKU-111 | Widget Lite | $12.99 |

🔴 Removed rows (1):
  | SKU-042 | Old Widget | $9.99 |

🟡 Modified cells (7):
  Row 23: $19.99 → $21.99
  Row 56: $15.00 → $16.50
  Row 78: "Widget" → "Widget v2"
  ... (4 more)

📊 Summary: 3 added, 1 removed, 7 cell changes, 132 unchanged
```

## Implementation Notes

- **Diff algorithm**: Myers diff (O(ND)) for text; recursive DFS with key alignment for structured formats
- **Format detection priority**: Extension → content signature → MIME → fallback to text
- **AI explanation**: Only diff hunks (max 4000 chars) sent to LLM; credential patterns auto-redacted
- **Sensitive file protection**: `.env`, `credentials.*`, `*secret*`, `*.pem`, `*.key`, `id_rsa*`
- **Path security**: Prevents traversal attacks; restricted to working directory unless `--allow-system`
- **All processing is local**: Uses configured LLM for AI explanation, no external content sharing

## Safety

- Never sends raw file content to external services
- Sensitive files trigger confirmation prompts before comparison
- AI explanation hunks are redacted for credential patterns
- HTML output sanitizes user content (HTML entity escaping)
- Terminal output filters malicious ANSI escape sequences
- Audit logs record AI explanation requests (path + timestamp only)
