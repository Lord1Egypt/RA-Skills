import sys
import datetime

# 训练课表模板
TRAINING_PLAN = [
    {"days_before": 7, "summary": "🛀 完全休息", "description": "全身拉伸 + 泡沫轴放松"},
    {"days_before": 6, "summary": "🟢 Z1 恢复跑", "description": "平路慢跑 30-40min (HR 131-146)"},
    {"days_before": 5, "summary": "⚡ 神经唤醒", "description": "2km 热身 + 800m×3 (6:00-6:15/km) + 2km 冷身"},
    {"days_before": 4, "summary": "😴 完全休息", "description": "早睡第一优先级"},
    {"days_before": 3, "summary": "🟢 极简慢跑", "description": "20-30min 慢跑 + 开始增加碳水"},
    {"days_before": 2, "summary": "⚡ 赛前激活", "description": "15min 慢跑 + 80m 冲刺×2"},
    {"days_before": 1, "summary": "🍚 赛前准备", "description": "前往赛场 / 领包 / 晚上10点前入睡"},
    {"days_before": 0, "summary": "🏁 比赛日", "description": "按路书执行"}
]

def generate_calendar_script(race_date_str, race_name):
    try:
        race_date = datetime.datetime.strptime(race_date_str, "%Y-%m-%d")
    except ValueError:
        print("Error: Date format must be YYYY-MM-DD")
        return

    script_content = f"""
import subprocess
import datetime

events = ["""
    
    for plan in TRAINING_PLAN:
        event_date = race_date - datetime.timedelta(days=plan["days_before"])
        date_str = event_date.strftime("%Y-%m-%d")
        summary = f"{plan['summary']} - {race_name}"
        desc = plan['description']
        script_content += f'\n    {{"date": "{date_str}", "summary": "{summary}", "description": "{desc}"}},'

    script_content += """
]

def add_event(event):
    date_str = event["date"]
    summary = event["summary"]
    description = event["description"]
    
    script = f'''
    tell application "Calendar"
        set event_date to date "{{date_str}}"
        set target_calendar to missing value
        try
            set target_calendar to first calendar whose name is "iCloud"
        on error
            try
                set target_calendar to first calendar whose name is "日历"
            on error
                set target_calendar to calendar 1
            end try
        end try
        
        if target_calendar is not missing value then
            tell target_calendar
                make new event with properties {{summary:"{{summary}}", start date:event_date, end date:event_date, allday event:true, description:"{{description}}"}}
            end tell
        end if
    end tell
    '''
    subprocess.run(["osascript", "-e", script], check=True)

if __name__ == "__main__":
    for event in events:
        add_event(event)
    print("Calendar sync complete.")
"""
    return script_content

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python sync_gen.py YYYY-MM-DD 'Race Name'")
    else:
        print(generate_calendar_script(sys.argv[1], sys.argv[2]))
