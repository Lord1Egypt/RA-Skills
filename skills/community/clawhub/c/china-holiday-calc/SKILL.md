---
name: china-holiday-calc
description: Chinese mainland calendar service - identifies法定节假日, weekends, makeup workdays, and supports city-specific vacations
license: MIT
---

# China Holiday

中国大陆日历服务，判断任意日期的假期状态。

## Features

- **法定节假日**: 元旦、春节、清明、五一、端午、中秋、国庆
- **调休**: 识别补班日
- **周末**: 自动识别周六、周日
- **寒暑假**: 支持主要城市
- **春秋假**: 部分地区学校

## Usage

```bash
# Check if today is a holiday
python holiday.py today

# Check specific date
python holiday.py 2026-01-01

# Query Beijing summer vacation
python holiday.py vacation 北京

# List all holidays for a year
python holiday.py list 2026
```

## API

```python
from holiday import is_holiday, is_workday, get_holiday_name

# Check if holiday
is_holiday("2026-01-01")  # True (New Year's Day)

# Check if workday
is_workday("2026-01-28")  # True (Spring Festival makeup workday)

# Get holiday name
get_holiday_name("2026-01-01")  # "元旦"
```

## Supported Cities

- Beijing, Shanghai, Guangzhou, Shenzhen
- More cities to be added...

## Implementation

Uses official Chinese government holiday schedules with local variations for schools and universities.

## License

MIT License