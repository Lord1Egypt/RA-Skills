# Dataify Google Local API

Endpoint: `POST https://scraperapi.dataify.com/request`

Submit the request as `application/x-www-form-urlencoded` form data. Use UTF-8.

## Parameters

| Field | Location | Type | Required | Default | Description |
|---|---|---|---:|---|---|
| `Authorization` | header | string | yes | none | Dataify API token. Use `Bearer TOKEN`; the bundled script adds the prefix when omitted. |
| `engine` | body | string | yes | `google_local` | Fixed engine value for Google Local. |
| `q` | body | string | yes | none | Search query content. |
| `json` | body | string | yes | `1` | Output format. `1` returns JSON, `2` returns JSON+HTML, `3` returns HTML, `4` returns Light JSON. |
| `google_domain` | body | string | no | `google.com` | Google domain to use. |
| `gl` | body | string | no | none | Two-letter Google country/region code, for example `us`, `uk`, or `fr`. |
| `hl` | body | string | no | none | Google language code, for example `en`, `es`, or `fr`. |
| `location` | body | string | no | none | Geographic location where the search originates. If multiple locations match, Dataify/Google selects the most popular one. |
| `uule` | body | string | no | none | Google encoded location. `uule` and `location` cannot be used together. |
| `start` | body | string | no | none | Result offset for pagination. It skips the specified number of results. |
| `ludocid` | body | string | no | none | Google place CID/customer identifier. |
| `tbs` | body | string | no | none | Advanced search parameter not represented by the regular query field. |
| `no_cache` | body | string | no | `false` | Defaults to cached results when available. Set to `true` to bypass cache. |

## Output Modes

| `json` value | Meaning |
|---|---|
| `1` | JSON |
| `2` | JSON+HTML |
| `3` | HTML |
| `4` | Light JSON |

## Response

The API returns a raw HTTP response body. Typical successful responses contain `code`, `data.task_id`, and `data.result` fields, where `data.result` may include `html`, `json`, and `response_time`.
