#!/usr/bin/env python3
"""
Attendance Check Script for 基础业务开发部
Queries attendance data from Feishu API and generates two reports:
1. Employees with monthly avg working hours < 9.5h
2. Employees with missing clock-in/out records this month

Usage:
    python3 query_attendance.py                    # current month
    python3 query_attendance.py 202606             # specific month (YYYYMM)
"""

import sys
import json
import subprocess
from collections import defaultdict
from datetime import date, timedelta

# === CONFIGURATION ===
# Employee IDs in 基础业务开发部 (compile from organization data)
# These IDs need to be maintained as team members change
EMPLOYEE_IDS = [
    "000079", "000083", "000088", "000089", "000160", "000533", "000707",
    "000750", "000929", "001601", "004544", "004805", "005046", "005218",
    "005289", "005367", "005423", "007380", "007381", "007528", "007761",
    "007969", "008381", "008983", "009789", "010157", "010161", "011337",
    "011760", "011912", "012133", "014017", "014066", "014172", "014558",
    "014859", "014939", "015320", "015356", "015549", "015546", "015813",
    "015727", "017276", "017327", "017719", "017894", "019041", "019051",
    "019121"
]

# Department sub-groups under 基础业务开发部
VALID_DEPARTMENTS = [
    "支付清算组", "支付前端组", "支付应用组", "APP组",
    "商户运营组", "增值业务组", "业务管理组"
]

# Attendance check config
APP_ID = "cli_aa938ed066385cb2"
APP_SECRET = "3ZPSW3hWLdiYmOSjziXJBhKTLOPRi5Q1"
OPERATOR_USER_ID = "000929"


def get_token():
    """Get Feishu tenant_access_token"""
    result = subprocess.run([
        'curl', '-s', '-X', 'POST',
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        '-H', 'Content-Type: application/json; charset=utf-8',
        '-d', json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET})
    ], capture_output=True, text=True)
    data = json.loads(result.stdout)
    if data.get('code') != 0:
        raise RuntimeError(f"Failed to get token: {data.get('msg')}")
    return data['tenant_access_token']


def query_attendance(token, start_date, end_date, user_ids):
    """Query daily attendance stats for a date range (max 200 users per call)"""
    payload = {
        "locale": "zh",
        "stats_type": "daily",
        "start_date": start_date,
        "end_date": end_date,
        "user_ids": user_ids,
        "user_id": OPERATOR_USER_ID
    }
    result = subprocess.run([
        'curl', '-s', '-X', 'POST',
        'https://open.feishu.cn/open-apis/attendance/v1/user_stats_datas/query?employee_type=employee_id',
        '-H', f'Authorization: Bearer {token}',
        '-H', 'Content-Type: application/json; charset=utf-8',
        '-d', json.dumps(payload)
    ], capture_output=True, text=True)
    return json.loads(result.stdout)


def parse_daily_data(user_datas):
    """Parse the API response into structured daily records"""
    records = []
    for ud in user_datas:
        info = {
            'name': '', 'dept': '', 'date': '', 'should_hours': 0.0,
            'actual_hours': 0.0, 'leave': '-', 'result': '',
            'clock_in': '-', 'clock_out': '-'
        }
        for d in ud.get('datas', []):
            code = d.get('code', '')
            if code == '50101':
                info['name'] = d.get('value', '')
            elif code == '50102':
                info['dept'] = d.get('value', '')
            elif code == '51201':
                info['date'] = d.get('value', '')
            elif code == '51302':
                dn = d.get('duration_num', {})
                info['should_hours'] = float(dn.get('hour', 0))
            elif code == '51303':
                dn = d.get('duration_num', {})
                info['actual_hours'] = float(dn.get('hour', 0))
            elif code == '51401':
                info['leave'] = d.get('value', '-')
            elif code == '51503-1-1':
                info['result'] = d.get('value', '')
            elif code == '51502-1-1':
                info['clock_in'] = d.get('value', '-')
            elif code == '51502-1-2':
                info['clock_out'] = d.get('value', '-')
        records.append(info)
    return records


def is_in_base_business_dept(dept_name):
    """Check if the department belongs to 基础业务开发部"""
    for valid in VALID_DEPARTMENTS:
        if valid in dept_name:
            return True
    return False


def get_base_dept(dept_name):
    """Extract the base group name from a full department string
    
    Examples:
      '支付清算组'       → '支付清算组'
      '支付清算组 | iPE'  → '支付清算组'
      'APP组 | iPE'      → 'APP组'
      '产研中心 | 基础业务开发部 | 26届校招生' → '其他'
    """
    for valid in VALID_DEPARTMENTS:
        if dept_name.startswith(valid):
            return valid
    return '其他'


def get_leave_days(leave_str):
    """Extract the number of leave days from the leave string
    
    Returns the numeric value (1.0 for full day, 0.5 for half day), or 0 if not a leave day.
    Examples:
      '1 天'  → 1.0
      '0.5 天' → 0.5
      '1天'    → 1.0
      '-'      → 0.0
    """
    if leave_str in ('-', '', '0'):
        return 0.0
    import re
    match = re.search(r'(\d+(\.\d+)?)', leave_str)
    if match:
        return float(match.group(1))
    # For '全天' or other full-day indicators
    return 1.0


def is_leave_day(leave_str):
    """Check if this day has any type of leave (full or partial)"""
    return get_leave_days(leave_str) > 0


def report_low_avg_hours(biz_records):
    """Report employees with average monthly working hours < 9.5h
    
    Calculation logic:
    - Only count scheduled workdays (should_hours >= 8h means a regular workday)
    - Any leave day (full OR half): 
      - Counted in leave_days (1.0 for full, 0.5 for half)
      - Excluded from work_days count in the average calculation
      - Actual hours on half-day leaves are still counted in total_hours
    - Average = total_actual_hours / work_days
    """
    stats = defaultdict(lambda: {'dept': '', 'total_hours': 0.0, 'work_days': 0, 'leave_days': 0.0})

    for r in biz_records:
        # Skip weekends and holidays (no scheduled work)
        if r['should_hours'] == 0:
            continue

        key = f"{r['name']}|{r['dept']}"
        s = stats[key]
        s['name'] = r['name']
        s['dept'] = r['dept']

        leave_d = get_leave_days(r['leave'])
        if leave_d > 0:
            s['leave_days'] += leave_d

        # Any leave day (full or half): excluded from work_days denominator
        if is_leave_day(r['leave']):
            # But half-day leave actual hours still count
            s['total_hours'] += r['actual_hours']
            continue

        # Normal work day (no leave): count fully
        s['total_hours'] += r['actual_hours']
        s['work_days'] += 1

    results = []
    for key, s in stats.items():
        if s['work_days'] == 0:
            continue
        avg = round(s['total_hours'] / s['work_days'], 1)
        if avg < 9.5:
            results.append({
                'name': s['name'],
                'dept': s['dept'],
                'avg_hours': avg,
                'work_days': s['work_days'],
                'leave_days': round(s['leave_days'], 1),
                'total_hours': round(s['total_hours'], 1)
            })
    return sorted(results, key=lambda x: x['avg_hours'])


def report_group_avg_hours(biz_records):
    """Calculate average monthly working hours per group"""
    group_stats = defaultdict(lambda: {'total_hours': 0.0, 'work_days': 0, 'employees': set()})
    person_avgs = defaultdict(list)

    # First pass: compute per-person stats (same logic as report_low_avg_hours)
    person_stats = defaultdict(lambda: {
        'dept': '', 'total_hours': 0.0, 'work_days': 0, 'leave_days': 0.0
    })

    for r in biz_records:
        if r['should_hours'] == 0:
            continue
        key = f"{r['name']}|{get_base_dept(r['dept'])}"
        s = person_stats[key]
        s['name'] = r['name']
        s['dept'] = get_base_dept(r['dept'])

        leave_d = get_leave_days(r['leave'])
        if leave_d > 0:
            s['leave_days'] += leave_d
        if is_leave_day(r['leave']):
            s['total_hours'] += r['actual_hours']
            continue
        s['total_hours'] += r['actual_hours']
        s['work_days'] += 1

    # Second pass: aggregate by group
    for key, s in person_stats.items():
        if s['work_days'] == 0:
            continue
        dept = s['dept']
        gs = group_stats[dept]
        gs['total_hours'] += s['total_hours']
        gs['work_days'] += s['work_days']
        gs['employees'].add(s['name'])

    results = []
    for dept, gs in sorted(group_stats.items(), key=lambda x: -x[1]['total_hours'] / x[1]['work_days'] if x[1]['work_days'] > 0 else 0):
        if gs['work_days'] == 0:
            continue
        avg = round(gs['total_hours'] / gs['work_days'], 1)
        results.append({
            'dept': dept,
            'avg_hours': avg,
            'total_hours': round(gs['total_hours'], 1),
            'work_days': gs['work_days'],
            'employee_count': len(gs['employees'])
        })
    return results


def report_missing_clock(biz_records, exclude_date=None):
    """Report employees with missing clock-in/out records"""
    results = []
    for r in biz_records:
        # Skip today (incomplete data) or specified date
        if exclude_date and r['date'] == exclude_date:
            continue
        # Skip non-work days (weekends/holidays)
        if r['clock_in'] == '-' and r['clock_out'] == '-':
            continue
        missing = []
        if r['clock_in'] in ('-', ''):
            missing.append('上班缺卡')
        if r['clock_out'] in ('-', ''):
            missing.append('下班缺卡')
        if missing:
            results.append({
                'name': r['name'],
                'dept': r['dept'],
                'date': r['date'],
                'type': '、'.join(missing)
            })
    return sorted(results, key=lambda x: (x['name'], x['date']))


def print_report_1(low_hours):
    """Print report: employees with low average hours"""
    print(f"{'姓名':<8} {'团队':<14} {'平均工时':<10} {'总工时':<8} {'工作日':<6} {'请假天':<6}")
    print("-" * 56)
    for r in low_hours:
        ld = r['leave_days']
        ld_str = f"{ld}天" if ld != int(ld) else f"{int(ld)}天"
        print(f"{r['name']:<8} {r['dept']:<14} {r['avg_hours']}h{'':8} {r['total_hours']}h{'':4} {r['work_days']}天{'':2} {ld_str}")


def print_report_3(groups):
    """Print report: average hours per group (sorted descending)"""
    print(f"{'团队':<14} {'人数':<6} {'平均工时':<10} {'总工时':<10} {'总工作日':<8}")
    print("-" * 52)
    for g in groups:
        print(f"{g['dept']:<14} {g['employee_count']}人{'':4} {g['avg_hours']}h{'':8} {g['total_hours']}h{'':6} {g['work_days']}天")


def print_report_2(missing):
    """Print report: missing clock-in records"""
    print(f"{'姓名':<8} {'团队':<14} {'日期':<12} {'缺卡类型':<12}")
    print("-" * 50)
    for r in missing:
        date_str = f"{r['date'][:4]}-{r['date'][4:6]}-{r['date'][6:]}"
        print(f"{r['name']:<8} {r['dept']:<14} {date_str:<12} {r['type']:<12}")


def main():
    # Parse target month from command line or use current month
    if len(sys.argv) > 1:
        ym = sys.argv[1]
        year, month = int(ym[:4]), int(ym[4:6])
    else:
        today = date.today()
        year, month = today.year, today.month

    # Calculate start/end dates for the month
    start_date = f"{year}{month:02d}01"
    end_of_month = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year, 12, 31)
    today = date.today()
    end_date = min(today, end_of_month).strftime("%Y%m%d")

    print(f"\n📋 基础业务开发部考勤报告：{year}年{month:02d}月 ({start_date} ~ {end_date})")
    print(f"=" * 60)

    # Get API token
    try:
        token = get_token()
    except RuntimeError as e:
        print(f"❌ 获取 token 失败: {e}")
        sys.exit(1)

    # Query all employees in batches
    all_records = []
    batch_size = 50
    for i in range(0, len(EMPLOYEE_IDS), batch_size):
        batch = EMPLOYEE_IDS[i:i + batch_size]
        data = query_attendance(token, start_date, end_date, batch)
        if data.get('code') != 0:
            print(f"⚠️  API 返回错误: {data.get('msg')}")
            continue
        user_datas = data.get('data', {}).get('user_datas', [])
        records = parse_daily_data(user_datas)
        all_records.extend(records)

    # Filter to only 基础业务开发部 employees
    biz_records = [r for r in all_records if is_in_base_business_dept(r['dept'])]

    if not biz_records:
        print("❌ 未找到基础业务开发部相关的考勤数据")
        sys.exit(1)

    # === Report 3: Average hours per group (new, shown first) ===
    print(f"\n{'─' * 60}")
    print(f"📊 一、各组平均工时排行")
    print(f"{'─' * 60}")
    groups = report_group_avg_hours(biz_records)
    print_report_3(groups)

    # === Report 1: Average hours < 9.5 ===
    print(f"\n{'─' * 60}")
    print(f"📊 二、月平均工时低于 9.5h 的员工")
    print(f"{'─' * 60}")

    low_hours = report_low_avg_hours(biz_records)
    if low_hours:
        print_report_1(low_hours)
    else:
        print("✅ 所有员工月平均工时均 >= 9.5h")

    # === Report 2: Missing clock-in records ===
    print(f"\n{'─' * 60}")
    print(f"🔍 三、当月缺卡情况")
    print(f"{'─' * 60}")

    # Exclude today from missing clock report (data incomplete for current day)
    today_str = date.today().strftime("%Y%m%d")
    missing = report_missing_clock(biz_records, exclude_date=today_str)
    if missing:
        print_report_2(missing)
        # Summary by person
        print(f"\n   📈 按人员汇总：")
        person_summary = defaultdict(lambda: {'dept': '', 'count': 0})
        for r in missing:
            k = f"{r['name']}|{r['dept']}"
            person_summary[k]['name'] = r['name']
            person_summary[k]['dept'] = r['dept']
            person_summary[k]['count'] += 1
        for k, ps in sorted(person_summary.items(), key=lambda x: -x[1]['count']):
            print(f"    {ps['name']:<8} ({ps['dept']}) — {ps['count']}次缺卡")
    else:
        print("✅ 本月暂无缺卡记录")

    print(f"\n{'=' * 60}")
    print(f"✅ 报告完成")


if __name__ == '__main__':
    main()
