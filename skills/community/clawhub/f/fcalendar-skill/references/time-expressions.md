# Time Expression Types Reference

This document provides detailed information about all time expression types supported by fcalendar-skill.

## 1. Relative Day Expressions (相对日期表达)

**Description**: Expressions that refer to days relative to today.

**Supported Forms**:
- 明天 (tomorrow)
- 后天 (day after tomorrow)
- 大后天 (two days after tomorrow)
- 大大后天 (three days after tomorrow)
- And further stacking patterns

**Examples**:
- "明天下午三点开会" → resolves to tomorrow's date
- "后天去旅游" → resolves to the day after tomorrow
- "大后天有活动" → resolves to two days after tomorrow

---

## 2. Relative Week Expressions (相对周表达)

**Description**: Expressions that refer to specific weekdays in current or future weeks.

**Supported Forms**:
- 本周一, 本周二, ..., 本周日 (this Monday, this Tuesday, ..., this Sunday)
- 下周一, 下周二, ..., 下周日 (next Monday, next Tuesday, ..., next Sunday)
- 下下周一, 下下周二, ..., 下下周日 (the week after next Monday, ...)

**Examples**:
- "本周五开会" → resolves to this Friday's date
- "下周一提交报告" → resolves to next Monday's date
- "下下周三有培训" → resolves to the Wednesday of the week after next

---

## 3. Weekend Expressions (周末表达)

**Description**: Expressions referring to weekends.

**Supported Forms**:
- 本周末 (this weekend)
- 下周末 (next weekend)
- 下下周末 (the weekend after next)

**Examples**:
- "本周末去爬山" → resolves to this Saturday and Sunday
- "下周末有聚会" → resolves to next weekend's dates

---

## 4. Chinese Public Holidays (中国法定节假日)

**Description**: Official Chinese public holidays.

**Supported Forms**:
- 春节 (Spring Festival / Chinese New Year)
- 国庆节 (National Day)
- 清明节 (Qingming Festival / Tomb-Sweeping Day)
- 劳动节 (Labor Day)
- 端午节 (Dragon Boat Festival)
- 中秋节 (Mid-Autumn Festival)
- 元旦 (New Year's Day)

**Examples**:
- "春节回家" → resolves to Spring Festival date
- "国庆节去旅游" → resolves to National Day date
- "清明节扫墓" → resolves to Qingming Festival date

---

## 5. Lunar Traditional Festivals (农历传统节日)

**Description**: Traditional Chinese festivals based on the lunar calendar.

**Supported Forms**:
- 元宵节 (Lantern Festival)
- 七夕 (Qixi Festival / Chinese Valentine's Day)
- 重阳节 (Double Ninth Festival)
- 除夕 (Chinese New Year's Eve)

**Examples**:
- "元宵节看灯会" → resolves to Lantern Festival date
- "七夕送礼物" → resolves to Qixi Festival date
- "除夕吃年夜饭" → resolves to Chinese New Year's Eve date

---

## 6. Lunar Date Expressions (农历日期)

**Description**: Specific dates in the lunar calendar.

**Supported Forms**:
- 正月十五 (15th day of the first lunar month)
- 腊月二十三 (23rd day of the twelfth lunar month)
- 农历八月十五 (15th day of the eighth lunar month)
- 阴历三月初三 (3rd day of the third lunar month)

**Examples**:
- "正月十五闹元宵" → resolves to the 15th day of the first lunar month
- "农历八月十五赏月" → resolves to Mid-Autumn Festival date

---

## 7. Western Festivals (西方节日)

**Description**: Western holidays and celebrations.

**Supported Forms**:
- 圣诞节 (Christmas)
- 万圣节 (Halloween)
- 情人节 (Valentine's Day)
- 复活节 (Easter)
- 感恩节 (Thanksgiving)

**Examples**:
- "圣诞节交换礼物" → resolves to December 25
- "万圣节装扮" → resolves to October 31
- "情人节约会" → resolves to February 14

---

## 8. 24 Solar Terms (24节气)

**Description**: The 24 solar terms in the traditional Chinese calendar.

**Supported Forms**:
- 春分, 秋分 (Spring Equinox, Autumn Equinox)
- 冬至, 夏至 (Winter Solstice, Summer Solstice)
- 立春, 立夏, 立秋, 立冬 (Beginning of Spring/Summer/Autumn/Winter)
- And all other 24 solar terms
- Supports year prefix: 2026年冬至

**Examples**:
- "春分时节" → resolves to Spring Equinox date
- "2026年冬至" → resolves to Winter Solstice in 2026
- "立秋后天气转凉" → resolves to Beginning of Autumn date

---

## 9. Season Expressions (季节表达)

**Description**: Expressions referring to seasons.

**Supported Forms**:
- 春季 (spring)
- 夏季 (summer)
- 秋季 (autumn/fall)
- 冬季 (winter)

**Examples**:
- "春季旅游" → resolves to spring season date range
- "夏季度假" → resolves to summer season date range

---

## 10. Relative Month Expressions (相对月份)

**Description**: Expressions referring to months relative to the current month.

**Supported Forms**:
- 下个月 (next month)
- 下下个月 (the month after next)
- And further stacking patterns

**Examples**:
- "下个月出差" → resolves to next month's date range
- "下下个月开会" → resolves to the month after next

---

## 11. Specific Date Expressions (具体日期)

**Description**: Explicit date expressions.

**Supported Forms**:
- 7月15日 (July 15)
- 2026年国庆节 (National Day 2026)
- 8月20号 (August 20)
- Month + day combinations

**Examples**:
- "7月15日开会" → resolves to July 15
- "2026年国庆节旅游" → resolves to October 1, 2026
- "8月20号提交报告" → resolves to August 20

---

## 12. Bare Weekday Expressions (单独工作日表达)

**Description**: Weekday references without week context.

**Supported Forms**:
- 周一, 周二, ..., 周日 (Monday, Tuesday, ..., Sunday)
- 这周末 (this weekend)
- 本周一 (this Monday)

**Examples**:
- "周三开会" → resolves to the nearest Wednesday
- "这周末休息" → resolves to this weekend's dates

---

## 13. Single Month Expressions (单独月份)

**Description**: Month-only references.

**Supported Forms**:
- 7月, 三月, 十二月 (July, March, December)
- Both Arabic numerals and Chinese numerals

**Examples**:
- "7月去旅游" → resolves to July date range
- "三月开学" → resolves to March date range

---

## 14. Year Cycle Expressions (年度周期)

**Description**: Expressions referring to quarters or half-years.

**Supported Forms**:
- Q1, Q2, Q3, Q4 (quarters)
- 上半年 (first half of the year)
- 下半年 (second half of the year)

**Examples**:
- "Q1业绩目标" → resolves to Q1 date range (Jan-Mar)
- "上半年完成项目" → resolves to first half year (Jan-Jun)
- "下半年招聘" → resolves to second half year (Jul-Dec)

---

## 15. English Time Expressions (英文时间表达)

**Description**: Time expressions in English.

**Supported Forms**:
- tomorrow (明天)
- next week (下周)
- Christmas (圣诞节)
- next Monday (下周一)
- this weekend (本周末)
- And other common English time expressions

**Examples**:
- "meeting tomorrow" → resolves to tomorrow's date
- "vacation next week" → resolves to next week's date range
- "party this weekend" → resolves to this weekend's dates

---

## Usage Notes

1. **Language Auto-Detection**: fcalendar automatically detects whether the input is Chinese or English.
2. **Mixed Language**: You can mix Chinese and English time expressions in the same text.
3. **Context Sensitivity**: The tool uses the `--today` parameter as the reference date for resolving relative expressions.
4. **Ambiguity Resolution**: When multiple interpretations are possible, the tool chooses the nearest future date.

## See Also

- [holidays.md](holidays.md) - Detailed information about Chinese public holidays and solar terms
- [SKILL.md](../SKILL.md) - Main skill documentation with usage examples
