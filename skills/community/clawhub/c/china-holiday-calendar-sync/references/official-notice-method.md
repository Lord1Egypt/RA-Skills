# Official Notice Method

## Source Priority

1. `notice_urls` in local config
2. Official China government policy search:
   - `https://sousuo.www.gov.cn/sousuo/search.shtml?code=17da70961a7&dataTypeId=107&searchWord=<query>`
3. Public-search fallback only if the official search page is temporarily unavailable

Only accept candidates matching:

```text
https://www.gov.cn/zhengce/content/<yyyymm>/content_<id>.htm
```

Then validate by fetching the candidate page again:

- `og:title` or `<title>` contains `国务院办公厅关于<year>年部分节假日安排的通知`
- or the official content block contains the same title text

## Query Strategy

Try exact and near-exact queries:

1. `国务院办公厅关于<year>年部分节假日安排的通知`
2. `<year>年 部分节假日安排 通知`
3. `<year>年 节假日安排 国务院办公厅`

## Parsing Rules

Holiday notice paragraphs typically look like:

```text
一、元旦：1月1日（周四）至3日（周六）放假调休，共3天。1月4日（周日）上班。
```

Recommended extraction:

- Holiday line: `^[一二三四五六七八九十]+、([^：]+)：(.+)$`
- Date range: `(?P<start_month>\d{1,2})月(?P<start_day>\d{1,2})日.*?至(?:(?P<end_month>\d{1,2})月)?(?P<end_day>\d{1,2})日`
- Single date: `(?P<month>\d{1,2})月(?P<day>\d{1,2})日`
- Adjusted workday: `(?P<month>\d{1,2})月(?P<day>\d{1,2})日（周[一二三四五六日天]）上班`

Mapping rules:

- Holiday ranges become one row per day with `is_holiday=true`
- Adjusted workdays become one row per day with `is_workday=true`
- Use `<holiday_name>调休上班` for adjusted workday names

## Frequency Rules

Use low-frequency discovery for future years:

- For `year <= current_year`: discovery may run immediately if the URL is unknown.
- For `year > current_year`: probe only from day `15` onward.
- Cache discovery results by month, not by day.

That means:

- If `2027` was checked on `2026-04-16` and no notice existed, skip all later checks in `2026-04`.
- Try again in `2026-05` once the probe window opens.

## Local Caching Pattern

Keep two different stores:

### `notice_urls`

Long-lived source-of-truth mapping once an official URL is confirmed.

```json
{
  "notice_urls": {
    "2026": "https://www.gov.cn/zhengce/content/202511/content_7047090.htm"
  }
}
```

### `discovery_cache`

Short-lived monthly probe history.

```json
{
  "discovery_cache": {
    "2027": {
      "checked_at": "2026-04-16",
      "url": null
    }
  }
}
```

## Scheduling Use

After holiday rows are in storage:

- determine `is_workday(date)`
- compute `first_workday_of_week(reference_day)`
- use that date to decide whether a weekly digest should send

For holiday-aware weekly sending in China, this official-calendar layer should gate the send day instead of plain weekday logic.
