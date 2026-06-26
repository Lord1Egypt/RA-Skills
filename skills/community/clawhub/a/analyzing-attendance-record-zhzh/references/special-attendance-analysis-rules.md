# Special Attendance Analysis Rules

## Table of Contents

--[Rule 0: Daily Statistical](#rule-0-daily-statistical)
--[Rule 1: Weekend Rotation Identification](#rule-1-weekend-rotation-identification)
--[Rule 2: Holiday Statistics](#rule-2-holiday-statistics)

## Rule 0: Daily Statistical

The xlsx files usually contain attendance data spanning **5 days, 6 days, or 7 days**. The expected clock-in count per employee depends on both their **branch** and their **role** (regular or weekend-rotation):

### Standard calculation (non-holiday weeks)

| Branch | Staff Type | Working days | Expected clock-ins |
|--------|-----------|-------------|-------------------|
| 火车站支行 / 茅坪支行 / 滨江支行 / 珠晖支行本部 | All staff | Mon–Fri (5 days) | 10 |
| 新湘支行 / 茶山支行 | Regular staff | Mon–Fri (5 days) | 10 |
| 新湘支行 / 茶山支行 | Weekend-rotation staff (3 people) | 5 days (Sat + 4 weekdays) | 10 |
| 珠晖支行营业部 | Regular staff | Mon–Fri (5 days) | 10 |
| 珠晖支行营业部 | Weekend-rotation staff (3 people, rest 2 weekdays) | 5 days (Sat+Sun + 3 weekdays) | 10 |
| 珠晖支行营业部 | Weekend-rotation staff (3 people, rest 1 weekday) | 6 days (Sat+Sun + 4 weekdays) | 12 |

### How to determine actual expected clock-ins from data

1. For each employee, count the **distinct dates** they have clock-in records (including 缺卡 records, as 缺卡 means they were supposed to work that day).
2. Expected clock-ins = number of distinct working dates × 2 (one for 上班打卡, one for 下班打卡).
3. Verify this against the branch schedule rules to ensure consistency.

## Rule 1: Weekend Rotation Identification

To identify weekend-rotation staff from the Excel data:

### For 新湘支行 / 茶山支行:
1. Filter employees who have **any records on Saturday (周六)**.
2. These employees (should be ~3 per branch) are weekend-rotation staff.
3. They will be **missing records on one weekday** — this is their scheduled rest day and should NOT count as absence.
4. Their expected clock-ins remain **10 per week** (5 working days × 2).

### For 珠晖支行营业部:
1. Filter employees who have **any records on Saturday (周六) or Sunday (周日)**.
2. These employees (should be ~3) are weekend-rotation staff.
3. They will be **missing records on 1–2 weekdays** — these are their scheduled rest days and should NOT count as absence.
4. Calculate their expected clock-ins:
   - Count the total distinct dates they have records on (including 缺卡).
   - Expected clock-ins = total working dates × 2.

## Rule 2: Holiday Statistics

### Public Holiday List (China)

The following are the standard Chinese public holidays. During these holidays, **attendance rules may differ** from normal weeks:

| Holiday | Date(s) | Notes |
|---------|---------|-------|
| 元旦 (New Year's Day) | January 1 | 1 day off |
| 春节 (Chinese New Year) | Lunar New Year (typically late Jan–mid Feb) | 7 days off (with weekend makeup days) |
| 清明节 (Qingming Festival) | April 4–6 (approximate) | 3 days off |
| 劳动节 (Labor Day) | May 1–5 (approximate) | 5 days off (with weekend makeup days) |
| 端午节 (Dragon Boat Festival) | Lunar calendar 5th month 5th day (typically June) | 3 days off |
| 中秋节 (Mid-Autumn Festival) | Lunar calendar 8th month 15th day (typically Sept–Oct) | 3 days off |
| 国庆节 (National Day) | October 1–7 | 7 days off (with weekend makeup days) |

### Holiday attendance rules

1. **Holiday weeks**: If the data period includes a public holiday, the expected clock-ins for ALL employees should be reduced accordingly. For example, if a holiday takes 1 day from the work week, the expected clock-ins = (normal working days - holiday days) × 2.

2. **Weekend makeup days (调休)**: Some holidays require employees to work on a Saturday or Sunday as a makeup day. If the data shows clock-in records on a weekend during a holiday adjustment period, treat these as **normal working days**.

3. **User-specified holidays**: The user may provide specific instructions for holiday attendance. When this happens, follow the user's instructions rather than the general rules above.

4. **Branch-specific holiday rules**: For branches like 珠晖支行营业部 that normally provide 7-day coverage, holiday attendance should follow the specific schedule provided by the user, as some staff may still need to work during holidays.