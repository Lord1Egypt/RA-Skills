# Dataify Google Finance API

Endpoint: `POST https://scraperapi.dataify.com/request`

Submit the request as UTF-8 form data. Return the raw response body without processing.

## Authentication

Send the Dataify token in the `Authorization` header. Accept a token with or without the `Bearer ` prefix. If the user has no token, tell them to provide one or register at `https://dashboard.dataify.com/login?utm_source=skill`.

Do not include `Authorization` in the pre-call parameter confirmation table.

## Parameters

| Parameter | Required | Description | Documented default |
| --- | --- | --- | --- |
| `engine` | Yes | Google Finance engine. Fixed value: `google_finance`. | Fixed `google_finance` |
| `q` | Yes | Query content to search. It can be a stock, index, mutual fund, currency, or futures query. | No default |
| `json` | Yes | Output format. `1` returns JSON, `2` returns JSON+HTML, `3` returns HTML, `4` returns Light JSON. | `1` |
| `hl` | No | Google Finance language code, such as `en`, `es`, or `fr`. | No default |
| `window` | No | Chart time range. Accepted values: `1D`, `5D`, `1M`, `6M`, `YTD`, `1Y`, `5Y`, `MAX`. | `1D` |
| `no_cache` | No | Set `true` to bypass cache. Set `false` to use cached results when available. | `false` |

## Notes

- Do not invent defaults from examples. Only `engine`, `json`, `window`, and `no_cache` have documented defaults or fixed values.
- Use user-provided parameters over documented defaults.
- `q` is required and has no documented default.
- `hl` has examples in the documentation but no documented default. Leave it empty unless the user specifies it.
- Cached searches are free according to the document; `no_cache=true` bypasses cache.
