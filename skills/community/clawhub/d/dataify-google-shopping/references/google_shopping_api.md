# Dataify Google Shopping API Reference

Endpoint: `POST https://scraperapi.dataify.com/request`

Submit the request as form data using UTF-8 encoding. The API URL is fixed and must not be read from the environment.

## Complete Parameter Table

Use this field list for the required pre-call preview table. Do not use example values as defaults.

| 参数名 | 默认值 | 说明 |
|---|---|---|
| Authorization | 无 | Header. Dataify API token. Accept a raw token or a value prefixed with `Bearer `. If missing, ask the user to provide a token or register at https://dashboard.dataify.com/login?utm_source=skill. Mask this value in previews. |
| engine | google_shopping | Body. Fixed engine value for Google Shopping. Always send `google_shopping`. |
| q | 无 | Body. Required shopping search query. |
| json | 1 | Body. Output format: `1` JSON, `2` JSON+HTML, `3` HTML, `4` Light JSON. |
| google_domain | google.com | Body. Google domain to use. |
| gl | 空 | Body. Two-letter country or region code for Google behavior, such as `us`, `uk`, `fr`, `cn`, or `jp`. |
| hl | 空 | Body. Interface/search language code, such as `en`, `zh-cn`, `es`, `fr`, or `ja`. |
| location | 空 | Body. Geographic location where the search originates. Do not use together with `uule`. |
| uule | 空 | Body. Google encoded location. If present, omit `location`. |
| start | 空 | Body. Result offset for pagination. For page N, commonly use `(N - 1) * 10`. |
| shoprs | 空 | Body. Raw Google Shopping filter token. When using `shoprs`, `q` may be unnecessary. Join multiple filters with `\|\|`. |
| min_price | 空 | Body. Lower bound for price filtering. Overrides the matching price filter embedded in `shoprs`. |
| max_price | 空 | Body. Upper bound for price filtering. Overrides the matching price filter embedded in `shoprs`. |
| sort_by | 空 | Body. Shopping sort order. Use `1` for price low to high and `2` for price high to low. Overrides the matching sort filter embedded in `shoprs`. |
| free_shipping | 空 | Body. Set to `true` to show only products with free shipping. Overrides the matching filter embedded in `shoprs`. |
| on_sale | 空 | Body. Set to `true` to show only sale or promotional products. Overrides the matching filter embedded in `shoprs`. |
| small_business | 空 | Body. Set to `true` to show only products from small businesses. Overrides the matching filter embedded in `shoprs`. |
| no_cache | false | Body. Set to `true` to bypass cached results. Default behavior uses cache. |

## Request Notes

- Required fields: `Authorization`, `engine`, and either a clear `q` or a raw `shoprs` token that represents the search/filter state.
- Prefer `q` for normal shopping searches.
- Keep all submitted form values as strings.
- Return the raw API response body exactly as received.
