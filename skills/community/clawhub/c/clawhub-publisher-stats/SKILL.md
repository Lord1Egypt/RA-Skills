---
name: clawhub-publisher-stats
description: Fetch live ClawHub publisher metrics for a specific user, including published skills, author rank, total downloads, stars, current installs, all-time installs, comments, and top-skill breakdowns. Use when users ask to 查某个 ClawHub/OpenClaw 用户发布了哪些 skill、查作者数据、查发布者表现、查技能市场数据、看安装量/下载量/星标/评论、统计某个作者的 skills、分析某个发布者的 marketplace performance, publisher stats, author stats, creator analytics, install counts, download counts, star counts, comment counts, top skills, or a per-skill metrics report.
---

# ClawHub Publisher Stats

Use this skill when the user wants marketplace data for a ClawHub publisher.

Common trigger phrases:
- 查某个用户发布了哪些 skill
- 查作者数据 / 查发布者数据
- 看某个 ClawHub 用户的安装量、下载量、星标
- 统计这个作者的 skills 表现
- 分析这个发布者的 marketplace performance
- fetch ClawHub publisher stats
- show this creator's skills and metrics
- get install/download/star counts for an author's skills

## Workflow

1. Run the bundled script:

```bash
python3 skills/clawhub-publisher-stats/scripts/fetch_clawhub_publisher_stats.py --user <handle> --limit 20 --format markdown
```

2. Use `--include-skill-pages` when the user needs per-skill install counts or comment counts:

```bash
python3 skills/clawhub-publisher-stats/scripts/fetch_clawhub_publisher_stats.py --user <handle> --limit 20 --include-skill-pages --format markdown
```

3. Use `--format json` when the user wants machine-readable output.

## Output Rules

- Always report the author aggregate block first when available:
  - rank
  - published skill count
  - total downloads
  - total stars
- Then report per-skill metrics for the returned skills.
- Call out source limitations explicitly:
  - the searchable API may return fewer skills than the aggregate author total
  - ClawHub public pages expose stars and comments, but may not expose a separate user rating field
- If skill-page fetches fail for some rows, keep the search API values and mark install/comment fields as unavailable.

## Notes

- Data is fetched live from public pages on each run.
- The script filters results to the exact publisher handle to avoid mixed search matches.
- Read `references/sources.md` only if you need to explain where the numbers come from.
