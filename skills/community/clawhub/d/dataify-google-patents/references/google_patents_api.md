# Dataify Google Patents API Reference

Endpoint: `POST https://scraperapi.dataify.com/request`

Authentication header: `Authorization: Bearer <DATAIFY_API_TOKEN>`

The Python script stores the endpoint as a constant. Do not read the API URL from the current environment.

Submit requests as form data with `Content-Type: application/x-www-form-urlencoded`. Do not send the API body as JSON. Encode form data as UTF-8.

## Documented Defaults

Use only these defaults when the user does not specify a value. Values marked as "omit" are API defaults that are activated by leaving the form field out.

| Field | Default value | Source from parameter description |
| --- | --- | --- |
| `Authorization` | none | No token default. Ask the user for a token or direct them to `https://dashboard.dataify.com/login?utm_source=skill`. |
| `engine` | `google_patents` | Fixed value for Google Patents. |
| `q` | none | No documented default. |
| `json` | `1` | Default output format is JSON. |
| `page` | `0` | Page `0` is the default first page. |
| `num` | none | No documented default. |
| `sort` | omit, relevance | Default sorting is by relevance. |
| `clustered` | none | No documented default. |
| `dups` | `family` | Default deduplication is by family. |
| `patents` | `true` | Patent results are included by default. |
| `scholar` | `false` | Google Scholar results are excluded by default. |
| `before` | none | No documented default. |
| `after` | none | No documented default. |
| `inventor` | none | No documented default. |
| `assignee` | none | No documented default. |
| `country` | none | No documented default. |
| `language` | none | No documented default. |
| `status` | none | No documented default. |
| `type` | none | No documented default. |
| `litigation` | none | No documented default. |
| `no_cache` | `false` | Cache is used by default. |

Do not treat sample values in the source document as defaults.

## Complete Parameter List

| Field | Meaning | Accepted values or format |
| --- | --- | --- |
| `Authorization` | Dataify API token in the request header. | `Bearer <token>`; the script adds `Bearer ` when omitted. |
| `engine` | API engine. | Always `google_patents`. |
| `q` | Patent search query. Semicolons can separate multiple search expressions. | Raw query string. |
| `json` | Output mode. | `1` JSON, `2` JSON+HTML, `3` HTML, `4` Light JSON. |
| `page` | Result page number. | `0` for first page, `1` for second page, and so on. |
| `num` | Results per page. | Minimum `10`, maximum `100`. |
| `sort` | Sort order. | `new` for newest, `old` for oldest, omit for relevance. |
| `clustered` | Group results. | `true` for grouped results. |
| `dups` | Deduplication mode. | `family` for family deduplication, `language` for publication deduplication. |
| `patents` | Include Google Patents results. | `true` or `false`; default `true`. |
| `scholar` | Include Google Scholar results. | `true` or `false`; default `false`. |
| `before` | Maximum result date. | `priority:YYYYMMDD`, `filing:YYYYMMDD`, or `publication:YYYYMMDD`. |
| `after` | Minimum result date. | `priority:YYYYMMDD`, `filing:YYYYMMDD`, or `publication:YYYYMMDD`. |
| `inventor` | Inventor filter. | One or more names. Use commas to separate names; wrap names containing commas in parentheses. |
| `assignee` | Assignee filter. | One or more names. Use commas to separate names; wrap names containing commas in parentheses. |
| `country` | Patent country or region filter. | One or more country/region codes separated by commas, such as `US`, `WO`, or `EP`. |
| `language` | Patent language filter. | One or more language names separated by commas. |
| `status` | Patent status filter. | `GRANT` or `APPLICATION`. |
| `type` | Patent type filter. | `PATENT` or `DESIGN`. |
| `litigation` | Litigation status filter. | `YES` or `NO`. |
| `no_cache` | Bypass cached results. | `true` to bypass cache, `false` to use cache. |

## Natural-Language Mapping Hints

- Search terms become `q`.
- "JSON", "JSON+HTML", "HTML", or "Light JSON" become `json` values `1`, `2`, `3`, or `4`.
- User-facing page numbers are one-based; API `page` is zero-based.
- "newest", "latest", or "最新" become `sort: "new"`.
- "oldest", "earliest", or "最早" become `sort: "old"`.
- "by relevance" or "默认相关性" means omit `sort`.
- "grouped" or "分组" becomes `clustered: "true"`.
- "family dedupe" or "家族去重" becomes `dups: "family"`.
- "publication dedupe" or "公开/公布去重" becomes `dups: "language"`.
- "granted" or "授权" becomes `status: "GRANT"`.
- "application" or "申请" becomes `status: "APPLICATION"`.
- "design" or "外观设计" becomes `type: "DESIGN"`.
- "patent type" or "专利类型" becomes `type: "PATENT"`.
- "with litigation" or "有诉讼" becomes `litigation: "YES"`.
- "without litigation" or "无诉讼" becomes `litigation: "NO"`.
- Date filters must include the date type when inferred from natural language: priority, filing, or publication.
