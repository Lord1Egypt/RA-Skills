---
name: daily-report-generator
version: "1.8.0"
description: "Generate daily and weekly work reports in Markdown from JSON data."
metadata:
  openclaw:
    emoji: "📊"
    category: productivity

Generate structured Markdown work reports (daily or weekly) from JSON input data.

## Usage

```bash
python3 scripts/generate_report.py --type daily
python3 scripts/generate_report.py --type weekly
python3 scripts/generate_report.py --type daily --date 2026-04-10
python3 scripts/generate_report.py --data my_data.json
```

## Data format

Optional JSON file with completed/in_progress/planned/risks/metrics fields.
If no data file is provided, an empty template is generated.

## Options

- `--type` daily or weekly
- `--date` target date YYYY-MM-DD
- `--data` path to JSON data file
- `--output` doc/chat/both

## Requirements

Python 3.7+, no external dependencies (stdlib only).

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
