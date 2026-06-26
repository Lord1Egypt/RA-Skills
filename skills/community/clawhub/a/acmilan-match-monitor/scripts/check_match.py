#!/usr/bin/env python3
"""
AC Milan 昨日比赛检查脚本
数据来源：ESPN 公开 API（无需 token，无地区限制）
逻辑：先查预置赛程确认昨天是否有比赛，有则查结果+集锦+新闻，无则静默
"""
import json
import os
import re
import subprocess
from datetime import datetime, timedelta, timezone

tz_sh = timezone(timedelta(hours=8))
yesterday = (datetime.now(tz_sh) - timedelta(days=1)).strftime("%Y-%m-%d")

# 1. 查预置赛程，确认昨天是否有比赛
skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
schedule_path = os.path.join(skill_dir, "schedule.json")

has_scheduled_match = False
match_info = None

if os.path.exists(schedule_path):
    with open(schedule_path) as f:
        schedule = json.load(f)
    for m in schedule.get("matches", []):
        kickoff = m.get("kickoff_bj", "00:00")
        match_date = m["date"]
        hour = int(kickoff.split(":")[0])
        if hour < 8:
            actual_match_day = (datetime.strptime(match_date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
        else:
            actual_match_day = match_date
        if actual_match_day == yesterday:
            has_scheduled_match = True
            match_info = m
            break

if not has_scheduled_match:
    exit(0)

# 2. 查 ESPN 获取实际比赛结果
TEAM_ABBR = {
    "MIL": "AC米兰", "INT": "国际米兰", "JUV": "尤文图斯",
    "NAP": "那不勒斯", "LAZ": "拉齐奥", "ROM": "罗马", "ROMA": "罗马",
    "ATA": "亚特兰大", "FIO": "佛罗伦萨", "TOR": "都灵", "BOL": "博洛尼亚",
    "LEC": "莱切", "CAG": "卡利亚里", "UDI": "乌迪内斯", "VER": "维罗纳",
    "SAS": "萨索洛", "PAR": "帕尔马", "GEN": "热那亚",
    "CRE": "克雷莫内塞", "PIS": "比萨", "COMO": "科莫",
}

def get_name(abbr):
    return TEAM_ABBR.get(abbr, abbr)

r = subprocess.run(
    ["/usr/bin/curl", "-s",
     "https://site.api.espn.com/apis/site/v2/sports/soccer/ita.1/teams/103/schedule?limit=5"],
    capture_output=True, text=True, timeout=15
)

data = json.loads(r.stdout)
home = away = home_score = away_score = result_str = opponent_en = ""

for e in data.get("events", []):
    dt = datetime.fromisoformat(e.get("date", "").replace("Z", "+00:00")).astimezone(tz_sh)
    matched = (dt.strftime("%Y-%m-%d") == yesterday) or \
              (dt.hour < 8 and (dt - timedelta(days=1)).strftime("%Y-%m-%d") == yesterday)
    if not matched:
        continue

    home_won = away_won = False
    home_abbr = away_abbr = ""

    for c in e.get("competitions", [{}]):
        for comp in c.get("competitors", []):
            abbr = comp.get("team", {}).get("abbreviation", "")
            score = comp.get("score", {})
            sv = score.get("displayValue", "?") if isinstance(score, dict) else str(score)
            winner = score.get("winner", False) if isinstance(score, dict) else False
            if comp.get("homeAway") == "home":
                home = get_name(abbr); home_score = sv; home_won = winner; home_abbr = abbr
            else:
                away = get_name(abbr); away_score = sv; away_won = winner; away_abbr = abbr

    milan_is_home = "AC米兰" in home
    opponent_en = comp.get("team", {}).get("displayName", away_abbr if not milan_is_home else home_abbr)

    if milan_is_home:
        result_str = "胜 ✅" if home_won else ("平 🤝" if home_score == away_score else "负 ❌")
    else:
        result_str = "胜 ✅" if away_won else ("平 🤝" if home_score == away_score else "负 ❌")
    break

if not result_str:
    exit(0)

# 3. YouTube 精彩集锦搜索链接
opp_name = match_info.get("short", "").replace("MIL", "").replace("@", "").strip()
yt_query = f"AC+Milan+{opp_name}+highlights+Serie+A".replace(" ", "+")
youtube_url = f"https://www.youtube.com/results?search_query={yt_query}"

# 4. Google News 最新新闻（取前3条）
news_query = f"AC+Milan+{opp_name}+Serie+A".replace(" ", "+")
rss_url = f"https://news.google.com/rss/search?q={news_query}&hl=en&gl=US&ceid=US:en"

news_r = subprocess.run(
    ["/usr/bin/curl", "-s", "-L", "--max-time", "10", rss_url],
    capture_output=True, text=True, timeout=15
)

news_items = []
for item in re.findall(r'<item>(.*?)</item>', news_r.stdout, re.DOTALL):
    title_m = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
    link_m = re.search(r'<link>(.*?)</link>', item)
    if not title_m:
        title_m = re.search(r'<title>(.*?)</title>', item)
    if title_m and link_m:
        title = title_m.group(1).strip()
        link = link_m.group(1).strip()
        if title and link:
            news_items.append((title, link))
    if len(news_items) >= 3:
        break

# 5. 输出完整推送
print(f"⚽ AC米兰 {result_str}")
print(f"比分：{home} {home_score} - {away_score} {away}")
print(f"赛事：意甲联赛（Serie A）")
print()
print(f"🎬 精彩集锦：{youtube_url}")

if news_items:
    print()
    print("📰 赛后新闻：")
    for i, (title, link) in enumerate(news_items, 1):
        print(f"{i}. {title}")
        print(f"   {link}")
