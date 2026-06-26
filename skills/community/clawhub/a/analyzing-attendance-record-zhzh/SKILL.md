---
name: analyzing-attendance-record-zhzh
description: Analyze the weekly attendance records of employees at Zhuihui Branch and generate an attendance report in docx format. At the same time, output an xlsx file as a detailed supplement.
---

# Attendance record analysis for Zhuihui Branch

Automated analysis of attendance record data.

## Input Requirements

The expected input of attendance data should be in xlsx format. The first two rows are headers (Row 1: group headers, Row 2: column names). Data starts from Row 3. The columns are:

### Basic Info (基本信息)

--**姓名**：employee's name information

--**工号**：employee ID number (may be '-' for some employees)

--**部门**：department information of the employees, including: '珠晖支行营业部', '新湘支行', '火车站支行', '茶山支行', '茅坪支行', '滨江支行', '珠晖支行本部'.

--**日期**：the date format is YYYYMMDD.

### Clock-in Info (打卡信息)

--**上班1打卡时间**：primary clock-in time, format HH:MM. '-' or empty means no clock-in.

--**下班1打卡时间**：primary clock-out time, format HH:MM. '-' or empty means no clock-out.

--**上班2/下班2/上班3/下班3打卡时间**：additional clock-in/out pairs (usually empty, used for split shifts).

--**考勤结果**：The attendance results are classified into these categories: '正常', '缺卡', '迟到', '早退', '迟到早退', and '-' (no attendance data, typically for excluded or absent employees).

### Time Statistics (时长统计)

--**应出勤(小时)**：expected work hours per day.

--**计薪时长(小时)**：paid hours.

--**实际出勤(小时)**：actual work hours.

--**迟到时长(分钟)**：late duration in minutes.

--**早退时长(分钟)**：early leave duration in minutes.

--**加班时长(小时)**：overtime hours.

## Data Quality Check

1.Group and count by department for the statistics.

2.'新湘支行' needs to remove '珠晖-新湘-王治国' and '珠晖-新湘-魏紫兰','茶山支行' needs to remove '珠晖-茶山-陈妍','火车站支行' needs to remove '珠晖-周文娟','珠晖支行本部' needs to remove '陈喆' and '刘一婧' and '谭国球' and '谭庆荣' and '谢清林'. Additionally, ensure '陈迪' is adjusted to '茶山支行' for the output statistical analysis regardless of their original department.

3.The main office of '珠晖支行本部' consists of four departments, namely '综合管理部', '业务管理部', '公司业务部', and '个人金融部'. The staff of '综合管理部' are: '彭涵'、'谢祎'、'王友'、'蒋蕙'  and '朱亚民'. '业务管理部' are: '彭国柱'、'肖冬梅'、'邓意平'、'王知生'、'颜慧松'、'李娜'、'刘新恒' and '李卿'. '公司业务部' are: '陈瑶'、'周鹍'、'甘健生'、'管巧林' and '欧海滨'. '个人金融部' are: '刘平'、'廖欢'、'陈杰'、'吴欣钰'、'费鸿平' and '汤锋'. Please divide the main office of '珠晖支行本部' into these four departments to record the attendance records.

## Branch Work Schedule

Each branch has a different work schedule. The AI must apply the correct schedule when calculating expected clock-ins.

### Standard branches (Monday to Friday, 5 days/week)

The following branches work **Monday to Friday**. Each employee is expected to clock in **10 times per week** (2 times/day × 5 days).

--火车站支行
--茅坪支行
--滨江支行
--珠晖支行本部 (including all 4 sub-departments: 综合管理部, 业务管理部, 公司业务部, 个人金融部)

### Weekend-rotation branches: 新湘支行 and 茶山支行 (Monday to Saturday coverage)

These branches maintain **Saturday coverage** through a rotation system, but the total required clock-ins for EVERY employee in these branches remains **10 times per week** (2 times/day × 5 working days).

--**Regular staff**: Work Monday to Friday (10 clock-ins/week).
--**Weekend-rotation staff**: Work Saturday and typically rest one day during Monday to Friday. Due to this compensatory leave, they will appear to have missed clock-ins on a weekday. The AI must correctly judge this: as long as their total actual clock-ins reach 10 times across Monday to Saturday, the weekday "absences" are normal rest days and should NOT be counted as missing cards (`缺卡`).

### Full-coverage branch: 珠晖支行营业部 (7-day coverage)

This branch maintains coverage on **all 7 days** through a rotation system:

--**Regular staff**: Work Monday to Friday (10 clock-ins/week).
--**Weekend-rotation staff (3 people)**: Work Saturday and Sunday, and rest 1–2 days during Monday to Friday. Their expected clock-ins depend on their actual schedule:
  - If rest 2 weekdays: work 5 days total → **10 clock-ins/week**
  - If rest 1 weekday: work 6 days total → **12 clock-ins/week**

**How to identify weekend-rotation staff**: Check the Excel data for employees in 珠晖支行营业部 who have clock-in records on **Saturday (周六) and/or Sunday (周日)**. Cross-reference with their weekday records to determine how many weekdays they rested, then calculate the correct expected clock-ins accordingly.

### Holiday exceptions

All the above schedules are for **normal working weeks only**. During public holidays, attendance should follow the specific holiday schedule. See `references/special-attendance-analysis-rules.md` for holiday rules.

## Mainly Analyzed Data

Calculate attendance rate:

--**attendance rate** = The actual number of check-ins by the department / The number of times the department should clock in × 100%

**Calculating "the number of times the department should clock in"**: Sum up the expected clock-ins for each employee in the department, based on their individual schedule (see Branch Work Schedule above). Do NOT assume a uniform number for all employees — weekend-rotation staff may have different expected clock-ins than regular staff.

Sort by department attendance rate.

Output the attendance rate, the number of required clock-ins, the actual clock-ins, the number of missed clock-ins, the personnel who missed clock-ins, as well as the details of those who were late or left early for each department.

## Special Attendance Analysis Rules

If user asks about '特殊考勤情况分析', read `references/special-attendance-analysis-rules.md` for performance-based actions and constraints.