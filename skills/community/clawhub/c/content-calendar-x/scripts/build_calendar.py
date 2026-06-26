#!/usr/bin/env python3
"""
Content Calendar Builder
Usage: python3 build_calendar.py --config calendar_config.json
       python3 build_calendar.py --demo

Config JSON format:
{
  "brand": "Acme Corp",
  "start_date": "2026-04-01",
  "weeks": 4,
  "platforms": ["linkedin", "twitter"],
  "cadence": {"linkedin": 3, "twitter": 5},
  "pillars": [
    {"name": "Education", "pct": 40, "goal": "Awareness"},
    {"name": "Social Proof", "pct": 25, "goal": "Trust"},
    {"name": "Behind the Scenes", "pct": 20, "goal": "Engagement"},
    {"name": "Promotional", "pct": 15, "goal": "Conversion"}
  ]
}
"""

import json
import sys
import argparse
from datetime import datetime, timedelta

PLATFORM_FORMATS = {
    "linkedin": ["Text Post", "Carousel", "Poll", "Short Video"],
    "twitter": ["Thread", "Single Tweet", "Quote Tweet", "Poll"],
    "instagram": ["Carousel", "Reel", "Story", "Single Image"],
    "blog": ["How-To Guide", "Listicle", "Case Study", "Opinion Piece"],
    "youtube": ["Tutorial", "Case Study", "List Video", "Vlog"],
}

POSTING_DAYS = {
    "linkedin": [1, 2, 3, 4],   # Mon-Thu (0=Mon)
    "twitter": [0, 1, 2, 3, 4], # Mon-Fri
    "instagram": [1, 3, 5],     # Tue, Thu, Sat
    "blog": [1, 4],             # Tue, Fri
    "youtube": [3, 6],          # Thu, Sun
}


def get_post_days(start_date, weeks, platform, cadence):
    """Generate posting dates for a platform based on cadence."""
    preferred_days = POSTING_DAYS.get(platform, [0, 2, 4])
    all_dates = []
    current = start_date

    for _ in range(weeks * 7):
        if current.weekday() in preferred_days:
            all_dates.append(current)
        current += timedelta(days=1)

    # Sample based on cadence (posts per week)
    result = []
    week_count = {}
    for date in all_dates:
        week_num = date.isocalendar()[1]
        if week_count.get(week_num, 0) < cadence:
            result.append(date)
            week_count[week_num] = week_count.get(week_num, 0) + 1

    return result


def assign_pillars(dates, pillars):
    """Assign content pillars to dates based on percentages."""
    if not pillars or not dates:
        return []

    assignments = []
    total = len(dates)

    # Calculate how many posts per pillar
    pillar_counts = []
    remaining = total
    for i, pillar in enumerate(pillars):
        if i == len(pillars) - 1:
            count = remaining
        else:
            count = round(total * pillar["pct"] / 100)
            remaining -= count
        pillar_counts.append((pillar, count))

    # Interleave pillars for variety
    flat = []
    max_count = max(c for _, c in pillar_counts)
    for i in range(max_count):
        for pillar, count in pillar_counts:
            if i < count:
                flat.append(pillar)

    # Pair with dates
    for i, date in enumerate(dates):
        pillar = flat[i % len(flat)] if flat else {"name": "General", "goal": "Awareness"}
        assignments.append((date, pillar))

    return assignments


def format_post_entry(date, platform, pillar, post_num):
    formats = PLATFORM_FORMATS.get(platform, ["Post"])
    # Rotate formats
    fmt = formats[post_num % len(formats)]

    return {
        "date": date.strftime("%Y-%m-%d (%a)"),
        "platform": platform.capitalize(),
        "pillar": pillar["name"],
        "goal": pillar.get("goal", ""),
        "format": fmt,
        "hook": f"[Hook — {pillar['name']} angle, {fmt} format]",
        "body": "[Key points / talking points — fill in]",
        "cta": "[CTA — what should they do next?]",
        "hashtags": "[3–5 relevant hashtags]",
        "repurpose_as": "[Other platform / format this could become]",
        "status": "TODO"
    }


def build_markdown(brand, calendar_data):
    lines = [f"# Content Calendar — {brand}\n"]

    current_week = None
    for entry in calendar_data:
        date = datetime.strptime(entry["date"].split(" ")[0], "%Y-%m-%d")
        week_num = date.isocalendar()[1]

        if week_num != current_week:
            current_week = week_num
            lines.append(f"\n## Week {week_num}\n")

        lines.append(f"### {entry['date']} — {entry['platform']}")
        lines.append(f"- **Pillar:** {entry['pillar']} *(Goal: {entry['goal']})*")
        lines.append(f"- **Format:** {entry['format']}")
        lines.append(f"- **Hook:** {entry['hook']}")
        lines.append(f"- **Body:** {entry['body']}")
        lines.append(f"- **CTA:** {entry['cta']}")
        lines.append(f"- **Hashtags:** {entry['hashtags']}")
        lines.append(f"- **Repurpose as:** {entry['repurpose_as']}")
        lines.append(f"- **Status:** ☐ Draft  ☐ Scheduled  ☐ Published\n")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Content Calendar Builder")
    parser.add_argument("--config", help="JSON config file")
    parser.add_argument("--demo", action="store_true", help="Run with demo data")
    parser.add_argument("--output", help="Output markdown file")
    parser.add_argument("--format", default="markdown", choices=["markdown", "json"])
    args = parser.parse_args()

    if args.demo or (not args.config and sys.stdin.isatty()):
        config = {
            "brand": "YourBrand",
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "weeks": 4,
            "platforms": ["linkedin", "twitter"],
            "cadence": {"linkedin": 3, "twitter": 4},
            "pillars": [
                {"name": "Education", "pct": 35, "goal": "Awareness"},
                {"name": "Social Proof", "pct": 25, "goal": "Trust"},
                {"name": "Behind the Scenes", "pct": 25, "goal": "Engagement"},
                {"name": "Promotional", "pct": 15, "goal": "Conversion"}
            ]
        }
        print("Running in demo mode.\n", file=sys.stderr)
    elif args.config:
        with open(args.config) as f:
            config = json.load(f)
    else:
        config = json.loads(sys.stdin.read())

    start_date = datetime.strptime(config["start_date"], "%Y-%m-%d")
    weeks = config.get("weeks", 4)
    brand = config.get("brand", "Brand")
    pillars = config.get("pillars", [{"name": "General", "pct": 100, "goal": "Awareness"}])

    all_entries = []
    for platform in config.get("platforms", ["linkedin"]):
        cadence = config.get("cadence", {}).get(platform, 3)
        dates = get_post_days(start_date, weeks, platform, cadence)
        assignments = assign_pillars(dates, pillars)
        for i, (date, pillar) in enumerate(assignments):
            entry = format_post_entry(date, platform, pillar, i)
            all_entries.append(entry)

    # Sort by date
    all_entries.sort(key=lambda x: x["date"])

    if args.format == "json":
        output = json.dumps(all_entries, indent=2)
    else:
        output = build_markdown(brand, all_entries)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Calendar saved to {args.output}", file=sys.stderr)
    else:
        print(output)

    print(f"\n✅ Generated {len(all_entries)} posts across {len(config.get('platforms', []))} platforms over {weeks} weeks.", file=sys.stderr)


if __name__ == "__main__":
    main()
