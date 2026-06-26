---
name: chinese-workdays
description: Calculate legal working days in China according to official government holiday schedules. Uses State Council-published arrangements to exclude weekends, public holidays, and include makeup workdays. Supports date ranges, months, quarters, and full years with automatic holiday calendar management.
license: MIT
---

# Chinese Workdays Calculator

Calculate the number of working days between two dates according to Chinese government holiday schedules.

## Features

- 📅 Uses official Chinese holiday schedules published by the State Council
- 🔢 Calculates法定工作日 (legal working days) excluding weekends and public holidays
- 📊 Supports holiday makeup workdays (调休补班)
- 🗂️ Stores yearly holiday schedules in simple YAML data files
- 🔄 Can be updated when new annual holiday arrangements are released
- 📊 Provides monthly and yearly statistics
- 🤖 CLI tool for quick calculations

## Quick Start

### Basic calculation
```python
from chinese_workdays import ChineseWorkdays

calc = ChineseWorkdays()
workdays = calc.count_workdays("2026-01-01", "2026-12-31")
print(f"2026年全年工作日: {workdays}天")
```

### Monthly statistics
```python
march_workdays = calc.get_workdays_in_month(2026, 3)  # 22天
```

## Usage Examples

```
How many working days are there in March 2026?
Working days in Q1 2026?
Calculate workdays between 2026-02-10 and 2026-03-20
How many workdays in 2026?
```

### Command Line

```bash
# Quick calculations
python workdays_cmd.py 2026-03          # March 2026
python workdays_cmd.py 2026-Q1          # Q1 2026
python workdays_cmd.py 2026             # Full year
python workdays_cmd.py 2026-01-01 2026-06-30  # Custom range
```

## Data Format

Holiday schedules are stored in YAML format in the `data/` directory:

```yaml
year: 2026
country: "China"
holidays:
  - name: "元旦"
    start: "2026-01-01"
    end: "2026-01-03"
    days_off: ["2026-01-01", "2026-01-02"]  #放假日期
    makeup_workdays: ["2025-12-28", "2026-01-04"]  # 调休上班
    note: "官方通知原文"
```

## Updating Schedules

The State Council releases next year's holiday arrangement in November. Update the YAML file accordingly:

1. Locate the official notice at `https://www.gov.cn/gongbao/`
2. Extract dates and makeup workdays
3. Edit `data/2027.yaml` (or the relevant year)

## Implementation Details

- Uses Python's `datetime` for date arithmetic
- Holiday data stored as YAML for easy editing
- Supports makeup workdays that override weekend status
- Handles holidays that span multiple days

## Limitations

- Requires holiday schedules to be defined for the years being calculated
- Only works for dates after 2000 (easily extendable)
- Does not automatically fetch new schedules (manual update needed)
- Data accuracy depends on correct YAML configuration

## Examples of Output

```
📅 工作日统计
📊 期间: 2026-01-01 至 2026-12-31
📏 总天数: 365
💼 法定工作日: 248 天

工作日占比: 68.0%

📋 期间包含的节假日:
  • 元旦: 2026-01-01 ~ 2026-01-03
  • 春节: 2026-02-15 ~ 2026-02-23
  ...
```

## Technical Notes

### Calculation Priority

1. **Makeup workdays** (highest priority) → always counted as working days
2. **Public holidays** → excluded from working days
3. **Weekends** (Saturday/Sunday) → excluded unless makeup workday
4. **Regular weekdays** → counted as working days

### Algorithm

```python
for each day in date_range:
    if day in makeup_workdays:
        count += 1
    elif day in public_holidays:
        skip
    elif day is weekend:
        skip
    else:
        count += 1
```

## Files Structure

```
chinese-workdays/
├── SKILL.md              # This file
├── __init__.py           # Package entry point
├── chinese_workdays.py   # Core calculation engine
├── workdays_cmd.py       # CLI tool
├── README.md             # User documentation (optional)
└── data/
    ├── 2026.yaml         # 2026 holiday schedule (official)
    └── 2027.yaml         # 2027 holiday schedule (template)
```

## License

MIT License - Free to use and modify.