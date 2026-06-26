# Dataify Google Maps API Reference

Endpoint: `POST https://scraperapi.dataify.com/request`

Submit the request as UTF-8 encoded form data (`application/x-www-form-urlencoded`). Do not send JSON as the request body.

## Required Parameters

| Field | Location | Default | Description |
|---|---|---:|---|
| `engine` | body | `google_maps` | Fixed engine value for this skill. |
| `q` | body | none | Google Maps query text to search. |
| `json` | body | `1` | Output format: `1` JSON, `2` JSON+HTML, `3` HTML, `4` Light JSON. |

Do not show `Authorization` in the pre-call parameter table. Token handling belongs to the skill workflow, not the user-facing parameter table.

## Optional Parameters

| Field | Default | Description |
|---|---:|---|
| `ll` | none | Full Maps origin coordinate string. Format: `@latitude,longitude,zoomz` or `@latitude,longitude,heightm`. Do not combine with `location`, `lat`, `lon`, `z`, or `m`. |
| `location` | none | Named search origin. Use with `z` or `m`. Do not combine with `ll`, `lat`, or `lon`. |
| `lat` | none | Search origin latitude. Must be used with `lon` and with either `z` or `m`. Do not combine with `ll` or `location`. |
| `lon` | none | Search origin longitude. Must be used with `lat` and with either `z` or `m`. Do not combine with `ll` or `location`. |
| `z` | none | Map zoom level. Use as the scale component for `location` or `lat`/`lon`. Do not combine with `m`. |
| `m` | none | Map height in meters. Use as the scale component for `location` or `lat`/`lon`. Do not combine with `z`. |
| `nearby` | none | Force results closer to the supplied origin. Use with `ll`, `location`, or `lat`/`lon`; especially useful for "near me" queries with an origin. |
| `google_domain` | `google.com` | Google domain to use. |
| `hl` | none | Google Maps interface/search language code, such as `en`, `fr`, or `zh-cn`. These are examples, not defaults. |
| `gl` | none | Google country/region code, such as `us`, `uk`, or `fr`. These are examples, not defaults. |
| `start` | `0` | Result offset for pagination. Page 1 is `0`, page 2 is `20`, page 3 is `40`. |
| `type` | none | Search type. Use `search` for result lists or `place` for a specific-place lookup using `data`. `place_id` and `data_cid` do not require `type`. |
| `data` | none | Deprecated place/result filter. Prefer `place_id` or `data_cid`. |
| `place_id` | none | Unique Google Maps place ID. |
| `data_cid` | none | Google Maps CID. Do not combine with `place_id`. |
| `no_cache` | `false` | Set to `true` to bypass cached results; set to `false` to allow cache. |

## Constraints

- Use only one location-origin style: `ll`, `location`, or `lat`/`lon`.
- Use `lat` and `lon` as a pair.
- Use only one scale style: `z` or `m`.
- Use one of `z` or `m` when passing `location` or `lat`/`lon`.
- Use `nearby` only when an origin is present.
- Do not send `place_id` and `data_cid` together.
- Use defaults only when the parameter description documents a default and the user did not specify a value.
- Do not treat documentation examples as defaults. Only `engine=google_maps`, `json=1`, `google_domain=google.com`, `start=0`, and `no_cache=false` are defaults documented for this skill.

## Pre-Call Confirmation Table

Before every real API call, show a complete table with exactly these columns and all body parameters. Omit `Authorization`.

| 参数名 | 当前值 | 默认值 | 说明 |
|---|---|---|---|
| `engine` | current or `google_maps` | `google_maps` | Fixed engine value. |
| `q` | current or empty | none | Google Maps query text. |
| `json` | current or `1` | `1` | Output format: `1` JSON, `2` JSON+HTML, `3` HTML, `4` Light JSON. |
| `ll` | current or empty | none | Full Maps origin coordinate string. |
| `location` | current or empty | none | Named search origin. |
| `lat` | current or empty | none | Search origin latitude. |
| `lon` | current or empty | none | Search origin longitude. |
| `z` | current or empty | none | Map zoom level. |
| `m` | current or empty | none | Map height in meters. |
| `nearby` | current or empty | none | Force results closer to the supplied origin. |
| `google_domain` | current or `google.com` | `google.com` | Google domain to use. |
| `hl` | current or empty | none | Google Maps language code. |
| `gl` | current or empty | none | Google country/region code. |
| `start` | current or `0` | `0` | Result offset for pagination. |
| `type` | current or empty | none | Search type, `search` or `place`. |
| `data` | current or empty | none | Deprecated result filter. |
| `place_id` | current or empty | none | Unique Google Maps place ID. |
| `data_cid` | current or empty | none | Google Maps CID. |
| `no_cache` | current or `false` | `false` | Whether to bypass cached results. |

## Natural-Language Mapping Notes

- "返回 JSON" -> `json=1`
- "返回 JSON+HTML" -> `json=2`
- "返回 HTML" -> `json=3`
- "Light JSON" -> `json=4`
- "第 N 页" or "page N" -> `start=(N-1)*20`
- "不走缓存", "跳过缓存", "no cache", "bypass cache" -> `no_cache=true`
- "附近", "near me", "nearby" with an origin -> `nearby=true`
- "详情", "place details", or "地点详情" with `data` -> `type=place`
- "搜索列表", "search results", or ordinary searches -> `type=search` when the type is explicitly requested
