# Example: Weekly Attendance Analysis

## Scenario

Analyze the attendance records for Zhuihui Branch for the week of **2026/02/24 – 2026/02/28** (Tuesday to Saturday).

## Input File

[每日统计表_20260224_20260228.xlsx](./每日统计表_20260224_20260228.xlsx)

### Data Overview

| Item | Value |
|------|-------|
| Date range | 2026-02-24 (Tue) → 2026-02-28 (Sat) |
| Total records | 395 (excluding header rows) |
| Total employees | 79 |
| Departments | 7 |

### Column Structure

| Column | Description |
|--------|-------------|
| 姓名 | Employee name |
| 工号 | Employee ID |
| 部门 | Department |
| 日期 | Date (YYYYMMDD) |
| 上班1打卡时间 | Clock-in time (primary) |
| 下班1打卡时间 | Clock-out time (primary) |
| 上班2/下班2/上班3/下班3 | Additional clock-in/out pairs (usually empty) |
| 考勤结果 | Result: 正常/缺卡/迟到/早退/迟到早退/- |
| 应出勤(小时) | Required work hours |
| 计薪时长(小时) | Paid hours |
| 实际出勤(小时) | Actual work hours |
| 迟到时长(分钟) | Late duration (minutes) |
| 早退时长(分钟) | Early leave duration (minutes) |
| 加班时长(小时) | Overtime hours |

## Sample Prompt

> 请帮我分析这份考勤数据（每日统计表_20260224_20260228.xlsx），生成一份考勤报告。

## Expected Processing Steps

### Step 1: Data Clean-up

Remove excluded employees per rules:
- 新湘支行: remove 珠晖-新湘-王治国, 珠晖-新湘-魏紫兰
- 茶山支行: remove 珠晖-茶山-陈妍
- 火车站支行: remove 珠晖-周文娟
- 珠晖支行本部: remove 陈喆, 刘一婧, 谭国球, 谭庆荣, 谢清林

### Step 2: Split 珠晖支行本部 into sub-departments

| Sub-department | Staff |
|---------------|-------|
| 综合管理部 | 彭涵、谢祎、王友、蒋蕙、朱亚民 |
| 业务管理部 | 彭国柱、肖冬梅、邓意平、王知生、颜慧松、李娜、刘新恒、李卿 |
| 公司业务部 | 陈瑶、周鹍、甘健生、管巧林、欧海滨 |
| 个人金融部 | 刘平、廖欢、陈杰、吴欣钰、费鸿平、汤锋 |

### Step 3: Determine work schedules

**This week's data is Tue–Sat (5 days), so:**

- **Standard branches** (火车站/茅坪/滨江/珠晖支行本部): All staff worked Tue–Fri (4 weekdays). Saturday data exists but only weekend-duty staff or those with 正常 records are truly expected. Since the Excel includes Saturday for ALL employees, check the 考勤结果:
  - If Saturday result is `缺卡` with both 上班/下班 being `-`, this means the employee did NOT work Saturday → do NOT count Saturday as an expected work day.
  - If Saturday has valid clock-in data, count it.

- **新湘支行 / 茶山支行**: Similarly, identify the 3 weekend-rotation staff who have valid Saturday records.

- **珠晖支行营业部**: Identify the ~3 weekend-rotation staff from Saturday data.

### Step 4: Calculate attendance metrics

For each department (after exclusions and sub-department split):

1. **应打卡次数** = Sum of each employee's expected clock-ins based on their actual working days × 2
2. **实际打卡次数** = Count of all valid clock-ins (上班 + 下班, excluding `-` and empty)
3. **出勤率** = 实际打卡次数 / 应打卡次数 × 100%
4. **缺卡次数** = 应打卡次数 - 实际打卡次数
5. **缺卡人员** = List of employees who missed clock-ins
6. **迟到/早退详情** = For each employee marked 迟到 or 早退, list: name, date, time, duration

### Step 5: Output

Generate:
- `.docx` report: Department ranking by attendance rate, summary of issues
- `.xlsx` detailed supplement: Per-employee breakdown with all metrics

## Key Observations from This Dataset

- 考勤结果 includes a 6th category `迟到早退` (both late AND early) not in the original SKILL.md — the SKILL now handles this.
- Some employees have result `-` with empty clock-in data (e.g., 甘健生, 刘一婧) — these are excluded employees whose data should be ignored.
- The data includes Saturday for ALL departments/employees, even those who don't work Saturdays — use the clock-in data to distinguish actual workers from non-workers.
