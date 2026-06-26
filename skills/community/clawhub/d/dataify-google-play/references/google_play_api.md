# Dataify Google Play API Reference

Endpoint: `POST https://scraperapi.dataify.com/request`

Authentication header: `Authorization: Bearer <DATAIFY_API_TOKEN>`

The Python script stores the endpoint as a constant. Do not read the API URL from the current environment.

Submit requests as form data with `Content-Type: application/x-www-form-urlencoded`. Do not send the API body as JSON.

## Form Fields

Complete request field checklist:

| Field | Required | Default | Description |
| --- | --- | --- | --- |
| `engine` | yes | `google_play` | Fixed Dataify engine value for Google Play. |
| `q` | yes | none | Query to search in the Google Play app store. |
| `json` | yes | `1` | Output format. |
| `hl` | no | none | Google Play language code, such as `en`, `zh-cn`, `ja`, or `fr`. |
| `gl` | no | `us` | Google Play country/region code. The API docs state `us` is the default. |
| `apps_category` | no | none | Google Play app category. |
| `next_page_token` | no | none | Token for the next page of results. Do not combine with `section_page_token`, `see_more_token`, or `chart`. |
| `section_page_token` | no | none | Token for paginated results from a section. Do not combine with `next_page_token`, `see_more_token`, or `chart`. |
| `chart` | no | none | Shows a popular ranking chart, returning up to 50 results. Do not combine with pagination or see-more tokens. |
| `see_more_token` | no | none | Token for a section's "see more" results. Do not combine with `section_page_token`, `next_page_token`, or `chart`. |
| `store_device` | no | `phone` | Device used to browse/rank results. Do not combine with `apps_category` or `q`. |
| `age` | no | none | Age-range subcategory. Use only when `apps_category` is `FAMILY`. |
| `no_cache` | no | `false` | Set `true` to bypass the default 5-minute cache, or `false` to use cache. |

Use only documented defaults. Do not treat examples as defaults.

## Output Modes

| User asks for | `json` |
| --- | --- |
| JSON | `1` |
| JSON plus HTML | `2` |
| HTML | `3` |
| Light JSON | `4` |

## Common Categories

| Category | `apps_category` |
| --- | --- |
| Wear OS | `ANDROID_WEAR` |
| Art & Design | `ART_AND_DESIGN` |
| Auto & Vehicles | `AUTO_AND_VEHICLES` |
| Beauty | `BEAUTY` |
| Books & Reference | `BOOKS_AND_REFERENCE` |
| Business | `BUSINESS` |
| Comics | `COMICS` |
| Communication | `COMMUNICATION` |
| Dating | `DATING` |
| Education | `EDUCATION` |
| Entertainment | `ENTERTAINMENT` |
| Events | `EVENTS` |
| Finance | `FINANCE` |
| Food & Drink | `FOOD_AND_DRINK` |
| Health & Fitness | `HEALTH_AND_FITNESS` |
| House & Home | `HOUSE_AND_HOME` |
| Libraries & Demo | `LIBRARIES_AND_DEMO` |
| Lifestyle | `LIFESTYLE` |
| Maps & Navigation | `MAPS_AND_NAVIGATION` |
| Medical | `MEDICAL` |
| Music & Audio | `MUSIC_AND_AUDIO` |
| News & Magazines | `NEWS_AND_MAGAZINES` |
| Parenting | `PARENTING` |
| Personalization | `PERSONALIZATION` |
| Photography | `PHOTOGRAPHY` |
| Productivity | `PRODUCTIVITY` |
| Shopping | `SHOPPING` |
| Social | `SOCIAL` |
| Sports | `SPORTS` |
| Tools | `TOOLS` |
| Travel & Local | `TRAVEL_AND_LOCAL` |
| Video Players & Editors | `VIDEO_PLAYERS` |
| Watch Faces | `WATCH_FACE` |
| Weather | `WEATHER` |
| Kids / Family | `FAMILY` |

## Device Values

| Device | `store_device` |
| --- | --- |
| Phone | `phone` |
| Tablet | `tablet` |
| TV | `tv` |
| Chromebook | `chromebook` |
| Watch | `watch` |
| Car | `car` |

## Age Values

| Age range | `age` |
| --- | --- |
| 5 and under | `AGE_RANGE1` |
| 6 to 8 | `AGE_RANGE2` |
| 9 to 12 | `AGE_RANGE3` |

## Examples

Search Google Play in English from the United States:

```json
{"q":"meditation app","json":"1","gl":"us","hl":"en"}
```

Search Japanese Google Play and include HTML:

```json
{"q":"fitness","json":"2","gl":"jp","hl":"ja"}
```

Browse family apps for ages 6 to 8:

```json
{"q":"kids games","json":"1","apps_category":"FAMILY","age":"AGE_RANGE2"}
```
