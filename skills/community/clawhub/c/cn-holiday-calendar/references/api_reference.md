# Gov Holiday Reference

## Search Endpoint

`POST https://sousuoht.www.gov.cn/athena/forward/2B22E8E39E850E17F95A016A74FCB6B673336FA8B6FEC0E2955907EF9AEE06BE`

Use this endpoint to search gov.cn holiday notices.

### Dynamic request values

- `T-T`: current Unix timestamp in milliseconds
- `T-SIGN`: `md5(T-KEY + T-SEC + T-T + "TRS")`
- `searchWord`: query text such as `节假日安排`
- `pageNo` and `pageSize`: pagination controls

### Static request values

- `code`: `17da70961a7`
- `dataTypeId`: `107`
- `orderBy`: `time`
- `searchBy`: `title`
- `granularity`: `ALL`
- `trackTotalHits`: `true`
- `athenaAppKey`: captured encoded key from the browser session
- `athenaAppName`: `%E5%9B%BD%E7%BD%91%E6%90%9C%E7%B4%A2`
- `T-KEY`: `irs-c-box`
- `T-SEC`: `99b2eeecb4f10339`

### Search response

The result list lives at:

`result.data.middle.list`

Useful fields in each item:

- `title`
- `title_no_tag`
- `url`
- `linkUrl`
- `sourceUrl`
- `summary`
- `time`

## Notice Body Extraction

Fetch the selected notice URL with `requests`, set the response encoding from `apparent_encoding`, and extract the main article text from:

- `div.trs_editor_view`
- fallback: `#UCAP-CONTENT`

## Cache Schema

The skill cache stores one file per year:

`cache/YYYY.json`

Recommended shape:

```json
{
  "year": 2026,
  "notice_title": "国务院办公厅关于2026年部分节假日安排的通知",
  "notice_url": "https://www.gov.cn/gongbao/2025/issue_12406/202511/content_7048922.html",
  "special_days": [
    {
      "date": "2026-01-01",
      "workday": false,
      "holiday": "元旦",
      "kind": "holiday"
    }
  ]
}
```

Interpretation rules:

- If `workday` is `false`, the date is a holiday rest day.
- If `workday` is `true` and `holiday` is present, the date is a make-up workday.
- If a date is absent from `special_days`, use the normal weekday rule only as a fallback.
