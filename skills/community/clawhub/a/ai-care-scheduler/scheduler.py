"""
智能照护排班工具
纯对话式排班生成器
"""

import json
import csv
from datetime import datetime, timedelta

class CareScheduleGenerator:
    """养老机构排班生成器"""
    
    # 默认班次配置
    SHIFTS = [
        {"id": "morning", "name": "早班", "start": "07:00", "end": "15:00", "required": 2},
        {"id": "afternoon", "name": "中班", "start": "15:00", "end": "23:00", "required": 2},
        {"id": "night", "name": "夜班", "start": "23:00", "end": "07:00", "required": 1},
    ]
    
    WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    
    def __init__(self, staff_list, shifts_per_week=5, cycle="week", start_date=None):
        """
        初始化排班器
        :param staff_list: 员工姓名列表
        :param shifts_per_week: 每人每周班次
        :param cycle: 周期 "week" 或 "month"
        :param start_date: 开始日期字符串 YYYY-MM-DD
        """
        self.staff = [{"name": name, "shifts": 0, "last_date": None, "last_shift": None} 
                      for name in staff_list]
        self.shifts_per_week = shifts_per_week
        self.cycle = cycle
        self.days = 7 if cycle == "week" else 30
        
        if start_date:
            self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        else:
            # 默认下周周一
            today = datetime.now()
            days_until_monday = (7 - today.weekday()) % 7
            if days_until_monday == 0:
                days_until_monday = 7
            self.start_date = today + timedelta(days=days_until_monday)
    
    def generate(self):
        """生成排班表"""
        schedule = []
        
        for day in range(self.days):
            current_date = self.start_date + timedelta(days=day)
            date_str = current_date.strftime("%Y-%m-%d")
            weekday = current_date.weekday()
            
            for shift in self.SHIFTS:
                assigned = self._assign_staff(shift, weekday, date_str)
                if assigned:
                    schedule.append({
                        "date": date_str,
                        "weekday": self.WEEKDAYS[weekday],
                        "shift": shift["name"],
                        "time": f"{shift['start']}-{shift['end']}",
                        "staff": "、".join(assigned)
                    })
        
        return schedule
    
    def _assign_staff(self, shift, weekday, date_str):
        """为班次分配员工"""
        assigned = []
        
        # 筛选可用员工
        available = []
        for s in self.staff:
            # 检查周班次上限
            week_num = (datetime.strptime(date_str, "%Y-%m-%d") - self.start_date).days // 7
            week_start = self.start_date + timedelta(days=week_num * 7)
            week_end = week_start + timedelta(days=6)
            
            # 统计本周已上班次
            week_shifts = sum(1 for ss in self.staff 
                            if ss.get("week_num", -1) == week_num and ss.get("shifts", 0) > 0)
            
            if s["shifts"] >= self.shifts_per_week:
                continue
            
            # 检查是否连续排班
            if s["last_date"]:
                last = datetime.strptime(s["last_date"], "%Y-%m-%d")
                current = datetime.strptime(date_str, "%Y-%m-%d")
                if (current - last).days < 2:  # 48小时内连续
                    continue
            
            # 检查夜班后休息
            if shift["id"] == "morning" and s.get("last_shift") == "night":
                continue
            
            # 按已上班次排序，少的优先
            available.append(s)
        
        available.sort(key=lambda x: x["shifts"])
        
        # 分配员工
        for s in available:
            if len(assigned) >= shift["required"]:
                break
            assigned.append(s["name"])
            s["shifts"] += 1
            s["last_date"] = date_str
            s["last_shift"] = shift["id"]
        
        return assigned
    
    def format_markdown(self, schedule):
        """格式化为 Markdown 表格"""
        lines = ["| 日期 | 班次 | 时间 | 值班人员 |",
                 "|------|------|------|----------|"]
        
        current_date = ""
        for s in schedule:
            date_display = f"{s['date']} {s['weekday']}"
            if s['date'] == current_date:
                date_display = ""
            else:
                current_date = s['date']
            lines.append(f"| {date_display} | {s['shift']} | {s['time']} | {s['staff']} |")
        
        return "\n".join(lines)
    
    def export_csv(self, schedule, filename):
        """导出 CSV 文件"""
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['日期', '星期', '班次', '时间', '值班人员'])
            for s in schedule:
                writer.writerow([s['date'], s['weekday'], s['shift'], s['time'], s['staff']])
        return filename


def quick_schedule(staff_str, shifts_per_week=5, cycle="week", start_date=None):
    """
    快速生成排班表
    :param staff_str: 员工姓名，逗号或换行分隔
    :param shifts_per_week: 每人每周班次
    :param cycle: "week" 或 "month"
    :param start_date: 开始日期 YYYY-MM-DD
    :return: (markdown表格, csv文件路径)
    """
    # 解析员工列表
    staff_list = [s.strip() for s in staff_str.replace('\n', ',').split(',') if s.strip()]
    
    # 生成排班
    generator = CareScheduleGenerator(staff_list, shifts_per_week, cycle, start_date)
    schedule = generator.generate()
    
    # 格式化输出
    markdown = generator.format_markdown(schedule)
    
    # 导出CSV
    date_str = generator.start_date.strftime("%Y%m%d")
    csv_file = f"排班表_{date_str}_{cycle}.csv"
    generator.export_csv(schedule, csv_file)
    
    return markdown, csv_file


if __name__ == "__main__":
    # 测试
    staff = "张护士,李护理员,王护工,赵阿姨,钱大姐,孙护士,周护理员"
    md, csv_file = quick_schedule(staff, shifts_per_week=5, cycle="week")
    print(md)
    print(f"\n已导出: {csv_file}")
