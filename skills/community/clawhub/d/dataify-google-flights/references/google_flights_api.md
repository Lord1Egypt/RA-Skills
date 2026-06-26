# Dataify Google Flights API Reference

Endpoint: `POST https://scraperapi.dataify.com/request`

Authentication header: `Authorization: Bearer <DATAIFY_API_TOKEN>`

The Python script stores the endpoint as a constant. Do not read the API URL from the current environment.

Submit requests as form data with UTF-8 encoding and `Content-Type: application/x-www-form-urlencoded`. Do not send the API body as JSON.

## Required Fields

| Field | Required | Value or rule |
| --- | --- | --- |
| `Authorization` | yes | Dataify API token in the HTTP header. If absent, ask the user to provide a token or register at `https://dashboard.dataify.com/login?utm_source=skill`. |
| `engine` | yes | Always `google_flights`. |
| `json` | yes | Output mode. Default `1` for JSON. |

## Flight Inputs

The API marks flight inputs such as dates as optional body fields. Do not treat example dates or blank placeholders as defaults. For an initial route search, provide route fields when the user gives them; include dates only when the user asks for a dated itinerary.

| Search type | User intent fields |
| --- | --- |
| Round trip, `type=1` | Usually `departure_id`, `arrival_id`; include `outbound_date` and `return_date` when supplied |
| One-way, `type=2` | Usually `departure_id`, `arrival_id`; include `outbound_date` when supplied |
| Multi-city, `type=3` | `multi_city_json` |
| Continuation or return-leg lookup | `departure_token` when the user wants to choose a prior outbound flight and fetch the next leg |

## Form Fields

Only the documented defaults below are defaults. Do not use examples or blank placeholder values as defaults.

## Defaults Added To Payload

When the user does not provide these fields, the script adds the documented defaults below to the form payload:

| Field | Default |
| --- | --- |
| `engine` | `google_flights` |
| `json` | `1` |
| `currency` | `USD` |
| `type` | `1` |
| `travel_class` | `1` |
| `show_hidden` | `false` |
| `exclude_basic` | `false` |
| `deep_search` | `false` |
| `adults` | `1` |
| `children` | `0` |
| `infants_in_seat` | `0` |
| `infants_on_lap` | `0` |
| `sort_by` | `1` |
| `stops` | `0` |
| `bags` | `0` |
| `no_cache` | `false` |

| Field | Required | Default | Meaning | Accepted values or format |
| --- | --- | --- | --- | --- |
| `engine` | yes | `google_flights` | API engine | Fixed value `google_flights` |
| `departure_id` | no | none | Departure airport code or Google kgmid. Multiple values can be comma-separated. | `CDG`, `ORY`, `/m/04jpl` |
| `arrival_id` | no | none | Arrival airport code or Google kgmid. Multiple values can be comma-separated. | `LAX`, `/m/0vzm` |
| `json` | yes | `1` | Output format | `1` JSON, `2` JSON+HTML, `3` HTML, `4` Light JSON |
| `gl` | no | none | Google Flights country/region behavior | Two-letter country or region code such as `us`, `uk`, `fr`, `cn` |
| `hl` | no | none | Google Flights interface/search language | Language code such as `en`, `zh-cn`, `ja`, `fr` |
| `currency` | no | `USD` | Currency for returned prices | ISO currency code such as `USD`, `CNY`, `EUR`, `JPY` |
| `type` | no | `1` | Flight search type | `1` round trip, `2` one-way, `3` multi-city |
| `outbound_date` | no | none | Departure date | `YYYY-MM-DD` |
| `return_date` | no | none | Return date | `YYYY-MM-DD` |
| `travel_class` | no | `1` | Cabin class | `1` economy, `2` premium economy, `3` business, `4` first |
| `multi_city_json` | conditional | none | Multi-city flight legs as a JSON string | JSON string containing flight-leg objects |
| `show_hidden` | no | `false` | Include hidden flight results | `true` or `false` |
| `exclude_basic` | no | `false` | Exclude basic economy fares. Only applies to US domestic flights when `gl=us` and `travel_class=1`. | `true` or `false` |
| `deep_search` | no | `false` | Enable slower deep search for potentially better results | `true` or `false` |
| `adults` | no | `1` | Adult passenger count | Non-negative integer, normally at least `1` |
| `children` | no | `0` | Child passenger count | Non-negative integer |
| `infants_in_seat` | no | `0` | Infant passengers occupying seats | Non-negative integer |
| `infants_on_lap` | no | `0` | Infant passengers on lap | Non-negative integer |
| `sort_by` | no | `1` | Result sorting | `1` best/popular, `2` price, `3` departure time, `4` arrival time, `5` duration, `6` emissions |
| `stops` | no | `0` | Stop filter | `0` any stops, `1` nonstop only, `2` one stop or fewer, `3` two stops or fewer |
| `exclude_airlines` | no | none | Airline codes to exclude. Cannot be used with `include_airlines`. | Comma-separated airline codes |
| `include_airlines` | no | none | Airline codes to include. Cannot be used with `exclude_airlines`. | Comma-separated airline codes |
| `bags` | no | `0` | Carry-on bag count | Non-negative integer; should not exceed passengers allowed to carry bags |
| `max_price` | no | none | Maximum ticket price | Number in selected `currency`; no limit if omitted |
| `outbound_times` | no | none | Outbound time range | Two or four comma-separated hour numbers |
| `return_times` | no | none | Return time range | Two or four comma-separated hour numbers |
| `emissions` | no | none | Emissions filter | `1` low-emission flights only |
| `layover_duration` | no | none | Layover duration range in minutes | `min,max`, such as `90,330` |
| `exclude_conns` | no | none | Connection airport codes to exclude | Uppercase airport codes, comma-separated |
| `max_duration` | no | none | Maximum total flight duration in minutes | Integer minutes |
| `departure_token` | no | none | Token from a prior outbound result, used to select a flight and fetch a return or next-leg result | Raw token string |
| `no_cache` | no | `false` | Bypass cached results | `true` bypasses cache; `false` uses cached results |

## Natural-Language Mapping Hints

- Map "from X to Y", "X to Y", "从 X 到 Y", or "X 飞 Y" to `departure_id` and `arrival_id` when X/Y are airport codes or kgmids. If X/Y are city names and the airport is ambiguous, ask for a code.
- Map "往返", "round trip", or "return trip" to `type=1`; map "单程", "one-way", or "single trip" to `type=2`; map "多城市" or "multi-city" to `type=3`.
- Convert all dates to `YYYY-MM-DD`. Do not pass relative date text to the API.
- Map "中文" to `hl=zh-cn`, "English" to `hl=en`, and country/region requirements such as "美国地区" or "US results" to `gl=us`.
- Map passenger counts directly: adults -> `adults`, children -> `children`, infants with seat -> `infants_in_seat`, lap infants -> `infants_on_lap`.
- Map "直飞" or "nonstop" to `stops=1`; "最多一次中转" or "one stop or fewer" to `stops=2`.
- Map "只看低排放" or "low emission only" to `emissions=1`.
- Map "不走缓存", "跳过缓存", "no cache", or "bypass cache" to `no_cache=true`.

## Output Modes

| User asks for | `json` |
| --- | --- |
| JSON | `1` |
| JSON plus HTML | `2` |
| HTML | `3` |
| Light JSON | `4` |
