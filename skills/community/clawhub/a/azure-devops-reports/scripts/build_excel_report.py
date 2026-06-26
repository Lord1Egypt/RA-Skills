import json
import argparse
import os
from datetime import datetime, timedelta
import xlsxwriter

def get_week_start(dt_str):
    if not dt_str:
        return None
    try:
        # Azure DevOps dates are usually like "2020-06-25T14:44:56.623Z"
        dt = datetime.strptime(dt_str[:10], '%Y-%m-%d')
        # Start of week (Monday)
        start = dt - timedelta(days=dt.weekday())
        return start.strftime('%Y-%m-%d')
    except:
        return None

def build_report(input_json, output_xlsx):
    with open(input_json, 'r') as f:
        bundle = json.load(f)

    items = bundle.get('items', [])
    summary = bundle.get('summary', {})

    workbook = xlsxwriter.Workbook(output_xlsx)
    
    # Formats
    header_fmt = workbook.add_format({'bold': True, 'bg_color': '#CFE2F3', 'border': 1})
    date_fmt = workbook.add_format({'num_format': 'yyyy-mm-dd'})
    bold_fmt = workbook.add_format({'bold': True})

    # --- Raw Data Sheet ---
    raw_sheet = workbook.add_worksheet('RawData')
    columns = [
        'id', 'title', 'state', 'type', 'assignedTo', 
        'project', 'iterationPath', 'areaPath', 'priority', 
        'createdDate', 'changedDate', 'closedDate'
    ]
    
    for col_num, col_name in enumerate(columns):
        raw_sheet.write(0, col_num, col_name, header_fmt)

    for row_num, item in enumerate(items, 1):
        for col_num, col_name in enumerate(columns):
            val = item.get(col_name, '')
            if col_name in ['createdDate', 'changedDate', 'closedDate'] and val:
                raw_sheet.write(row_num, col_num, val[:10], date_fmt)
            else:
                raw_sheet.write(row_num, col_num, val)
    raw_sheet.freeze_panes(1, 0)
    raw_sheet.set_column(1, 1, 50) # Title column width

    # --- Summary Sheet ---
    summary_sheet = workbook.add_worksheet('Summary')
    summary_sheet.write(0, 0, 'Category', header_fmt)
    summary_sheet.write(0, 1, 'Value', header_fmt)
    summary_sheet.write(0, 2, 'Count', header_fmt)

    curr_row = 1
    summary_sheet.write(curr_row, 0, 'Total Work Items', bold_fmt)
    summary_sheet.write(curr_row, 2, summary.get('totals', {}).get('workItems', 0))
    curr_row += 2

    for section, label in [('byState', 'By State'), ('byType', 'By Type'), ('byAssignee', 'By Assignee')]:
        summary_sheet.write(curr_row, 0, label, bold_fmt)
        curr_row += 1
        data_list = summary.get(section, [])
        for entry in data_list:
            name = entry.get('name', 'Unknown')
            count = entry.get('count', 0)
            summary_sheet.write(curr_row, 1, name)
            summary_sheet.write(curr_row, 2, count)
            curr_row += 1
        curr_row += 1

    # --- Weekly Trend Sheet ---
    trend_sheet = workbook.add_worksheet('WeeklyTrendData')
    trend_sheet.write(0, 0, 'Week Start', header_fmt)
    trend_sheet.write(0, 1, 'Created', header_fmt)
    trend_sheet.write(0, 2, 'Closed', header_fmt)

    weekly_created = {}
    weekly_closed = {}
    
    for item in items:
        c_week = get_week_start(item.get('createdDate'))
        if c_week:
            weekly_created[c_week] = weekly_created.get(c_week, 0) + 1
        
        closed_week = get_week_start(item.get('closedDate'))
        if closed_week:
             weekly_closed[closed_week] = weekly_closed.get(closed_week, 0) + 1

    all_weeks = sorted(list(set(list(weekly_created.keys()) + list(weekly_closed.keys()))))
    
    for row_num, week in enumerate(all_weeks, 1):
        trend_sheet.write(row_num, 0, week, date_fmt)
        trend_sheet.write(row_num, 1, weekly_created.get(week, 0))
        trend_sheet.write(row_num, 2, weekly_closed.get(week, 0))

    # --- Trend Chart Sheet ---
    chart_sheet = workbook.add_worksheet('Charts')
    chart = workbook.add_chart({'type': 'line'})
    
    num_weeks = len(all_weeks)
    if num_weeks > 0:
        chart.add_series({
            'name':       ['WeeklyTrendData', 0, 1],
            'categories': ['WeeklyTrendData', 1, 0, num_weeks, 0],
            'values':     ['WeeklyTrendData', 1, 1, num_weeks, 1],
            'line':       {'color': '#4285F4'},
        })
        chart.add_series({
            'name':       ['WeeklyTrendData', 0, 2],
            'categories': ['WeeklyTrendData', 1, 0, num_weeks, 0],
            'values':     ['WeeklyTrendData', 1, 2, num_weeks, 2],
            'line':       {'color': '#34A853'},
        })

        chart.set_title({'name': 'Weekly Created vs Closed Trend'})
        chart.set_x_axis({
            'name': 'Week Starting',
            'num_font': {'rotation': -90}
        })
        chart.set_y_axis({'name': 'Work Items'})
        chart_sheet.insert_chart('B2', chart, {'x_scale': 1.5, 'y_scale': 1.5})

    workbook.close()
    print(f"Excel report generated: {output_xlsx}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build Excel report from Azure DevOps JSON bundle')
    parser.add_argument('--input', required=True, help='Path to input JSON file')
    parser.add_argument('--output', required=True, help='Path to output XLSX file')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input file {args.input} not found")
        exit(1)
        
    build_report(args.input, args.output)
