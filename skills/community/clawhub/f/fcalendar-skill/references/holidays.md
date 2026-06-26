# Chinese Holidays and Solar Terms Reference

This document provides detailed information about Chinese public holidays, traditional festivals, and the 24 solar terms supported by fcalendar-skill.

## Chinese Public Holidays (中国法定节假日)

These are official public holidays in China with mandated time off.

### 1. 元旦 (New Year's Day)
- **Date**: January 1
- **Duration**: Typically 1-3 days
- **Description**: Celebrates the beginning of the Gregorian calendar year

### 2. 春节 (Spring Festival / Chinese New Year)
- **Date**: First day of the first lunar month (varies, usually late January to mid-February)
- **Duration**: Typically 7 days
- **Description**: The most important traditional Chinese festival, celebrating the lunar new year
- **Also known as**: 过年 (Guo Nian)

### 3. 清明节 (Qingming Festival / Tomb-Sweeping Day)
- **Date**: Around April 4-6 (based on solar calendar)
- **Duration**: Typically 3 days
- **Description**: A day to honor ancestors by visiting and cleaning their graves

### 4. 劳动节 (Labor Day / May Day)
- **Date**: May 1
- **Duration**: Typically 3-5 days
- **Description**: International Workers' Day, celebrating laborers and the working class

### 5. 端午节 (Dragon Boat Festival)
- **Date**: Fifth day of the fifth lunar month (varies, usually in June)
- **Duration**: Typically 3 days
- **Description**: Commemorates the ancient poet Qu Yuan, featuring dragon boat races and eating zongzi (rice dumplings)

### 6. 中秋节 (Mid-Autumn Festival / Moon Festival)
- **Date**: 15th day of the eighth lunar month (varies, usually in September)
- **Duration**: Typically 3 days
- **Description**: Celebrates the harvest and family reunion, featuring mooncakes and moon gazing

### 7. 国庆节 (National Day)
- **Date**: October 1
- **Duration**: Typically 7 days (Golden Week)
- **Description**: Celebrates the founding of the People's Republic of China in 1949

---

## Traditional Festivals (传统节日)

These are traditional Chinese festivals that may not be official public holidays but are culturally significant.

### 1. 元宵节 (Lantern Festival)
- **Date**: 15th day of the first lunar month
- **Description**: Marks the end of Spring Festival celebrations, featuring lantern displays and eating tangyuan (sweet rice balls)

### 2. 七夕 (Qixi Festival / Chinese Valentine's Day)
- **Date**: Seventh day of the seventh lunar month
- **Description**: Celebrates the annual meeting of the cowherd and weaver girl in Chinese mythology

### 3. 重阳节 (Double Ninth Festival)
- **Date**: Ninth day of the ninth lunar month
- **Description**: A day to honor the elderly, featuring hiking and eating chongyang cake

### 4. 除夕 (Chinese New Year's Eve)
- **Date**: Last day of the twelfth lunar month
- **Description**: The evening before Spring Festival, featuring family reunion dinners

---

## 24 Solar Terms (24节气)

The 24 solar terms are a traditional Chinese calendar system that divides the year into 24 periods based on the sun's position.

### Spring (春季)
1. **立春** (Lichun / Beginning of Spring) - ~February 3-5
2. **雨水** (Yushui / Rain Water) - ~February 18-20
3. **惊蛰** (Jingzhe / Awakening of Insects) - ~March 5-7
4. **春分** (Chunfen / Spring Equinox) - ~March 20-22
5. **清明** (Qingming / Pure Brightness) - ~April 4-6
6. **谷雨** (Guyu / Grain Rain) - ~April 19-21

### Summer (夏季)
7. **立夏** (Lixia / Beginning of Summer) - ~May 5-7
8. **小满** (Xiaoman / Grain Buds) - ~May 20-22
9. **芒种** (Mangzhong / Grain in Ear) - ~June 5-7
10. **夏至** (Xiazhi / Summer Solstice) - ~June 21-22
11. **小暑** (Xiaoshu / Minor Heat) - ~July 6-8
12. **大暑** (Dashu / Major Heat) - ~July 22-24

### Autumn (秋季)
13. **立秋** (Liqiu / Beginning of Autumn) - ~August 7-9
14. **处暑** (Chushu / End of Heat) - ~August 22-24
15. **白露** (Bailu / White Dew) - ~September 7-9
16. **秋分** (Qiufen / Autumn Equinox) - ~September 22-24
17. **寒露** (Hanlu / Cold Dew) - ~October 7-9
18. **霜降** (Shuangjiang / Descent of Frost) - ~October 23-24

### Winter (冬季)
19. **立冬** (Lidong / Beginning of Winter) - ~November 7-8
20. **小雪** (Xiaoxue / Minor Snow) - ~November 22-23
21. **大雪** (Daxue / Major Snow) - ~December 6-8
22. **冬至** (Dongzhi / Winter Solstice) - ~December 21-23
23. **小寒** (Xiaohan / Minor Cold) - ~January 5-7
24. **大寒** (Dahan / Major Cold) - ~January 20-21

---

## Western Festivals (西方节日)

fcalendar also supports common Western holidays:

### 1. 情人节 (Valentine's Day)
- **Date**: February 14

### 2. 复活节 (Easter)
- **Date**: Variable (first Sunday after the first full moon following the spring equinox)

### 3. 万圣节 (Halloween)
- **Date**: October 31

### 4. 感恩节 (Thanksgiving)
- **Date**: Fourth Thursday of November (US)

### 5. 圣诞节 (Christmas)
- **Date**: December 25

---

## Holiday Query Rules

When using the `fcalendar holiday` command:

### Included in Results
- ✅ **Chinese public holidays** (法定节假日): Official holidays with mandated time off
- ✅ **Normal weekends** (周末): Regular Saturday-Sunday weekends that are rest days

### Excluded from Results
- ❌ **Workdays on weekends** (调休上班): Weekends that are designated as workdays to compensate for extended holiday periods
- ❌ **Traditional festivals without time off**: Festivals like 元宵节, 七夕, 重阳节 (unless they coincide with official holidays)

### Scope Options

The `--scope` parameter determines the time range for holiday queries:

| Scope | Description | Example |
|-------|-------------|---------|
| `half_year` (default) | Next 180 days | All holidays in the next 6 months |
| `this_week` | Current week (Mon-Sun) | Holidays this week |
| `next_week` | Next week (Mon-Sun) | Holidays next week |
| `next_month` | Next calendar month | All holidays in the next month |
| `weeks=N` | Next N weeks | Holidays in the next 3 weeks |
| `months=N` | Next N months | Holidays in the next 2 months |

### Output Format

Results are returned as a JSON array sorted by start date:

```json
[
  {
    "type": "holiday",
    "name": "劳动节",
    "start": "2026-05-01",
    "end": "2026-05-05",
    "days": 5
  },
  {
    "type": "weekend",
    "name": "周末",
    "start": "2026-05-09",
    "end": "2026-05-10",
    "days": 2
  }
]
```

**Field Descriptions**:
- `type`: Either `"holiday"` (public holiday) or `"weekend"` (normal weekend)
- `name`: Name of the holiday or "周末" for weekends
- `start`: Start date in ISO format (YYYY-MM-DD)
- `end`: End date in ISO format (YYYY-MM-DD)
- `days`: Number of days in the holiday period

---

## Important Notes

1. **Lunar Calendar Variations**: Dates for lunar-based holidays vary each year in the Gregorian calendar
2. **Government Adjustments**: Actual holiday schedules may be adjusted by government announcements
3. **Workday Compensation**: Extended holidays often require working on adjacent weekends (调休), but these workdays are NOT included in the holiday query results
4. **Regional Differences**: Some regions may have additional local holidays not covered by this tool

---

## See Also

- [time-expressions.md](time-expressions.md) - Detailed information about time expression types
- [SKILL.md](../SKILL.md) - Main skill documentation with usage examples
