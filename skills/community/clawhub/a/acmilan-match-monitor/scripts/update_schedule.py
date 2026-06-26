#!/usr/bin/env python3
"""
AC Milan 赛程自动更新脚本
从 ESPN API 拉取未来赛程，更新 schedule.json
每周一 07:00 运行，确保赛程始终最新
"""
import json
import os
import subprocess
from datetime import datetime, timedelta, timezone

tz_sh = timezone(timedelta(hours=8))
now = datetime.now(tz_sh)

skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
schedule_path = os.path.join(skill_dir, "schedule.json")

TEAM_ABBR_CN = {
    "MIL": "AC米兰", "INT": "国际米兰", "JUV": "尤文图斯",
    "NAP": "那不勒斯", "LAZ": "拉齐奥", "ROM": "罗马", "ROMA": "罗马",
    "ATA": "亚特兰大", "FIO": "佛罗伦萨", "TOR": "都灵", "BOL": "博洛尼亚",
    "LEC": "莱切", "CAG": "卡利亚里", "UDI": "乌迪内斯", "VER": "维罗纳",
    "SAS": "萨索洛", "PAR": "帕尔马", "GEN": "热那亚",
    "CRE": "克雷莫内塞", "PIS": "比萨", "COMO": "科莫",
}

all_matches = []
seen = set()

# 分段查询未来6个月
end_dates = [
    (now.strftime("%Y%m%d"), (now + timedelta(days=90)).strftime("%Y%m%d")),
    ((now + timedelta(days=90)).strftime("%Y%m%d"), (now + timedelta(days=180)).strftime("%Y%m%d")),
]

for start, end in end_dates:
    r = subprocess.run(
        ["/usr/bin/curl", "-s",
         f"https://site.api.espn.com/apis/site/v2/sports/soccer/ita.1/scoreboard?limit=100&dates={start}-{end}"],
        capture_output=True, text=True, timeout=15
    )
    try:
        data = json.loads(r.stdout)
    except:
        continue

    for e in data.get("events", []):
        name = e.get("name", "")
        if "Milan" not in name:
            continue
        dt = datetime.fromisoformat(e.get("date", "").replace("Z", "+00:00")).astimezone(tz_sh)
        if dt < now:
            continue

        key = dt.strftime("%Y-%m-%d") + e.get("shortName", "")
        if key in seen:
            continue
        seen.add(key)

        comps = e.get("competitions", [{}])
        home_abbr = away_abbr = ""
        for c in comps:
            for comp in c.get("competitors", []):
                abbr = comp.get("team", {}).get("abbreviation", "")
                if comp.get("homeAway") == "home":
                    home_abbr = abbr
                else:
                    away_abbr = abbr

        all_matches.append({
            "date": dt.strftime("%Y-%m-%d"),
            "kickoff_bj": dt.strftime("%H:%M"),
            "short": e.get("shortName", ""),
            "home": TEAM_ABBR_CN.get(home_abbr, home_abbr),
            "away": TEAM_ABBR_CN.get(away_abbr, away_abbr),
            "venue": "home" if home_abbr == "MIL" else "away"
        })

all_matches.sort(key=lambda x: x["date"])

# 读取旧数据
old_schedule = {}
if os.path.exists(schedule_path):
    with open(schedule_path) as f:
        old_schedule = json.load(f)

old_count = len(old_schedule.get("matches", []))
new_count = len(all_matches)

schedule = {
    "updated": now.strftime("%Y-%m-%d"),
    "season": "2025-26",
    "note": "意甲剩余赛程（北京时间），比赛结束次日 08:30 推送结果",
    "matches": all_matches
}

with open(schedule_path, "w") as f:
    json.dump(schedule, f, ensure_ascii=False, indent=2)

# 只在赛程有变化时输出
if new_count != old_count:
    print(f"📅 AC Milan 赛程已更新：{old_count} → {new_count} 场")
    if all_matches:
        next_m = all_matches[0]
        print(f"下一场：{next_m['date']} {next_m['kickoff_bj']} | {next_m['short']}")
