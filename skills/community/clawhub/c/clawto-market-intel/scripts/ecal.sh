#!/usr/bin/env bash
# Economic Calendar — 本周宏观事件
set -euo pipefail

python3 << 'PYEOF'
from datetime import datetime, timedelta
import urllib.request, re, html
from xml.etree import ElementTree as ET

today = datetime.now()
week_start = today - timedelta(days=today.weekday())
week_end = week_start + timedelta(days=6)
next_week_start = week_end + timedelta(days=1)
next_week_end = next_week_start + timedelta(days=6)

# Major scheduled events for 2026
events = [
    # (date, time, name, country, impact 1-5)
    ("2026-05-07", "02:00", "美联储 FOMC 利率决议", "🇺🇸", 5),
    ("2026-05-08", "20:30", "美国 非农就业 NFP", "🇺🇸", 5),
    ("2026-05-07", "20:15", "欧央行 ECB 利率决议", "🇪🇺", 5),
    ("2026-05-06", "09:30", "中国 财新服务业 PMI", "🇨🇳", 4),
    ("2026-05-10", "09:30", "中国 CPI 消费者物价指数", "🇨🇳", 4),
    ("2026-05-01", "11:00", "日本央行 BOJ 利率决议", "🇯🇵", 4),
    ("2026-05-13", "20:30", "美国 CPI 消费者物价指数", "🇺🇸", 5),
    ("2026-05-14", "20:30", "美国 PPI 生产者物价指数", "🇺🇸", 4),
    ("2026-05-17", "10:00", "中国 规模以上工业增加值", "🇨🇳", 3),
    ("2026-05-20", "09:15", "中国 LPR 贷款市场报价利率", "🇨🇳", 5),
    ("2026-06-05", "20:30", "美国 非农就业 NFP", "🇺🇸", 5),
    ("2026-06-10", "20:30", "美国 CPI 消费者物价指数", "🇺🇸", 5),
    ("2026-06-18", "02:00", "美联储 FOMC 利率决议", "🇺🇸", 5),
    ("2026-06-19", "11:00", "日本央行 BOJ 利率决议", "🇯🇵", 4),
]

this_week = []
next_week = []

for date_str, time_str, name, country, impact in events:
    try:
        evt_date = datetime.strptime(date_str, "%Y-%m-%d")
    except:
        continue

    icon = {5:"🔴", 4:"🟠", 3:"🟡"}.get(impact, "⚪")
    day_label = evt_date.strftime("%m/%d")
    line = f"  {icon} {day_label} {time_str} | {country} {name}"

    if week_start <= evt_date <= week_end:
        this_week.append(line)
    elif next_week_start <= evt_date <= next_week_end:
        next_week.append(line)

# Try live hints from RSS
live_hints = []
try:
    req = urllib.request.Request(
        "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114",
        headers={"User-Agent": "Mozilla/5.0"})
    xml_text = urllib.request.urlopen(req, timeout=8).read().decode("utf-8", errors="replace")
    xml_text = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', '&amp;', xml_text)
    root = ET.fromstring(xml_text)
    keywords = ['fed', 'cpi', 'ppi', 'gdp', 'nfp', 'jobs', 'payroll', 'inflation',
                'rate decision', 'ecb', 'boj', 'pboc', 'pmi', 'opec',
                'earnings', 'data', 'calendar', 'week ahead']
    for item in root.findall(".//item")[:8]:
        title_el = item.find("title")
        if title_el is not None and title_el.text:
            title = html.unescape(title_el.text.strip())
            if any(kw in title.lower() for kw in keywords):
                live_hints.append(f"  💬 {title}")
except:
    pass

# Output
print(f"\n===== 财经日历 =====\n")
print(f"本周 ({week_start.strftime('%m/%d')}~{week_end.strftime('%m/%d')})")
if this_week:
    for l in this_week:
        print(l)
else:
    print("  (暂无重要事件)")

print()
print(f"下周预告 ({next_week_start.strftime('%m/%d')}~{next_week_end.strftime('%m/%d')})")
if next_week:
    for l in next_week:
        print(l)
else:
    print("  (待更新)")

if live_hints:
    print(f"\n相关快讯:")
    for h in live_hints[:3]:
        print(h)

print(f"\n🔴=高影响  🟠=中高  🟡=中等")
print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M CST')}")
PYEOF
