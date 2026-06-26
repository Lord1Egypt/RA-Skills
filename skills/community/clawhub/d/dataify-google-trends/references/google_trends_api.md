# Dataify Google Trends API Reference

Endpoint: `POST https://scraperapi.dataify.com/request`

Authentication header: `Authorization: Bearer <DATAIFY_API_TOKEN>`

The Python script stores the endpoint as a constant. Do not read the API URL from the current environment.

Submit requests as form data with `Content-Type: application/x-www-form-urlencoded`. Do not send the API body as JSON.

## Complete Field List

| Field | Required | Default | Meaning |
| --- | --- | --- | --- |
| `Authorization` | yes | none | Dataify API token in the request header. If the token has no `Bearer ` prefix, add it before calling. Hide the actual value in parameter tables. |
| `engine` | yes | `google_trends` | Fixed engine value for Google Trends. |
| `q` | yes | none | Search query. The API documentation mentions `pizza` as an example/default, but the skill must not use it as a default; infer this from the user or ask. |
| `json` | yes | `1` | Output mode. |
| `hl` | no | unset | Google Trends language code, such as `en`, `zh-cn`, `es`, or `fr`. |
| `geo` | no | unset, meaning global | Search geography. |
| `region` | no | depends on `geo` | More specific region level for regional comparison or interest-by-region chart types. |
| `data_type` | no | unset | Google Trends data type. |
| `tz` | no | `420` | Timezone offset in minutes. Valid range: `-1439` to `1439`. |
| `cat` | no | `0` | Google Trends category, where `0` means all categories. |
| `gprop` | no | unset, meaning web search | Google property used to sort/filter results. |
| `date` | no | unset | Date or date range expression accepted by Google Trends. |
| `csv` | no | unset | Set to `true` to retrieve CSV results as an array. |
| `include_low_search_volume` | no | unset | Set to `true` to include low-search-volume regions. |
| `no_cache` | no | `false` | Set to `true` to bypass the 5-minute cache. |

## Output Modes

| User asks for | `json` |
| --- | --- |
| JSON | `1` |
| JSON plus HTML | `2` |
| HTML | `3` |
| Light JSON | `4` |

## Region Values

| User asks for | `region` |
| --- | --- |
| Country/region | `COUNTRY` |
| Subregion | `REGION` |
| DMA / metro | `DMA` |
| City | `CITY` |

## Data Types

| User asks for | `data_type` |
| --- | --- |
| Time trend analysis / interest over time | `TIMESERIES` |
| Regional comparison analysis | `GEO_MAP` |
| Regional interest distribution | `GEO_MAP_0` |
| Related topics | `RELATED_TOPICS` |
| Related queries | `RELATED_QUERIES` |

## Category Shortcuts

| User asks for | `cat` |
| --- | --- |
| All categories | `0` |
| Arts & Entertainment | `3` |
| Computers & Electronics | `5` |
| Finance | `7` |
| Games | `8` |
| Home & Garden | `11` |
| Business & Industrial | `12` |
| Internet & Telecom | `13` |
| People & Society | `14` |
| News | `16` |

## Google Properties

| User asks for | `gprop` |
| --- | --- |
| Image Search | `images` |
| News Search | `news` |
| Google Shopping | `froogle` |
| YouTube Search | `youtube` |
| Web Search | unset |

## Examples

Search Google Trends for AI in JSON:

```json
{"q":"AI","json":"1"}
```

Search United States English time trend results:

```json
{"q":"AI","json":"1","geo":"United+States","hl":"en","data_type":"TIMESERIES"}
```

Search related queries on YouTube and bypass cache:

```json
{"q":"AI","json":"1","gprop":"youtube","data_type":"RELATED_QUERIES","no_cache":"true"}
```
