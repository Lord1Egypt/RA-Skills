# Modes and parameters

Read this reference only when selecting a non-default mode or mapping advanced fields.

## URL Mode Parameters

Use this section only when the user chooses `url`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | `https://www.youtube.com/@mrbeast` | YouTube channel URL. The URL must use the `https://www.youtube.com` domain. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Use the default when the user does not change it. |


Also ask: "Do you want to collect multiple YouTube profile URL groups? If yes, provide multiple `url` values."

URL mode handling:

- Accept only URLs whose scheme and host are exactly `https://www.youtube.com`. Reject any other scheme, host, or subdomain as non-compliant.
- Submit `spider_id=youtube_profiles_by-url`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"url":"https://www.youtube.com/@mrbeast"}]
```

## Keyword Mode Parameters

Use this section only when the user chooses `keyword`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `keyword` | Yes | `MrBeast` | Keyword used to search YouTube channels or profiles. |
| `page_turning` | Yes | `1` | Integer greater than or equal to `0`. Specifies how many search result pages to collect. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Use the default when the user does not change it. |


Also ask: "Do you want to collect multiple YouTube profile keyword groups? If yes, provide multiple groups of `keyword` and `page_turning`."

Keyword mode handling:

- Trim leading and trailing whitespace from `keyword`.
- `keyword` cannot be empty.
- `page_turning` is required. Default: `1`. It must be an integer greater than or equal to `0`.
- Submit numeric values as strings to match the Builder examples, for example `"page_turning":"1"`.
- Submit `spider_id=youtube_profiles_by-keyword`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"keyword":"MrBeast","page_turning":"1"}]
```
