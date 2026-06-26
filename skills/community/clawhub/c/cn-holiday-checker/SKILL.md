# 中国节假日助手 (cn-holiday-checker) / Chinese Holiday Assistant (cn-holiday-checker)

该技能用于查询中国节假日、调休安排及工作日判定。
This skill is used for querying Chinese holidays, work-shift arrangements, and workday determination.

## 功能说明 / Functionality
- **节假日识别 / Holiday Recognition**：支持多文件数据源，自动合并解析 `data/` 目录下的所有 `.ics` 文件。 / Supports multi-file data sources; automatically merges and parses all `.ics` files in the `data/` directory.
- **跨日事件处理 / Cross-day Event Processing**：支持处理具有 `DTSTART` 和 `DTEND` 的持续性事件，不再仅限于单日标记。 / Supports processing continuous events with `DTSTART` and `DTEND`, no longer limited to single-day markers.
- **自动判定 / Automatic Determination**：优先匹配节假日/调休事件；若无匹配，则根据自然周（周一至周五工作日，周六至周日休息日）进行判定。 / Prioritizes matching holiday/work-shift events; if no match, determines based on the natural week (Mon-Fri as workday, Sat-Sun as rest day).
- **自动更新 / Automatic Update**：通过 `cron` 定时任务每月自动拉取最新日历数据。 / Automatically pulls the latest calendar data monthly via `cron`.

## 环境要求 / Requirements
- Python 3.x
- 已安装依赖 / Installed dependencies: `requests`, `icalendar`

## 使用方法 / Usage

### 1. 查询指定日期 / Query a specific date
支持通过 `--date` 参数传入日期（格式为 YYYY-MM-DD），若不传入则默认使用当天日期：
Supports querying a specific date via the `--date` parameter (format: YYYY-MM-DD); defaults to today if not provided:
```bash
python3 cn-holiday-checker/scripts/holiday_checker.py --date "2026-03-19"
```

### 2. 手动更新数据 / Manual Data Update
如果需要立即更新节假日数据，请运行：
If you need to update holiday data immediately, please run:
```bash
python3 cn-holiday-checker/scripts/download_ics.py
```

## 配置说明 (config.json) / Configuration (config.json)
- 存放技能相关的环境变量。 / Stores environment variables related to the skill.
- 支持 `PRIMARY_URL` (主数据源) 与 `BACKUP_URL` (备用数据源)。 / Supports `PRIMARY_URL` and `BACKUP_URL` (backup data source).
- 脚本会自动向上回溯识别 `config.json` 文件，确保迁移目录后配置依然有效。 / The script automatically traces upward to identify the `config.json` file, ensuring configuration remains valid after migrating the directory.
