---
name: dataify-google-flights
description: When the user requests "calling Google Flights" or "searching for flight prices/itineraries", or explicitly mentions the flight query field, the dataify-google-flights skill is triggered.
---

# Dataify Google Flights

Use this skill to turn a user's Google Flights request into a Dataify Scraper API form POST.

## Required Pre-Call Confirmation

Before every real API call, follow this confirmation flow. These rules override any older workflow order in this skill.

1. Parse the user's request into the API body fields and fixed `engine` value.
2. Apply defaults only when the parameter description explicitly states a default. Do not use example YAML values, sample prompts, placeholder values, or examples such as `pizza`, `us`, `en`, dates, airport codes, or tokens as defaults.
3. If a required parameter has no documented default and cannot be inferred from the user request, ask for that parameter before building the table.
4. Show a Markdown table before calling the API. Do not include `Authorization`. Include the complete body field list from this skill's reference document, including `engine`, even when a field is currently blank.
5. The table must have exactly these columns: `参数名`, `当前值`, `默认值`, `说明`.
6. After the table, ask the user whether they want to modify any parameter. Do not call the API until the user explicitly confirms.
7. If the user changes a parameter, regenerate the table and ask for confirmation again.
8. If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.

Use the bundled preview helper whenever possible to generate the confirmation table from this skill's reference document:

```bash
python3 scripts/preview_params.py --params-json '{"q":"USER_QUERY"}'
```

Pass every parsed current value to `preview_params.py` using `--params-json` or matching `--field value` arguments. The helper reads defaults and descriptions from `references/*api.md`; if the helper cannot parse a default, leave the default blank rather than inventing one.
9. After confirmation and token handling, call the bundled Python script with `python3` and return the API response body directly without summarizing, extracting, cleaning, translating, or reshaping it.
## Workflow

1. Parse the user's request into Dataify Google Flights fields. Read `references/google_flights_api.md` for the full field list, accepted values, defaults, and conditional requirements.
2. Before every API call, run the script in dry-run Markdown mode and show the user the complete request parameter table. Then ask whether they want to modify anything. Do not call the API until the user confirms.
   - Do not show `Authorization`.
   - Show the complete documented body field list, not only fields present in the user request.
   - Use exactly these columns: `参数名`, `当前值`, `默认值`, `说明`.
   - For parameters whose description states a default value, use that default when the user did not specify a value.
   - Leave default value blank when the parameter description does not state a default.
   - Never use examples, placeholders, sample YAML values, or blank values as defaults.
3. If the token is missing, stop and tell the user to sign in at [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) to obtain `DATAIFY_API_TOKEN`.
4. Build request parameters with documented defaults only. The script submits these parameters as form data, not a JSON request body.
5. After the user confirms the table, run the bundled Python script with `python3`. Run it from this skill directory, or use the absolute path to `scripts/google_flights.py`.

```bash
python3 scripts/google_flights.py --params-json '{"departure_id":"JFK","arrival_id":"LAX","type":"2","outbound_date":"2026-06-01","currency":"USD","gl":"us","hl":"en"}' --dry-run --dry-run-format markdown
```

If the user confirms and provided a token in the conversation instead of an environment variable, pass it with `--token` and never echo it back:

```bash
python3 scripts/google_flights.py --token "USER_TOKEN" --params-json '{"departure_id":"JFK","arrival_id":"LAX","type":"2","outbound_date":"2026-06-01"}'
```

6. Return the script output directly to the user. Do not summarize, extract, clean, translate, or reshape the API response body.

## Mapping Rules

- Always submit the API request as form data with UTF-8 encoding and `Content-Type: application/x-www-form-urlencoded`.
- Always force `engine` to `google_flights`.
- Use `json: "1"` unless the user asks for another output format.
- Resolve relative dates from the conversation date, then pass dates as `YYYY-MM-DD`.
- Ask a follow-up when the user's route or requested continuation cannot be inferred safely. Do not require dates unless the user explicitly asks for a dated itinerary.
- If the user gives city names instead of airport codes and the airport is ambiguous, ask for the airport code or Google kgmid.
- Normalize token values in the script. A token without `Bearer ` is accepted and prefixed automatically.

Common mappings:

- "JSON" -> `json: "1"`
- "JSON+HTML" -> `json: "2"`
- "HTML" -> `json: "3"`
- "Light JSON" -> `json: "4"`
- one-way/single trip -> `type: "2"`
- round trip/return trip -> `type: "1"`
- multi-city -> `type: "3"` and `multi_city_json`
- economy/premium economy/business/first -> `travel_class: "1"`, `"2"`, `"3"`, `"4"`
- best/price/departure time/arrival time/duration/emissions sort -> `sort_by: "1"`, `"2"`, `"3"`, `"4"`, `"5"`, `"6"`
- any stops/nonstop/one stop or fewer/two stops or fewer -> `stops: "0"`, `"1"`, `"2"`, `"3"`
- bypass cache/no cache -> `no_cache: "true"`
- deep search -> `deep_search: "true"`


