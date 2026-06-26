import os
import datetime
from icalendar import Calendar

# 获取数据文件夹路径 (相对路径)
# 假定脚本在 .../skills/cn-holiday-checker/scripts/ 中
# data 目录在 .../skills/cn-holiday-checker/data/ 中
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

def get_holiday_map():
    holiday_map = {}
    if not os.path.exists(DATA_DIR):
        return holiday_map
    
    # 扫描目录下所有的 .ics 文件
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.ics'):
            file_path = os.path.join(DATA_DIR, filename)
            with open(file_path, 'rb') as f:
                try:
                    cal = Calendar.from_ical(f.read())
                    for component in cal.walk():
                        if component.name == "VEVENT":
                            summary = str(component.get('summary'))
                            dtstart = component.get('dtstart')
                            dtend = component.get('dtend')
                            
                            if not dtstart:
                                continue
                            
                            # 获取开始日期
                            start_val = dtstart.dt
                            if isinstance(start_val, datetime.datetime):
                                start_date = start_val.date()
                            else:
                                start_date = start_val
                            
                            # 获取结束日期 (如果有)
                            if dtend:
                                end_val = dtend.dt
                                if isinstance(end_val, datetime.datetime):
                                    end_date = end_val.date()
                                else:
                                    end_date = end_val
                            else:
                                # 没有结束日期，默认为单日事件
                                end_date = start_date + datetime.timedelta(days=1)
                            
                            # 遍历所有日期并添加到地图
                            curr = start_date
                            while curr < end_date:
                                holiday_map[curr] = summary
                                curr += datetime.timedelta(days=1)
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
    return holiday_map

def check_date(target_date):
    """
    判断 target_date (date object) 是工作日还是休息日
    """
    holiday_map = get_holiday_map()
    
    # 1. 检查是否有特殊事件
    if target_date in holiday_map:
        event = holiday_map[target_date]
        if '班' in event:
            return "工作日", event
        elif '休' in event:
            return "休息日", event
        # 其他类型节日，依然按周判断
    
    # 2. 按自然周判断 (周一至周五=工作日，周六至周日=休息日)
    if target_date.weekday() < 5:
        return "工作日", "正常工作日"
    else:
        return "休息日", "正常周末"

if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, help="YYYY-MM-DD")
    args = parser.parse_args()
    
    if args.date:
        target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
    else:
        target_date = datetime.date.today()
        
    status, detail = check_date(target_date)
    print(f"日期: {target_date}, 状态: {status}, 详情: {detail}")
