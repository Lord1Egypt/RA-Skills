---
name: china-holiday-calendar-sync
description: Discover and parse China's official holiday notices from gov.cn, normalize holiday and adjusted-workday rows, and apply low-frequency probing rules for future years. Use when Codex needs to build or explain a China business calendar, sync official holiday schedules into storage, determine the first workday of a week, or implement holiday-aware weekly sending logic.
---

# China Holiday Calendar Sync

Use only official `gov.cn` holiday notices as the source of truth for China holiday and adjusted-workday schedules.

Keep the workflow conservative:

- Prefer configured `notice_urls` first.
- Use China government policy search for discovery before any public-search fallback.
- Parse official notice正文 into structured holiday/workday rows.
- Treat future-year discovery as low-frequency work, not a daily poll.

## Workflow

1. Load configured notice URLs.
   - Reuse known official notice URLs from local config first.
   - For already-synced years, prefer local calendar storage instead of refetching the notice page.

2. Discover missing future-year notices carefully.
   - Build exact queries around `国务院办公厅关于<year>年部分节假日安排的通知`.
   - Prefer China government policy search.
   - Accept only `https://www.gov.cn/zhengce/content/...` candidate pages.
   - Re-fetch the candidate and validate title/body before trusting it.

3. Throttle discovery.
   - For future years, probe at most once per month.
   - Default probe window starts on the 15th of the month.
   - Cache both positive and negative discovery results for that month.

4. Parse official notice content.
   - Extract holiday ranges such as `1月1日至3日`.
   - Extract adjusted workdays such as `1月4日（周日）上班`.
   - Emit normalized rows with `date`, `is_holiday`, `is_workday`, `holiday_name`, and `source_url`.

5. Persist two layers separately.
   - Stable source mapping in `notice_urls`
   - Probe history in `discovery_cache`

## Rules

- Do not use third-party holiday calendars as authoritative data.
- Do not fabricate future-year schedules before an official notice exists.
- If a future year has not been published yet, return no URL and cache that negative check for the month.
- If a year is already present in local holiday storage, do not refetch the official notice unless the caller explicitly wants a refresh.

## References

- For source priority, parsing regex patterns, and caching rules, read [references/official-notice-method.md](references/official-notice-method.md).

## Output Shape

Normalize notice parsing results into a shape close to:

```json
{
  "date": "2026-10-08",
  "is_holiday": false,
  "is_workday": true,
  "holiday_name": "国庆节调休上班",
  "source_url": "https://www.gov.cn/zhengce/content/202511/content_7047090.htm"
}
```
