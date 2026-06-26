# Dataify Google Videos API

Endpoint: `https://scraperapi.dataify.com/request`

Method: `POST`

Submission format: form data, encoded as `application/x-www-form-urlencoded` with UTF-8.

Return handling: return the raw response body directly to the user.

## Complete Parameter List

| Parameter | Default | Description |
|---|---|---|
| Authorization | none | Dataify API token in the `Authorization` header. Accept a user-provided token or `DATAIFY_API_TOKEN`; add `Bearer ` when missing. If unavailable, ask the user to provide a token or register at `https://dashboard.dataify.com/login?utm_source=skill`. |
| engine | google_videos | Fixed body value for Google Videos. |
| q | none | Required search query content. |
| json | 1 | Output format. `1` returns JSON, `2` returns JSON+HTML, `3` returns HTML, `4` returns Light JSON. |
| google_domain | google.com | Google domain to use. |
| gl | none | Two-letter country or region code for Google search behavior, such as `us`, `uk`, or `fr`. These are examples, not defaults. |
| hl | none | Language code for Google search UI/results, such as `en`, `es`, or `fr`. These are examples, not defaults. |
| location | none | Named geographic location to originate the search from. |
| uule | none | Google encoded location. Do not use together with `location`. |
| start | none | Result offset for pagination. For page N, commonly use `(N - 1) * 10`. |
| tbs | none | Advanced Google search parameters for filters such as date, duration, quality, or source. |
| no_cache | false | Set `true` to bypass cached results; set `false` to allow cache use. |
| lr | none | Restrict results to one or more languages, formatted like `lang_fr` or `lang_fr|lang_de`. |
| safe | none | Safe search level. Use `active` to enable or `off` to disable when requested. |
| nfpr | 0 | Whether to exclude results from autocorrected queries. `1` excludes them, `0` includes them. |
| filter | 0 | Similar and omitted results filter. `0` enables the filters, `1` disables them. |

## Script Notes

- Use `scripts/google_videos.py --preview-table` to generate the Markdown confirmation table.
- Use `scripts/google_videos.py --dry-run` to print the normalized form payload as JSON without calling the API.
- Call the API only after the user confirms the parameter table.
- Do not add undocumented defaults. In particular, examples such as `us`, `en`, `India`, or `true` are not defaults.
