---
name: chinese-holidays
description: >
  Query Chinese statutory holidays, check if a date is a working day/holiday, 
  and get holiday schedules. Use when the user asks about Chinese holidays, 
  working days, statutory holidays, or needs to know if a specific date is 
  a holiday in China. Supports queries like "Is tomorrow a holiday?", 
  "When is Spring Festival?", "Is May 1st a working day?".
---

# Chinese Holidays

Query Chinese statutory holidays and working day status.

## Quick Start

```bash
python scripts/holidays.py today
python scripts/holidays.py check 2025-01-01
python scripts/holidays.py list 2025
```

## Commands

### `today` — Check today's status

Check if today is a working day, holiday, or weekend.

```bash
python scripts/holidays.py today
```

Output:
```
2025-01-01 (Wednesday)
Status: HOLIDAY - New Year's Day (元旦)
```

### `check <date>` — Check specific date

Check if a specific date is a working day or holiday.

```bash
python scripts/holidays.py check 2025-02-10
```

Output:
```
2025-02-10 (Monday)
Status: HOLIDAY - Spring Festival (春节)
```

### `list <year>` — List all holidays in a year

List all statutory holidays for a given year.

```bash
python scripts/holidays.py list 2025
```

Output:
```
=== 2025 Chinese Statutory Holidays ===

1. New Year's Day (元旦)
   2025-01-01

2. Spring Festival (春节)
   2025-01-28 to 2025-02-04 (8 days)

3. Qingming Festival (清明节)
   2025-04-04 to 2025-04-06 (3 days)

4. Labor Day (劳动节)
   2025-05-01 to 2025-05-05 (5 days)

5. Dragon Boat Festival (端午节)
   2025-05-31 to 2025-06-02 (3 days)

6. Mid-Autumn Festival (中秋节)
   2025-10-06 (1 day, combined with National Day)

7. National Day (国庆节)
   2025-10-01 to 2025-10-07 (7 days)
```

### `next` — Find next holiday

Find the next upcoming holiday.

```bash
python scripts/holidays.py next
```

Output:
```
Next holiday: Spring Festival (春节)
Date: 2025-01-28 to 2025-02-04
Days until: 15 days
```

## Return Codes

| Code | Meaning |
|------|---------|
| 0 | Working day |
| 1 | Weekend |
| 2 | Statutory holiday |
| 3 | Adjusted working day (调休) |

## Data Source

Holiday data is based on official announcements from the State Council of China (国务院办公厅). The script includes:

- Statutory holiday dates
- Adjusted working days (调休)
- Holiday names in Chinese and English

## Notes

- Adjusted working days (调休) are weekends that become working days due to holiday adjustments
- Some holidays may change based on official announcements - data is updated annually
- Supports dates from 2024 onwards
