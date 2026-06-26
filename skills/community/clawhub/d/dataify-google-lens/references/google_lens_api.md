# Dataify Google Lens API Reference

Endpoint: `POST https://scraperapi.dataify.com/request`

Authentication header: `Authorization: Bearer <DATAIFY_API_TOKEN>`

The Python script stores the endpoint as a constant. Do not read the API URL from the current environment.

Submit requests as form data with `Content-Type: application/x-www-form-urlencoded`. Do not send the API body as JSON. Encode request data as UTF-8.

## Parameters

Show this complete field list before every API call. The preview table must contain only: parameter name, current value, default value, and description. Do not include `Authorization` in that table.

| Parameter | Required | Default | Description |
| --- | --- | --- | --- |
| `engine` | yes | `google_lens` | Fixed engine value for Google Lens. |
| `url` | yes | none | Image URL to search with Google Lens. Do not use an example URL as a default. |
| `json` | yes | `1` | Output mode. |
| `hl` | no | none | Google Lens language/interface language code, such as `en`, `zh-cn`, `ja`, or `fr`. These are examples, not defaults. |
| `country` | no | none | Two-letter country or region code for Google Lens, such as `us`, `fr`, or `de`. These are examples, not defaults. |
| `type` | no | `all` | Google Lens result type. |
| `q` | no | none | Extra search query/refinement used with `type=all`, `type=visual_matches`, or `type=products`. |
| `safe` | no | none | Adult-content filter level. Accepted values: `active` or `off`. |
| `no_cache` | no | `false` | Use `true` to bypass cache; use `false` to use cached results when available. |

## Output Modes

| User asks for | `json` |
| --- | --- |
| JSON | `1` |
| JSON plus HTML | `2` |
| HTML | `3` |
| Light JSON | `4` |

## Lens Types

| User asks for | `type` |
| --- | --- |
| All results | `all` |
| Products | `products` |
| About this image | `about_this_image` |
| Exact matches | `exact_matches` |
| Visual matches, similar images | `visual_matches` |

`q` is only meaningful with `all`, `visual_matches`, or `products`.

## Examples

These are examples only. Do not treat example values as defaults.

Search Lens with default JSON output:

```json
{"url":"https://example.com/image.jpg"}
```

Search product matches in the United States:

```json
{"url":"https://example.com/shoe.jpg","type":"products","country":"us"}
```

Return JSON plus HTML and bypass cache:

```json
{"url":"https://example.com/item.png","json":"2","no_cache":"true"}
```
