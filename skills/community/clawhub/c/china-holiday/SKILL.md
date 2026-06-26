---
name: china-holiday
description: 中国大陆日历服务 - 识别法定节假日、周末、调休，各地寒暑假、春秋假
homepage: https://github.com/your-repo/china-holiday
metadata: {"clawdbot":{"emoji":"📅","requires":{"bins":["python3"]}}}
---

# China Holiday

中国大陆日历服务，判断任意日期的假期状态。

## 功能

- **法定节假日**：元旦、春节、清明、五一、端午、中秋、国庆
- **调休**：识别补班日
- **周末**：自动识别周六日
- **寒暑假**：支持主要城市
- **春秋假**：部分地区

## 使用示例

```bash
# 判断今天是否上班
python holiday.py today

# 判断指定日期
python holiday.py 2026-01-01

# 查询北京暑假时间
python holiday.py vacation 北京

# 查询某年所有节假日
python holiday.py list 2026
```

## API 调用

```python
from holiday import is_holiday, is_workday, get_holiday_name

# 判断是否为假日
is_holiday("2026-01-01")  # True (元旦)

# 判断是否上班
is_workday("2026-01-28")  # True (春节前调休)

# 获取假日名称
get_holiday_name("2026-01-01")  # "元旦"
```

## 支持城市

- 北京、上海、广州、深圳
- 更多城市陆续添加...
