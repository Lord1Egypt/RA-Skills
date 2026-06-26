# Dataify Google Images API Reference

Endpoint: `POST https://scraperapi.dataify.com/request`

Authentication header: `Authorization: Bearer <DATAIFY_API_TOKEN>`

The Python script stores the endpoint as a constant. Do not read the API URL from the current environment.

Submit requests as form data with `Content-Type: application/x-www-form-urlencoded`. Do not send the API body as JSON. Encode request data as UTF-8.

## Form Fields

Always include:

| Field | Required | Value or default |
| --- | --- | --- |
| `engine` | yes | Always `google_images` |
| `q` | yes | Image search query inferred from the user. No default; examples are not defaults. |
| `json` | yes | Output mode, default `1` |

Optional fields:

| Field | Meaning | Accepted values, format, or default |
| --- | --- | --- |
| `google_domain` | Google domain | Default `google.com`; examples include `google.com`, `google.co.jp`, `google.co.uk` |
| `gl` | Google country/region | Two-letter country/region code, e.g. `us`, `jp`, `fr`; no documented default |
| `hl` | Google language | Language code, e.g. `en`, `zh-cn`, `ja`, `fr`; no documented default |
| `cr` | Restrict result country | `country` + uppercase country code, e.g. `countryFR` |
| `lr` | Restrict result language | `lang_` + language code, e.g. `lang_fr` |
| `location` | Search origin location | Named location such as `United States`; do not use with `uule`, `lat`, or `lon` |
| `uule` | Google encoded location | Raw UULE value; do not use with `location`, `lat`, `lon`, or `radius` |
| `lat` | GPS latitude | Use together with `lon` |
| `lon` | GPS longitude | Use together with `lat` |
| `radius` | Location bias radius in meters | Desktop range `1` to `199`; tablet/mobile range `1` to `1000`; only meaningful with coordinates |
| `start` | Result offset | Default `0`; `10` for second page, `20` for third page |
| `tbm` | Search type | `isch` for Google Images; no documented default |
| `ludocid` | Google CID for a place | Raw CID value |
| `lsig` | Local/knowledge panel signature | Raw `lsig` value |
| `kgmid` | Google Knowledge Graph MID | Raw KGMID value |
| `si` | Cached search parameter | Raw `si` value |
| `ibp` | Layout/expansion parameter | Raw `ibp` value |
| `uds` | Search filter parameter | Raw `uds` value |
| `tbs` | Advanced Google search parameter | Raw Google `tbs` value for image filters |
| `safe` | Safe search | `active` or `off`; no documented default beyond Google behavior |
| `nfpr` | Exclude auto-corrected query results | Default `0`; use `1` to exclude auto-corrected results |
| `filter` | Similar/omitted result filter | Default `1`; use `0` to enable these filters |
| `device` | Device type | Default `desktop`; accepted `desktop`, `tablet`, `mobile` |
| `render_js` | Render JavaScript | `true` or `false`; no documented default |
| `no_cache` | Bypass cache | Default `false`; use `true` to bypass cache |
| `ai_overview` | Include Google AI Overview | `true` or `false`; no documented default |

Only the values explicitly labeled as defaults in this reference should be applied when the user does not specify a field. Example values from the original API documentation are not defaults.

## Pre-Call Parameter Table

Before calling the API, show the full field list except `Authorization` in a Markdown table with these exact columns:

| 参数名 | 当前值 | 默认值 | 说明 |
| --- | --- | --- | --- |

Rules:

- Include `engine` and every body field from the form field list.
- Set `当前值` to the value that will be sent after applying documented defaults, or leave it empty when the field will not be sent.
- Set `默认值` only when the parameter description documents a default. Leave it empty when no default is documented.
- Do not show `Authorization` or the API token in the table.
- Ask the user whether to modify any parameter, and call the API only after explicit confirmation.

## Output Modes

| User asks for | `json` |
| --- | --- |
| JSON | `1` |
| JSON plus HTML | `2` |
| HTML | `3` |
| Light JSON | `4` |

## Search Type

For Google Images use:

| User asks for | `tbm` |
| --- | --- |
| Images | `isch` |

The source documentation lists other Google verticals, but this skill is for `engine=google_images`; keep `tbm=isch` unless the user explicitly asks for a raw override.

Do not apply `tbm=isch` as a default when the user does not specify it.

## Parameter Conflict Rules

- `location` cannot be used with `uule`, `lat`, or `lon`.
- `uule` cannot be used with `location`, `lat`, `lon`, or `radius`.
- `lat` and `lon` must be supplied together.
- `radius` should only be used with `lat` and `lon`.

## Examples

Search Google Images with default JSON output:

```json
{"q":"red sneakers"}
```

Search Google Images on mobile from Japan with Japanese language:

```json
{"q":"東京 weather icons","json":"1","google_domain":"google.co.jp","gl":"jp","hl":"ja","device":"mobile"}
```

Get the second page with safe search enabled and cache bypassed:

```json
{"q":"modern kitchen design","start":"10","safe":"active","no_cache":"true"}
```
