---
name: chinese-calendar
description: Calculate Chinese lunar calendar dates with Heavenly Stems (天干) and Earthly Branches (地支). Use when generating Chinese calendar tables, checking 黄历, or converting Gregorian dates to 干支 (stem-branch) dates for year/month/day.
---

# Chinese Calendar Calculator

## Usage

Run the script to generate weekly calendar:

```bash
python3 scripts/calendar.py
```

Output format:
```
丙午(马年) 🐎
| Date | Weekday | Nongli | 月天干地支 | 日天干地支 |
| ---- | ------- | ------ | ---------- | ---------- |
| 3月6日 | 周五 | 农历正月十八 | 辛卯月 | 己卯日 |
```

## Calculation Method

### Reference Date
- **1983-02-05 = 甲子日** (calibrated against verified sources)
- Day stem-branch: `(days since reference) % 60` → stem = pos % 10, branch = pos % 12

### Day Calculation
```
delta = (date - 1983-02-05).days
stem_idx = delta % 10
branch_idx = delta % 12
day_stem_branch = STEMS[stem_idx] + BRANCHES[branch_idx]
```

### Month Calculation
Month branches: 正月=寅, 二月=卯, 三月=辰...
```
month_branch_idx = (month + 1) % 12
month_stem_idx = (year_stem_idx * 2 + month) % 10
month_stem_branch = STEMS[month_stem_idx] + BRANCHES[month_branch_idx]
```

### Year Calculation
```
cycle_pos = (year - 4) % 60
year_stem_idx = cycle_pos % 10
year_branch_idx = cycle_pos % 12
year_stem_branch = STEMS[year_stem_idx] + BRANCHES[year_branch_idx]
```

## Constants

```python
STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
ZODIAC = {
    '子': '鼠', '丑': '牛', '寅': '虎', '卯': '兔',
    '辰': '龙', '巳': '蛇', '午': '马', '未': '羊',
    '申': '猴', '酉': '鸡', '戌': '狗', '亥': '猪'
}
```
