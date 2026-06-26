# 快速测试脚本
staff = ['张护士', '李护理员', '王护工', '赵阿姨', '钱大姐', '孙护士', '周护理员']
from datetime import datetime, timedelta

class G:
    SHIFTS = [
        {'id': 'morning', 'name': '早班', 'start': '07:00', 'end': '15:00', 'required': 2},
        {'id': 'afternoon', 'name': '中班', 'start': '15:00', 'end': '23:00', 'required': 2},
        {'id': 'night', 'name': '夜班', 'start': '23:00', 'end': '07:00', 'required': 1},
    ]
    WEEKDAYS = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

    def __init__(self, staff_list, shifts_per_week=5, cycle='week'):
        self.staff = [{'name': n, 'shifts': 0, 'last_date': None, 'last_shift': None} for n in staff_list]
        self.spw = shifts_per_week
        self.days = 7 if cycle == 'week' else 30
        today = datetime.now()
        days_until_monday = (7 - today.weekday()) % 7
        if days_until_monday == 0: days_until_monday = 7
        self.start = today + timedelta(days=days_until_monday)

    def gen(self):
        r = []
        for d in range(self.days):
            cd = self.start + timedelta(days=d)
            ds = cd.strftime('%Y-%m-%d')
            wk = cd.weekday()
            for sh in self.SHIFTS:
                av = [s for s in self.staff if s['shifts'] < self.spw]
                av.sort(key=lambda x: x['shifts'])
                asd = []
                for s in av:
                    if len(asd) >= sh['required']: break
                    asd.append(s['name'])
                    s['shifts'] += 1
                    s['last_date'] = ds
                    s['last_shift'] = sh['id']
                if asd:
                    r.append({'date': ds, 'weekday': self.WEEKDAYS[wk], 'shift': sh['name'], 'time': f"{sh['start']}-{sh['end']}", 'staff': '、'.join(asd)})
        return r

g = G(staff, 5, 'week')
s = g.gen()
print('| 日期 | 班次 | 时间 | 值班人员 |')
print('|------|------|------|----------|')
for x in s: print(f"| {x['date']} {x['weekday']} | {x['shift']} | {x['time']} | {x['staff']} |")
