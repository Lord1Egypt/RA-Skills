---
name: disk-space-analyzer
description: >
  磁盘空间分析与优化建议工具。自动扫描所有磁盘驱动器，生成包含目录占用排名、
  爆满元凶锁定、可清理缓存识别和优化建议的完整报告。
  触发词: 磁盘空间分析、C盘满了、硬盘空间不足、磁盘爆满、磁盘占用、磁盘分析、
  磁盘清理、C盘空间、磁盘空间报告、扫描磁盘、disk space、磁盘满了、磁盘空间不够、
  帮我看看磁盘、磁盘空间分析工具、清理磁盘空间、磁盘瘦身
---

# Disk Space Analyzer

扫描用户所有磁盘驱动器，生成专业的空间分析报告（HTML）。

## Workflow

### Phase 1: Scan

Run the bundled scanner script to collect disk usage data:

```bash
python scripts/disk_scan.py --top 10 --deep --output <output_path>
```

- `--top N`: Number of top directories per drive (default 10)
- `--deep`: Deep-trace the top 3 directories on each drive, recursively following the largest child up to 5 levels deep to find the true culprit
- `--output`: Save JSON to file (recommended for large reports)
- Output: JSON with per-drive data, progress to stderr

Read the JSON output. Key fields:
- `drives[]`: Per-drive overview with `top_directories`
- `drives[].deep_consumers[]`: Top 3 dirs with their children + `culprit_trace` (recursive deep trace result with `chain`, `leaf`, `breadcrumb`)
- `special_locations`: Cache/temp locations across all drives
- `windows_components`: C:\Windows subfolder breakdown

### Phase 2: Generate Report

Create an HTML report by:

1. Read the scan JSON data
2. Copy `assets/report_template.html` to the workspace as the HTML output file
3. Replace `__REPORT_DATA__` in the HTML with the raw JSON string from `json.dumps(data, ensure_ascii=False, separators=(',',':'))`
4. The HTML template uses `const REPORT_DATA = __REPORT_DATA__;` — JSON is injected directly as a JS object literal, no parsing needed
5. Deliver the HTML file and preview it

⚠️ **Simply replace `__REPORT_DATA__` with the raw JSON output. Do NOT add any extra escaping.**

Python snippet for report generation:
```python
import json

with open(scan_json_path, encoding='utf-8') as f:
    data = json.load(f)

with open(template_path, encoding='utf-8') as f:
    html = f.read()

json_str = json.dumps(data, ensure_ascii=False, separators=(',',':'))
html = html.replace('__REPORT_DATA__', json_str)

with open(output_html_path, 'w', encoding='utf-8') as f:
    f.write(html)
```

### Phase 3: Present & Advise

After showing the visual report, provide a text summary to the user:

1. **每个盘元凶锁定**: Every drive gets a culprit alert — the deep tracer recursively follows the largest child directory up to 5 levels to find the true space hog (e.g., `Program Files → NetEase → MuMu → vms`)
2. **追踪路径可视化**: Show the breadcrumb path of how the culprit was traced
3. **前3目录深度分析**: Show children breakdown for each drive's top 3 directories
4. **可清理项**: List safe-to-clean caches and temp files with total savings
5. **优化建议**: Actionable recommendations ordered by impact

#### Suggestion Rules

- If a directory exceeds **30%** of drive used space, flag it as the primary culprit
- For Windows systems, note `WinSxS` is not safe to manually delete; recommend `Dism /Online /Cleanup-Image /StartComponentCleanup`
- For MuMu/Android emulators, recommend migrating VM storage to another drive
- For cache/temp files, confirm with user before deleting (show the list first)

### Edge Cases

- If a drive scan fails (permission denied), skip and note it
- On non-Windows systems, the `special_locations` scan will simply find fewer items
- If only one drive exists, still run the full workflow
