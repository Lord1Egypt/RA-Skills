---
name: cn-holiday-calendar
description: Query gov.cn Chinese holiday notices to determine workdays, holidays, and make-up workdays. Use when the user needs to check whether a specific date is a workday, generate a month's date list with workday status, or inspect holiday names and make-up shifts from official State Council notices.
---

# CN Holiday Calendar

## Overview

Use this skill to answer date questions that depend on China's holiday schedule rather than a simple Monday-to-Friday rule. It handles statutory holidays, weekend make-up workdays, ordinary weekdays using official gov.cn notices, and calendar queries based on `lunar-python`.

## Environment

Before using this skill, make sure the runtime environment is ready:

- `python3` available in the active environment
- `lunar-python` installed in that same environment
- network access available only when the year cache needs to be refreshed from gov.cn

If you are setting up the environment manually, install the dependency first and then verify the skill script can import `lunar_python` before relying on detailed calendar output.

## Input Modes

Support two input shapes:

1. `YYYY-MM`
2. `YYYY-MM-DD`

If the input is a month, return every date in that month with:

- Date
- Weekday
- Workday status
- Holiday or make-up shift name if present
- Lunar date summary
- Optional solar term summary if present

If the input is a single date, return a short structured summary that includes:

- Specific date
- Lunar date
- Weekday
- Whether it is a holiday
- Holiday name if it is a holiday or make-up day
- Solar term if present

When answering holiday/workday queries, always include the date's lunar summary by default. If the user asks for more, return the expanded calendar information for the date.

## Workflow

Resolve the target year's holiday data first:

1. Look for `cache/YYYY.json` inside this skill.
2. If the file exists, use it to answer directly.
3. If the file does not exist, say `正在获取{年份}年最新节假日安排` once, then call `gov_search()` from `scripts/query_holiday.py` to search gov.cn for `{年份} 节假日安排`.
4. Use this prompt to pick the best search result:

   `从下列查询结果的标题中选择最适配 {年份} 节假日安排的一个，并给我对应查询结果的链接：{查询结果}`

5. Fetch the selected notice page body with `fetch_notice_body(url)`.
6. Use this prompt to turn the notice body into JSON:

   `这是国务院关于节假日安排的通知，请从这个通知里解析出节假日放假的日期和因为假期调休为工作日的日期：{通知内容}，以json的形式体现`

7. Validate the JSON before caching it. At minimum, it should contain:
   - `year`
   - `notice_title`
   - `notice_url`
   - `special_days`
8. Save the validated result as `cache/{年份}.json`.
9. If you need a one-shot helper, use `refresh_year(year)` from `scripts/query_holiday.py`, or the CLI `refresh` command.
10. For lunar calendar data, use `lunar-python` through `scripts/query_holiday.py`.

## Interpretation Rules

- Do not infer workday status from weekdays alone.
- Treat weekend make-up shifts as workdays.
- Treat holiday rest days as non-workdays even if they fall on Monday to Friday.
- If the cache has a matching date, use it first.
- If the cache does not list a date, fall back to the normal weekday rule: Monday to Friday are workdays, Saturday and Sunday are not.
- Do not mention cache hits, cache refresh, or other internal retrieval steps in the user-facing answer; only present the final skill result.
- If you need a progress line, use only `正在获取{年份}年最新节假日安排` and nothing about cache.
- For normal answers, include the lunar date summary and the most relevant solar term information if available. If the user explicitly asks for more calendar detail, return the expanded lunar calendar information.

## Output Format

For a month query, output a compact table:

- `date`
- `weekday`
- `workday`
- `kind`
- `holiday`
- `lunar`
- `jieqi`

For a single-date query, output a short structured summary with:

- `date`
- `weekday`
- `workday`
- `kind`
- `holiday`
- `lunar`
- `jieqi`

The user-facing answer should first state whether the date is a workday, then explicitly state the date, lunar date, weekday, whether it is a holiday, the holiday name if applicable, and the solar term if present. It must also remind the user that they can view more comprehensive information for that day.
For expanded calendar output, include a `calendar` object with the full lunar profile returned by `lunar-python`. That profile should include the standard fields plus the complete set of public no-arg `get*()` values exposed by the library.

## Lunar Coverage

The `lunar-python` package can provide more than lunar date and solar terms. Useful date-level information commonly available through the package includes:

- Lunar date strings and full lunar descriptions
- Current, previous, and next solar term information
- Heavenly stems and earthly branches for year, month, day, and time
- Zodiac information
- Lunar day auspicious and inauspicious activities
- Solar, lunar, and traditional festival names
- Eight characters and related calendar metadata
- Additional Chinese calendar metadata such as fu periods, seasons, and other traditional calendar attributes

Use the full calendar profile only when the user asks for more detail. For standard holiday/workday answers, keep the response concise and surface the lunar summary by default. In detail mode, expose the full `calendar` object rather than trimming it to a small hand-picked subset.

## Script

Use `scripts/query_holiday.py` as the primary entry point for deterministic search, notice-body extraction, cache loading, cache refresh, and date classification.
