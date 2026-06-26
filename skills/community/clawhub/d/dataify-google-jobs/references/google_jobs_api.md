# Dataify Google Jobs API

Endpoint: `POST https://scraperapi.dataify.com/request`

Submit the request as form data. Use UTF-8. Return the raw response body without processing.

## Authentication

Send the Dataify token in the `Authorization` header. Accept a token with or without the `Bearer ` prefix. If the user has no token, tell them to provide one or register at `https://dashboard.dataify.com/login?utm_source=skill`.

## Parameters

| Parameter | Required | Description | Documented default |
| --- | --- | --- | --- |
| `Authorization` | Yes | Header containing the Dataify API token. | No default |
| `engine` | Yes | Google Jobs engine. Fixed value: `google_jobs`. | Fixed `google_jobs` |
| `q` | Yes | Job search query content. | No default |
| `json` | Yes | Output format. `1` returns JSON, `2` returns JSON+HTML, `3` returns HTML, `4` returns Light JSON. | `1` |
| `google_domain` | No | Google domain to use for the request. | `google.com` |
| `gl` | No | Google country/region code, usually a two-letter code such as `us`, `uk`, or `fr`. | No default |
| `hl` | No | Google Jobs language code, such as `en`, `es`, or `fr`. | No default |
| `location` | No | Geographic location where the search starts. Do not use together with `uule`. | No default |
| `uule` | No | Google encoded location for the search. Do not use together with `location`. | No default |
| `next_page_token` | No | Token for retrieving the next page of results. | No default |
| `chips` | No | Extra Google Jobs query/filter condition token extracted from the jobs page. | No default |
| `lrad` | No | Search radius in kilometers. | No default |
| `ltype` | No | Work-from-home filter. The document notes this parameter has been deprecated by Google. Accepted values include `true` or `1`. | No default |
| `uds` | No | Google-provided search filter string. | No default |
| `no_cache` | No | Set `true` to bypass cache. Set `false` to use cached results when available. | `false` |

## Notes

- Do not invent defaults from examples. Only `engine`, `json`, `google_domain`, and `no_cache` have documented defaults or fixed values.
- Use user-provided parameters over documented defaults.
- Before every API call, show the complete body parameter table excluding `Authorization`, then ask the user whether to modify values. Call the API only after the user confirms.
- For parameters with no documented default, leave the current value empty unless the user supplied a value.
- If `uule` and `location` are both provided, use `uule` and omit `location`.
- Cached searches are free according to the document; `no_cache=true` bypasses cache.
