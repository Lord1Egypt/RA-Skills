---
name: csv-tools
description: |
  CSV 工具集 v1.1.0 — 子命令+安全增强。
  预览、筛选、排序、合并、分割、去重、验证、统计、
  列操作(重命名/选择/计算列)、类型检测、数据画像、抽样。
  纯Python标准库(csv模块)，无外部依赖。

  Use when:
  - 需要快速处理CSV文件（预览/筛选/排序/统计）
  - 合并多个CSV文件或分割大CSV文件
  - CSV数据去重、列操作、类型检测、数据画像

  Do NOT use when:
  - 非CSV格式数据（JSON/YAML/Excel/数据库）
  - 需要写回原始输入文件
  - 简单的数据查看（推荐用 cat/head 等系统命令）

  🎉 v1.1.0 新增子命令:
  - stats — 列统计(sum/avg/min/max/std/中位数)
  - columns — 列操作(重命名/选择/添加计算列)
  - detect — 数据类型自动检测
  - profile — 数据画像(缺失率条形图/唯一值/分布)
  - sample — 随机抽样(head/tail/random/systematic)

  v1.0.0 子命令:
  - preview / filter / sort / merge / split / dedup / validate

  触发关键词：CSV文件操作、CSV格式转换、CSV数据清洗、CSV合并拆分、CSV验证统计
  Do not trigger for: 非CSV格式数据处理、数据库操作、JSON/YAML/XML处理、图片处理
  适用范围：CSV / TSV 格式数据文件
  运行模式：纯本地，无网络请求 ❎
  外部依赖：Python标准库（无需额外安装）
---

# 📊 CSV Tools v1.1.0

## Overview
12个子命令覆盖日常CSV数据处理的完整工作流——从预览、筛选、排序到统计、类型检测、数据画像和抽样。所有操作基于Python标准库csv模块，无需安装任何第三方依赖。

## Usage

### stats — 列统计 (NEW)
```bash
python3 scripts/csv_tools.py stats data.csv

# 📊 Column Statistics — data.csv
#    [amount] — 数值列
#      计数: 1000 | 空: 0 | 总和: 485,230.00
#      平均: 485.23 | 中位: 320.00
#      最小: -8,500.00 | 最大: 25,000.00 | 标准差: 1,234.56
#    [name] — 文本列
#      非空: 980 | 空: 20 | 唯一值: 450
#      最常见: "张三" (15次)
```

### columns — 列操作 (NEW)
```bash
# 重命名 + 选择列
python3 scripts/csv_tools.py columns data.csv \
  --rename "old_name=new_name" --select "id,name,amount"

# 添加计算列
python3 scripts/csv_tools.py columns data.csv \
  --add "total=price * quantity" --output result.csv
```

### detect — 类型检测 (NEW)
```bash
python3 scripts/csv_tools.py detect --verbose data.csv

# 🔎 Data Type Detection — data.csv
#    [amount] → 浮点数(Float)
#    [date] → 日期(Date)
#    [is_active] → 布尔(Boolean)
#    [name] → 文本
```

### profile — 数据画像 (NEW)
```bash
python3 scripts/csv_tools.py profile data.csv

# 📋 Data Profile — data.csv
#    Rows: 1000 | Columns: 8
#    [email]
#      非空: 850 / 1000 (████████████████████ 15% 缺失)
#      唯一值: 830 (98%)
#      最常见: "user@example.com"(3), ...
```

### sample — 随机抽样 (NEW)
```bash
# 随机抽10条
python3 scripts/csv_tools.py sample data.csv --n 10 --method random

# 等距抽50条
python3 scripts/csv_tools.py sample data.csv --n 50 --method systematic --output sample.csv
```

### 原有命令
```bash
python3 scripts/csv_tools.py preview data.csv
python3 scripts/csv_tools.py filter data.csv --where "status=active"
python3 scripts/csv_tools.py sort data.csv --by "date" --desc
python3 scripts/csv_tools.py merge a.csv b.csv --output merged.csv
python3 scripts/csv_tools.py split data.csv --chunk-size 1000
python3 scripts/csv_tools.py dedup data.csv --on "email"
python3 scripts/csv_tools.py validate data.csv
```

## Use Cases
- **数据导入前清洗**: dedup + validate + sort
- **ETL管线**: split 大文件 → merge 多个源 → stats 检查分布
- **数据质量审计**: profile 检查缺失率 → detect 确认类型
- **探索性分析**: preview 快速查看 → stats 列统计 → sample 抽样

## Security
### Usage Boundaries
- This skill is designed for **CSV files only** — CSV, TSV, and pipe-delimited text
- It should NOT be used for non-tabular text, binary files, or structured data in other formats
- Input files must be explicitly specified by the user — no auto-scanning
- For simple data inspection (e.g. view first 5 rows), system tools (cat/head) are preferred

### Declared Capabilities
| Script | Purpose | Input | Output | Network | Filesystem Write | Constraints |
|--------|---------|-------|--------|---------|-----------------|-------------|
| csv_tools.py | CSV读写操作 | File path(s) or stdin | CSV file / JSON / stdout | No | Yes (user-specified paths only) | Writes only to --output paths; never modifies input files; no overwrite without explicit user confirmation |

### Explicitly Denied
- ❌ No network access (no HTTP, socket, or API calls)
- ❌ No arbitrary code execution via exec()/eval() (使用安全数学解析器，无 eval)
- ❌ No system commands via subprocess/shell
- ❌ No telemetry or usage reporting
- ❌ No auto-writes to input files (only writes to --output paths)
- ❌ No writes outside the working directory without user confirmation
- ❌ No file deletion or modification of existing data

### Permission Boundaries
- All write operations go to user-specified `--output` paths only
- Input files are read-only; never modified
- Default output is stdout when no `--output` is specified
- Temporary files (if any) are cleaned up after operation
- All scripts require explicit user-provided file paths — no auto-scanning of filesystem
