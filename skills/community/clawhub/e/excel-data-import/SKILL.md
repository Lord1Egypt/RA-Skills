---
name: excel-data-import
description: >
  Import, merge, and transform data from Excel (.xlsx/.csv) files using YAML-driven configuration.
  Use when the user asks to: (1) import data from Excel/CSV into a template,
  (2) batch-process multiple files in a directory, (3) merge/consolidate data from multiple sources,
  (4) map and transform columns with validation rules, (5) do incremental data updates on existing spreadsheets.
  当用户要求导入Excel、CSV导入、表格数据导入、Excel数据合并、批量处理Excel、字段映射、数据校验、
  表头自动检测、增量更新Excel、多sheet合并时使用此技能。
  Supports Chinese field names, multi-layer merged cell headers, auto header detection,
  CSV (auto-encoding), custom validators, and multi-source imports.
---

# Excel Data Import

Configuration-driven data import from Excel and CSV files with field mapping, validation, and batch processing.

## Prerequisites

- Python 3.8+
- **Required**: `pip3 install openpyxl pyyaml`
- **Optional**: `pip3 install python-calamine` (for .xls legacy format)

## Quick Start

```yaml
# import_config.yaml
task_name: "人员信息导入"
source:
  file_path: "data/source.xlsx"
  sheet_name: "Sheet1"
  header_row: 1
  key_field: "身份证号"
target:
  file_path: "output/result.xlsx"
  sheet_name: "人员信息"
  header_row: 2
  data_start_row: 3
field_mappings:
  - source: "姓名"
    target: "员工姓名"
    required: true
  - source: "身份证号"
    target: "身份证号码"
    required: true
    validate: "id_card"
  - source: "部门"
    target: "所属部门"
    default: "待分配"
error_handling:
  backup: true
```

```bash
python3 scripts/excel_import.py import_config.yaml
python3 scripts/excel_import.py import_config.yaml --dry-run   # preview only
```

## Import Modes

| Mode | Source Config | Use Case |
|------|--------------|----------|
| Single file | `source.file_path` | One-to-one import |
| Directory batch | `source.type: "directory"` | Process all files in a folder |
| Multi-source | `sources: [...]` | Merge from multiple files |
| CSV | `.csv` file_path | Auto-encoding detection (UTF-8/GBK/GB2312) |
| Legacy .xls | `.xls` file_path | Requires `python-calamine` |
| Auto header | `header_row: "auto"` | Detect header in complex sheets |

For full parameter docs, see [data-mapping-guide.md](references/data-mapping-guide.md).

## Key Features

- **Incremental update**: Match by `key_field`, update existing or append new rows
- **Multi-layer merged headers**: Auto-detect and expand merged cell values
- **Validation rollback**: Failed rows are skipped entirely (no partial writes)
- **Source deduplication**: Duplicate keys across files are merged
- **Auto-create target**: Template generated from field_mappings if missing

## Built-in Transforms & Validators

**Transforms**: `strip`, `upper`, `lower`, `title`, `int`, `float`, `date`

**Validators**: `required`, `not_empty`, `id_card`, `phone`, `email`, `numeric`, `range`, `regex`, `length`

For advanced usage, see [advanced-features.md](references/advanced-features.md).

## CLI Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview mode, no file writes |
| `--verbose` | Detailed per-record output |
| `--no-backup` | Skip target file backup |

## Reference Documents

- **Data Mapping Guide**: [data-mapping-guide.md](references/data-mapping-guide.md) — field mapping, transforms, validators
- **Advanced Features**: [advanced-features.md](references/advanced-features.md) — multi-source, batch, auto-header
- **Auto Header Detection**: [auto_header_detection.md](references/auto_header_detection.md) — complex header detection
- **Quickstart**: [quickstart.md](references/quickstart.md) — step-by-step tutorial
- **Workflow**: [workflow.md](references/workflow.md) — detailed execution flow
- **Best Practices**: [best_practices.md](references/best_practices.md) — usage recommendations
- **Error Handling**: [error-handling.md](references/error-handling.md) — error codes and recovery
- **Troubleshooting**: [troubleshooting.md](references/troubleshooting.md) — common issues

## Workflow

1. Read user's import requirements and source/target file info
2. Create or adjust YAML config file
3. Run `python3 scripts/excel_import.py <config.yaml>` with `--dry-run` first
4. Review output, fix issues, then run without `--dry-run`
5. Check the JSON report alongside the output file
